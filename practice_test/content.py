"""Hardcoded content for the IELTS practice test.

Kept intentionally small so this app is self-contained — no admin panel
needed to ship the v1 of /test/. The data structures here are stable so the
templates can render them directly.
"""

# ===================== READING =====================
# 3 passages × ~13 questions each = 40 questions total.
# Question types: TFNG, gap fill, matching headings, multiple choice.

READING_PASSAGES = [
    {
        "number": 1,
        "title": "The rise of urban farming",
        "paragraphs": [
            "Urban farming — the practice of cultivating, processing and distributing food in or around urban areas — has grown rapidly in many cities over the last decade. Rooftops, balconies and even disused warehouses are being converted into productive growing spaces. Supporters argue that locally grown produce reduces transport costs, cuts greenhouse gas emissions and brings fresh food to neighbourhoods that have long lacked access to it.",
            "Yet urban farming is not a new idea. During both World Wars, governments encouraged citizens to plant ‘victory gardens’ in order to ease pressure on food supplies. What is new is the scale of recent expansion and the technologies involved. Vertical farms, in which crops are grown in stacked layers under LED lighting, can produce many times more lettuce per square metre than a traditional field, with a fraction of the water.",
            "Critics, however, point out that the energy demands of indoor farms are substantial. Lighting plants 16 hours a day requires reliable electricity, and unless that electricity comes from renewable sources, the climate benefits may be smaller than they first appear. There are also questions about whether vertical farms can ever produce staple crops such as wheat or rice at a competitive price.",
            "Despite the debate, councils in cities including Paris, Singapore and Toronto have set ambitious targets for the share of food they want to grow locally. Whether those targets are realistic remains to be seen, but the conversation about how cities feed themselves has clearly shifted.",
        ],
        "questions": [
            {"type": "tfng", "id": "r1q1", "text": "Urban farming has only become common since the year 2000.", "answer": "FALSE"},
            {"type": "tfng", "id": "r1q2", "text": "Vertical farms typically use less water than traditional fields.", "answer": "TRUE"},
            {"type": "tfng", "id": "r1q3", "text": "Most cities now produce more than half of their own food.", "answer": "NOT GIVEN"},
            {"type": "tfng", "id": "r1q4", "text": "Indoor farms can have high energy requirements.", "answer": "TRUE"},
            {"type": "tfng", "id": "r1q5", "text": "Vertical farms have proven they can produce wheat cheaply.", "answer": "FALSE"},
            {"type": "gap", "id": "r1q6", "text": "During the World Wars, citizens were urged to plant ____ gardens.", "answer": "victory"},
            {"type": "gap", "id": "r1q7", "text": "Stacked indoor crops are typically grown under ____ lighting.", "answer": "LED"},
            {"type": "gap", "id": "r1q8", "text": "Critics worry indoor lighting needs reliable ____.", "answer": "electricity"},
            {"type": "mcq", "id": "r1q9", "text": "What is the main idea of paragraph 1?",
             "options": ["Cities have always grown their own food.", "Urban farming has spread fast and is changing how cities source food.", "Vertical farming is the cheapest method.", "Rooftops are illegal to use for crops."],
             "answer": "Urban farming has spread fast and is changing how cities source food."},
            {"type": "mcq", "id": "r1q10", "text": "What is one drawback of vertical farming mentioned?",
             "options": ["Slow growth time", "High energy use", "Lack of demand", "Poor taste"],
             "answer": "High energy use"},
            {"type": "mcq", "id": "r1q11", "text": "Which city is NOT mentioned as having set local-food targets?",
             "options": ["Paris", "Singapore", "Toronto", "Lima"],
             "answer": "Lima"},
            {"type": "tfng", "id": "r1q12", "text": "The author concludes that urban farming targets are unrealistic.", "answer": "NOT GIVEN"},
            {"type": "gap", "id": "r1q13", "text": "Disused ____ are sometimes converted into growing spaces.", "answer": "warehouses"},
        ],
    },
    {
        "number": 2,
        "title": "Sleep and memory",
        "paragraphs": [
            "Sleep researchers have long suspected that one of the brain’s main jobs during the night is to sort through what we learned during the day. Experiments first conducted in the 1990s suggested that periods of slow-wave sleep — the deepest stage — play a key role in consolidating factual memories such as names, dates and vocabulary. More recent studies indicate that rapid eye movement (REM) sleep helps the brain make creative connections between unrelated pieces of information.",
            "The implication for students is significant. Cramming late into the night may help in the very short term, but if it cuts into sleep it can actually reduce how much is recalled the following morning. Conversely, learning new material a few hours before bed and allowing a full night’s sleep appears to boost retention.",
            "What is less clear is whether short naps offer the same benefits. Some studies have found that a 20-minute nap improves alertness without delivering meaningful memory gains, while a 90-minute nap that includes both slow-wave and REM stages can yield benefits closer to a full night’s sleep — though obviously few workplaces will tolerate naps of that length.",
        ],
        "questions": [
            {"type": "tfng", "id": "r2q1", "text": "Slow-wave sleep mostly helps with creative thinking.", "answer": "FALSE"},
            {"type": "tfng", "id": "r2q2", "text": "REM sleep can help link different ideas together.", "answer": "TRUE"},
            {"type": "tfng", "id": "r2q3", "text": "Cramming all night always improves test scores.", "answer": "FALSE"},
            {"type": "tfng", "id": "r2q4", "text": "Twenty-minute naps boost long-term memory significantly.", "answer": "NOT GIVEN"},
            {"type": "tfng", "id": "r2q5", "text": "Some workplaces officially encourage 90-minute naps.", "answer": "NOT GIVEN"},
            {"type": "gap", "id": "r2q6", "text": "The 1990s studies highlighted the role of ____-wave sleep.", "answer": "slow"},
            {"type": "gap", "id": "r2q7", "text": "REM stands for rapid eye ____.", "answer": "movement"},
            {"type": "gap", "id": "r2q8", "text": "A short nap of about ____ minutes improves alertness.", "answer": "20"},
            {"type": "mcq", "id": "r2q9", "text": "Which memory benefit is linked with REM sleep?",
             "options": ["Memorising names", "Linking unrelated ideas", "Repeating dates", "Recalling phone numbers"],
             "answer": "Linking unrelated ideas"},
            {"type": "mcq", "id": "r2q10", "text": "What is the writer's advice to students?",
             "options": ["Cram all night before tests", "Skip sleep after studying", "Sleep a full night after studying", "Only study in the morning"],
             "answer": "Sleep a full night after studying"},
            {"type": "mcq", "id": "r2q11", "text": "Why might workplaces resist 90-minute naps?",
             "options": ["Naps cost money", "They are too long for most jobs", "They reduce productivity", "They are illegal"],
             "answer": "They are too long for most jobs"},
            {"type": "tfng", "id": "r2q12", "text": "Sleeping after learning new material helps retention.", "answer": "TRUE"},
            {"type": "gap", "id": "r2q13", "text": "A nap of ____ minutes can include both slow-wave and REM stages.", "answer": "90"},
        ],
    },
    {
        "number": 3,
        "title": "Coral reefs under pressure",
        "paragraphs": [
            "Coral reefs cover less than one per cent of the ocean floor but are home to roughly a quarter of all marine species. They are also among the ecosystems most exposed to climate change. When sea temperatures rise by even one degree above the long-term average for several weeks, corals expel the colourful algae that live inside them and turn white — a phenomenon known as bleaching. If conditions do not improve quickly, bleached corals starve and die.",
            "Scientists have observed widespread bleaching events in the Great Barrier Reef in 2016, 2017, 2020 and 2022. Each event has reduced the diversity of species the reef supports. Some governments have responded by reducing nutrient runoff from agriculture, which lowers other stresses on the corals, while others are funding research into heat-resistant coral varieties that could be planted on damaged reefs.",
            "Even so, marine scientists agree that the long-term future of coral reefs depends on global decisions about greenhouse gas emissions. Local protection measures can buy time, but cannot replace the need to limit warming itself.",
        ],
        "questions": [
            {"type": "tfng", "id": "r3q1", "text": "Coral reefs cover roughly a quarter of the ocean floor.", "answer": "FALSE"},
            {"type": "tfng", "id": "r3q2", "text": "Bleached corals lose the algae living inside them.", "answer": "TRUE"},
            {"type": "tfng", "id": "r3q3", "text": "All bleached corals die immediately.", "answer": "FALSE"},
            {"type": "tfng", "id": "r3q4", "text": "Reducing farm runoff is one local response to coral stress.", "answer": "TRUE"},
            {"type": "tfng", "id": "r3q5", "text": "Heat-resistant corals have already replaced most damaged reefs.", "answer": "NOT GIVEN"},
            {"type": "gap", "id": "r3q6", "text": "Corals turn white in a process called ____.", "answer": "bleaching"},
            {"type": "gap", "id": "r3q7", "text": "The text mentions widespread bleaching of the Great ____ Reef.", "answer": "Barrier"},
            {"type": "gap", "id": "r3q8", "text": "Scientists are funding research into ____-resistant corals.", "answer": "heat"},
            {"type": "mcq", "id": "r3q9", "text": "What proportion of marine species depend on reefs?",
             "options": ["About one tenth", "About a quarter", "About half", "Almost all"],
             "answer": "About a quarter"},
            {"type": "mcq", "id": "r3q10", "text": "Which year is NOT listed for major Great Barrier Reef bleaching?",
             "options": ["2016", "2017", "2020", "2019"],
             "answer": "2019"},
            {"type": "mcq", "id": "r3q11", "text": "What do scientists agree is essential for reefs long-term?",
             "options": ["Tourism limits", "Cutting emissions globally", "Bigger fishing quotas", "Removing all coral"],
             "answer": "Cutting emissions globally"},
            {"type": "tfng", "id": "r3q12", "text": "Local action alone is enough to save coral reefs.", "answer": "FALSE"},
            {"type": "tfng", "id": "r3q13", "text": "Coral reefs have steadily grown more diverse since 2016.", "answer": "FALSE"},
            {"type": "gap", "id": "r3q14", "text": "Local steps can buy time but cannot replace cutting global ____.", "answer": "emissions"},
        ],
    },
]


