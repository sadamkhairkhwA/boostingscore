import hashlib
import httpx
import json
import logging
import os
import random
import re
from datetime import timedelta
from urllib.parse import urlencode

from django.conf import settings
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from openai import AuthenticationError, OpenAI

from boostingscore.openai_key import resolve_openai_api_key

from .ielts_topic_ai import sync_tier_words_to_db
from .topic_words import TOPIC_WORDS
from .models import (
    CustomCard,
    CustomDeck,
    CustomDeckWord,
    TopicIELTSWordCache,
    TypeItAttempt,
    TypeItResult,
    VocabularyProgress,
    Word,
)
from .type_it_enrichment import (
    deck_title,
    enrich_word,
    ordered_words_for_deck,
    parse_deck_slug,
)
from .streak_utils import bump_streak_for_user

logger = logging.getLogger(__name__)


def _streak_ctx(request):
    streak = getattr(getattr(request.user, "profile", None), "streak", 0) or 0
    return {"streak": streak}


def _type_it_passes(mode: str, total: int) -> bool:
    m = (mode or TypeItAttempt.MODE_BOTH).strip()
    if m == TypeItAttempt.MODE_BOTH:
        return total >= 7
    if m in (TypeItAttempt.MODE_DEFINITION, TypeItAttempt.MODE_SENTENCE):
        return total >= 4
    return total >= 7


def _type_it_meta_from_attempts(attempts):
    """Return display meta for one word from its attempts (may be empty)."""
    if not attempts:
        return {"total": 0, "out_of": 10, "passed": False, "mode": None}
    passing = [a for a in attempts if _type_it_passes(getattr(a, "mode", None) or "both", a.total_score)]
    if passing:
        best = max(passing, key=lambda x: x.total_score)
        passed = True
    else:
        best = max(attempts, key=lambda x: x.total_score)
        passed = False
    m = getattr(best, "mode", None) or TypeItAttempt.MODE_BOTH
    out_of = 10 if m == TypeItAttempt.MODE_BOTH else 5
    return {"total": best.total_score, "out_of": out_of, "passed": passed, "mode": m}


def _type_it_word_bests_payload(user, words_payload):
    result = {
        w["item_id"]: {"total": 0, "out_of": 10, "passed": False, "mode": None} for w in words_payload
    }
    wids = [w["word_id"] for w in words_payload if w.get("word_id")]
    cwids = [w["custom_word_id"] for w in words_payload if w.get("custom_word_id")]
    if not wids and not cwids:
        return result
    q = None
    if wids:
        q = Q(word_id__in=wids)
    if cwids:
        q = Q(custom_word_id__in=cwids) if q is None else (q | Q(custom_word_id__in=cwids))
    qs = TypeItAttempt.objects.filter(student=user).filter(q)
    groups = {}
    for a in qs:
        if a.word_id:
            key = f"w-{a.word_id}"
        elif a.custom_word_id:
            key = f"cw-{a.custom_word_id}"
        else:
            continue
        groups.setdefault(key, []).append(a)
    for item_id, att_list in groups.items():
        if item_id in result:
            result[item_id] = _type_it_meta_from_attempts(att_list)
    return result


def _coerce_session_card_limit(raw, upper: int):
    """Max cards in this session; None means use the full deck (upper may be 0)."""
    if raw is None:
        return None
    s = str(raw).strip().lower()
    if s in ("", "all", "0", "none"):
        return None
    try:
        n = int(s)
    except ValueError:
        return None
    if n <= 0:
        return None
    return min(n, upper)


def _session_limit_option_values(word_count: int):
    """Preset sizes for session picker (always includes full deck count when > 0)."""
    if word_count <= 0:
        return []
    presets = [5, 10, 15, 20, 25, 30, 40, 50]
    out = [p for p in presets if p <= word_count]
    if word_count not in out:
        out.append(word_count)
    return sorted(set(out))


def _default_session_limit_str(word_count: int) -> str:
    if word_count <= 0:
        return ""
    if word_count >= 10:
        return "10"
    if word_count >= 5:
        return "5"
    return ""


def _next_review_delta(profile, hard: bool):
    from datetime import timedelta

    days = profile.review_hard_days if hard else profile.review_easy_days
    return timezone.now() + timedelta(days=days)


def _ensure_progress(user, word):
    prog, _ = VocabularyProgress.objects.get_or_create(
        student=user,
        word=word,
        defaults={"next_review": timezone.now()},
    )
    return prog


MASTERY_STAGE_LABEL = {
    1: "New",
    2: "Recognizing",
    3: "Learning",
    4: "Confident",
    5: "Mastered",
}


def _mastery_for_word_id(user, word_id):
    if not word_id:
        return 1
    try:
        return VocabularyProgress.objects.get(student=user, word_id=word_id).mastery_level
    except VocabularyProgress.DoesNotExist:
        return 1


def _word_card_from_model(user, w: Word) -> dict:
    return {
        "id": w.id,
        "word": w.word,
        "definition": w.definition,
        "example_sentence": w.example_sentence,
        "topic": w.topic,
        "topic_key": w.topic,
        "is_custom": False,
        "card_id": None,
        "part_of_speech": (w.part_of_speech or "word").strip() or "word",
        "phonetic": (w.phonetic or "").strip(),
        "level": w.level,
        "level_label": w.get_level_display(),
        "topic_label": w.get_topic_display(),
        "mastery_level": _mastery_for_word_id(user, w.id),
    }


def _word_quiz_deck_item(user, w: Word) -> dict:
    """Shape expected by static/js/quiz_runner.js (matches vocab index quiz deck items)."""
    c = _word_card_from_model(user, w)
    c["word_id"] = w.id
    c["example"] = (w.example_sentence or "").strip()
    c["synonyms"] = []
    c["times_marked_hard"] = 0
    return c


_QUIZ_METHOD_KEYS = frozenset({"mc", "truefalse", "fillblank", "match", "type", "listen"})


def _flashcard_query_url(hidden: dict, offset: int) -> str:
    q = {"offset": str(offset)}
    for key, val in hidden.items():
        if val:
            q[key] = val
    return f"{reverse('vocabulary:flashcard_deck')}?{urlencode(q)}"


def _apply_flashcard_rating(user, profile, word_id, card_id, rating: str) -> None:
    """Apply one Easy/Hard rating (Word progress or custom card streak)."""
    if rating not in ("easy", "hard"):
        raise ValueError("bad rating")
    hard = rating == "hard"
    wid = (str(word_id).strip() if word_id is not None else "") or ""
    cid = (str(card_id).strip() if card_id is not None else "") or ""
    if wid:
        word = get_object_or_404(Word, pk=wid)
        prog = _ensure_progress(user, word)
        if hard:
            prog.times_wrong += 1
            prog.mastery_level = max(1, prog.mastery_level - 1)
        else:
            prog.times_correct += 1
            prog.mastery_level = min(5, prog.mastery_level + 1)
            prog.easy_chip_master_count = min(3, (prog.easy_chip_master_count or 0) + 1)
        prog.last_reviewed = timezone.now()
        prog.next_review = _next_review_delta(profile, hard=hard)
        prog.status = "reviewing" if prog.mastery_level < 5 else "mastered"
        prog.save()
        bump_streak_for_user(user)
    elif cid:
        bump_streak_for_user(user)
    else:
        raise ValueError("no target")


