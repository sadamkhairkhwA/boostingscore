"""Content for IELTS Practice Test 4.

Module-level data only (plain Python literals), matching the shapes used by
``papers.py``:

    READING    -> list of 3 passage dicts (40 questions total)
    LISTENING  -> {"minutes": 30, "sections": [4 section dicts]} (40 questions)
    WRITING    -> {"task1": {...}, "task2": {...}}
"""

# ============================================================================
#  READING  — 3 passages, 40 questions total
# ============================================================================

READING = [
    {
        "number": 1,
        "title": "The science of taste and flavour",
        "paragraphs": [
            "Most people use the words ‘taste’ and ‘flavour’ as if they meant the same thing, but scientists draw a careful distinction between them. Taste, strictly speaking, refers only to the sensations produced when chemicals in food dissolve in saliva and stimulate the taste buds on the tongue and the roof of the mouth. Flavour is a far richer experience: it is the brain’s combined interpretation of taste, smell, texture, temperature and even sound. When researchers say that flavour is ‘multisensory’, they mean that the enjoyment of a meal draws on almost every sense at once, with the nose doing a surprising amount of the work that most diners credit to the tongue.",
            "For a long time, textbooks claimed that the tongue was divided into zones, each responsible for a single taste — sweetness at the tip, bitterness at the back, and so on. This famous ‘tongue map’ has since been shown to be a misreading of older research. In reality, taste buds capable of detecting all the basic tastes are spread across the whole surface of the tongue. Today most scientists recognise five basic tastes: sweet, salty, sour, bitter and umami, the last of these being a savoury sensation associated with glutamate and first described by a Japanese chemist in 1908. Some researchers argue that the body may also detect fat and certain metallic compounds as additional basic tastes, though this remains a matter of debate.",
            "Each basic taste is thought to carry an evolutionary message. Sweetness signals the presence of energy-rich sugars, while saltiness points to minerals the body needs to regulate fluids. Sourness can warn that fruit is unripe or that food has begun to spoil, and bitterness is widely interpreted as a caution against potential toxins, which may explain why many children reject vegetables that adults learn to enjoy. Umami, meanwhile, indicates the presence of protein. Seen in this light, the sense of taste is less a source of pleasure than an ancient chemical alarm system that helped our ancestors decide what was safe to swallow.",
            "Yet taste alone accounts for only a small part of what we experience as flavour. The dominant contributor is smell, and in particular a process known as retronasal olfaction. When we chew, volatile molecules released from the food travel upwards from the back of the mouth into the nasal cavity, where they reach the olfactory receptors. This is quite different from sniffing a dish before eating it, which is called orthonasal smell. A simple demonstration makes the point: if you hold your nose while eating a jellybean, you may register only sweetness, but the moment you release your nose the specific fruit flavour suddenly appears. People who lose their sense of smell, whether through illness or injury, often report that food has become disappointingly bland, even though their taste buds remain perfectly intact.",
            "Beyond smell, the brain folds in a stream of other information before it decides how something tastes. Texture matters enormously: the same tomato soup is judged creamier when it is thicker, and crisps are rated as fresher when they make a louder crunch. Temperature alters perceived sweetness, which is why melted ice cream can taste cloying while the frozen version seems balanced. Even colour and the weight of the cutlery have measurable effects. In one well-known study, a dessert served on a white plate was rated as sweeter than the identical dessert served on a black plate, and wine has been judged as more expensive simply because a higher price was displayed beside it. Such findings show that flavour is not a fixed property of the food itself but a construction assembled by the mind.",
            "Individuals also differ markedly in how intensely they experience taste. So-called ‘supertasters’ possess an unusually high density of taste buds and tend to find bitter foods, strong coffee and even some leafy greens overpowering, whereas ‘non-tasters’ may need far stronger seasoning to register the same intensity. These differences are partly genetic and help explain why members of the same family can disagree so sharply about whether a dish is delicious or unpleasant.",
            "Understanding flavour as a multisensory construction has practical consequences. Food companies now design products with the crunch, colour and aroma of a snack in mind, not merely its chemical taste, and chefs increasingly manipulate expectation, plating and even background music to shape how a meal is received. For people whose sense of smell has faded with age or illness, the same science offers hope: dishes can be redesigned around texture, temperature and visual appeal to restore some of the pleasure that a weakened nose would otherwise remove.",
        ],
        "questions": [
            {"type": "tfng", "id": "t4r1q1", "text": "Scientists use the words ‘taste’ and ‘flavour’ to mean exactly the same thing.", "answer": "FALSE"},
            {"type": "tfng", "id": "t4r1q2", "text": "The ‘tongue map’ showing separate zones for each taste is now considered inaccurate.", "answer": "TRUE"},
            {"type": "tfng", "id": "t4r1q3", "text": "Umami was first described by a researcher working in Japan.", "answer": "TRUE"},
            {"type": "tfng", "id": "t4r1q4", "text": "All scientists agree that fat should be classified as a sixth basic taste.", "answer": "FALSE"},
            {"type": "tfng", "id": "t4r1q5", "text": "Supertasters are more common in cold climates than in warm ones.", "answer": "NOT GIVEN"},
            {"type": "gap", "id": "t4r1q6", "text": "The savoury taste linked to glutamate is known as ____.", "answer": "umami"},
            {"type": "gap", "id": "t4r1q7", "text": "When we chew, smell molecules reach the nose through a process called ____ olfaction.", "answer": "retronasal"},
            {"type": "gap", "id": "t4r1q8", "text": "People who lose their sense of smell often complain that food tastes ____.", "answer": "bland"},
            {"type": "mcq", "id": "t4r1q9", "text": "According to the passage, bitterness probably evolved to warn us about",
             "options": ["a lack of minerals", "possible toxins", "unripe fruit", "high-energy sugars"],
             "answer": "possible toxins"},
            {"type": "mcq", "id": "t4r1q10", "text": "The jellybean example is used to show that",
             "options": ["sweetness is the strongest taste", "smell contributes greatly to flavour", "colour changes how food tastes", "texture affects freshness"],
             "answer": "smell contributes greatly to flavour"},
            {"type": "mcq", "id": "t4r1q11", "text": "Which factor is NOT mentioned as influencing how food is perceived?",
             "options": ["the colour of the plate", "the loudness of a crunch", "the time of day", "the displayed price"],
             "answer": "the time of day"},
            {"type": "match", "id": "t4r1q12", "text": "Paragraph 4 (beginning ‘Yet taste alone…’)",
             "options": [
                 "i  Why each taste may have evolved",
                 "ii  The leading role of smell in flavour",
                 "iii  Practical uses of flavour science",
                 "iv  Differences between individuals",
                 "v  Correcting an old myth about the tongue",
                 "vi  How other senses shape what we taste",
             ],
             "answer": "ii  The leading role of smell in flavour"},
            {"type": "match", "id": "t4r1q13", "text": "Paragraph 5 (beginning ‘Beyond smell…’)",
             "options": [
                 "i  Why each taste may have evolved",
                 "ii  The leading role of smell in flavour",
                 "iii  Practical uses of flavour science",
                 "iv  Differences between individuals",
                 "v  Correcting an old myth about the tongue",
                 "vi  How other senses shape what we taste",
             ],
             "answer": "vi  How other senses shape what we taste"},
        ],
    },
    {
        "number": 2,
        "title": "Roman roads and the engineering of empire",
        "paragraphs": [
            "At its height, the Roman Empire was bound together by a network of paved roads that stretched for some 80,000 kilometres, linking the cold frontiers of northern Britain with the deserts of the Near East. These roads were far more than convenient routes between towns. They were instruments of power: they allowed legions to march swiftly to trouble spots, enabled officials and messengers to move information across vast distances, and knitted distant provinces into a single economic and administrative system. The Roman saying that ‘all roads lead to Rome’ captured a literal truth, for the entire network was conceived as radiating outward from the capital.",
            "What set Roman roads apart from those of earlier civilisations was the quality of their construction. Rather than simply clearing a track, Roman engineers built up the road in carefully prepared layers. First a trench was dug and the soft topsoil removed down to firm ground. Into this foundation they laid a course of large stones, followed by a layer of smaller stones or gravel bound with lime mortar, and sometimes a further bed of sand or fine gravel. The visible surface was often made of tightly fitted paving stones or compacted gravel, raised in a gentle curve known as a camber so that rainwater would drain off into ditches dug along each side. A well-built road could therefore stay usable in conditions that would have turned an ordinary track into mud.",
            "Equally impressive was the Roman commitment to building roads as straight as the landscape allowed. Surveyors, using a simple sighting instrument called a groma, would establish a line between two points and drive the road towards its destination with remarkable determination, cutting through hills and bridging valleys rather than meandering around obstacles. This preference for the direct route reflected military priorities: the shortest path meant the fastest march. Where mountains or marshes made a straight line impossible, the engineers were perfectly willing to compromise, but the underlying ambition was always speed and directness.",
            "Maintaining the network was a serious administrative undertaking. Milestones, inscribed stone pillars set at regular intervals, told travellers how far they were from the next town and often recorded which emperor had ordered repairs. Alongside the major routes, the state operated a relay system of staging posts where official couriers could change horses and rest, allowing urgent messages to travel at speeds that would not be matched in Europe for well over a thousand years. Ordinary travellers, traders and pilgrims used the same roads, so that goods, ideas, languages and even diseases spread along them with unprecedented ease.",
            "The roads also reshaped the economy of the provinces. Heavy goods such as grain, wine, oil and building stone could be moved overland far more reliably than before, and towns naturally grew up at junctions and river crossings. Some historians caution, however, that road transport remained expensive compared with shipping by sea or river; for very heavy or bulky cargo, water routes were still preferred wherever they existed. The roads were most valuable for moving people, official correspondence and high-value goods quickly and predictably, rather than for replacing waterborne trade altogether.",
            "It is a striking testament to Roman engineering that many of these routes are still in use today, often hidden beneath modern highways that follow the original alignments. In Britain, several major roads trace lines first laid down by Roman surveyors, and across Europe the Latin names of old routes survive in local place names. Stretches of original paving can still be walked in Italy and the eastern Mediterranean. The endurance of these roads owes much to the layered construction and careful drainage that protected them from the freeze-and-thaw cycles and standing water that destroy lesser surfaces. More than the monuments of the capital, it may be these unglamorous strips of stone that best reveal how the Romans turned a collection of conquered territories into a working empire.",
        ],
        "questions": [
            {"type": "tfng", "id": "t4r2q1", "text": "The Roman road network was designed to spread outward from the capital.", "answer": "TRUE"},
            {"type": "tfng", "id": "t4r2q2", "text": "Roman roads were built simply by clearing a track across the ground.", "answer": "FALSE"},
            {"type": "tfng", "id": "t4r2q3", "text": "The camber of a Roman road helped rainwater drain away.", "answer": "TRUE"},
            {"type": "tfng", "id": "t4r2q4", "text": "Roman surveyors always avoided hills by building roads around them.", "answer": "FALSE"},
            {"type": "tfng", "id": "t4r2q5", "text": "Roman couriers could travel faster than any messengers in Europe for centuries afterwards.", "answer": "TRUE"},
            {"type": "gap", "id": "t4r2q6", "text": "The total Roman road network covered roughly ____ kilometres.", "answer": "80,000"},
            {"type": "gap", "id": "t4r2q7", "text": "Surveyors set out a straight line using a sighting tool called a ____.", "answer": "groma"},
            {"type": "gap", "id": "t4r2q8", "text": "Inscribed pillars known as ____ recorded distances and repairs.", "answer": "milestones"},
            {"type": "mcq", "id": "t4r2q9", "text": "The main purpose of building roads in straight lines was to",
             "options": ["save money on stone", "allow faster military movement", "avoid private land", "make surveying easier"],
             "answer": "allow faster military movement"},
            {"type": "mcq", "id": "t4r2q10", "text": "What do some historians point out about Roman road transport?",
             "options": ["It was cheaper than sea transport", "It was unreliable in winter", "It was costly compared with water transport", "It was used only by the army"],
             "answer": "It was costly compared with water transport"},
            {"type": "mcq", "id": "t4r2q11", "text": "According to the final paragraph, the survival of Roman roads is mainly due to",
             "options": ["their decorative paving", "their layered construction and drainage", "constant rebuilding by later rulers", "the mild European climate"],
             "answer": "their layered construction and drainage"},
            {"type": "match", "id": "t4r2q12", "text": "Paragraph 2 (beginning ‘What set Roman roads apart…’)",
             "options": [
                 "i  Roads as tools of imperial power",
                 "ii  The layered method of construction",
                 "iii  A preference for straight routes",
                 "iv  Running and maintaining the network",
                 "v  Effects on trade and the economy",
                 "vi  A legacy that endures today",
             ],
             "answer": "ii  The layered method of construction"},
            {"type": "match", "id": "t4r2q13", "text": "Paragraph 5 (beginning ‘The roads also reshaped…’)",
             "options": [
                 "i  Roads as tools of imperial power",
                 "ii  The layered method of construction",
                 "iii  A preference for straight routes",
                 "iv  Running and maintaining the network",
                 "v  Effects on trade and the economy",
                 "vi  A legacy that endures today",
             ],
             "answer": "v  Effects on trade and the economy"},
        ],
    },
    {
        "number": 3,
        "title": "Artificial intelligence in medical diagnosis",
        "paragraphs": [
            "Few areas of medicine have attracted as much excitement in recent years as the use of artificial intelligence to help diagnose disease. The branch of AI responsible for most of this progress is machine learning, in which a computer system is shown very large numbers of examples and gradually learns to recognise the patterns that distinguish one category from another. When applied to medical images — X-rays, retinal scans, slides of tissue or photographs of skin — such systems can be trained to flag the subtle visual signs of illness, sometimes detecting features that are difficult for the human eye to perceive.",
            "The results in narrow tasks have been remarkable. Trained on hundreds of thousands of labelled images, some systems can identify diabetic damage to the retina, or pick out suspicious nodules on a lung scan, with an accuracy that rivals or even exceeds that of experienced specialists. Because a computer never tires and can examine an image in a fraction of a second, supporters argue that AI could bring expert-level screening to regions of the world where trained radiologists and pathologists are in critically short supply. A clinic with a camera and an internet connection might, in principle, gain access to diagnostic skill that would otherwise be unavailable.",
            "The potential benefits go beyond simply matching human performance. AI systems can work tirelessly through enormous backlogs of routine scans, freeing specialists to concentrate on complex or ambiguous cases. They can act as a safety net, drawing a doctor’s attention to an easily missed detail in a busy clinic. In some studies, the best outcomes have come not from the machine or the clinician working alone, but from the two working together, with the algorithm offering a second opinion that the human expert is free to accept or overrule.",
            "These successes, however, come with important limitations. A machine-learning system is only as good as the data it was trained on, and if those data are not representative of the patients it later encounters, its performance can fall sharply. A model trained mainly on images from one hospital, one type of scanner or one population may make systematic errors when used elsewhere. Skin-cancer detectors trained largely on lighter skin, for instance, have proved less reliable on darker skin, raising serious concerns about fairness. Models can also latch on to irrelevant clues — learning, say, that images containing a ruler are more likely to show a tumour simply because doctors tend to place a ruler beside lesions they already suspect.",
            "A further and much-discussed difficulty is the ‘black box’ problem. Many of the most powerful systems cannot easily explain why they reached a particular conclusion; they output a probability without showing their reasoning in a way a clinician can inspect. This opacity is troubling in medicine, where a doctor may need to justify a decision to a patient, a colleague or a court. If an algorithm recommends an invasive procedure, both physician and patient may reasonably want to know on what grounds. Researchers are actively developing methods to make these systems more transparent, but progress has been uneven and there is as yet no complete solution.",
            "The ethical questions extend further still. Who is responsible when an AI system makes a mistake — the doctor who relied on it, the hospital that bought it, or the company that built it? How should the vast quantities of sensitive patient data needed to train these models be collected, stored and protected? And there is a subtler worry that clinicians who lean too heavily on automated tools may, over time, allow their own diagnostic skills to erode, a phenomenon sometimes called automation bias. Regulators in several countries have begun approving AI tools for clinical use, but most insist that the technology support rather than replace human judgement.",
            "For all these caveats, few experts doubt that artificial intelligence will play a growing part in diagnosis. The most plausible future is not one in which machines replace doctors, but one in which they become a routine instrument of the clinic, much as the stethoscope or the blood test did before them. Realising that promise safely will depend less on raw computing power than on careful attention to the quality of data, the transparency of decisions and the clear allocation of responsibility when things go wrong.",
        ],
        "questions": [
            {"type": "tfng", "id": "t4r3q1", "text": "Machine learning systems improve by being shown large numbers of examples.", "answer": "TRUE"},
            {"type": "tfng", "id": "t4r3q2", "text": "AI systems have completely replaced human radiologists in most hospitals.", "answer": "FALSE"},
            {"type": "tfng", "id": "t4r3q3", "text": "Some AI image systems can match or beat specialists at narrow diagnostic tasks.", "answer": "TRUE"},
            {"type": "tfng", "id": "t4r3q4", "text": "AI diagnostic tools are now equally accurate for every patient population.", "answer": "FALSE"},
            {"type": "tfng", "id": "t4r3q5", "text": "Combining a clinician with an algorithm has sometimes produced the best results.", "answer": "TRUE"},
            {"type": "gap", "id": "t4r3q6", "text": "Most recent progress comes from a branch of AI called ____ learning.", "answer": "machine"},
            {"type": "gap", "id": "t4r3q7", "text": "An AI system is only as good as the ____ it was trained on.", "answer": "data"},
            {"type": "gap", "id": "t4r3q8", "text": "The difficulty of understanding an AI's reasoning is called the ____ box problem.", "answer": "black"},
            {"type": "gap", "id": "t4r3q9", "text": "Over-reliance on automated tools may cause an erosion of clinicians' diagnostic ____.", "answer": "skills"},
            {"type": "mcq", "id": "t4r3q10", "text": "The example of the ruler beside a lesion illustrates that AI may",
             "options": ["work faster than doctors", "learn from irrelevant clues", "need expensive cameras", "explain its reasoning clearly"],
             "answer": "learn from irrelevant clues"},
            {"type": "mcq", "id": "t4r3q11", "text": "Why is the 'black box' problem especially serious in medicine?",
             "options": ["Scans take too long to read", "Doctors may need to justify decisions", "Computers are too slow", "Patients dislike technology"],
             "answer": "Doctors may need to justify decisions"},
            {"type": "mcq", "id": "t4r3q12", "text": "What do most regulators currently require of medical AI?",
             "options": ["that it replace doctors entirely", "that it support human judgement", "that it be used only in research", "that it work without any data"],
             "answer": "that it support human judgement"},
            {"type": "match", "id": "t4r3q13", "text": "Paragraph 4 (beginning ‘These successes, however…’)",
             "options": [
                 "i  How machine learning reads medical images",
                 "ii  Matching or beating specialists",
                 "iii  Benefits beyond raw accuracy",
                 "iv  When training data lets a model down",
                 "v  The problem of unexplained decisions",
                 "vi  Responsibility, privacy and other ethics",
             ],
             "answer": "iv  When training data lets a model down"},
            {"type": "match", "id": "t4r3q14", "text": "Paragraph 6 (beginning ‘The ethical questions…’)",
             "options": [
                 "i  How machine learning reads medical images",
                 "ii  Matching or beating specialists",
                 "iii  Benefits beyond raw accuracy",
                 "iv  When training data lets a model down",
                 "v  The problem of unexplained decisions",
                 "vi  Responsibility, privacy and other ethics",
             ],
             "answer": "vi  Responsibility, privacy and other ethics"},
        ],
    },
]


