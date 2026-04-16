import base64
import binascii
import json
import logging
import math
import uuid
from datetime import timedelta
from typing import Set, Tuple
from urllib.parse import quote

from django.contrib import messages
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Avg, Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods, require_POST

from boostingscore.context_processors import study_streak
from boostingscore.models import UserProfile

from writing.models import WordBankEntry

from .ai_deck import MAX_CARDS, generate_flashcard_set
from .ai_fill import (
    check_type_practice,
    evaluate_type_it_session,
    generate_definition_and_example,
)
from .ai_image import generate_illustration_png_bytes
from .forms import CustomCardForm
from .models import CustomCard, CustomDeck, TypeItResult, VocabFavorite, VocabularyProgress, Word
from .progress_service import (
    build_struggling_deck_payload,
    custom_decks_for_studio,
    end_session_for_keys,
    get_struggling_banner,
    mastery_map_for_student,
    record_flashcard_rating,
    record_type_example_success,
    times_marked_hard_map_for_student,
    topic_decks_for_studio,
    TOPIC_DECK_EMOJI,
    word_is_due_for_flash_review,
)

logger = logging.getLogger(__name__)

SR_INTERVALS = [1, 3, 7, 14, 30]

_REVIEW_EASY_DAYS_ALLOWED = frozenset({3, 5, 7, 14, 30})
_REVIEW_HARD_DAYS_ALLOWED = frozenset({1, 2, 3, 5})
_REVIEW_SESSION_SIZE_ALLOWED = frozenset({0, 10, 20, 30})


def _flash_review_prefs(user) -> dict[str, int]:
    if not user.is_authenticated:
        return {"easy_days": 7, "hard_days": 1, "session_size": 20}
    row = UserProfile.objects.filter(user=user).values(
        "review_easy_days", "review_hard_days", "review_session_size"
    ).first()
    if not row:
        return {"easy_days": 7, "hard_days": 1, "session_size": 20}
    ss = row["review_session_size"]
    return {
        "easy_days": int(row["review_easy_days"] or 7),
        "hard_days": int(row["review_hard_days"] or 1),
        "session_size": 20 if ss is None else int(ss),
    }


def _apply_review_session_cap(user, words: list) -> list:
    if not user.is_authenticated or not words:
        return words
    row = UserProfile.objects.filter(user=user).values_list(
        "review_session_size", flat=True
    ).first()
    cap = 20 if row is None else int(row)
    if cap <= 0:
        return words
    return words[:cap]


def _assign_custom_deck(
    user, card: CustomCard, *, deck: CustomDeck | None
) -> None:
    """Attach personal card to a named deck, or clear when not personal."""
    if card.topic == CustomCard.TOPIC_OTHER and deck is not None:
        card.deck = deck
    else:
        card.deck = None


def _topic_choices_full():
    return list(Word.TOPIC_CHOICES) + [
        next(c for c in CustomCard.TOPIC_CHOICES if c[0] == CustomCard.TOPIC_OTHER),
    ]


def _valid_topic(code: str) -> bool:
    return code in {t[0] for t in _topic_choices_full()}


_CUSTOM_FORM_LEVEL_CARDS = [
    (1, "Beginner", "Everyday words"),
    (2, "Standard", "IELTS-style"),
    (3, "Advanced", "Academic"),
]

_STUDY_PANEL_IDS = frozenset(
    {"flashcards", "list", "quiz", "type", "favorites", "browse", "guide"}
)
_STUDY_PANEL_LABELS = {
    "flashcards": "Flashcards",
    "list": "Word list",
    "quiz": "Quiz",
    "type": "Type it",
    "favorites": "Favored",
    "browse": "Browse",
    "guide": "Guide",
}


def _parse_study_panel(request: HttpRequest) -> str:
    raw = (request.GET.get("panel") or "flashcards").strip().lower()
    return raw if raw in _STUDY_PANEL_IDS else "flashcards"


def _absolute_media_url(request: HttpRequest, file_field) -> str:
    if not file_field or not getattr(file_field, "name", ""):
        return ""
    try:
        path = file_field.url
    except ValueError:
        return ""
    return request.build_absolute_uri(path)


def _normalize_str_list(raw) -> list[str]:
    if not raw:
        return []
    if isinstance(raw, list):
        return [str(x).strip() for x in raw if str(x).strip()]
    return []


def _lexical_word_fields(w: Word) -> dict:
    phonetic = (
        getattr(w, "phonetic", None)
        or getattr(w, "ipa", None)
        or getattr(w, "pronunciation", None)
        or ""
    )
    return {
        "part_of_speech": (w.part_of_speech or "").strip(),
        "phonetic": str(phonetic).strip(),
        "synonyms": _normalize_str_list(w.synonyms),
        "antonyms": _normalize_str_list(w.antonyms),
        "collocations": _normalize_str_list(w.collocations),
    }


def _lexical_card_fields(c: CustomCard) -> dict:
    phonetic = (
        getattr(c, "phonetic", None)
        or getattr(c, "ipa", None)
        or getattr(c, "pronunciation", None)
        or ""
    )
    return {
        "part_of_speech": (c.part_of_speech or "").strip(),
        "phonetic": str(phonetic).strip(),
        "synonyms": _normalize_str_list(c.synonyms),
        "antonyms": _normalize_str_list(c.antonyms),
        "collocations": _normalize_str_list(c.collocations),
    }


def _favorite_pair_set(user) -> Set[Tuple[str, int]]:
    if not user.is_authenticated:
        return set()
    pairs: Set[Tuple[str, int]] = set()
    for wid, cid in VocabFavorite.objects.filter(user=user).values_list(
        "word_id", "custom_card_id"
    ):
        if wid:
            pairs.add(("w", wid))
        if cid:
            pairs.add(("c", cid))
    return pairs


def _full_word_list_for_topic(
    topic: str,
    user,
    request: HttpRequest,
    fav_pairs: Set[Tuple[str, int]],
    mastery_map: dict[str, int] | None = None,
    level_filter: int | None = None,
    hard_map: dict[str, int] | None = None,
):
    """All global + all user's custom cards in topic (full reference list for Word list)."""
    mastery_map = mastery_map or {}
    hard_map = hard_map or {}
    items = []
    wq = Word.objects.filter(topic=topic)
    if level_filter is not None:
        wq = wq.filter(level=level_filter)
    for w in wq.order_by("level", "word"):
        wk = f"w:{w.pk}"
        row = {
            "word": w.word,
            "definition": w.definition or "",
            "example": w.example_sentence or "",
            "level": w.level,
            "is_custom": False,
            "custom_id": None,
            "word_id": w.pk,
            "image_url": _absolute_media_url(request, w.definition_image),
            "favorited": ("w", w.pk) in fav_pairs,
            "mastery_level": mastery_map.get(wk, 0),
            "times_marked_hard": hard_map.get(wk, 0),
            "is_mastered_card": False,
        }
        row.update(_lexical_word_fields(w))
        items.append(row)
    if user.is_authenticated:
        cq = CustomCard.objects.filter(student=user, topic=topic)
        if level_filter is not None:
            cq = cq.filter(level=level_filter)
        for c in cq.order_by("level", "word"):
            ck = f"c:{c.pk}"
            row = {
                "word": c.word,
                "definition": c.definition or "",
                "example": c.example_sentence or "",
                "level": c.level,
                "is_custom": True,
                "custom_id": c.pk,
                "word_id": None,
                "image_url": _absolute_media_url(request, c.definition_image),
                "favorited": ("c", c.pk) in fav_pairs,
                "mastery_level": mastery_map.get(ck, 0),
                "times_marked_hard": hard_map.get(ck, 0),
                "is_mastered_card": bool(c.is_mastered),
            }
            row.update(_lexical_card_fields(c))
            items.append(row)
    items.sort(key=lambda x: (x["level"], x["word"].lower()))
    return items


def _favorites_payload(user, request: HttpRequest, topic_labels: dict) -> list[dict]:
    if not user.is_authenticated:
        return []
    out = []
    qs = (
        VocabFavorite.objects.filter(user=user)
        .select_related("word", "custom_card")
        .order_by("-created_at")
    )
    for f in qs:
        if f.word_id and f.word:
            w = f.word
            out.append(
                {
                    "word": w.word,
                    "definition": w.definition or "",
                    "example": w.example_sentence or "",
                    "level": w.level,
                    "is_custom": False,
                    "custom_id": None,
                    "word_id": w.pk,
                    "kind": "word",
                    "topic": w.topic,
                    "topic_label": topic_labels.get(w.topic, w.topic),
                    "image_url": _absolute_media_url(request, w.definition_image),
                    "favorited": True,
                }
            )
        elif f.custom_card_id and f.custom_card:
            c = f.custom_card
            out.append(
                {
                    "word": c.word,
                    "definition": c.definition or "",
                    "example": c.example_sentence or "",
                    "level": c.level,
                    "is_custom": True,
                    "custom_id": c.pk,
                    "word_id": None,
                    "kind": "custom",
                    "topic": c.topic,
                    "topic_label": topic_labels.get(c.topic, c.topic),
                    "image_url": _absolute_media_url(request, c.definition_image),
                    "favorited": True,
                }
            )
    return out


def _merged_deck(
    topic: str,
    user,
    now,
    request: HttpRequest,
    level_filter: int | None = None,
    mastery_map: dict[str, int] | None = None,
):
    """Global words + user's custom cards (not mastered, due for spaced review)."""
    mastery_map = mastery_map or {}
    items = []
    wq = Word.objects.filter(topic=topic)
    if level_filter is not None:
        wq = wq.filter(level=level_filter)
    word_rows = list(wq.order_by("level", "word"))
    wpks = [w.pk for w in word_rows]
    prog_by_wid: dict = {}
    if user.is_authenticated and wpks:
        for p in VocabularyProgress.objects.filter(
            student=user, word_id__in=wpks
        ).only("word_id", "next_review", "last_reviewed"):
            prog_by_wid[p.word_id] = p
    for w in word_rows:
        prog_w = prog_by_wid.get(w.pk) if user.is_authenticated else None
        row = {
            "word": w.word,
            "definition": w.definition or "",
            "example": w.example_sentence or "",
            "level": w.level,
            "is_custom": False,
            "custom_id": None,
            "word_id": w.pk,
            "image_url": _absolute_media_url(request, w.definition_image),
            "due": word_is_due_for_flash_review(
                user, now, w.pk, prog_w, mastery_map
            ),
            "last_reviewed": (
                prog_w.last_reviewed.isoformat()
                if prog_w and prog_w.last_reviewed
                else None
            ),
        }
        row.update(_lexical_word_fields(w))
        items.append(row)
    if user.is_authenticated:
        custom_qs = CustomCard.objects.filter(
            student=user,
            topic=topic,
            is_mastered=False,
        ).filter(Q(next_review_at__isnull=True) | Q(next_review_at__lte=now))
        if level_filter is not None:
            custom_qs = custom_qs.filter(level=level_filter)
        custom_rows = list(custom_qs.order_by("level", "word"))
        cids = [c.pk for c in custom_rows]
        prog_by_cid: dict = {}
        if cids:
            for p in VocabularyProgress.objects.filter(
                student=user, custom_card_id__in=cids
            ).only("custom_card_id", "last_reviewed"):
                prog_by_cid[p.custom_card_id] = p
        for c in custom_rows:
            prog_c = prog_by_cid.get(c.pk)
            row = {
                "word": c.word,
                "definition": c.definition or "",
                "example": c.example_sentence or "",
                "level": c.level,
                "is_custom": True,
                "custom_id": c.pk,
                "word_id": None,
                "image_url": _absolute_media_url(request, c.definition_image),
                "due": True,
                "last_reviewed": (
                    prog_c.last_reviewed.isoformat()
                    if prog_c and prog_c.last_reviewed
                    else None
                ),
            }
            row.update(_lexical_card_fields(c))
            items.append(row)
    items.sort(key=lambda x: (x["level"], x["word"].lower()))
    return items