@login_required
@require_POST
def flashcard_rate_api(request):
    """JSON: rate one card (typically Easy immediately)."""
    user = request.user
    profile = user.profile
    try:
        data = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "invalid json"}, status=400)
    rating = data.get("rating")
    word_id = data.get("word_id")
    card_id = data.get("card_id")
    try:
        _apply_flashcard_rating(user, profile, word_id, card_id, rating)
    except ValueError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=400)
    except Http404:
        return JsonResponse({"ok": False, "error": "not found"}, status=404)
    return JsonResponse({"ok": True})


@login_required
@require_POST
def flashcard_save_pending_api(request):
    """Apply queued Hard ratings (saved when user clicks Save progress)."""
    user = request.user
    profile = user.profile
    try:
        data = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "invalid json"}, status=400)
    items = data.get("items") or []
    if not isinstance(items, list):
        return JsonResponse({"ok": False, "error": "items must be a list"}, status=400)
    applied = 0
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            _apply_flashcard_rating(
                user,
                profile,
                item.get("word_id"),
                item.get("card_id"),
                "hard",
            )
            applied += 1
        except ValueError:
            continue
        except Http404:
            continue
    return JsonResponse({"ok": True, "applied": applied})


def _flashcard_session_api_urls():
    return {
        "flashcard_rate_url": reverse("vocabulary:flashcard_rate"),
        "flashcard_save_pending_url": reverse("vocabulary:flashcard_save_pending"),
    }


@login_required
def deck_create(request):
    """Create a custom flashcard deck (name + cards + optional AI generation)."""
    user = request.user
    streak = getattr(getattr(user, "profile", None), "streak", 0) or 0
    profile = user.profile
    topic_choices = list(Word.TOPIC_CHOICES) + [("other", "Personal vocabulary")]
    return render(
        request,
        "vocabulary/deck_create.html",
        {
            "streak": streak,
            "topic_choices": topic_choices,
            "user_vocab_level": int(profile.level),
            "initial_topic": "environment",
            "max_cards": 30,
            **_streak_ctx(request),
        },
    )


@login_required
@require_POST
def deck_create_save(request):
    """JSON: create CustomDeck + CustomCards; optional redirect to study session."""
    try:
        data = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)
    name = (data.get("name") or "").strip()
    if not name:
        return JsonResponse({"ok": False, "error": "Deck name is required."}, status=400)
    description = (data.get("description") or "").strip()
    cards_in = data.get("cards") or []
    if not isinstance(cards_in, list) or len(cards_in) == 0:
        return JsonResponse({"ok": False, "error": "Add at least one card."}, status=400)

    deck = CustomDeck.objects.create(
        student=request.user,
        name=name[:100],
        description=description[:4000] if description else "",
    )
    n = 0
    for c in cards_in:
        if not isinstance(c, dict):
            continue
        w = (c.get("word") or "").strip()
        d = (c.get("definition") or "").strip()
        if not w or not d:
            continue
        ex = (c.get("example_sentence") or "").strip()
        CustomCard.objects.create(
            student=request.user,
            deck=deck,
            word=w[:200],
            definition=d,
            example_sentence=ex[:2000],
        )
        n += 1
    if n == 0:
        deck.delete()
        return JsonResponse({"ok": False, "error": "No valid cards to save."}, status=400)

    q = urlencode({"deck_id": deck.pk})
    redirect_url = f"{reverse('vocabulary:flashcard_deck')}?{q}"
    return JsonResponse({"ok": True, "deck_id": deck.pk, "redirect_url": redirect_url})


@login_required
@require_POST
def flashcard_set_generate(request):
    """AI: generate flashcard rows from a free-form prompt (JSON cards list)."""
    if not settings.OPENAI_API_KEY:
        return JsonResponse({"ok": False, "error": "OpenAI API key is not configured."}, status=503)
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)
    prompt = (payload.get("prompt") or "").strip()
    if not prompt:
        return JsonResponse({"ok": False, "error": "Enter a prompt."}, status=400)
    try:
        count = int(payload.get("count") or 10)
    except (TypeError, ValueError):
        count = 10
    count = max(1, min(30, count))
    try:
        level = int(payload.get("level") or 2)
    except (TypeError, ValueError):
        level = 2
    level = max(1, min(3, level))
    topic = (payload.get("topic") or "environment").strip()
    valid_topics = {k for k, _ in Word.TOPIC_CHOICES} | {"other"}
    if topic not in valid_topics:
        topic = "environment"
    topic_label = (
        "Personal / mixed"
        if topic == "other"
        else _topic_label(topic)
    )
    band = _band_for_level(level)

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    system_msg = "You are an IELTS vocabulary expert. Return only valid JSON."
    user_msg = (
        f"User request:\n{prompt}\n\n"
        f"Topic context: {topic_label}\n"
        f"Difficulty band: {band}\n\n"
        f"Generate exactly {count} vocabulary flashcards.\n"
        'Return JSON with this exact shape:\n'
        '{"cards": [\n'
        '  {"word": string, "definition": string, "example_sentence": string}\n'
        "]}\n"
        "Rules: short definitions; one IELTS-style example sentence per word; no duplicates."
    )
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.5,
        )
        raw = completion.choices[0].message.content or ""
    except Exception as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=502)

    parsed = _extract_json_object(raw)
    if not isinstance(parsed, dict):
        return JsonResponse({"ok": False, "error": "Could not parse AI response."}, status=502)
    cards_raw = parsed.get("cards")
    if not isinstance(cards_raw, list):
        return JsonResponse({"ok": False, "error": "Invalid AI response shape."}, status=502)
    cards_out = []
    for item in cards_raw[:count]:
        if not isinstance(item, dict):
            continue
        w = (item.get("word") or "").strip()
        d = (item.get("definition") or "").strip()
        if not w or not d:
            continue
        ex = (item.get("example_sentence") or "").strip()
        cards_out.append(
            {
                "word": w[:200],
                "definition": d,
                "example_sentence": ex[:2000],
            }
        )
    if not cards_out:
        return JsonResponse({"ok": False, "error": "No cards in AI response."}, status=502)
    return JsonResponse({"ok": True, "cards": cards_out})


@login_required
@require_POST
def custom_ai_image_preview(request):
    """Placeholder for per-card illustration generation (optional)."""
    return JsonResponse(
        {
            "ok": False,
            "error": "AI illustrations are not available in this build. Save your deck without images.",
        },
        status=501,
    )


@login_required
def vocabulary_home(request):
    user = request.user
    streak = getattr(getattr(user, "profile", None), "streak", 0) or 0
    words_learned = due_count = mastered_count = mastered_pct = 0
    continue_href = ""
    continue_pct = 0
    try:
        now = timezone.now()
        all_prog = VocabularyProgress.objects.filter(student=user)
        words_learned = all_prog.count()
        mastered_count = all_prog.filter(mastery_level=5).count()
        mastered_pct = round(mastered_count / words_learned * 100) if words_learned else 0
        due_qs = all_prog.filter(next_review__lte=now).select_related("word")
        due_count = due_qs.count()
        first = due_qs.first()
        if first:
            params = {"mode": "due", "limit": "12"}
            continue_href = f"{reverse('vocabulary:flashcard_deck')}?{urlencode(params)}"
            continue_pct = min(100, int(round((words_learned - due_count) / max(words_learned, 1) * 100)))
        else:
            params = {"topic": "environment", "level": "1"}
            continue_href = reverse("vocabulary:flashcard_topic", kwargs={"topic": "environment"})
            continue_pct = mastered_pct
    except Exception:
        continue_href = reverse("vocabulary:index")
        continue_pct = 0

    method_stats = {
        "flashcard": words_learned,
        "quiz": min(words_learned, 40),
        "type_it": TypeItResult.objects.filter(student=user).count(),
    }

    return render(
        request,
        "vocabulary/vocabulary_home.html",
        {
            "streak": streak,
            "words_learned": words_learned,
            "due_count": due_count,
            "mastered_count": mastered_count,
            "mastered_pct": mastered_pct,
            "continue_href": continue_href,
            "continue_pct": continue_pct,
            "method_stats": method_stats,
            **_streak_ctx(request),
        },
    )


