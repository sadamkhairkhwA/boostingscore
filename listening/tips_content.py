"""Simple IELTS listening tips with examples — shown on each question-type page.

Each type has: a plain-English intro, numbered tips (each with an example),
common mistakes, and a quick “try this” exercise.  GENERAL_TIPS is optional
extra reading at the bottom of the type page.
"""

TYPE_TIPS = {
    "multiple-choice": {
        "name": "Multiple choice",
        "intro": (
            "You hear a short piece of audio and pick the correct answer — usually "
            "A, B or C. The trick is that the right answer is almost never the "
            "exact words you hear; it's a paraphrase."
        ),
        "tips": [
            {
                "title": "Read all the options before the audio starts",
                "body": "Use the pause to read the question and every option. Underline the key idea in each one so you know what you're listening for.",
                "example": "Question: Why did she choose the blue car?\nA  it was cheaper  B  it uses less fuel  C  it looks modern\n→ Listen for the reason she gives, not just the words 'blue car'.",
            },
            {
                "title": "Watch out for speakers changing their mind",
                "body": "A speaker often mentions one option, then rejects it. The correct answer is what they decide in the end.",
                "example": "Audio: 'I was going to take the bus… but actually the train is faster, so I'll get the train.'\n→ Answer is about the train, not the bus.",
            },
            {
                "title": "Don't fall for word-matching traps",
                "body": "Wrong options often repeat words from the recording to trick you. The correct answer usually uses different words with the same meaning.",
                "example": "Audio: 'The course is quite demanding.'\nOption B: 'The course is demanding.' ← sounds right but may be wrong\nOption C: 'The course is challenging.' ← paraphrase = correct",
            },
            {
                "title": "Eliminate wrong answers as you listen",
                "body": "Cross out options that are clearly wrong. This leaves fewer choices and makes the final decision easier.",
                "example": "Audio clearly says 'We don't open on Sundays.'\n→ Cross out any option that says 'open every day including Sunday'.",
            },
        ],
        "mistakes": [
            "Choosing an answer because you heard the same word (not the same meaning).",
            "Answering too quickly before the speaker finishes the point.",
            "Not reading the options during preparation time.",
        ],
        "try_this": "Pick any MCQ practice test. Before you press Begin, read all 5 questions and options and predict what kind of answer each needs.",
    },
    "gap-fill": {
        "name": "Form, note & table completion",
        "intro": (
            "You fill gaps in a form, notes or table with words or numbers from "
            "the recording. Unlike multiple choice, you usually write exactly what "
            "you hear — spelling counts."
        ),
        "tips": [
            {
                "title": "Predict what type of word fits each gap",
                "body": "Before listening, decide if each gap needs a name, number, date, place or noun. This helps your ear catch the right word.",
                "example": "Gap: 'Date of birth: ____'\n→ You expect a date like 14 March or 14/03.",
            },
            {
                "title": "Follow the word limit exactly",
                "body": "If it says ONE WORD AND/OR A NUMBER, never write two words unless the limit allows it. Extra words = wrong answer.",
                "example": "Limit: ONE WORD ONLY. Audio says 'a small garden'.\n→ Write 'garden', not 'small garden'.",
            },
            {
                "title": "Spell carefully — especially names and numbers",
                "body": "Misspelled answers are marked wrong. When someone spells a name aloud, write each letter.",
                "example": "Audio: 'My surname is Clarke — C-L-A-R-K-E.'\n→ Write 'Clarke', not 'Clark'.",
            },
            {
                "title": "Use the headings to stay oriented",
                "body": "Forms and tables have headings that tell you the topic. If you get lost, find the heading that matches what you just heard.",
                "example": "Heading: 'Payment details'\n→ The next gaps are probably about money, not dates or addresses.",
            },
        ],
        "mistakes": [
            "Writing too many words for the gap.",
            "Spelling errors on names and places.",
            "Writing '15' when the speaker said '50' (similar-sounding numbers).",
        ],
        "try_this": "Before each gap-fill test, look at all 5 gaps and write what type of answer you expect (number / name / noun / date).",
    },
    "sentence": {
        "name": "Sentence completion",
        "intro": (
            "You complete a sentence with a word or short phrase from the audio. "
            "The sentence on the paper is usually a paraphrase of what is said, "
            "so you need to understand the meaning, not just match words."
        ),
        "tips": [
            {
                "title": "Read the full sentence — grammar tells you the answer",
                "body": "The missing word must fit grammatically. Is it a noun, verb or adjective? Singular or plural?",
                "example": "The research was carried out over several ____.\n→ Needs a plural noun (e.g. 'months', 'years'). 'Month' would be wrong.",
            },
            {
                "title": "Listen for the idea, write the exact word",
                "body": "The sentence paraphrases the audio, but your answer should be the actual word(s) spoken, within the word limit.",
                "example": "Audio: 'Plants on rooftops reduce the heat island effect.'\nSentence: 'Green roofs help lower the urban ____ island effect.'\n→ Answer: 'heat'",
            },
            {
                "title": "Answers come in order",
                "body": "Question 2 always comes after question 1 in the audio. Use this to know where you are.",
                "example": "If you've answered Q1 and Q2 but missed Q3, don't wait — move on to Q4 when you hear it.",
            },
        ],
        "mistakes": [
            "Writing an answer that fits the meaning but breaks grammar.",
            "Copying a long phrase when only one word is allowed.",
            "Stopping after a missed question and losing the next ones.",
        ],
        "try_this": "Cover the gap in each sentence and guess the part of speech (noun/verb/adjective) before you listen.",
    },
    "matching": {
        "name": "Matching",
        "intro": (
            "You match items (tasks, places, opinions) to a list of people or "
            "options. Common in Section 3 when two or three people discuss "
            "something together."
        ),
        "tips": [
            {
                "title": "Read the options box first",
                "body": "Know the list of people or choices before the audio starts. Then read the items you need to match.",
                "example": "Options: A Tom  B Lucy  C both\nItems: introduction, data collection, conclusion\n→ Now listen for who says 'I'll do the introduction'.",
            },
            {
                "title": "Track who is speaking",
                "body": "In a discussion, write the speaker's initial (T/L) next to each item as you hear it.",
                "example": "Lucy: 'I'll write the introduction.' → Write 'B' next to Introduction immediately.",
            },
            {
                "title": "Options can be used more than once — or not at all",
                "body": "Don't assume each person gets exactly one item unless the instructions say so.",
                "example": "Tom does data collection AND charts. Lucy does introduction AND conclusion. 'Both' does survey design.",
            },
        ],
        "mistakes": [
            "Assuming one option per person.",
            "Confusing which speaker said what in a fast discussion.",
            "Falling behind and trying to remember instead of writing quickly.",
        ],
        "try_this": "On the matching tests, write T, L or B (both) as shorthand while listening, then transfer to the dropdown after.",
    },
    "map": {
        "name": "Map, plan & diagram labelling",
        "intro": (
            "You label places on a map or plan using letters (A, B, C…). A speaker "
            "describes locations and you match each place to the correct letter."
        ),
        "tips": [
            {
                "title": "Find the starting point first",
                "body": "The speaker usually says where you are ('We're at the entrance'). Mark that spot, then follow directions from there.",
                "example": "'We're standing at the entrance at the bottom of the map.' → Put your finger on the entrance before listening further.",
            },
            {
                "title": "Learn direction language",
                "body": "Left, right, straight ahead, opposite, next to, at the end of, on your left — these appear in almost every map task.",
                "example": "'Take the path on your left and the café is the first building you reach.' → First building on the left path.",
            },
            {
                "title": "Move your finger along the map as you listen",
                "body": "Follow the route step by step. Don't jump ahead to label a place until the speaker reaches it.",
                "example": "Speaker: 'Past the toilets… keep going… now on your right is the playground.' → Label playground only when you hear 'playground'.",
            },
        ],
        "mistakes": [
            "Mixing up left and right (it's from the visitor's viewpoint).",
            "Labelling the wrong building when several are close together.",
            "Not finding the entrance first, so all directions are wrong.",
        ],
        "try_this": "Open a map test and trace the path with your finger before pressing Begin, following the entrance → first stop → second stop.",
    },
    "short-answer": {
        "name": "Short-answer questions",
        "intro": (
            "You answer direct questions in a few words or a number. The answer is "
            "usually stated clearly in the audio — listen for facts like times, "
            "prices and names."
        ),
        "tips": [
            {
                "title": "Check the word limit on every question",
                "body": "'NO MORE THAN TWO WORDS AND/OR A NUMBER' means exactly that. Count your words before writing.",
                "example": "Q: What must visitors leave at the cloakroom?\nAudio: 'large bags'\n→ Write 'bags' or 'large bags' (2 words max). Not 'their large bags'.",
            },
            {
                "title": "Question words tell you what to listen for",
                "body": "How much → price. How long → time. When → date/time. Where → place. What → thing.",
                "example": "How long does the tour last?\n→ Listen for a duration: 'ninety minutes', 'an hour and a half'.",
            },
            {
                "title": "Write only the answer — not a full sentence",
                "body": "Short-answer means short. Just the key word(s) or number.",
                "example": "Q: On which day is the museum closed?\nAudio: 'except Monday'\n→ Write 'Monday', not 'The museum is closed on Monday'.",
            },
        ],
        "mistakes": [
            "Writing too many words.",
            "Missing the number or unit (minutes, pounds, kilometres).",
            "Answering with a full sentence instead of the key words.",
        ],
        "try_this": "For each short-answer question, circle the question word (What/How/When) and predict the answer type before listening.",
    },
}

GENERAL_TIPS = [
    "Use every second of preparation time to read ahead — don't wait for the audio.",
    "Answers always come in order; use the questions to track where you are.",
    "If you miss one answer, move on immediately — don't lose the next three.",
    "Listen for signpost words: 'however', 'the main reason', 'finally', 'actually'.",
    "Practise with British English podcasts and news to train your ear.",
    "After each practice test, read the explanations — they show you what to listen for.",
]


def get_type_tips(slug: str) -> dict | None:
    return TYPE_TIPS.get(slug)
