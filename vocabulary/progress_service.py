"""Vocabulary per-word progress: flashcard ratings, sessions, mastery levels."""
from __future__ import annotations

from collections import defaultdict
from datetime import timedelta

from django.db.models import Q
from django.http import HttpRequest
from django.utils import timezone

from boostingscore.models import UserProfile

from vocabulary.icon_registry import TOPIC_ICONS, resolve_icon

from .models import CustomCard, CustomDeck, VocabularyProgress, Word


def _absolute_media_url(request: HttpRequest, file_field) -> str:
    if not file_field or not getattr(file_field, "name", ""):
        return ""
    try:
        path = file_field.url
    except ValueError:
        return ""
    return request.build_absolute_uri(path)


def progress_key_for_word(word_pk: int) -> str:
    return f"w:{word_pk}"


def progress_key_for_custom(custom_pk: int) -> str:
    return f"c:{custom_pk}"


def word_is_due_for_flash_review(
    user,
    now,
    word_pk: int,
    prog: VocabularyProgress | None,
    mastery_map: dict[str, int],
) -> bool:
    """Whether a global Word should appear in the spaced-repetition review queue."""
    if not user.is_authenticated:
        return True
    wk = progress_key_for_word(word_pk)
    if mastery_map.get(wk, 0) >= 5:
        return False
    if prog is None:
        return True
    nr = prog.next_review
    if nr is None:
        return True
    return nr <= now


def count_due_global_words_in_topic(
    user, now, word_pks: list[int], mastery_map: dict[str, int]
) -> int:
    if not user.is_authenticated or not word_pks:
        return 0
    prog_by: dict[int, VocabularyProgress] = {}
    for p in VocabularyProgress.objects.filter(
        student=user, word_id__in=word_pks
    ).only("word_id", "next_review"):
        prog_by[p.word_id] = p
    n = 0
    for wpk in word_pks:
        if word_is_due_for_flash_review(
            user, now, wpk, prog_by.get(wpk), mastery_map
        ):
            n += 1
    return n


def get_or_create_progress(
    student, *, word: Word | None = None, custom_card: CustomCard | None = None
) -> VocabularyProgress:
    if word is not None and custom_card is None:
        prog, _ = VocabularyProgress.objects.get_or_create(
            student=student,
            word=word,
            defaults={"custom_card": None},
        )
        return prog
    if custom_card is not None and word is None:
        prog, _ = VocabularyProgress.objects.get_or_create(
            student=student,
            custom_card=custom_card,
            defaults={"word": None},
        )
        return prog
    raise ValueError("Exactly one of word or custom_card must be set")


def review_interval_days_for_student(student) -> tuple[int, int]:
    row = (
        UserProfile.objects.filter(user=student)
        .values_list("review_easy_days", "review_hard_days")
        .first()
    )
    if not row:
        return 7, 1
    easy, hard = row
    return (
        int(easy) if easy is not None else 7,
        int(hard) if hard is not None else 1,
    )


def update_mastery_level(
    progress: VocabularyProgress, *, easy_interval_days: float = 7.0
) -> None:
    ts = progress.times_seen
    tc = progress.times_correct
    acc = (tc / ts * 100.0) if ts > 0 else 0.0
    now = timezone.now()
    nr = progress.next_review
    days_ahead = 0.0
    if nr:
        days_ahead = (nr - now).total_seconds() / 86400.0

    if tc >= 10 and acc >= 90.0 and days_ahead >= easy_interval_days:
        progress.mastery_level = 5
    elif tc >= 6 and acc >= 75.0 and progress.type_success_count >= 1:
        progress.mastery_level = 4
    elif tc >= 3 and acc >= 60.0:
        progress.mastery_level = 3
    elif tc >= 1:
        progress.mastery_level = 2
    else:
        progress.mastery_level = 1


