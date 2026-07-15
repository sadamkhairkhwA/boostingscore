import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from boostingscore.plan_limits import (
    FEATURE_SPEAKING_PHRASES,
    FEATURE_SPEAKING_PRONUNCIATION,
    FEATURE_SPEAKING_QUESTIONS,
    FEATURE_SPEAKING_RECORD,
    FEATURE_SPEAKING_TIPS,
    guard_feature,
)

from .content import (
    FILLER_OVERUSE_WARNING,
    FILLER_PHRASE_GROUPS,
    MISPRONOUNCED_WORDS,
    MINIMAL_PAIRS,
    PART1_TOPICS,
    PART2_CUE_CARDS,
    PART3_THEMES,
    PHRASE_GROUPS,
    QUESTION_PARTS,
    SECTION_TABS,
    SILENT_LETTERS,
    SPEAKING_TIPS,
    TRICKY_WORD_ENDINGS,
    VALID_QUESTION_PARTS,
    VALID_SECTIONS,
    build_recording_questions,
)

SPEAKING_SECTION_FEATURES = {
    "questions": FEATURE_SPEAKING_QUESTIONS,
    "pronunciation": FEATURE_SPEAKING_PRONUNCIATION,
    "phrases": FEATURE_SPEAKING_PHRASES,
    "tips": FEATURE_SPEAKING_TIPS,
    "record": FEATURE_SPEAKING_RECORD,
}


@login_required
def speaking_home(request):
    section = request.GET.get("section", "questions")
    if section not in VALID_SECTIONS:
        section = "questions"

    blocked = guard_feature(request, SPEAKING_SECTION_FEATURES[section])
    if blocked:
        return blocked

    question_part = 1
    if section == "questions":
        try:
            question_part = int(request.GET.get("part", 1))
        except (TypeError, ValueError):
            question_part = 1
        if question_part not in VALID_QUESTION_PARTS:
            question_part = 1

    recording_questions = build_recording_questions() if section == "record" else []
    if section == "record":
        from boostingscore.review_schedule import mark_section_reviewed
        mark_section_reviewed(request.user, "speaking_record")

    return render(
        request,
        "speaking/home.html",
        {
            "section": section,
            "section_tabs": SECTION_TABS,
            "question_part": question_part,
            "question_parts": QUESTION_PARTS,
            "part1_topics": PART1_TOPICS,
            "part2_cue_cards": PART2_CUE_CARDS,
            "part3_themes": PART3_THEMES,
            "mispronounced_words": MISPRONOUNCED_WORDS,
            "silent_letters": SILENT_LETTERS,
            "tricky_word_endings": TRICKY_WORD_ENDINGS,
            "minimal_pairs": MINIMAL_PAIRS,
            "phrase_groups": PHRASE_GROUPS,
            "speaking_tips": SPEAKING_TIPS,
            "filler_phrase_groups": FILLER_PHRASE_GROUPS,
            "filler_overuse_warning": FILLER_OVERUSE_WARNING,
            "recording_questions": recording_questions,
            "recording_questions_json": json.dumps(recording_questions),
        },
    )
