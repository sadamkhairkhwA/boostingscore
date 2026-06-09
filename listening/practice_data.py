"""Data for the Listening "Practice by question type" section.

HOW TO ADD A PRACTICE SET
=========================
1. Drop the audio file in:  static/listening_practice/<filename>.mp3
   (or add a `lines` script below and run:
        python manage.py prepare_listening_practice_audio
    which synthesises the MP3 with the same multi-voice TTS pipeline used by
    the full Practice Tests.)
2. Add a dict to PRACTICE_SETS[<type-slug>] with this shape:

    {
        "id": "matching-2",                  # unique id for this set
        "title": "Volunteering roles",        # shown to the student
        "audio": "matching_2.mp3",            # file in static/listening_practice/
        "instructions": "Questions 1-5 ...",  # IELTS-style rubric
        "lines": [("W", "..."), ("M", "...")],# OPTIONAL: TTS script (not shown)
        "map_svg": MAP_SVG,                   # OPTIONAL: only for map sets
        "questions": [
            {
                "id": "q1",                   # unique within the set
                "render": "radio",            # radio | text | select
                "text": "Question text",
                "options": ["A  ...", "B  ..."],   # radio/select only
                "answer": "A  ...",                 # str OR list of accepted
                "explanation": "Why this is correct.",
            },
            ...
        ],
    }

`render` controls the input shown:
    radio  -> multiple choice (one option)
    select -> dropdown (matching / map labelling)
    text   -> free text (gap-fill, sentence completion, short answer)

`answer` may be a single string or a list of accepted answers (text inputs are
matched case-insensitively, ignoring surrounding punctuation).

Speaker codes for `lines` map to TTS voices (see practice_test/listening_content.py):
    NARRATOR, W, W2 (female), M, M2 (male).
"""

# Question types shown on the Listening home page, in IELTS order of familiarity.
QUESTION_TYPES = [
    {
        "slug": "multiple-choice",
        "name": "Multiple choice",
        "blurb": "Pick the correct option (A, B or C) from what you hear.",
    },
    {
        "slug": "gap-fill",
        "name": "Form, note & table completion",
        "blurb": "Fill the gaps in a form, set of notes or table.",
    },
    {
        "slug": "sentence",
        "name": "Sentence completion",
        "blurb": "Complete sentences with words from the recording.",
    },
    {
        "slug": "matching",
        "name": "Matching",
        "blurb": "Match items to a list of options or people.",
    },
    {
        "slug": "map",
        "name": "Map, plan & diagram labelling",
        "blurb": "Label a map or plan using letters from the audio.",
    },
    {
        "slug": "short-answer",
        "name": "Short-answer questions",
        "blurb": "Answer questions in one, two or three words / a number.",
    },
]

TYPE_LABELS = {t["slug"]: t["name"] for t in QUESTION_TYPES}


# --------------------------------------------------------------------------- #
#  Shared map for the map-labelling set (letters only, no place names).
# --------------------------------------------------------------------------- #
RIVERSIDE_PARK_MAP_SVG = """
<svg viewBox="0 0 460 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Riverside park map">
  <rect x="12" y="12" width="436" height="276" rx="16" fill="#f3f8f1" stroke="#86b07f" stroke-width="2"/>
  <path d="M120 286 V70 M120 150 H360" stroke="#cdbb95" stroke-width="14" stroke-linecap="round"/>
  <path d="M360 40 q40 90 0 230" fill="none" stroke="#a9d2ea" stroke-width="22" stroke-linecap="round"/>
  <rect x="96" y="262" width="56" height="20" rx="4" fill="#3a3a3a"/><text x="124" y="276" text-anchor="middle" font-size="10" fill="#fff">ENTRANCE</text>
  <rect x="44" y="188" width="58" height="42" rx="8" fill="#fff" stroke="#5a8a52"/><text x="73" y="214" text-anchor="middle" font-size="18" font-weight="700">A</text>
  <rect x="150" y="170" width="58" height="42" rx="8" fill="#fff" stroke="#5a8a52"/><text x="179" y="196" text-anchor="middle" font-size="18" font-weight="700">B</text>
  <rect x="44" y="96" width="58" height="42" rx="8" fill="#fff" stroke="#5a8a52"/><text x="73" y="122" text-anchor="middle" font-size="18" font-weight="700">C</text>
  <rect x="150" y="60" width="58" height="42" rx="8" fill="#fff" stroke="#5a8a52"/><text x="179" y="86" text-anchor="middle" font-size="18" font-weight="700">D</text>
  <rect x="244" y="92" width="58" height="42" rx="8" fill="#fff" stroke="#5a8a52"/><text x="273" y="118" text-anchor="middle" font-size="18" font-weight="700">E</text>
  <rect x="300" y="196" width="58" height="42" rx="8" fill="#fff" stroke="#5a8a52"/><text x="329" y="222" text-anchor="middle" font-size="18" font-weight="700">F</text>
</svg>
"""