def _merged_custom_deck(
    deck: CustomDeck,
    user,
    now,
    request: HttpRequest,
    level_filter: int | None = None,
):
    """Due custom cards in one named deck only."""
    items = []
    custom_qs = CustomCard.objects.filter(
        student=user,
        deck=deck,
        topic=CustomCard.TOPIC_OTHER,
        is_mastered=False,
    ).filter(Q(next_review_at__isnull=True) | Q(next_review_at__lte=now))
    if level_filter is not None:
        custom_qs = custom_qs.filter(level=level_filter)
    custom_rows = list(custom_qs.order_by("level", "word"))
    cids = [c.pk for c in custom_rows]
    prog_by_cid: dict = {}
    if user.is_authenticated and cids:
        for p in VocabularyProgress.objects.filter(
            student=user, custom_card_id__in=cids
        ).only("custom_card_id", "last_reviewed"):
            prog_by_cid[p.custom_card_id] = p
    for c in custom_rows:
        prog_c = prog_by_cid.get(c.pk)
        row = {
            "word": c.word,
            "definition": c.definition or "",
            "example": c.example_sentence or "",
            "level": c.level,
            "is_custom": True,
            "custom_id": c.pk,
            "word_id": None,
            "image_url": _absolute_media_url(request, c.definition_image),
            "due": True,
            "last_reviewed": (
                prog_c.last_reviewed.isoformat()
                if prog_c and prog_c.last_reviewed
                else None
            ),
        }
        row.update(_lexical_card_fields(c))
        items.append(row)
    items.sort(key=lambda x: (x["level"], x["word"].lower()))
    return items


def _full_word_list_custom_deck(
    deck: CustomDeck,
    user,
    request: HttpRequest,
    fav_pairs: Set[Tuple[str, int]],
    mastery_map: dict[str, int] | None = None,
    level_filter: int | None = None,
    hard_map: dict[str, int] | None = None,
):
    mastery_map = mastery_map or {}
    hard_map = hard_map or {}
    items = []
    cq = CustomCard.objects.filter(student=user, deck=deck, topic=CustomCard.TOPIC_OTHER)
    if level_filter is not None:
        cq = cq.filter(level=level_filter)
    for c in cq.order_by("level", "word"):
        ck = f"c:{c.pk}"
        row = {
            "word": c.word,
            "definition": c.definition or "",
            "example": c.example_sentence or "",
            "level": c.level,
            "is_custom": True,
            "custom_id": c.pk,
            "word_id": None,
            "image_url": _absolute_media_url(request, c.definition_image),
            "favorited": ("c", c.pk) in fav_pairs,
            "mastery_level": mastery_map.get(ck, 0),
            "times_marked_hard": hard_map.get(ck, 0),
            "is_mastered_card": bool(c.is_mastered),
        }
        row.update(_lexical_card_fields(c))
        items.append(row)
    return items


def _full_word_list_all(
    user,
    request: HttpRequest,
    fav_pairs: Set[Tuple[str, int]],
    topic_labels: dict[str, str],
    mastery_map: dict[str, int] | None = None,
    level_filter: int | None = None,
    hard_map: dict[str, int] | None = None,
):
    """Every global word and every custom card for the student, filtered by level (studio-wide list)."""
    mastery_map = mastery_map or {}
    hard_map = hard_map or {}
    items: list[dict] = []
    wq = Word.objects.all()
    if level_filter is not None:
        wq = wq.filter(level=level_filter)
    for w in wq.order_by("topic", "word"):
        wk = f"w:{w.pk}"
        row = {
            "word": w.word,
            "definition": w.definition or "",
            "example": w.example_sentence or "",
            "level": w.level,
            "is_custom": False,
            "custom_id": None,
            "word_id": w.pk,
            "image_url": _absolute_media_url(request, w.definition_image),
            "favorited": ("w", w.pk) in fav_pairs,
            "mastery_level": mastery_map.get(wk, 0),
            "times_marked_hard": hard_map.get(wk, 0),
            "is_mastered_card": False,
            "practice_topic_code": w.topic,
            "practice_deck_pk": None,
            "source_label": topic_labels.get(w.topic, w.topic),
        }
        row.update(_lexical_word_fields(w))
        items.append(row)
    if user.is_authenticated:
        cq = CustomCard.objects.filter(student=user).select_related("deck")
        if level_filter is not None:
            cq = cq.filter(level=level_filter)
        for c in cq.order_by("topic", "word"):
            ck = f"c:{c.pk}"
            if c.topic == CustomCard.TOPIC_OTHER:
                src = c.deck.name if c.deck_id else "My vocabulary"
            else:
                src = topic_labels.get(c.topic, c.topic)
            row = {
                "word": c.word,
                "definition": c.definition or "",
                "example": c.example_sentence or "",
                "level": c.level,
                "is_custom": True,
                "custom_id": c.pk,
                "word_id": None,
                "image_url": _absolute_media_url(request, c.definition_image),
                "favorited": ("c", c.pk) in fav_pairs,
                "mastery_level": mastery_map.get(ck, 0),
                "times_marked_hard": hard_map.get(ck, 0),
                "is_mastered_card": bool(c.is_mastered),
                "practice_topic_code": CustomCard.TOPIC_OTHER
                if c.topic == CustomCard.TOPIC_OTHER
                else c.topic,
                "practice_deck_pk": c.deck_id
                if c.topic == CustomCard.TOPIC_OTHER and c.deck_id
                else None,
                "source_label": src,
            }
            row.update(_lexical_card_fields(c))
            items.append(row)
    items.sort(key=lambda x: (x["word"].lower(), x.get("source_label") or ""))
    return items


def _sync_new_card_to_word_bank(user, card: CustomCard) -> None:
    phrase = f"{card.word} — {(card.definition or '').strip()[:450]}".strip()
    if len(phrase) < 2:
        phrase = card.word
    WordBankEntry.objects.create(user=user, phrase=phrase[:500], essay=None)


def _vocab_level_for_request(request: HttpRequest) -> int | None:
    if not request.user.is_authenticated:
        return None
    row = UserProfile.objects.filter(user=request.user).values_list(
        "level", flat=True
    ).first()
    return int(row) if row is not None else 2


def _profile_vocab_level_int(user) -> int:
    row = UserProfile.objects.filter(user=user).values_list("level", flat=True).first()
    return int(row) if row is not None else 2


def _row_progress_key(row: dict) -> str:
    if row.get("is_custom") and row.get("custom_id") is not None:
        return f"c:{int(row['custom_id'])}"
    if row.get("word_id") is not None:
        return f"w:{int(row['word_id'])}"
    return ""


def _parse_words_param_list(request: HttpRequest) -> list[str] | None:
    """Parse ``?words=`` — comma tokens: ``12`` / ``w:12`` / ``c:3`` (order preserved, deduped)."""
    raw = (request.GET.get("words") or "").strip()
    if not raw:
        return None
    out: list[str] = []
    seen: set[str] = set()
    for part in raw.split(","):
        t = part.strip()
        if not t:
            continue
        key: str | None = None
        if ":" in t:
            kind, _, rest = t.partition(":")
            kind_l = kind.strip().lower()
            rest = rest.strip()
            if not rest.isdigit():
                continue
            pk = int(rest)
            if kind_l in ("w", "word"):
                key = f"w:{pk}"
            elif kind_l in ("c", "custom"):
                key = f"c:{pk}"
        elif t.isdigit():
            key = f"w:{int(t)}"
        if key and key not in seen:
            seen.add(key)
            out.append(key)
    return out or None


def _flash_rows_for_progress_keys(
    user,
    request: HttpRequest,
    now,
    keys: list[str],
    mastery_map: dict[str, int],
) -> list[dict]:
    """Build flashcard ``words_payload`` rows for arbitrary word/custom IDs (any topic)."""
    mastery_map = mastery_map or {}
    items: list[dict] = []
    for key in keys:
        if key.startswith("w:"):
            pk = int(key[2:])
            w = Word.objects.filter(pk=pk).first()
            if not w:
                continue
            wk = f"w:{w.pk}"
            prog_w = None
            if user.is_authenticated:
                prog_w = (
                    VocabularyProgress.objects.filter(student=user, word_id=w.pk)
                    .only("word_id", "next_review", "last_reviewed")
                    .first()
                )
            row = {
                "word": w.word,
                "definition": w.definition or "",
                "example": w.example_sentence or "",
                "level": w.level,
                "is_custom": False,
                "custom_id": None,
                "word_id": w.pk,
                "image_url": _absolute_media_url(request, w.definition_image),
                "due": word_is_due_for_flash_review(
                    user, now, w.pk, prog_w, mastery_map
                ),
                "last_reviewed": (
                    prog_w.last_reviewed.isoformat()
                    if prog_w and prog_w.last_reviewed
                    else None
                ),
            }
            row.update(_lexical_word_fields(w))
            items.append(row)
        elif key.startswith("c:"):
            pk = int(key[2:])
            c = CustomCard.objects.filter(pk=pk, student=user).first()
            if not c:
                continue
            prog_c = None
            if user.is_authenticated:
                prog_c = (
                    VocabularyProgress.objects.filter(student=user, custom_card_id=c.pk)
                    .only("custom_card_id", "last_reviewed")
                    .first()
                )
            row = {
                "word": c.word,
                "definition": c.definition or "",
                "example": c.example_sentence or "",
                "level": c.level,
                "is_custom": True,
                "custom_id": c.pk,
                "word_id": None,
                "image_url": _absolute_media_url(request, c.definition_image),
                "due": True,
                "last_reviewed": (
                    prog_c.last_reviewed.isoformat()
                    if prog_c and prog_c.last_reviewed
                    else None
                ),
            }
            row.update(_lexical_card_fields(c))
            items.append(row)
    return items