_FLASHCARD_TOPIC_ICONS = {
    "environment": "🌿",
    "health": "🩺",
    "technology": "💻",
    "education": "🎓",
    "society": "🏛️",
    "travel": "✈️",
    "science": "🔬",
    "business": "💼",
}


@login_required
def flashcard_deck(request):
    user = request.user
    streak = getattr(getattr(user, "profile", None), "streak", 0) or 0
    now = timezone.now()
    due_count = VocabularyProgress.objects.filter(student=user, next_review__lte=now).count()
    topic_counts = {
        row["topic"]: row["n"]
        for row in Word.objects.values("topic").annotate(n=Count("id"))
    }
    topic_rows = [
        {
            "key": k,
            "label": label,
            "count": topic_counts.get(k, 0),
            "icon": _FLASHCARD_TOPIC_ICONS.get(k, "📇"),
        }
        for k, label in Word.TOPIC_CHOICES
    ]
    custom_decks = (
        CustomDeck.objects.filter(student=user)
        .annotate(card_count=Count("customcard"))
        .order_by("-created_at")[:20]
    )
    for d in custom_decks:
        n = d.card_count or 0
        d.session_limit_options = _session_limit_option_values(n)
        d.default_session_limit = _default_session_limit_str(n)
    return render(
        request,
        "vocabulary/flashcard_deck.html",
        {
            "streak": streak,
            "due_count": due_count,
            "due_limit_options": _session_limit_option_values(due_count),
            "due_default_limit": _default_session_limit_str(due_count),
            "topic_rows": topic_rows,
            "custom_decks": custom_decks,
            **_streak_ctx(request),
        },
    )


def _topic_label(topic_key: str) -> str:
    for k, v in Word.TOPIC_CHOICES:
        if k == topic_key:
            return v
    return topic_key


def _band_for_level(level: int) -> str:
    return {1: "IELTS Band 4–5", 2: "IELTS Band 5.5–6.5", 3: "IELTS Band 7–9"}.get(level, "IELTS Band 4–5")


_TOPIC_LEVEL_BLURBS = {
    1: (
        "Simple everyday vocabulary for this topic — common nouns, verbs, and phrases "
        "a Band 5 learner would recognise and use."
    ),
    2: (
        "IELTS-ready vocabulary — collocations, academic phrases, and topic-specific "
        "expressions for Writing Task 2 and Speaking (Band 6–7)."
    ),
    3: (
        "Band 7+ vocabulary — nuanced terms, sophisticated collocations, and precise "
        "academic language."
    ),
}


def _chip_mastered_from_prog(prog):
    if not prog:
        return False
    return (prog.easy_chip_master_count or 0) >= 3


def _topic_word_goals(topic: str) -> dict[int, int]:
    tw = TOPIC_WORDS.get(topic)
    if not tw:
        return {1: 65, 2: 68, 3: 62}
    return {
        1: len(tw["beginner"]),
        2: len(tw["standard"]),
        3: len(tw["advanced"]),
    }


def _topic_hub_levels_payload(user, topic: str):
    goals = _topic_word_goals(topic)
    titles = {1: "Beginner", 2: "Standard", 3: "Advanced"}
    pack = TopicIELTSWordCache.objects.filter(
        topic=topic, status=TopicIELTSWordCache.STATUS_READY
    ).first()
    out = {}
    for lvl in (1, 2, 3):
        base = (
            Word.objects.filter(topic=topic, topic_pack=pack)
            if pack
            else Word.objects.none()
        )
        wlist = list(base.filter(level=lvl).order_by("word"))
        wids = [w.id for w in wlist]
        pmap = {
            p.word_id: p
            for p in VocabularyProgress.objects.filter(student=user, word_id__in=wids)
        }
        words_payload = []
        mastered_n = 0
        for w in wlist:
            p = pmap.get(w.id)
            m = _chip_mastered_from_prog(p)
            if m:
                mastered_n += 1
            words_payload.append({"id": w.id, "text": w.word, "mastered": m})
        out[str(lvl)] = {
            "level": lvl,
            "title": titles[lvl],
            "description": _TOPIC_LEVEL_BLURBS[lvl],
            "word_goal": goals[lvl],
            "word_count": len(words_payload),
            "mastered_in_level": mastered_n,
            "words": words_payload,
        }
    return out


def _ensure_topic_ielts_words(user, topic: str, *, force: bool = False):
    """Populate TopicIELTSWordCache + Word rows from ``TOPIC_WORDS``; return status dict."""
    _ = user  # reserved for future per-user behaviour
    tiers = TOPIC_WORDS.get(topic)
    if not tiers:
        return {
            "ok": False,
            "status": TopicIELTSWordCache.STATUS_ERROR,
            "message": "Unknown topic",
            "error_code": "bad_topic",
        }

    if force:
        TopicIELTSWordCache.objects.filter(topic=topic).delete()
        Word.objects.filter(topic=topic, topic_pack__isnull=True).delete()

    obj, _ = TopicIELTSWordCache.objects.update_or_create(
        topic=topic,
        defaults={
            "status": TopicIELTSWordCache.STATUS_READY,
            "error_message": "",
            "beginner": list(tiers["beginner"]),
            "standard": list(tiers["standard"]),
            "advanced": list(tiers["advanced"]),
        },
    )
    sync_tier_words_to_db(topic, tiers, obj)
    allowed = {w.strip().lower() for ws in tiers.values() for w in ws if (w or "").strip()}
    for w in Word.objects.filter(topic_pack=obj):
        if w.word.strip().lower() not in allowed:
            w.delete()
    return {"ok": True, "status": TopicIELTSWordCache.STATUS_READY}


@login_required
def api_topic_ielts(request, topic: str):
    valid = {k for k, _ in Word.TOPIC_CHOICES}
    if topic not in valid:
        return JsonResponse({"ok": False, "error": "bad_topic"}, status=400)
    force = request.GET.get("force") == "1"
    ensure = _ensure_topic_ielts_words(request.user, topic, force=force)
    if ensure.get("status") == TopicIELTSWordCache.STATUS_GENERATING:
        return JsonResponse(ensure)
    if not ensure.get("ok"):
        return JsonResponse(ensure, status=503)

    levels = _topic_hub_levels_payload(request.user, topic)
    total = sum(len(levels[str(i)]["words"]) for i in (1, 2, 3))
    mastered_total = sum(
        1 for i in (1, 2, 3) for w in levels[str(i)]["words"] if w.get("mastered")
    )
    pct = round(100 * mastered_total / total) if total else 0
    return JsonResponse(
        {
            "ok": True,
            "status": TopicIELTSWordCache.STATUS_READY,
            "topic": topic,
            "topic_label": _topic_label(topic),
            "total_words": total,
            "mastered_total": mastered_total,
            "overall_pct": pct,
            "levels": levels,
        }
    )


