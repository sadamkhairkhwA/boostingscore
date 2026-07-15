"""IELTS Speaking study reference content (text only)."""

from .question_examples import PART1_TOPICS, PART2_CUE_CARDS, PART3_THEMES
from .pronunciation_content import (
    MINIMAL_PAIRS,
    MISPRONOUNCED_WORDS,
    SILENT_LETTERS,
    TRICKY_WORD_ENDINGS,
)

VALID_SECTIONS = ("questions", "pronunciation", "phrases", "tips", "record")

SECTION_TABS = (
    {"id": "questions", "label": "Common questions"},
    {"id": "pronunciation", "label": "Pronunciation"},
    {"id": "phrases", "label": "Useful phrases"},
    {"id": "tips", "label": "Tips"},
    {"id": "record", "label": "Practice recording"},
)

VALID_QUESTION_PARTS = (1, 2, 3)

QUESTION_PARTS = (
    {"id": 1, "title": "Part 1", "label": "Familiar topics"},
    {"id": 2, "title": "Part 2", "label": "Cue cards (long turn)"},
    {"id": 3, "title": "Part 3", "label": "Discussion"},
)


# ---------------------------------------------------------------------------
# Commonly mispronounced words (see pronunciation_content.py)
# ---------------------------------------------------------------------------
# MISPRONOUNCED_WORDS imported above

# ---------------------------------------------------------------------------
# Useful phrases by function
# ---------------------------------------------------------------------------
PHRASE_GROUPS = [
    {
        "group": "Giving opinions",
        "phrases": [
            ("In my view, …", "Neutral and clear — works well in Part 3."),
            ("From my perspective, …", "Slightly more formal; good for abstract topics."),
            ("I would argue that …", "Strong opinion without sounding aggressive."),
            ("Personally, I believe …", "Natural for Part 1 and Part 3."),
            ("It seems to me that …", "Softens a firm opinion."),
            ("I am convinced that …", "Shows confidence on important points."),
        ],
    },
    {
        "group": "Agreeing and disagreeing",
        "phrases": [
            ("I completely agree with that idea.", "Direct agreement in discussion."),
            ("That is a fair point, but …", "Polite partial disagreement."),
            ("I see what you mean; however, …", "Acknowledges the examiner before contrasting."),
            ("I am not entirely convinced that …", "Formal disagreement."),
            ("On the contrary, …", "Strong contrast — use sparingly."),
            ("I tend to disagree because …", "Natural disagreement with a reason ready to follow."),
        ],
    },
    {
        "group": "Giving examples",
        "phrases": [
            ("For instance, …", "Standard example introducer."),
            ("A good example of this is …", "Useful when the topic is abstract."),
            ("To illustrate this, …", "Slightly more formal; strong in Part 3."),
            ("This is particularly true in the case of …", "Links a general point to a specific situation."),
            ("I experienced this myself when …", "Personal example — very effective in Part 2 and 3."),
            ("Take … as an example.", "Clear structure for one supporting case."),
        ],
    },
    {
        "group": "Comparing and contrasting",
        "phrases": [
            ("In comparison with …", "Formal comparison."),
            ("Similarly, …", "Shows parallel ideas."),
            ("By contrast, …", "Highlights a difference."),
            ("On the one hand … on the other hand …", "Balanced view for Part 3."),
            ("Whereas in the past … nowadays …", "Useful for change-over-time questions."),
            ("This is quite different from …", "Simple, natural contrast."),
        ],
    },
    {
        "group": "Buying thinking time",
        "phrases": [
            ("That is an interesting question.", "Buys a second while you plan."),
            ("I have never thought about that before.", "Honest — follow with a real answer."),
            ("Let me think for a moment.", "Acceptable occasionally; do not overuse."),
            ("Well, it depends on the situation.", "Works when the question has no single answer."),
            ("Off the top of my head, …", "Signals a quick first thought, not a final essay."),
            ("If I had to choose, I would say …", "Useful for either/or questions."),
        ],
    },
    {
        "group": "Concluding and summarising",
        "phrases": [
            ("So, overall, …", "Simple summary to end a Part 3 answer."),
            ("To sum up, …", "Clear conclusion after two or three points."),
            ("All things considered, …", "Balanced final judgement."),
            ("The main reason is …", "Focuses a long answer."),
            ("That is why I feel …", "Links evidence back to your opinion."),
            ("Looking ahead, I think …", "Strong close for future-oriented questions."),
        ],
    },
]