def record_flashcard_rating(student, kind: str, pk: int, rating: str) -> VocabularyProgress:
    rating = (rating or "").strip().lower()
    if rating not in ("easy", "hard"):
        raise ValueError("rating must be easy or hard")

    if kind == "word":
        w = Word.objects.get(pk=pk)
        prog = get_or_create_progress(student, word=w)
    elif kind == "custom":
        c = CustomCard.objects.get(pk=pk, student=student)
        prog = get_or_create_progress(student, custom_card=c)
    else:
        raise ValueError("kind must be word or custom")

    easy_days, hard_days = review_interval_days_for_student(student)
    now = timezone.now()
    prog.times_seen += 1
    prog.last_reviewed = now
    if rating == "easy":
        prog.times_correct += 1
        prog.next_review = now + timedelta(days=easy_days)
    else:
        prog.times_wrong += 1
        prog.times_marked_hard += 1
        prog.next_review = now + timedelta(days=hard_days)

    update_mastery_level(prog, easy_interval_days=float(easy_days))
    prog.save()
    return prog


def end_session_for_keys(student, keys: list[str]) -> int:
    """Increment sessions_seen for progress rows matching keys (w:pk / c:pk). Returns count updated."""
    today = timezone.now().date()
    updated = 0
    for key in keys:
        if not key or ":" not in key:
            continue
        prefix, _, sid = key.partition(":")
        try:
            pk = int(sid)
        except ValueError:
            continue
        prog = None
        try:
            if prefix == "w":
                w = Word.objects.get(pk=pk)
                prog = VocabularyProgress.objects.filter(student=student, word=w).first()
            elif prefix == "c":
                c = CustomCard.objects.get(pk=pk, student=student)
                prog = VocabularyProgress.objects.filter(
                    student=student, custom_card=c
                ).first()
        except (Word.DoesNotExist, CustomCard.DoesNotExist):
            continue
        if not prog:
            continue
        prog.sessions_seen += 1
        prog.last_session_date = today
        prog.save(update_fields=["sessions_seen", "last_session_date"])
        updated += 1
    return updated


def get_struggling_queryset(student, vocab_level: int | None = None):
    qs = (
        VocabularyProgress.objects.filter(
            student=student,
            sessions_seen__gte=3,
            times_marked_hard__gte=2,
        )
        .filter(Q(word__isnull=False) | Q(custom_card__isnull=False))
        .select_related("word", "custom_card")
        .order_by("-times_marked_hard", "-sessions_seen")
    )
    if vocab_level is not None:
        qs = qs.filter(
            Q(word__isnull=False, word__level=vocab_level)
            | Q(custom_card__isnull=False, custom_card__level=vocab_level)
        )
    return qs


def get_struggling_banner(student, limit: int = 3, vocab_level: int | None = None):
    qs = get_struggling_queryset(student, vocab_level=vocab_level)
    total = qs.count()
    names: list[str] = []
    for p in qs[:limit]:
        if p.word_id and p.word:
            names.append(p.word.word)
        elif p.custom_card_id and p.custom_card:
            names.append(p.custom_card.word)
    return names, total


def build_struggling_deck_payload(
    request: HttpRequest, student, vocab_level: int | None = None
) -> list[dict]:
    """Same shape as vocabulary deck items for flashcard JS."""
    out: list[dict] = []
    for p in get_struggling_queryset(student, vocab_level=vocab_level):
        if p.word_id and p.word:
            w = p.word
            out.append(
                {
                    "word": w.word,
                    "definition": w.definition or "",
                    "example": w.example_sentence or "",
                    "level": w.level,
                    "part_of_speech": (w.part_of_speech or "").strip(),
                    "is_custom": False,
                    "custom_id": None,
                    "word_id": w.pk,
                    "image_url": _absolute_media_url(request, w.definition_image),
                }
            )
        elif p.custom_card_id and p.custom_card:
            c = p.custom_card
            out.append(
                {
                    "word": c.word,
                    "definition": c.definition or "",
                    "example": c.example_sentence or "",
                    "level": c.level,
                    "part_of_speech": (c.part_of_speech or "").strip(),
                    "is_custom": True,
                    "custom_id": c.pk,
                    "word_id": None,
                    "image_url": _absolute_media_url(request, c.definition_image),
                }
            )
    return out


