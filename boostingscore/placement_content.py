"""Untimed placement test — auto-graded vocab, grammar, reading, writing awareness.

No OpenAI calls. Within each section, difficulty rises from ~band 4–5 to ~band 7–8.
Harder items carry higher weight when mapping to an estimated band range.
Distractors are same category / part of speech and topically plausible.
"""
from __future__ import annotations

from datetime import timedelta
from typing import Any

PLACEMENT_QUESTION_COUNT = 20
RETAKE_COOLDOWN_DAYS = 14

# ---------------------------------------------------------------------------
# Vocabulary (6) — B1 → C1; all options same POS + topical set
# band_tag = approximate target ability; weight rises with hardness
# ---------------------------------------------------------------------------
VOCAB_QUESTIONS = [
    {
        "id": "v1",
        "band_tag": "4–5",
        "weight": 1,
        "prompt": "Cities face serious air ____ from traffic and factories.",
        "type": "choice",
        "options": [
            {"value": "a", "label": "pollution"},
            {"value": "b", "label": "emission"},
            {"value": "c", "label": "contamination"},
            {"value": "d", "label": "litter"},
        ],
        "answer": "a",
        # pollution = general urban air problem; emission = often singular source;
        # contamination = usually water/soil; litter = solid waste on ground
    },
    {
        "id": "v2",
        "band_tag": "5–5.5",
        "weight": 1,
        "prompt": "Protecting ____ means looking after wild animals and plants in their natural habitats.",
        "type": "choice",
        "options": [
            {"value": "a", "label": "livestock"},
            {"value": "b", "label": "vegetation"},
            {"value": "c", "label": "wildlife"},
            {"value": "d", "label": "fisheries"},
        ],
        "answer": "c",
    },
    {
        "id": "v3",
        "band_tag": "5.5–6.5",
        "weight": 2,
        "prompt": "What does “urbanisation” most nearly mean?",
        "type": "choice",
        "options": [
            {"value": "a", "label": "The restoration of abandoned farmland"},
            {"value": "b", "label": "The growth of cities and the movement of people into them"},
            {"value": "c", "label": "The temporary relocation of workers overseas"},
            {"value": "d", "label": "The construction of roads through national parks only"},
        ],
        "answer": "b",
    },
    {
        "id": "v4",
        "band_tag": "6–6.5",
        "weight": 2,
        "prompt": "Better transport ____ between towns makes commuting and trade easier.",
        "type": "choice",
        "options": [
            {"value": "a", "label": "isolation"},
            {"value": "b", "label": "congestion"},
            {"value": "c", "label": "connectivity"},
            {"value": "d", "label": "capacity"},
        ],
        "answer": "c",
    },
    {
        "id": "v5",
        "band_tag": "7–7.5",
        "weight": 3,
        "prompt": "Rising temperatures can ____ existing water shortages in dry regions.",
        "type": "choice",
        "options": [
            {"value": "a", "label": "alleviate"},
            {"value": "b", "label": "exacerbate"},
            {"value": "c", "label": "mitigate"},
            {"value": "d", "label": "stabilise"},
        ],
        "answer": "b",
        # All are verbs used in environmental discourse; only exacerbate = make worse
    },
    {
        "id": "v6",
        "band_tag": "7.5–8",
        "weight": 3,
        "prompt": "In academic writing, “anthropogenic” climate change refers to change that is:",
        "type": "choice",
        "options": [
            {"value": "a", "label": "driven primarily by natural orbital cycles"},
            {"value": "b", "label": "caused by human activity"},
            {"value": "c", "label": "limited to polar regions only"},
            {"value": "d", "label": "predicted but not yet observed"},
        ],
        "answer": "b",
    },
]