def reading_total_questions() -> int:
    return sum(len(p["questions"]) for p in READING_PASSAGES)


# ===================== WRITING =====================

WRITING_TASKS = {
    "task1": {
        "kind": "task1",
        "title": "Writing — Task 1",
        "minutes": 20,
        "min_words": 150,
        "instructions": (
            "The chart below shows the proportion of households using four "
            "different modes of transport for commuting in a European city "
            "between 1990 and 2020. Summarise the information by selecting "
            "and reporting the main features, and make comparisons where relevant."
        ),
        # Inline SVG bar chart so we don't need an image asset.
        "chart_svg": """
<svg viewBox="0 0 520 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Bar chart of household commuting modes">
  <style>
    .ax { stroke:#cbd5e1; stroke-width:1; }
    .gr { stroke:#eef0ef; stroke-width:1; }
    .lab{ font: 600 11px 'Segoe UI', Arial, sans-serif; fill:#3a4252; }
    .ttl{ font: 700 12px 'Segoe UI', Arial, sans-serif; fill:#1a1f2b; }
    .val{ font: 700 10px 'Segoe UI', Arial, sans-serif; fill:#fff; }
  </style>
  <text x="20" y="18" class="ttl">Household commuting mode (%)</text>

  <!-- Y gridlines + labels -->
  <g>
    <line x1="50" y1="40"  x2="500" y2="40"  class="gr"/>
    <line x1="50" y1="80"  x2="500" y2="80"  class="gr"/>
    <line x1="50" y1="120" x2="500" y2="120" class="gr"/>
    <line x1="50" y1="160" x2="500" y2="160" class="gr"/>
    <line x1="50" y1="200" x2="500" y2="200" class="ax"/>
    <text x="22" y="44"  class="lab">80</text>
    <text x="22" y="84"  class="lab">60</text>
    <text x="22" y="124" class="lab">40</text>
    <text x="22" y="164" class="lab">20</text>
    <text x="28" y="204" class="lab">0</text>
  </g>

  <!-- 4 grouped bars per category (Car, Bus, Bike, Walk) for 1990, 2005, 2020 -->
  <g transform="translate(80,0)">
    <!-- Car: 65, 60, 50  → height = pct*2 -->
    <rect x="0"  y="70"  width="14" height="130" fill="#2d6a0a"/>
    <rect x="16" y="80"  width="14" height="120" fill="#1e3a5f"/>
    <rect x="32" y="100" width="14" height="100" fill="#6f4ed0"/>
    <text x="20" y="218" class="lab">Car</text>
  </g>
  <g transform="translate(190,0)">
    <!-- Bus: 18, 22, 25 -->
    <rect x="0"  y="164" width="14" height="36" fill="#2d6a0a"/>
    <rect x="16" y="156" width="14" height="44" fill="#1e3a5f"/>
    <rect x="32" y="150" width="14" height="50" fill="#6f4ed0"/>
    <text x="20" y="218" class="lab">Bus</text>
  </g>
  <g transform="translate(300,0)">
    <!-- Bike: 7, 10, 17 -->
    <rect x="0"  y="186" width="14" height="14" fill="#2d6a0a"/>
    <rect x="16" y="180" width="14" height="20" fill="#1e3a5f"/>
    <rect x="32" y="166" width="14" height="34" fill="#6f4ed0"/>
    <text x="14" y="218" class="lab">Bike</text>
  </g>
  <g transform="translate(410,0)">
    <!-- Walk: 10, 8, 8 -->
    <rect x="0"  y="180" width="14" height="20" fill="#2d6a0a"/>
    <rect x="16" y="184" width="14" height="16" fill="#1e3a5f"/>
    <rect x="32" y="184" width="14" height="16" fill="#6f4ed0"/>
    <text x="12" y="218" class="lab">Walk</text>
  </g>

  <!-- Legend -->
  <g transform="translate(380,18)">
    <rect x="0"  y="0" width="10" height="10" fill="#2d6a0a"/><text x="14" y="9" class="lab">1990</text>
    <rect x="46" y="0" width="10" height="10" fill="#1e3a5f"/><text x="60" y="9" class="lab">2005</text>
    <rect x="92" y="0" width="10" height="10" fill="#6f4ed0"/><text x="106" y="9" class="lab">2020</text>
  </g>
</svg>
""",
    },
    "task2": {
        "kind": "task2",
        "title": "Writing — Task 2",
        "minutes": 40,
        "min_words": 250,
        "instructions": (
            "Some people believe that universities should focus on providing "
            "academic skills rather than preparing students for a specific career. "
            "Others argue that the main purpose of university is to make graduates "
            "ready for the job market. Discuss both views and give your own opinion."
        ),
    },
}


