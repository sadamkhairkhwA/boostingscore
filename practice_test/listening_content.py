"""Scripts + question bank for the IELTS Listening test.

Each section stores its audio as a list of ``(speaker, text)`` lines. Different
speakers map to different OpenAI TTS voices via ``VOICES`` so dialogues sound
like a real multi-person IELTS recording. Scripts include light, natural
hesitations and paraphrase the question wording (as real IELTS does).

Question ``type`` controls how it is rendered and graded:
    form / note / sentence / table / gap  -> text input, exact-answer match
    short                                 -> keyword match
    mcq                                   -> radio options
    matching / map                        -> dropdown from a shared option list

Answers always appear in the same order they are spoken, and difficulty rises
from Section 1 (everyday) to Section 4 (academic monologue).
"""

# Speaker label -> OpenAI TTS voice.
VOICES: dict[str, str] = {
    "NARRATOR": "fable",
    "W": "nova",
    "W2": "shimmer",
    "M": "onyx",
    "M2": "echo",
}

# Per-speaker delivery instructions (passed to gpt-4o-mini-tts).
INSTRUCTIONS: dict[str, str] = {
    "M": (
        "Speak in a warm, natural, conversational British English accent, like a "
        "real person chatting on the phone — relaxed everyday pace, light "
        "intonation, natural rhythm. Not a news reader."
    ),
    "M2": (
        "Speak in a clear, friendly British English accent like a university "
        "tutor or lecturer — measured, engaged and natural, never robotic."
    ),
    "W": (
        "Speak in a warm, natural, conversational British English accent, like a "
        "real person chatting on the phone — relaxed everyday pace, light "
        "intonation and natural rhythm. Not a news reader."
    ),
    "W2": (
        "Speak in a friendly, polished British English accent like a tour guide "
        "addressing visitors — clear, welcoming and natural, with light warmth."
    ),
    "NARRATOR": (
        "Speak in a clear, neutral British English accent at a steady, natural "
        "exam pace. Calm and human, easy to follow, but not stiff or robotic."
    ),
}
DEFAULT_INSTRUCTIONS = INSTRUCTIONS["NARRATOR"]

OPENING_NARRATION = (
    "Welcome to the IELTS practice Listening test. You will hear four recordings "
    "and you must answer the questions for each section as you listen. "
    "The recording is played once only."
)

SECTION_BREAK = (
    "That is the end of the section. You now have half a minute to check your "
    "answers. We will now move on to the next section."
)


# Shared map for Section 2 (map labelling). Letters A–G mark fixed positions;
# the Section 2 script gives directions consistent with these positions.
SECTION2_MAP_SVG = """
<svg viewBox="0 0 360 300" role="img" aria-label="Map of Eastfield Botanical Garden"
     xmlns="http://www.w3.org/2000/svg" class="pt-map-svg">
  <rect x="0" y="0" width="360" height="300" rx="10" fill="#f3f5ef"/>
  <path d="M40 40 H320 V260 H40 Z" fill="#e7ede0" stroke="#c4cfb6" stroke-width="2"/>
  <!-- lake -->
  <ellipse cx="250" cy="135" rx="46" ry="30" fill="#bcd6e6" stroke="#9cbdd2" stroke-width="2"/>
  <text x="250" y="139" text-anchor="middle" font-size="10" fill="#5b7488">Lake</text>
  <!-- main paths -->
  <path d="M180 260 V70" stroke="#cbb892" stroke-width="6" fill="none" stroke-linecap="round"/>
  <path d="M70 165 H300" stroke="#cbb892" stroke-width="6" fill="none" stroke-linecap="round"/>
  <!-- entrance -->
  <rect x="156" y="262" width="48" height="18" rx="4" fill="#3a3a3a"/>
  <text x="180" y="275" text-anchor="middle" font-size="9" fill="#fff">ENTRANCE</text>
  <!-- lettered markers -->
  <g font-size="12" font-weight="700" text-anchor="middle">
    <circle cx="80"  cy="210" r="14" fill="#fff" stroke="#2d6a0a" stroke-width="2"/><text x="80"  y="214" fill="#2d6a0a">A</text>
    <circle cx="285" cy="210" r="14" fill="#fff" stroke="#2d6a0a" stroke-width="2"/><text x="285" y="214" fill="#2d6a0a">B</text>
    <circle cx="80"  cy="120" r="14" fill="#fff" stroke="#2d6a0a" stroke-width="2"/><text x="80"  y="124" fill="#2d6a0a">C</text>
    <circle cx="180" cy="120" r="14" fill="#fff" stroke="#2d6a0a" stroke-width="2"/><text x="180" y="124" fill="#2d6a0a">D</text>
    <circle cx="180" cy="210" r="14" fill="#fff" stroke="#2d6a0a" stroke-width="2"/><text x="180" y="214" fill="#2d6a0a">E</text>
    <circle cx="120" cy="70"  r="14" fill="#fff" stroke="#2d6a0a" stroke-width="2"/><text x="120" y="74"  fill="#2d6a0a">F</text>
    <circle cx="240" cy="70"  r="14" fill="#fff" stroke="#2d6a0a" stroke-width="2"/><text x="240" y="74"  fill="#2d6a0a">G</text>
  </g>
</svg>
"""

