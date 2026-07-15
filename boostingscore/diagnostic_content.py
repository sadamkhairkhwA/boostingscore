"""Short diagnostic shown once after signup — under 10 minutes."""
from __future__ import annotations

DIAGNOSTIC_SECTIONS = [
    {
        "id": "reading",
        "title": "Reading",
        "skill": "reading",
        "questions": [
            {
                "id": "dr-1",
                "prompt": "Passage: 'Remote teams report stable productivity after year one.' Statement: Productivity usually collapses after the first year.",
                "type": "choice",
                "options": [
                    {"value": "a", "label": "True"},
                    {"value": "b", "label": "False"},
                    {"value": "c", "label": "Not Given"},
                ],
                "answer": "b",
                "weight": 1,
            },
            {
                "id": "dr-2",
                "prompt": "A question asks about 'rapid urban expansion'. Which phrase is the closest paraphrase to hunt for?",
                "type": "choice",
                "options": [
                    {"value": "a", "label": "fast city growth"},
                    {"value": "b", "label": "slow rural decline"},
                    {"value": "c", "label": "ancient customs"},
                    {"value": "d", "label": "mountain weather"},
                ],
                "answer": "a",
                "weight": 1,
            },
        ],
    },
    {
        "id": "listening",
        "title": "Listening",
        "skill": "listening",
        "questions": [
            {
                "id": "dl-1",
                "prompt": "You hear: 'The seminar begins at a quarter past nine.' What time is that?",
                "type": "choice",
                "options": [
                    {"value": "a", "label": "9:15"},
                    {"value": "b", "label": "9:45"},
                    {"value": "c", "label": "9:05"},
                    {"value": "d", "label": "10:15"},
                ],
                "answer": "a",
                "weight": 1,
            },
            {
                "id": "dl-2",
                "prompt": "You hear: 'Reference number A L seven four two nine.' What do you write?",
                "type": "choice",
                "options": [
                    {"value": "a", "label": "AL7429"},
                    {"value": "b", "label": "AL74209"},
                    {"value": "c", "label": "AL7942"},
                    {"value": "d", "label": "AL4729"},
                ],
                "answer": "a",
                "weight": 1,
            },
        ],
    },
    {
        "id": "writing",
        "title": "Writing",
        "skill": "writing",
        "questions": [
            {
                "id": "dw-1",
                "prompt": "Which sentence is grammatically correct for Task 2?",
                "type": "choice",
                "options": [
                    {"value": "a", "label": "The government should invest more in public transport."},
                    {"value": "b", "label": "The government should invests more in public transport."},
                    {"value": "c", "label": "The government should investing more in public transport."},
                    {"value": "d", "label": "The government should to invest more in public transport."},
                ],
                "answer": "a",
                "weight": 1,
            },
            {
                "id": "dw-2",
                "prompt": "Choose the best formal replacement for 'a lot of' in an essay.",
                "type": "choice",
                "options": [
                    {"value": "a", "label": "a significant number of"},
                    {"value": "b", "label": "tons of"},
                    {"value": "c", "label": "loads of"},
                    {"value": "d", "label": "so many"},
                ],
                "answer": "a",
                "weight": 1,
            },
        ],
    },
    {
        "id": "speaking",
        "title": "Speaking",
        "skill": "speaking",
        "questions": [
            {
                "id": "ds-1",
                "prompt": "How confident do you feel speaking for 2 minutes without long pauses?",
                "type": "choice",
                "options": [
                    {"value": "a", "label": "Very confident — rarely stuck"},
                    {"value": "b", "label": "Fairly confident — occasional pauses"},
                    {"value": "c", "label": "Unsure — I pause often"},
                    {"value": "d", "label": "Not confident — I struggle to keep going"},
                ],
                "answer": "a",
                "weight": 0,
                "self_report": True,
            },
            {
                "id": "ds-2",
                "prompt": "Can you paraphrase a question before answering in Part 3?",
                "type": "choice",
                "options": [
                    {"value": "a", "label": "Yes, easily"},
                    {"value": "b", "label": "Sometimes"},
                    {"value": "c", "label": "Rarely"},
                    {"value": "d", "label": "No"},
                ],
                "answer": "a",
                "weight": 0,
                "self_report": True,
            },
        ],
    },
]

RECOMMENDATIONS = {
    "reading": ("Reading strategies & timed practice", "reading:strategies"),
    "listening": ("Listening detail drills", "listening:detail_drills"),
    "writing": ("Writing grammar checklist", "writing:grammar_mistakes"),
    "speaking": ("Speaking tips & recording practice", "speaking:home"),
}


def score_diagnostic(answers: dict) -> dict:
    """Return per-skill scores and estimated bands."""
    skill_correct: dict[str, int] = {}
    skill_total: dict[str, int] = {}
    self_report: dict[str, list[str]] = {}

    for section in DIAGNOSTIC_SECTIONS:
        skill = section["skill"]
        for q in section["questions"]:
            if q.get("self_report"):
                self_report.setdefault(skill, []).append(answers.get(q["id"], ""))
                continue
            skill_total[skill] = skill_total.get(skill, 0) + q.get("weight", 1)
            if answers.get(q["id"]) == q["answer"]:
                skill_correct[skill] = skill_correct.get(skill, 0) + q.get("weight", 1)

    def pct_to_band(pct: float) -> float:
        if pct >= 75:
            return 7.0
        if pct >= 50:
            return 6.0
        if pct >= 35:
            return 5.5
        return 5.0

    skill_bands = {}
    for skill in ("reading", "writing", "listening"):
        total = skill_total.get(skill, 0)
        if total:
            pct = skill_correct.get(skill, 0) / total * 100
            skill_bands[skill] = round(pct_to_band(pct) * 2) / 2

    speaking_map = {"a": 7.0, "b": 6.0, "c": 5.0, "d": 4.5}
    speak_vals = []
    for skill, vals in self_report.items():
        for v in vals:
            speak_vals.append(speaking_map.get(v, 5.5))
    if speak_vals:
        skill_bands["speaking"] = round(sum(speak_vals) / len(speak_vals) * 2) / 2

    available = [b for b in skill_bands.values() if b]
    overall = round(sum(available) / len(available) * 2) / 2 if available else None

    weakest = None
    if skill_bands:
        weakest = min(skill_bands, key=lambda k: skill_bands[k])

    recs = []
    if weakest:
        label, url_name = RECOMMENDATIONS[weakest]
        recs.append({"skill": weakest, "label": label, "url_name": url_name})
    for skill in ("reading", "listening", "writing", "speaking"):
        if skill != weakest and skill in skill_bands and skill_bands[skill] < 6.5:
            label, url_name = RECOMMENDATIONS[skill]
            recs.append({"skill": skill, "label": label, "url_name": url_name})

    return {
        "skill_bands": skill_bands,
        "overall_band": overall,
        "skill_scores": skill_correct,
        "recommendations": recs[:3],
        "answers": answers,
    }
