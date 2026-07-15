"""Core Reading strategies — Khan Academy-style course data.

Each lesson has a learn block (rendered in templates) and practice questions (JSON for JS).
Add lessons to CORE_STRATEGY_LESSONS; mixed review questions go in MIXED_REVIEW.
"""

GOLDEN_RULE = (
    "Answer from the passage, not background knowledge. If it is not written "
    "(or clearly implied), do not invent it — especially for Not Given."
)

# learn_layout: skim | keywords | mapping | tfng | timebox | gapfill
CORE_STRATEGY_LESSONS = [
    {
        "id": "skim-first",
        "title": "Skim first",
        "short_title": "Skim first",
        "description": (
            "Read headings and the first line of each paragraph before you touch the "
            "questions — build a map of the text in under two minutes."
        ),
        "learn_layout": "skim",
        "learn": {
            "example_label": "Read these only when skimming",
            "passage_html": (
                '<span class="rs-hl-yellow">Urban forests cool neighbourhoods, absorb stormwater, '
                "and improve mental health.</span> "
                '<span class="rs-hl-yellow">Cities from Singapore to Medellín now treat green corridors '
                "as core infrastructure.</span> "
                "Detailed species lists and maintenance budgets appear later in the report."
            ),
            "footnote": "Highlighted = what you read. You know the topic without reading every word.",
        },
        "practice": {
            "instructions": "Skim the passage below (read openings only), then answer without re-reading every line.",
            "passage": (
                "The regional rail authority announced a phased upgrade of signalling equipment across "
                "three lines over the next eighteen months. Peak-hour delays are expected during weekends "
                "while contractors replace outdated cables. Passengers are advised to allow an extra fifteen "
                "minutes for connections until work completes in December. Officials claim modern signalling "
                "could cut average wait times by almost a quarter once systems stabilise. Critics argue "
                "communications around disruptions remain vague, and that smaller stations still lack "
                "real-time boards."
            ),
            "questions": [
                {
                    "id": "skim-1",
                    "prompt": "Without reading every word, what is the passage mainly about?",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "A rail signalling upgrade and its timing"},
                        {"value": "b", "label": "The history of train travel in Europe"},
                        {"value": "c", "label": "How to build new railway stations"},
                        {"value": "d", "label": "Ticket price increases for commuters"},
                    ],
                    "answer": "a",
                    "explanation": "Skimming the opening and topic sentences points to equipment upgrades, weekend delays, and a December completion date.",
                },
                {
                    "id": "skim-2",
                    "prompt": "Which detail would you expect to find in the middle of the passage rather than in your skim?",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "The exact percentage cut in wait times once stable"},
                        {"value": "b", "label": "Whether the topic is transport infrastructure"},
                        {"value": "c", "label": "That passengers may need extra connection time"},
                        {"value": "d", "label": "That work runs over eighteen months"},
                    ],
                    "answer": "a",
                    "explanation": "Skimming gives you the gist; precise figures like “almost a quarter” are supporting detail you locate when a question asks for them.",
                },
                {
                    "id": "skim-3",
                    "prompt": "When skimming, which lines are most useful to read first?",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "The first sentence of each paragraph"},
                        {"value": "b", "label": "Only the final sentence of the passage"},
                        {"value": "c", "label": "Every adjective in the text"},
                        {"value": "d", "label": "Footnotes and references"},
                    ],
                    "answer": "a",
                    "explanation": "Topic sentences and paragraph openings reveal structure — the core skim skill before you attack the questions.",
                },
            ],
        },
    },
    {
        "id": "keywords",
        "title": "Keywords",
        "short_title": "Keywords",
        "description": (
            "Underline key terms in the question, then scan the passage for synonyms — "
            "IELTS rarely repeats the same wording."
        ),
        "learn_layout": "keywords",
        "learn": {
            "question_html": (
                "What did <span class=\"rs-hl-blue\">scientists</span> "
                "<span class=\"rs-hl-blue\">discover</span> about "
                "<span class=\"rs-hl-blue\">ocean temperatures</span>?"
            ),
            "passage_html": (
                "<span class=\"rs-hl-green\">Researchers</span> "
                "<span class=\"rs-hl-green\">found</span> that "
                "<span class=\"rs-hl-green\">sea surface heat</span> had risen significantly."
            ),
            "footnote": "scientists → Researchers · discover → found · ocean temperatures → sea surface heat",
        },
        "practice": {
            "instructions": "Underline the keywords in the question, then find the paraphrase in the passage.",
            "passage": (
                "A recent survey indicated that municipal authorities have tightened regulations "
                "on waste disposal. Inspectors reported a sharp decline in illegal dumping after "
                "cameras were installed at landfill entrances. However, small businesses complain "
                "that compliance costs remain burdensome."
            ),
            "questions": [
                {
                    "id": "kw-1",
                    "prompt": "Question: What did officials notice about unlawful tipping?",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "illegal dumping"},
                        {"value": "b", "label": "sharp decline"},
                        {"value": "c", "label": "cameras"},
                        {"value": "d", "label": "businesses"},
                    ],
                    "answer": "a",
                    "explanation": "“Unlawful tipping” paraphrases “illegal dumping” — scan for meaning, not identical words.",
                },
                {
                    "id": "kw-2",
                    "prompt": "Which phrase in the passage matches “municipal authorities”?",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "municipal authorities (same words)"},
                        {"value": "b", "label": "inspectors"},
                        {"value": "c", "label": "small businesses"},
                        {"value": "d", "label": "landfill entrances"},
                    ],
                    "answer": "a",
                    "explanation": "Sometimes IELTS repeats a phrase, but often “officials” or “regulators” replaces “authorities” — here the wording is unchanged, so locate it directly.",
                },
                {
                    "id": "kw-3",
                    "prompt": "The question asks about a “sharp decline”. Which words carry the same idea?",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "reported a sharp decline"},
                        {"value": "b", "label": "tightened regulations"},
                        {"value": "c", "label": "compliance costs"},
                        {"value": "d", "label": "recent survey"},
                    ],
                    "answer": "a",
                    "explanation": "Keywords guide your scan; “sharp decline” appears with the same meaning in the passage.",
                },
            ],
        },
    },
    {
        "id": "paragraph-mapping",
        "title": "Paragraph mapping",
        "short_title": "Paragraph mapping",
        "description": (
            "Label each paragraph with a three-word gist before matching headings or information — "
            "you answer from the map, not from memory."
        ),
        "learn_layout": "mapping",
        "learn": {
            "map_rows": [
                {
                    "para": "Para A: History of fossil fuels from the industrial era…",
                    "label": "History of energy",
                },
                {
                    "para": "Para B: Renewable infrastructure barriers in grid design…",
                    "label": "Current challenges",
                },
                {
                    "para": "Para C: Battery technology projections through 2040…",
                    "label": "Future solutions",
                },
            ],
        },
        "practice": {
            "instructions": "Read each paragraph gist and choose the best three-word label.",
            "passage": (
                "Paragraph A describes how early universities were funded by church patronage and later "
                "by state grants. Paragraph B explains current funding gaps and rising tuition fees. "
                "Paragraph C outlines proposed scholarship models for the next decade."
            ),
            "questions": [
                {
                    "id": "map-1",
                    "prompt": "Paragraph A is mainly about:",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "Historical funding sources"},
                        {"value": "b", "label": "Future scholarship models"},
                        {"value": "c", "label": "Student protest movements"},
                        {"value": "d", "label": "Online degree platforms"},
                    ],
                    "answer": "a",
                    "explanation": "Church patronage and state grants = historical funding — label the whole paragraph, not one detail.",
                },
                {
                    "id": "map-2",
                    "prompt": "Which label best fits Paragraph B?",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "Present financial pressures"},
                        {"value": "b", "label": "Medieval university life"},
                        {"value": "c", "label": "Laboratory safety rules"},
                        {"value": "d", "label": "Sports facility upgrades"},
                    ],
                    "answer": "a",
                    "explanation": "Funding gaps and tuition fees describe present-day financial pressure on institutions.",
                },
                {
                    "id": "map-3",
                    "prompt": "Paragraph C focuses on:",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "Planned support for students"},
                        {"value": "b", "label": "Ancient library collections"},
                        {"value": "c", "label": "Declining exam standards"},
                        {"value": "d", "label": "Campus parking shortages"},
                    ],
                    "answer": "a",
                    "explanation": "Scholarship models for the next decade = planned future support — your map should capture that forward look.",
                },
            ],
        },
    },
    {
        "id": "tfng-discipline",
        "title": "TFNG discipline",
        "short_title": "TFNG discipline",
        "description": (
            "If the passage does not mention the claim, choose Not Given — not False. "
            "False needs a direct contradiction."
        ),
        "learn_layout": "tfng",
        "learn": {
            "statement": "Scientists have proven that coffee improves long-term memory.",
            "passage_html": (
                "Some studies <span class=\"rs-hl-yellow\">suggest a possible link</span> "
                "between caffeine and short-term alertness."
            ),
            "answer_label": "NOT GIVEN",
            "footnote": (
                "The passage hedges (“suggest”, “possible”) and never “proves” memory — "
                "but it also never denies it outright, so it is not False."
            ),
        },
        "practice": {
            "instructions": "Read the passage, then decide True, False, or Not Given for each statement.",
            "passage": (
                "Remote teams often report stable productivity after the first year. Managers rarely "
                "cite video fatigue as the main obstacle; instead, unclear priorities dominate exit "
                "surveys. No data in the report compares remote pay with office-based salaries."
            ),
            "questions": [
                {
                    "id": "tfng-1",
                    "prompt": "Video fatigue is the primary reason managers struggle with remote teams.",
                    "type": "tfng",
                    "options": [
                        {"value": "T", "label": "True"},
                        {"value": "F", "label": "False"},
                        {"value": "NG", "label": "Not Given"},
                    ],
                    "answer": "F",
                    "explanation": "The passage says managers rarely cite video fatigue — the opposite of the statement.",
                },
                {
                    "id": "tfng-2",
                    "prompt": "Productivity among remote teams usually collapses after the first year.",
                    "type": "tfng",
                    "options": [
                        {"value": "T", "label": "True"},
                        {"value": "F", "label": "False"},
                        {"value": "NG", "label": "Not Given"},
                    ],
                    "answer": "F",
                    "explanation": "The passage states productivity stays stable after year one — a direct contradiction.",
                },
                {
                    "id": "tfng-3",
                    "prompt": "Remote workers earn less than office workers.",
                    "type": "tfng",
                    "options": [
                        {"value": "T", "label": "True"},
                        {"value": "F", "label": "False"},
                        {"value": "NG", "label": "Not Given"},
                    ],
                    "answer": "NG",
                    "explanation": "Pay is never mentioned — do not infer from background knowledge.",
                },
            ],
        },
    },
    {
        "id": "time-boxing",
        "title": "Time boxing",
        "short_title": "Time boxing",
        "description": (
            "Aim for roughly twenty minutes per passage so Part 3 still gets full attention."
        ),
        "learn_layout": "timebox",
        "learn": {
            "footnote": "≈13–14 questions per part · ~90 seconds per question on average · move on if stuck.",
        },
        "practice": {
            "instructions": "Apply the 60-minute plan — choose the best time-management decision.",
            "passage": (
                "You have completed Part 1 with three minutes to spare and Part 2 is a matching-headings "
                "set. Part 3 is a dense academic text with several Not Given items. The exam ends in "
                "twenty-two minutes."
            ),
            "questions": [
                {
                    "id": "time-1",
                    "prompt": "You have spent eight minutes on one Part 3 question with no progress. Best action?",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "Guess, mark the question, and continue"},
                        {"value": "b", "label": "Re-read the entire passage from the start"},
                        {"value": "c", "label": "Leave the test and check Part 1 again"},
                        {"value": "d", "label": "Ask the invigilator for extra time"},
                    ],
                    "answer": "a",
                    "explanation": "Time boxing means moving on — eight minutes on one item risks leaving easier marks unanswered.",
                },
                {
                    "id": "time-2",
                    "prompt": "Roughly how long should you allow for each full passage in Academic Reading?",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "About 20 minutes"},
                        {"value": "b", "label": "About 40 minutes"},
                        {"value": "c", "label": "About 5 minutes"},
                        {"value": "d", "label": "About 60 minutes"},
                    ],
                    "answer": "a",
                    "explanation": "Three passages in sixty minutes ≈ twenty minutes each, including reading and answering.",
                },
                {
                    "id": "time-3",
                    "prompt": "When should you transfer answers to the answer sheet?",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "Keep a few minutes at the end of the hour"},
                        {"value": "b", "label": "Only after all three passages are fully memorised"},
                        {"value": "c", "label": "Never — rough notes are enough"},
                        {"value": "d", "label": "Before reading any passage"},
                    ],
                    "answer": "a",
                    "explanation": "Reserve the final two minutes for transfer and spelling checks — a core part of time planning.",
                },
            ],
        },
    },
    {
        "id": "gapfill-grammar",
        "title": "Gap-fill grammar",
        "short_title": "Gap-fill grammar",
        "description": (
            "The gap must be grammatically correct in the sentence and match the passage meaning — "
            "check word class before you copy."
        ),
        "learn_layout": "gapfill",
        "learn": {
            "gap_sentence": "The scheme led to a measurable drop in <span class=\"rs-gap-blank\"></span> during morning peaks.",
            "gap_options": [
                {"text": "produce", "ok": False, "note": "noun/verb clash"},
                {"text": "congestion", "ok": True, "note": "fits + matches passage"},
                {"text": "vehicles", "ok": False, "note": "plausible but wrong meaning"},
            ],
        },
        "practice": {
            "instructions": "Choose the word that fits the grammar and matches the passage excerpt.",
            "passage": (
                "The report attributes the delay chiefly to disruption in supply chains. Officials "
                "warned that further shocks could slow delivery schedules through the autumn."
            ),
            "questions": [
                {
                    "id": "gap-1",
                    "prompt": "The report attributes the delay chiefly to _____ in supply chains.",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "disruption"},
                        {"value": "b", "label": "disrupt"},
                        {"value": "c", "label": "disruptive"},
                        {"value": "d", "label": "disrupted"},
                    ],
                    "answer": "a",
                    "explanation": "After “to” you need a noun — “disruption” matches the passage exactly.",
                },
                {
                    "id": "gap-2",
                    "prompt": "Further shocks could _____ delivery schedules.",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "slow"},
                        {"value": "b", "label": "slowly"},
                        {"value": "c", "label": "slowness"},
                        {"value": "d", "label": "slowed"},
                    ],
                    "answer": "a",
                    "explanation": "Modal “could” + base verb “slow” — copy meaning and check grammar before writing the answer.",
                },
                {
                    "id": "gap-3",
                    "prompt": "Which answer obeys “NO MORE THAN ONE WORD” if the gap is in: There was a measurable drop in _____.",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "traffic"},
                        {"value": "b", "label": "traffic levels"},
                        {"value": "c", "label": "the traffic"},
                        {"value": "d", "label": "very heavy traffic"},
                    ],
                    "answer": "a",
                    "explanation": "One word only — “traffic” fits the noun slot; multi-word phrases break instructions even if meaning is right.",
                },
            ],
        },
    },
]