def mastery_map_for_student(student) -> dict[str, int]:
    m: dict[str, int] = {}
    for p in VocabularyProgress.objects.filter(student=student).only(
        "word_id", "custom_card_id", "mastery_level"
    ):
        if p.word_id:
            m[progress_key_for_word(p.word_id)] = p.mastery_level
        if p.custom_card_id:
            m[progress_key_for_custom(p.custom_card_id)] = p.mastery_level
    return m


def times_marked_hard_map_for_student(student) -> dict[str, int]:
    """Map progress keys (w:pk / c:pk) to times_marked_hard for word list struggling badge."""
    m: dict[str, int] = {}
    for p in VocabularyProgress.objects.filter(student=student).only(
        "word_id", "custom_card_id", "times_marked_hard"
    ):
        if p.word_id:
            m[progress_key_for_word(p.word_id)] = p.times_marked_hard
        if p.custom_card_id:
            m[progress_key_for_custom(p.custom_card_id)] = p.times_marked_hard
    return m


TOPIC_DECK_ICON = {
    Word.TOPIC_ENVIRONMENT: TOPIC_ICONS["environment"],
    Word.TOPIC_HEALTH: TOPIC_ICONS["health"],
    Word.TOPIC_TECHNOLOGY: TOPIC_ICONS["technology"],
    Word.TOPIC_EDUCATION: TOPIC_ICONS["education"],
    Word.TOPIC_SOCIETY: TOPIC_ICONS["society"],
    CustomCard.TOPIC_OTHER: TOPIC_ICONS["other"],
}


def topic_decks_for_studio(user, now, vocab_level: int | None = None) -> list[dict]:
    """
    Per-topic deck cards for the vocabulary picker modal: counts, due custom
    cards, mastery progress, last studied. Order: five themes, then personal.
    """
    topic_slugs = [t[0] for t in Word.TOPIC_CHOICES] + [CustomCard.TOPIC_OTHER]
    labels = {t[0]: t[1] for t in Word.TOPIC_CHOICES}
    labels[CustomCard.TOPIC_OTHER] = "My vocabulary"

    words_by_topic: dict[str, list[int]] = defaultdict(list)
    wq = Word.objects.all()
    if vocab_level is not None:
        wq = wq.filter(level=vocab_level)
    for pk, topic in wq.values_list("pk", "topic"):
        words_by_topic[topic].append(pk)

    customs_by_topic: dict[str, list[CustomCard]] = defaultdict(list)
    due_by_topic: dict[str, int] = defaultdict(int)
    if user.is_authenticated:
        cq = CustomCard.objects.filter(student=user)
        if vocab_level is not None:
            cq = cq.filter(level=vocab_level)
        for card in cq.only("pk", "topic", "is_mastered", "next_review_at"):
            customs_by_topic[card.topic].append(card)
            if not card.is_mastered and (
                card.next_review_at is None or card.next_review_at <= now
            ):
                due_by_topic[card.topic] += 1

    mastery_map = mastery_map_for_student(user) if user.is_authenticated else {}

    last_by_topic: dict[str, object | None] = {}
    if user.is_authenticated:
        progs = VocabularyProgress.objects.filter(student=user).select_related(
            "word", "custom_card"
        )
        for p in progs:
            slug = None
            if p.word_id and p.word:
                if vocab_level is not None and p.word.level != vocab_level:
                    continue
                slug = p.word.topic
            elif p.custom_card_id and p.custom_card:
                if vocab_level is not None and p.custom_card.level != vocab_level:
                    continue
                slug = p.custom_card.topic
            if not slug:
                continue
            cand = []
            if p.last_reviewed:
                cand.append(p.last_reviewed.date())
            if p.last_session_date:
                cand.append(p.last_session_date)
            if not cand:
                continue
            best = max(cand)
            prev = last_by_topic.get(slug)
            last_by_topic[slug] = best if prev is None else max(prev, best)

    rows: list[dict] = []
    for slug in topic_slugs:
        wpks = words_by_topic.get(slug, [])
        cards = customs_by_topic.get(slug, [])
        word_count = len(wpks) + len(cards)

        mastered = 0
        for wpk in wpks:
            if mastery_map.get(progress_key_for_word(wpk), 0) >= 5:
                mastered += 1
        for c in cards:
            if c.is_mastered or mastery_map.get(progress_key_for_custom(c.pk), 0) >= 5:
                mastered += 1

        last_d = last_by_topic.get(slug)
        due_count = due_by_topic.get(slug, 0) if user.is_authenticated else 0
        if user.is_authenticated and wpks:
            due_count += count_due_global_words_in_topic(
                user, now, wpks, mastery_map
            )

        progress_pct = (
            min(100, int(round(mastered * 100 / word_count))) if word_count else 0
        )

        rows.append(
            {
                "slug": slug,
                "label": labels.get(slug, slug),
                "emoji": TOPIC_DECK_ICON.get(slug, "book"),
                "word_count": word_count,
                "mastered_count": mastered,
                "due_count": due_count,
                "last_studied": last_d,
                "is_personal": slug == CustomCard.TOPIC_OTHER,
                "is_custom_deck": False,
                "deck_pk": None,
                "progress_pct": progress_pct,
            }
        )
    return rows


