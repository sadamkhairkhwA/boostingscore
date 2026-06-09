"""Content for IELTS Practice Test 5 (Advanced).

Exposes three module-level structures consumed by ``papers.py``:

    READING    -> list of 3 passage dicts (40 questions total)
    LISTENING  -> {"minutes": 30, "sections": [4 section dicts]} (40 questions)
    WRITING    -> {"task1": {...}, "task2": {...}}

Only plain Python literals are used here — no imports, no functions.
"""

# ===================== READING =====================
# 3 passages, 40 questions total. Types: tfng, gap, mcq, matching headings.

READING = [
    {
        "number": 1,
        "title": "The first farmers: how plants were tamed",
        "paragraphs": [
            "For more than ninety per cent of the time that anatomically modern humans have existed, people fed themselves by hunting wild animals and gathering wild plants. This way of life was mobile, flexible and, in many environments, surprisingly secure. Then, beginning around eleven thousand years ago in a region of south-west Asia known as the Fertile Crescent, a handful of communities started to do something new. Instead of simply collecting wild seeds, they began to sow them, tend the resulting plants and harvest them deliberately. Over many generations this practice reshaped both the plants and the people who depended on them. The shift from foraging to farming — often called the Neolithic Revolution — was one of the most consequential transitions in human history, even though no one living through it could have recognised it as a revolution at all.",
            "Domestication is more than simply growing a plant in a garden. It refers to the genetic changes that accumulate when humans, rather than nature, control which seeds survive to reproduce. Wild cereals such as einkorn wheat and wild barley have a brittle stalk, or rachis, that shatters when the grain is ripe, scattering seeds across the ground so the plant can propagate. For a forager this is inconvenient, because much of the harvest is lost. Occasionally, however, a mutant plant appears whose rachis does not shatter and whose seeds therefore remain attached. Early farmers, by cutting ripe stands and replanting what they collected, unintentionally favoured exactly these tough-rachised mutants. Within centuries the cultivated cereals had larger seeds, lost their natural means of dispersal and could no longer survive without human assistance.",
            "The Fertile Crescent is an arc of relatively well-watered land stretching from the eastern Mediterranean coast through modern Syria, Turkey and Iraq to the foothills of the Zagros mountains in Iran. It was unusually rich in plant and animal species that happened to be suitable for domestication. Botanists often speak of eight 'founder crops' that were brought under cultivation there: emmer wheat, einkorn wheat, barley, lentils, peas, chickpeas, bitter vetch and flax. The wild ancestors of all eight grew naturally in the region, frequently in dense stands that early peoples already harvested. The same area was home to the wild sheep, goats, cattle and pigs that would later be domesticated, making it a rare place where the full package of farming could assemble.",
            "Why farming began at this particular time and place has been much debated. The end of the last Ice Age brought a warmer, wetter and more stable climate that allowed wild grasses to spread widely. A sharp cold snap known as the Younger Dryas may then have reduced wild food supplies and pushed communities to manage plants more actively. Crucially, the Fertile Crescent offered the right raw materials: a concentration of large-seeded grasses and easily tamed animals that simply did not exist together in many other regions. Agriculture later arose independently in China, Mesoamerica and elsewhere, but the Fertile Crescent provides the earliest and best-documented example.",
            "The consequences of farming reached far beyond the field. A reliable, storable food surplus allowed people to remain in one place, and permanent villages such as those uncovered at Jericho and Çatalhöyük grew steadily in size. Storage of grain created, for the first time, wealth that could be hoarded, inherited and fought over. Populations rose because settled mothers could raise more children than mobile foragers. As villages expanded, not everyone needed to produce food, and specialists — potters, weavers, priests and eventually scribes — emerged. With surplus and specialisation came social hierarchy, organised religion and the administrative structures that would later underpin the world's first cities and states.",
            "Yet the agricultural transition was not unambiguously beneficial for those who lived through it. Skeletal evidence suggests that early farmers were often shorter, less well nourished and more prone to disease than the foragers who preceded them. A diet dominated by a few starchy cereals lacked the variety of a foraged one, and dense settlements living close to animals encouraged the spread of infectious illness. Labour, too, became harder and more repetitive. Some scholars have therefore described the adoption of farming as a kind of trap: each small step raised the population, which made a return to foraging impossible and locked communities ever more tightly into the demanding routines of the farm.",
        ],
        "questions": [
            {"type": "tfng", "id": "t5r1q1", "text": "Hunting and gathering was an insecure way of life in every environment.", "answer": "FALSE"},
            {"type": "tfng", "id": "t5r1q2", "text": "The people living through the shift to farming recognised it as a revolution.", "answer": "FALSE"},
            {"type": "tfng", "id": "t5r1q3", "text": "Cultivated cereals eventually became unable to survive without human help.", "answer": "TRUE"},
            {"type": "tfng", "id": "t5r1q4", "text": "All eight founder crops had wild ancestors that grew in the Fertile Crescent.", "answer": "TRUE"},
            {"type": "tfng", "id": "t5r1q5", "text": "Çatalhöyük had a larger population than Jericho.", "answer": "NOT GIVEN"},
            {"type": "gap", "id": "t5r1q6", "text": "The shift from foraging to farming is often called the Neolithic ____.", "answer": "Revolution"},
            {"type": "gap", "id": "t5r1q7", "text": "The brittle stalk of a wild cereal is known as a ____.", "answer": "rachis"},
            {"type": "gap", "id": "t5r1q8", "text": "A cold period called the Younger ____ may have pushed communities to manage plants.", "answer": "Dryas"},
            {"type": "mcq", "id": "t5r1q9", "text": "According to the passage, what did early farmers unintentionally do?",
             "options": ["Favour plants whose seeds scattered easily", "Favour plants whose seeds stayed attached", "Reduce the size of cereal seeds", "Prevent any genetic change in crops"],
             "answer": "Favour plants whose seeds stayed attached"},
            {"type": "mcq", "id": "t5r1q10", "text": "Which of the following is given as a social consequence of farming?",
             "options": ["The disappearance of religion", "The emergence of specialists such as potters and scribes", "A fall in human population", "An end to social hierarchy"],
             "answer": "The emergence of specialists such as potters and scribes"},
            {"type": "match", "id": "t5r1q11", "text": "Paragraph B",
             "options": ["i  How farming reshaped human society", "ii  What domestication actually involves", "iii  The region where it all began", "iv  Reasons for the timing and location", "v  The hidden costs of the change", "vi  A definition of foraging"],
             "answer": "ii  What domestication actually involves"},
            {"type": "match", "id": "t5r1q12", "text": "Paragraph E",
             "options": ["i  How farming reshaped human society", "ii  What domestication actually involves", "iii  The region where it all began", "iv  Reasons for the timing and location", "v  The hidden costs of the change", "vi  A definition of foraging"],
             "answer": "i  How farming reshaped human society"},
            {"type": "match", "id": "t5r1q13", "text": "Paragraph F",
             "options": ["i  How farming reshaped human society", "ii  What domestication actually involves", "iii  The region where it all began", "iv  Reasons for the timing and location", "v  The hidden costs of the change", "vi  A definition of foraging"],
             "answer": "v  The hidden costs of the change"},
        ],
    },
    {
        "number": 2,
        "title": "The physics of bridges",
        "paragraphs": [
            "A bridge is, at heart, a structure that carries a load across a gap while transferring the weight safely to the ground at either end. However elegant its appearance, every bridge must cope with the same basic forces. The two most important are compression, which squeezes and shortens a material, and tension, which stretches and lengthens it. Stone and concrete are strong in compression but weak in tension; steel cable, by contrast, is superb in tension. The art of bridge design lies in arranging materials so that each is asked to do only what it does best. The three classic families of bridge — beam, arch and suspension — can each be understood as a different solution to the problem of managing these two forces over an ever-greater span.",
            "The beam bridge is the oldest and simplest form: a rigid horizontal deck resting on supports at each end. When a load is placed in the middle, the beam bends. Its upper surface is squeezed in compression while its lower surface is stretched in tension, and the material must resist both. Because a long, unsupported beam sags under its own weight, simple beam bridges are limited to fairly short spans, which is why long beam crossings are broken into many sections carried by a row of piers. Modern box girders and trusses are sophisticated descendants of the humble beam, using clever cross-sections to add stiffness without excessive weight.",
            "The arch bridge solves the span problem in a different way. Its curved shape channels the load outward and downward along the line of the arch, so that the whole structure is held almost entirely in compression. This makes the arch ideal for stone and brick, materials that resist crushing but crack under tension. Roman engineers exploited this principle two thousand years ago, building semicircular stone arches whose aqueducts and bridges still stand today. The thrust at the base of an arch must be resisted by solid abutments or by the rock of a gorge; without firm foundations, the arch will spread and collapse. With them, an arch can carry enormous loads across a wide, deep valley.",
            "For the very longest spans, engineers turn to the suspension bridge, in which the deck hangs from cables draped between tall towers. The main cables are held purely in tension and are anchored firmly into the ground at each end, while the towers carry the resulting downward push in compression. Because high-quality steel cable is extraordinarily strong for its weight, suspension bridges can leap distances no beam or arch could manage. The Golden Gate Bridge in San Francisco spans more than a kilometre between its towers, and Japan's Akashi Kaikyō Bridge stretches almost two kilometres in a single span, demonstrating how far the principle can be pushed.",
            "The history of bridge building is also a history of instructive failures. In 1879 the Tay Bridge in Scotland collapsed in a storm as a train was crossing, killing everyone aboard; investigators concluded that the design had badly underestimated the force of the wind. More famous still is the Tacoma Narrows Bridge in the United States, which in 1940 twisted itself apart only months after opening. A moderate wind set the slender deck oscillating in a phenomenon related to resonance, and the swaying grew until the structure tore itself to pieces — an event captured on film and studied by engineers ever since.",
            "Such disasters transformed the profession. Engineers learned to test designs in wind tunnels, to add stiffening trusses that resist twisting, and to build in generous safety factors so that a structure can bear loads far greater than it will ever meet in service. Redundancy — providing more than one path for forces to travel — means that the failure of a single component need not bring down the whole bridge. The result is that, despite the spectacular collapses of the past, modern bridges are among the safest structures ever built, quietly carrying millions of crossings every day with a reliability their early designers could only have dreamed of.",
        ],
        "questions": [
            {"type": "tfng", "id": "t5r2q1", "text": "Stone is stronger in tension than it is in compression.", "answer": "FALSE"},
            {"type": "tfng", "id": "t5r2q2", "text": "A loaded beam bridge experiences both compression and tension.", "answer": "TRUE"},
            {"type": "tfng", "id": "t5r2q3", "text": "All Roman arch bridges have since been destroyed.", "answer": "FALSE"},
            {"type": "tfng", "id": "t5r2q4", "text": "The Akashi Kaikyō Bridge is the most expensive bridge ever built.", "answer": "NOT GIVEN"},
            {"type": "gap", "id": "t5r2q5", "text": "Steel cable is especially strong in ____.", "answer": "tension"},
            {"type": "gap", "id": "t5r2q6", "text": "The thrust at the base of an arch must be resisted by solid ____.", "answer": "abutments"},
            {"type": "gap", "id": "t5r2q7", "text": "The Tacoma Narrows Bridge failed in a phenomenon related to ____.", "answer": "resonance"},
            {"type": "mcq", "id": "t5r2q8", "text": "Why are simple beam bridges limited to short spans?",
             "options": ["They are too expensive to build", "A long beam sags under its own weight", "They cannot carry trains", "Steel is too weak for them"],
             "answer": "A long beam sags under its own weight"},
            {"type": "mcq", "id": "t5r2q9", "text": "What chiefly holds an arch bridge together structurally?",
             "options": ["Tension in cables", "Compression along its curve", "The weight of the deck alone", "Steel reinforcing bars"],
             "answer": "Compression along its curve"},
            {"type": "mcq", "id": "t5r2q10", "text": "What lesson did engineers draw from past failures?",
             "options": ["Bridges should never cross rivers", "Designs should be tested and given safety factors", "Stone should never be used", "Towers are unnecessary"],
             "answer": "Designs should be tested and given safety factors"},
            {"type": "match", "id": "t5r2q11", "text": "Paragraph B",
             "options": ["i  The bridge that hangs from cables", "ii  The forces every bridge must handle", "iii  Learning from collapse", "iv  The curved design held in compression", "v  The simplest span and its limits", "vi  How modern bridges stay safe"],
             "answer": "v  The simplest span and its limits"},
            {"type": "match", "id": "t5r2q12", "text": "Paragraph D",
             "options": ["i  The bridge that hangs from cables", "ii  The forces every bridge must handle", "iii  Learning from collapse", "iv  The curved design held in compression", "v  The simplest span and its limits", "vi  How modern bridges stay safe"],
             "answer": "i  The bridge that hangs from cables"},
            {"type": "match", "id": "t5r2q13", "text": "Paragraph E",
             "options": ["i  The bridge that hangs from cables", "ii  The forces every bridge must handle", "iii  Learning from collapse", "iv  The curved design held in compression", "v  The simplest span and its limits", "vi  How modern bridges stay safe"],
             "answer": "iii  Learning from collapse"},
        ],
    },
    {
        "number": 3,
        "title": "Memory champions and the art of remembering",
        "paragraphs": [
            "Every year, competitors gather at memory championships to perform feats that look almost superhuman. They memorise the order of a shuffled pack of cards in well under a minute, recall hundreds of random digits after a single reading, and match dozens of names to unfamiliar faces. It would be natural to assume that such people are born with extraordinary brains. Yet when researchers have studied these 'memory athletes', they have generally found that their raw memory, measured in ordinary ways, is no better than anyone else's. What sets them apart is not a gift but a set of techniques — ancient strategies that almost anyone can learn with enough practice.",
            "The most important of these techniques is the method of loci, also known as the memory palace. According to legend, it was devised by the Greek poet Simonides, who, after a banquet hall collapsed, was able to identify the crushed guests by recalling exactly where each had been sitting. The method exploits the fact that human spatial memory — our memory for places and routes — is remarkably powerful and durable. To use it, a person imagines a familiar location, such as their childhood home, and mentally places the items to be remembered at specific points along a route through it. To recall the list, they simply take an imaginary walk and 'collect' the items in order.",
            "The trick that makes the memory palace so effective is the conversion of dull, abstract information into vivid, often bizarre mental images. A shopping list is easy; numbers and playing cards are harder, because they carry no natural picture. Competitors therefore prepare elaborate coding systems in advance. In one popular scheme, known as the Person–Action–Object or PAO system, every two-digit number or card is linked to a particular person doing a particular action with a particular object. Long strings of digits can then be packaged into a handful of striking scenes, each placed at a location in the palace. The stranger and more emotional the image, the more easily the brain holds on to it.",
            "Becoming a champion, however, demands a great deal of training. Studies of memory athletes show that they typically spend many hours each week rehearsing their systems and building ever larger and more detailed palaces. When ordinary volunteers with no special ability were given six weeks of structured practice in these methods, their performance on memory tasks improved dramatically, in some cases approaching competition levels. Brain scans taken before and after revealed no growth in memory-related structures; instead, the trained volunteers had begun to use the brain's spatial-navigation networks in the same way the experts did. The lesson is that the skill rests on practice and strategy, not on inherited talent.",
            "These findings tell us something important about the nature of memory itself. They suggest that the capacity of human memory is far less fixed than it appears, and that the main obstacle to remembering is usually not storage but the way information is encoded. By attaching meaning, imagery and a spatial framework to otherwise meaningless material, the memory athlete makes it 'sticky'. The research also confirms how deeply human memory is tied to place: our brains seem to have evolved to remember where things are, and the method of loci simply borrows that ancient machinery for new purposes.",
            "It would be a mistake, though, to imagine that these techniques turn their users into geniuses. The improvements are strikingly specific: a competitor who can memorise a thousand digits may be no better than average at remembering a friend's birthday or where the car keys were left, unless the method is deliberately applied. Mastering the memory palace does not raise general intelligence, nor does it improve unrelated mental skills. For most people the greatest value of these methods is practical and modest — learning vocabulary, names or the points of a speech — rather than the spectacular but narrow performances seen on the competition stage.",
        ],
        "questions": [
            {"type": "tfng", "id": "t5r3q1", "text": "Memory athletes usually have naturally superior raw memory.", "answer": "FALSE"},
            {"type": "tfng", "id": "t5r3q2", "text": "The method of loci relies on the strength of human spatial memory.", "answer": "TRUE"},
            {"type": "tfng", "id": "t5r3q3", "text": "Simonides identified the banquet victims by recognising their faces.", "answer": "FALSE"},
            {"type": "tfng", "id": "t5r3q4", "text": "Vivid and unusual images are easier to remember than dull ones.", "answer": "TRUE"},
            {"type": "tfng", "id": "t5r3q5", "text": "Memory championships offer large cash prizes to winners.", "answer": "NOT GIVEN"},
            {"type": "gap", "id": "t5r3q6", "text": "The method of loci is also known as the memory ____.", "answer": "palace"},
            {"type": "gap", "id": "t5r3q7", "text": "Numbers and cards can be coded using the Person–Action–____ system.", "answer": "Object"},
            {"type": "gap", "id": "t5r3q8", "text": "After training, volunteers began to use the brain's spatial-____ networks.", "answer": "navigation"},
            {"type": "mcq", "id": "t5r3q9", "text": "What did brain scans of trained volunteers show?",
             "options": ["Growth in memory structures", "No growth, but new use of spatial-navigation networks", "A permanent rise in intelligence", "Damage to the hippocampus"],
             "answer": "No growth, but new use of spatial-navigation networks"},
            {"type": "mcq", "id": "t5r3q10", "text": "According to the passage, the main obstacle to remembering is usually:",
             "options": ["a lack of storage space in the brain", "the way information is encoded", "poor eyesight", "advancing age"],
             "answer": "the way information is encoded"},
            {"type": "mcq", "id": "t5r3q11", "text": "What does the passage say about the benefits of these techniques?",
             "options": ["They raise general intelligence", "They improve all mental skills broadly", "They are specific and do not boost unrelated abilities", "They work only for professional athletes"],
             "answer": "They are specific and do not boost unrelated abilities"},
            {"type": "match", "id": "t5r3q12", "text": "Paragraph B",
             "options": ["i  An old method with a famous origin", "ii  Coding numbers as pictures", "iii  Skill from practice, not birth", "iv  Astonishing feats by ordinary brains", "v  What the research reveals about memory", "vi  The limits of the technique"],
             "answer": "i  An old method with a famous origin"},
            {"type": "match", "id": "t5r3q13", "text": "Paragraph D",
             "options": ["i  An old method with a famous origin", "ii  Coding numbers as pictures", "iii  Skill from practice, not birth", "iv  Astonishing feats by ordinary brains", "v  What the research reveals about memory", "vi  The limits of the technique"],
             "answer": "iii  Skill from practice, not birth"},
            {"type": "match", "id": "t5r3q14", "text": "Paragraph F",
             "options": ["i  An old method with a famous origin", "ii  Coding numbers as pictures", "iii  Skill from practice, not birth", "iv  Astonishing feats by ordinary brains", "v  What the research reveals about memory", "vi  The limits of the technique"],
             "answer": "vi  The limits of the technique"},
        ],
    },
]