# Option bank shared by the Section 2 map-labelling questions.
MAP_OPTIONS = ["A", "B", "C", "D", "E", "F", "G"]

# Option bank for the Section 3 matching task.
S3_MATCH_OPTIONS = [
    "A — recommended by the tutor",
    "B — too time-consuming",
    "C — not representative",
    "D — reaches only a limited group",
]


LISTENING_TEST = {
    "sections": [
        # ===================== SECTION 1 — everyday, form completion =========
        {
            "number": 1,
            "title": "Section 1 — Sports centre membership enquiry",
            "instructions": "Questions 1–10. Complete the form. Write ONE WORD AND/OR A NUMBER for each answer.",
            "lines": [
                ("NARRATOR",
                 "Section 1. You will hear a telephone conversation between a man "
                 "who wants to join a sports centre and a receptionist. First, you "
                 "have some time to look at questions 1 to 10."),
                ("W", "Good morning, Greenfield Sports Centre — Marina speaking. How can I help?"),
                ("M", "Oh, hi. Erm, I'm thinking of joining the gym, and I just wanted to ask about the membership options, if that's okay?"),
                ("W", "Of course. So, we've got three plans. The Standard one — that's just the gym — is forty pounds a month."),
                ("M", "Forty, right."),
                ("W", "Then there's Plus, which is the gym plus all the classes, and that one comes to fifty-five pounds a month."),
                ("M", "Okay, fifty-five. And, um, is there a family option? There might be four of us."),
                ("W", "There is, yes. The Family plan covers up to four people, and that's ninety pounds a month."),
                ("M", "Great. I think Plus is probably right for me. What classes are there?"),
                ("W", "Loads, really. The most popular one is on Monday evenings — that's the yoga. Spin and pilates are later in the week."),
                ("M", "Yoga on Mondays, lovely. And, sorry, when does the spin class actually start?"),
                ("W", "Spin's on Wednesdays. It kicks off at half past seven in the evening."),
                ("M", "Seven thirty. And how long do the classes run for?"),
                ("W", "They're all sixty minutes — so a full hour."),
                ("M", "Perfect. What about opening hours? I tend to train late."),
                ("W", "On weekdays we open at six in the morning, and the last entry's at ten at night. Weekends we close a bit earlier."),
                ("M", "Ten p.m. on weekdays, that works. So what do I need to bring to sign up?"),
                ("W", "Just bring some photo identification and proof of your address — oh, and a bank card to set up the monthly payment."),
                ("M", "Photo ID and proof of address, got it. Is there a joining fee?"),
                ("W", "There is a one-off joining fee, I'm afraid — it's twenty-five pounds."),
                ("M", "That's fine. My name's Daniel — surname Park, that's P-A-R-K."),
                ("W", "P-A-R-K. Lovely. We'll see you soon, Daniel."),
            ],
            "questions": [
                {"type": "form", "id": "l1q1", "text": "Standard membership: £____ per month", "answer": "40"},
                {"type": "form", "id": "l1q2", "text": "Plus membership: £____ per month", "answer": "55"},
                {"type": "form", "id": "l1q3", "text": "Family plan covers up to ____ people", "answer": ["four", "4"]},
                {"type": "mcq", "id": "l1q4", "text": "Which class is held on Monday evenings?",
                 "options": ["Yoga", "Spin", "Pilates", "Aerobics"], "answer": "Yoga"},
                {"type": "form", "id": "l1q5", "text": "Spin class start time: ____ pm (Wednesdays)", "answer": ["7:30", "7.30", "half past seven", "19:30"]},
                {"type": "form", "id": "l1q6", "text": "Length of each class: ____ minutes", "answer": "60"},
                {"type": "form", "id": "l1q7", "text": "Weekday closing time: ____ pm", "answer": "10"},
                {"type": "short", "id": "l1q8", "text": "Name TWO documents the member must bring.",
                 "answer_keywords": ["photo id", "photo identification", "identification", "proof of address", "address", "bank card", "id"]},
                {"type": "form", "id": "l1q9", "text": "One-off joining fee: £____", "answer": "25"},
                {"type": "form", "id": "l1q10", "text": "Surname spelling: P-A-R-____", "answer": "K"},
            ],
        },
        # ===================== SECTION 2 — monologue, MAP + MCQ + completion ==
        {
            "number": 2,
            "title": "Section 2 — Visit to Eastfield Botanical Garden",
            "instructions": "Questions 11–15: label the map. Questions 16–20: choose / complete the answer.",
            "map": {"svg": SECTION2_MAP_SVG, "options": MAP_OPTIONS},
            "lines": [
                ("NARRATOR",
                 "Section 2. You will hear a guide giving a short talk to visitors "
                 "at the Eastfield Botanical Garden. First, you have some time to "
                 "look at questions 11 to 20."),
                ("W2", "Hello everyone, and a warm welcome to Eastfield. I'm Sophie, and I'll point out the main areas before you explore on your own. Have a look at the map on your handout."),
                ("W2", "So, we're standing here at the entrance, at the bottom. If you take the path to your left, the very first area you reach is the Rose Garden — that's the marker on the lower left."),
                ("W2", "Now, carry straight on up that same left-hand path, and at the top of it you'll find the Tropical House — it's the one further up on the left."),
                ("W2", "Right in the middle of the garden, where the two main paths cross, that central point is the Bamboo Grove. You really can't miss it."),
                ("W2", "For the Lakeside Café, head along the path to the right until you reach the water — the café sits just beside the lake, up on the right."),
                ("W2", "The Gift Shop is up on the right, at the top of the garden — you'll see it marked on the map there."),
                ("W2", "A few important reminders. Inside the Tropical House you're welcome to take photographs, but please — no flash, as the bright light disturbs the butterflies."),
                ("W2", "In the Bamboo Grove, do keep your voices down. It's a designated quiet zone, mainly because of the birds that nest there."),
                ("W2", "And throughout the garden, please don't pick or touch the plants — some of them are surprisingly delicate."),
                ("W2", "Lunch is included today. It starts with a mushroom soup, followed by a light salad, and there's a fruit tart for dessert."),
                ("W2", "Finally, if you visit the gift shop, members of today's tour get ten per cent off everything. Enjoy your visit!"),
            ],
            "questions": [
                {"type": "map", "id": "l2q11", "text": "Rose Garden", "options": MAP_OPTIONS, "answer": "A"},
                {"type": "map", "id": "l2q12", "text": "Tropical House", "options": MAP_OPTIONS, "answer": "C"},
                {"type": "map", "id": "l2q13", "text": "Bamboo Grove", "options": MAP_OPTIONS, "answer": "E"},
                {"type": "map", "id": "l2q14", "text": "Lakeside Café", "options": MAP_OPTIONS, "answer": "B"},
                {"type": "map", "id": "l2q15", "text": "Gift Shop", "options": MAP_OPTIONS, "answer": "G"},
                {"type": "mcq", "id": "l2q16", "text": "In the Tropical House, visitors must not",
                 "options": ["take any photographs", "use a flash", "speak to the guide", "bring food inside"],
                 "answer": "use a flash"},
                {"type": "mcq", "id": "l2q17", "text": "The Bamboo Grove is a quiet zone mainly because of",
                 "options": ["nearby houses", "nesting birds", "fragile bamboo", "other visitors"],
                 "answer": "nesting birds"},
                {"type": "sentence", "id": "l2q18", "text": "Visitors are asked not to pick or touch the ____.", "answer": ["plants", "flowers"]},
                {"type": "sentence", "id": "l2q19", "text": "Lunch begins with mushroom ____.", "answer": "soup"},
                {"type": "form", "id": "l2q20", "text": "Tour members get ____ per cent off in the gift shop.", "answer": ["10", "ten"]},
            ],
        },
        # ===================== SECTION 3 — discussion, MATCHING + MCQ + comp ==
        {
            "number": 3,
            "title": "Section 3 — Tutorial on a research project",
            "instructions": "Questions 21–24: match each recruitment method to the tutor's view. Questions 25–30: complete / choose the answer.",
            "match": {"options": S3_MATCH_OPTIONS},
            "lines": [
                ("NARRATOR",
                 "Section 3. You will hear two students, Hannah and Omar, "
                 "discussing their research project with their tutor, Dr Reid. "
                 "First, you have some time to look at questions 21 to 30."),
                ("M2", "So, how's the project on urban green spaces coming along? Have you sorted out how you'll recruit people?"),
                ("W", "That's actually the tricky part. We thought about leaving flyers in cafés, but I'm worried the people we'd get just aren't representative of the wider community."),
                ("M2", "That's a fair concern — café-goers do tend to be a narrow slice. What else have you considered?"),
                ("M", "Door-to-door, knocking on people's doors. The trouble is it would take us absolutely ages to get fifty interviews that way."),
                ("M2", "Mm, yes — thorough, but it'll eat up your whole timetable. I wouldn't rely on it alone."),
                ("W", "We also wondered about social media. It's quick, but Omar pointed out we'd mainly reach younger people."),
                ("M2", "Right, so on its own it skews young. Now — here's my suggestion. If you put flyers in community centres, you tend to reach a real mix of ages. That's the approach I'd go with."),
                ("M", "Community centres — okay, that makes sense. So we'll plan around fifty residents in total."),
                ("W", "Across three different neighbourhoods, so we can compare."),
                ("M2", "Good. And will you offer anything for taking part?"),
                ("W", "We were thinking a small thank-you — a five-pound voucher each."),
                ("M2", "Reasonable. Just remember the deadline: your ethics application has to be in by the fifteenth of next month."),
                ("M", "The fifteenth, noted. And for the write-up, what matters most?"),
                ("M2", "The single most important thing — make sure you anonymise every quotation. No real names anywhere."),
            ],
            "questions": [
                {"type": "matching", "id": "l3q21", "text": "Flyers in cafés", "options": S3_MATCH_OPTIONS, "answer": "C — not representative"},
                {"type": "matching", "id": "l3q22", "text": "Door-to-door visits", "options": S3_MATCH_OPTIONS, "answer": "B — too time-consuming"},
                {"type": "matching", "id": "l3q23", "text": "Social media", "options": S3_MATCH_OPTIONS, "answer": "D — reaches only a limited group"},
                {"type": "matching", "id": "l3q24", "text": "Flyers in community centres", "options": S3_MATCH_OPTIONS, "answer": "A — recommended by the tutor"},
                {"type": "sentence", "id": "l3q25", "text": "They will interview around ____ residents in total.", "answer": ["50", "fifty"]},
                {"type": "sentence", "id": "l3q26", "text": "The survey will cover ____ different neighbourhoods.", "answer": ["three", "3"]},
                {"type": "mcq", "id": "l3q27", "text": "The tutor finally recommends recruiting through",
                 "options": ["cafés", "door-to-door visits", "social media", "community centres"],
                 "answer": "community centres"},
                {"type": "sentence", "id": "l3q28", "text": "Each participant will receive a £____ voucher.", "answer": "5"},
                {"type": "sentence", "id": "l3q29", "text": "The ethics application is due on the ____ of next month.", "answer": ["15", "15th", "fifteenth"]},
                {"type": "short", "id": "l3q30", "text": "What must the students do to every quotation?",
                 "answer_keywords": ["anonymise", "anonymize", "anonymous", "remove names", "no names"]},
            ],
        },
        # ===================== SECTION 4 — lecture, NOTES + TABLE + MCQ =======
        {
            "number": 4,
            "title": "Section 4 — Lecture: the science of habit formation",
            "instructions": "Questions 31–40. Complete the notes and table. Write ONE WORD AND/OR A NUMBER unless told otherwise.",
            "table": {
                "title": "How long habits take to become automatic",
                "columns": ["Type of habit", "Average time"],
                "rows": [
                    [{"text": "Any new behaviour (average)"}, {"q": "l4q36", "suffix": "days"}],
                    [{"text": "A simple morning habit"}, {"q": "l4q37", "suffix": "days"}],
                    [{"text": "A complex routine (e.g. exercise)"}, {"q": "l4q38", "prefix": "over", "suffix": "days"}],
                ],
            },
            "lines": [
                ("NARRATOR",
                 "Section 4. You will hear part of a lecture on the science of "
                 "habit formation. First, you have some time to look at questions "
                 "31 to 40."),
                ("M2", "Good afternoon. Today I want to unpack how habits actually form in the brain, and why some are so stubborn. Now, researchers describe every habit as a loop made up of three parts."),
                ("M2", "The first part is the cue — that's the trigger, the signal that tells your brain to begin a particular behaviour."),
                ("M2", "The second part is the routine itself, the action you carry out. And the third part is the reward — the pay-off that tells your brain this loop is worth repeating."),
                ("M2", "So, a famous study from the nineteen-nineties looked at London taxi drivers. What caught the researchers' attention was that the drivers had unusually well-developed hippocampi — that's the brain region tied to memory and navigation."),
                ("M2", "And remarkably, this change showed up after just two years on the job — clear evidence that the adult brain can be reshaped by repetition."),
                ("M2", "Now, how long does a new habit take to stick? Popular wisdom says twenty-one days, but the research paints a more varied picture. On average, a new behaviour takes about sixty-six days to become automatic."),
                ("M2", "Something very simple — say, drinking a glass of water each morning — might lock in within around twenty days. But a more demanding routine, like regular exercise, can take over two hundred days."),
                ("M2", "Here's the practical bit. To break a bad habit, the trick is not to fight the cue or the reward — keep those — but to swap out the routine in the middle for something better."),
                ("M2", "And one last finding I love: people who deliberately celebrate small wins are roughly three times more likely to stick with a new habit than those who wait for one big result."),
            ],
            "questions": [
                {"type": "sentence", "id": "l4q31", "text": "A habit is described as a loop with ____ parts.", "answer": ["three", "3"]},
                {"type": "note", "id": "l4q32", "text": "Part 1 — the ____ : the trigger to start a behaviour.", "answer": ["cue", "trigger"]},
                {"type": "note", "id": "l4q33", "text": "Part 3 — the ____ : the pay-off for repeating the loop.", "answer": "reward"},
                {"type": "mcq", "id": "l4q34", "text": "London taxi drivers were of interest because their",
                 "options": ["reaction times were faster", "hippocampi were unusually developed", "memory was poor", "navigation apps failed"],
                 "answer": "hippocampi were unusually developed"},
                {"type": "note", "id": "l4q35", "text": "The brain change appeared after only ____ years of driving.", "answer": ["two", "2"]},
                {"type": "table", "id": "l4q36", "text": "Average new habit — number of days", "answer": "66"},
                {"type": "table", "id": "l4q37", "text": "Simple morning habit — number of days", "answer": "20"},
                {"type": "table", "id": "l4q38", "text": "Complex routine — number of days", "answer": "200"},
                {"type": "mcq", "id": "l4q39", "text": "To break a bad habit, the lecturer advises changing the",
                 "options": ["cue", "routine", "reward", "location"],
                 "answer": "routine"},
                {"type": "sentence", "id": "l4q40", "text": "People who celebrate small wins are about ____ times more likely to succeed.", "answer": ["three", "3"]},
            ],
        },
    ],
}


def total_questions() -> int:
    return sum(len(s["questions"]) for s in LISTENING_TEST["sections"])
