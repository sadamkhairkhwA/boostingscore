QUESTION_TYPE_CATALOG = [
    {
        "slug": "true-false-not-given",
        "title": "True / False / Not Given",
        "description": "Check factual statements against the passage and separate contradiction from absence.",
        "icon": "scale",
        "lesson_id": "tfng-ynng",
        "learn_variant": "tfng",
        "strategy_titles": ["True / False / Not Given"],
    },
    {
        "slug": "yes-no-not-given",
        "title": "Yes / No / Not Given",
        "description": "Track the writer's view carefully and watch for hedging or qualified opinion.",
        "icon": "compass",
        "lesson_id": "tfng-ynng",
        "learn_variant": "ynng",
        "strategy_titles": ["Yes / No / Not Given"],
    },
    {
        "slug": "multiple-choice",
        "title": "Multiple choice",
        "description": "Eliminate distractors and prove each answer from the exact part of the text.",
        "icon": "letters",
        "lesson_id": "multiple-choice",
        "learn_variant": "multiple-choice",
        "strategy_titles": [],
    },
    {
        "slug": "matching-headings",
        "title": "Matching headings",
        "description": "Match each paragraph to its main idea, not just one attractive detail.",
        "icon": "target",
        "lesson_id": "matching-headings",
        "learn_variant": "matching-headings",
        "strategy_titles": ["Matching headings"],
    },
    {
        "slug": "matching-information-features",
        "title": "Matching information / features",
        "description": "Scan for where details appear and remember that paragraphs or names can repeat.",
        "icon": "link",
        "lesson_id": "matching-information",
        "learn_variant": "matching-information-features",
        "strategy_titles": ["Matching information", "Matching features"],
    },
    {
        "slug": "sentence-summary-completion",
        "title": "Sentence & summary completion",
        "description": "Use the word limit, paraphrase clues, and exact copying to fill the gaps correctly.",
        "icon": "pen",
        "lesson_id": "sentence-completion",
        "extra_lesson_id": "summary-completion",
        "learn_variant": "sentence-summary",
        "strategy_titles": ["Gap-fill"],
    },
    {
        "slug": "short-answer",
        "title": "Short answer",
        "description": "Find a precise detail and answer in a few words without breaking the word limit.",
        "icon": "clipboard",
        "lesson_id": None,
        "learn_variant": "short-answer",
        "strategy_titles": ["Short answer"],
    },
]


