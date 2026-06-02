"""Scripts + question bank for the IELTS Listening test.

The `script` field for each section is sent to OpenAI TTS to produce one
continuous audio file. The `questions` are graded server-side after submit
(spelling matters in gap-fill, just like real IELTS).
"""

# IELTS-style opening narration so the generated audio feels official.
OPENING_NARRATION = (
    "Welcome to the IELTS practice listening test. "
    "You will hear four recordings. Listen carefully and answer the questions "
    "for each section as you listen. The recording will play once only."
)

# Brief verbal pause between sections; TTS renders these as actual pauses.
SECTION_BREAK = (
    "End of section. You now have a short time to check your answers. "
    "We will now begin the next section."
)


LISTENING_TEST = {
    "voice": "alloy",  # OpenAI TTS voice
    "sections": [
        # ===================== SECTION 1 =====================
        {
            "number": 1,
            "title": "Section 1 — Enquiring about sports membership",
            "script": (
                "Section 1. You will hear a phone conversation between a customer "
                "and a receptionist at the Greenfield Community Sports Centre. "
                "First you have some time to look at questions 1 to 10.\n\n"
                "Receptionist: Good morning, Greenfield Community Sports Centre, "
                "Marina speaking. How can I help you?\n"
                "Caller: Hi, I'm interested in joining the gym. Could you tell me "
                "about the membership options?\n"
                "Receptionist: Of course. We have three main plans. Our Standard "
                "membership is forty pounds per month and gives you full gym "
                "access. The Plus membership is fifty-five pounds per month and "
                "also includes group classes. And the Family membership covers up "
                "to four people for ninety pounds per month.\n"
                "Caller: Great. The Plus membership sounds good. Can I see the "
                "list of group classes?\n"
                "Receptionist: Certainly. We offer yoga on Mondays at six pm, "
                "spin class on Wednesdays at seven thirty, and pilates on "
                "Saturdays at ten am. All classes are sixty minutes long.\n"
                "Caller: Thanks. And what are the opening hours?\n"
                "Receptionist: The gym is open from six am to ten pm on weekdays, "
                "and from eight am to eight pm on weekends.\n"
                "Caller: Perfect. To sign up, what do I need to bring?\n"
                "Receptionist: You'll need photo identification, proof of your "
                "current address, and a bank card for the monthly payment. "
                "There's also a one-off joining fee of twenty-five pounds.\n"
                "Caller: Okay. My name is Daniel Park, that's P-A-R-K. My phone "
                "number is zero seven, double-four, five, two, eight, one, "
                "nine, three, six.\n"
                "Receptionist: Thank you, Daniel. We'll see you on Saturday."
            ),
            "questions": [
                {"type": "gap", "id": "l1q1", "text": "Standard membership costs £____ per month.", "answer": "40"},
                {"type": "gap", "id": "l1q2", "text": "Plus membership costs £____ per month.", "answer": "55"},
                {"type": "gap", "id": "l1q3", "text": "Family membership covers up to ____ people.", "answer": "four"},
                {"type": "mcq", "id": "l1q4", "text": "Which class is on Monday evenings?",
                 "options": ["Yoga", "Spin", "Pilates", "Boxing"], "answer": "Yoga"},
                {"type": "gap", "id": "l1q5", "text": "Spin class starts at ____ pm on Wednesdays.", "answer": "7:30"},
                {"type": "gap", "id": "l1q6", "text": "Each class lasts ____ minutes.", "answer": "60"},
                {"type": "gap", "id": "l1q7", "text": "Weekday opening hours are 6am – ____ pm.", "answer": "10"},
                {"type": "short", "id": "l1q8", "text": "Name TWO documents required to sign up.",
                 "answer_keywords": ["photo identification", "proof of address", "bank card", "id", "address"]},
                {"type": "gap", "id": "l1q9", "text": "There is a one-off joining fee of £____.", "answer": "25"},
                {"type": "gap", "id": "l1q10", "text": "Caller's surname is spelled P-A-R-____.", "answer": "K"},
            ],
        },
        # ===================== SECTION 2 =====================
        {
            "number": 2,
            "title": "Section 2 — Guided tour of a botanical garden",
            "script": (
                "Section 2. You will hear a tour guide welcoming visitors to the "
                "Eastfield Botanical Garden. First you have some time to look at "
                "questions 11 to 20.\n\n"
                "Good morning everyone, and welcome to Eastfield Botanical Garden. "
                "My name is Sophie and I'll be your guide for the next hour. "
                "Before we start, just a few practical points. The whole garden "
                "covers eighteen hectares, so we won't see all of it today, but "
                "the highlights are well worth your visit.\n\n"
                "Our walk begins at the Rose Garden, which contains over three "
                "hundred varieties of roses, many of them rare. From there we'll "
                "move to the Tropical House, where the temperature is kept at a "
                "constant twenty-eight degrees Celsius year-round to support "
                "plants from the Amazon.\n\n"
                "The next stop is the Bamboo Grove. Please walk on the marked "
                "wooden path only — the soil is very soft and easily damaged.\n\n"
                "We finish at the Lakeside Café. Lunch is included for tour "
                "members, and today's menu features mushroom soup, grilled "
                "vegetables and a fruit tart for dessert.\n\n"
                "A few reminders: photography is welcome, but please do not use "
                "a flash inside the Tropical House. Touching the plants is not "
                "permitted at any time, and please keep your voices low in the "
                "Bamboo Grove — it's a quiet zone for visiting wildlife.\n\n"
                "If you need the toilets, they are next to the main entrance. "
                "The gift shop is open until five pm and offers a ten percent "
                "discount to tour members."
            ),
            "questions": [
                {"type": "gap", "id": "l2q1", "text": "The garden covers ____ hectares.", "answer": "18"},
                {"type": "gap", "id": "l2q2", "text": "The Rose Garden has more than ____ varieties of roses.", "answer": "300"},
                {"type": "gap", "id": "l2q3", "text": "The Tropical House is kept at ____ degrees Celsius.", "answer": "28"},
                {"type": "mcq", "id": "l2q4", "text": "Why must visitors stay on the path in the Bamboo Grove?",
                 "options": ["It is too dark", "The soil damages easily", "It is private property", "The path is shorter"],
                 "answer": "The soil damages easily"},
                {"type": "short", "id": "l2q5", "text": "Where does the tour finish?",
                 "answer_keywords": ["lakeside café", "lakeside cafe", "café", "cafe"]},
                {"type": "gap", "id": "l2q6", "text": "Lunch starts with mushroom ____.", "answer": "soup"},
                {"type": "mcq", "id": "l2q7", "text": "Which dessert is served?",
                 "options": ["Chocolate cake", "Fruit tart", "Ice cream", "Cheesecake"],
                 "answer": "Fruit tart"},
                {"type": "mcq", "id": "l2q8", "text": "Inside the Tropical House visitors must NOT:",
                 "options": ["take photos", "use flash", "speak", "take notes"],
                 "answer": "use flash"},
                {"type": "gap", "id": "l2q9", "text": "Toilets are next to the ____ entrance.", "answer": "main"},
                {"type": "gap", "id": "l2q10", "text": "Tour members get a ____ percent discount in the gift shop.", "answer": "10"},
            ],
        },
        # ===================== SECTION 3 =====================
        {
            "number": 3,
            "title": "Section 3 — Discussion about a research project",
            "script": (
                "Section 3. You will hear two students, Hannah and Omar, "
                "discussing their research project with their tutor, Dr Reid. "
                "First you have some time to look at questions 21 to 30.\n\n"
                "Dr Reid: So, where are you with your project on urban green spaces?\n"
                "Hannah: We've completed the literature review and started "
                "designing the survey. We're planning to interview around fifty "
                "residents in three different neighbourhoods.\n"
                "Omar: Right. But we're having trouble deciding how to recruit "
                "participants. We thought about putting flyers in cafés, but "
                "Hannah thinks that might bias the sample.\n"
                "Hannah: Yes — café visitors aren't representative of the whole "
                "community. I'd prefer to use door-to-door visits.\n"
                "Dr Reid: Door-to-door is more representative but very time "
                "consuming. Have you considered using social media?\n"
                "Omar: We discussed that, but we worried we'd only reach younger "
                "people.\n"
                "Dr Reid: A good point. I'd suggest combining two methods — "
                "social media plus a few well-placed flyers in community "
                "centres, which tend to attract a wider age group.\n"
                "Hannah: That makes sense. We could also offer a small reward "
                "like a five-pound voucher.\n"
                "Dr Reid: That works, but make sure you mention it in your "
                "ethics application. By the way, when's the application due?\n"
                "Omar: We have to submit it by the fifteenth of next month, "
                "with results of the survey by mid-July.\n"
                "Dr Reid: Plenty of time. Now, what about the data analysis?\n"
                "Hannah: We'll use simple descriptive statistics — averages and "
                "percentages — plus a few quotes from the interviews to add "
                "depth.\n"
                "Dr Reid: Good. Just remember to anonymise all quotes."
            ),
            "questions": [
                {"type": "mcq", "id": "l3q1", "text": "The project focuses on:",
                 "options": ["café culture", "urban green spaces", "social media use", "community centres"],
                 "answer": "urban green spaces"},
                {"type": "gap", "id": "l3q2", "text": "They plan to interview around ____ residents.", "answer": "50"},
                {"type": "gap", "id": "l3q3", "text": "They will survey people in ____ neighbourhoods.", "answer": "three"},
                {"type": "mcq", "id": "l3q4", "text": "Why does Hannah object to recruiting in cafés?",
                 "options": ["too expensive", "biased sample", "no permission", "café owners refused"],
                 "answer": "biased sample"},
                {"type": "mcq", "id": "l3q5", "text": "Why is social media alone a poor recruitment method?",
                 "options": ["too slow", "only reaches younger people", "blocked at university", "needs payment"],
                 "answer": "only reaches younger people"},
                {"type": "short", "id": "l3q6", "text": "Where does Dr Reid suggest placing flyers?",
                 "answer_keywords": ["community centres", "community centers", "community centre", "community center"]},
                {"type": "gap", "id": "l3q7", "text": "They will offer a £____ voucher as a small reward.", "answer": "5"},
                {"type": "gap", "id": "l3q8", "text": "The ethics application is due on the ____ of next month.", "answer": "15"},
                {"type": "short", "id": "l3q9", "text": "What kind of statistics will they use?",
                 "answer_keywords": ["descriptive", "averages", "percentages"]},
                {"type": "short", "id": "l3q10", "text": "Dr Reid reminds them to do what with the quotes?",
                 "answer_keywords": ["anonymise", "anonymize", "anonymous"]},
            ],
        },
        # ===================== SECTION 4 =====================
        {
            "number": 4,
            "title": "Section 4 — Lecture on habit formation",
            "script": (
                "Section 4. You will hear a short lecture on the science of "
                "habit formation. First you have some time to look at questions "
                "31 to 40.\n\n"
                "Good afternoon. Today's lecture is about how habits are formed "
                "in the brain, and why some habits are so much harder to break "
                "than others.\n\n"
                "Researchers describe a habit as a loop with three parts. First "
                "there is a cue, which is the trigger that tells your brain to "
                "start a behaviour. Second is the routine itself — the "
                "behaviour you carry out. And third is the reward, which tells "
                "your brain that the loop is worth remembering for next time.\n\n"
                "A famous experiment in the nineteen nineties tracked the "
                "behaviour of taxi drivers in London. Researchers found that "
                "drivers had unusually well-developed hippocampi — the part of "
                "the brain involved in memory and navigation — after just two "
                "years of driving the city. This showed that adult brains can "
                "be reshaped by repeated behaviour.\n\n"
                "Modern studies suggest that, on average, it takes about sixty-"
                "six days for a new behaviour to become automatic. Simple "
                "habits like drinking a glass of water in the morning may "
                "become automatic within just twenty days, while more complex "
                "ones such as a regular exercise routine can take over two "
                "hundred days.\n\n"
                "To change a bad habit, researchers recommend keeping the cue "
                "and the reward, but replacing the routine. For example, if "
                "boredom is the cue and pleasure is the reward, a student who "
                "wants to stop scrolling on their phone could replace that "
                "routine with reading a chapter of a book.\n\n"
                "One final tip: small wins matter. People who celebrate even "
                "tiny progress are about three times more likely to stick with "
                "a new habit than those who wait for big results."
            ),
            "questions": [
                {"type": "gap", "id": "l4q1", "text": "A habit loop has ____ parts.", "answer": "three"},
                {"type": "short", "id": "l4q2", "text": "What is the first part of the habit loop called?",
                 "answer_keywords": ["cue", "trigger"]},
                {"type": "short", "id": "l4q3", "text": "What is the third part of the habit loop?",
                 "answer_keywords": ["reward"]},
                {"type": "mcq", "id": "l4q4", "text": "London taxi drivers were studied because their:",
                 "options": ["English was unusual", "hippocampi were unusually well-developed", "income was high", "shifts were short"],
                 "answer": "hippocampi were unusually well-developed"},
                {"type": "gap", "id": "l4q5", "text": "Effects were seen after just ____ years of driving.", "answer": "two"},
                {"type": "gap", "id": "l4q6", "text": "Modern studies suggest new habits become automatic after about ____ days on average.", "answer": "66"},
                {"type": "gap", "id": "l4q7", "text": "A simple morning habit may become automatic in just ____ days.", "answer": "20"},
                {"type": "gap", "id": "l4q8", "text": "Complex habits can take over ____ days.", "answer": "200"},
                {"type": "mcq", "id": "l4q9", "text": "To change a bad habit, you should replace the:",
                 "options": ["cue", "routine", "reward", "trigger"],
                 "answer": "routine"},
                {"type": "gap", "id": "l4q10", "text": "People who celebrate small wins are about ____ times more likely to stick with new habits.", "answer": "three"},
            ],
        },
    ],
}


def total_questions() -> int:
    return sum(len(s["questions"]) for s in LISTENING_TEST["sections"])