MIXED_REVIEW = {
    "title": "Mixed review",
    "short_title": "Review",
    "instructions": "Short questions drawn from every strategy — no new rules, just apply what you learned.",
    "questions": [
        {
            "id": "mix-1",
            "strategy": "Skim first",
            "prompt": "You skim a passage and see the first lines mention “battery recycling” and “end-of-life cells”. The passage is probably about:",
            "type": "choice",
            "options": [
                {"value": "a", "label": "Waste management for batteries"},
                {"value": "b", "label": "Medieval poetry"},
                {"value": "c", "label": "Ocean fishing quotas"},
                {"value": "d", "label": "Airport security screening"},
            ],
            "answer": "a",
            "explanation": "Skimming topic sentences gives you the subject area before detail questions.",
        },
        {
            "id": "mix-2",
            "strategy": "Keywords",
            "prompt": "A question asks about “rapid urban expansion”. Which phrase is the closest paraphrase to hunt for?",
            "type": "choice",
            "options": [
                {"value": "a", "label": "fast city growth"},
                {"value": "b", "label": "slow rural decline"},
                {"value": "c", "label": "ancient village customs"},
                {"value": "d", "label": "mountain weather patterns"},
            ],
            "answer": "a",
            "explanation": "rapid → fast · urban → city · expansion → growth.",
        },
        {
            "id": "mix-3",
            "strategy": "TFNG discipline",
            "prompt": "Passage: “Some analysts expect demand to rise.” Statement: “All analysts agree demand will rise.”",
            "type": "tfng",
            "options": [
                {"value": "T", "label": "True"},
                {"value": "F", "label": "False"},
                {"value": "NG", "label": "Not Given"},
            ],
            "answer": "F",
            "explanation": "“Some” and “expect” contradict “all” and “will” — False, not Not Given.",
        },
        {
            "id": "mix-4",
            "strategy": "Time boxing",
            "prompt": "You have five minutes left and ten answers still on the question paper. Best plan?",
            "type": "choice",
            "options": [
                {"value": "a", "label": "Transfer what you have and guess blanks quickly"},
                {"value": "b", "label": "Start reading Passage 1 again"},
                {"value": "c", "label": "Leave answers blank"},
                {"value": "d", "label": "Rewrite every answer in different words"},
            ],
            "answer": "a",
            "explanation": "Never leave the answer sheet empty — use remaining time to transfer and complete guesses.",
        },
        {
            "id": "mix-5",
            "strategy": "Gap-fill grammar",
            "prompt": "Gap: “The policy led to a reduction in _____.” Which word class fits?",
            "type": "choice",
            "options": [
                {"value": "a", "label": "pollution (noun)"},
                {"value": "b", "label": "pollute (verb)"},
                {"value": "c", "label": "polluting (verb form)"},
                {"value": "d", "label": "polluted (adjective)"},
            ],
            "answer": "a",
            "explanation": "After “in” you need a noun — grammar check before meaning.",
        },
    ],
}