QUESTION_TYPE_PRACTICE_SETS = {
    "true-false-not-given": [
        {
            "set_number": 1,
            "title": "Set 1",
            "timer_minutes": 20,
            "instruction": "Read the passage and decide whether each statement is True, False, or Not Given.",
            "passage_title": "Why cities are switching to electric buses",
            "passage_intro": "One passage. Ten TFNG questions. Suggested time: 20 minutes.",
            "passage_paragraphs": [
                {
                    "label": "A",
                    "text": (
                        "Over the last decade, many city governments have announced plans to replace "
                        "diesel buses with electric fleets. The strongest argument has been air quality. "
                        "Buses travel through dense urban corridors for long hours each day, so reducing "
                        "tailpipe emissions can have an immediate effect near schools, hospitals, and major "
                        "junctions. Several cities report that electric buses are especially attractive on "
                        "routes where traffic is slow and frequent stopping amplifies fuel waste."
                    ),
                },
                {
                    "label": "B",
                    "text": (
                        "Cost, however, remains a barrier. Electric buses are usually more expensive to "
                        "buy than diesel models, and operators must also invest in charging systems, depot "
                        "upgrades, and staff training. Supporters argue that lower maintenance and fuel "
                        "costs partly offset these expenses over time, but the savings vary according to "
                        "energy prices, route length, and climate."
                    ),
                },
                {
                    "label": "C",
                    "text": (
                        "Performance has improved rapidly. Early fleets were criticised because batteries "
                        "lost range in cold weather and charging schedules were difficult to plan around "
                        "peak service hours. Manufacturers have since improved battery management systems, "
                        "and many operators now use overnight charging combined with short top-ups at key "
                        "terminals. Even so, very long suburban routes can still be challenging."
                    ),
                },
                {
                    "label": "D",
                    "text": (
                        "Some transport analysts warn that electrification alone is not enough. If bus "
                        "frequency remains poor or routes are unreliable, passengers may continue choosing "
                        "private cars. For this reason, the most successful programmes combine cleaner "
                        "vehicles with bus-lane protection, timetable redesign, and better passenger "
                        "information. In other words, technology works best when paired with service reform."
                    ),
                },
            ],
            "questions": [
                {
                    "number": 1,
                    "prompt": "Cities mainly support electric buses because they are more comfortable for drivers.",
                    "input_type": "choice",
                    "options": ["True", "False", "Not Given"],
                    "answer": "False",
                    "explanation": "The passage says the strongest argument is air quality, not driver comfort.",
                },
                {
                    "number": 2,
                    "prompt": "Electric buses are presented as especially useful on slow urban routes.",
                    "input_type": "choice",
                    "options": ["True", "False", "Not Given"],
                    "answer": "True",
                    "explanation": "Paragraph A says they are especially attractive where traffic is slow and stopping is frequent.",
                },
                {
                    "number": 3,
                    "prompt": "Every city that introduced electric buses has already reduced pollution around hospitals.",
                    "input_type": "choice",
                    "options": ["True", "False", "Not Given"],
                    "answer": "Not Given",
                    "explanation": "The passage says reducing emissions can have an effect near hospitals, but it does not say every city has already achieved that result.",
                },
                {
                    "number": 4,
                    "prompt": "Operators can avoid all additional infrastructure spending when they buy electric buses.",
                    "input_type": "choice",
                    "options": ["True", "False", "Not Given"],
                    "answer": "False",
                    "explanation": "Paragraph B says operators must invest in charging systems and depot upgrades.",
                },
                {
                    "number": 5,
                    "prompt": "Long-term savings from electric buses are identical in all regions.",
                    "input_type": "choice",
                    "options": ["True", "False", "Not Given"],
                    "answer": "False",
                    "explanation": "Savings vary according to energy prices, route length, and climate.",
                },
                {
                    "number": 6,
                    "prompt": "Early electric fleets were criticised for battery range problems in winter.",
                    "input_type": "choice",
                    "options": ["True", "False", "Not Given"],
                    "answer": "True",
                    "explanation": "Paragraph C states that early fleets lost range in cold weather.",
                },
                {
                    "number": 7,
                    "prompt": "Manufacturers solved every charging challenge faced by suburban routes.",
                    "input_type": "choice",
                    "options": ["True", "False", "Not Given"],
                    "answer": "False",
                    "explanation": "The passage says very long suburban routes can still be challenging.",
                },
                {
                    "number": 8,
                    "prompt": "The article states that passengers prefer quieter buses to more frequent services.",
                    "input_type": "choice",
                    "options": ["True", "False", "Not Given"],
                    "answer": "Not Given",
                    "explanation": "There is no comparison between quieter buses and more frequent services.",
                },
                {
                    "number": 9,
                    "prompt": "Service reform is described as important alongside electrification.",
                    "input_type": "choice",
                    "options": ["True", "False", "Not Given"],
                    "answer": "True",
                    "explanation": "Paragraph D says technology works best when paired with service reform.",
                },
                {
                    "number": 10,
                    "prompt": "Bus-lane protection is criticised as ineffective in the passage.",
                    "input_type": "choice",
                    "options": ["True", "False", "Not Given"],
                    "answer": "False",
                    "explanation": "It is listed as part of the most successful programmes, not criticised.",
                },
            ],
        }
    ],
    "yes-no-not-given": [
        {
            "set_number": 1,
            "title": "Set 1",
            "timer_minutes": 20,
            "instruction": "Read the writer's argument and decide whether the statements agree with the writer's views: Yes, No, or Not Given.",
            "passage_title": "Should universities adopt a four-day teaching week?",
            "passage_intro": "One passage. Ten Y/N/NG questions. Suggested time: 20 minutes.",
            "passage_paragraphs": [
                {
                    "label": "A",
                    "text": (
                        "Proposals for a four-day teaching week at universities are often presented as a "
                        "simple efficiency reform, but the issue is more complicated. Supporters argue "
                        "that concentrated schedules reduce commuting costs and free one day for independent "
                        "study, paid work, or rest. These advantages are real, particularly for students "
                        "who travel long distances or balance study with family commitments."
                    ),
                },
                {
                    "label": "B",
                    "text": (
                        "However, compressed timetables can also intensify the academic week. If the same "
                        "contact hours are squeezed into fewer days, teaching blocks become longer and "
                        "mental fatigue may increase, especially in subjects that require sustained problem "
                        "solving. A reform that looks efficient on paper may therefore disadvantage students "
                        "who need more time between sessions to process material."
                    ),
                },
                {
                    "label": "C",
                    "text": (
                        "The strongest case for change appears in programmes where a large share of learning "
                        "already happens through seminars, recorded lectures, and project work rather than "
                        "daily laboratory attendance. In those contexts, timetable redesign can improve "
                        "flexibility without necessarily reducing academic quality. Yet institutions should "
                        "avoid presenting one model as universally suitable."
                    ),
                },
                {
                    "label": "D",
                    "text": (
                        "For this reason, universities considering a four-day structure should pilot it "
                        "selectively, collect evidence, and give departments room to adapt. A cautious trial "
                        "is preferable to sweeping implementation driven by branding alone. Higher education "
                        "is too diverse for a slogan-based reform."
                    ),
                },
            ],
            "questions": [
                {
                    "number": 1,
                    "prompt": "The writer believes the reform is completely straightforward to implement.",
                    "input_type": "choice",
                    "options": ["Yes", "No", "Not Given"],
                    "answer": "No",
                    "explanation": "The passage opens by saying the issue is more complicated, so the writer rejects that view.",
                },
                {
                    "number": 2,
                    "prompt": "The writer accepts that some students could save money under a four-day teaching week.",
                    "input_type": "choice",
                    "options": ["Yes", "No", "Not Given"],
                    "answer": "Yes",
                    "explanation": "Paragraph A says reduced commuting costs are a real advantage.",
                },
                {
                    "number": 3,
                    "prompt": "The writer thinks all university subjects would benefit equally from compressed schedules.",
                    "input_type": "choice",
                    "options": ["Yes", "No", "Not Given"],
                    "answer": "No",
                    "explanation": "The writer says one model should not be presented as universally suitable.",
                },
                {
                    "number": 4,
                    "prompt": "Mental fatigue may rise when the same teaching hours are packed into fewer days.",
                    "input_type": "choice",
                    "options": ["Yes", "No", "Not Given"],
                    "answer": "Yes",
                    "explanation": "Paragraph B directly states that mental fatigue may increase.",
                },
                {
                    "number": 5,
                    "prompt": "The writer says laboratory-based courses should always stay on a five-day pattern.",
                    "input_type": "choice",
                    "options": ["Yes", "No", "Not Given"],
                    "answer": "Not Given",
                    "explanation": "The writer says the strongest case is in less lab-dependent programmes, but does not make an absolute statement about all laboratory courses.",
                },
                {
                    "number": 6,
                    "prompt": "Programmes built around seminars and project work may handle the reform more effectively.",
                    "input_type": "choice",
                    "options": ["Yes", "No", "Not Given"],
                    "answer": "Yes",
                    "explanation": "Paragraph C says the strongest case appears in programmes with that structure.",
                },
                {
                    "number": 7,
                    "prompt": "The writer argues that flexibility automatically improves academic quality.",
                    "input_type": "choice",
                    "options": ["Yes", "No", "Not Given"],
                    "answer": "No",
                    "explanation": "The writer says flexibility can improve without necessarily reducing quality, not that it automatically improves quality.",
                },
                {
                    "number": 8,
                    "prompt": "The writer supports a cautious pilot before a wider rollout.",
                    "input_type": "choice",
                    "options": ["Yes", "No", "Not Given"],
                    "answer": "Yes",
                    "explanation": "Paragraph D says a cautious trial is preferable.",
                },
                {
                    "number": 9,
                    "prompt": "The writer believes students should spend the free day on paid work rather than rest.",
                    "input_type": "choice",
                    "options": ["Yes", "No", "Not Given"],
                    "answer": "Not Given",
                    "explanation": "The writer lists several possible uses of the day and does not rank them.",
                },
                {
                    "number": 10,
                    "prompt": "The writer criticises reforms designed mainly for image or branding purposes.",
                    "input_type": "choice",
                    "options": ["Yes", "No", "Not Given"],
                    "answer": "Yes",
                    "explanation": "Paragraph D warns against sweeping implementation driven by branding alone.",
                },
            ],
        }
    ],
    "multiple-choice": [
        {
            "set_number": 1,
            "title": "Set 1",
            "timer_minutes": 20,
            "instruction": "Read the passage and choose the best answer, A, B, C, or D, for each question.",
            "passage_title": "How city libraries are redefining public space",
            "passage_intro": "One passage. Ten multiple-choice questions. Suggested time: 20 minutes.",
            "passage_paragraphs": [
                {
                    "label": "A",
                    "text": (
                        "Modern libraries are no longer defined only by the books they hold. In many "
                        "cities, library managers have redesigned quiet reading rooms, added digital "
                        "studios, and opened flexible community areas that can host language classes, "
                        "career workshops, or local advice sessions. This shift reflects a broader view "
                        "of the library as shared civic infrastructure rather than a narrow storage system."
                    ),
                },
                {
                    "label": "B",
                    "text": (
                        "Demand for these new services grew quickly after local councils realised that "
                        "many residents lacked reliable study space, fast internet, or access to basic "
                        "technical support at home. Librarians, however, note that broadening the role of "
                        "the institution creates new pressures. Staff need training, rooms must be booked "
                        "carefully, and some traditional users worry that noise levels will rise."
                    ),
                },
                {
                    "label": "C",
                    "text": (
                        "The strongest library programmes tend to solve this tension through zoning rather "
                        "than choosing one identity over another. Silent areas remain protected, while "
                        "group work and public events move into distinct spaces with clearer scheduling. "
                        "This model accepts that different users need different environments and that a "
                        "public building can support several forms of learning at once."
                    ),
                },
                {
                    "label": "D",
                    "text": (
                        "There are financial limits, of course. Extending opening hours or installing "
                        "specialist equipment costs money at a time when many councils face tight budgets. "
                        "Even so, supporters argue that libraries still offer unusually high public value "
                        "per pound spent because they combine education, access, and social support in one "
                        "place. The debate is therefore less about whether libraries matter and more about "
                        "what kind of institution they should become."
                    ),
                },
            ],
            "questions": [
                {
                    "number": 1,
                    "prompt": "What main change in city libraries does the passage describe?",
                    "input_type": "choice",
                    "options": [
                        "A. They are storing fewer printed books than before.",
                        "B. They are becoming wider community learning spaces.",
                        "C. They are being moved to cheaper suburban sites.",
                        "D. They are focusing only on digital entertainment.",
                    ],
                    "answer": "B. They are becoming wider community learning spaces.",
                    "explanation": "The passage focuses on libraries expanding into shared civic and learning spaces, not on reducing printed books.",
                },
                {
                    "number": 2,
                    "prompt": "Why did councils see a need for broader library services?",
                    "input_type": "choice",
                    "options": [
                        "A. Residents wanted more fiction titles.",
                        "B. Libraries had too many unused staff.",
                        "C. Many people lacked study space, internet, or technical support at home.",
                        "D. Private companies stopped offering training courses.",
                    ],
                    "answer": "C. Many people lacked study space, internet, or technical support at home.",
                    "explanation": "Paragraph B gives those three reasons directly.",
                },
                {
                    "number": 3,
                    "prompt": "What concern do some traditional users have?",
                    "input_type": "choice",
                    "options": [
                        "A. Noise could increase.",
                        "B. Book loans will be banned.",
                        "C. Libraries will open too early.",
                        "D. Staff will remove silent areas completely.",
                    ],
                    "answer": "A. Noise could increase.",
                    "explanation": "Paragraph B says some traditional users worry that noise levels will rise.",
                },
                {
                    "number": 4,
                    "prompt": "The word 'zoning' in paragraph C is closest in meaning to:",
                    "input_type": "choice",
                    "options": [
                        "A. reducing the size of the building",
                        "B. separating the building into areas with different uses",
                        "C. selling off unused land",
                        "D. limiting entry to staff only",
                    ],
                    "answer": "B. separating the building into areas with different uses",
                    "explanation": "The passage explains that silent areas stay protected while group work moves elsewhere.",
                },
                {
                    "number": 5,
                    "prompt": "What is presented as the best way to manage different user needs?",
                    "input_type": "choice",
                    "options": [
                        "A. Closing community events",
                        "B. Forcing everyone into one shared room",
                        "C. Protecting quiet zones while using separate spaces for louder activities",
                        "D. Ending digital services entirely",
                    ],
                    "answer": "C. Protecting quiet zones while using separate spaces for louder activities",
                    "explanation": "Paragraph C describes this as the strongest approach.",
                },
                {
                    "number": 6,
                    "prompt": "Which statement best reflects the writer's position on funding?",
                    "input_type": "choice",
                    "options": [
                        "A. Library expansion is impossible because councils are under pressure.",
                        "B. Costs exist, but libraries may still deliver strong public value.",
                        "C. Funding problems are exaggerated and unimportant.",
                        "D. Only specialist equipment deserves investment.",
                    ],
                    "answer": "B. Costs exist, but libraries may still deliver strong public value.",
                    "explanation": "Paragraph D balances financial limits against high public value.",
                },
                {
                    "number": 7,
                    "prompt": "What does the writer say the debate is now mostly about?",
                    "input_type": "choice",
                    "options": [
                        "A. Whether libraries should continue to exist at all",
                        "B. Which publishers should supply new books",
                        "C. What kind of institution libraries should become",
                        "D. Whether printed books should be removed this year",
                    ],
                    "answer": "C. What kind of institution libraries should become",
                    "explanation": "The final sentence states this directly.",
                },
                {
                    "number": 8,
                    "prompt": "Which of the following is NOT mentioned as a new library use?",
                    "input_type": "choice",
                    "options": [
                        "A. Language classes",
                        "B. Career workshops",
                        "C. Local advice sessions",
                        "D. Hospital treatment rooms",
                    ],
                    "answer": "D. Hospital treatment rooms",
                    "explanation": "The other three appear in paragraph A; hospital treatment rooms do not.",
                },
                {
                    "number": 9,
                    "prompt": "Why do librarians need extra training according to the passage?",
                    "input_type": "choice",
                    "options": [
                        "A. Because the institution's role has broadened",
                        "B. Because printed books are difficult to catalogue",
                        "C. Because children now visit more often",
                        "D. Because councils require daily exams",
                    ],
                    "answer": "A. Because the institution's role has broadened",
                    "explanation": "Paragraph B links broader services with new pressures, including staff training.",
                },
                {
                    "number": 10,
                    "prompt": "What is the main purpose of the passage?",
                    "input_type": "choice",
                    "options": [
                        "A. To argue that libraries should return to a book-only model",
                        "B. To describe how libraries are evolving and the tensions that creates",
                        "C. To compare libraries with museums in detail",
                        "D. To explain how to design digital studios cheaply",
                    ],
                    "answer": "B. To describe how libraries are evolving and the tensions that creates",
                    "explanation": "The whole passage explains the shift in library function and the trade-offs involved.",
                },
            ],
        }
    ],
    "matching-headings": [
        {
            "set_number": 1,
            "title": "Set 1",
            "timer_minutes": 20,
            "instruction": "Choose the correct heading for each paragraph from the list of headings.",
            "passage_title": "Restoring an urban river",
            "passage_intro": "One passage. Eight matching-headings questions. Suggested time: 20 minutes.",
            "headings": [
                "i. Resistance from local traders",
                "ii. A polluted river hidden from view",
                "iii. Measuring whether the project really worked",
                "iv. Why engineers first focused on flood control",
                "v. The return of wildlife after habitat redesign",
                "vi. Education programmes for nearby schools",
                "vii. Turning the river back into a public place",
                "viii. Long-term maintenance as the deciding factor",
                "ix. A plan that joined design with community input",
                "x. Unexpected pressure on housing prices",
                    ],
            "passage_paragraphs": [
                {
                    "label": "A",
                    "text": (
                        "For decades, the River Len was treated as a technical problem rather than a "
                        "public asset. Concrete walls narrowed the channel, sections were covered, and "
                        "most residents could walk through the district without realising a river still "
                        "ran beneath it. By the early 2000s, however, the cost of repeated drainage "
                        "failures made that approach harder to defend."
                    ),
                },
                {
                    "label": "B",
                    "text": (
                        "The city's first response was practical rather than ecological. Engineers widened "
                        "culverts and reworked junction points to move stormwater away faster during heavy "
                        "rain. This reduced immediate flood risk, but it did little to improve public "
                        "access, water quality, or the visual condition of the area."
                    ),
                },
                {
                    "label": "C",
                    "text": (
                        "A more ambitious phase began when planners invited residents, business owners, and "
                        "local schools to comment on early proposals. Their feedback changed the scheme "
                        "substantially: footpaths were added, sitting areas were redesigned, and planting "
                        "choices shifted toward species people said they wanted to see in the corridor."
                    ),
                },
                {
                    "label": "D",
                    "text": (
                        "Once sections of the river were uncovered, the project team concentrated on making "
                        "the banks usable rather than decorative only. Access ramps, low seating, and safer "
                        "crossings were inserted so that the river could function as part of daily movement "
                        "through the district, not just as a feature to admire from a distance."
                    ),
                },
                {
                    "label": "E",
                    "text": (
                        "Ecological monitoring later showed encouraging changes. Invertebrate counts rose, "
                        "banks supported more native vegetation, and bird sightings became more frequent in "
                        "areas that had previously offered little shelter. These gains were strongest where "
                        "shallow edges and varied planting had been built into the restoration plan."
                    ),
                },
                {
                    "label": "F",
                    "text": (
                        "Yet success was not judged by appearance alone. The council compared flood records, "
                        "water-testing results, user surveys, and maintenance costs over several years. "
                        "Officials argued that without this evidence, it would have been easy to celebrate a "
                        "photogenic project without knowing whether it actually solved the old problems."
                    ),
                },
                {
                    "label": "G",
                    "text": (
                        "Some positive side effects created fresh debate. Cafes and small businesses nearby "
                        "benefited from higher footfall, but rents also began to rise. Residents who had "
                        "long supported the restoration worried that improved public space might eventually "
                        "push lower-income households away from the district."
                    ),
                },
                {
                    "label": "H",
                    "text": (
                        "Project leaders now say the hardest work begins after construction ends. Paths, "
                        "planting, litter removal, and water-flow management all require steady funding and "
                        "clear responsibility. Without that, even a well-designed river corridor can decline "
                        "quickly and lose the trust built during redevelopment."
                    ),
                },
            ],
            "questions": [
                {"number": 1, "prompt": "Paragraph A", "input_type": "choice", "options": ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"], "answer": "ii", "explanation": "Paragraph A describes a river that was covered and barely visible."},
                {"number": 2, "prompt": "Paragraph B", "input_type": "choice", "options": ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"], "answer": "iv", "explanation": "The paragraph focuses on the first flood-control response by engineers."},
                {"number": 3, "prompt": "Paragraph C", "input_type": "choice", "options": ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"], "answer": "ix", "explanation": "Design changed after input from residents and other groups."},
                {"number": 4, "prompt": "Paragraph D", "input_type": "choice", "options": ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"], "answer": "vii", "explanation": "The paragraph is about making the river part of daily public use."},
                {"number": 5, "prompt": "Paragraph E", "input_type": "choice", "options": ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"], "answer": "v", "explanation": "The central idea is the return of wildlife and vegetation."},
                {"number": 6, "prompt": "Paragraph F", "input_type": "choice", "options": ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"], "answer": "iii", "explanation": "This paragraph is about measuring whether the project worked."},
                {"number": 7, "prompt": "Paragraph G", "input_type": "choice", "options": ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"], "answer": "x", "explanation": "The paragraph focuses on rising rents and housing pressure."},
                {"number": 8, "prompt": "Paragraph H", "input_type": "choice", "options": ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"], "answer": "viii", "explanation": "It stresses maintenance after construction as the key long-term issue."},
            ],
        }
    ],
    "matching-information-features": [
        {
            "set_number": 1,
            "title": "Set 1",
            "timer_minutes": 20,
            "instruction": "Which paragraph (A-E) contains the following information? Paragraphs may be used more than once.",
            "passage_title": "Five approaches to reducing food waste",
            "passage_intro": "One passage. Ten matching-information / features questions. Suggested time: 20 minutes.",
            "passage_paragraphs": [
                {
                    "label": "A",
                    "text": (
                        "A hospital group in Leeds cut kitchen waste by introducing smaller default portions "
                        "for evening meals while allowing patients to request extra servings. Nutrition staff "
                        "reported that plate waste fell without reducing patient satisfaction."
                    ),
                },
                {
                    "label": "B",
                    "text": (
                        "A supermarket chain tested dynamic discount labels that lowered the price of fresh "
                        "food as its sell-by date approached. Managers said the system worked best when staff "
                        "explained clearly that the products were still safe to eat."
                    ),
                },
                {
                    "label": "C",
                    "text": (
                        "At one university, researchers redesigned cafeteria trays so fruit and salads were "
                        "more visible at the start of the serving line. They found that selection patterns "
                        "changed even before students noticed the layout had been altered."
                    ),
                },
                {
                    "label": "D",
                    "text": (
                        "Several local councils invested in household composting schemes, but results were "
                        "mixed. Participation was highest where residents received both free starter kits and "
                        "simple instructions about what could and could not be composted."
                    ),
                },
                {
                    "label": "E",
                    "text": (
                        "A mobile app developed in Bristol allowed restaurants to sell unsold meals at the "
                        "end of the day for reduced prices. Owners liked the additional income, but some said "
                        "predicting how much food would remain was difficult during festival periods."
                    ),
                },
            ],
            "questions": [
                {"number": 1, "prompt": "mentions a method that depended on good customer communication", "input_type": "choice", "options": ["A", "B", "C", "D", "E"], "answer": "B", "explanation": "Paragraph B says the discount system worked best when staff explained it clearly."},
                {"number": 2, "prompt": "describes uncertainty caused by unusual seasonal demand", "input_type": "choice", "options": ["A", "B", "C", "D", "E"], "answer": "E", "explanation": "Festival periods made it hard to predict leftovers in paragraph E."},
                {"number": 3, "prompt": "reports that satisfaction stayed stable after portion sizes changed", "input_type": "choice", "options": ["A", "B", "C", "D", "E"], "answer": "A", "explanation": "Paragraph A says plate waste fell without reducing satisfaction."},
                {"number": 4, "prompt": "shows that behaviour changed before users consciously recognised the intervention", "input_type": "choice", "options": ["A", "B", "C", "D", "E"], "answer": "C", "explanation": "Paragraph C says selection patterns changed before students noticed the redesign."},
                {"number": 5, "prompt": "contains an example with mixed success across different locations", "input_type": "choice", "options": ["A", "B", "C", "D", "E"], "answer": "D", "explanation": "Paragraph D explicitly says results were mixed."},
                {"number": 6, "prompt": "mentions extra earnings as a benefit", "input_type": "choice", "options": ["A", "B", "C", "D", "E"], "answer": "E", "explanation": "Restaurant owners liked the additional income in paragraph E."},
                {"number": 7, "prompt": "focuses on changing the default amount people received", "input_type": "choice", "options": ["A", "B", "C", "D", "E"], "answer": "A", "explanation": "Paragraph A describes smaller default portions."},
                {"number": 8, "prompt": "explains that free equipment helped participation", "input_type": "choice", "options": ["A", "B", "C", "D", "E"], "answer": "D", "explanation": "Free starter kits are mentioned in paragraph D."},
                {"number": 9, "prompt": "describes a strategy based on timing price reductions", "input_type": "choice", "options": ["A", "B", "C", "D", "E"], "answer": "B", "explanation": "Dynamic labels reduced price as the sell-by date approached in paragraph B."},
                {"number": 10, "prompt": "involves the visual order in which people saw food choices", "input_type": "choice", "options": ["A", "B", "C", "D", "E"], "answer": "C", "explanation": "Paragraph C is about making fruit and salads visible at the start of the line."},
            ],
        }
    ],
    "sentence-summary-completion": [
        {
            "set_number": 1,
            "title": "Set 1",
            "timer_minutes": 20,
            "instruction": "Complete the sentences and summary using NO MORE THAN TWO WORDS AND/OR A NUMBER from the passage.",
            "passage_title": "Battery recycling and the supply chain",
            "passage_intro": "One passage. Ten completion questions. Suggested time: 20 minutes.",
            "passage_paragraphs": [
                {
                    "label": "A",
                    "text": (
                        "As demand for electric vehicles grows, battery recycling is moving from a niche "
                        "industry to a strategic priority. Manufacturers once treated used batteries mainly "
                        "as a waste problem, but they now see them as a secondary source of materials such "
                        "as lithium, nickel, and cobalt. Recovering these inputs can reduce pressure on new "
                        "mining projects and improve supply resilience."
                    ),
                },
                {
                    "label": "B",
                    "text": (
                        "The process is not simple. Before valuable metals can be recovered, batteries "
                        "must be collected, sorted by chemistry, and discharged safely. This stage is labour "
                        "intensive and expensive, especially when packs arrive in different sizes and states "
                        "of damage. Transport rules are also strict because defective units can overheat."
                    ),
                },
                {
                    "label": "C",
                    "text": (
                        "Even so, analysts expect recycling to become more competitive as larger volumes of "
                        "end-of-life batteries return from the first generation of electric vehicles. Scale "
                        "matters because plants can spread fixed costs more efficiently once supply becomes "
                        "steady rather than irregular."
                    ),
                },
                {
                    "label": "D",
                    "text": (
                        "Policy will shape the pace of growth. Some governments already require producers "
                        "to finance collection systems, while others are setting minimum recycled-content "
                        "targets for new batteries. Industry groups support clearer regulation, arguing that "
                        "predictable rules make investment decisions easier."
                    ),
                },
            ],
            "questions": [
                {"number": 1, "prompt": "Used batteries are now seen as a ________ of valuable materials.", "input_type": "text", "answer": "secondary source", "accepted": ["secondary source"], "explanation": "Paragraph A says they are seen as a secondary source of materials."},
                {"number": 2, "prompt": "Recovering lithium and cobalt can improve supply ________.", "input_type": "text", "answer": "resilience", "accepted": ["resilience"], "explanation": "Paragraph A uses the phrase supply resilience."},
                {"number": 3, "prompt": "Batteries have to be ________ safely before metal recovery begins.", "input_type": "text", "answer": "discharged", "accepted": ["discharged"], "explanation": "Paragraph B says batteries must be discharged safely."},
                {"number": 4, "prompt": "Sorting is difficult because battery packs arrive in different sizes and states of ________.", "input_type": "text", "answer": "damage", "accepted": ["damage"], "explanation": "Paragraph B names different sizes and states of damage."},
                {"number": 5, "prompt": "Transport rules are strict because defective units can ________.", "input_type": "text", "answer": "overheat", "accepted": ["overheat"], "explanation": "Paragraph B says defective units can overheat."},
                {"number": 6, "prompt": "Summary: Recycling becomes more competitive when larger ________ of used batteries return to the market.", "input_type": "text", "answer": "volumes", "accepted": ["volumes", "larger volumes"], "explanation": "Paragraph C says larger volumes of end-of-life batteries will return."},
                {"number": 7, "prompt": "Summary: Greater scale helps plants spread their fixed ________ more efficiently.", "input_type": "text", "answer": "costs", "accepted": ["costs", "fixed costs"], "explanation": "Paragraph C states that plants can spread fixed costs more efficiently."},
                {"number": 8, "prompt": "Summary: Governments may require producers to finance ________ systems.", "input_type": "text", "answer": "collection", "accepted": ["collection", "collection systems"], "explanation": "Paragraph D says some governments require producers to finance collection systems."},
                {"number": 9, "prompt": "Summary: Some countries are setting minimum recycled-content ________ for new batteries.", "input_type": "text", "answer": "targets", "accepted": ["targets", "minimum recycled-content targets"], "explanation": "Paragraph D uses the word targets."},
                {"number": 10, "prompt": "Summary: Industry groups say predictable rules make ________ decisions easier.", "input_type": "text", "answer": "investment", "accepted": ["investment", "investment decisions"], "explanation": "Paragraph D says predictable rules make investment decisions easier."},
            ],
        }
    ],
    "short-answer": [
        {
            "set_number": 1,
            "title": "Set 1",
            "timer_minutes": 20,
            "instruction": "Answer the questions below using NO MORE THAN TWO WORDS AND/OR A NUMBER from the passage.",
            "passage_title": "Late-night museum openings",
            "passage_intro": "One passage. Ten short-answer questions. Suggested time: 20 minutes.",
            "passage_paragraphs": [
                {
                    "label": "A",
                    "text": (
                        "Several national museums have extended opening hours on one evening each week "
                        "to attract visitors who cannot attend during the day. Early trials showed that "
                        "late sessions appealed strongly to young professionals and tourists, especially "
                        "in city centres where restaurants and public transport remained active after work."
                    ),
                },
                {
                    "label": "B",
                    "text": (
                        "Managers initially assumed that ticket revenue would justify the change, but the "
                        "first benefits appeared elsewhere. Shops sold more exhibition catalogues, cafes "
                        "performed better, and special talks created sponsorship opportunities. Security and "
                        "staffing costs still rose, however, so profitability depended on careful programming."
                    ),
                },
                {
                    "label": "C",
                    "text": (
                        "Audience research also revealed that families used evening openings differently "
                        "from other visitors. Parents preferred shorter routes through major galleries and "
                        "responded well to activity sheets or timed storytelling sessions. Where museums "
                        "ignored this pattern, family dwell time was lower than expected."
                    ),
                },
                {
                    "label": "D",
                    "text": (
                        "The most successful institutions treated late openings as a distinct offer rather "
                        "than simply a longer version of the daytime schedule. They adjusted lighting, added "
                        "live interpretation, and timed events around commuter patterns. This made the visit "
                        "feel intentional, not accidental."
                    ),
                },
            ],
            "questions": [
                {"number": 1, "prompt": "Which group, besides tourists, was especially attracted by late sessions?", "input_type": "text", "answer": "young professionals", "accepted": ["young professionals"], "explanation": "Paragraph A says late sessions appealed strongly to young professionals and tourists."},
                {"number": 2, "prompt": "What remained active after work in city centres besides restaurants?", "input_type": "text", "answer": "public transport", "accepted": ["public transport"], "explanation": "Paragraph A says restaurants and public transport remained active."},
                {"number": 3, "prompt": "What did managers first expect would justify the timetable change?", "input_type": "text", "answer": "ticket revenue", "accepted": ["ticket revenue"], "explanation": "Paragraph B says managers initially assumed ticket revenue would justify it."},
                {"number": 4, "prompt": "What type of museum publication sold more during late openings?", "input_type": "text", "answer": "catalogues", "accepted": ["catalogues", "exhibition catalogues"], "explanation": "Paragraph B says shops sold more exhibition catalogues."},
                {"number": 5, "prompt": "What kind of opportunities did special talks create?", "input_type": "text", "answer": "sponsorship opportunities", "accepted": ["sponsorship opportunities", "sponsorship"], "explanation": "Paragraph B uses the phrase sponsorship opportunities."},
                {"number": 6, "prompt": "Which group preferred shorter routes through major galleries?", "input_type": "text", "answer": "parents", "accepted": ["parents"], "explanation": "Paragraph C says parents preferred shorter routes."},
                {"number": 7, "prompt": "Name one format that improved the family experience.", "input_type": "text", "answer": "activity sheets", "accepted": ["activity sheets", "storytelling sessions", "timed storytelling sessions"], "explanation": "Paragraph C gives activity sheets and timed storytelling sessions as examples."},
                {"number": 8, "prompt": "What was lower than expected when museums ignored family behaviour patterns?", "input_type": "text", "answer": "family dwell time", "accepted": ["family dwell time", "dwell time"], "explanation": "Paragraph C says family dwell time was lower than expected."},
                {"number": 9, "prompt": "Successful institutions treated late openings as a distinct ________.", "input_type": "text", "answer": "offer", "accepted": ["offer", "distinct offer"], "explanation": "Paragraph D says they treated it as a distinct offer."},
                {"number": 10, "prompt": "Events were timed around which visitor movement pattern?", "input_type": "text", "answer": "commuter patterns", "accepted": ["commuter patterns", "commuter pattern"], "explanation": "Paragraph D says events were timed around commuter patterns."},
            ],
        }
    ],
}


def question_type_catalog_map():
    return {item["slug"]: item for item in QUESTION_TYPE_CATALOG}


def get_question_type_set(slug, set_number):
    for row in QUESTION_TYPE_PRACTICE_SETS.get(slug, []):
        if int(row.get("set_number", 0)) == int(set_number):
            return row
    return None