def custom_decks_for_studio(user, now, vocab_level: int | None = None) -> list[dict]:
    """Named custom decks for deck picker (alongside topic decks)."""
    if not user.is_authenticated:
        return []

    mastery_map = mastery_map_for_student(user)
    rows: list[dict] = []

    last_by_deck: dict[int, object] = {}
    progs = VocabularyProgress.objects.filter(student=user).select_related(
        "custom_card__deck"
    )
    for p in progs:
        if not p.custom_card_id or not p.custom_card:
            continue
        if vocab_level is not None and p.custom_card.level != vocab_level:
            continue
        d = p.custom_card.deck
        if d is None:
            continue
        dk = d.pk
        cand = []
        if p.last_reviewed:
            cand.append(p.last_reviewed.date())
        if p.last_session_date:
            cand.append(p.last_session_date)
        if not cand:
            continue
        best = max(cand)
        prev = last_by_deck.get(dk)
        last_by_deck[dk] = best if prev is None else max(prev, best)

    for d in CustomDeck.objects.filter(student=user).order_by("-created_at"):
        dq = CustomCard.objects.filter(student=user, deck=d)
        if vocab_level is not None:
            dq = dq.filter(level=vocab_level)
        cards = list(dq.only("pk", "is_mastered", "next_review_at"))
        word_count = len(cards)
        mastered = 0
        due_count = 0
        for c in cards:
            if c.is_mastered or mastery_map.get(progress_key_for_custom(c.pk), 0) >= 5:
                mastered += 1
            if not c.is_mastered and (
                c.next_review_at is None or c.next_review_at <= now
            ):
                due_count += 1

        last_d = last_by_deck.get(d.pk)
        progress_pct = (
            min(100, int(round(mastered * 100 / word_count))) if word_count else 0
        )

        rows.append(
            {
                "slug": f"deck-{d.pk}",
                "label": d.name,
                "emoji": resolve_icon(getattr(d, "emoji", None), "folder"),
                "word_count": word_count,
                "mastered_count": mastered,
                "due_count": due_count,
                "last_studied": last_d,
                "is_personal": False,
                "is_custom_deck": True,
                "deck_pk": d.pk,
                "progress_pct": progress_pct,
            }
        )
    return rows


def record_type_example_success(student, word_text: str, topic: str) -> None:
    """Count a successful Type-it example check toward mastery level 4."""
    word_text = (word_text or "").strip()
    topic = (topic or "").strip().lower()
    if not word_text:
        return

    w = Word.objects.filter(word__iexact=word_text, topic=topic).first()
    if w:
        prog = get_or_create_progress(student, word=w)
        prog.type_success_count += 1
        update_mastery_level(prog)
        prog.save(update_fields=["type_success_count", "mastery_level"])
        return

    c = CustomCard.objects.filter(
        student=student, word__iexact=word_text, topic=topic
    ).first()
    if c:
        prog = get_or_create_progress(student, custom_card=c)
        prog.type_success_count += 1
        update_mastery_level(prog)
        prog.save(update_fields=["type_success_count", "mastery_level"])