@login_required
def flashcard_topic(request, topic: str):
    valid = {k for k, _ in Word.TOPIC_CHOICES}
    if topic not in valid:
        raise Http404("Unknown topic")
    streak = getattr(getattr(request.user, "profile", None), "streak", 0) or 0
    return render(
        request,
        "vocabulary/topic_ielts_hub.html",
        {
            "streak": streak,
            "topic": topic,
            "topic_label": _topic_label(topic),
            "api_url": reverse("vocabulary:api_topic_ielts", kwargs={"topic": topic}),
            "flashcard_session_url": reverse("vocabulary:flashcard_deck"),
            **_streak_ctx(request),
        },
    )


@login_required
@require_POST
def generate_ielts_vocab_api(request):
    if not settings.OPENAI_API_KEY:
        return JsonResponse({"ok": False, "error": "OpenAI API key is not configured."}, status=503)
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON body."}, status=400)

    topic = (payload.get("topic") or "").strip()
    level_raw = payload.get("level")
    valid_topics = {k for k, _ in Word.TOPIC_CHOICES}
    if topic not in valid_topics:
        return JsonResponse({"ok": False, "error": "Invalid topic."}, status=400)
    try:
        level = int(level_raw)
    except (TypeError, ValueError):
        return JsonResponse({"ok": False, "error": "Invalid level."}, status=400)
    if level not in (1, 2, 3):
        return JsonResponse({"ok": False, "error": "Level must be 1, 2, or 3."}, status=400)

    topic_label = _topic_label(topic)
    band = _band_for_level(level)

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    system_msg = "You are an IELTS Academic vocabulary expert. Return only valid JSON."
    user_msg = (
        f'Topic area: {topic_label}\n'
        f"Target difficulty: {band}\n\n"
        "Return JSON with this exact shape:\n"
        '{"words": [\n'
        '  {"word": string, "definition": string, "example_sentence": string, '
        '"collocations": [string], "part_of_speech": string, "phonetic": string}\n'
        "]}\n\n"
        "Rules:\n"
        "- Generate exactly 12 words.\n"
        "- Words must be useful for IELTS Writing Task 2 and Academic Reading.\n"
        "- Collocations: 2–4 natural phrases per word.\n"
        "- Example sentences: one clear IELTS-style sentence each.\n"
        "- No duplicate words in the list.\n"
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.45,
            max_tokens=3500,
        )
        raw = completion.choices[0].message.content or ""
    except Exception as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=502)

    data = _extract_json_object(raw)
    if not isinstance(data, dict):
        return JsonResponse({"ok": False, "error": "Could not parse AI response."}, status=502)

    words = data.get("words")
    if not isinstance(words, list):
        return JsonResponse({"ok": False, "error": "Invalid words array."}, status=502)

    created = 0
    skipped = 0
    for item in words:
        if not isinstance(item, dict):
            skipped += 1
            continue
        w = (item.get("word") or "").strip()
        if not w:
            skipped += 1
            continue
        definition = (item.get("definition") or "").strip() or "—"
        example = (item.get("example_sentence") or "").strip() or "—"
        collocs = item.get("collocations")
        if not isinstance(collocs, list):
            collocs = []
        collocs = [str(x).strip() for x in collocs if str(x).strip()][:12]
        pos = (item.get("part_of_speech") or "").strip()
        phon = (item.get("phonetic") or "").strip()

        exists = Word.objects.filter(topic=topic, level=level, word__iexact=w).exists()
        if exists:
            skipped += 1
            continue
        Word.objects.create(
            word=w[:100],
            topic=topic,
            level=level,
            definition=definition,
            example_sentence=example,
            collocations=collocs,
            part_of_speech=pos[:50],
            phonetic=phon[:100],
        )
        created += 1

    return JsonResponse(
        {
            "ok": True,
            "created": created,
            "skipped": skipped,
        }
    )


@login_required
def flashcard_session(request):
    user = request.user
    streak = getattr(getattr(user, "profile", None), "streak", 0) or 0
    profile = user.profile

    if request.method == "POST":
        word_id = request.POST.get("word_id")
        card_id = request.POST.get("card_id")
        rating = request.POST.get("rating")
        topic = request.POST.get("topic") or ""
        level = request.POST.get("level") or ""
        mode = request.POST.get("mode") or ""
        deck_id = request.POST.get("deck_id") or ""
        offset = int(request.POST.get("offset") or "0")
        limit_post = (request.POST.get("limit") or "").strip()
        words_post = (request.POST.get("words") or "").strip()

        if rating in ("easy", "hard"):
            try:
                _apply_flashcard_rating(user, profile, word_id, card_id, rating)
            except ValueError:
                pass

        offset = offset + 1
        q = {"offset": str(offset)}
        if topic:
            q["topic"] = topic
        if level:
            q["level"] = level
        if mode:
            q["mode"] = mode
        if deck_id:
            q["deck_id"] = deck_id
        if limit_post:
            q["limit"] = limit_post
        if words_post:
            q["words"] = words_post
        return redirect(f"{reverse('vocabulary:flashcard_deck')}?{urlencode(q)}")

    topic = request.GET.get("topic")
    level = request.GET.get("level")
    mode = request.GET.get("mode")
    deck_id = request.GET.get("deck_id")
    words_q = (request.GET.get("words") or "").strip()
    selected_word_ids = []
    if words_q:
        seen = set()
        for raw in words_q.split(","):
            raw = raw.strip()
            if not raw:
                continue
            try:
                wid = int(raw)
            except ValueError:
                continue
            if wid not in seen:
                seen.add(wid)
                selected_word_ids.append(wid)

    words = []
    if deck_id:
        deck = get_object_or_404(CustomDeck, pk=deck_id, student=user)
        cards = list(CustomCard.objects.filter(deck=deck).order_by("id"))
        for c in cards:
            words.append(
                {
                    "id": None,
                    "word": c.word,
                    "definition": c.definition,
                    "example_sentence": c.example_sentence,
                    "topic": "custom",
                    "is_custom": True,
                    "card_id": c.id,
                    "part_of_speech": "phrase",
                    "phonetic": "",
                    "level": 1,
                    "level_label": "Custom",
                    "topic_label": "Custom deck",
                    "topic_key": "custom",
                    "mastery_level": 1,
                }
            )
    elif mode == "due":
        now = timezone.now()
        due = (
            VocabularyProgress.objects.filter(student=user, next_review__lte=now)
            .select_related("word")
            .order_by("next_review")
        )
        for p in due:
            card = _word_card_from_model(user, p.word)
            card["mastery_level"] = p.mastery_level
            words.append(card)
    else:
        qs = Word.objects.all()
        if topic:
            qs = qs.filter(topic=topic)
            pack = TopicIELTSWordCache.objects.filter(
                topic=topic, status=TopicIELTSWordCache.STATUS_READY
            ).first()
            if pack:
                qs = qs.filter(topic_pack=pack)
        if level:
            qs = qs.filter(level=int(level))
        qs = qs.order_by("topic", "word")
        words = [_word_card_from_model(user, w) for w in qs]

    if request.GET.get("shuffle") == "1" and words:
        random.shuffle(words)
    initial_shuffle = request.GET.get("shuffle") == "1"

    if selected_word_ids:
        selected_set = set(selected_word_ids)
        words = [w for w in words if w.get("id") in selected_set]
        order_map = {wid: i for i, wid in enumerate(selected_word_ids)}
        words.sort(key=lambda w: order_map.get(w.get("id"), 10**9))

    full_deck_total = len(words)
    limit_requested = _coerce_session_card_limit(request.GET.get("limit"), full_deck_total)
    if limit_requested is not None:
        words = words[:limit_requested]

    hidden = {}
    if topic:
        hidden["topic"] = topic
    if level:
        hidden["level"] = level
    if mode:
        hidden["mode"] = mode
    if deck_id:
        hidden["deck_id"] = deck_id
    if selected_word_ids:
        hidden["words"] = ",".join(str(wid) for wid in selected_word_ids)
    if limit_requested is not None:
        hidden["limit"] = str(limit_requested)

    total = len(words)
    if total == 0:
        topic_href = ""
        if topic:
            try:
                topic_href = reverse("vocabulary:flashcard_topic", kwargs={"topic": topic})
            except Exception:
                topic_href = ""
        return render(
            request,
            "vocabulary/flashcard_session.html",
            {
                "streak": streak,
                "empty": True,
                "done": False,
                "deck_words": [],
                "current": None,
                "offset": 0,
                "total": 0,
                "progress_pct": 0,
                "hidden_fields": hidden,
                "querystring": "",
                "topic_for_empty": topic or "",
                "topic_href": topic_href,
                **_streak_ctx(request),
            },
        )

    limit_key = str(limit_requested) if limit_requested is not None else "all"
    stat_storage_key = hashlib.sha256(
        f"{topic}_{level}_{mode}_{deck_id}_{','.join(map(str, selected_word_ids))}_{full_deck_total}_{limit_key}_{initial_shuffle}".encode(
            "utf-8"
        )
    ).hexdigest()[:20]
    study_q = {k: v for k, v in hidden.items() if v}
    study_again_url = f"{reverse('vocabulary:flashcard_deck')}?{urlencode(study_q)}"

    return render(
        request,
        "vocabulary/flashcard_session.html",
        {
            "streak": streak,
            "empty": False,
            "done": False,
            "deck_words": words,
            "total": total,
            "progress_pct": 0,
            "hidden_fields": hidden,
            "hidden_fields_json": json.dumps(hidden),
            "stat_storage_key": stat_storage_key,
            "initial_shuffle": initial_shuffle,
            "mastery_labels": MASTERY_STAGE_LABEL,
            "study_again_url": study_again_url,
            **_flashcard_session_api_urls(),
            **_streak_ctx(request),
        },
    )


