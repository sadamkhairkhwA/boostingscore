"""Text content for the Listening "Tips & how to improve" page.

All text — no audio. Each question type has: how to approach it, common
mistakes, and how to improve. GENERAL_TIPS covers overall listening skill.
Edit freely; the tips page renders whatever is here.
"""

TYPE_TIPS = [
    {
        "slug": "multiple-choice",
        "name": "Multiple choice",
        "intro": "You hear a short stretch of speech and choose the option (usually A, B or C) that matches it. These questions test detailed understanding, not just keyword spotting.",
        "approach": [
            "Use the pause before the section to read the question and all options. Underline the key idea in each.",
            "Listen for meaning, not matching words — the correct option is almost always a paraphrase, while a wrong option often repeats words you hear.",
            "Track the speaker's final decision. Speakers frequently mention an option, then reject or change it ('I was going to… but actually…').",
            "Eliminate as you go. Cross out options that are clearly contradicted so you're choosing between fewer.",
        ],
        "mistakes": [
            "Choosing an option just because you heard the same word in the recording (a 'word-match trap').",
            "Picking the first option that sounds right before the speaker finishes the point.",
            "Not reading the options during the preparation time, then trying to read and listen at once.",
        ],
        "improve": [
            "Practise predicting paraphrases: for each option, ask 'how else could this be said?'",
            "Re-listen to questions you got wrong and find the exact words that signalled the right (and wrong) answers.",
        ],
    },
    {
        "slug": "gap-fill",
        "name": "Form, note & table completion",
        "intro": "You complete a form, set of notes or table with words or numbers from the recording. Common in Section 1 (everyday information) and Section 4 (lectures).",
        "approach": [
            "Read the title and headings first so you know the topic and what kind of information fits each gap.",
            "Predict the answer type before you listen — a name, number, date, time, or noun? This primes your ear.",
            "Check the word limit ('ONE WORD AND/OR A NUMBER', etc.) and never exceed it — over-length answers are marked wrong.",
            "Write exactly what you hear; answers are usually not paraphrased here, unlike multiple choice.",
        ],
        "mistakes": [
            "Going over the word limit (e.g. writing 'a blue car' when only two words are allowed and the answer is 'blue car').",
            "Spelling mistakes — misspelled answers are marked wrong, even if you heard correctly.",
            "Getting numbers, dates and times in the wrong format, or confusing 13/30, 15/50, etc.",
        ],
        "improve": [
            "Drill spelling of letters and numbers — practise writing names spelled aloud and prices/dates at speed.",
            "Learn how British speakers say dates, phone numbers and decimals ('double four', 'oh', 'point five').",
        ],
    },
    {
        "slug": "sentence",
        "name": "Sentence completion",
        "intro": "You fill a gap in a sentence with words from the audio. The sentence is usually a paraphrase of what is said, so meaning matters.",
        "approach": [
            "Read the whole sentence and decide what part of speech the gap needs (noun, verb, adjective).",
            "Use grammar to check your answer fits — singular/plural, verb form and articles must all make sense.",
            "Listen for the idea, then capture the exact word(s) that fill the gap, within the word limit.",
            "Remember answers come in order, so use the questions to keep your place in the recording.",
        ],
        "mistakes": [
            "Writing an answer that fits the meaning but breaks the grammar of the sentence.",
            "Copying a long phrase when only one or two words are required.",
            "Losing your place after a hard question and missing the next one.",
        ],
        "improve": [
            "Practise with transcripts: blank out key words and refill them, checking grammar each time.",
            "Build collocation knowledge ('heavy rain', 'make a decision') so likely answers come to mind faster.",
        ],
    },
    {
        "slug": "matching",
        "name": "Matching",
        "intro": "You match a list of items (e.g. tasks, places, opinions) to a set of options or people. Common in Section 3 discussions.",
        "approach": [
            "Read the options box first and the list of items second; know what you're matching before the audio starts.",
            "Follow who is speaking — with two or three speakers, answers often depend on which person says what.",
            "Options can be used once, more than once, or not at all unless told otherwise — don't assume one each.",
            "Note quick shorthand next to each item as you listen; you can tidy answers afterwards.",
        ],
        "mistakes": [
            "Assuming every option is used exactly once and forcing a wrong match.",
            "Confusing which speaker holds which view in a multi-person discussion.",
            "Falling behind because the speakers move quickly between items.",
        ],
        "improve": [
            "Practise tracking speakers: listen to discussions and note each person's opinion.",
            "Get comfortable with agreement/disagreement language ('I'm not so sure', 'exactly', 'I'd rather').",
        ],
    },
    {
        "slug": "map",
        "name": "Map, plan & diagram labelling",
        "intro": "You label places on a map or plan using letters. Common in Section 2 (e.g. a tour or orientation talk).",
        "approach": [
            "Before listening, find your starting point (often 'the entrance') and orient yourself: left, right, top, bottom.",
            "Learn direction and location language: opposite, next to, behind, beside, at the end of, on your left.",
            "Follow the route the speaker describes — they usually move logically around the map.",
            "Keep your pencil on the current location so you don't lose track when they jump to the next place.",
        ],
        "mistakes": [
            "Losing orientation and mixing up left and right (remember it's from the visitor's point of view).",
            "Jumping ahead and labelling the wrong building when several are close together.",
            "Ignoring the starting point, so every direction afterwards is off.",
        ],
        "improve": [
            "Practise with maps and audio describing routes; pause and predict the next place.",
            "Drill prepositions of place until they're automatic.",
        ],
    },
    {
        "slug": "short-answer",
        "name": "Short-answer questions",
        "intro": "You answer direct questions in a few words or a number. They test specific factual detail.",
        "approach": [
            "Turn each question word (How long? How much? Where? What?) into a prediction of the answer type.",
            "Respect the word limit strictly — 'NO MORE THAN TWO WORDS AND/OR A NUMBER' means exactly that.",
            "Listen for the precise detail; the answer is usually stated directly, not paraphrased.",
            "Don't add extra words like 'the' or 'a' unless they're needed and within the limit.",
        ],
        "mistakes": [
            "Exceeding the word limit and losing an otherwise-correct mark.",
            "Writing a full sentence instead of the key word(s).",
            "Mishearing numbers or missing units (minutes, pounds, kilometres).",
        ],
        "improve": [
            "Practise extracting just the answer from a spoken sentence — say it in two words or fewer.",
            "Train your ear on numbers, measurements and times.",
        ],
    },
]