# ===================== SPEAKING =====================

SPEAKING_PARTS = [
    {
        "part": 1,
        "title": "Part 1 — Introduction and interview",
        "minutes": 5,
        "intro": (
            "You will be asked five everyday questions about familiar topics "
            "such as your hometown, studies, work and free time. Try to give "
            "short, natural answers of 2–4 sentences each."
        ),
        "questions": [
            "Can you tell me your full name and where you are from?",
            "Do you work or are you a student? Could you describe what you do?",
            "What do you usually do in your free time?",
            "How often do you read books or articles in English?",
            "What kind of weather do you prefer, and why?",
        ],
    },
    {
        "part": 2,
        "title": "Part 2 — The long turn (cue card)",
        "minutes": 4,
        "intro": (
            "You will be given a topic card. You have ONE minute to prepare "
            "(notes are encouraged). Then speak for 1–2 minutes without "
            "stopping. The examiner may ask one short follow-up question."
        ),
        "prep_seconds": 60,
        "questions": [
            (
                "Describe a skill you would like to learn in the future. "
                "You should say:\n"
                "  • what the skill is\n"
                "  • why you want to learn it\n"
                "  • how you plan to learn it\n"
                "and explain how learning this skill will benefit you."
            ),
        ],
    },
    {
        "part": 3,
        "title": "Part 3 — Two-way discussion",
        "minutes": 5,
        "intro": (
            "You will discuss more abstract ideas connected to the Part 2 topic. "
            "Try to give longer answers, explain your reasoning and use examples."
        ),
        "questions": [
            "Why do you think some people find it harder than others to learn new skills as adults?",
            "How has technology changed the way people learn new skills today?",
            "Do you think schools focus enough on practical life skills? Why or why not?",
            "In your view, will future jobs require people to keep learning new skills throughout their lives?",
        ],
    },
]


