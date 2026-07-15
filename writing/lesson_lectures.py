"""Structured Learn-step lectures for each Writing lesson.

Highlight markup: wrap key phrases in <span class="wl-hl">...</span>
"""

LESSON_LECTURES = {
    "t1-structure": {
        "band_7_focus": (
            "Use a four-paragraph structure: paraphrased introduction, overview of key trends, "
            "and two body paragraphs with grouped comparisons and precise data."
        ),
        "what_this_is": (
            "Task 1 is a short report, not an essay. The four-paragraph formula gives examiners a "
            "clear path through your answer: what the visual shows, the main picture, then selected detail. "
            "This directly affects Task Achievement (covering requirements) and Coherence & Cohesion "
            "(logical organisation)."
        ),
        "method_steps": [
            "Read the prompt and identify chart type, subject, place, and time period.",
            "Plan one sentence per paragraph role: intro (paraphrase only), overview (big picture), body 1 and body 2 (grouped detail).",
            "Write the introduction and overview before any figures in the body.",
            "Split body paragraphs by category or time — never list every number in order.",
            "Leave 2–3 minutes to check tense, units, and that the overview is easy to find.",
        ],
        "worked_example": {
            "prompt": (
                "The chart below shows the percentage of households in one country that used selected "
                "forms of transport to travel to work in 2005 and 2015."
            ),
            "example_html": (
                "<strong>Paragraph plan (not full essay):</strong><br>"
                "1. Intro — <span class=\"wl-hl\">The bar chart illustrates the proportion of households "
                "using five modes of transport for commuting</span> in a single country "
                "<span class=\"wl-hl\">across two years</span> (2005 and 2015).<br>"
                "2. Overview — <span class=\"wl-hl\">Car use remained dominant while walking and motorcycle "
                "use declined</span>; public transport and cycling grew.<br>"
                "3. Body 1 — Compare motorised modes (car vs public transport vs motorcycle).<br>"
                "4. Body 2 — Compare active travel (cycling vs walking) and link to the downward walking trend."
            ),
            "swaps": [
                {"before": "shows", "after": "illustrates"},
                {"before": "percentage of households", "after": "proportion of households"},
                {"before": "travel to work", "after": "commuting"},
            ],
            "walkthrough": (
                "Each line states a paragraph job before writing prose. The intro paraphrases without data; "
                "the overview names trends only; bodies are grouped by theme. Examiners can locate the overview "
                "immediately — a Band 7+ requirement."
            ),
        },
        "band_compare": {
            "weak": {
                "text": "One long paragraph describing every bar in order from left to right with all percentages.",
                "note": "No overview and no grouping — Task Achievement stays low even if numbers are correct.",
            },
            "strong": {
                "text": "Four short paragraphs: paraphrase → two-sentence overview → body grouped by transport type → body on changes over time.",
                "note": "Clear roles make the report scannable; comparisons are easier to follow.",
            },
        },
        "common_mistakes": [
            {"mistake": "Writing one block of data with no overview.", "fix": "Add a standalone overview after the introduction — examiners look for it explicitly."},
            {"mistake": "Putting specific figures in the overview.", "fix": "State trends only; save numbers for body paragraphs."},
            {"mistake": "Using opinion language (e.g. “fortunately”, “worryingly”).", "fix": "Stay neutral — Task 1 is descriptive, not argumentative."},
            {"mistake": "A conclusion paragraph at the end.", "fix": "Stop after two body paragraphs; a conclusion is unnecessary and wastes words."},
        ],
    },
    "t1-intro": {
        "band_7_focus": (
            "Paraphrase the question with accurate vocabulary, keep it concise, and avoid opinions "
            "or extra details in Task 1 introductions."
        ),
        "what_this_is": (
            "The introduction tells the reader what the visual is about — nothing more. It should "
            "paraphrase the task prompt in one or two sentences. Examiners use it to judge Task Achievement "
            "(have you understood the task?) and Lexical Resource (can you rephrase without copying?)."
        ),
        "method_steps": [
            "Read the prompt and identify chart type, subject, place, and time period.",
            "Swap key words for accurate synonyms (e.g. shows → illustrates, proportion → percentage).",
            "Change the sentence structure — do not mirror the question word for word.",
            "Do not add data, opinions, or an overview — that belongs in later paragraphs.",
            "Stop at 25–40 words; longer introductions waste time and word count.",
        ],
        "worked_example": {
            "prompt": (
                "The chart below shows the percentage of households in one country that used selected "
                "forms of transport to travel to work in 2005 and 2015."
            ),
            "example_html": (
                "<span class=\"wl-hl\">The bar chart illustrates the proportion of households in one country "
                "that commuted by various means of transport</span> "
                "<span class=\"wl-hl\">in 2005 and 2015</span>."
            ),
            "swaps": [
                {"before": "shows", "after": "illustrates"},
                {"before": "the percentage of", "after": "the proportion of"},
                {"before": "travel to work", "after": "commuted"},
                {"before": "selected forms of transport", "after": "various means of transport"},
            ],
            "walkthrough": (
                "Every element of the question appears in new wording, but no figures are introduced. "
                "The time frame and chart type are explicit, so the reader knows what follows."
            ),
        },
        "band_compare": {
            "weak": {
                "text": "The chart below shows the percentage of households in one country that used selected forms of transport to travel to work in 2005 and 2015.",
                "note": "Copied from the rubric — shows limited paraphrase skill.",
            },
            "strong": {
                "text": "The bar chart compares how households in one country travelled to work, as a percentage, in 2005 and 2015.",
                "note": "Same information, new structure and vocabulary — Band 7+ lexical control.",
            },
        },
        "common_mistakes": [
            {"mistake": "Copying the question with one word changed.", "fix": "Change both vocabulary and grammar (e.g. active → passive, clause order)."},
            {"mistake": "Including the overview or data in sentence one.", "fix": "Introduce the topic only; trends and numbers come later."},
            {"mistake": "Wrong chart type (calling a line graph a bar chart).", "fix": "Name the visual accurately — examiners notice mismatches."},
            {"mistake": "Adding “In this essay I will…”.", "fix": "Task 1 is a report, not an essay — drop meta-commentary."},
        ],
    },
    "t1-overview": {
        "band_7_focus": (
            "Your overview should identify the biggest trends, highest/lowest values, or notable "
            "changes without too many numbers."
        ),
        "what_this_is": (
            "The overview is the most important paragraph in Task 1. It answers: “What is the big picture?” "
            "Examiners must find a clear overview to award Band 7+ for Task Achievement. It is not a list of "
            "every figure — it is a summary of what matters most."
        ),
        "method_steps": [
            "Scan the visual for the largest trend, biggest gap, or clearest change over time.",
            "Write 2–3 sentences stating those patterns without precise data (or at most one anchor figure).",
            "Place the overview after the introduction — many candidates use the second paragraph.",
            "Use general language: “the majority”, “a noticeable rise”, “the only category to fall”.",
            "Check that someone reading only your overview would grasp the main message of the chart.",
        ],
        "worked_example": {
            "prompt": (
                "Transport to work bar chart: Car 67%→71%; public transport 24%→31%; bicycle 8%→15%; "
                "walking 18%→12%; motorcycle 5%→3% (2005 vs 2015)."
            ),
            "example_html": (
                "<span class=\"wl-hl\">Overall, car travel remained the most common option throughout the period</span>, "
                "while <span class=\"wl-hl\">walking and motorcycle use both declined</span>. "
                "<span class=\"wl-hl\">Public transport and cycling became more popular</span>, with cycling "
                "showing the sharper proportional increase."
            ),
            "swaps": [
                {"before": "car use was highest", "after": "car travel remained the most common option"},
                {"before": "walking went down", "after": "walking … declined"},
            ],
            "walkthrough": (
                "Three trends, no exact percentages. “Remained the most common” covers dominance; paired declines "
                "and rises show the examiner you compared categories, not just described one bar."
            ),
        },
        "band_compare": {
            "weak": {
                "text": "Car was 67% then 71%, public transport was 24% then 31%, bicycle was 8% then 15%…",
                "note": "A data list, not a summary — overview criterion not met.",
            },
            "strong": {
                "text": "Cars dominated throughout, while active travel lost share and public modes gained ground.",
                "note": "General trends without a spreadsheet — clear Band 7+ overview.",
            },
        },
        "common_mistakes": [
            {"mistake": "No overview at all.", "fix": "Always include one — it is the fastest way to gain a full band point."},
            {"mistake": "Burying the overview in the last paragraph.", "fix": "Put it early (usually paragraph 2) so examiners see it immediately."},
            {"mistake": "Only describing one category.", "fix": "Cover at least two major patterns or comparisons."},
            {"mistake": "Using “In conclusion”.", "fix": "Overviews are not conclusions — avoid essay language."},
        ],
    },
    "t1-body": {
        "band_7_focus": (
            "Group related data points and compare them directly. Use figures to support every key statement."
        ),
        "what_this_is": (
            "Body paragraphs carry the selected detail that supports your overview. Each paragraph should "
            "group related categories or time periods and compare them with accurate figures. This shapes "
            "Task Achievement (relevant detail) and Coherence (one clear focus per paragraph)."
        ),
        "method_steps": [
            "Decide how to split data — by category, by time, or by highest vs lowest.",
            "Open with a topic sentence that states the paragraph focus (e.g. motorised transport).",
            "Support each claim with a figure; compare two items in the same sentence where possible.",
            "Use comparison language: “higher than”, “while”, “in contrast”, “roughly double”.",
            "Stop when the paragraph is developed — do not repeat the overview or add new main trends.",
        ],
        "worked_example": {
            "prompt": "Same transport chart — write body 1 on motorised modes only.",
            "example_html": (
                "<span class=\"wl-hl\">Regarding motorised travel, car use rose modestly from 67% to 71%</span>, "
                "remaining well above all other options. "
                "<span class=\"wl-hl\">Public transport increased more sharply, from 24% to 31%</span>, "
                "whereas <span class=\"wl-hl\">motorcycle commuting almost halved, falling to just 3%</span>."
            ),
            "swaps": [
                {"before": "went up a little", "after": "rose modestly"},
                {"before": "was much bigger than", "after": "remained well above"},
            ],
            "walkthrough": (
                "The topic is motorised modes only. Each clause has a number and a comparison. "
                "“Whereas” links public transport growth to motorcycle decline in one logical unit."
            ),
        },
        "band_compare": {
            "weak": {
                "text": "Car 67, 71. Bus 24, 31. Bike 8, 15. Walk 18, 12. Moto 5, 3.",
                "note": "Numbers without grouping or comparison verbs — reads like notes.",
            },
            "strong": {
                "text": "Car use climbed slightly to 71%, while public transport grew by seven percentage points, narrowing the gap between the two.",
                "note": "Selected figures with explicit comparison — controlled and readable.",
            },
        },
        "common_mistakes": [
            {"mistake": "Listing every value in the chart.", "fix": "Select key figures that support your overview — omit minor noise."},
            {"mistake": "Mixing unrelated categories in one sentence.", "fix": "One paragraph theme; compare items that belong together."},
            {"mistake": "No units or wrong tense.", "fix": "Match the visual (percentages, years) and use past tense for past data."},
            {"mistake": "Repeating the overview verbatim.", "fix": "Bodies add evidence; do not copy overview sentences."},
        ],
    },
    "t1-qtypes": {
        "band_7_focus": (
            "Focus on trend verbs, proportional comparison language, and period-by-period changes."
        ),
        "what_this_is": (
            "Bar charts and line graphs usually show change over time or differences between categories. "
            "Examiners expect precise trend vocabulary (rose, peaked, levelled off) and time phrases "
            "(between 2000 and 2010, over the decade). This affects Lexical Resource and Task Achievement."
        ),
        "method_steps": [
            "Identify whether the main story is change over time (line) or comparison at points (bar).",
            "Note start and end values, any peak/trough, and periods of stability or rapid change.",
            "Use varied trend verbs — avoid repeating “increased” five times.",
            "For line graphs, describe the shape (steady climb, sharp dip, plateau).",
            "Compare endpoints and mention the most dramatic period with figures.",
        ],
        "worked_example": {
            "prompt": (
                "Line graph: energy use in Transport — 38 (1990), 50 (2000), 61 (2010); "
                "Industry — 62, 58, 49 over the same years."
            ),
            "example_html": (
                "<span class=\"wl-hl\">Transport consumption climbed steadily across the period</span>, "
                "from 38 million tonnes to 61, <span class=\"wl-hl\">making it the fastest-growing sector by 2010</span>. "
                "By contrast, <span class=\"wl-hl\">industrial use trended downward</span>, "
                "falling from 62 to 49 million tonnes."
            ),
            "swaps": [
                {"before": "went up constantly", "after": "climbed steadily"},
                {"before": "went down", "after": "trended downward"},
            ],
            "walkthrough": (
                "Trend verbs match the lines’ shapes. Start and end figures anchor the description; "
                "a cross-sector comparison (“fastest-growing”) adds Band 7+ depth."
            ),
        },
        "band_compare": {
            "weak": {
                "text": "Transport went up and industry went down from 1990 to 2010.",
                "note": "Vague — no figures, weak trend language, no sense of pace.",
            },
            "strong": {
                "text": "Transport rose steadily to 61 million tonnes, overtaking industry, whose consumption slipped to 49 by 2010.",
                "note": "Precise verbs, endpoints, and a meaningful comparison.",
            },
        },
        "common_mistakes": [
            {"mistake": "Describing every small fluctuation on a busy line.", "fix": "Prioritise start, end, and the most notable movement."},
            {"mistake": "Using present tense for past years.", "fix": "Past data → past tense (rose, fell), unless the chart says “projected”."},
            {"mistake": "Same verb repeated (increased × 6).", "fix": "Use a range: grew, surged, edged up, plateaued, dipped."},
            {"mistake": "Ignoring the time axis on bar charts.", "fix": "When bars show years, describe change over time, not static comparison only."},
        ],
    },
    "t1-pie-table": {
        "band_7_focus": (
            "Prioritise dominant segments and significant contrasts. Avoid listing all numbers mechanically."
        ),
        "what_this_is": (
            "Pie charts and tables show proportions or structured comparisons. The skill is selection: "
            "which slices or cells matter most, and how they contrast. Examiners reward proportion language "
            "(the majority, a minority, accounted for) and clear contrasts, not full transcription."
        ),
        "method_steps": [
            "Find the largest and smallest shares, or the biggest gender/regional gap in a table.",
            "Use proportion phrases before giving one or two anchor percentages.",
            "In tables, compare rows or columns — do not read the grid cell by cell.",
            "Highlight doubles, halves, or gaps of more than 20 percentage points.",
            "Link back to your overview — bodies should prove what you summarised.",
        ],
        "worked_example": {
            "prompt": (
                "Table: university enrolment by gender — Engineering M 78% / F 22%; "
                "Education M 25% / F 75%; Business M 55% / F 45%; Arts M 35% / F 65%."
            ),
            "example_html": (
                "<span class=\"wl-hl\">Engineering was heavily male-dominated</span>, with men accounting for "
                "78% of students, <span class=\"wl-hl\">whereas education showed the reverse pattern</span>, "
                "as women made up three quarters of enrolments. "
                "Business and arts sat between these extremes, though <span class=\"wl-hl\">arts still had "
                "twice as many female as male students</span>."
            ),
            "swaps": [
                {"before": "most students were men", "after": "heavily male-dominated"},
                {"before": "the opposite", "after": "the reverse pattern"},
            ],
            "walkthrough": (
                "Extremes first (engineering vs education), then middle categories with one precise comparison. "
                "Not every cell is quoted — the reader still understands the full table."
            ),
        },
        "band_compare": {
            "weak": {
                "text": "Engineering 78 male, 22 female. Education 25 male, 75 female. Business 55, 45. Arts 35, 65.",
                "note": "Reads the table aloud — no interpretation.",
            },
            "strong": {
                "text": "The starkest divide was in engineering and education, which mirror each other by gender; business was almost balanced.",
                "note": "Selects contrasts and uses academic proportion language.",
            },
        },
        "common_mistakes": [
            {"mistake": "Quoting every cell in a large table.", "fix": "Report patterns and extremes; skip redundant similar rows."},
            {"mistake": "Saying “52%” without context on pie charts.", "fix": "State what the slice represents (e.g. “just over half of energy from coal”)."},
            {"mistake": "Comparing pies without referencing both years.", "fix": "When two pies exist, focus on what changed between dates."},
            {"mistake": "Forgetting units (percent vs absolute numbers).", "fix": "Check headers — tables often mix percentages and counts."},
        ],
    },
    "t1-process": {
        "band_7_focus": (
            "Use sequencing words and passive structures where the actor is unknown or unimportant."
        ),
        "what_this_is": (
            "A process diagram shows stages in order — natural, man-made, or cyclical. "
            "Your job is to describe each stage logically, often with passive voice because the focus "
            "is the material, not who performs the action. Task Achievement and Grammatical Range are key."
        ),
        "method_steps": [
            "Find the start and end of the process; note whether it is linear or cyclical.",
            "Write one sentence (or two short ones) per main stage in chronological order.",
            "Use sequencers: first, then, next, after that, finally; for cycles use “the process begins again”.",
            "Prefer passive when the doer is obvious or unknown: “water is filtered”, “bottles are sealed”.",
            "Include an overview sentence stating the number of stages or the overall purpose.",
        ],
        "worked_example": {
            "prompt": "Drinking water production: river intake → sand filtration → chemical treatment → storage → distribution.",
            "example_html": (
                "<span class=\"wl-hl\">Initially, raw water is extracted from a river</span> and "
                "<span class=\"wl-hl\">passed through layers of sand and gravel to remove impurities</span>. "
                "<span class=\"wl-hl\">Next, chemicals are added to disinfect the supply</span>, after which "
                "the clean water <span class=\"wl-hl\">is stored in large tanks before being pumped</span> "
                "through pipes to homes and businesses."
            ),
            "swaps": [
                {"before": "people take water from", "after": "raw water is extracted from"},
                {"before": "they add chemicals", "after": "chemicals are added"},
            ],
            "walkthrough": (
                "Passive verbs keep focus on the water. Sequencers mark order without numbering every box. "
                "Four stages covered in three sentences — efficient and clear."
            ),
        },
        "band_compare": {
            "weak": {
                "text": "First workers get water. Then they filter it. Then chemicals. Then tanks. Then pipes.",
                "note": "Choppy, active voice only, sounds like instructions for staff.",
            },
            "strong": {
                "text": "Having been drawn from the river, the water is filtered, treated chemically, stored, and finally distributed via an underground network.",
                "note": "Linked passive clauses show grammatical range and flow.",
            },
        },
        "common_mistakes": [
            {"mistake": "Random stage order.", "fix": "Follow the arrow direction — order errors hurt Task Achievement."},
            {"mistake": "Only present simple active (“people pour”).", "fix": "Mix passive and participle clauses for Band 7 grammar."},
            {"mistake": "No overview of the whole process.", "fix": "Add one sentence on total stages or purpose in the intro or overview."},
            {"mistake": "Inventing stages not in the diagram.", "fix": "Describe only what is shown — do not guess missing steps."},
        ],
    },
    "t1-map": {
        "band_7_focus": (
            "Highlight major transformations and preserve clear spatial references with location phrases."
        ),
        "what_this_is": (
            "Map tasks show how a place changed between two dates. Examiners look for location language "
            "(north of, to the east, replaced by) and a focus on significant developments, not every building. "
            "Task Achievement and Lexical Resource (spatial vocabulary) matter most."
        ),
        "method_steps": [
            "Compare both maps and list what appeared, disappeared, or changed function.",
            "Select the three or four biggest changes — ignore minor footpaths unless they are central.",
            "Use location phrases: “in the north-east”, “to the west of the centre”, “formerly”.",
            "Group changes: new transport, land-use change, facilities replaced.",
            "Write an overview naming the general direction of change (more urban, more residential, etc.).",
        ],
        "worked_example": {
            "prompt": "Town centre 1990 vs 2020: market square → shopping mall; library → community centre; farmland east → housing; new bypass west; bus station south of mall.",
            "example_html": (
                "<span class=\"wl-hl\">The town centre became considerably more commercial</span>, as "
                "<span class=\"wl-hl\">the central market square was replaced by a large shopping mall</span>. "
                "<span class=\"wl-hl\">To the east, former farmland was converted into a housing estate</span>, "
                "while <span class=\"wl-hl\">a new bypass was constructed along the western edge</span>, "
                "with a bus station added immediately south of the mall."
            ),
            "swaps": [
                {"before": "the square became a mall", "after": "the market square was replaced by a shopping mall"},
                {"before": "houses were built on the farm", "after": "farmland was converted into a housing estate"},
            ],
            "walkthrough": (
                "Each change has a location anchor. Passive forms suit map tasks. The opening sentence gives "
                "a general overview before detail."
            ),
        },
        "band_compare": {
            "weak": {
                "text": "There is a mall now. There are houses. There is a road. The library changed.",
                "note": "No positions — reader cannot picture the map.",
            },
            "strong": {
                "text": "East of the centre, agricultural land gave way to housing, while the core itself shifted from an open square to a covered retail complex.",
                "note": "Spatial language plus summary of the type of change.",
            },
        },
        "common_mistakes": [
            {"mistake": "Describing only one map.", "fix": "Always compare — “was replaced by”, “a new X was added”."},
            {"mistake": "No compass / position language.", "fix": "Use north, south, adjacent to, in the centre — examiners expect it."},
            {"mistake": "Listing every tiny path or tree.", "fix": "Major infrastructure and land-use shifts are enough."},
            {"mistake": "Present tense for past maps.", "fix": "Use past for the older map and “was built / was converted” for changes."},
        ],
    },
    "t2-structure": {
        "band_7_focus": (
            "Present a clear thesis, build one central idea per body paragraph, and end with a concise conclusion."
        ),
        "what_this_is": (
            "Task 2 is a formal opinion essay with a predictable shape: introduction with thesis, two developed "
            "body paragraphs, and a short conclusion. Structure carries Task Response (clear position throughout) "
            "and Coherence & Cohesion (one main idea per paragraph, logical progression)."
        ),
        "method_steps": [
            "Analyse the question type: opinion, discussion, problem/solution, advantages, or double question.",
            "Write a one-sentence thesis stating your position or main answer.",
            "Plan body 1 and body 2 — each gets one reason or view, not two mixed ideas.",
            "Ensure every paragraph links back to the thesis with a topic sentence and a link sentence.",
            "Conclude by restating your position — no new arguments in the final paragraph.",
        ],
        "worked_example": {
            "prompt": "Some people think online learning is better than classroom learning for university students. To what extent do you agree or disagree?",
            "example_html": (
                "<strong>Plan (four blocks):</strong><br>"
                "Intro — <span class=\"wl-hl\">Paraphrase + thesis: largely agree that online learning benefits "
                "university students when combined with some face-to-face contact</span>.<br>"
                "Body 1 — <span class=\"wl-hl\">Flexibility and access for diverse learners</span>.<br>"
                "Body 2 — <span class=\"wl-hl\">Acknowledge classroom value, but argue online tools improve revision "
                "and self-paced depth</span>.<br>"
                "Conclusion — <span class=\"wl-hl\">Restate balanced agreement; online should complement, not replace, "
                "campus teaching</span>."
            ),
            "swaps": [
                {"before": "I think online is better", "after": "largely agree that online learning benefits university students"},
            ],
            "walkthrough": (
                "The thesis is specific (not 100% one-sided unless you choose that). Each body has one job; "
                "the plan can be written in under two minutes before drafting."
            ),
        },
        "band_compare": {
            "weak": {
                "text": "Introduction, three ideas in one paragraph, no clear conclusion.",
                "note": "Ideas compete — examiner cannot track your position.",
            },
            "strong": {
                "text": "Thesis in intro → body on flexibility → body on depth of learning → two-sentence conclusion restating view.",
                "note": "One idea per block; position is visible throughout.",
            },
        },
        "common_mistakes": [
            {"mistake": "No clear thesis in the introduction.", "fix": "Answer the question directly in one sentence — examiners look in the first paragraph."},
            {"mistake": "Two different ideas in one body paragraph.", "fix": "Split them — paragraph unity is a Band 7 coherence requirement."},
            {"mistake": "Ignoring part of the question (e.g. only causes, no solutions).", "fix": "Underline every task word before planning."},
            {"mistake": "A very long conclusion with new examples.", "fix": "Conclusions summarise; new ideas belong in the body."},
        ],
    },
    "t2-intro": {
        "band_7_focus": (
            "Paraphrase the task and state your position directly in one clear thesis sentence."
        ),
        "what_this_is": (
            "The Task 2 introduction sets up your entire essay. You paraphrase the question to show vocabulary "
            "range, then give a thesis that answers it. Task Response is judged from here — a vague or missing "
            "position limits your band regardless of later paragraphs."
        ),
        "method_steps": [
            "Paraphrase the statement in 1–2 sentences — change word forms and structure, not just synonyms.",
            "State your position clearly: agree, disagree, partly agree, or which view you favour.",
            "Match the question type — discussion essays need “both views” signalled even before the body.",
            "Keep to 40–55 words; do not preview every argument in detail.",
            "Avoid “In this essay I will discuss” — show the position instead of announcing it.",
        ],
        "worked_example": {
            "prompt": "Some people think online learning is better than classroom learning for university students. To what extent do you agree or disagree?",
            "example_html": (
                "<span class=\"wl-hl\">It is argued that university courses delivered online can be more effective "
                "than traditional face-to-face classes</span>. "
                "<span class=\"wl-hl\">I largely agree with this view</span>, as digital platforms offer flexibility "
                "and richer revision tools, <span class=\"wl-hl\">although some subjects still require physical attendance</span>."
            ),
            "swaps": [
                {"before": "Some people think", "after": "It is argued that"},
                {"before": "online learning is better", "after": "courses delivered online can be more effective"},
                {"before": "classroom learning", "after": "traditional face-to-face classes"},
            ],
            "walkthrough": (
                "Paraphrase + thesis + brief hedge in one tight unit. The examiner knows your position before body 1."
            ),
        },
        "band_compare": {
            "weak": {
                "text": "Some people think online learning is better. I will discuss both sides in this essay.",
                "note": "Copied prompt and no real thesis — Task Response capped.",
            },
            "strong": {
                "text": "While campus contact remains valuable, I believe online delivery better serves most university learners because of flexibility and self-paced review.",
                "note": "Clear, defensible position with a hint of nuance.",
            },
        },
        "common_mistakes": [
            {"mistake": "Thesis that does not answer the exact question.", "fix": "Mirror task words — “to what extent” needs agree/disagree language."},
            {"mistake": "Only background about education, no position.", "fix": "Cut general statements; state your view by sentence three at latest."},
            {"mistake": "Extreme position without support planned.", "fix": "If you write “completely agree”, both bodies must strongly support it."},
            {"mistake": "Over-long introductions (80+ words).", "fix": "Save development for bodies — intros should be lean."},
        ],
    },
    "t2-teel": {
        "band_7_focus": (
            "Use a strong topic sentence, then explain, support with examples, and link back to the thesis."
        ),
        "what_this_is": (
            "TEEL (Topic, Explain, Example, Link) is the standard body paragraph frame for Task 2. "
            "Each paragraph proves one reason that supports your thesis. Examiners reward fully developed "
            "ideas (Task Response) and clear internal paragraph structure (Coherence)."
        ),
        "method_steps": [
            "Topic sentence — state the paragraph’s one main idea in plain language.",
            "Explain — say why this idea matters (1–2 sentences of reasoning).",
            "Example — give a specific case, country, or scenario (not “for example, many people”).",
            "Link — tie the paragraph back to your thesis or the question wording.",
            "Read the paragraph alone — if the topic sentence is true, the rest should prove it.",
        ],
        "worked_example": {
            "prompt": "Same online education question — one body paragraph arguing flexibility.",
            "example_html": (
                "<span class=\"wl-hl\">Firstly, online programmes give students greater control over when and "
                "where they study</span>. "
                "This flexibility matters because many undergraduates work part-time or care for family members, "
                "so rigid timetables can limit attendance. "
                "<span class=\"wl-hl\">For instance, recorded lectures allow a nursing student on night shifts "
                "to review materials in the morning</span>, which would be difficult in a fixed classroom schedule. "
                "<span class=\"wl-hl\">Therefore, digital delivery can widen access without lowering academic standards</span>."
            ),
            "swaps": [
                {"before": "Online is convenient", "after": "online programmes give students greater control"},
                {"before": "For example", "after": "For instance"},
            ],
            "walkthrough": (
                "T = flexibility; E = why it matters; E.g. = concrete student case; L = connects to thesis "
                "(access and standards). No second main idea intrudes."
            ),
        },
        "band_compare": {
            "weak": {
                "text": "Online learning is good. It is flexible. Students like it. Technology is important nowadays.",
                "note": "Assertions without development — Band 5–6 Task Response.",
            },
            "strong": {
                "text": "Topic + reason + specific example + link — four sentences, one idea, fully supported.",
                "note": "Each sentence adds a new layer; nothing is repeated emptyly.",
            },
        },
        "common_mistakes": [
            {"mistake": "Topic sentence that is too broad (“Technology is useful”).", "fix": "Narrow to one arguable claim tied to the question."},
            {"mistake": "Example that is only “many people” or “everyone”.", "fix": "Name a realistic scenario — a job, a subject, a country."},
            {"mistake": "Missing link sentence — paragraph feels disconnected.", "fix": "End by referring back to your thesis words."},
            {"mistake": "Two ideas (e.g. flexibility and cost) in one paragraph.", "fix": "Split into two TEEL paragraphs."},
        ],
    },
    "t2-conclusion": {
        "band_7_focus": (
            "Summarise your key points briefly and restate your opinion without introducing new arguments."
        ),
        "what_this_is": (
            "The conclusion closes the essay by reminding the reader of your position and main reasons. "
            "It should be short — often two or three sentences. New ideas here hurt Task Response; "
            "a clear restatement supports coherence and leaves a controlled final impression."
        ),
        "method_steps": [
            "Signal closure with “In conclusion” or “To sum up” — one phrase only.",
            "Restate your thesis in different words from the introduction.",
            "Optionally mention your two body themes in one compressed phrase each.",
            "Do not add new statistics, examples, or a third main argument.",
            "Keep to 35–50 words — examiners penalise rambling endings.",
        ],
        "worked_example": {
            "prompt": "Conclusion for: largely agree online learning benefits university students (flexibility + revision tools).",
            "example_html": (
                "<span class=\"wl-hl\">In conclusion, although face-to-face teaching remains valuable for some disciplines</span>, "
                "<span class=\"wl-hl\">I believe online platforms better meet the needs of most university students</span> "
                "by offering flexible schedules and powerful tools for independent review. "
                "<span class=\"wl-hl\">Schools should therefore integrate digital learning rather than resist it</span>."
            ),
            "swaps": [
                {"before": "I think online is good", "after": "online platforms better meet the needs of most university students"},
            ],
            "walkthrough": (
                "Brief concession, restated thesis, practical implication without a new body argument. "
                "Vocabulary differs from the intro while the position stays consistent."
            ),
        },
        "band_compare": {
            "weak": {
                "text": "In conclusion, online learning is a big topic with many advantages and disadvantages that society must consider in the future.",
                "note": "Generic filler — no clear restated position.",
            },
            "strong": {
                "text": "In conclusion, the flexibility and self-paced review that online study provides outweigh its limitations for most undergraduates, so universities should adopt a blended model.",
                "note": "Summarises reasons and restates view in fresh wording.",
            },
        },
        "common_mistakes": [
            {"mistake": "Introducing a brand-new argument.", "fix": "If you think of it late, leave it out — conclusions only summarise."},
            {"mistake": "Copy-pasting the introduction.", "fix": "Same position, different words and slightly wider view."},
            {"mistake": "Apologising or changing your thesis.", "fix": "Stay consistent — switching position confuses the reader."},
            {"mistake": "Over-long conclusion (80+ words).", "fix": "Two or three sentences are enough for Band 7+."},
        ],
    },
}


def get_lesson_lecture(lesson_id):
    return LESSON_LECTURES.get(lesson_id)