def _type_it_rows_for_progress_keys(
    user,
    request: HttpRequest,
    keys: list[str],
    study_level: int | None,
    fav_pairs: Set[Tuple[str, int]],
    mastery_map: dict[str, int],
    hard_map: dict[str, int],
) -> list[dict]:
    """Rows compatible with ``_type_it_load_rows`` / ``_row_progress_key`` for ad-hoc word picks."""
    rows: list[dict] = []
    for key in keys:
        if key.startswith("w:"):
            pk = int(key[2:])
            w = Word.objects.filter(pk=pk).first()
            if not w:
                continue
            wk = f"w:{w.pk}"
            row = {
                "word": w.word,
                "definition": w.definition or "",
                "example": w.example_sentence or "",
                "level": w.level,
                "is_custom": False,
                "custom_id": None,
                "word_id": w.pk,
                "image_url": _absolute_media_url(request, w.definition_image),
                "favorited": ("w", w.pk) in fav_pairs,
                "mastery_level": mastery_map.get(wk, 0),
                "times_marked_hard": hard_map.get(wk, 0),
                "is_mastered_card": False,
            }
            row.update(_lexical_word_fields(w))
            rows.append(row)
        elif key.startswith("c:"):
            pk = int(key[2:])
            c = CustomCard.objects.filter(pk=pk, student=user).first()
            if not c:
                continue
            ck = f"c:{c.pk}"
            row = {
                "word": c.word,
                "definition": c.definition or "",
                "example": c.example_sentence or "",
                "level": c.level,
                "is_custom": True,
                "custom_id": c.pk,
                "word_id": None,
                "image_url": _absolute_media_url(request, c.definition_image),
                "favorited": ("c", c.pk) in fav_pairs,
                "mastery_level": mastery_map.get(ck, 0),
                "times_marked_hard": hard_map.get(ck, 0),
                "is_mastered_card": bool(c.is_mastered),
            }
            row.update(_lexical_card_fields(c))
            rows.append(row)
    return rows


def _word_list_pos_badge(raw: str) -> str:
    t = (raw or "").strip().lower().rstrip(".")
    m = {
        "n": "noun",
        "noun": "noun",
        "v": "verb",
        "verb": "verb",
        "adj": "adj",
        "adjective": "adj",
        "adv": "adverb",
        "adverb": "adverb",
    }
    return m.get(t, "")


@login_required
def word_list_page(request: HttpRequest) -> HttpResponse:
    """Full word list for a topic, a named deck, or all vocabulary (``?all=1``)."""
    study_level = _profile_vocab_level_int(request.user)
    level_label_by_num = {n: label for n, label, _ in _CUSTOM_FORM_LEVEL_CARDS}
    user_level_label = f"Level {study_level} — {level_label_by_num.get(study_level, '')}"

    topic_labels = dict(_topic_choices_full())
    all_raw = (request.GET.get("all") or "").strip().lower()
    word_list_all = all_raw in ("1", "true", "yes", "all")

    topic_raw = (request.GET.get("topic") or "").strip().lower()
    if not word_list_all:
        if not topic_raw or not _valid_topic(topic_raw):
            messages.info(request, "Pick a vocabulary topic from the studio.")
            return redirect(reverse("vocabulary:index"))

    active_deck: CustomDeck | None = None
    dr = (request.GET.get("deck") or "").strip()
    if not word_list_all and dr.isdigit():
        active_deck = CustomDeck.objects.filter(
            pk=int(dr), student=request.user
        ).first()
        if active_deck:
            topic_raw = CustomCard.TOPIC_OTHER

    if word_list_all:
        topic_name = "All vocabulary"
        topic_code = topic_raw or Word.TOPIC_CHOICES[0][0]
    elif active_deck:
        topic_name = active_deck.name
        topic_code = CustomCard.TOPIC_OTHER
    else:
        topic_name = topic_labels.get(topic_raw, topic_raw.replace("_", " ").title())
        topic_code = topic_raw

    fav_pairs = _favorite_pair_set(request.user)
    mastery_map = mastery_map_for_student(request.user)
    hard_map = times_marked_hard_map_for_student(request.user)

    if word_list_all:
        rows = _full_word_list_all(
            request.user,
            request,
            fav_pairs,
            topic_labels,
            mastery_map,
            study_level,
            hard_map,
        )
    elif active_deck:
        rows = _full_word_list_custom_deck(
            active_deck,
            request.user,
            request,
            fav_pairs,
            mastery_map,
            study_level,
            hard_map,
        )
    else:
        rows = _full_word_list_for_topic(
            topic_raw,
            request.user,
            request,
            fav_pairs,
            mastery_map,
            study_level,
            hard_map,
        )

    wl_items: list[dict] = []
    for row in rows:
        ml = int(row.get("mastery_level") or 0)
        if row.get("is_mastered_card"):
            ml = max(ml, 5)
        is_mastered = ml >= 5
        th = int(row.get("times_marked_hard") or 0)
        is_struggling = th >= 2 and not is_mastered
        pos_badge = _word_list_pos_badge(row.get("part_of_speech") or "")

        if row.get("is_custom"):
            rid = f"c-{row['custom_id']}"
            kind = "custom"
            word_pk = None
            custom_pk = int(row["custom_id"])
        else:
            rid = f"w-{row['word_id']}"
            kind = "word"
            word_pk = int(row["word_id"])
            custom_pk = None

        item = {
            "row_id": rid,
            "progress_key": _row_progress_key(row),
            "kind": kind,
            "word_id": word_pk,
            "custom_id": custom_pk,
            "word_text": row["word"],
            "part_of_speech": pos_badge,
            "definition": (row.get("definition") or "").strip(),
            "example": (row.get("example") or "").strip(),
            "synonyms": row.get("synonyms") or [],
            "antonyms": row.get("antonyms") or [],
            "collocations": row.get("collocations") or [],
            "mastery_level": min(5, ml),
            "favorited": bool(row.get("favorited")),
            "is_struggling": is_struggling,
            "is_mastered": is_mastered,
        }
        if word_list_all:
            item["practice_topic"] = row.get("practice_topic_code") or topic_code
            item["practice_deck_pk"] = row.get("practice_deck_pk")
            item["source_label"] = row.get("source_label") or ""
        wl_items.append(item)

    total_words = len(wl_items)
    mastered_count = sum(1 for x in wl_items if x["is_mastered"])
    struggling_count = sum(1 for x in wl_items if x["is_struggling"])
    favored_count = sum(1 for x in wl_items if x["favorited"])

    toggle_url = reverse("vocabulary:vocab_toggle_favorite")
    word_bank_url = reverse("vocabulary:word_bank_add_vocab")
    deck_create_save_url = reverse("vocabulary:deck_create_save")
    url_flashcard_pick = reverse("vocabulary:flashcard")
    url_quiz_setup = reverse("vocabulary:quiz_setup")
    url_type_it_session = reverse("vocabulary:type_it_session")

    return render(
        request,
        "vocabulary/word_list.html",
        {
            "topic_name": topic_name,
            "topic_code": topic_code,
            "active_deck": None if word_list_all else active_deck,
            "word_list_all": word_list_all,
            "user_level_label": user_level_label,
            "study_level": study_level,
            "total_words": total_words,
            "mastered_count": mastered_count,
            "struggling_count": struggling_count,
            "favored_count": favored_count,
            "wl_items": wl_items,
            "toggle_url": toggle_url,
            "word_bank_url": word_bank_url,
            "deck_create_save_url": deck_create_save_url,
            "url_flashcard_pick": url_flashcard_pick,
            "url_quiz_setup": url_quiz_setup,
            "url_type_it_session": url_type_it_session,
        },
    )


@login_required
def quiz_setup_page(request: HttpRequest) -> HttpResponse:
    """Three-step quiz wizard: pick deck, words, and question types."""
    now = timezone.now()
    study_level = _vocab_level_for_request(request)
    topic_decks = topic_decks_for_studio(request.user, now, vocab_level=study_level)
    topic_decks = topic_decks + custom_decks_for_studio(
        request.user, now, vocab_level=study_level
    )
    words_api_url = reverse("vocabulary:quiz_setup_words")
    index_url = reverse("vocabulary:index")
    flashcard_pick_url = reverse("vocabulary:flashcard")
    return render(
        request,
        "vocabulary/quiz_setup.html",
        {
            "topic_decks": topic_decks,
            "words_api_url": words_api_url,
            "index_url": index_url,
            "flashcard_pick_url": flashcard_pick_url,
            "preset_words": (request.GET.get("words") or "").strip(),
        },
    )


@login_required
@require_http_methods(["GET"])
def quiz_setup_words(request: HttpRequest) -> JsonResponse:
    """JSON list of words in a deck for quiz setup step 2."""
    pick = _parse_words_param_list(request)
    if pick:
        study_level = _profile_vocab_level_int(request.user)
        fav_pairs = _favorite_pair_set(request.user)
        mastery_map = mastery_map_for_student(request.user)
        hard_map = times_marked_hard_map_for_student(request.user)
        rows = _type_it_rows_for_progress_keys(
            request.user,
            request,
            pick,
            study_level,
            fav_pairs,
            mastery_map,
            hard_map,
        )
        out = []
        for row in rows:
            k = _row_progress_key(row)
            if not k:
                continue
            ml = int(row.get("mastery_level") or 0)
            if row.get("is_mastered_card"):
                ml = max(ml, 5)
            is_mastered = ml >= 5
            th = int(row.get("times_marked_hard") or 0)
            struggling = th >= 2 and not is_mastered
            pos = _word_list_pos_badge(row.get("part_of_speech") or "")
            out.append(
                {
                    "id": k,
                    "word": row["word"],
                    "pos": pos,
                    "mastery": min(5, ml),
                    "favored": bool(row.get("favorited")),
                    "struggling": struggling,
                }
            )
        return JsonResponse({"ok": True, "words": out})

    topic_raw = (request.GET.get("topic") or "").strip().lower()
    dr = (request.GET.get("deck") or "").strip()
    if not topic_raw or not _valid_topic(topic_raw):
        return JsonResponse({"ok": False, "error": "Invalid topic."}, status=400)

    study_level = _profile_vocab_level_int(request.user)
    fav_pairs = _favorite_pair_set(request.user)
    mastery_map = mastery_map_for_student(request.user)
    hard_map = times_marked_hard_map_for_student(request.user)

    active_deck: CustomDeck | None = None
    if dr.isdigit():
        active_deck = CustomDeck.objects.filter(
            pk=int(dr), student=request.user
        ).first()
        if active_deck:
            topic_raw = CustomCard.TOPIC_OTHER

    if active_deck:
        rows = _full_word_list_custom_deck(
            active_deck,
            request.user,
            request,
            fav_pairs,
            mastery_map,
            study_level,
            hard_map,
        )
    else:
        rows = _full_word_list_for_topic(
            topic_raw,
            request.user,
            request,
            fav_pairs,
            mastery_map,
            study_level,
            hard_map,
        )

    out = []
    for row in rows:
        k = _row_progress_key(row)
        if not k:
            continue
        ml = int(row.get("mastery_level") or 0)
        if row.get("is_mastered_card"):
            ml = max(ml, 5)
        is_mastered = ml >= 5
        th = int(row.get("times_marked_hard") or 0)
        struggling = th >= 2 and not is_mastered
        pos = _word_list_pos_badge(row.get("part_of_speech") or "")
        out.append(
            {
                "id": k,
                "word": row["word"],
                "pos": pos,
                "mastery": min(5, ml),
                "favored": bool(row.get("favorited")),
                "struggling": struggling,
            }
        )
    return JsonResponse({"ok": True, "words": out})


def _type_it_row_with_name(row: dict) -> dict:
    out = dict(row)
    out["name"] = (row.get("label") or row.get("slug") or "").strip()
    return out