# ---------------------------------------------------------------------------
# Tips — strategy per part + general advice
# ---------------------------------------------------------------------------
SPEAKING_TIPS = {
    "overview": [
        "The IELTS Speaking test lasts 11–14 minutes and has three parts. There is no separate grammar or vocabulary test — everything is assessed through your spoken answers.",
        "Examiners score fluency and coherence, lexical resource, grammatical range and accuracy, and pronunciation. You are not marked down for your opinion, only for how you express it.",
        "This section is a study guide only. Read the questions aloud, practise structuring answers, and review phrases and pronunciation — but you do not need to record or submit anything here.",
    ],
    "parts": [
        {
            "part": "Part 1",
            "duration": "4–5 minutes",
            "format": "Short questions about familiar topics (home, work, hobbies, daily life).",
            "video": "speaking_tips/tips_part1.mp4",
            "video_heading": "Watch: Part 1 explained",
            "strategy": [
                "Give full but concise answers — usually two to four sentences, not single words.",
                "Extend naturally: add a reason (because), an example (for instance), or a contrast (but / however).",
                "Use the present tense for habits and facts; past tense when the question asks about childhood or past experience.",
                "Do not memorise entire scripts — examiners recognise rehearsed answers and may change the topic.",
            ],
            "structure": "Answer the question → give one reason or detail → optional short example or feeling.",
            "mistakes": [
                "Answering with one word: Yes. / No. / Swimming.",
                "Giving overly long speeches — Part 1 should feel like a conversation.",
                "Listing without connecting ideas: I like A, B, C, D with no linking words.",
            ],
        },
        {
            "part": "Part 2",
            "duration": "3–4 minutes (1 min prep + 1–2 min speaking)",
            "format": "You receive a cue card, have one minute to prepare, then speak for one to two minutes on the topic.",
            "video": "speaking_tips/tips_part2.mp4",
            "video_heading": "Watch: Part 2 explained",
            "strategy": [
                "Use the one-minute preparation time: note key words for each bullet point on the paper provided.",
                "Cover all the bullets on the card — they guide the examiner's expectations.",
                "Aim for 90–120 seconds. Too short suggests limited language; too long may be interrupted.",
                "Tell a clear mini-story: set the scene (when/where), describe details, explain your feelings or opinion at the end.",
            ],
            "structure": "Brief introduction → point 1 → point 2 → point 3 → final explanation (why / how you felt).",
            "mistakes": [
                "Only describing the first bullet and running out of things to say.",
                "Reading notes word-for-word instead of speaking naturally.",
                "Ignoring the final “explain why” bullet — it usually carries the most weight.",
            ],
        },
        {
            "part": "Part 3",
            "duration": "4–5 minutes",
            "format": "Two-way discussion linked to the Part 2 topic, with more abstract and analytical questions.",
            "video": "speaking_tips/tips_part3.mp4",
            "video_heading": "Watch: Part 3 explained",
            "strategy": [
                "Give developed answers: state your position, support it with reasons and examples, then briefly conclude.",
                "It is fine to say “It depends” if you explain the different situations.",
                "Use comparing language (on the other hand, whereas) and generalising (many people, in most cases) appropriately.",
                "If you do not understand, politely ask: Could you explain what you mean by …? This is better than guessing.",
            ],
            "structure": "Direct answer → reason 1 (+ example) → reason 2 or contrast → short summary.",
            "mistakes": [
                "Giving personal mini-stories only — Part 3 needs general, societal or analytical comments.",
                "Repeating the same vocabulary from Part 2 without paraphrasing.",
                "Stopping after one sentence — examiners often wait for you to continue.",
            ],
        },
    ],
    "fluency": [
        "Speak at a natural pace. Faster is not better if clarity suffers.",
        "Use discourse markers to connect ideas: well, actually, in addition, as a result, mind you.",
        "Self-correction is acceptable if quick: Sorry, I mean … / What I wanted to say is …",
        "Pause briefly at clause boundaries instead of filling every gap with er/um — occasional fillers are normal.",
        "Practise aloud daily: describe your room, summarise a news story, or answer one Part 3 question per day.",
    ],
    "pronunciation": [
        "Focus on word stress — wrong stress changes meaning or sounds unnatural (e.g. PHOtograph vs phoTOgraphy).",
        "End consonants matter in clarity: walked, tasks, world — do not drop them entirely.",
        "Sentence stress: emphasise content words (nouns, main verbs, adjectives); reduce function words (the, of, to).",
        "Intonation: rise slightly for lists; fall at the end of completed statements.",
        "Record yourself occasionally outside this app and compare with model pronunciations — consistency beats a perfect accent.",
    ],
}

