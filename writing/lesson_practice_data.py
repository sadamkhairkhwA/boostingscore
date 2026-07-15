"""Fixed practice tasks for each Writing lesson (one per lesson)."""

TRANSPORT_BAR_CHART = """Task 1 prompt:
The chart below shows the percentage of households in one country that used selected forms of transport to travel to work in 2005 and 2015.

Chart data (percentages of households):
• Car: 67% (2005) → 71% (2015)
• Public transport: 24% → 31%
• Bicycle: 8% → 15%
• Walking: 18% → 12%
• Motorcycle: 5% → 3%"""

ENERGY_LINE_GRAPH = """Task 1 prompt:
The line graph below shows energy consumption in millions of tonnes of oil equivalent across four sectors in a country between 1990 and 2010.

Chart data (million tonnes oil equivalent):
• Industry: 62 (1990) → 58 (2000) → 49 (2010)
• Transport: 38 → 50 → 61
• Residential: 44 → 41 → 37
• Services: 18 → 24 → 29"""

ENERGY_SOURCES_PIE = """Task 1 prompt:
The pie charts below show the proportion of energy generated from different sources in a country in 1990 and 2010.

1990: Coal 52%, Oil 28%, Gas 12%, Nuclear 5%, Renewables 3%
2010: Coal 38%, Oil 22%, Gas 18%, Nuclear 12%, Renewables 10%"""

UNIVERSITY_TABLE = """Task 1 prompt:
The table below shows the percentage of male and female students enrolled in four university subject areas in a country in 2018.

• Engineering: Male 78%, Female 22%
• Education: Male 25%, Female 75%
• Business: Male 55%, Female 45%
• Arts: Male 35%, Female 65%"""

WATER_PROCESS = """Task 1 prompt:
The diagram below shows how drinking water is produced and distributed in a town.

Process stages:
1. Raw water is taken from a river.
2. Water is filtered through sand and gravel.
3. Chemicals are added to kill bacteria.
4. Clean water is stored in large tanks.
5. Water is pumped through underground pipes to homes and businesses."""

TOWN_MAP = """Task 1 prompt:
The maps below show changes to a town centre between 1990 and 2020.

1990: A large market square in the centre; a library north of the square; farmland to the east; a single main road running north–south through the centre.

2020: The market square replaced by a shopping mall; the library converted into a community centre; farmland developed into a housing estate; a new bypass road built to the west of the centre; a bus station added south of the mall."""

ONLINE_EDUCATION_T2 = """Task 2 prompt:
Some people think online learning is better than classroom learning for university students. To what extent do you agree or disagree?"""

