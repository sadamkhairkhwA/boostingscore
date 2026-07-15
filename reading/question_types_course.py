"""IELTS Reading question types — merged guides + practice (Stage 2 of the reading journey).

Each entry: what it is, solve steps, worked example fields, and practice questions.
Add types to QUESTION_TYPE_LESSONS; practice blocks match core_strategies_course format.
"""

QUESTION_TYPE_LESSONS = [
    {
        "id": "multiple-choice",
        "title": "Multiple choice",
        "short_title": "Multiple choice",
        "badges": [("MCQ", "core"), ("Common", "core")],
        "what": (
            "You choose one correct answer (A, B, C, or D) from four options. Questions may ask "
            "about the main idea, a specific detail, the writer's purpose, or the meaning of a word "
            "in context. All distractors are designed to look plausible."
        ),
        "steps": [
            "Read the question stem first — know exactly what is being asked before you scan.",
            "Underline keywords in the stem and scan the passage for paraphrases, not identical words.",
            "Eliminate options that contradict the passage or only match one minor detail.",
            "If two options seem close, return to the exact sentence that supports your choice.",
        ],
        "example_layout": "mc",
        "worked_example": {
            "passage": (
                "The harbour authority introduced timed entry slots for cruise ships after congestion "
                "delayed passenger transfers for three consecutive summers. Officials report that average "
                "waiting times fell by nearly a third in the first season, though smaller operators "
                "complain the booking system favours large vessels."
            ),
            "question": "What was the main reason for introducing timed entry slots?",
            "options": [
                {"label": "A", "text": "To increase revenue from large cruise operators"},
                {"label": "B", "text": "To reduce delays caused by overcrowding"},
                {"label": "C", "text": "To ban smaller vessels from the harbour"},
                {"label": "D", "text": "To extend the cruise season into winter"},
            ],
            "correct": "B",
            "explanation": (
                "Congestion delayed transfers — the passage links slots to overcrowding delays. "
                "Revenue, bans, and winter seasons are not stated."
            ),
        },
        "practice": {
            "instructions": "Read the passage, then choose the best answer for each question.",
            "passage": (
                "Researchers tracking urban bee populations found that rooftop gardens on commercial "
                "buildings supported more diverse species than ground-level parks in the same district. "
                "The team suggests elevated plantings may offer safer foraging routes away from "
                "road pollution, though they caution that pesticide use on nearby rooftops could "
                "undermine the benefit."
            ),
            "questions": [
                {
                    "id": "mc-1",
                    "prompt": "According to the passage, rooftop gardens differed from ground parks because they:",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "supported more diverse bee species"},
                        {"value": "b", "label": "eliminated all road pollution"},
                        {"value": "c", "label": "required no maintenance"},
                        {"value": "d", "label": "were studied for only one week"},
                    ],
                    "answer": "a",
                    "explanation": "The passage directly compares species diversity on rooftops versus ground parks.",
                },
                {
                    "id": "mc-2",
                    "prompt": "The researchers' caution about pesticides implies that:",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "rooftop benefits could be reduced by chemical use nearby"},
                        {"value": "b", "label": "pesticides are banned on all commercial buildings"},
                        {"value": "c", "label": "bees avoid all urban areas"},
                        {"value": "d", "label": "ground parks use more pesticides than rooftops"},
                    ],
                    "answer": "a",
                    "explanation": "They caution that pesticide use could undermine the benefit — a possible limit, not a ban.",
                },
            ],
        },
    },
    {
        "id": "tfng-ynng",
        "title": "True / False / Not Given & Yes / No / Not Given",
        "short_title": "TFNG / YNNG",
        "badges": [("TFNG", "tfng"), ("Opinion", "opinion")],
        "what": (
            "TFNG tests factual claims against the passage: True (stated), False (contradicted), "
            "Not Given (not mentioned). YNNG tests the writer's views the same way — look for "
            "opinion verbs like argues, believes, suggests, insists. Hedged language often means "
            "Not Given."
        ),
        "steps": [
            "Read the statement slowly — identify the claim and any absolute words (all, never, prove).",
            "Locate the relevant part of the passage; do not use outside knowledge.",
            "If the passage says the opposite, choose False / No.",
            "If the topic is absent or only vaguely hedged, choose Not Given — not False.",
        ],
        "example_layout": "tfng_ynng",
        "worked_example": {
            "tfng": {
                "passage": (
                    "The Amazon produces 20% of the world's oxygen. Deforestation has accelerated "
                    "since 2015. No international agreement limits logging."
                ),
                "rows": [
                    {
                        "answer": "True",
                        "answer_class": "true",
                        "text": '"Amazon produces 20% of oxygen" — directly stated.',
                    },
                    {
                        "answer": "False",
                        "answer_class": "false",
                        "text": '"Deforestation has slowed" — passage says accelerated (opposite).',
                    },
                    {
                        "answer": "Not Given",
                        "answer_class": "ng",
                        "text": '"Brazil supports an agreement" — not mentioned at all.',
                    },
                ],
            },
            "ynng": {
                "passage_html": (
                    'The author <span class="rs-hl-yellow">suggests</span> regulations '
                    '<span class="rs-hl-yellow">could help</span> reduce emissions.'
                ),
                "statement": "The author believes stricter laws are necessary.",
                "answer": "Not Given",
                "answer_class": "ng",
                "explanation": (
                    "suggests / could ≠ believes / necessary — the opinion is hedged, "
                    "not stated as a firm belief."
                ),
            },
        },
        "practice": {
            "instructions": "Read the passage, then decide True, False, or Not Given for each statement.",
            "passage": (
                "Some studies suggest a possible link between caffeine and short-term alertness. "
                "No trial has demonstrated improved long-term memory. Researchers stress that "
                "participants were healthy adults under forty only."
            ),
            "questions": [
                {
                    "id": "tfng-p1",
                    "prompt": "Scientists have proven that coffee improves long-term memory.",
                    "type": "tfng",
                    "options": [
                        {"value": "T", "label": "True"},
                        {"value": "F", "label": "False"},
                        {"value": "NG", "label": "Not Given"},
                    ],
                    "answer": "F",
                    "explanation": "The passage says no trial has demonstrated improved long-term memory — a direct contradiction of 'proven'.",
                },
                {
                    "id": "tfng-p2",
                    "prompt": "Caffeine may affect alertness over a short period.",
                    "type": "tfng",
                    "options": [
                        {"value": "T", "label": "True"},
                        {"value": "F", "label": "False"},
                        {"value": "NG", "label": "Not Given"},
                    ],
                    "answer": "T",
                    "explanation": "A possible link with short-term alertness supports the statement.",
                },
                {
                    "id": "tfng-p3",
                    "prompt": "Older adults were included in every trial.",
                    "type": "tfng",
                    "options": [
                        {"value": "T", "label": "True"},
                        {"value": "F", "label": "False"},
                        {"value": "NG", "label": "Not Given"},
                    ],
                    "answer": "F",
                    "explanation": "Participants were under forty only — older adults were not included.",
                },
            ],
        },
    },
    {
        "id": "matching-headings",
        "title": "Matching headings",
        "short_title": "Headings",
        "badges": [("Matching", "matching"), ("Heading", "heading")],
        "what": (
            "You match a list of headings to paragraphs. Each heading must capture the main idea "
            "of the whole paragraph — not a single detail or keyword match."
        ),
        "steps": [
            "Skim all headings first and note any that look similar.",
            "Read paragraph openings and label each with a three-word gist.",
            "Match the gist to a heading; eliminate headings as you use them.",
            "Re-read the full paragraph before confirming — one vivid detail is not the main idea.",
        ],
        "example_layout": "headings",
        "worked_example": {
            "paragraph": (
                "Installation costs for household solar have fallen faster than policy analysts "
                "predicted, yet uptake remains uneven across regions because financing rules still "
                "favour large commercial buyers."
            ),
            "heading_options": [
                {
                    "text": "ii. The history of solar panel invention",
                    "correct": False,
                    "reason": "Too narrow — invention is not the focus.",
                },
                {
                    "text": "iv. Commercial buyers and tax credits",
                    "correct": False,
                    "reason": "A true detail inside the paragraph, but not the whole main idea.",
                },
                {
                    "text": "vii. Falling costs versus uneven household uptake",
                    "correct": True,
                    "reason": "Matches cost drop and the regional uptake gap.",
                },
            ],
        },
        "practice": {
            "instructions": "Read the paragraph gist, then choose the best heading.",
            "passage": (
                "Paragraph A: Early universities relied on church patronage before state grants "
                "expanded access. Paragraph B: Funding gaps now push tuition higher despite "
                "enrolment growth. Paragraph C: Proposed scholarship models aim to widen access "
                "over the next decade."
            ),
            "questions": [
                {
                    "id": "mh-1",
                    "prompt": "Which heading best fits Paragraph A?",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "Historical sources of university funding"},
                        {"value": "b", "label": "Future scholarship programmes"},
                        {"value": "c", "label": "Declining student enrolment"},
                        {"value": "d", "label": "Sports facilities on campus"},
                    ],
                    "answer": "a",
                    "explanation": "Church patronage and state grants describe historical funding sources.",
                },
                {
                    "id": "mh-2",
                    "prompt": "Which heading best fits Paragraph B?",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "Present financial pressures on students"},
                        {"value": "b", "label": "Medieval library collections"},
                        {"value": "c", "label": "Laboratory safety regulations"},
                        {"value": "d", "label": "Online degree platforms"},
                    ],
                    "answer": "a",
                    "explanation": "Funding gaps and rising tuition = present financial pressure.",
                },
            ],
        },
    },
    {
        "id": "sentence-completion",
        "title": "Sentence completion",
        "short_title": "Sentence completion",
        "badges": [("Gap", "gap"), ("Core", "core")],
        "what": (
            "You complete sentences using words from the passage. Instructions limit how many words "
            "you may use — often NO MORE THAN TWO WORDS AND/OR A NUMBER. Copy spelling exactly; "
            "the question sentence is usually a paraphrase of the passage."
        ),
        "steps": [
            "Read the word limit before you scan — one extra word makes the answer wrong.",
            "Underline keywords in the incomplete sentence and find the paraphrased location.",
            "Check grammar: the gap must fit the sentence structure (noun, verb, adjective).",
            "Copy the exact word(s) from the passage — do not paraphrase your answer.",
        ],
        "example_layout": "gap",
        "worked_example": {
            "sentence": "The report attributes the delay chiefly to _____ in supply chains.",
            "passage_html": (
                "…the delay chiefly to <span class=\"rs-hl-green\">disruption</span> in supply chains…"
            ),
            "answer": "disruption",
            "footnote": "Copy exactly — do not paraphrase. Answer: disruption (same spelling as the passage).",
        },
        "practice": {
            "instructions": "Choose the word that correctly completes each sentence and obeys the word limit.",
            "passage": (
                "Officials warned that further shocks could slow delivery schedules through the autumn. "
                "The report attributes the delay chiefly to disruption in supply chains."
            ),
            "questions": [
                {
                    "id": "sc-1",
                    "prompt": "The report attributes the delay chiefly to _____ in supply chains.",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "disruption"},
                        {"value": "b", "label": "disrupt"},
                        {"value": "c", "label": "disruptive"},
                        {"value": "d", "label": "disrupted"},
                    ],
                    "answer": "a",
                    "explanation": "After 'to' you need a noun — copy disruption from the passage.",
                },
                {
                    "id": "sc-2",
                    "prompt": "Further shocks could _____ delivery schedules. (one word)",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "slow"},
                        {"value": "b", "label": "slowly"},
                        {"value": "c", "label": "slowness"},
                        {"value": "d", "label": "slowed"},
                    ],
                    "answer": "a",
                    "explanation": "Modal 'could' + base verb slow — grammar and meaning both match.",
                },
            ],
        },
    },
    {
        "id": "summary-completion",
        "title": "Summary completion",
        "short_title": "Summary completion",
        "badges": [("Gap", "gap"), ("Box", "core")],
        "what": (
            "A summary of part of the passage contains gaps. You either choose words from a box "
            "or write words from the passage. Distractors in the box often fit grammatically but "
            "change the meaning — always verify against the passage."
        ),
        "steps": [
            "Read the whole summary first to understand the overall argument.",
            "Predict the word class needed for each gap (noun, verb, adjective).",
            "If a word box is given, eliminate options that break meaning even if grammar fits.",
            "Return to the passage to confirm — never choose from the box from memory alone.",
        ],
        "example_layout": "summary",
        "worked_example": {
            "summary": (
                "Urban forests cool neighbourhoods and absorb stormwater. Cities now treat green "
                "corridors as core _____ rather than optional parks."
            ),
            "word_box": ["infrastructure", "legislation", "competition", "pollution"],
            "correct_word": "infrastructure",
            "passage_hint": "…treat green corridors as core infrastructure rather than optional parks.",
            "explanation": (
                "Infrastructure fits meaning and grammar. Legislation and pollution change the "
                "sense; competition is unrelated."
            ),
        },
        "practice": {
            "instructions": "Complete the summary using the best word from the box or passage.",
            "passage": (
                "Remote teams often report stable productivity after the first year. Managers rarely "
                "cite video fatigue as the main obstacle; unclear priorities dominate exit surveys."
            ),
            "questions": [
                {
                    "id": "sum-1",
                    "prompt": "Summary: Managers rarely cite _____ as the main obstacle to remote work.",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "video fatigue"},
                        {"value": "b", "label": "office rent"},
                        {"value": "c", "label": "annual bonuses"},
                        {"value": "d", "label": "commuting costs"},
                    ],
                    "answer": "a",
                    "explanation": "The passage states managers rarely cite video fatigue as the main obstacle.",
                },
                {
                    "id": "sum-2",
                    "prompt": "Summary: _____ feature prominently in exit surveys.",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "Unclear priorities"},
                        {"value": "b", "label": "Higher salaries"},
                        {"value": "c", "label": "Video fatigue"},
                        {"value": "d", "label": "Office location"},
                    ],
                    "answer": "a",
                    "explanation": "Unclear priorities dominate exit surveys — the summary gap needs that idea.",
                },
            ],
        },
    },
    {
        "id": "matching-information",
        "title": "Matching information",
        "short_title": "Matching information",
        "badges": [("Matching", "matching"), ("Core", "core")],
        "what": (
            "You match statements to the paragraph (A, B, C…) where the information appears. "
            "Paragraphs may be used more than once; some paragraphs may not be used at all."
        ),
        "steps": [
            "Read all statements first — underline unique keywords in each.",
            "Scan paragraph openings to build a quick map of topics.",
            "Search for paraphrases, not identical wording — IELTS rarely repeats phrases.",
            "Do not assume each paragraph is used only once; check the instructions.",
        ],
        "example_layout": "match_info",
        "worked_example": {
            "paragraphs": [
                {"label": "A", "text": "Early pilots near schools recorded lower peak pollution after junction redesigns."},
                {"label": "B", "text": "Freight windows that remain unclear can create new bottlenecks for residents."},
                {"label": "C", "text": "Successful programmes publish baseline traffic data before trials begin."},
            ],
            "statements": [
                {
                    "text": "Air quality improved near sensitive sites.",
                    "answer": "A",
                    "explanation": "Lower peak pollution near schools matches paragraph A.",
                },
                {
                    "text": "Transparency about data helps justify difficult changes.",
                    "answer": "C",
                    "explanation": "Publishing baseline data before trials aligns with paragraph C.",
                },
            ],
        },
        "practice": {
            "instructions": "Which paragraph (A, B, or C) contains each piece of information?",
            "passage": (
                "Paragraph A: The museum extended opening hours after visitor numbers rose among "
                "families during school holidays. Paragraph B: Curators digitised fragile manuscripts "
                "to reduce handling damage. Paragraph C: A new wing dedicated to local industry "
                "opened following a regional grant."
            ),
            "questions": [
                {
                    "id": "mi-1",
                    "prompt": "Visitor numbers increased among families in holiday periods.",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "Paragraph A"},
                        {"value": "b", "label": "Paragraph B"},
                        {"value": "c", "label": "Paragraph C"},
                        {"value": "d", "label": "Not stated"},
                    ],
                    "answer": "a",
                    "explanation": "Paragraph A links extended hours to rising family visitors during school holidays.",
                },
                {
                    "id": "mi-2",
                    "prompt": "Funding from a regional source supported a new exhibition space.",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "Paragraph A"},
                        {"value": "b", "label": "Paragraph B"},
                        {"value": "c", "label": "Paragraph C"},
                        {"value": "d", "label": "Not stated"},
                    ],
                    "answer": "c",
                    "explanation": "Paragraph C describes a new wing opened following a regional grant.",
                },
                {
                    "id": "mi-3",
                    "prompt": "Digital copies were made to protect delicate documents.",
                    "type": "choice",
                    "options": [
                        {"value": "a", "label": "Paragraph A"},
                        {"value": "b", "label": "Paragraph B"},
                        {"value": "c", "label": "Paragraph C"},
                        {"value": "d", "label": "Not stated"},
                    ],
                    "answer": "b",
                    "explanation": "Paragraph B mentions digitising manuscripts to reduce handling damage.",
                },
            ],
        },
    },
]

READING_JOURNEY_STAGES = [
    {"id": "strategies", "title": "Strategies", "num": 1},
    {"id": "question-types", "title": "Question types", "num": 2},
    {"id": "skills", "title": "Skills lab", "num": 3},
    {"id": "time", "title": "Time plan", "num": 4},
]