# ---------------------------------------------------------------------------
# Sounding natural — fillers & hesitation (Tips subsection)
# ---------------------------------------------------------------------------
FILLER_PHRASE_GROUPS = [
    {
        "group": "Buying thinking time",
        "note": "Use sparingly — one or two per answer sounds natural; every sentence sounds hesitant.",
        "phrases": [
            ("That's an interesting question.", "Buys a second while you plan your structure."),
            ("Let me think about that for a moment.", "Honest pause — follow with a real answer."),
            ("Well, I suppose …", "Soft opener before a balanced opinion."),
            ("I have never really considered that before.", "Works for unusual Part 3 questions."),
            ("If I had to choose, I would say …", "Useful for either/or questions."),
        ],
    },
    {
        "group": "Clarifying or reframing",
        "note": "Shows you understood the question before answering.",
        "phrases": [
            ("Do you mean … or …?", "Polite clarification in Part 3."),
            ("So, in other words, you're asking about …", "Paraphrase the question aloud."),
            ("It depends what you mean by …", "Valid when the question is broad."),
        ],
    },
    {
        "group": "Softening opinions",
        "note": "Avoids sounding too absolute — good for Band 7+ nuance.",
        "phrases": [
            ("To some extent, …", "Hedges a strong claim."),
            ("I tend to think that …", "Personal but not dogmatic."),
            ("On balance, …", "Signals you weighed both sides."),
            ("It seems to me that …", "Natural in Part 3 discussion."),
        ],
    },
    {
        "group": "Recovering from a mistake",
        "note": "Quick self-correction is fine; long apologies waste time.",
        "phrases": [
            ("Sorry — what I meant was …", "Fast correction."),
            ("Let me put that another way.", "Restart a unclear sentence."),
            ("Actually, a better example would be …", "Swap a weak example."),
        ],
    },
]

FILLER_OVERUSE_WARNING = (
    "Fillers and hesitation phrases buy thinking time, but overusing them (especially "
    "um, er, like, you know) lowers fluency scores. Aim for one purposeful phrase, then speak."
)


def build_recording_questions():
    """Flat list of practice questions for self-recording mode."""
    items = []
    for topic in PART1_TOPICS:
        for q in topic["questions"]:
            items.append(
                {
                    "id": f"p1-{topic['topic'][:20]}-{len(items)}",
                    "part": 1,
                    "label": topic["topic"],
                    "prompt": q["text"],
                }
            )
    for i, card in enumerate(PART2_CUE_CARDS):
        items.append(
            {
                "id": f"p2-{i}",
                "part": 2,
                "label": card["title"],
                "prompt": card["title"],
                "bullets": card.get("bullets", []),
            }
        )
    for theme in PART3_THEMES:
        for q in theme["questions"]:
            items.append(
                {
                    "id": f"p3-{theme['theme'][:15]}-{len(items)}",
                    "part": 3,
                    "label": theme["theme"],
                    "prompt": q["text"],
                }
            )
    return items