# ---------------------------------------------------------------------------
# Grammar (6) — typical learner traps; 4 tempting options each
# ---------------------------------------------------------------------------
GRAMMAR_QUESTIONS = [
    {
        "id": "g1",
        "band_tag": "4–5",
        "weight": 1,
        "prompt": "Choose the correct article.",
        "stem": "She hopes to become ____ engineer after graduation.",
        "type": "choice",
        "options": [
            {"value": "a", "label": "a"},
            {"value": "b", "label": "an"},
            {"value": "c", "label": "the"},
            {"value": "d", "label": "(no article)"},
        ],
        "answer": "b",
        "topic": "articles",
    },
    {
        "id": "g2",
        "band_tag": "5–5.5",
        "weight": 1,
        "prompt": "Choose the best tense.",
        "stem": "By the time the examiner arrived, the candidates ____ the listening section.",
        "type": "choice",
        "options": [
            {"value": "a", "label": "finished"},
            {"value": "b", "label": "have finished"},
            {"value": "c", "label": "had finished"},
            {"value": "d", "label": "were finishing"},
        ],
        "answer": "c",
        "topic": "verb-tenses",
    },
    {
        "id": "g3",
        "band_tag": "5.5–6.5",
        "weight": 2,
        "prompt": "Choose the correct preposition.",
        "stem": "There was a sharp rise ____ unemployment after the factory closed.",
        "type": "choice",
        "options": [
            {"value": "a", "label": "of"},
            {"value": "b", "label": "on"},
            {"value": "c", "label": "in"},
            {"value": "d", "label": "at"},
        ],
        "answer": "c",
        "topic": "prepositions-data",
    },
    {
        "id": "g4",
        "band_tag": "6–6.5",
        "weight": 2,
        "prompt": "Choose the grammatically correct sentence.",
        "type": "choice",
        "options": [
            {
                "value": "a",
                "label": "Although the graph shows growth, but wages remain low.",
            },
            {
                "value": "b",
                "label": "Although the graph shows growth, wages remain low.",
            },
            {
                "value": "c",
                "label": "Although the graph shows growth wages remain low.",
            },
            {
                "value": "d",
                "label": "Although showing growth, but wages remain low.",
            },
        ],
        "answer": "b",
        "topic": "sentence-types",
    },
    {
        "id": "g5",
        "band_tag": "7–7.5",
        "weight": 3,
        "prompt": "Choose the sentence with a correct relative clause.",
        "type": "choice",
        "options": [
            {
                "value": "a",
                "label": "Students which practise every day often improve faster.",
            },
            {
                "value": "b",
                "label": "Students who practise every day often improve faster.",
            },
            {
                "value": "c",
                "label": "Students what practise every day often improve faster.",
            },
            {
                "value": "d",
                "label": "Students practise every day who often improve faster.",
            },
        ],
        "answer": "b",
        "topic": "relative-clauses",
    },
    {
        "id": "g6",
        "band_tag": "7.5–8",
        "weight": 3,
        "prompt": "Choose the most accurate conditional sentence.",
        "type": "choice",
        "options": [
            {
                "value": "a",
                "label": "If governments will invest more in rail, congestion would decrease.",
            },
            {
                "value": "b",
                "label": "If governments invest more in rail, congestion would have decreased.",
            },
            {
                "value": "c",
                "label": "If governments invested more in rail, congestion would decrease.",
            },
            {
                "value": "d",
                "label": "If governments invested more in rail, congestion will decrease.",
            },
        ],
        "answer": "c",
        "topic": "conditionals",
    },
]

# ---------------------------------------------------------------------------
# Reading — one ~150-word C1 paragraph + 5 questions (TFNG + MC)
# Paraphrase rule: stems do not copy passage wording wholesale.
# ---------------------------------------------------------------------------
READING_PASSAGE = (
    "Several European universities have begun replacing long end-of-term examinations "
    "with shorter, staged assessments spread across the academic year. Advocates argue "
    "that this approach reduces last-minute cramming and gives lecturers earlier warning "
    "when students are struggling. Preliminary surveys suggest that most undergraduates "
    "prefer the new pattern, especially those balancing paid work with study. Critics, "
    "however, contend that continuous testing can increase chronic stress and leave too "
    "little time for deep reading. They also note that designing reliable mini-assessments "
    "demands more staff time than a single traditional paper. A few faculties have therefore "
    "adopted a hybrid model: regular low-stakes quizzes for feedback, followed by one "
    "substantial examination that still carries the majority of the final mark. Research "
    "comparing the two systems remains limited, and outcomes appear to vary by discipline "
    "and by how carefully the staged tasks are designed. Until larger controlled studies "
    "are available, many departments are treating the change as an experiment rather than "
    "a permanent policy."
)