def type_it_deck_select(request: HttpRequest) -> HttpResponse:
    """Dedicated Type it deck picker (same counts as studio; links to type-it session)."""
    now = timezone.now()
    study_level = _vocab_level_for_request(request)
    theme_and_other = topic_decks_for_studio(
        request.user, now, vocab_level=study_level
    )
    custom_list = custom_decks_for_studio(
        request.user, now, vocab_level=study_level
    )
    merged = theme_and_other + custom_list

    topic_decks = [
        _type_it_row_with_name(d)
        for d in theme_and_other
        if d["slug"] != CustomCard.TOPIC_OTHER
    ]
    my_src = next(
        (d for d in theme_and_other if d["slug"] == CustomCard.TOPIC_OTHER),
        None,
    )
    if my_src:
        my_vocab = _type_it_row_with_name(my_src)
    else:
        my_vocab = {
            "name": "My vocabulary",
            "label": "My vocabulary",
            "slug": CustomCard.TOPIC_OTHER,
            "emoji": TOPIC_DECK_EMOJI.get(CustomCard.TOPIC_OTHER, "⭐"),
            "word_count": 0,
            "mastered_count": 0,
            "due_count": 0,
            "progress_pct": 0,
            "last_studied": None,
        }
    custom_decks = [_type_it_row_with_name(d) for d in custom_list]

    total_words = sum(d["word_count"] for d in merged)
    total_mastered = sum(d["mastered_count"] for d in merged)
    total_due = (
        sum(d["due_count"] for d in merged) if request.user.is_authenticated else 0
    )
    streak = study_streak(request.user)

    return render(
        request,
        "vocabulary/type_it_deck_select.html",
        {
            "topic_decks": topic_decks,
            "my_vocab": my_vocab,
            "custom_decks": custom_decks,
            "total_words": total_words,
            "total_mastered": total_mastered,
            "total_due": total_due,
            "streak": streak,
            "type_it_session_url": reverse("vocabulary:type_it_session"),
        },
    )


_TYPE_IT_MASTERY_STAGES = (
    "New",
    "Recognizing",
    "Learning",
    "Practicing",
    "Near mastery",
    "Mastered",
)


def _type_it_mastery_label(level: int) -> str:
    n = max(0, min(5, int(level)))
    return _TYPE_IT_MASTERY_STAGES[n]


def _type_it_topic_badge_label(
    row: dict, topic_param: str, topic_labels: dict[str, str]
) -> str:
    if row.get("is_custom") and row.get("custom_id"):
        t = (
            CustomCard.objects.filter(pk=int(row["custom_id"]))
            .values_list("topic", flat=True)
            .first()
        )
        return topic_labels.get(t or CustomCard.TOPIC_OTHER, t or "")
    if row.get("word_id"):
        t = (
            Word.objects.filter(pk=int(row["word_id"]))
            .values_list("topic", flat=True)
            .first()
        )
        return topic_labels.get(t or topic_param, topic_param)
    return topic_labels.get(topic_param, topic_param)


def _type_it_load_rows(
    *,
    request: HttpRequest,
    user,
    topic_param: str,
    active_deck: CustomDeck | None,
    study_level: int | None,
    fav_pairs: Set[Tuple[str, int]],
    mastery_map: dict[str, int],
    hard_map: dict[str, int],
):
    if active_deck:
        return _full_word_list_custom_deck(
            active_deck,
            user,
            request,
            fav_pairs,
            mastery_map,
            study_level,
            hard_map,
        )
    return _full_word_list_for_topic(
        topic_param,
        user,
        request,
        fav_pairs,
        mastery_map,
        study_level,
        hard_map,
    )


@ensure_csrf_cookie
@login_required
def type_it_session(request: HttpRequest) -> HttpResponse:
    """Dedicated Type it practice page (word-by-word) for a topic or named deck."""
    if request.GET.get("skip") == "1":
        request.session["type_it_skipped"] = int(
            request.session.get("type_it_skipped", 0)
        ) + 1
        request.session.modified = True

    study_level = _vocab_level_for_request(request)
    fav_pairs = _favorite_pair_set(request.user)
    mastery_map = mastery_map_for_student(request.user)
    hard_map = times_marked_hard_map_for_student(request.user)

    words_q_raw = (request.GET.get("words") or "").strip()
    words_pick_keys = _parse_words_param_list(request) or []
    pick_mode = bool(words_pick_keys)

    active_deck: CustomDeck | None = None
    topic_param: str
    if pick_mode:
        rows = _type_it_rows_for_progress_keys(
            request.user,
            request,
            words_pick_keys,
            study_level,
            fav_pairs,
            mastery_map,
            hard_map,
        )
        topic_param = CustomCard.TOPIC_OTHER
    else:
        custom_raw = (request.GET.get("custom_deck") or "").strip()
        topic_raw = (request.GET.get("topic") or "").strip().lower()
        if custom_raw.isdigit():
            active_deck = CustomDeck.objects.filter(
                pk=int(custom_raw), student=request.user
            ).first()
            if not active_deck:
                return redirect("vocabulary:type_it_deck_select")
            topic_param = CustomCard.TOPIC_OTHER
        elif topic_raw and _valid_topic(topic_raw):
            topic_param = topic_raw
        else:
            return redirect("vocabulary:type_it_deck_select")

        rows = _type_it_load_rows(
            request=request,
            user=request.user,
            topic_param=topic_param,
            active_deck=active_deck,
            study_level=study_level,
            fav_pairs=fav_pairs,
            mastery_map=mastery_map,
            hard_map=hard_map,
        )

    total_words = len(rows)
    if total_words == 0:
        return redirect("vocabulary:type_it_deck_select")

    if pick_mode:
        scope = "pick:" + ",".join(words_pick_keys)
        if request.session.get("type_it_scope") != scope:
            request.session["type_it_scope"] = scope
            request.session["type_it_topic"] = topic_param
            request.session["type_it_deck_pk"] = None
            request.session["type_it_pick_keys"] = list(words_pick_keys)
            request.session["type_it_pick_query"] = words_q_raw
            request.session["type_it_bands"] = []
            request.session["type_it_history"] = []
            request.session["type_it_done"] = 0
            request.session["type_it_skipped"] = 0
            request.session.modified = True
    else:
        scope = f"{topic_param}:{active_deck.pk if active_deck else ''}"
        if request.session.get("type_it_scope") != scope:
            request.session["type_it_scope"] = scope
            request.session["type_it_topic"] = topic_param
            request.session["type_it_deck_pk"] = active_deck.pk if active_deck else None
            request.session.pop("type_it_pick_keys", None)
            request.session.pop("type_it_pick_query", None)
            request.session["type_it_bands"] = []
            request.session["type_it_history"] = []
            request.session["type_it_done"] = 0
            request.session["type_it_skipped"] = 0
            request.session.modified = True

    try:
        idx_one = int((request.GET.get("index") or "1").strip())
    except ValueError:
        idx_one = 1
    if idx_one > total_words:
        return redirect("vocabulary:type_it_session_result")
    current_index = max(1, min(idx_one, total_words))
    row = rows[current_index - 1]

    topic_labels = dict(_topic_choices_full())
    topic_badge = _type_it_topic_badge_label(row, topic_param, topic_labels)

    ml = int(row.get("mastery_level") or 0)
    if row.get("is_mastered_card"):
        ml = max(ml, 5)
    ml = min(5, max(0, ml))

    word_display = {
        "key": _row_progress_key(row),
        "word": row["word"],
        "part_of_speech": (row.get("part_of_speech") or "").strip(),
        "level": row.get("level"),
        "topic": topic_badge,
        "phonetic": (row.get("phonetic") or "").strip(),
        "definition": (row.get("definition") or "").strip(),
    }
    progress = {
        "mastery_level": ml,
        "mastery_label": _type_it_mastery_label(ml),
    }

    bands = request.session.get("type_it_bands") or []
    session_done = int(request.session.get("type_it_done", 0))
    session_skipped = int(request.session.get("type_it_skipped", 0))
    session_avg_band = round(sum(bands) / len(bands), 1) if bands else None
    session_remaining = max(0, total_words - current_index)

    progress_pct = (
        int(round((current_index - 1) * 100 / total_words)) if total_words else 0
    )
    past_index = total_words + 1
    result_url = reverse("vocabulary:type_it_session_result")
    base = reverse("vocabulary:type_it_session")
    if pick_mode:
        wq = quote(request.session.get("type_it_pick_query") or words_q_raw or "")
        if current_index >= total_words:
            next_url_done = result_url
            next_url_skip = f"{base}?words={wq}&index={past_index}&skip=1"
        else:
            next_idx = current_index + 1
            q = f"?words={wq}&index={next_idx}"
            next_url_done = f"{base}{q}"
            next_url_skip = f"{base}{q}&skip=1"
    elif active_deck:
        if current_index >= total_words:
            next_url_done = result_url
            next_url_skip = (
                f"{base}?custom_deck={active_deck.pk}&index={past_index}&skip=1"
            )
        else:
            next_idx = current_index + 1
            q = f"?custom_deck={active_deck.pk}&index={next_idx}"
            next_url_done = f"{base}{q}"
            next_url_skip = f"{base}{q}&skip=1"
    else:
        if current_index >= total_words:
            next_url_done = result_url
            next_url_skip = (
                f"{base}?topic={quote(topic_param)}&index={past_index}&skip=1"
            )
        else:
            next_idx = current_index + 1
            q = f"?topic={quote(topic_param)}&index={next_idx}"
            next_url_done = f"{base}{q}"
            next_url_skip = f"{base}{q}&skip=1"

    next_index = past_index if current_index >= total_words else current_index + 1

    return render(
        request,
        "vocabulary/type_it_session.html",
        {
            "word": word_display,
            "progress": progress,
            "topic": topic_param,
            "current_index": current_index,
            "total_words": total_words,
            "next_index": next_index,
            "progress_pct": progress_pct,
            "session_done": session_done,
            "session_remaining": session_remaining,
            "session_avg_band": session_avg_band,
            "session_skipped": session_skipped,
            "type_it_check_api_url": reverse("vocabulary:type_it_check_api"),
            "next_url_skip": next_url_skip,
            "next_url_done": next_url_done,
            "type_it_is_last_word": current_index >= total_words,
        },
    )