LESSON_PRACTICE = {
    "t1-structure": {
        "skill_focus": "Task 1 four-paragraph structure planning",
        "instruction": (
            "Read the chart description below. Write a brief plan with exactly four short sentences — "
            "one for each paragraph (introduction, overview, body 1, body 2). "
            "Do not write full paragraphs; state what each paragraph will cover."
        ),
        "prompt_context": TRANSPORT_BAR_CHART,
        "min_words": 20,
        "max_words_hint": "About 40–60 words",
    },
    "t1-intro": {
        "skill_focus": "Task 1 introduction — paraphrasing the prompt",
        "instruction": (
            "Using the chart description below, write only the introduction paragraph "
            "(1–2 sentences). Paraphrase the task — do not include data, opinions, or an overview."
        ),
        "prompt_context": TRANSPORT_BAR_CHART,
        "min_words": 15,
        "max_words_hint": "About 25–40 words",
    },
    "t1-overview": {
        "skill_focus": "Task 1 overview — identifying main trends without detail",
        "instruction": (
            "Using the same chart, write only the overview paragraph (2–3 sentences). "
            "Summarise the biggest trends and changes. Avoid listing every figure."
        ),
        "prompt_context": TRANSPORT_BAR_CHART,
        "min_words": 20,
        "max_words_hint": "About 35–55 words",
    },
    "t1-body": {
        "skill_focus": "Task 1 body paragraph — grouped comparisons with data",
        "instruction": (
            "Using the same chart, write one body paragraph only. "
            "Group related categories, compare them, and support your points with specific figures."
        ),
        "prompt_context": TRANSPORT_BAR_CHART,
        "min_words": 40,
        "max_words_hint": "About 50–80 words",
    },
    "t1-qtypes": {
        "skill_focus": "Bar and line graph language — trends over time",
        "instruction": (
            "Using the line graph below, write one body paragraph describing how energy use "
            "changed in two sectors between 1990 and 2010. Use accurate trend vocabulary and figures."
        ),
        "prompt_context": ENERGY_LINE_GRAPH,
        "min_words": 40,
        "max_words_hint": "About 50–80 words",
    },
    "t1-pie-table": {
        "skill_focus": "Pie charts and tables — proportions and key contrasts",
        "instruction": (
            "Using the table below, write one paragraph highlighting the most significant "
            "gender differences across the four subjects. Select key data — do not list every cell."
        ),
        "prompt_context": UNIVERSITY_TABLE,
        "min_words": 35,
        "max_words_hint": "About 45–70 words",
    },
    "t1-process": {
        "skill_focus": "Process diagram — sequencing and passive voice",
        "instruction": (
            "Using the process below, write 3–4 sentences describing stages 2 to 4 only "
            "(filtering through to storage). Use sequencing words and passive structures where appropriate."
        ),
        "prompt_context": WATER_PROCESS,
        "min_words": 35,
        "max_words_hint": "About 45–70 words",
    },
    "t1-map": {
        "skill_focus": "Map description — location language and major changes",
        "instruction": (
            "Using the maps below, write one paragraph describing the three most significant "
            "changes to the town centre between 1990 and 2020. Use clear location phrases."
        ),
        "prompt_context": TOWN_MAP,
        "min_words": 40,
        "max_words_hint": "About 50–80 words",
    },
    "t2-structure": {
        "skill_focus": "Task 2 essay structure — thesis and paragraph roles",
        "instruction": (
            "Read the Task 2 question below. Write a brief essay plan: one thesis sentence "
            "stating your position, then one sentence each for body paragraph 1 and body paragraph 2 "
            "(what each paragraph will argue). Do not write full paragraphs."
        ),
        "prompt_context": ONLINE_EDUCATION_T2,
        "min_words": 25,
        "max_words_hint": "About 40–60 words",
    },
    "t2-intro": {
        "skill_focus": "Task 2 introduction — paraphrase plus clear thesis",
        "instruction": (
            "Write only the introduction (2–3 sentences) for the question below. "
            "Paraphrase the task and state your position clearly in a thesis sentence."
        ),
        "prompt_context": ONLINE_EDUCATION_T2,
        "min_words": 25,
        "max_words_hint": "About 40–55 words",
    },
    "t2-teel": {
        "skill_focus": "Task 2 body paragraph — TEEL structure",
        "instruction": (
            "For the question below, write one body paragraph only using TEEL "
            "(topic sentence, explanation, example, link). Argue one clear reason supporting your position."
        ),
        "prompt_context": ONLINE_EDUCATION_T2,
        "min_words": 50,
        "max_words_hint": "About 70–100 words",
    },
    "t2-conclusion": {
        "skill_focus": "Task 2 conclusion — summarise and restate position",
        "instruction": (
            "Assume you have argued that online learning is beneficial for university students. "
            "Write only the conclusion (2–3 sentences) for the question below. "
            "Summarise your view and do not introduce new arguments."
        ),
        "prompt_context": ONLINE_EDUCATION_T2,
        "min_words": 25,
        "max_words_hint": "About 35–50 words",
    },
}


def get_lesson_practice(lesson_id):
    return LESSON_PRACTICE.get(lesson_id)