@login_required
def word_list(request):
    user = request.user
    streak = getattr(getattr(user, "profile", None), "streak", 0) or 0

    if request.method == "POST":
        action = request.POST.get("action")
        wid = request.POST.get("word_id")
        if action == "toggle_favorite" and wid:
            word = get_object_or_404(Word, pk=wid)
            prog, _ = VocabularyProgress.objects.get_or_create(
                student=user,
                word=word,
                defaults={"next_review": timezone.now()},
            )
            prog.is_favored = not prog.is_favored
            prog.save()

    topic = request.GET.get("topic") or ""
    level = request.GET.get("level") or ""

    qs = Word.objects.all().order_by("topic", "word")
    if topic:
        qs = qs.filter(topic=topic)
    if level:
        qs = qs.filter(level=int(level))

    rows = []
    for w in qs:
        prog = None
        try:
            prog = VocabularyProgress.objects.get(student=user, word=w)
        except VocabularyProgress.DoesNotExist:
            pass
        rows.append(
            {
                "word": w,
                "progress": prog,
                "mastery": prog.mastery_level if prog else 0,
                "favored": prog.is_favored if prog else False,
            }
        )

    return render(
        request,
        "vocabulary/word_list.html",
        {
            "streak": streak,
            "rows": rows,
            "topics": Word.TOPIC_CHOICES,
            "levels": Word.LEVEL_CHOICES,
            "filter_topic": topic,
            "filter_level": level,
            **_streak_ctx(request),
        },
    )


@login_required
def quiz_topic_words_api(request, topic: str):
    valid = {k for k, _ in Word.TOPIC_CHOICES}
    if topic not in valid:
        raise Http404("Unknown topic")
    words = list(Word.objects.filter(topic=topic).order_by("word").values("id", "word"))
    return JsonResponse({"words": words})


@login_required
def quiz_session(request):
    """Run interactive quiz (MC, T/F, etc.) from query params produced by quiz setup."""
    user = request.user
    raw_ids = request.GET.get("words") or ""
    topic_key = (request.GET.get("topic") or "").strip()
    method_raw = (request.GET.get("quiz_types") or "mc").strip().lower().split(",")[0].strip()
    limit_raw = (request.GET.get("quiz_limit") or "all").strip().lower()

    id_parts = [x.strip() for x in raw_ids.split(",") if x.strip().isdigit()]
    ids = [int(x) for x in id_parts][:800]
    if len(ids) < 3:
        return redirect(f"{reverse('vocabulary:quiz_setup')}?error=minwords")

    qs = Word.objects.filter(pk__in=ids)
    if topic_key:
        valid_topics = {k for k, _ in Word.TOPIC_CHOICES}
        if topic_key in valid_topics:
            qs = qs.filter(topic=topic_key)
    by_id = {w.id: w for w in qs}
    ordered_models = [by_id[i] for i in ids if i in by_id]
    if len(ordered_models) < 3:
        return redirect(f"{reverse('vocabulary:quiz_setup')}?error=minwords")

    deck = [_word_quiz_deck_item(user, w) for w in ordered_models]
    random.shuffle(deck)
    if limit_raw in ("5", "10", "20"):
        n = int(limit_raw)
        deck = deck[: min(n, len(deck))]

    quiz_method = method_raw if method_raw in _QUIZ_METHOD_KEYS else "mc"
    topic_label = _topic_label(topic_key) if topic_key else "Mixed"

    quiz_config = {
        "deck": deck,
        "quizMethod": quiz_method,
        "topicLabel": topic_label,
        "setupUrl": reverse("vocabulary:quiz_setup"),
    }
    streak = getattr(getattr(user, "profile", None), "streak", 0) or 0
    return render(
        request,
        "vocabulary/quiz_session.html",
        {
            "streak": streak,
            "quiz_config": quiz_config,
            **_streak_ctx(request),
        },
    )


@login_required
def quiz_setup(request):
    streak = getattr(getattr(request.user, "profile", None), "streak", 0) or 0
    quiz_topic_words_url = reverse(
        "vocabulary:quiz_topic_words", kwargs={"topic": "__topic__"}
    )
    return render(
        request,
        "vocabulary/quiz_setup.html",
        {
            "streak": streak,
            "topics": Word.TOPIC_CHOICES,
            "quiz_topic_words_url": quiz_topic_words_url,
            "quiz_session_url": reverse("vocabulary:quiz_session"),
            **_streak_ctx(request),
        },
    )


TYPE_IT_TOPIC_EMOJI = {
    "environment": "🌿",
    "health": "🩺",
    "technology": "💻",
    "education": "📚",
    "society": "🏙️",
    "travel": "✈️",
    "science": "🔬",
    "business": "💼",
}
TYPE_IT_LEVEL_SLUG = {1: "beginner", 2: "standard", 3: "advanced"}
TYPE_IT_LEVEL_CARD = {
    1: {
        "tier_title": "Easy",
        "icon_emoji": "📗",
        "ielts": "Beginner",
        "desc": (
            "Core everyday vocabulary — simple definitions and common phrases."
        ),
        "badge": "easy",
    },
    2: {
        "tier_title": "Medium",
        "icon_emoji": "📘",
        "ielts": "Standard",
        "desc": (
            "IELTS-ready vocabulary — collocations, academic phrases, "
            "and topic-specific expressions."
        ),
        "badge": "medium",
    },
    3: {
        "tier_title": "Hard",
        "icon_emoji": "📙",
        "ielts": "Advanced",
        "desc": (
            "Band 7+ vocabulary — complex academic language and sophisticated collocations."
        ),
        "badge": "hard",
    },
}