GENERAL_TIPS = {
    "before": [
        "Use every pause to read ahead and predict answers — preparation time is part of the test.",
        "Read instructions and word limits carefully; they change between sections.",
        "Underline keywords in questions so you know what to listen for.",
    ],
    "during": [
        "The recording plays once — if you miss an answer, let it go and focus on the next question. Don't freeze.",
        "Answers come in order, so the questions act as a map through the audio.",
        "Listen for signpost words ('however', 'finally', 'the main reason') that flag important information.",
        "Beware of distractors: speakers often correct themselves or reject an option they first mention.",
        "Write answers as you hear them; don't rely on memory until the section ends.",
    ],
    "after": [
        "On paper-based tests you get 10 minutes to transfer answers — copy carefully and check spelling.",
        "Never leave a blank: a sensible guess can still be correct, and there's no penalty for wrong answers.",
        "Check grammar and word limits as you review.",
    ],
    "longterm": [
        "Listen to British and other English accents daily — podcasts, news, lectures, documentaries.",
        "Practise active listening: pause, summarise what you heard, then continue.",
        "Use transcripts after listening to catch the words you missed and learn new phrases.",
        "Build vocabulary by topic (education, environment, health) — familiar topics are far easier to follow.",
        "Do full timed sections regularly so the once-only pace feels normal on exam day.",
    ],
}