@login_required
@require_POST
def type_it_check_api(request: HttpRequest) -> JsonResponse:
    """AI evaluation for Type it session; persists TypeItResult and updates session stats."""
    try:
        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)

        word_key = (data.get("word_key") or data.get("word_id") or "").strip()
        student_text = (data.get("student_text") or "").strip()
        mode = (data.get("mode") or "sentence").strip().lower()
        if mode not in ("sentence", "definition"):
            mode = "sentence"

        raw_ielts = data.get("ielts_mode")
        if isinstance(raw_ielts, str):
            ielts_mode = raw_ielts.strip().lower() in ("1", "true", "yes", "on")
        else:
            ielts_mode = bool(raw_ielts) if raw_ielts is not None else True

        if not word_key or not student_text:
            return JsonResponse(
                {"ok": False, "error": "word_key and student_text are required."},
                status=400,
            )
        if len(student_text) > 4000:
            return JsonResponse({"ok": False, "error": "Text is too long."}, status=400)

        topic_param = request.session.get("type_it_topic")
        deck_pk = request.session.get("type_it_deck_pk")
        if not topic_param:
            return JsonResponse(
                {
                    "ok": False,
                    "error": "Session expired. Open Type it from the deck list.",
                },
                status=400,
            )

        study_level = _vocab_level_for_request(request)
        fav_pairs = _favorite_pair_set(request.user)
        mastery_map = mastery_map_for_student(request.user)
        hard_map = times_marked_hard_map_for_student(request.user)

        pick_keys = request.session.get("type_it_pick_keys")
        active_deck = None
        if pick_keys:
            rows = _type_it_rows_for_progress_keys(
                request.user,
                request,
                list(pick_keys),
                study_level,
                fav_pairs,
                mastery_map,
                hard_map,
            )
        else:
            if deck_pk:
                active_deck = CustomDeck.objects.filter(
                    pk=int(deck_pk), student=request.user
                ).first()
                if not active_deck:
                    return JsonResponse({"ok": False, "error": "Invalid deck."}, status=400)

            rows = _type_it_load_rows(
                request=request,
                user=request.user,
                topic_param=str(topic_param),
                active_deck=active_deck,
                study_level=study_level,
                fav_pairs=fav_pairs,
                mastery_map=mastery_map,
                hard_map=hard_map,
            )
        allowed = {_row_progress_key(r) for r in rows}
        if word_key not in allowed:
            return JsonResponse(
                {"ok": False, "error": "Unknown word for this session."},
                status=400,
            )

        row = None
        for r in rows:
            if _row_progress_key(r) == word_key:
                row = r
                break
        if row is None:
            return JsonResponse(
                {"ok": False, "error": "Unknown word for this session."},
                status=400,
            )
        word_text = (row.get("word") or "").strip()
        definition = (row.get("definition") or "").strip()
        pos = (row.get("part_of_speech") or "").strip()
        topic_labels = dict(_topic_choices_full())
        topic_display = _type_it_topic_badge_label(
            row, str(topic_param), topic_labels
        )
        level = _profile_vocab_level_int(request.user)

        try:
            out = evaluate_type_it_session(
                word=word_text,
                definition=definition,
                part_of_speech=pos,
                topic_label=topic_display,
                student_text=student_text,
                mode=mode,
                ielts_mode=ielts_mode,
                level=level,
            )
        except (RuntimeError, json.JSONDecodeError, ValueError, TypeError, KeyError) as exc:
            return JsonResponse({"ok": False, "error": str(exc)}, status=502)

        word_obj = None
        custom_obj = None
        if row.get("is_custom") and row.get("custom_id"):
            custom_obj = CustomCard.objects.filter(
                pk=int(row["custom_id"]), student=request.user
            ).first()
        elif row.get("word_id"):
            word_obj = Word.objects.filter(pk=int(row["word_id"])).first()

        if not word_obj and not custom_obj:
            return JsonResponse({"ok": False, "error": "Word not found."}, status=400)

        TypeItResult.objects.create(
            student=request.user,
            word=word_obj,
            custom_card=custom_obj,
            student_text=student_text,
            mode=mode,
            band_score=float(out["band"]),
            improved_text=out.get("improved") or "",
            ielts_mode=ielts_mode,
            response_json=out,
        )

        bands = list(request.session.get("type_it_bands") or [])
        bands.append(float(out["band"]))
        request.session["type_it_bands"] = bands
        hist = list(request.session.get("type_it_history") or [])
        hist.append(
            {
                "word": word_text,
                "band": float(out["band"]),
                "sentence": student_text[:500],
            }
        )
        request.session["type_it_history"] = hist
        request.session["type_it_done"] = int(request.session.get("type_it_done", 0)) + 1
        request.session.modified = True

        is_sentence = mode == "sentence"
        is_ok = float(out["band"]) >= 6.0
        if is_sentence and is_ok:
            topic_for_record = str(topic_param)
            if word_obj and getattr(word_obj, "topic", None):
                topic_for_record = str(word_obj.topic)
            elif custom_obj and getattr(custom_obj, "topic", None):
                topic_for_record = str(custom_obj.topic)
            record_type_example_success(request.user, word_text, topic_for_record)

        return JsonResponse({"ok": True, **out})
    except Exception as exc:
        logger.exception("type_it_check_api failed")
        return JsonResponse({"ok": False, "error": str(exc)}, status=500)


@login_required
def type_it_session_result(request: HttpRequest) -> HttpResponse:
    """End-of-session summary after the last word or when index runs past the deck."""
    history = list(request.session.get("type_it_history") or [])
    bands_flat = list(request.session.get("type_it_bands") or [])
    if not history and bands_flat:
        history = [
            {"word": "", "band": float(b), "sentence": ""} for b in bands_flat
        ]
    if not history:
        return redirect("vocabulary:type_it_deck_select")

    rows: list[dict] = []
    for item in history:
        b = float(item.get("band") or 0)
        rows.append(
            {
                "word": str(item.get("word") or ""),
                "band": b,
                "sentence": str(item.get("sentence") or ""),
                "band_pct": min(100, max(0, int(round(b / 9.0 * 100)))),
            }
        )

    total = len(rows)
    avg_band = round(sum(r["band"] for r in rows) / total, 1) if total else 0.0
    best = max(rows, key=lambda r: r["band"]) if rows else None
    worst = min(rows, key=lambda r: r["band"]) if rows else None

    request.session["type_it_history"] = []
    request.session["type_it_bands"] = []
    request.session.modified = True

    return render(
        request,
        "vocabulary/type_it_result.html",
        {
            "items": rows,
            "total": total,
            "avg_band": avg_band,
            "best": best,
            "worst": worst,
        },
    )


@login_required
def vocabulary_home(request: HttpRequest) -> HttpResponse:
    """Compact vocabulary dashboard: stats, continue card, and study method shortcuts."""
    user = request.user
    now = timezone.now()
    topic_labels = dict(_topic_choices_full())
    default_topic = Word.TOPIC_CHOICES[0][0]

    all_progress = VocabularyProgress.objects.filter(student=user)
    words_learned = all_progress.count()
    mastered_count = all_progress.filter(mastery_level=5).count()
    mastered_pct = round((mastered_count / words_learned * 100) if words_learned else 0)
    due_count = all_progress.filter(
        next_review__isnull=False, next_review__lte=now
    ).count()
    favored_count = VocabFavorite.objects.filter(user=user).count()

    try:
        streak = int(getattr(user.profile, "streak", 0) or 0)
    except Exception:
        streak = study_streak(user)

    week_ago = now - timedelta(days=7)
    words_this_week = all_progress.filter(last_reviewed__gte=week_ago).count()

    last_progress = (
        all_progress.filter(last_reviewed__isnull=False)
        .order_by("-last_reviewed")
        .select_related("word", "custom_card")
        .first()
    )
    latest_type_it = (
        TypeItResult.objects.filter(student=user)
        .order_by("-created_at")
        .select_related("word", "custom_card")
        .first()
    )

    last_session = None
    if latest_type_it and (
        not last_progress
        or latest_type_it.created_at > last_progress.last_reviewed
    ):
        delta = now - latest_type_it.created_at
        if delta.days == 0:
            ago_label = "Today"
        elif delta.days == 1:
            ago_label = "Yesterday"
        else:
            ago_label = f"{delta.days} days ago"

        topic_label = "My vocabulary"
        if latest_type_it.word_id and latest_type_it.word:
            t = latest_type_it.word.topic
            topic_label = topic_labels.get(t, t)
        elif latest_type_it.custom_card_id and latest_type_it.custom_card:
            t = latest_type_it.custom_card.topic
            topic_label = topic_labels.get(t, t or "My vocabulary")

        topic_slug = None
        if latest_type_it.word_id and latest_type_it.word:
            topic_slug = latest_type_it.word.topic
        elif latest_type_it.custom_card_id and latest_type_it.custom_card:
            topic_slug = latest_type_it.custom_card.topic

        topic_total = 0
        topic_done = 0
        if topic_slug:
            topic_total = all_progress.filter(
                Q(word__topic=topic_slug) | Q(custom_card__topic=topic_slug)
            ).count()
            topic_done = all_progress.filter(
                Q(word__topic=topic_slug) | Q(custom_card__topic=topic_slug),
                mastery_level__gte=3,
            ).count()
            session_pct = round((topic_done / topic_total * 100) if topic_total else 0)
        else:
            session_pct = 0

        topic_done_num = topic_done if topic_slug else 0
        topic_total_num = topic_total if topic_slug else 0
        last_session = {
            "method": "Type it",
            "topic": topic_label,
            "ago": ago_label,
            "session_pct": session_pct,
            "pct": session_pct,
            "done": topic_done_num,
            "total": topic_total_num,
            "url": reverse("vocabulary:type_it_deck_select"),
        }
    elif last_progress:
        delta = now - last_progress.last_reviewed
        if delta.days == 0:
            ago_label = "Today"
        elif delta.days == 1:
            ago_label = "Yesterday"
        else:
            ago_label = f"{delta.days} days ago"

        topic_slug = None
        topic_label = "My vocabulary"
        if last_progress.word_id and last_progress.word:
            topic_slug = last_progress.word.topic
            topic_label = topic_labels.get(topic_slug, topic_slug)
        elif last_progress.custom_card_id and last_progress.custom_card:
            topic_slug = last_progress.custom_card.topic
            topic_label = topic_labels.get(topic_slug, topic_slug or "My vocabulary")

        topic_total = 0
        topic_done = 0
        if topic_slug:
            topic_total = all_progress.filter(
                Q(word__topic=topic_slug) | Q(custom_card__topic=topic_slug)
            ).count()
            topic_done = all_progress.filter(
                Q(word__topic=topic_slug) | Q(custom_card__topic=topic_slug),
                mastery_level__gte=3,
            ).count()
            session_pct = round((topic_done / topic_total * 100) if topic_total else 0)
        else:
            session_pct = 0

        flash_url = reverse("vocabulary:index")
        if topic_slug:
            flash_url = (
                f"{reverse('vocabulary:index')}?topic={quote(topic_slug)}"
                "&panel=flashcards#flashcard"
            )

        topic_done_num = topic_done if topic_slug else 0
        topic_total_num = topic_total if topic_slug else 0
        last_session = {
            "method": "Flashcards",
            "topic": topic_label,
            "ago": ago_label,
            "session_pct": session_pct,
            "pct": session_pct,
            "done": topic_done_num,
            "total": topic_total_num,
            "url": flash_url,
        }

    agg = TypeItResult.objects.filter(student=user).aggregate(avg=Avg("band_score"))
    avg_band = (
        round(agg["avg"], 1) if agg["avg"] is not None else None
    )

    profile = UserProfile.objects.filter(user=user).first()
    level = int(profile.level) if profile else 2

    try:
        due_today = all_progress.filter(
            next_review__isnull=False,
            next_review__date=now.date(),
        ).count()
    except Exception:
        due_today = 0

    try:
        type_it_count = TypeItResult.objects.filter(student=user).count()
    except Exception:
        type_it_count = 0

    context = {
        "words_learned": words_learned,
        "words_tracked": words_learned,
        "words_this_week": words_this_week,
        "streak": streak,
        "mastered_count": mastered_count,
        "mastered": mastered_count,
        "mastered_pct": mastered_pct,
        "due_count": due_count,
        "due_review": due_count,
        "due_today": due_today,
        "favored_count": favored_count,
        "favorites": favored_count,
        "type_it_count": type_it_count,
        "avg_band": avg_band,
        "last_session": last_session,
        "level": level,
        "level_label": {1: "Beginner", 2: "Standard", 3: "Advanced"}.get(
            level, "Beginner"
        ),
        "band_range": {1: "4–5", 2: "5–6.5", 3: "6.5+"}.get(level, "4–5"),
        "default_topic": default_topic,
    }
    return render(request, "vocabulary/vocabulary_home.html", context)