READING_QUESTIONS = [
    {
        "id": "r1",
        "band_tag": "5–5.5",
        "weight": 1,
        "prompt": "Some universities are moving away from one long final exam toward assessment divided across the year.",
        "type": "tfng",
        "options": [
            {"value": "T", "label": "True"},
            {"value": "F", "label": "False"},
            {"value": "NG", "label": "Not Given"},
        ],
        "answer": "T",
    },
    {
        "id": "r2",
        "band_tag": "5.5–6.5",
        "weight": 2,
        "prompt": "Every faculty that tried staged assessment has abandoned continuous testing completely.",
        "type": "tfng",
        "options": [
            {"value": "T", "label": "True"},
            {"value": "F", "label": "False"},
            {"value": "NG", "label": "Not Given"},
        ],
        # Passage: some use hybrid; not abandoned → False
        "answer": "F",
    },
    {
        "id": "r3",
        "band_tag": "6–6.5",
        "weight": 2,
        "prompt": "The passage gives the exact percentage of students who prefer staged assessment.",
        "type": "tfng",
        "options": [
            {"value": "T", "label": "True"},
            {"value": "F", "label": "False"},
            {"value": "NG", "label": "Not Given"},
        ],
        "answer": "NG",
    },
    {
        "id": "r4",
        "band_tag": "7–7.5",
        "weight": 3,
        "prompt": "According to critics mentioned in the passage, one drawback of continuous testing is that it can:",
        "type": "choice",
        "options": [
            {"value": "a", "label": "raise ongoing pressure and squeeze time for careful study"},
            {"value": "b", "label": "give lecturers earlier notice when students need support"},
            {"value": "c", "label": "reduce the staff time needed to design each assessment"},
            {"value": "d", "label": "eliminate all end-of-year examinations in every faculty"},
        ],
        "answer": "a",
    },
    {
        "id": "r5",
        "band_tag": "7.5–8",
        "weight": 3,
        "prompt": "Which statement best matches the hybrid model described?",
        "type": "choice",
        "options": [
            {
                "value": "a",
                "label": "Only informal class discussion, with no recorded marks at all",
            },
            {
                "value": "b",
                "label": "Frequent light quizzes for feedback, plus one major exam that counts most",
            },
            {
                "value": "c",
                "label": "A single final paper replaced by unsupervised homework only",
            },
            {
                "value": "d",
                "label": "Daily high-stakes tests that each carry equal weight in the final grade",
            },
        ],
        "answer": "b",
    },
]

# ---------------------------------------------------------------------------
# Writing awareness (3) — formal essay judgment, no free writing / no AI
# ---------------------------------------------------------------------------
WRITING_QUESTIONS = [
    {
        "id": "w1",
        "band_tag": "5–5.5",
        "weight": 1,
        "prompt": "Which sentence is most appropriate for a formal IELTS Task 2 essay?",
        "type": "choice",
        "options": [
            {
                "value": "a",
                "label": "I reckon governments need to spend way more money on trains.",
            },
            {
                "value": "b",
                "label": "Governments should allocate greater funding to public transport.",
            },
            {
                "value": "c",
                "label": "I think the government must give lots of cash for transport.",
            },
            {
                "value": "d",
                "label": "Everyone knows trains are better, so of course we should pay more.",
            },
        ],
        "answer": "b",
    },
    {
        "id": "w2",
        "band_tag": "6–6.5",
        "weight": 2,
        "prompt": "Which sentence contains a clear grammar or style error for academic writing?",
        "type": "choice",
        "options": [
            {
                "value": "a",
                "label": "Although online courses are convenient, they require strong self-discipline.",
            },
            {
                "value": "b",
                "label": "Although online courses are convenient, but they require strong self-discipline.",
            },
            {
                "value": "c",
                "label": "Online courses are convenient; however, they require strong self-discipline.",
            },
            {
                "value": "d",
                "label": "While online courses offer flexibility, learners still need self-discipline.",
            },
        ],
        "answer": "b",
    },
    {
        "id": "w3",
        "band_tag": "7–8",
        "weight": 3,
        "prompt": "Choose the best linking word for this Task 1-style sentence.",
        "stem": "Sales rose steadily in the first quarter; ____, they fell sharply after June.",
        "type": "choice",
        "options": [
            {"value": "a", "label": "for example"},
            {"value": "b", "label": "in addition"},
            {"value": "c", "label": "by contrast"},
            {"value": "d", "label": "in other words"},
        ],
        "answer": "c",
    },
]

