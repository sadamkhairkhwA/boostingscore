"""Writing — common grammar mistakes checklist (data-driven)."""

GRAMMAR_MISTAKES = [
    {
        "id": "articles",
        "title": "Article misuse (a / an / the)",
        "summary": "Missing articles before singular countable nouns, or using the when meaning is general.",
        "wrong": "Government should invest in public transport.",
        "correct": "The government should invest in public transport.",
        "tip": "Use the when referring to a specific government, study, or trend already in context.",
    },
    {
        "id": "subject-verb",
        "title": "Subject–verb agreement",
        "summary": "The verb must agree with the true subject, not a nearby noun.",
        "wrong": "The number of cars have increased sharply.",
        "correct": "The number of cars has increased sharply.",
        "tip": "The subject is number (singular), not cars.",
    },
    {
        "id": "run-on",
        "title": "Run-on sentences & comma splices",
        "summary": "Two independent clauses joined only by a comma.",
        "wrong": "Many people work remotely, they save commuting time.",
        "correct": "Many people work remotely, so they save commuting time.",
        "tip": "Use a conjunction, semicolon, or split into two sentences.",
    },
    {
        "id": "prepositions",
        "title": "Wrong prepositions",
        "summary": "Fixed phrases in English — learn collocations, not word-by-word translation.",
        "wrong": "This leads in pollution in cities.",
        "correct": "This leads to pollution in cities.",
        "tip": "lead to · depend on · responsible for · result in",
    },
    {
        "id": "tense-mix",
        "title": "Tense mixing",
        "summary": "Shifting tenses without a clear time reason confuses the reader.",
        "wrong": "The chart shows that sales rose and prices are falling last year.",
        "correct": "The chart shows that sales rose and prices fell last year.",
        "tip": "Match time markers (last year, currently, by 2030) to consistent tenses.",
    },
    {
        "id": "plural",
        "title": "Countable / uncountable nouns",
        "summary": "Using plural forms where English uses uncountable nouns.",
        "wrong": "There are many informations about the topic.",
        "correct": "There is a lot of information about the topic.",
        "tip": "information · research · evidence · advice — no plural -s in formal writing.",
    },
    {
        "id": "word-form",
        "title": "Word form errors",
        "summary": "Using adjective/adverb/noun forms interchangeably.",
        "wrong": "Technology develops quick in modern societies.",
        "correct": "Technology develops quickly in modern societies.",
        "tip": "Check whether the gap needs an adverb (-ly) to modify a verb.",
    },
]

SELF_CHECK_ITEMS = [
    "Every sentence has a clear subject and verb.",
    "Articles (a/an/the) are correct before countable nouns.",
    "I used one main tense per time period unless the meaning requires a shift.",
    "Prepositions match common collocations (lead to, depend on, etc.).",
    "No comma splices — two full sentences are not joined by a comma alone.",
    "Task 2 has four paragraphs: introduction, two body paragraphs, conclusion.",
    "I paraphrased the question in the introduction — I did not copy it word for word.",
    "I left two minutes to check spelling and word forms.",
]