def speaking_total_questions() -> int:
    return sum(len(p["questions"]) for p in SPEAKING_PARTS)


# ===================== SPEAKING — VIDEO FLOW =====================
# Used by the new video-driven /test/speaking/ page. Each step plays one
# video; ``question`` steps then auto-record the student's answer.
#
# Question texts mirror what's spoken in the videos so that GPT can score the
# response in context. Edit a ``text`` here if the underlying video changes —
# the rest of the flow (video order, parts, prep timer) is structural.

# ``max_seconds`` is the hard recording cap for each question. When the
# student reaches it the recorder stops automatically and the test advances.
# Values mirror real IELTS timing: short answers in Part 1, the long turn in
# Part 2 gets the most time, Part 3 answers sit in between.
_P1_MAX = 90    # 1.5 min per Part 1 answer
_P2_LONG_MAX = 240  # 4 min for the long turn (1–2 min expected, generous cap)
_P2_FOLLOWUP_MAX = 90
_P3_MAX = 180   # 3 min per Part 3 answer

SPEAKING_VIDEO_FLOW = [
    # The opening clip greets the candidate and asks their name, so it records
    # an answer just like a question (it is not a passive intro).
    {"kind": "question", "video": "intro.mp4", "part": 1, "index": 0,
     "max_seconds": _P1_MAX,
     "text": "Can you tell me your full name, please?"},
    {"kind": "intro", "video": "intro_p1.mp4", "label": "Part 1 introduction"},

    {"kind": "question", "video": "p1_q1.mp4", "part": 1, "index": 1,
     "max_seconds": _P1_MAX,
     "text": "Can you tell me your full name and where you are from?"},
    {"kind": "question", "video": "p1_q2.mp4", "part": 1, "index": 2,
     "max_seconds": _P1_MAX,
     "text": "Do you work or are you a student? Could you describe what you do?"},
    {"kind": "question", "video": "p1_q3.mp4", "part": 1, "index": 3,
     "max_seconds": _P1_MAX,
     "text": "What do you usually do in your free time?"},
    {"kind": "question", "video": "p1_q4.mp4", "part": 1, "index": 4,
     "max_seconds": _P1_MAX,
     "text": "How often do you read books or articles in English?"},
    {"kind": "question", "video": "p1_q5.mp4", "part": 1, "index": 5,
     "max_seconds": _P1_MAX,
     "text": "What kind of weather do you prefer, and why?"},

    {"kind": "intro", "video": "intro_p2.mp4", "label": "Part 2 introduction"},

    {"kind": "question", "video": "p2_q1.mp4", "part": 2, "index": 0,
     "prep_seconds": 60, "max_seconds": _P2_LONG_MAX,
     "text": (
         "Describe a skill you would like to learn in the future. "
         "You should say:\n"
         "  • what the skill is\n"
         "  • why you want to learn it\n"
         "  • how you plan to learn it\n"
         "and explain how learning this skill will benefit you."
     )},
    {"kind": "question", "video": "p2_followup.mp4", "part": 2, "index": 1,
     "max_seconds": _P2_FOLLOWUP_MAX,
     "text": "Do you think this skill is something most people would find useful? Why?"},

    {"kind": "intro", "video": "intro_p3.mp4", "label": "Part 3 introduction"},

    {"kind": "question", "video": "p3_q1.mp4", "part": 3, "index": 0,
     "max_seconds": _P3_MAX,
     "text": "Why do you think some people find it harder than others to learn new skills as adults?"},
    {"kind": "question", "video": "p3_q2.mp4", "part": 3, "index": 1,
     "max_seconds": _P3_MAX,
     "text": "How has technology changed the way people learn new skills today?"},
    {"kind": "question", "video": "p3_q3.mp4", "part": 3, "index": 2,
     "max_seconds": _P3_MAX,
     "text": "Do you think schools focus enough on practical life skills? Why or why not?"},
    {"kind": "question", "video": "p3_q4.mp4", "part": 3, "index": 3,
     "max_seconds": _P3_MAX,
     "text": "In your view, will future jobs require people to keep learning new skills throughout their lives?"},

    {"kind": "outro", "video": "outro.mp4", "label": "End of test"},
]


def speaking_video_questions_total() -> int:
    return sum(1 for s in SPEAKING_VIDEO_FLOW if s["kind"] == "question")


# ===================== LISTENING =====================
# Audio files are not yet shipped; the runner shows a Coming Soon banner but
# keeps the section structure intact so it can plug in later without changes.

LISTENING_SECTIONS = [
    {"number": 1, "title": "Section 1 — A conversation (everyday context)", "minutes": 7, "questions": 10},
    {"number": 2, "title": "Section 2 — A monologue (everyday context)",   "minutes": 7, "questions": 10},
    {"number": 3, "title": "Section 3 — A conversation (academic context)", "minutes": 8, "questions": 10},
    {"number": 4, "title": "Section 4 — A monologue (academic lecture)",    "minutes": 8, "questions": 10},
]
LISTENING_AVAILABLE = False  # flip when an audio asset + question bank ship