PLACEMENT_SECTIONS = [
    {
        "id": "vocabulary",
        "title": "Vocabulary",
        "hint": "6 questions",
        "questions": VOCAB_QUESTIONS,
    },
    {
        "id": "grammar",
        "title": "Grammar",
        "hint": "6 questions",
        "questions": GRAMMAR_QUESTIONS,
    },
    {
        "id": "reading",
        "title": "Reading",
        "hint": "1 passage · 5 questions",
        "passage": READING_PASSAGE,
        "questions": READING_QUESTIONS,
    },
    {
        "id": "writing",
        "title": "Writing awareness",
        "hint": "3 questions · no essay writing",
        "questions": WRITING_QUESTIONS,
    },
]

SECTION_ORDER = ("vocabulary", "grammar", "reading", "writing")


def all_questions() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for sec in PLACEMENT_SECTIONS:
        for q in sec["questions"]:
            item = dict(q)
            item["section"] = sec["id"]
            out.append(item)
    return out


def format_review_list() -> str:
    """Human-readable review of all items with answers and band tags."""
    lines = [
        "Placement test review — 20 questions",
        "Untimed · takes most people under 10 minutes",
        "",
    ]
    for sec in PLACEMENT_SECTIONS:
        lines.append(f"## {sec['title']} ({len(sec['questions'])})")
        if sec.get("passage"):
            words = len(sec["passage"].split())
            lines.append(f"(Passage ≈ {words} words)")
            lines.append("")
        for i, q in enumerate(sec["questions"], 1):
            ans = q["answer"]
            ans_label = next(
                (o["label"] for o in q["options"] if o["value"] == ans),
                ans,
            )
            lines.append(
                f"{i}. [{q.get('band_tag', '?')}] weight={q.get('weight', 1)}  id={q['id']}"
            )
            lines.append(f"   Prompt: {q['prompt']}")
            if q.get("stem"):
                lines.append(f"   Stem: {q['stem']}")
            for o in q["options"]:
                mark = "✓" if o["value"] == ans else " "
                lines.append(f"   [{mark}] {o['value']}. {o['label']}")
            lines.append(f"   Answer: {ans} — {ans_label}")
            lines.append("")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _section_label(pct: float) -> str:
    if pct >= 75:
        return "Strong"
    if pct >= 50:
        return "Solid"
    return "Developing"


def _band_range_from_weighted_pct(pct: float) -> tuple[str, int]:
    """Return (band_range_label, study_level 1/2/3)."""
    if pct < 28:
        return "Band 4.0–5.0", 1
    if pct < 42:
        return "Band 5.0–5.5", 1
    if pct < 56:
        return "Band 5.5–6.5", 2
    if pct < 70:
        return "Band 6.5–7.0", 2
    if pct < 84:
        return "Band 7.0–7.5", 3
    return "Band 7.5–8.5", 3