# ============================================================================
#  LISTENING  — 4 sections, 10 questions each (40 total)
# ============================================================================

LISTENING = {
    "minutes": 30,
    "sections": [
        {
            "number": 1,
            "title": "Section 1 — Enrolling in an evening course",
            "instructions": "Questions 1–10. Listen to a conversation between a man and a receptionist at a community learning centre and answer the questions below. Write ONE WORD AND/OR A NUMBER for the gap-fill questions, and choose the correct letter for the multiple-choice questions.",
            "audio": "test4_s1.mp3",
            "questions": [
                {"type": "gap", "id": "t4l1q1", "text": "The caller's full name is Daniel ____.", "answer": "Foster"},
                {"type": "mcq", "id": "t4l1q2", "text": "Which course does the man finally decide to enrol in?",
                 "options": ["A  Beginner Italian", "B  Thai cookery", "C  Digital photography"],
                 "answer": "B  Thai cookery"},
                {"type": "gap", "id": "t4l1q3", "text": "The class takes place every ____ evening.", "answer": "Wednesday"},
                {"type": "gap", "id": "t4l1q4", "text": "Lessons run from 7 p.m. until ____ p.m.", "answer": "9"},
                {"type": "gap", "id": "t4l1q5", "text": "The course lasts for a total of ____ weeks.", "answer": "ten"},
                {"type": "mcq", "id": "t4l1q6", "text": "How much is the full course fee?",
                 "options": ["A  £95", "B  £120", "C  £150"],
                 "answer": "B  £120"},
                {"type": "gap", "id": "t4l1q7", "text": "Students must bring their own ____ to each lesson.", "answer": "apron"},
                {"type": "gap", "id": "t4l1q8", "text": "All other ingredients and equipment are provided in the ____.", "answer": "kitchen"},
                {"type": "mcq", "id": "t4l1q9", "text": "What discount is available to the caller?",
                 "options": ["A  a student discount", "B  an early-booking discount", "C  a senior discount"],
                 "answer": "B  an early-booking discount"},
                {"type": "gap", "id": "t4l1q10", "text": "To confirm his place, the man must pay a deposit by ____.", "answer": "Friday"},
            ],
        },
        {
            "number": 2,
            "title": "Section 2 — A ranger's guided walk",
            "instructions": "Questions 11–20. Listen to a park ranger introducing a guided walk at a nature reserve and answer the questions below. Write ONE WORD AND/OR A NUMBER for the gap-fill questions, and choose the correct letter for the multiple-choice questions.",
            "audio": "test4_s2.mp3",
            "questions": [
                {"type": "gap", "id": "t4l2q1", "text": "The full guided walk takes about ____ hours.", "answer": "two"},
                {"type": "mcq", "id": "t4l2q2", "text": "Where does the walk begin?",
                 "options": ["A  at the car park", "B  at the visitor centre", "C  at the lake"],
                 "answer": "B  at the visitor centre"},
                {"type": "gap", "id": "t4l2q3", "text": "The first part of the trail passes through an area of ancient ____.", "answer": "woodland"},
                {"type": "gap", "id": "t4l2q4", "text": "Visitors are most likely to spot ____ near the lake in the early morning.", "answer": "deer"},
                {"type": "mcq", "id": "t4l2q5", "text": "Which bird is the reserve especially famous for?",
                 "options": ["A  the kingfisher", "B  the heron", "C  the woodpecker"],
                 "answer": "A  the kingfisher"},
                {"type": "gap", "id": "t4l2q6", "text": "For the best views, walkers should climb the wooden ____ on the hill.", "answer": "tower"},
                {"type": "gap", "id": "t4l2q7", "text": "Visitors must keep all ____ on a lead at all times.", "answer": "dogs"},
                {"type": "gap", "id": "t4l2q8", "text": "Walkers should not pick any ____ or remove plants from the reserve.", "answer": "flowers"},
                {"type": "mcq", "id": "t4l2q9", "text": "What should visitors do if it starts to rain heavily?",
                 "options": ["A  return to the car park", "B  shelter in the bird hide", "C  continue to the lake"],
                 "answer": "B  shelter in the bird hide"},
                {"type": "gap", "id": "t4l2q10", "text": "The ranger advises everyone to carry a bottle of ____.", "answer": "water"},
            ],
        },
        {
            "number": 3,
            "title": "Section 3 — Planning a group project",
            "instructions": "Questions 21–30. Listen to two students, Maya and Tom, discussing a group project on sustainable architecture and answer the questions below. Write ONE WORD AND/OR A NUMBER for the gap-fill questions, and choose the correct letter for the multiple-choice questions.",
            "audio": "test4_s3.mp3",
            "questions": [
                {"type": "gap", "id": "t4l3q1", "text": "The project is for their module on sustainable ____.", "answer": "architecture"},
                {"type": "mcq", "id": "t4l3q2", "text": "What is the main topic the students choose for their project?",
                 "options": ["A  solar housing", "B  green roofs", "C  recycled building materials"],
                 "answer": "B  green roofs"},
                {"type": "gap", "id": "t4l3q3", "text": "Maya will be responsible for researching the ____ benefits of the design.", "answer": "environmental"},
                {"type": "gap", "id": "t4l3q4", "text": "Tom will focus on the ____ of construction.", "answer": "cost"},
                {"type": "mcq", "id": "t4l3q5", "text": "Which building do they decide to use as their case study?",
                 "options": ["A  the city library", "B  the new hospital", "C  the train station"],
                 "answer": "A  the city library"},
                {"type": "gap", "id": "t4l3q6", "text": "They plan to interview the building's chief ____.", "answer": "architect"},
                {"type": "gap", "id": "t4l3q7", "text": "The presentation should last no longer than ____ minutes.", "answer": "fifteen"},
                {"type": "gap", "id": "t4l3q8", "text": "They agree to include several ____ to make the talk more visual.", "answer": "diagrams"},
                {"type": "mcq", "id": "t4l3q9", "text": "When is the first draft due?",
                 "options": ["A  next Monday", "B  in two weeks", "C  at the end of the month"],
                 "answer": "B  in two weeks"},
                {"type": "gap", "id": "t4l3q10", "text": "They decide to meet again in the ____ on Thursday afternoon.", "answer": "library"},
            ],
        },
        {
            "number": 4,
            "title": "Section 4 — The history of timekeeping",
            "instructions": "Questions 31–40. Listen to part of a university lecture on the history of timekeeping and answer the questions below. Write ONE WORD AND/OR A NUMBER for the gap-fill questions, and choose the correct letter for the multiple-choice questions.",
            "audio": "test4_s4.mp3",
            "questions": [
                {"type": "gap", "id": "t4l4q1", "text": "The earliest devices used the movement of a ____ to mark the hours.", "answer": "shadow"},
                {"type": "gap", "id": "t4l4q2", "text": "A major drawback of the sundial was that it did not work at ____.", "answer": "night"},
                {"type": "mcq", "id": "t4l4q3", "text": "Which device measured time using a steady flow of water?",
                 "options": ["A  the hourglass", "B  the water clock", "C  the candle clock"],
                 "answer": "B  the water clock"},
                {"type": "gap", "id": "t4l4q4", "text": "The first mechanical clocks appeared in European ____ during the Middle Ages.", "answer": "monasteries"},
                {"type": "gap", "id": "t4l4q5", "text": "Early mechanical clocks were regulated by a device called the ____.", "answer": "escapement"},
                {"type": "mcq", "id": "t4l4q6", "text": "Whose work led to the much more accurate pendulum clock?",
                 "options": ["A  Galileo and Huygens", "B  Newton and Hooke", "C  Harrison and Cook"],
                 "answer": "A  Galileo and Huygens"},
                {"type": "gap", "id": "t4l4q7", "text": "Accurate clocks at sea finally allowed sailors to calculate their ____.", "answer": "longitude"},
                {"type": "gap", "id": "t4l4q8", "text": "In the twentieth century, the ____ crystal greatly improved everyday clocks.", "answer": "quartz"},
                {"type": "mcq", "id": "t4l4q9", "text": "What do modern atomic clocks use to keep time?",
                 "options": ["A  the swing of a pendulum", "B  the vibration of atoms", "C  the decay of uranium"],
                 "answer": "B  the vibration of atoms"},
                {"type": "gap", "id": "t4l4q10", "text": "Atomic clocks are essential to the working of satellite ____ systems.", "answer": "navigation"},
            ],
        },
    ],
}