@login_required
def favored_redirect(request: HttpRequest) -> HttpResponse:
    """Alias URL: ``/vocabulary/favored/`` → flashcards index with favorites panel."""
    return redirect(reverse("vocabulary:index") + "?panel=favorites")


@login_required
def vocabulary_guide(request: HttpRequest) -> HttpResponse:
    """Standalone IELTS vocabulary guide (methods, tips, bands, study plan)."""
    return render(request, "vocabulary/guide.html")


def flashcards(request: HttpRequest) -> HttpResponse:
    topic_labels = dict(_topic_choices_full())
    topic_raw = (request.GET.get("topic") or "").strip().lower()
    study_level = _vocab_level_for_request(request)

    active_deck: CustomDeck | None = None
    if request.user.is_authenticated:
        dr = (request.GET.get("deck") or "").strip()
        if dr.isdigit():
            active_deck = CustomDeck.objects.filter(
                pk=int(dr), student=request.user
            ).first()
            if active_deck:
                topic_raw = CustomCard.TOPIC_OTHER

    words_keys_list = _parse_words_param_list(request) or []
    from_words_param = bool(request.user.is_authenticated and words_keys_list)
    if from_words_param:
        active_deck = None
        topic_raw = Word.TOPIC_ENVIRONMENT

    study_mode = bool(topic_raw and _valid_topic(topic_raw))

    now = timezone.now()
    fav_pairs = _favorite_pair_set(request.user)
    mastery_map: dict[str, int] = {}
    struggling_preview: list[str] = []
    struggling_count = 0
    struggling_more = 0
    hard_map: dict[str, int] = {}
    if request.user.is_authenticated:
        mastery_map = mastery_map_for_student(request.user)
        hard_map = times_marked_hard_map_for_student(request.user)
        struggling_preview, struggling_count = get_struggling_banner(
            request.user, limit=3, vocab_level=study_level
        )
        struggling_more = max(0, struggling_count - len(struggling_preview))

    guest_type_ai_left = 0
    if not request.user.is_authenticated:
        guest_type_ai_left = 0 if request.session.get("vocab_type_free_used") else 1

    topic_decks = topic_decks_for_studio(request.user, now, vocab_level=study_level)
    topic_decks = topic_decks + custom_decks_for_studio(
        request.user, now, vocab_level=study_level
    )
    topic_decks_summary = {
        "total_words": sum(d["word_count"] for d in topic_decks),
        "total_mastered": sum(d["mastered_count"] for d in topic_decks),
        "total_due": (
            sum(d["due_count"] for d in topic_decks)
            if request.user.is_authenticated
            else 0
        ),
    }

    study_panel = _parse_study_panel(request) if study_mode else "flashcards"
    study_panel_label = _STUDY_PANEL_LABELS.get(study_panel, "Study")
    level_label_by_num = {n: label for n, label, _ in _CUSTOM_FORM_LEVEL_CARDS}
    level_labels_json = json.dumps(
        {str(k): v for k, v in level_label_by_num.items()}, separators=(",", ":")
    )
    study_level_segment = "All levels"
    if request.user.is_authenticated:
        vl = study_level if study_level is not None else 2
        study_level_segment = (
            f"Level {vl} — {level_label_by_num.get(vl, '')}"
        )
    flash_review_mode = (
        request.user.is_authenticated
        and (request.GET.get("review") or "").strip().lower() in ("1", "true", "yes")
    )
    flash_due_count = 0
    flash_cards_count = 0
    flash_theme_slug = "environment"
    flash_review_cta = False
    flash_deck_emoji = "📖"

    if from_words_param:
        topic_param = Word.TOPIC_ENVIRONMENT
        words_payload = _flash_rows_for_progress_keys(
            request.user, request, now, words_keys_list, mastery_map
        )
        words_list_payload: list[dict] = []
        word_count = len(words_payload)
        flash_due_count = sum(1 for w in words_payload if w.get("due"))
        flash_cards_count = len(words_payload)
        flash_theme_slug = "pick"
        flash_deck_emoji = "✨"
        flash_review_cta = False
        topic_total_words = max(1, word_count)
        topic_progress_pct = 100 if word_count else 0
        ring_r = 16
        ring_c = 2 * math.pi * ring_r
        ring_dash = f"{(topic_progress_pct / 100.0) * ring_c:.2f} {ring_c:.2f}"
        current_topic_label = "Your selection"
    elif study_mode:
        topic_param = topic_raw
        if active_deck:
            words_payload_full = _merged_custom_deck(
                active_deck, request.user, now, request, study_level
            )
            words_payload = words_payload_full
            if flash_review_mode and request.user.is_authenticated:
                words_payload = _apply_review_session_cap(request.user, words_payload)
            word_count = len(words_payload_full)
            flash_due_count = word_count
            flash_cards_count = len(words_payload)
            flash_theme_slug = "named"
            flash_deck_emoji = "📚"
            flash_review_cta = False
            gq_base = CustomCard.objects.filter(
                student=request.user,
                deck=active_deck,
                topic=CustomCard.TOPIC_OTHER,
            )
            if study_level is not None:
                gq_base = gq_base.filter(level=study_level)
            topic_total_words = gq_base.count()
            global_n = 0
            custom_n = topic_total_words
            topic_progress_pct = (
                100
                if topic_total_words == 0
                else min(100, round(word_count / topic_total_words * 100))
            )
            ring_r = 16
            ring_c = 2 * math.pi * ring_r
            ring_dash = f"{(topic_progress_pct / 100.0) * ring_c:.2f} {ring_c:.2f}"
            current_topic_label = active_deck.name
            words_list_payload = _full_word_list_custom_deck(
                active_deck,
                request.user,
                request,
                fav_pairs,
                mastery_map,
                study_level,
                hard_map,
            )
        else:
            words_payload_full = _merged_deck(
                topic_param,
                request.user,
                now,
                request,
                study_level,
                mastery_map,
            )
            word_count = len(words_payload_full)
            flash_due_count = sum(1 for w in words_payload_full if w.get("due"))
            flash_review_cta = bool(
                request.user.is_authenticated and flash_due_count > 0
            )
            if flash_review_mode and request.user.is_authenticated:
                words_payload = [w for w in words_payload_full if w.get("due")]
                words_payload = _apply_review_session_cap(request.user, words_payload)
            else:
                words_payload = words_payload_full
            flash_cards_count = len(words_payload)
            flash_theme_slug = topic_param
            flash_deck_emoji = TOPIC_DECK_EMOJI.get(topic_param, "📖")
            gq = Word.objects.filter(topic=topic_param)
            if study_level is not None:
                gq = gq.filter(level=study_level)
            global_n = gq.count()
            custom_n = 0
            if request.user.is_authenticated:
                cq = CustomCard.objects.filter(student=request.user, topic=topic_param)
                if study_level is not None:
                    cq = cq.filter(level=study_level)
                custom_n = cq.count()
            topic_total_words = global_n + custom_n
            topic_progress_pct = (
                100
                if topic_total_words == 0
                else min(100, round(word_count / topic_total_words * 100))
            )
            ring_r = 16
            ring_c = 2 * math.pi * ring_r
            ring_dash = f"{(topic_progress_pct / 100.0) * ring_c:.2f} {ring_c:.2f}"
            current_topic_label = topic_labels.get(
                topic_param, topic_param.replace("_", " ").title()
            )
            if topic_param == CustomCard.TOPIC_OTHER:
                current_topic_label = "Personal vocabulary"

            words_list_payload = _full_word_list_for_topic(
                topic_param,
                request.user,
                request,
                fav_pairs,
                mastery_map,
                study_level,
                hard_map,
            )
        filter_q = (request.GET.get("words") or request.GET.get("quiz_words") or "").strip()
        if (
            study_panel in ("quiz", "flashcards", "type")
            and filter_q
            and request.user.is_authenticated
        ):
            sel = {x.strip() for x in filter_q.split(",") if x.strip()}
            if active_deck:
                full_rows = _full_word_list_custom_deck(
                    active_deck,
                    request.user,
                    request,
                    fav_pairs,
                    mastery_map,
                    study_level,
                    hard_map,
                )
            else:
                full_rows = _full_word_list_for_topic(
                    topic_param,
                    request.user,
                    request,
                    fav_pairs,
                    mastery_map,
                    study_level,
                    hard_map,
                )
            words_payload = [r for r in full_rows if _row_progress_key(r) in sel]
            word_count = len(words_payload)
            flash_cards_count = len(words_payload)
    else:
        topic_param = Word.TOPIC_CHOICES[0][0]
        words_payload = []
        words_list_payload = []
        word_count = 0
        topic_total_words = 0
        topic_progress_pct = 0
        ring_r = 16
        ring_c = 2 * math.pi * ring_r
        ring_dash = f"0 {ring_c:.2f}"
        current_topic_label = topic_labels.get(topic_param, "")

    deck_q = f"&deck={active_deck.pk}" if active_deck else ""
    flash_study_all_url = (
        f"{reverse('vocabulary:index')}?topic={quote(topic_param)}&panel=flashcards{deck_q}#flashcard"
        if study_mode
        else ""
    )
    flash_review_due_url = (
        f"{reverse('vocabulary:index')}?topic={quote(topic_param)}&panel=flashcards&review=1{deck_q}#flashcard"
        if study_mode
        else ""
    )
    flash_urls_json = json.dumps(
        {
            "studyAll": flash_study_all_url,
            "reviewDue": flash_review_due_url,
            "changeDeck": reverse("vocabulary:index"),
            "caughtUp": flash_study_all_url,
        },
        separators=(",", ":"),
    )

    flash_review_prefs = _flash_review_prefs(request.user)
    flash_review_prefs_json = json.dumps(flash_review_prefs, separators=(",", ":"))

    favorites_payload = _favorites_payload(request.user, request, topic_labels)

    return render(
        request,
        "vocabulary/index.html",
        {
            "current_topic": topic_param,
            "current_topic_label": current_topic_label,
            "topic_choices": _topic_choices_full(),
            "topic_decks": topic_decks,
            "topic_decks_summary": topic_decks_summary,
            "words_payload": words_payload,
            "words_list_payload": words_list_payload,
            "favorites_payload": favorites_payload,
            "struggling_preview": struggling_preview,
            "struggling_count": struggling_count,
            "struggling_more": struggling_more,
            "word_count": word_count,
            "topic_total_words": topic_total_words,
            "topic_progress_pct": topic_progress_pct,
            "topic_ring_dasharray": ring_dash,
            "guest_type_ai_left": guest_type_ai_left,
            "study_mode": study_mode,
            "study_level": study_level,
            "study_panel": study_panel,
            "study_panel_label": study_panel_label,
            "study_level_segment": study_level_segment,
            "level_label_by_num": level_label_by_num,
            "active_deck": active_deck,
            "flash_review_mode": flash_review_mode,
            "flash_due_count": flash_due_count,
            "flash_cards_count": flash_cards_count,
            "flash_theme_slug": flash_theme_slug,
            "flash_review_cta": flash_review_cta,
            "flash_deck_emoji": flash_deck_emoji,
            "level_labels_json": level_labels_json,
            "flash_urls_json": flash_urls_json,
            "flash_review_prefs_json": flash_review_prefs_json,
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def custom_create(request: HttpRequest) -> HttpResponse:
    back_topic = Word.TOPIC_ENVIRONMENT
    if request.method == "POST":
        form = CustomCardForm(request.POST, request.FILES, user=request.user)
        t = (request.POST.get("topic") or "").strip().lower()
        if _valid_topic(t):
            back_topic = t
        if form.is_valid():
            card = form.save(commit=False)
            card.student = request.user
            card.next_review_at = None
            _assign_custom_deck(
                request.user, card, deck=form.cleaned_data.get("deck")
            )
            try:
                card.save()
            except IntegrityError:
                form.add_error(
                    "word",
                    "You already have a card with this word in this topic.",
                )
            else:
                _sync_new_card_to_word_bank(request.user, card)
                messages.success(request, "Flashcard saved.")
                url = reverse("vocabulary:index") + f"?topic={card.topic}"
                if card.deck_id:
                    url += f"&deck={card.deck_id}"
                url += "#flashcard"
                return redirect(url)
    else:
        t = (request.GET.get("topic") or "").strip().lower()
        initial_topic = t if _valid_topic(t) else Word.TOPIC_ENVIRONMENT
        back_topic = initial_topic
        initial = {"topic": initial_topic}
        d_raw = (request.GET.get("deck") or "").strip()
        if d_raw.isdigit():
            dk = CustomDeck.objects.filter(
                pk=int(d_raw), student=request.user
            ).first()
            if dk:
                initial["topic"] = CustomCard.TOPIC_OTHER
                initial["deck"] = dk.pk
        form = CustomCardForm(initial=initial, user=request.user)

    ctx = {
        "form": form,
        "title": "Create flashcard",
        "submit_label": "Save flashcard",
        "back_topic": back_topic,
        "topic_choices": CustomCard.TOPIC_CHOICES,
        "user_vocab_level": _profile_vocab_level_int(request.user),
    }
    return render(request, "vocabulary/custom_form.html", ctx)


@login_required
@require_http_methods(["GET", "POST"])
def custom_edit(request: HttpRequest, pk: int) -> HttpResponse:
    card = get_object_or_404(CustomCard, pk=pk, student=request.user)
    if request.method == "POST":
        form = CustomCardForm(request.POST, request.FILES, instance=card, user=request.user)
        if form.is_valid():
            card = form.save(commit=False)
            _assign_custom_deck(
                request.user, card, deck=form.cleaned_data.get("deck")
            )
            try:
                card.save()
            except IntegrityError:
                form.add_error(
                    "word",
                    "You already have a card with this word in this topic.",
                )
            else:
                messages.success(request, "Flashcard updated.")
                red = reverse("vocabulary:index") + f"?topic={card.topic}"
                if card.deck_id:
                    red += f"&deck={card.deck_id}"
                return redirect(red + "#flashcard")
    else:
        form = CustomCardForm(instance=card, user=request.user)

    ctx = {
        "form": form,
        "title": "Edit flashcard",
        "submit_label": "Save changes",
        "card": card,
        "back_topic": card.topic,
        "topic_choices": CustomCard.TOPIC_CHOICES,
        "user_vocab_level": _profile_vocab_level_int(request.user),
    }
    return render(request, "vocabulary/custom_form.html", ctx)


@login_required
@require_POST
def custom_delete(request: HttpRequest, pk: int) -> HttpResponse:
    card = get_object_or_404(CustomCard, pk=pk, student=request.user)
    topic = card.topic
    card.delete()
    messages.success(request, "Flashcard deleted.")
    return redirect(reverse("vocabulary:index") + f"?topic={topic}#flashcard")


@login_required
@require_POST
def custom_master(request: HttpRequest, pk: int) -> HttpResponse:
    card = get_object_or_404(CustomCard, pk=pk, student=request.user)
    card.is_mastered = True
    card.save(update_fields=["is_mastered"])
    messages.success(request, "Marked as mastered — removed from review deck.")
    return redirect(reverse("vocabulary:index") + f"?topic={card.topic}#flashcard")


@login_required
@require_POST
def custom_reviewed(request: HttpRequest, pk: int) -> HttpResponse:
    """Spaced repetition: schedule next appearance."""
    card = get_object_or_404(CustomCard, pk=pk, student=request.user)
    idx = min(card.review_count, len(SR_INTERVALS) - 1)
    days = SR_INTERVALS[idx]
    card.review_count += 1
    card.next_review_at = timezone.now() + timedelta(days=days)
    card.save(update_fields=["review_count", "next_review_at"])
    messages.info(request, f"Next review in {days} day(s).")
    return redirect(reverse("vocabulary:index") + f"?topic={card.topic}#flashcard")


@login_required
@require_POST
def custom_ai_fill(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)

    word = (data.get("word") or "").strip()
    topic = (data.get("topic") or "general").strip().lower()
    level = _profile_vocab_level_int(request.user)

    if not word:
        return JsonResponse({"ok": False, "error": "Word is required."}, status=400)

    try:
        out = generate_definition_and_example(word=word, topic=topic, level=level)
    except (RuntimeError, json.JSONDecodeError, KeyError, ValueError) as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=502)

    return JsonResponse({"ok": True, **out})


@login_required
@require_POST
def custom_ai_image_preview(request: HttpRequest) -> JsonResponse:
    """Return base64 PNG for the create/edit form (user attaches file via JS)."""
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)

    word = (data.get("word") or "").strip()
    definition = (data.get("definition") or "").strip()
    topic = (data.get("topic") or "general").strip().lower()
    level = _profile_vocab_level_int(request.user)

    if not word:
        return JsonResponse({"ok": False, "error": "Word is required."}, status=400)

    try:
        png = generate_illustration_png_bytes(
            word=word, definition=definition, topic=topic, level=level
        )
    except RuntimeError as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=502)
    except Exception as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=502)

    return JsonResponse(
        {
            "ok": True,
            "image_base64": base64.standard_b64encode(png).decode("ascii"),
        }
    )