def _type_it_level_progress(user, topic_key: str, level: int):
    words = list(Word.objects.filter(topic=topic_key, level=level).order_by("word"))
    total = len(words)
    if not total:
        return 0, 0, 0
    wids = [w.id for w in words]
    passed_map = {wid: False for wid in wids}
    for a in TypeItAttempt.objects.filter(student=user, word_id__in=wids).only(
        "word_id", "total_score", "mode"
    ):
        if a.word_id and _type_it_passes(getattr(a, "mode", None) or "both", a.total_score):
            passed_map[a.word_id] = True
    done = sum(1 for v in passed_map.values() if v)
    pct = int(round((100 * done) / total)) if total else 0
    return total, done, pct


@login_required
def type_it_deck(request):
    user = request.user
    streak = getattr(getattr(user, "profile", None), "streak", 0) or 0
    type_it_topics = []
    for topic_key, topic_label in Word.TOPIC_CHOICES:
        levels_payload = []
        topic_total = 0
        topic_done = 0
        for lvl, _lvl_label in Word.LEVEL_CHOICES:
            meta = TYPE_IT_LEVEL_CARD.get(int(lvl))
            slug = TYPE_IT_LEVEL_SLUG.get(int(lvl))
            if not meta or not slug:
                continue
            total, done, pct = _type_it_level_progress(user, topic_key, int(lvl))
            topic_total += total
            topic_done += done
            words_url = reverse(
                "vocabulary:type_it_words_topic_level",
                kwargs={"topic": topic_key, "level_slug": slug},
            )
            levels_payload.append(
                {
                    "slug": slug,
                    "tier_title": meta["tier_title"],
                    "icon_emoji": meta["icon_emoji"],
                    "ielts": meta["ielts"],
                    "desc": meta["desc"],
                    "badge": meta["badge"],
                    "count": total,
                    "done": done,
                    "pct": pct,
                    "words_url": words_url,
                }
            )
        topic_pct = int(round((100 * topic_done) / topic_total)) if topic_total else 0
        type_it_topics.append(
            {
                "topic": topic_key,
                "name": topic_label,
                "emoji": TYPE_IT_TOPIC_EMOJI.get(topic_key, "📖"),
                "total_words": topic_total,
                "done": topic_done,
                "pct": topic_pct,
                "levels": levels_payload,
            }
        )

    custom = []
    for d in CustomDeck.objects.filter(student=user).order_by("-created_at"):
        cwords = list(d.words.all().order_by("id"))
        cids = [w.id for w in cwords]
        passed_map = {cid: False for cid in cids}
        for a in TypeItAttempt.objects.filter(student=user, custom_word_id__in=cids).only(
            "custom_word_id", "total_score", "mode"
        ):
            if a.custom_word_id and _type_it_passes(getattr(a, "mode", None) or "both", a.total_score):
                passed_map[a.custom_word_id] = True
        done = sum(1 for v in passed_map.values() if v)
        total = len(cwords)
        custom.append(
            {
                "id": f"custom-{d.id}",
                "emoji": d.emoji or "📖",
                "name": d.name,
                "colour": d.colour or "navy",
                "count": total,
                "done": done,
                "pct": int(round((100 * done) / total)) if total else 0,
                "url": reverse("vocabulary:type_it_words", kwargs={"deck_id": f"custom-{d.id}"}),
            }
        )

    return render(
        request,
        "vocabulary/type_it_deck.html",
        {
            "streak": streak,
            "type_it_topics": type_it_topics,
            "custom_decks": custom,
            "create_url": reverse("vocabulary:type_it_custom_deck_create"),
            **_streak_ctx(request),
        },
    )


@login_required
def type_it_session(request):
    user = request.user
    streak = getattr(getattr(user, "profile", None), "streak", 0) or 0

    topic = request.GET.get("topic")
    level = request.GET.get("level")
    word_id = request.GET.get("word_id")

    word_obj = None
    if word_id:
        word_obj = get_object_or_404(Word, pk=word_id)
    else:
        qs = Word.objects.all()
        if topic:
            qs = qs.filter(topic=topic)
        if level:
            qs = qs.filter(level=int(level))
        word_obj = qs.order_by("?").first()

    return render(
        request,
        "vocabulary/type_it_session.html",
        {
            "streak": streak,
            "word_obj": word_obj,
            "topic": topic or "",
            "level": level or "",
            **_streak_ctx(request),
        },
    )


@login_required
def favored(request):
    user = request.user
    streak = getattr(getattr(user, "profile", None), "streak", 0) or 0
    qs = (
        VocabularyProgress.objects.filter(student=user, is_favored=True)
        .select_related("word")
        .order_by("-last_reviewed")
    )
    return render(
        request,
        "vocabulary/favored.html",
        {
            "streak": streak,
            "items": qs,
            **_streak_ctx(request),
        },
    )


@login_required
def vocabulary_guide(request):
    streak = getattr(getattr(request.user, "profile", None), "streak", 0) or 0
    return render(
        request,
        "vocabulary/guide.html",
        {
            "streak": streak,
            **_streak_ctx(request),
        },
    )


def _extract_json_object(text: str):
    """Parse first JSON object from model text; tolerate ```json fences."""
    text = (text or "").strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines and lines[0].lstrip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    if text.startswith("{") and text.endswith("}"):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
    m = re.search(r"\{[\s\S]*\}", text)
    if not m:
        return None
    try:
        return json.loads(m.group())
    except json.JSONDecodeError:
        return None


@login_required
@require_POST
def type_it_check_api(request):
    if not settings.OPENAI_API_KEY:
        return JsonResponse({"ok": False, "error": "OpenAI API key is not configured."}, status=503)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON body."}, status=400)

    word_text = (payload.get("word") or "").strip()
    student_text = (payload.get("student_text") or "").strip()
    word_id = payload.get("word_id")

    if not word_text or not student_text:
        return JsonResponse({"ok": False, "error": "word and student_text are required."}, status=400)

    profile = request.user.profile
    level_label = profile.level_label

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    system_msg = "You are an IELTS examiner scoring student sentences. Return only valid JSON."
    user_msg = (
        f"Student level: {level_label}\n"
        f"Word to use: {word_text}\n"
        f"Student sentence: {student_text}\n\n"
        "Return JSON: {band: float 1-9, title: string, subtitle: string, improved: string, "
        "strengths: [strings], improvements: [strings], errors: [strings], ielts_tip: string, "
        "understanding_check: string}"
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.3,
        )
        raw = completion.choices[0].message.content or ""
    except Exception as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=502)

    data = _extract_json_object(raw)
    if not isinstance(data, dict):
        return JsonResponse({"ok": False, "error": "Could not parse model response."}, status=502)

    band = data.get("band")
    try:
        band_f = float(band) if band is not None else None
    except (TypeError, ValueError):
        band_f = None

    word_obj = None
    if word_id:
        try:
            word_obj = Word.objects.get(pk=int(word_id))
        except (Word.DoesNotExist, ValueError, TypeError):
            word_obj = None

    TypeItResult.objects.create(
        student=request.user,
        word=word_obj,
        student_text=student_text,
        mode="word",
        band_score=band_f,
        improved_text=str(data.get("improved") or ""),
        ielts_mode=True,
    )
    bump_streak_for_user(request.user)

    return JsonResponse({"ok": True, "result": data})


