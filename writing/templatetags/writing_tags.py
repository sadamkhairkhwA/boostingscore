from django import template

from writing.highlights import extract_span_lists, merge_and_render_highlights
from writing.span_schema import SPAN_KEYS

register = template.Library()

_FEEDBACK_LABELS = {
    # Paraphrase
    "reference_improved_version": "Reference paraphrase",
    "collocations": "Strong collocations",
    "grammar_notes": "Grammar help",
    "vocabulary_upgrades": "Better vocabulary",
    "what_to_improve": "What to improve first",
    # Coaching round 1
    "deficiencies": "Main gaps",
    "grammar_to_study": "Grammar to practice",
    "vocabulary_and_collocations": "Vocabulary & collocations",
    "rewrite_focus": "Next rewrite — focus on",
    # Coaching round 2
    "improvements_since_draft1": "Changes since draft 1",
    "topic_and_task_response": "Task & question focus",
    "ielts_tips_for_this_question_type": "IELTS tips for this type",
    "short_roadmap": "Short study roadmap",
    # Round 3
    "journey_summary": "How your writing grew",
    "final_study_points": "Keep studying these",
    "exam_day_reminders": "On exam day",
    "error": "Note",
}


@register.filter
def feedback_label(key: str) -> str:
    if not key:
        return ""
    return _FEEDBACK_LABELS.get(key, key.replace("_", " ").title())


@register.filter
def is_span_key(key: str) -> bool:
    return key in SPAN_KEYS


@register.filter(needs_autoescape=False)
def essay_highlights(text, meta) -> str:
    plain = "" if text is None else str(text)
    issues, strengths = extract_span_lists(meta if isinstance(meta, dict) else {})
    return merge_and_render_highlights(plain, issues, strengths)


@register.filter
def feedback_round_title(key: str) -> str:
    mapping = {
        "round1": "After your first draft",
        "round2": "After your second draft",
        "round3": "After your final draft",
    }
    return mapping.get(key, key.replace("_", " ").title())