@login_required
@require_POST
def custom_ai_image_save(request: HttpRequest, pk: int) -> JsonResponse:
    """Generate illustration and save onto an existing custom card (e.g. from flashcards)."""
    card = get_object_or_404(CustomCard, pk=pk, student=request.user)
    try:
        png = generate_illustration_png_bytes(
            word=card.word,
            definition=(card.definition or "").strip(),
            topic=card.topic,
            level=card.level,
        )
    except RuntimeError as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=502)
    except Exception as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=502)

    fname = f"vocab_ai_{card.pk}_{uuid.uuid4().hex[:10]}.png"
    card.definition_image.save(fname, ContentFile(png), save=True)
    image_url = _absolute_media_url(request, card.definition_image)
    return JsonResponse({"ok": True, "image_url": image_url})


@require_POST
def type_check_sentence(request: HttpRequest) -> JsonResponse:
    """AI: judge example sentence or student definition; guests get one free check per session."""
    if not request.user.is_authenticated and request.session.get("vocab_type_free_used"):
        return JsonResponse(
            {
                "ok": False,
                "error": "You've used your free AI check. Log in for unlimited practice.",
                "need_login": True,
            },
            status=403,
        )

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)

    word = (data.get("word") or "").strip()
    topic = (data.get("topic") or "general").strip().lower()
    sentence = (data.get("sentence") or "").strip()
    deck_definition = (data.get("deck_definition") or "").strip()
    deck_example = (data.get("deck_example") or "").strip()
    mode = (data.get("mode") or "example").strip().lower()
    if mode not in ("example", "definition"):
        mode = "example"

    raw_ielts = data.get("ielts_mode")
    if isinstance(raw_ielts, str):
        ielts_mode = raw_ielts.strip().lower() in ("1", "true", "yes", "on")
    else:
        ielts_mode = bool(raw_ielts) if raw_ielts is not None else True

    if request.user.is_authenticated:
        level = _profile_vocab_level_int(request.user)
    else:
        try:
            level = int(data.get("level") or 2)
        except (TypeError, ValueError):
            level = 2
        level = level if level in (1, 2, 3) else 2

    if not word:
        return JsonResponse({"ok": False, "error": "Word is required."}, status=400)
    if not sentence:
        err = "Write a definition first." if mode == "definition" else "Write a sentence first."
        return JsonResponse({"ok": False, "error": err}, status=400)
    if len(sentence) > 2500:
        return JsonResponse({"ok": False, "error": "Text is too long."}, status=400)

    try:
        out = check_type_practice(
            word=word,
            topic=topic,
            level=level,
            student_text=sentence,
            deck_definition=deck_definition,
            deck_example=deck_example,
            mode=mode,
            ielts_mode=ielts_mode,
        )
    except (RuntimeError, json.JSONDecodeError, KeyError, ValueError) as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=502)

    is_ok = bool(out.get("is_correct", out.get("correct")))
    if request.user.is_authenticated and is_ok and mode == "example":
        record_type_example_success(request.user, word, topic)

    if not request.user.is_authenticated:
        request.session["vocab_type_free_used"] = True
        request.session.modified = True

    return JsonResponse({"ok": True, **out})


@login_required
@require_http_methods(["GET"])
def deck_create(request: HttpRequest) -> HttpResponse:
    t = (request.GET.get("topic") or "").strip().lower()
    initial_topic = t if _valid_topic(t) else Word.TOPIC_ENVIRONMENT
    return render(
        request,
        "vocabulary/deck_create.html",
        {
            "max_cards": MAX_CARDS,
            "user_vocab_level": _profile_vocab_level_int(request.user),
            "topic_choices": _topic_choices_full(),
            "initial_topic": initial_topic,
        },
    )