@login_required
def type_it_practice(request, deck_id: str):
    # Backward-compatible alias to new words selector URL.
    return redirect("vocabulary:type_it_words", deck_id=deck_id)


@login_required
@require_POST
def type_it_feedback(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON body."}, status=400)

    item_id = (payload.get("item_id") or "").strip()
    word_id = payload.get("word_id")
    deck_slug = (payload.get("deck_slug") or "").strip().lower()
    definition_text = (payload.get("definition_text") or "").strip()
    sentence_text = (payload.get("sentence_text") or "").strip()
    assisted = bool(payload.get("assisted"))

    word_obj = None
    custom_word = None
    enriched = None
    if item_id.startswith("cw-"):
        try:
            cwid = int(item_id.split("-", 1)[1])
        except (TypeError, ValueError):
            return JsonResponse({"ok": False, "error": "invalid item id"}, status=400)
        custom_word = get_object_or_404(CustomDeckWord, pk=cwid, deck__student=request.user)
        enriched = {
            "id": custom_word.id,
            "word": custom_word.word,
            "definition": "No saved definition for this custom word yet.",
            "example": f"In IELTS essays, use '{custom_word.word}' in a clear topic sentence.",
            "collocations": [],
            "ielts_note": "Because this is a custom word, focus on clarity and accurate meaning in context.",
            "pos": "word",
        }
    else:
        if not word_id:
            word_id = item_id.split("-", 1)[1] if item_id.startswith("w-") else word_id
        try:
            wid = int(word_id)
        except (TypeError, ValueError):
            return JsonResponse({"ok": False, "error": "word_id required."}, status=400)
        word_obj = get_object_or_404(Word, pk=wid)
        enriched = enrich_word(word_obj)

    if not definition_text and not sentence_text:
        return JsonResponse(
            {
                "ok": False,
                "error": "empty_submission",
                "message": "Write a definition, a sentence, or both — then request feedback.",
            },
            status=400,
        )

    if definition_text and sentence_text:
        mode = TypeItAttempt.MODE_BOTH
    elif definition_text:
        mode = TypeItAttempt.MODE_DEFINITION
    else:
        mode = TypeItAttempt.MODE_SENTENCE

    api_key = (getattr(settings, "OPENAI_API_KEY", None) or resolve_openai_api_key() or "").strip()
    if not api_key:
        return JsonResponse(
            {"ok": False, "error": "OpenAI API key is not configured.", "message": "Something went wrong — try again."},
            status=503,
        )

    common = (
        "You are an IELTS vocabulary examiner.\n\n"
        f'Target word: "{enriched["word"]}"\n'
        f'Correct definition: "{enriched["definition"]}"\n'
        f'IELTS example sentence: "{enriched["example"]}"\n\n'
    )
    if mode == TypeItAttempt.MODE_BOTH:
        prompt = (
            common
            + "Student wrote:\n"
            + f'Definition: "{definition_text}"\n'
            + f'Sentence: "{sentence_text}"\n\n'
            + "Score both definition and sentence.\n"
            + "Return ONLY this JSON. No explanation, no markdown, no backticks:\n"
            + "{\n"
            + '  "definition_score": number from 1 to 5,\n'
            + '  "definition_good": "what they got right in 1-2 sentences",\n'
            + '  "definition_missing": "what was wrong or missing — empty string if score is 4 or above",\n'
            + '  "sentence_score": number from 1 to 5,\n'
            + '  "sentence_good": "what was good about the sentence",\n'
            + '  "sentence_improve": "what to improve — empty string if score is 4 or above",\n'
            + '  "better_sentence": "a stronger IELTS-style sentence using the word",\n'
            + '  "band_tip": "one sentence on what band level this shows and one tip to improve"\n'
            + "}\n"
        )
    elif mode == TypeItAttempt.MODE_DEFINITION:
        prompt = (
            common
            + "The student submitted ONLY a definition (no sentence).\n"
            + f'Student definition: "{definition_text}"\n\n'
            + "Score the definition only.\n"
            + "Return ONLY this JSON. No explanation, no markdown, no backticks:\n"
            + "{\n"
            + '  "definition_score": number from 1 to 5,\n'
            + '  "definition_good": "what they got right in 1-2 sentences",\n'
            + '  "definition_missing": "what was wrong or missing — empty string if score is 4 or above",\n'
            + '  "band_tip": "one sentence on vocabulary level shown and one tip to improve"\n'
            + "}\n"
        )
    else:
        prompt = (
            common
            + "The student submitted ONLY a sentence (no definition).\n"
            + f'Student sentence: "{sentence_text}"\n\n'
            + "Score the sentence only.\n"
            + "Return ONLY this JSON. No explanation, no markdown, no backticks:\n"
            + "{\n"
            + '  "sentence_score": number from 1 to 5,\n'
            + '  "sentence_good": "what was good about the sentence",\n'
            + '  "sentence_improve": "what to improve — empty string if score is 4 or above",\n'
            + '  "better_sentence": "a stronger IELTS-style sentence using the word",\n'
            + '  "band_tip": "one sentence on vocabulary level shown and one tip to improve"\n'
            + "}\n"
        )

    model = (os.environ.get("OPENAI_TYPE_IT_FEEDBACK_MODEL") or "").strip() or "gpt-4o-mini"
    try:
        # Ignore shell/OS proxy env vars for this request path; a local proxy can block api.openai.com.
        client = OpenAI(api_key=api_key, http_client=httpx.Client(trust_env=False))
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an IELTS vocabulary examiner. Return only valid JSON as instructed. No markdown fences.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=2048,
        )
        raw_text = (completion.choices[0].message.content or "").strip()
        if not raw_text:
            raise RuntimeError("OpenAI returned empty content")
    except AuthenticationError:
        logger.warning("type_it_feedback: OpenAI authentication failed (invalid or revoked API key)")
        return JsonResponse(
            {
                "ok": False,
                "success": False,
                "error": "invalid_api_key",
                "message": (
                    "OpenAI rejected your API key. Create a new secret key at "
                    "https://platform.openai.com/account/api-keys , set OPENAI_API_KEY in your "
                    ".env file (or export it in the same terminal), restart runserver, and try again."
                ),
            },
            status=401,
        )
    except Exception:
        logger.exception("type_it_feedback: OpenAI call failed (model=%s)", model)
        return JsonResponse(
            {
                "ok": False,
                "success": False,
                "error": "ai_request_failed",
                "message": (
                    "AI feedback could not be completed. Check your internet connection, "
                    "confirm your OpenAI API key is set, then try again."
                ),
            },
            status=502,
        )

    parsed = _extract_json_object(raw_text)
    if not isinstance(parsed, dict):
        logger.warning("type_it_feedback: parse_failed raw=%s", (raw_text or "")[:800])
        return JsonResponse(
            {
                "ok": False,
                "success": False,
                "error": "Invalid JSON from AI (parse_failed).",
                "message": "Something went wrong — try again.",
            },
            status=502,
        )

    def _clamp_int(v, lo, hi, default):
        try:
            n = int(v)
            return max(lo, min(hi, n))
        except (TypeError, ValueError):
            return default

    if mode == TypeItAttempt.MODE_BOTH:
        ds = _clamp_int(parsed.get("definition_score"), 1, 5, 3)
        ss = _clamp_int(parsed.get("sentence_score"), 1, 5, 3)
        total = ds + ss
        feedback_json = parsed
    elif mode == TypeItAttempt.MODE_DEFINITION:
        ds = _clamp_int(parsed.get("definition_score"), 1, 5, 3)
        ss = None
        total = ds
        feedback_json = {
            **parsed,
            "sentence_score": None,
            "sentence_good": "",
            "sentence_improve": "",
            "better_sentence": "",
        }
    else:
        ds = None
        ss = _clamp_int(parsed.get("sentence_score"), 1, 5, 3)
        total = ss
        feedback_json = {
            **parsed,
            "definition_score": None,
            "definition_good": "",
            "definition_missing": "",
        }

    try:
        attempt = TypeItAttempt.objects.create(
            student=request.user,
            word=word_obj,
            custom_word=custom_word,
            deck_slug=deck_slug or "unknown",
            mode=mode,
            definition_score=ds,
            sentence_score=ss,
            total_score=total,
            assisted=assisted,
            student_definition=definition_text if mode != TypeItAttempt.MODE_SENTENCE else "",
            student_sentence=sentence_text if mode != TypeItAttempt.MODE_DEFINITION else "",
            feedback_json=feedback_json,
        )
        bump_streak_for_user(request.user)
    except Exception:
        logger.exception("type_it_feedback: failed to save TypeItAttempt")
        return JsonResponse(
            {
                "ok": False,
                "error": "save_failed",
                "message": "Something went wrong — try again.",
            },
            status=500,
        )

    return JsonResponse(
        {
            "ok": True,
            "success": True,
            "attempt_id": attempt.id,
            "mode": mode,
            "total_score": total,
            "definition_score": ds,
            "sentence_score": ss,
            "feedback": feedback_json,
            "word": enriched,
        }
    )