# ===================== LISTENING =====================
# 4 sections × 10 questions = 40. Each section: ~7 gap + ~3 mcq.

LISTENING = {
    "minutes": 30,
    "sections": [
        {
            "number": 1,
            "title": "Section 1 — Making a hotel reservation",
            "instructions": "Questions 1–10. Complete the notes and answer the multiple-choice questions. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each gap.",
            "audio": "test5_s1.mp3",
            "questions": [
                {"type": "gap", "id": "t5l1q1", "text": "Guest's surname (spelled out as H-A-R-T-L-E-Y): ____", "answer": "Hartley"},
                {"type": "gap", "id": "t5l1q2", "text": "Room required: a ____ room with a sea view.", "answer": "double"},
                {"type": "gap", "id": "t5l1q3", "text": "Number of nights booked: ____", "answer": "three"},
                {"type": "gap", "id": "t5l1q4", "text": "Arrival date: the 12th of ____.", "answer": "April"},
                {"type": "gap", "id": "t5l1q5", "text": "Price per night: £____", "answer": "110"},
                {"type": "gap", "id": "t5l1q6", "text": "Breakfast is served in the ____ until 10 a.m.", "answer": "conservatory"},
                {"type": "gap", "id": "t5l1q7", "text": "From the airport the hotel can arrange ____.", "answer": "a taxi"},
                {"type": "mcq", "id": "t5l1q8", "text": "How will the guest pay for the room?",
                 "options": ["A  By cash on arrival", "B  By credit card now", "C  By bank transfer later"],
                 "answer": "B  By credit card now"},
                {"type": "mcq", "id": "t5l1q9", "text": "Which extra does the guest add to the booking?",
                 "options": ["A  Airport parking", "B  An evening meal", "C  A cot for a child"],
                 "answer": "C  A cot for a child"},
                {"type": "mcq", "id": "t5l1q10", "text": "What is the hotel's cancellation policy?",
                 "options": ["A  Free up to 24 hours before arrival", "B  Free up to 48 hours before arrival", "C  No refunds at any time"],
                 "answer": "A  Free up to 24 hours before arrival"},
            ],
        },
        {
            "number": 2,
            "title": "Section 2 — The refurbished community centre",
            "instructions": "Questions 11–20. Complete the notes and answer the multiple-choice questions. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each gap.",
            "audio": "test5_s2.mp3",
            "questions": [
                {"type": "gap", "id": "t5l2q1", "text": "The community centre will reopen in the month of ____.", "answer": "May"},
                {"type": "gap", "id": "t5l2q2", "text": "A new ____ pool has been added on the ground floor.", "answer": "swimming"},
                {"type": "gap", "id": "t5l2q3", "text": "The main hall can now seat up to ____ people.", "answer": "200"},
                {"type": "gap", "id": "t5l2q4", "text": "The ____ studio offers yoga and dance classes.", "answer": "fitness"},
                {"type": "gap", "id": "t5l2q5", "text": "The café on the first floor sells locally grown ____.", "answer": "vegetables"},
                {"type": "gap", "id": "t5l2q6", "text": "Children's art classes take place every ____ morning.", "answer": "Saturday"},
                {"type": "gap", "id": "t5l2q7", "text": "Annual membership for adults costs £____.", "answer": "45"},
                {"type": "mcq", "id": "t5l2q8", "text": "What time does the centre close on weekdays?",
                 "options": ["A  8 p.m.", "B  9 p.m.", "C  10 p.m."],
                 "answer": "B  9 p.m."},
                {"type": "mcq", "id": "t5l2q9", "text": "Who can use the centre free of charge?",
                 "options": ["A  University students", "B  Children under five", "C  Residents over 65"],
                 "answer": "C  Residents over 65"},
                {"type": "mcq", "id": "t5l2q10", "text": "How should people book a class?",
                 "options": ["A  By telephone", "B  Through the website", "C  In person at reception"],
                 "answer": "B  Through the website"},
            ],
        },
        {
            "number": 3,
            "title": "Section 3 — Designing a transport survey",
            "instructions": "Questions 21–30. Complete the notes and answer the multiple-choice questions. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each gap.",
            "audio": "test5_s3.mp3",
            "questions": [
                {"type": "gap", "id": "t5l3q1", "text": "The survey will focus on students' use of ____ transport.", "answer": "public"},
                {"type": "gap", "id": "t5l3q2", "text": "They plan to collect a sample of ____ responses.", "answer": "300"},
                {"type": "gap", "id": "t5l3q3", "text": "Data will mainly be gathered using an online ____.", "answer": "questionnaire"},
                {"type": "gap", "id": "t5l3q4", "text": "They will also conduct a few face-to-face ____.", "answer": "interviews"},
                {"type": "gap", "id": "t5l3q5", "text": "The pilot study will run for one ____.", "answer": "week"},
                {"type": "gap", "id": "t5l3q6", "text": "The final report must be submitted in ____.", "answer": "December"},
                {"type": "gap", "id": "t5l3q7", "text": "The tutor suggests adding a question about ____ costs.", "answer": "travel"},
                {"type": "mcq", "id": "t5l3q8", "text": "What is the main aim of the survey?",
                 "options": ["A  To reduce traffic on campus", "B  To understand how students travel to campus", "C  To compare bus and train prices"],
                 "answer": "B  To understand how students travel to campus"},
                {"type": "mcq", "id": "t5l3q9", "text": "Why do the students reject a paper survey?",
                 "options": ["A  It is too expensive to print", "B  It is slower to analyse", "C  Students dislike using paper"],
                 "answer": "B  It is slower to analyse"},
                {"type": "mcq", "id": "t5l3q10", "text": "What does the tutor warn the students about?",
                 "options": ["A  Asking leading questions", "B  Surveying too many people", "C  Finishing the project too early"],
                 "answer": "A  Asking leading questions"},
            ],
        },
        {
            "number": 4,
            "title": "Section 4 — Volcanic soils and agriculture",
            "instructions": "Questions 31–40. Complete the notes and answer the multiple-choice questions. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each gap.",
            "audio": "test5_s4.mp3",
            "questions": [
                {"type": "gap", "id": "t5l4q1", "text": "Soils formed from volcanic ash are scientifically called ____.", "answer": "andisols"},
                {"type": "gap", "id": "t5l4q2", "text": "Volcanic ash weathers quickly to release valuable ____.", "answer": "minerals"},
                {"type": "gap", "id": "t5l4q3", "text": "These soils are especially rich in ____ and potassium.", "answer": "phosphorus"},
                {"type": "gap", "id": "t5l4q4", "text": "Their crumbly structure holds both water and ____ well.", "answer": "air"},
                {"type": "gap", "id": "t5l4q5", "text": "Many of Indonesia's farms lie on the island of ____.", "answer": "Java"},
                {"type": "gap", "id": "t5l4q6", "text": "A major risk is that an ____ can destroy crops without warning.", "answer": "eruption"},
                {"type": "gap", "id": "t5l4q7", "text": "Volcanic regions also face the danger of ____ flows.", "answer": "pyroclastic"},
                {"type": "mcq", "id": "t5l4q8", "text": "Why are volcanic soils so fertile?",
                 "options": ["A  They contain a great deal of clay", "B  Weathered ash releases minerals plants need", "C  They never require watering"],
                 "answer": "B  Weathered ash releases minerals plants need"},
                {"type": "mcq", "id": "t5l4q9", "text": "What is the main drawback of farming near volcanoes?",
                 "options": ["A  The soil is too acidic", "B  The constant risk of eruptions", "C  Crops grow too slowly"],
                 "answer": "B  The constant risk of eruptions"},
                {"type": "mcq", "id": "t5l4q10", "text": "Which region does the lecturer give as a key example?",
                 "options": ["A  The Sahara Desert", "B  The slopes of Mount Etna", "C  The Arctic tundra"],
                 "answer": "B  The slopes of Mount Etna"},
            ],
        },
    ],
}