@login_required
@require_POST
def deck_create_save(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)

    name = str(data.get("name") or "").strip()[:120]
    if not name:
        return JsonResponse({"ok": False, "error": "Deck name is required."}, status=400)

    description = str(data.get("description") or "").strip()[:4000]

    level = _profile_vocab_level_int(request.user)

    raw_cards = data.get("cards")
    if not isinstance(raw_cards, list):
        return JsonResponse({"ok": False, "error": "Expected a cards array."}, status=400)
    if len(raw_cards) > MAX_CARDS * 3:
        return JsonResponse({"ok": False, "error": "Too many rows."}, status=400)

    practice = bool(data.get("practice"))

    try:
        deck = CustomDeck.objects.create(
            student=request.user,
            name=name,
            description=description,
        )
    except IntegrityError:
        return JsonResponse(
            {
                "ok": False,
                "error": "You already have a deck with this name. Choose another name.",
            },
            status=400,
        )

    created = 0
    skipped: list[str] = []
    for item in raw_cards:
        if not isinstance(item, dict):
            continue
        w = str(item.get("word") or "").strip()[:255]
        if not w:
            continue
        definition = str(item.get("definition") or "").strip()[:4000]
        png_bytes: bytes | None = None
        img_b64 = item.get("image_base64")
        if img_b64 and isinstance(img_b64, str):
            raw_b64 = img_b64.strip()
            if raw_b64:
                try:
                    png_bytes = base64.standard_b64decode(raw_b64)
                except (binascii.Error, ValueError):
                    png_bytes = None
                if png_bytes and len(png_bytes) > 2 * 1024 * 1024:
                    png_bytes = None
        card = CustomCard(
            student=request.user,
            deck=deck,
            word=w,
            definition=definition,
            example_sentence="",
            topic=CustomCard.TOPIC_OTHER,
            level=level,
            next_review_at=None,
        )
        try:
            card.save()
        except IntegrityError:
            skipped.append(w)
        else:
            if png_bytes:
                fname = f"vocab_deck_{uuid.uuid4().hex[:12]}.png"
                card.definition_image.save(fname, ContentFile(png_bytes), save=True)
            _sync_new_card_to_word_bank(request.user, card)
            created += 1

    if created == 0:
        deck.delete()
        return JsonResponse(
            {"ok": False, "error": "Add at least one card with a term."},
            status=400,
        )

    index_base = request.build_absolute_uri(reverse("vocabulary:index"))
    sep = "&" if "?" in index_base else "?"
    base_q = (
        f"{index_base}{sep}topic={CustomCard.TOPIC_OTHER}&deck={deck.pk}"
    )
    redirect_url = f"{base_q}&panel=flashcards#flashcard" if practice else f"{base_q}#flashcard"

    return JsonResponse(
        {
            "ok": True,
            "created": created,
            "skipped": skipped,
            "deck_pk": deck.pk,
            "redirect_url": redirect_url,
        }
    )


@login_required
@require_http_methods(["GET"])
def flashcard_set_create(request: HttpRequest) -> HttpResponse:
    t = (request.GET.get("topic") or "").strip().lower()
    initial_topic = t if _valid_topic(t) else Word.TOPIC_ENVIRONMENT
    return render(
        request,
        "vocabulary/flashcard_set_create.html",
        {
            "max_cards": MAX_CARDS,
            "topic_choices": _topic_choices_full(),
            "initial_topic": initial_topic,
            "user_vocab_level": _profile_vocab_level_int(request.user),
        },
    )


@login_required
@require_POST
def flashcard_set_generate(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)

    prompt = (data.get("prompt") or "").strip()
    if len(prompt) > 120_000:
        return JsonResponse({"ok": False, "error": "Prompt is too long."}, status=400)
    if not prompt:
        return JsonResponse({"ok": False, "error": "Enter a prompt (e.g. medical vocabulary)."}, status=400)

    try:
        count = int(data.get("count") or 10)
    except (TypeError, ValueError):
        count = 10
    count = max(1, min(count, MAX_CARDS))

    level = _profile_vocab_level_int(request.user)

    topic_param = (data.get("topic") or "").strip().lower()
    if not _valid_topic(topic_param):
        return JsonResponse({"ok": False, "error": "Choose a topic."}, status=400)

    labels = dict(_topic_choices_full())
    topic_label = labels.get(topic_param, topic_param)

    try:
        cards, detected_topic = generate_flashcard_set(
            prompt=prompt,
            count=count,
            level=level,
            topic_slug=topic_param,
            topic_label=topic_label,
        )
    except (RuntimeError, json.JSONDecodeError, KeyError, ValueError) as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=502)

    effective_topic = topic_param
    if not _valid_topic(detected_topic):
        detected_topic = CustomCard.TOPIC_OTHER

    warn = None
    if len(cards) < count:
        warn = f"Got {len(cards)} cards (you asked for {count}). You can edit them or generate again."

    return JsonResponse(
        {
            "ok": True,
            "cards": cards,
            "warn": warn,
            "detected_topic": effective_topic,
            "topic_label": labels.get(effective_topic, topic_label),
        }
    )


@login_required
@require_POST
def flashcard_set_save(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)

    topic = (data.get("topic") or "").strip().lower()
    if not _valid_topic(topic):
        topic = CustomCard.TOPIC_OTHER

    level = _profile_vocab_level_int(request.user)

    raw_cards = data.get("cards")
    if not isinstance(raw_cards, list):
        return JsonResponse({"ok": False, "error": "Expected a cards array."}, status=400)
    if len(raw_cards) > MAX_CARDS * 3:
        return JsonResponse({"ok": False, "error": "Too many rows."}, status=400)

    set_title = str(data.get("set_title") or "").strip()[:120]
    set_description = str(data.get("set_description") or "").strip()[:4000]

    deck_obj = None
    if topic == CustomCard.TOPIC_OTHER:
        if not set_title:
            return JsonResponse(
                {"ok": False, "error": "Give your flashcard set a title."}, status=400
            )
        deck_obj, created_set = CustomDeck.objects.get_or_create(
            student=request.user,
            name=set_title,
            defaults={"description": set_description},
        )
        if not created_set and (deck_obj.description or "") != set_description:
            deck_obj.description = set_description
            deck_obj.save(update_fields=["description"])

    created = 0
    skipped: list[str] = []

    for item in raw_cards:
        if not isinstance(item, dict):
            continue
        w = str(item.get("word") or "").strip()[:255]
        if not w:
            continue
        definition = str(item.get("definition") or "").strip()[:4000]
        example_sentence = str(item.get("example_sentence") or "").strip()[:4000]
        card = CustomCard(
            student=request.user,
            deck=deck_obj,
            word=w,
            definition=definition,
            example_sentence=example_sentence,
            topic=topic,
            level=level,
            next_review_at=None,
        )
        try:
            card.save()
        except IntegrityError:
            skipped.append(w)
        else:
            _sync_new_card_to_word_bank(request.user, card)
            created += 1

    return JsonResponse(
        {
            "ok": True,
            "created": created,
            "skipped": skipped,
            "topic": topic,
        }
    )


@login_required
@require_POST
def word_bank_add_from_vocab(request: HttpRequest) -> JsonResponse:
    """Add a vocabulary row to the writing word bank (same shape as new custom card)."""
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)

    kind = (data.get("kind") or "").strip().lower()
    try:
        pk = int(data.get("id"))
    except (TypeError, ValueError):
        return JsonResponse({"ok": False, "error": "Invalid id."}, status=400)

    if kind == "word":
        word = get_object_or_404(Word, pk=pk)
        phrase = f"{word.word} — {(word.definition or '').strip()[:450]}".strip()
        if len(phrase) < 2:
            phrase = word.word
        WordBankEntry.objects.create(user=request.user, phrase=phrase[:500], essay=None)
        return JsonResponse({"ok": True})

    if kind == "custom":
        card = get_object_or_404(CustomCard, pk=pk, student=request.user)
        phrase = f"{card.word} — {(card.definition or '').strip()[:450]}".strip()
        if len(phrase) < 2:
            phrase = card.word
        WordBankEntry.objects.create(user=request.user, phrase=phrase[:500], essay=None)
        return JsonResponse({"ok": True})

    return JsonResponse({"ok": False, "error": "Use kind word or custom."}, status=400)


@login_required
@require_POST
def vocab_toggle_favorite(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)

    kind = (data.get("kind") or "").strip().lower()
    try:
        pk = int(data.get("id"))
    except (TypeError, ValueError):
        return JsonResponse({"ok": False, "error": "Invalid id."}, status=400)

    if kind == "word":
        word = get_object_or_404(Word, pk=pk)
        fav = VocabFavorite.objects.filter(user=request.user, word=word).first()
        if fav:
            fav.delete()
            return JsonResponse({"ok": True, "favorited": False})
        VocabFavorite.objects.create(user=request.user, word=word, custom_card=None)
        return JsonResponse({"ok": True, "favorited": True})

    if kind == "custom":
        card = get_object_or_404(CustomCard, pk=pk, student=request.user)
        fav = VocabFavorite.objects.filter(user=request.user, custom_card=card).first()
        if fav:
            fav.delete()
            return JsonResponse({"ok": True, "favorited": False})
        VocabFavorite.objects.create(user=request.user, word=None, custom_card=card)
        return JsonResponse({"ok": True, "favorited": True})

    return JsonResponse({"ok": False, "error": "Use kind word or custom."}, status=400)


@login_required
@require_POST
def progress_review_settings(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)

    try:
        easy = int(data.get("review_easy_days", 7))
        hard = int(data.get("review_hard_days", 1))
        sess = int(data.get("review_session_size", 20))
    except (TypeError, ValueError):
        return JsonResponse({"ok": False, "error": "Invalid values."}, status=400)

    if easy not in _REVIEW_EASY_DAYS_ALLOWED:
        return JsonResponse({"ok": False, "error": "Invalid easy interval."}, status=400)
    if hard not in _REVIEW_HARD_DAYS_ALLOWED:
        return JsonResponse({"ok": False, "error": "Invalid hard interval."}, status=400)
    if sess not in _REVIEW_SESSION_SIZE_ALLOWED:
        return JsonResponse({"ok": False, "error": "Invalid session size."}, status=400)

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.review_easy_days = easy
    profile.review_hard_days = hard
    profile.review_session_size = sess
    profile.save(
        update_fields=["review_easy_days", "review_hard_days", "review_session_size"]
    )

    return JsonResponse(
        {
            "ok": True,
            "review_easy_days": easy,
            "review_hard_days": hard,
            "review_session_size": sess,
        }
    )


@login_required
@require_POST
def progress_flashcard_rating(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)

    kind = (data.get("kind") or "").strip().lower()
    rating = (data.get("rating") or "").strip().lower()
    try:
        pk = int(data.get("id"))
    except (TypeError, ValueError):
        return JsonResponse({"ok": False, "error": "Invalid id."}, status=400)

    try:
        prog = record_flashcard_rating(request.user, kind, pk, rating)
    except Word.DoesNotExist:
        return JsonResponse({"ok": False, "error": "Word not found."}, status=404)
    except CustomCard.DoesNotExist:
        return JsonResponse({"ok": False, "error": "Card not found."}, status=404)
    except ValueError as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=400)

    return JsonResponse(
        {
            "ok": True,
            "mastery_level": prog.mastery_level,
            "times_seen": prog.times_seen,
            "times_marked_hard": prog.times_marked_hard,
        }
    )


@login_required
@require_POST
def progress_session_end(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)

    keys = data.get("keys")
    if not isinstance(keys, list):
        return JsonResponse({"ok": False, "error": "Expected keys array."}, status=400)
    key_strs = [str(x) for x in keys[:500]]
    n = end_session_for_keys(request.user, key_strs)
    return JsonResponse({"ok": True, "updated": n})


@login_required
@require_http_methods(["GET"])
def struggling_practice(request: HttpRequest) -> HttpResponse:
    deck = build_struggling_deck_payload(
        request,
        request.user,
        vocab_level=_profile_vocab_level_int(request.user),
    )
    return render(
        request,
        "vocabulary/struggling.html",
        {
            "deck": deck,
            "struggling_count": len(deck),
        },
    )