# Use the richer IELTS-style listening set (map labelling, matching, tables,
# form/note/sentence completion and MCQ) while keeping Reading/Writing intact.
from .listening_variety import TEST4_LISTENING as LISTENING


# ============================================================================
#  WRITING  — Task 1 (process diagram) + Task 2 (discussion essay)
# ============================================================================

WRITING = {
    "task1": {
        "kind": "task1",
        "title": "Writing — Task 1",
        "minutes": 20,
        "min_words": 150,
        "instructions": (
            "The diagram below shows the main stages in the production of chocolate "
            "from the cacao tree to the finished bar. The process begins when ripe "
            "cacao pods are harvested from the trees and ends when the liquid "
            "chocolate is moulded and cooled into bars ready for packaging. "
            "Summarise the information by selecting and reporting the main features."
        ),
        "chart_svg": """
<svg viewBox="0 0 520 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Flow diagram of how chocolate is made">
  <defs>
    <marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L7,3 L0,6 Z" fill="#1e3a5f"/>
    </marker>
  </defs>
  <style>
    .box { fill:#eef4ff; stroke:#1e3a5f; stroke-width:1.5; rx:6; }
    .lab { font: 600 10px 'Segoe UI', Arial, sans-serif; fill:#1a1f2b; }
    .ttl { font: 700 12px 'Segoe UI', Arial, sans-serif; fill:#1a1f2b; }
    .ln  { stroke:#1e3a5f; stroke-width:1.6; fill:none; }
  </style>

  <text x="14" y="18" class="ttl">How chocolate is made</text>

  <!-- Row 1 -->
  <rect class="box" x="14"  y="40" width="100" height="48" rx="6"/>
  <text x="64"  y="60" class="lab" text-anchor="middle">Cacao pods</text>
  <text x="64"  y="74" class="lab" text-anchor="middle">harvested</text>

  <rect class="box" x="148" y="40" width="100" height="48" rx="6"/>
  <text x="198" y="60" class="lab" text-anchor="middle">Beans</text>
  <text x="198" y="74" class="lab" text-anchor="middle">fermented</text>

  <rect class="box" x="282" y="40" width="100" height="48" rx="6"/>
  <text x="332" y="60" class="lab" text-anchor="middle">Beans dried</text>
  <text x="332" y="74" class="lab" text-anchor="middle">in the sun</text>

  <rect class="box" x="406" y="40" width="100" height="48" rx="6"/>
  <text x="456" y="60" class="lab" text-anchor="middle">Beans roasted</text>
  <text x="456" y="74" class="lab" text-anchor="middle">&amp; shelled</text>

  <!-- Row 1 arrows -->
  <line class="ln" x1="114" y1="64" x2="146" y2="64" marker-end="url(#arrow)"/>
  <line class="ln" x1="248" y1="64" x2="280" y2="64" marker-end="url(#arrow)"/>
  <line class="ln" x1="382" y1="64" x2="404" y2="64" marker-end="url(#arrow)"/>

  <!-- Down connector from row1 (right) to row2 (right) -->
  <path class="ln" d="M456,88 L456,120" marker-end="url(#arrow)"/>

  <!-- Row 2 (right to left) -->
  <rect class="box" x="406" y="122" width="100" height="48" rx="6"/>
  <text x="456" y="142" class="lab" text-anchor="middle">Nibs ground</text>
  <text x="456" y="156" class="lab" text-anchor="middle">into liquor</text>

  <rect class="box" x="282" y="122" width="100" height="48" rx="6"/>
  <text x="332" y="142" class="lab" text-anchor="middle">Sugar &amp; milk</text>
  <text x="332" y="156" class="lab" text-anchor="middle">added</text>

  <rect class="box" x="148" y="122" width="100" height="48" rx="6"/>
  <text x="198" y="142" class="lab" text-anchor="middle">Mixture</text>
  <text x="198" y="156" class="lab" text-anchor="middle">conched</text>

  <rect class="box" x="14"  y="122" width="100" height="48" rx="6"/>
  <text x="64"  y="142" class="lab" text-anchor="middle">Moulded &amp;</text>
  <text x="64"  y="156" class="lab" text-anchor="middle">cooled</text>

  <!-- Row 2 arrows (leftwards) -->
  <line class="ln" x1="406" y1="146" x2="384" y2="146" marker-end="url(#arrow)"/>
  <line class="ln" x1="282" y1="146" x2="250" y2="146" marker-end="url(#arrow)"/>
  <line class="ln" x1="148" y1="146" x2="116" y2="146" marker-end="url(#arrow)"/>

  <!-- Down connector from row2 (left) to final box -->
  <path class="ln" d="M64,170 L64,200" marker-end="url(#arrow)"/>

  <!-- Final box -->
  <rect class="box" x="14" y="202" width="160" height="44" rx="6" fill="#dff3e4" stroke="#2d6a0a"/>
  <text x="94" y="222" class="lab" text-anchor="middle">Chocolate bars</text>
  <text x="94" y="236" class="lab" text-anchor="middle">wrapped &amp; packed</text>
</svg>
""",
    },
    "task2": {
        "kind": "task2",
        "title": "Writing — Task 2",
        "minutes": 40,
        "min_words": 250,
        "instructions": (
            "Mass tourism brings both benefits and problems to popular destinations. "
            "Discuss the advantages and disadvantages of mass tourism. "
            "Give reasons for your answer and include any relevant examples from "
            "your own knowledge or experience."
        ),
    },
}