# Use the richer IELTS-style listening set (map labelling, matching, tables,
# form/note/sentence completion and MCQ) while keeping Reading/Writing intact.
from .listening_variety import TEST5_LISTENING as LISTENING


# ===================== WRITING =====================

WRITING = {
    "task1": {
        "kind": "task1",
        "title": "Writing — Task 1",
        "minutes": 20,
        "min_words": 150,
        "instructions": (
            "The two maps below show the centre of Maple Town as it was in 1990 "
            "and as it is today. They show how land beside the High Street and the "
            "river has changed, with a factory, a park, houses and small shops "
            "being replaced by flats, a shopping centre, a car park and new roads. "
            "Summarise the information by selecting and reporting the main "
            "features, and make comparisons where relevant."
        ),
        "chart_svg": """
<svg viewBox="0 0 520 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Two maps of Maple Town centre in 1990 and today">
  <style>
    .panel{ fill:#f7f9f7; stroke:#9aa3af; stroke-width:1.5; }
    .road{ stroke:#c69a4d; stroke-width:8; fill:none; stroke-linecap:round; }
    .roadline{ stroke:#ffffff; stroke-width:1; stroke-dasharray:4 4; fill:none; }
    .river{ stroke:#6db3e8; stroke-width:7; fill:none; stroke-linecap:round; }
    .bldg{ fill:#cdd6e3; stroke:#5b6675; stroke-width:1; }
    .green{ fill:#bfe0a8; stroke:#6f9a55; stroke-width:1; }
    .lot{ fill:#e4e7ea; stroke:#8b94a1; stroke-width:1; }
    .lab{ font: 600 9px 'Segoe UI', Arial, sans-serif; fill:#26303f; }
    .ttl{ font: 700 12px 'Segoe UI', Arial, sans-serif; fill:#1a1f2b; }
  </style>

  <!-- ===== 1990 (left) ===== -->
  <text x="14" y="18" class="ttl">Maple Town centre — 1990</text>
  <rect x="12" y="26" width="238" height="220" class="panel"/>
  <path d="M30 26 C 42 90, 18 150, 36 246" class="river"/>
  <text x="40" y="240" class="lab">River Maple</text>
  <path d="M12 150 H250" class="road"/>
  <path d="M12 150 H250" class="roadline"/>
  <text x="186" y="145" class="lab">High Street</text>
  <rect x="150" y="42" width="86" height="80" class="green"/>
  <text x="178" y="86" class="lab">park</text>
  <rect x="62" y="60" width="60" height="56" class="bldg"/>
  <text x="74" y="92" class="lab">houses</text>
  <rect x="62" y="176" width="120" height="54" class="bldg"/>
  <text x="98" y="206" class="lab">factory</text>

  <!-- ===== Today (right) ===== -->
  <text x="290" y="18" class="ttl">Maple Town centre — today</text>
  <rect x="272" y="26" width="238" height="220" class="panel"/>
  <path d="M290 26 C 302 90, 278 150, 296 246" class="river"/>
  <text x="300" y="240" class="lab">River Maple</text>
  <path d="M272 150 H510" class="road"/>
  <path d="M272 150 H510" class="roadline"/>
  <text x="446" y="145" class="lab">High Street</text>
  <path d="M392 150 V246" class="road"/>
  <path d="M392 150 V246" class="roadline"/>
  <text x="396" y="200" class="lab">Mill Road</text>
  <rect x="410" y="42" width="86" height="80" class="bldg"/>
  <text x="416" y="86" class="lab">shopping centre</text>
  <rect x="322" y="60" width="60" height="56" class="bldg"/>
  <text x="334" y="92" class="lab">flats</text>
  <rect x="322" y="176" width="120" height="54" class="lot"/>
  <text x="356" y="206" class="lab">car park</text>
</svg>
""",
    },
    "task2": {
        "kind": "task2",
        "title": "Writing — Task 2",
        "minutes": 40,
        "min_words": 250,
        "instructions": (
            "Some people believe that modern technology is reducing people's "
            "ability to communicate with each other face to face. To what extent "
            "do you agree or disagree? Give reasons for your answer and include "
            "any relevant examples from your own knowledge or experience."
        ),
    },
}
