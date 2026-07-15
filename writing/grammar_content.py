"""IELTS Writing grammar topics — study/reference content (no AI)."""

GRAMMAR_TOPICS: list[dict] = [
    {
        "id": "sentence-types",
        "icon": "structure",
        "title": "Sentence types",
        "subtitle": "Short and longer sentences",
        "rule": {
            "paragraphs": [
                "A short sentence has one idea: <em>The number of visitors rose sharply.</em>",
                "You can join ideas with because, although or which: "
                "<em>Although prices increased, demand remained stable.</em>",
            ],
            "key_point_label": "Key point",
            "key_point": (
                "Try to use because, although or which in each paragraph. "
                "This helps your grammar score."
            ),
        },
        "pairs": [
            {
                "wrong": "Sales increased. Demand was high. Prices went up.",
                "correct_html": (
                    "Sales increased <span class=\"wg-hl\">because</span> demand was high, "
                    "<span class=\"wg-hl\">which</span> pushed prices up."
                ),
                "fix": "Join the ideas with because and which.",
            },
            {
                "wrong": "The chart shows an increase. It is in urban areas.",
                "correct_html": (
                    "The chart shows <span class=\"wg-hl\">that</span> urban areas experienced "
                    "the largest increase."
                ),
                "fix": "Use one sentence with that instead of two short ones.",
            },
            {
                "wrong": "Many people work from home and they save time and they are happier.",
                "correct_html": (
                    "Many people work from home, <span class=\"wg-hl\">which</span> saves time "
                    "and improves wellbeing."
                ),
                "fix": "Too many ands — use which for the extra detail.",
            },
            {
                "wrong": "Pollution is serious. Governments should act.",
                "correct_html": (
                    "<span class=\"wg-hl\">Because</span> pollution is serious, governments should act."
                ),
                "fix": "Start with because to show the link between the ideas.",
            },
        ],
        "ielts_mistakes": [
            {
                "mistake": "Every sentence is very short. You list facts with full stops.",
                "fix": "Join ideas with although, while, which or because.",
            },
            {
                "mistake": "One sentence has many and and and parts.",
                "fix": "Split it into two sentences, or use which or because.",
            },
            {
                "mistake": "Two full sentences joined with only a comma.",
                "fix": "Use a full stop, or join with because or although.",
            },
            {
                "mistake": "The long sentence is hard to follow.",
                "fix": "Keep the main idea clear. Put extra detail after which or because.",
            },
        ],
    },
    {
        "id": "subject-verb-agreement",
        "icon": "check",
        "title": "Subject–verb agreement",
        "subtitle": "Match the verb to the subject",
        "rule": {
            "paragraphs": [
                "The verb must match the main subject — not a nearby word. "
                "<em>The number of cars has increased</em> (not have).",
                "Each and everyone take one verb: <em>Each student needs</em> more practice.",
            ],
            "key_point_label": "Key point",
            "key_point": (
                "After the number of, use a singular verb: "
                "The number of tourists has risen."
            ),
        },
        "pairs": [
            {
                "wrong": "The number of tourists have doubled since 2010.",
                "correct_html": "The number of tourists <span class=\"wg-hl\">has</span> doubled since 2010.",
                "fix": "The subject is number (singular), not tourists.",
            },
            {
                "wrong": "Each of the categories show a decline.",
                "correct_html": "Each of the categories <span class=\"wg-hl\">shows</span> a decline.",
                "fix": "Each takes a singular verb — shows, not show.",
            },
            {
                "wrong": "The data indicate that spending are rising.",
                "correct_html": (
                    "The data <span class=\"wg-hl\">indicate</span> that spending "
                    "<span class=\"wg-hl\">is</span> rising."
                ),
                "fix": "Data is plural. Spending is singular.",
            },
            {
                "wrong": "One of the main reason is cost.",
                "correct_html": "One of the main reason<span class=\"wg-hl\">s is</span> cost.",
                "fix": "One of the + plural noun + singular verb.",
            },
        ],
        "ielts_mistakes": [
            {
                "mistake": "You match the verb to the nearest noun, not the real subject.",
                "fix": "Find the main subject first — especially after the number of.",
            },
            {
                "mistake": "You add -s to uncountable words (informations, researchs).",
                "fix": "Say information and research — with a singular verb.",
            },
            {
                "mistake": "Everyone need instead of everyone needs.",
                "fix": "Everyone, each and nobody take a singular verb.",
            },
            {
                "mistake": "The verb is far from the subject and sounds wrong.",
                "fix": "Read the sentence aloud. If it sounds wrong, check the subject.",
            },
        ],
    },
    {
        "id": "articles",
        "icon": "book",
        "title": "Articles",
        "subtitle": "A, an, the and no article",
        "rule": {
            "paragraphs": [
                "Use a or an for one thing: <em>a significant increase</em>. "
                "Use the when you mean one specific thing: <em>the chart shows…</em>",
                "Often use no article with general ideas: <em>Education is important.</em> "
                "In Task 1, say <em>the bar chart illustrates…</em>",
            ],
            "key_point_label": "Key point",
            "key_point": (
                "Task 1: the chart, the table, the map. "
                "Task 2 general topics: no the before education or pollution."
            ),
        },
        "pairs": [
            {
                "wrong": "Chart shows consumption of the oil in 2020.",
                "correct_html": (
                    "<span class=\"wg-hl\">The</span> chart shows consumption of "
                    "<span class=\"wg-hl\">oil</span> in 2020."
                ),
                "fix": "Say the chart. Oil has no the.",
            },
            {
                "wrong": "Education is important for the society.",
                "correct_html": "Education is important for <span class=\"wg-hl\">society</span>.",
                "fix": "General ideas like society often have no the.",
            },
            {
                "wrong": "There was increase in the unemployment.",
                "correct_html": "There was <span class=\"wg-hl\">an</span> increase in <span class=\"wg-hl\">unemployment</span>.",
                "fix": "Say an increase. Unemployment has no the.",
            },
            {
                "wrong": "A Internet has changed communication.",
                "correct_html": "<span class=\"wg-hl\">The</span> Internet has changed communication.",
                "fix": "We always say the Internet.",
            },
        ],
        "ielts_mistakes": [
            {
                "mistake": "You forget the in Task 1: Bar chart shows…",
                "fix": "Say The line graph, The table, or The map.",
            },
            {
                "mistake": "You add the before general words: the education, the pollution.",
                "fix": "Drop the when you talk about ideas in general.",
            },
            {
                "mistake": "You use a before uncountable words: a research, a traffic.",
                "fix": "Say research shows or traffic increased instead.",
            },
            {
                "mistake": "Wrong a or an: a hour, an university.",
                "fix": "Listen to the sound: an hour, a university.",
            },
        ],
    },
    {
        "id": "verb-tenses",
        "icon": "pen",
        "title": "Verb tenses for writing",
        "subtitle": "Which tense to use",
        "rule": {
            "paragraphs": [
                "Use past for a finished time: <em>In 1990, sales stood at 40%.</em> "
                "Use has/have + past participle for change up to now: "
                "<em>Sales have risen since 2010.</em>",
                "Use present simple to describe the chart: "
                "<em>The graph shows that exports grew.</em>",
            ],
            "key_point_label": "Key point",
            "key_point": (
                "In 2015 → past tense. Since 2010 → has risen. "
                "Do not mix them in one sentence without a reason."
            ),
        },
        "pairs": [
            {
                "wrong": "In 2015, sales have reached 50 million.",
                "correct_html": "In 2015, sales <span class=\"wg-hl\">reached</span> 50 million.",
                "fix": "In 2015 is finished — use past tense.",
            },
            {
                "wrong": "The figure shows that production declined since 2010.",
                "correct_html": (
                    "The figure shows that production <span class=\"wg-hl\">has declined</span> since 2010."
                ),
                "fix": "Since 2010 → has + past participle.",
            },
            {
                "wrong": "Nowadays, people worked from home more often.",
                "correct_html": "Nowadays, people <span class=\"wg-hl\">work</span> from home more often.",
                "fix": "Nowadays means now — use present tense.",
            },
            {
                "wrong": "By 2030, the population was 10 million.",
                "correct_html": "By 2030, the population <span class=\"wg-hl\">is expected to reach</span> 10 million.",
                "fix": "By 2030 is in the future — use will or is expected to.",
            },
        ],
        "ielts_mistakes": [
            {
                "mistake": "You use has + past participle with a finished year: In 2005, has increased.",
                "fix": "Use past tense when the year is finished.",
            },
            {
                "mistake": "You switch between past and present in one Task 1 paragraph.",
                "fix": "Pick one time for the data. Use present only to describe the chart.",
            },
            {
                "mistake": "You use will for every prediction in Task 2.",
                "fix": "Also try may, might, is likely to, or could.",
            },
            {
                "mistake": "You miss ongoing trends: Sales rose in 2010 and 2011 and 2012…",
                "fix": "Say Sales were rising or Sales have been increasing.",
            },
        ],
    },
    {
        "id": "passive-voice",
        "icon": "refresh",
        "title": "The passive voice",
        "subtitle": "For process diagrams in Task 1",
        "rule": {
            "paragraphs": [
                "Passive means the thing receives the action. "
                "You do not always say who did it: <em>Water is heated.</em>",
                "Process diagrams use passive for each step: "
                "<em>The beans are crushed and roasted.</em>",
            ],
            "key_point_label": "Key point",
            "key_point": (
                "In process Task 1, describe each step with is or are + past participle."
            ),
        },
        "pairs": [
            {
                "wrong": "Workers crush the beans and then they roast them.",
                "correct_html": (
                    "The beans <span class=\"wg-hl\">are crushed</span> and then "
                    "<span class=\"wg-hl\">roasted</span>."
                ),
                "fix": "Describe the step, not the workers.",
            },
            {
                "wrong": "The government was implement new policies.",
                "correct_html": "The government <span class=\"wg-hl\">implemented</span> new policies.",
                "fix": "When you name who did it, active is fine.",
            },
            {
                "wrong": "Plastic is recycle in the final stage.",
                "correct_html": "Plastic <span class=\"wg-hl\">is recycled</span> in the final stage.",
                "fix": "Passive needs the -ed form: is recycled.",
            },
            {
                "wrong": "It can be see that exports grew.",
                "correct_html": "It can be <span class=\"wg-hl\">seen</span> that exports grew.",
                "fix": "After can be, use seen — not see.",
            },
        ],
        "ielts_mistakes": [
            {
                "mistake": "Process diagrams use active voice: people pour, machines cut.",
                "fix": "Rewrite each step as is/are + past participle.",
            },
            {
                "mistake": "Wrong -ed forms: was build, is showed.",
                "fix": "Learn common forms: built, shown, seen.",
            },
            {
                "mistake": "You forget be: The material heated.",
                "fix": "Always include is, are, was or were.",
            },
            {
                "mistake": "Too much passive in Task 2: It is believed that it is argued that…",
                "fix": "Say what you think directly. Use passive only sometimes.",
            },
        ],
    },
    {
        "id": "relative-clauses",
        "icon": "link",
        "title": "Relative clauses",
        "subtitle": "Which, that, who and whose",
        "rule": {
            "paragraphs": [
                "Use who for people. Use which or that for things: "
                "<em>Students who study abroad gain confidence.</em>",
                "Add extra detail in one sentence: "
                "<em>Renewable energy, which is growing fast, reduces emissions.</em>",
            ],
            "key_point_label": "Key point",
            "key_point": (
                "Use which or that to add detail — "
                "do not write a new very short sentence."
            ),
        },
        "pairs": [
            {
                "wrong": "The sector grew quickly. The sector employs millions.",
                "correct_html": (
                    "The sector <span class=\"wg-hl\">that</span> employs millions grew quickly."
                ),
                "fix": "Join with that or which.",
            },
            {
                "wrong": "Students who they study abroad gain confidence.",
                "correct_html": "Students <span class=\"wg-hl\">who study</span> abroad gain confidence.",
                "fix": "Do not repeat they after who.",
            },
            {
                "wrong": "The year, that saw the highest sales, was 2019.",
                "correct_html": "The year<span class=\"wg-hl\">,</span> which saw the highest sales<span class=\"wg-hl\">,</span> was 2019.",
                "fix": "Extra detail with commas → use which, not that.",
            },
            {
                "wrong": "A manager whose team performs well they receive bonuses.",
                "correct_html": (
                    "A manager <span class=\"wg-hl\">whose</span> team performs well "
                    "<span class=\"wg-hl\">receives</span> bonuses."
                ),
                "fix": "Whose means belonging to. Do not add they.",
            },
        ],
        "ielts_mistakes": [
            {
                "mistake": "You repeat the subject: people who they believe.",
                "fix": "Remove they or he/she inside the who clause.",
            },
            {
                "mistake": "You use that with commas around extra information.",
                "fix": "Use which when you add commas.",
            },
            {
                "mistake": "You add commas when which or that is essential.",
                "fix": "No commas when the detail identifies the noun.",
            },
            {
                "mistake": "You use where for things: the year where sales peaked.",
                "fix": "Use which or that for things. Where is for places.",
            },
        ],
    },
    {
        "id": "conditionals",
        "icon": "scale",
        "title": "Conditionals",
        "subtitle": "If… will, would and had",
        "rule": {
            "paragraphs": [
                "Real future: If + present, will: "
                "<em>If governments invest, pollution will fall.</em>",
                "Unreal idea now: If + past, would: "
                "<em>If every student had a laptop, learning would improve.</em>",
            ],
            "key_point_label": "Key point",
            "key_point": (
                "Do not use will after if: If governments invest — "
                "not If governments will invest."
            ),
        },
        "pairs": [
            {
                "wrong": "If governments will invest, pollution reduces.",
                "correct_html": (
                    "If governments <span class=\"wg-hl\">invest</span>, pollution "
                    "<span class=\"wg-hl\">will reduce</span>."
                ),
                "fix": "After if, use present — not will.",
            },
            {
                "wrong": "If I would have more time, I would travel.",
                "correct_html": "If I <span class=\"wg-hl\">had</span> more time, I <span class=\"wg-hl\">would travel</span>.",
                "fix": "After if, use had — not would.",
            },
            {
                "wrong": "If technology improved, we will solve the problem.",
                "correct_html": (
                    "If technology <span class=\"wg-hl\">improves</span>, we "
                    "<span class=\"wg-hl\">will solve</span> the problem."
                ),
                "fix": "Do not mix would and will in the same if-sentence.",
            },
            {
                "wrong": "If the law was passed last year, crime would fall now.",
                "correct_html": (
                    "If the law <span class=\"wg-hl\">had been passed</span> last year, crime "
                    "<span class=\"wg-hl\">would have fallen</span> by now."
                ),
                "fix": "Past unreal situation → had been + would have.",
            },
        ],
        "ielts_mistakes": [
            {
                "mistake": "Will after if: If people will work harder…",
                "fix": "Use present after if: If people work harder…",
            },
            {
                "mistake": "Would in both parts: If I would have time, I would…",
                "fix": "Would only in the second part.",
            },
            {
                "mistake": "You use if + will for something impossible in the past.",
                "fix": "Use had been + would have for past regrets.",
            },
            {
                "mistake": "No comma when the if-part comes first.",
                "fix": "Put a comma after the if-part: If X, Y.",
            },
        ],
    },
    {
        "id": "comparatives-superlatives",
        "icon": "chart",
        "title": "Comparatives and superlatives",
        "subtitle": "Comparing data in Task 1",
        "rule": {
            "paragraphs": [
                "Compare two with -er or more…than: <em>higher than</em>, "
                "<em>more significant than</em>.",
                "Pick the top or bottom with the: <em>the highest figure</em>, "
                "<em>the lowest rate</em>.",
            ],
            "key_point_label": "Key point",
            "key_point": (
                "Your Task 1 overview should name the highest and the lowest item."
            ),
        },
        "pairs": [
            {
                "wrong": "Sales were more high than costs.",
                "correct_html": "Sales were <span class=\"wg-hl\">higher than</span> costs.",
                "fix": "Short words take -er: higher, not more high.",
            },
            {
                "wrong": "Germany had the most highest figure.",
                "correct_html": "Germany had <span class=\"wg-hl\">the highest</span> figure.",
                "fix": "Use highest or most — not both.",
            },
            {
                "wrong": "Exports were two times high as imports.",
                "correct_html": "Exports were <span class=\"wg-hl\">twice as high as</span> imports.",
                "fix": "Say twice as high as.",
            },
            {
                "wrong": "The gap was significanter in 2020.",
                "correct_html": "The gap was <span class=\"wg-hl\">more significant</span> in 2020.",
                "fix": "Long words use more, not -er.",
            },
        ],
        "ielts_mistakes": [
            {
                "mistake": "You compare without than: lower 2019.",
                "fix": "Always add than: lower than in 2019.",
            },
            {
                "mistake": "You forget the: highest figure in the chart.",
                "fix": "Say the highest when it is the top one.",
            },
            {
                "mistake": "Vague words only: a bit more, a lot bigger — no numbers.",
                "fix": "Add data: 10% higher, double the amount.",
            },
            {
                "mistake": "Wrong forms: more good, most bad.",
                "fix": "Learn better/best, worse/worst.",
            },
        ],
    },
    {
        "id": "countable-uncountable",
        "icon": "list",
        "title": "Countable vs uncountable nouns",
        "subtitle": "Much/many, fewer/less",
        "rule": {
            "paragraphs": [
                "You can count cars and students — use many or fewer. "
                "You cannot count research or traffic — use much or less.",
                "Say <em>research shows</em> — not researches show.",
            ],
            "key_point_label": "Key point",
            "key_point": (
                "Fewer + plural noun (fewer cars). "
                "Less + no plural (less traffic)."
            ),
        },
        "pairs": [
            {
                "wrong": "There is less cars on the road.",
                "correct_html": "There are <span class=\"wg-hl\">fewer cars</span> on the road.",
                "fix": "Cars you can count → fewer cars.",
            },
            {
                "wrong": "Many research has been conducted.",
                "correct_html": "<span class=\"wg-hl\">Much research</span> has been conducted.",
                "fix": "Research is not countable → much research.",
            },
            {
                "wrong": "The amount of students increased.",
                "correct_html": "The <span class=\"wg-hl\">number</span> of students increased.",
                "fix": "Number of + things you count. Amount of + things you cannot count.",
            },
            {
                "wrong": "Governments need more equipments.",
                "correct_html": "Governments need <span class=\"wg-hl\">more equipment</span>.",
                "fix": "Equipment has no plural s.",
            },
        ],
        "ielts_mistakes": [
            {
                "mistake": "Less + plural: less people, less opportunities.",
                "fix": "Use fewer with plurals.",
            },
            {
                "mistake": "Plural s on uncountable words: informations, advices.",
                "fix": "Say information, advice, evidence — no s.",
            },
            {
                "mistake": "Many + uncountable: many traffic, many pollution.",
                "fix": "Say much traffic or a lot of pollution.",
            },
            {
                "mistake": "A few vs a little mixed up.",
                "fix": "A few reasons (countable). A little time (uncountable).",
            },
        ],
    },
    {
        "id": "prepositions-data",
        "icon": "target",
        "title": "Prepositions in data description",
        "subtitle": "Rise to, fall by, at, from…to",
        "rule": {
            "paragraphs": [
                "Rise to = reach a level: <em>rose to 40%</em>. "
                "Rise by = the change: <em>rose by 10%</em>.",
                "Use in for years: <em>in 2020</em>. "
                "Use from…to for a range: <em>from 20% to 30%</em>.",
            ],
            "key_point_label": "Key point",
            "key_point": (
                "To = the final number. By = how much it changed."
            ),
        },
        "pairs": [
            {
                "wrong": "Sales increased to 15% last year.",
                "correct_html": "Sales increased <span class=\"wg-hl\">by</span> 15% last year.",
                "fix": "By = the size of the change. To = the final level.",
            },
            {
                "wrong": "The figure peaked at 2019.",
                "correct_html": "The figure peaked <span class=\"wg-hl\">in</span> 2019.",
                "fix": "In + year. At + number (peaked at 80%).",
            },
            {
                "wrong": "Consumption fell from 30% by 10%.",
                "correct_html": "Consumption fell <span class=\"wg-hl\">from 30% to 20%</span>.",
                "fix": "From…to shows start and end.",
            },
            {
                "wrong": "There was a rise of 40% to 2015.",
                "correct_html": "There was a rise <span class=\"wg-hl\">in</span> 2015 <span class=\"wg-hl\">to 40%</span>.",
                "fix": "In + year. To + final figure.",
            },
        ],
        "ielts_mistakes": [
            {
                "mistake": "You mix up to and by: grew to 5% when you mean a 5-point rise.",
                "fix": "Ask: final level (to) or change size (by)?",
            },
            {
                "mistake": "On + year: on 2020.",
                "fix": "Say in 2020. On is for days.",
            },
            {
                "mistake": "Between 2010 to 2020.",
                "fix": "Say between 2010 and 2020, or from 2010 to 2020.",
            },
            {
                "mistake": "Account for vs consist of mixed up.",
                "fix": "Account for = make up a share. Consist of = are made of.",
            },
        ],
    },
    {
        "id": "punctuation",
        "icon": "write",
        "title": "Punctuation",
        "subtitle": "Commas and full stops",
        "rule": {
            "paragraphs": [
                "Use a comma after short openers: <em>Overall, the trend was upward.</em>",
                "Do not join two full sentences with only a comma. "
                "Use a full stop or a word like and or but.",
            ],
            "key_point_label": "Key point",
            "key_point": (
                "Two full sentences need a full stop — not just a comma between them."
            ),
        },
        "pairs": [
            {
                "wrong": "The trend increased, it peaked in 2019.",
                "correct_html": (
                    "The trend increased<span class=\"wg-hl\">;</span> it peaked in 2019."
                ),
                "fix": "Use a full stop or semicolon — not only a comma.",
            },
            {
                "wrong": "However pollution fell.",
                "correct_html": "<span class=\"wg-hl\">However,</span> pollution fell.",
                "fix": "However at the start needs a comma after it.",
            },
            {
                "wrong": "Although, costs rose, profits remained stable.",
                "correct_html": "Although costs rose<span class=\"wg-hl\">,</span> profits remained stable.",
                "fix": "No comma right after although.",
            },
            {
                "wrong": "The three sectors, manufacturing, services and agriculture, grew.",
                "correct_html": (
                    "The three sectors<span class=\"wg-hl\"> —</span> manufacturing, services and agriculture "
                    "<span class=\"wg-hl\">—</span> grew."
                ),
                "fix": "Too many commas — use dashes for the list.",
            },
        ],
        "ielts_mistakes": [
            {
                "mistake": "Comma between two full sentences in Task 2.",
                "fix": "Use a full stop, or join with and, but or so.",
            },
            {
                "mistake": "No comma after Furthermore or Therefore.",
                "fix": "Write Furthermore, or Therefore,",
            },
            {
                "mistake": "Apostrophe in the wrong place: government's should act.",
                "fix": "Apostrophe s only for belonging: the government's policy.",
            },
            {
                "mistake": "Too many dashes or exclamation marks.",
                "fix": "Keep it formal. Commas and full stops are enough.",
            },
        ],
    },
    {
        "id": "linking-cohesion",
        "icon": "link",
        "title": "Linking and cohesion grammar",
        "subtitle": "However, whereas, despite and although",
        "rule": {
            "paragraphs": [
                "Although + full sentence: <em>Although costs rose, profits stayed stable.</em>",
                "Despite + noun or short phrase — not a full sentence: "
                "<em>Despite the cost, sales grew.</em>",
            ],
            "key_point_label": "Key point",
            "key_point": (
                "Despite high prices ✓. Despite prices were high ✗ — use although instead."
            ),
        },
        "pairs": [
            {
                "wrong": "Despite the economy grew, unemployment rose.",
                "correct_html": (
                    "<span class=\"wg-hl\">Although</span> the economy grew, unemployment rose."
                ),
                "fix": "Despite + noun. Although + subject + verb.",
            },
            {
                "wrong": "However technology helps, it creates risks.",
                "correct_html": (
                    "<span class=\"wg-hl\">Although</span> technology helps, it creates risks."
                ),
                "fix": "However starts a new sentence. Although joins inside one sentence.",
            },
            {
                "wrong": "Whereas men prefer cars, but women prefer buses.",
                "correct_html": (
                    "Men prefer cars, <span class=\"wg-hl\">whereas</span> women prefer buses."
                ),
                "fix": "Use whereas or but — not both.",
            },
            {
                "wrong": "In spite of improve education, poverty persists.",
                "correct_html": (
                    "In spite of <span class=\"wg-hl\">improved education</span>, poverty persists."
                ),
                "fix": "After despite or in spite of, use a noun phrase.",
            },
        ],
        "ielts_mistakes": [
            {
                "mistake": "Despite + full sentence: Despite many people think…",
                "fix": "Use although, or change to Despite widespread belief…",
            },
            {
                "mistake": "However with no comma: However pollution fell.",
                "fix": "Write However, at the start of the sentence.",
            },
            {
                "mistake": "On the other hand with no first side stated.",
                "fix": "Use it only after you already showed one side.",
            },
            {
                "mistake": "Furthermore or Moreover at the start of every sentence.",
                "fix": "Vary: In addition, Another reason is, This also means.",
            },
        ],
    },
]


def get_grammar_topic(topic_id: str) -> dict | None:
    return next((t for t in GRAMMAR_TOPICS if t["id"] == topic_id), None)


def grammar_topic_ids() -> list[str]:
    return [t["id"] for t in GRAMMAR_TOPICS]