# Backward-compatible name for imports/tests
type_it_feedback_api = type_it_feedback


def _resolve_deck_for_user(user, deck_id: str):
    slug = (deck_id or "").strip().lower()
    if slug.startswith("custom-"):
        try:
            deck_pk = int(slug.split("-", 1)[1])
        except (TypeError, ValueError):
            raise Http404("Deck not found")
        deck = get_object_or_404(CustomDeck, pk=deck_pk, student=user)
        words = list(deck.words.all().order_by("id"))
        payload_words = []
        for w in words:
            payload_words.append(
                {
                    "item_id": f"cw-{w.id}",
                    "word_id": None,
                    "custom_word_id": w.id,
                    "word": w.word,
                    "pos": "word",
                    "definition": "No saved definition for this custom word yet.",
                    "example": f"In IELTS essays, use '{w.word}' naturally in context.",
                    "collocations": [],
                    "ielts_note": "Custom word: write a precise definition and a natural sentence.",
                    "topic_label": "Custom",
                    "level_label": "Custom",
                }
            )
        return {
            "slug": slug,
            "title": deck.name,
            "is_custom": True,
            "words": payload_words,
            "decks_url": reverse("vocabulary:type_it_deck"),
            "words_url": reverse("vocabulary:type_it_words", kwargs={"deck_id": slug}),
            "session_url": reverse("vocabulary:type_it_session_page", kwargs={"deck_id": slug}),
        }

    try:
        topic, level = parse_deck_slug(slug)
    except ValueError as exc:
        raise Http404("Deck not found") from exc
    words = ordered_words_for_deck(slug, topic, level)
    if not words:
        raise Http404("Deck not found")
    payload_words = []
    for w in words:
        e = enrich_word(w)
        payload_words.append(
            {
                "item_id": f"w-{w.id}",
                "word_id": w.id,
                "custom_word_id": None,
                "word": e["word"],
                "pos": e["pos"] or "word",
                "definition": e["definition"],
                "example": e["example"],
                "collocations": e["collocations"],
                "ielts_note": e["ielts_note"],
                "topic_label": e["topic_label"],
                "level_label": e["level_label"],
            }
        )
    return {
        "slug": slug,
        "title": deck_title(topic, level),
        "is_custom": False,
        "words": payload_words,
        "decks_url": reverse("vocabulary:type_it_deck"),
        "words_url": reverse("vocabulary:type_it_words", kwargs={"deck_id": slug}),
        "session_url": reverse("vocabulary:type_it_session_page", kwargs={"deck_id": slug}),
    }


def _type_it_words_page(request, deck_id: str):
    deck = _resolve_deck_for_user(request.user, deck_id)
    words = deck["words"]
    word_bests = _type_it_word_bests_payload(request.user, words)
    total = len(words)
    done = sum(1 for w in words if word_bests.get(w["item_id"], {}).get("passed"))
    payload = dict(deck)
    payload["words"] = words
    payload["word_bests"] = word_bests
    payload["mastery_total"] = total
    payload["mastery_done"] = done
    payload["mastery_pct"] = int(round((100 * done) / total)) if total else 0
    payload["feedback_url"] = reverse("vocabulary:type_it_feedback")
    return render(request, "vocabulary/type_it_words.html", {"deck": payload, **_streak_ctx(request)})


@login_required
def type_it_words(request, deck_id: str):
    return _type_it_words_page(request, deck_id)


@login_required
def type_it_words_topic_level(request, topic: str, level_slug: str):
    slug_map = {"beginner": 1, "standard": 2, "advanced": 3}
    t = (topic or "").strip().lower()
    lvl = slug_map.get((level_slug or "").strip().lower())
    valid_topics = {c[0] for c in Word.TOPIC_CHOICES}
    if lvl is None or t not in valid_topics:
        raise Http404("Deck not found")
    return _type_it_words_page(request, f"{t}-{lvl}")


@login_required
def type_it_session_page(request, deck_id: str):
    deck = _resolve_deck_for_user(request.user, deck_id)
    selected_raw = (request.GET.get("words") or "").strip()
    selected = [s.strip() for s in selected_raw.split(",") if s.strip()]
    valid = {w["item_id"]: w for w in deck["words"]}
    chosen = [valid[s] for s in selected if s in valid]
    if not chosen:
        return redirect("vocabulary:type_it_words", deck_id=deck_id)
    payload = {
        "deck": {
            "slug": deck["slug"],
            "title": deck["title"],
            "decks_url": deck["decks_url"],
            "words_url": deck["words_url"],
            "feedback_url": reverse("vocabulary:type_it_feedback"),
        },
        "words": chosen,
        "word_bests": _type_it_word_bests_payload(request.user, chosen),
    }
    return render(request, "vocabulary/type_it_session_flow.html", {"session_payload": payload, **_streak_ctx(request)})


@login_required
@require_POST
def type_it_custom_deck_create_api(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "invalid_json"}, status=400)
    name = (payload.get("name") or "").strip()
    colour = (payload.get("colour") or "navy").strip().lower()
    emoji = (payload.get("emoji") or "📖").strip()
    words_text = (payload.get("words") or "").strip()
    if not name:
        return JsonResponse({"ok": False, "error": "name_required"}, status=400)
    lines = [x.strip() for x in words_text.splitlines() if x.strip()]
    if not lines:
        return JsonResponse({"ok": False, "error": "words_required"}, status=400)
    deck = CustomDeck.objects.create(
        student=request.user,
        name=name[:100],
        colour=colour[:20] or "navy",
        emoji=emoji[:10] or "📖",
    )
    objs = []
    for w in lines[:200]:
        objs.append(CustomDeckWord(deck=deck, word=w[:100]))
    CustomDeckWord.objects.bulk_create(objs)
    return JsonResponse(
        {
            "ok": True,
            "deck_id": f"custom-{deck.id}",
            "words_url": reverse("vocabulary:type_it_words", kwargs={"deck_id": f"custom-{deck.id}"}),
        }
    )