MAP_OPTIONS = ["A", "B", "C", "D", "E", "F"]


# --------------------------------------------------------------------------- #
#  PRACTICE SETS  (one starter set per type — add more freely)
# --------------------------------------------------------------------------- #
PRACTICE_SETS = {

    # ===================== MULTIPLE CHOICE =============================== #
    "multiple-choice": [
        {
            "id": "mcq-1",
            "title": "Leisure centre announcement",
            "audio": "mcq_1.mp3",
            "instructions": "Questions 1-5. Listen to the announcement and choose the correct answer, A, B or C.",
            "lines": [
                ("NARRATOR", "You will hear the manager of a leisure centre talking to new visitors. Listen and answer questions 1 to 5."),
                ("W2", "Good morning everyone, and welcome to the newly refurbished Parkside Leisure Centre. Let me tell you what's changed."),
                ("W2", "The biggest news is our brand-new facility. Now, we did consider an outdoor pool, and a dance studio, but in the end we built a full climbing wall — it's the first of its kind in the area, and it's already proving very popular."),
                ("W2", "A quick word on prices. Our off-peak membership gives you the best value. It used to be cheapest at weekends, but from this month the lowest rates are on weekday mornings, before midday."),
                ("W2", "If you'd like to use the gym, please note that you can't just walk straight in. Before your first session, every new member has to attend a short induction with one of our trainers — it's free, but it is compulsory."),
                ("W2", "Many of you have asked about the café upstairs. It's no longer members-only, and it isn't closed for refurbishment any more either — I'm pleased to say it's now open to everyone, including the general public."),
                ("W2", "Finally, our fitness classes. You can no longer book these at reception or over the phone — all class bookings now go through our mobile app, which you can download for free. Thank you, and enjoy the centre."),
            ],
            "questions": [
                {"id": "q1", "render": "radio",
                 "text": "What is the main new feature at the centre?",
                 "options": ["A  an outdoor pool", "B  a climbing wall", "C  a dance studio"],
                 "answer": "B  a climbing wall",
                 "explanation": "An outdoor pool and a dance studio are mentioned only as ideas they 'considered'. The feature they actually built is the climbing wall."},
                {"id": "q2", "render": "radio",
                 "text": "Off-peak membership is now cheapest",
                 "options": ["A  on weekday mornings", "B  at weekends", "C  on weekday evenings"],
                 "answer": "A  on weekday mornings",
                 "explanation": "Weekends 'used to be' cheapest — that's the distractor. The lowest rates are now on weekday mornings, before midday."},
                {"id": "q3", "render": "radio",
                 "text": "Before using the gym, new members must",
                 "options": ["A  pay a deposit", "B  attend an induction", "C  bring a doctor's note"],
                 "answer": "B  attend an induction",
                 "explanation": "The induction is described as free but compulsory before a first session. Deposits and doctor's notes aren't mentioned."},
                {"id": "q4", "render": "radio",
                 "text": "The café is now",
                 "options": ["A  closed for refurbishment", "B  open only to members", "C  open to everyone"],
                 "answer": "C  open to everyone",
                 "explanation": "Both 'members-only' and 'closed for refurbishment' are explicitly denied ('no longer', 'isn't'). It is now open to the public."},
                {"id": "q5", "render": "radio",
                 "text": "Fitness classes can now be booked",
                 "options": ["A  at reception", "B  by phone", "C  through the app"],
                 "answer": "C  through the app",
                 "explanation": "Reception and phone booking are ruled out ('no longer'). All bookings now go through the mobile app."},
            ],
        },
    ],

    # ===================== FORM / NOTE / TABLE (GAP-FILL) =============== #
    "gap-fill": [
        {
            "id": "gap-1",
            "title": "Photography workshop booking",
            "audio": "gap_1.mp3",
            "instructions": "Questions 1-5. Complete the booking form. Write ONE WORD AND/OR A NUMBER for each answer.",
            "lines": [
                ("NARRATOR", "You will hear a telephone call between a man and the organiser of a photography workshop. Complete the form, questions 1 to 5."),
                ("W", "Hello, City Photography Club, how can I help?"),
                ("M", "Hi, I'd like to book a place on one of your weekend workshops."),
                ("W", "Of course. We run two — landscape and portrait. Which would you like?"),
                ("M", "The portrait one, please."),
                ("W", "Great, the portrait workshop. And that one runs on Saturday the ninth of March."),
                ("M", "Saturday the ninth, perfect. How much is it?"),
                ("W", "The full day is thirty-five pounds, including lunch."),
                ("M", "Thirty-five pounds, fine. Do I need to bring anything special?"),
                ("W", "We provide the cameras, but please bring your own tripod, as we don't have enough for everyone."),
                ("M", "A tripod, got it. And where do we meet?"),
                ("W", "The building has two entrances. Don't use the main one — we meet at the north entrance, by the car park."),
                ("M", "The north entrance. Brilliant, thank you."),
            ],
            "questions": [
                {"id": "q1", "render": "text",
                 "text": "Type of workshop: ____ photography",
                 "answer": ["portrait"],
                 "explanation": "He chooses the portrait workshop (landscape is the other option offered)."},
                {"id": "q2", "render": "text",
                 "text": "Date: Saturday the ____ of March",
                 "answer": ["9th", "9", "ninth"],
                 "explanation": "The workshop runs on Saturday the ninth (9th) of March."},
                {"id": "q3", "render": "text",
                 "text": "Cost for the full day: £____",
                 "answer": ["35", "35.00", "thirty-five"],
                 "explanation": "The full day costs thirty-five pounds, including lunch."},
                {"id": "q4", "render": "text",
                 "text": "Participants must bring their own ____",
                 "answer": ["tripod"],
                 "explanation": "Cameras are provided, but you must bring your own tripod."},
                {"id": "q5", "render": "text",
                 "text": "Meeting place: the ____ entrance",
                 "answer": ["north"],
                 "explanation": "They meet at the north entrance (not the main one)."},
            ],
        },
    ],

    # ===================== SENTENCE COMPLETION ========================== #
    "sentence": [
        {
            "id": "sentence-1",
            "title": "Lecture: green roofs in cities",
            "audio": "sentence_1.mp3",
            "instructions": "Questions 1-5. Complete the sentences. Write ONE WORD ONLY for each answer.",
            "lines": [
                ("NARRATOR", "You will hear part of a lecture about green roofs — roofs covered with plants. Complete the sentences, questions 1 to 5."),
                ("M2", "Today I want to look at green roofs and the benefits they bring to crowded cities."),
                ("M2", "The first benefit is temperature. Cities tend to be much hotter than the countryside — what we call the urban heat island. By covering rooftops with plants, green roofs help to lower this heat island effect."),
                ("M2", "Secondly, air quality. The leaves act like a natural filter; they trap airborne dust and other particles, so the air around the building becomes cleaner."),
                ("M2", "A third, very practical benefit is drainage. When there's a heavy storm, ordinary roofs send water rushing into the drains all at once. A green roof, by contrast, soaks it up and slows down the flow of rainwater."),
                ("M2", "Now, if green roofs are so good, why aren't they everywhere? The main obstacle for building owners is simply the initial cost — installing one is expensive, even though it saves money later."),
                ("M2", "And the final benefit is wildlife. By creating new habitats for insects and birds, green roofs noticeably increase urban biodiversity."),
            ],
            "questions": [
                {"id": "q1", "render": "text",
                 "text": "Green roofs help to lower the urban ____ island effect.",
                 "answer": ["heat"],
                 "explanation": "The 'urban heat island' makes cities hotter; green roofs lower this heat island effect."},
                {"id": "q2", "render": "text",
                 "text": "The leaves trap airborne ____ and clean the air.",
                 "answer": ["dust", "particles", "pollution"],
                 "explanation": "The leaves act as a filter, trapping airborne dust (and other particles)."},
                {"id": "q3", "render": "text",
                 "text": "During storms, green roofs slow down the flow of ____.",
                 "answer": ["rainwater", "water", "rain"],
                 "explanation": "Instead of water rushing off, a green roof soaks it up and slows the flow of rainwater."},
                {"id": "q4", "render": "text",
                 "text": "The main obstacle for owners is the initial ____.",
                 "answer": ["cost", "price", "expense"],
                 "explanation": "The chief barrier is the initial cost of installation, even though it saves money later."},
                {"id": "q5", "render": "text",
                 "text": "Green roofs create habitats and increase urban ____.",
                 "answer": ["biodiversity", "wildlife"],
                 "explanation": "By creating habitats for insects and birds, green roofs increase urban biodiversity."},
            ],
        },
    ],

    # ===================== MATCHING ===================================== #
    "matching": [
        {
            "id": "matching-1",
            "title": "Sharing out a group report",
            "audio": "matching_1.mp3",
            "instructions": "Questions 1-5. Who will do each part of the report? Choose A, B or C for each part.",
            "lines": [
                ("NARRATOR", "You will hear two students, Tom and Lucy, deciding who will write each part of their group report. Match each part to the correct person, questions 1 to 5."),
                ("M", "Okay Lucy, let's split up the report. There are five parts."),
                ("W", "Sure. I don't mind starting it off, so I'll write the introduction."),
                ("M", "Great, you take the introduction. I'll handle the data collection — I quite enjoy going out and gathering the figures."),
                ("W", "Perfect, data collection is yours. What about designing the survey itself? That's a big job."),
                ("M", "It is — why don't we do the survey design together?"),
                ("W", "Good idea, both of us on the survey design. Now, someone needs to turn the numbers into charts and graphs."),
                ("M", "I'm happy to do the charts and graphs as well, since I'll already have all the data."),
                ("W", "That makes sense, you do the charts. So that leaves the conclusion."),
                ("M", "Could you take the conclusion, Lucy? You're better at summing up than I am."),
                ("W", "Ha, all right — I'll write the conclusion too. That's everything sorted."),
            ],
            "questions": [
                {"id": "q1", "render": "select",
                 "text": "Introduction",
                 "options": ["A  Tom", "B  Lucy", "C  both of them"],
                 "answer": "B  Lucy",
                 "explanation": "Lucy says 'I'll write the introduction.'"},
                {"id": "q2", "render": "select",
                 "text": "Data collection",
                 "options": ["A  Tom", "B  Lucy", "C  both of them"],
                 "answer": "A  Tom",
                 "explanation": "Tom says 'I'll handle the data collection.'"},
                {"id": "q3", "render": "select",
                 "text": "Survey design",
                 "options": ["A  Tom", "B  Lucy", "C  both of them"],
                 "answer": "C  both of them",
                 "explanation": "They agree to do the survey design together — 'both of us'."},
                {"id": "q4", "render": "select",
                 "text": "Charts and graphs",
                 "options": ["A  Tom", "B  Lucy", "C  both of them"],
                 "answer": "A  Tom",
                 "explanation": "Tom takes the charts and graphs as he'll already have the data."},
                {"id": "q5", "render": "select",
                 "text": "Conclusion",
                 "options": ["A  Tom", "B  Lucy", "C  both of them"],
                 "answer": "B  Lucy",
                 "explanation": "Lucy agrees to write the conclusion ('you're better at summing up')."},
            ],
        },
    ],

    # ===================== MAP / PLAN / DIAGRAM ========================= #
    "map": [
        {
            "id": "map-1",
            "title": "Riverside Park orientation",
            "audio": "map_1.mp3",
            "instructions": "Questions 1-5. Label the map of Riverside Park. Choose the correct letter, A-F, for each place.",
            "map_svg": RIVERSIDE_PARK_MAP_SVG,
            "lines": [
                ("NARRATOR", "You will hear a guide describing Riverside Park to a group of visitors. Look at the map and answer questions 1 to 5."),
                ("W2", "Welcome to Riverside Park. We're standing here at the entrance, at the bottom of the map. Let me point a few things out."),
                ("W2", "As you come in, the café is immediately on your left, in the bottom-left corner — that's the building marked A. Do pop in for a coffee later."),
                ("W2", "Straight ahead of you, just a little way up the main path in the middle, you'll see the information point. That's the one marked B — go there if you have any questions."),
                ("W2", "Now, for the toilets, take the left-hand path and keep going up; they're about halfway along on the left, at the building marked C."),
                ("W2", "If you carry on to the very top of the park, in the open central area, there's a large playground for children — that's the area marked E."),
                ("W2", "And finally, over on the right by the river, you can hire rowing boats. The boat hire hut is marked F, right beside the water. Enjoy your visit!"),
            ],
            "questions": [
                {"id": "q1", "render": "select", "text": "Café", "options": MAP_OPTIONS, "answer": "A",
                 "explanation": "The café is 'immediately on your left, in the bottom-left corner' — marked A."},
                {"id": "q2", "render": "select", "text": "Information point", "options": MAP_OPTIONS, "answer": "B",
                 "explanation": "It is 'straight ahead, a little way up the main path in the middle' — marked B."},
                {"id": "q3", "render": "select", "text": "Toilets", "options": MAP_OPTIONS, "answer": "C",
                 "explanation": "Take the left-hand path, 'about halfway along on the left' — marked C."},
                {"id": "q4", "render": "select", "text": "Playground", "options": MAP_OPTIONS, "answer": "E",
                 "explanation": "It's at 'the very top of the park, in the open central area' — marked E."},
                {"id": "q5", "render": "select", "text": "Boat hire", "options": MAP_OPTIONS, "answer": "F",
                 "explanation": "The boat hire hut is 'over on the right by the river' — marked F."},
            ],
        },
    ],

    # ===================== SHORT-ANSWER ================================= #
    "short-answer": [
        {
            "id": "short-1",
            "title": "Museum visitor enquiry",
            "audio": "short_1.mp3",
            "instructions": "Questions 1-5. Answer the questions. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each answer.",
            "lines": [
                ("NARRATOR", "You will hear a man phoning a museum for information. Answer questions 1 to 5."),
                ("W", "Good morning, City Museum, how can I help?"),
                ("M", "Hi, I'm planning a visit. Could I ask a few questions?"),
                ("W", "Of course, go ahead."),
                ("M", "First, how long does the guided tour last?"),
                ("W", "The guided tour lasts ninety minutes — so an hour and a half."),
                ("M", "Ninety minutes, good. Is there anything I can't take inside?"),
                ("W", "Yes — for safety, visitors must leave any large bags at the cloakroom. Coats are fine, just bags."),
                ("M", "Right, leave bags at the cloakroom. Are you open every day?"),
                ("W", "Almost — we're open all week except Monday, when we're closed."),
                ("M", "Closed on Mondays, noted. How much is a family ticket?"),
                ("W", "A family ticket is twenty-five pounds, which covers two adults and up to three children."),
                ("M", "Twenty-five pounds. And is anything free?"),
                ("W", "Yes — on the first Sunday of every month, entry is completely free for all visitors."),
                ("M", "Free entry on the first Sunday. That's really helpful, thank you."),
            ],
            "questions": [
                {"id": "q1", "render": "text",
                 "text": "How long does the guided tour last?",
                 "answer": ["90 minutes", "ninety minutes", "90", "an hour and a half"],
                 "explanation": "The tour lasts ninety minutes (an hour and a half)."},
                {"id": "q2", "render": "text",
                 "text": "What must visitors leave at the cloakroom?",
                 "answer": ["bags", "large bags", "big bags"],
                 "explanation": "Visitors must leave large bags at the cloakroom (coats are allowed)."},
                {"id": "q3", "render": "text",
                 "text": "On which day is the museum closed?",
                 "answer": ["Monday", "Mondays"],
                 "explanation": "The museum is open all week except Monday."},
                {"id": "q4", "render": "text",
                 "text": "How much is a family ticket?",
                 "answer": ["£25", "25 pounds", "25", "twenty-five pounds"],
                 "explanation": "A family ticket costs twenty-five pounds (£25)."},
                {"id": "q5", "render": "text",
                 "text": "What is free on the first Sunday of each month?",
                 "answer": ["entry", "admission", "entrance"],
                 "explanation": "On the first Sunday of each month, entry is free for all visitors."},
            ],
        },
    ],
}


def get_types():
    """Question types annotated with how many practice sets each has."""
    out = []
    for t in QUESTION_TYPES:
        item = dict(t)
        item["set_count"] = len(PRACTICE_SETS.get(t["slug"], []))
        out.append(item)
    return out


def get_set(slug: str, set_id: str | None = None):
    """Return a practice set for a type slug (first set unless set_id given)."""
    sets = PRACTICE_SETS.get(slug) or []
    if not sets:
        return None
    if set_id:
        for s in sets:
            if s["id"] == set_id:
                return s
    return sets[0]