def _advice_for(section_pcts: dict[str, float]) -> list[dict[str, Any]]:
    """2–4 honest recommendations; free destinations first."""
    ranked = sorted(section_pcts.items(), key=lambda kv: kv[1])
    advice: list[dict[str, Any]] = []

    for section, pct in ranked:
        if len(advice) >= 3:
            break
        if section == "vocabulary" and pct < 75:
            advice.append(
                {
                    "text": (
                        "Start with the free Environment flashcard deck to build high-frequency IELTS words."
                    ),
                    "url_name": "vocabulary:flashcard_topic",
                    "url_kwargs": {"topic": "environment"},
                    "cta": "Open Environment flashcards",
                }
            )
        elif section == "grammar" and pct < 75:
            advice.append(
                {
                    "text": (
                        "Focus on articles, verb tenses, complex sentences, and prepositions. "
                        "The full grammar hub is on Pro — on Free, use your one scored Writing Task 1 attempt carefully."
                    ),
                    "url_name": "writing:task1",
                    "url_kwargs": {},
                    "cta": "Try Writing Task 1 (free attempt)",
                }
            )
        elif section == "reading" and pct < 75:
            advice.append(
                {
                    "text": (
                        "Practise True/False/Not Given with paraphrase discipline. "
                        "Academic Reading Test 1 is free; dedicated question-type drills are on Pro."
                    ),
                    "url_name": "reading:academic_tests_index",
                    "url_kwargs": {},
                    "cta": "Open Academic Reading tests",
                }
            )
        elif section == "writing" and pct < 75:
            advice.append(
                {
                    "text": (
                        "Work on formal tone, linking words, and common grammar traps. "
                        "You have one free scored attempt each for Writing Task 1 and Task 2."
                    ),
                    "url_name": "writing:task1",
                    "url_kwargs": {},
                    "cta": "Open Writing Task 1",
                }
            )

    if not advice:
        advice.append(
            {
                "text": (
                    "Solid start. Take free Practice Test 1 for a fuller picture across all four IELTS skills."
                ),
                "url_name": "practice_test:enter_test",
                "url_kwargs": {"n": 1},
                "cta": "Start Practice Test 1",
            }
        )
    elif len(advice) < 2:
        advice.append(
            {
                "text": (
                    "For a more accurate picture of Listening and Speaking, take free Practice Test 1."
                ),
                "url_name": "practice_test:enter_test",
                "url_kwargs": {"n": 1},
                "cta": "Start Practice Test 1",
            }
        )

    return advice[:4]


def score_placement(answers: dict[str, str]) -> dict[str, Any]:
    """Grade answers and return profile payload + display fields."""
    from django.urls import reverse

    section_earned: dict[str, float] = {s: 0.0 for s in SECTION_ORDER}
    section_max: dict[str, float] = {s: 0.0 for s in SECTION_ORDER}
    correct_count = 0
    answered_count = 0

    for q in all_questions():
        sec = q["section"]
        w = float(q.get("weight", 1))
        section_max[sec] += w
        raw = (answers.get(q["id"]) or "").strip()
        if raw:
            answered_count += 1
        if raw and raw == q["answer"]:
            section_earned[sec] += w
            correct_count += 1

    total_max = sum(section_max.values()) or 1.0
    total_earned = sum(section_earned.values())
    weighted_pct = round(100.0 * total_earned / total_max, 1)

    section_pcts = {
        sec: round(100.0 * section_earned[sec] / section_max[sec], 1)
        if section_max[sec]
        else 0.0
        for sec in SECTION_ORDER
    }
    section_labels = {sec: _section_label(pct) for sec, pct in section_pcts.items()}
    band_range, study_level = _band_range_from_weighted_pct(weighted_pct)

    advice = []
    for item in _advice_for(section_pcts):
        href = "/"
        try:
            kwargs = item.get("url_kwargs") or {}
            href = reverse(item["url_name"], kwargs=kwargs) if kwargs else reverse(item["url_name"])
        except Exception:
            href = "/"
        advice.append({**item, "href": href})

    return {
        "band_range": band_range,
        "study_level": study_level,
        "weighted_pct": weighted_pct,
        "correct": correct_count,
        "answered": answered_count,
        "total": len(all_questions()),
        "sections": {
            sec: {
                "pct": section_pcts[sec],
                "label": section_labels[sec],
                "earned": section_earned[sec],
                "max": section_max[sec],
            }
            for sec in SECTION_ORDER
        },
        "advice": advice,
        "disclaimer": (
            "This is a quick estimate — a full practice test gives a more accurate picture."
        ),
    }


def can_retake(profile, now=None) -> tuple[bool, int]:
    """Return (allowed, days_remaining)."""
    from django.utils import timezone

    now = now or timezone.now()
    taken_at = getattr(profile, "placement_taken_at", None)
    if not profile.placement_completed or not taken_at:
        return True, 0
    unlock = taken_at + timedelta(days=RETAKE_COOLDOWN_DAYS)
    if now >= unlock:
        return True, 0
    remaining = (unlock.date() - now.date()).days
    return False, max(remaining, 1)
