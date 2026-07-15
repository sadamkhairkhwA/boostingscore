"""
Hardcoded payload for IELTS Academic Reading Test 3 (client + server scoring).
"""
from __future__ import annotations

from .common import build_payload, q

PART1_HTML = """
<p class="art-pass__kicker">Part 1 · Visitor information</p>
<h1 class="art-pass__title">Museum visitor information</h1>

<h2 class="art-pass__sub">Text A — National Museum of Antiquities: general visitor information</h2>
<p>The museum is open <strong>Tuesday to Sunday</strong>, 10am to 5pm, and is closed on Mondays except on bank holidays, when normal hours apply. Last admission to all galleries is <strong>forty-five</strong> minutes before closing. Entry to the permanent galleries is free for everyone, and visitors <strong>under 18</strong> are admitted free of charge to every part of the museum at any time. Audio guides can be hired at the information desk for £4 and are available in <strong>eight</strong> languages. Photography without flash is permitted in the permanent galleries, but is not allowed in any special exhibition space. The café closes thirty minutes before the museum closes. Group visits of ten or more people must be booked at least two weeks in advance through the group-visits office.</p>

<h2 class="art-pass__sub">Text B — Special exhibition: "Voyages: Trade Routes of the Ancient World"</h2>
<p>This exhibition runs from 14 March to 7 <strong>September</strong>. Standard adult tickets cost £14; concessions are £9; museum members are admitted free. Online booking is strongly recommended, as entry is organised into timed slots released every thirty minutes. A full-colour exhibition guidebook is included free with every ticket. Highlights include cargo recovered from a Mediterranean shipwreck, a hoard of ancient gold coins, and an interactive map of historic trade routes. Guided tours run daily at 11am and 2pm for an additional charge of <strong>£5</strong> per person, and each tour group is limited to a maximum of <strong>twenty</strong> visitors. The exhibition shop operates separately from the main museum shop and stocks items related only to this exhibition.</p>

<h2 class="art-pass__sub">Text C — Learning and education workshops</h2>
<p>School workshops are designed for pupils in Years 3 to 11 and are led by trained museum education officers. Each workshop lasts <strong>ninety</strong> minutes and costs £5 per pupil, with one adult chaperone admitted free for every ten pupils. Schools must book workshops at least <strong>four</strong> weeks in advance using the online booking form. Family workshops take place on weekends, require no advance booking, and are free with general admission; they are suitable for children aged five to eleven. Homeschool sessions are held on the first Wednesday of every month and must be booked separately. Workshop themes include Ancient Trade, Archaeology Detectives, and Myths &amp; Legends. Schools that cancel a booking must give at least <strong>five</strong> working days' notice to receive a refund.</p>
"""

PART2_HTML = """
<p class="art-pass__kicker">Part 2 · Education &amp; technology</p>
<h1 class="art-pass__title">Remote learning at universities</h1>

<p><strong>Paragraph 1</strong><br>
Remote learning, once treated as a stopgap measure during large-scale campus closures, has become a permanent feature of higher-education planning. Most universities now offer at least some modules through hybrid delivery, combining face-to-face seminars with online lectures and discussion boards. Surveys of institutional strategy documents suggest that more than <strong>90%</strong> of universities across Europe and North America have retained some remote elements introduced during the disruption, even as campuses reopened fully. Administrators describe this not as a temporary compromise but as a structural redesign of how degree programmes are delivered.</p>

<p><strong>Paragraph 2</strong><br>
Proponents highlight flexibility as the central advantage. Students juggling part-time work, caregiving responsibilities, or long commutes can attend synchronous sessions from home or complete recorded lectures at a convenient time. A UNESCO survey of higher-education providers found that institutions offering flexible remote pathways reported broader enrolment among mature students and those living in rural areas without easy access to a campus. Widening participation, in this view, is one of the strongest arguments for maintaining remote options permanently rather than treating them as an emergency measure.</p>

<p><strong>Paragraph 3</strong><br>
Evidence on learning outcomes is mixed. Research from the Open University in the United Kingdom found that students in fully online courses achieved exam results comparable with campus-based peers when courses included frequent, structured checkpoints and regular tutor contact. However, the same research warned that students studying remotely without such structure were more likely to disengage gradually, a pattern researchers describe as "silent <strong>withdrawal</strong>." Course completion rates fell most sharply among <strong>first-year students</strong>, who researchers argue benefit disproportionately from the informal, in-person routines that remote study removes.</p>

<p><strong>Paragraph 4</strong><br>
A further concern is unequal access to the technology that remote learning assumes. Not every student has a reliable broadband connection or a personal laptop suitable for extended study, and this gap — sometimes called <strong>digital poverty</strong> — falls disproportionately on lower-income and rural households rather than affecting all students equally. In response, a growing number of universities have introduced device-loan schemes and subsidised data packages, though take-up varies widely between institutions. Critics argue that until connectivity is treated as basic infrastructure rather than a personal expense, remote learning risks widening rather than narrowing existing educational inequalities.</p>

<p><strong>Paragraph 5</strong><br>
For academic staff, the shift has meant substantial extra work. Redesigning a lecture-based module for online delivery can take several times longer than preparing the original in-person version, and many staff report receiving little formal training before being expected to teach through unfamiliar platforms. Some lecturers argue that video calls remove the spontaneous questions and informal exchanges that often clarify difficult material, leaving remote seminars feeling flatter than their in-person equivalents. Universities have responded by investing heavily in learning-management platforms, with several institutions reporting technology budgets rising by more than <strong>30%</strong> since remote teaching became routine.</p>

<p><strong>Paragraph 6</strong><br>
Looking ahead, few analysts expect universities to abandon remote elements altogether, even though most agree that some in-person contact remains valuable, particularly for laboratory work, clinical training, and early-stage student wellbeing. Employer attitudes toward online-taught degrees have also shifted; surveys suggest recruiters increasingly judge graduates on demonstrated skills and institutional reputation rather than on delivery mode alone. Yet questions about assessment integrity persist, and many institutions have expanded identity-verification and plagiarism-detection systems for remote exams. The likely outcome, most commentators agree, is neither a full return to campus nor a fully online future, but a durable hybrid model shaped by subject, cost, and student need.</p>
"""

PART3_HTML = """
<p class="art-pass__kicker">Part 3 · Environment &amp; business</p>
<h1 class="art-pass__title">The circular economy and plastic waste</h1>

<p><strong>A</strong><br>
For most of the twentieth century, plastic production followed a straightforward linear model: raw materials were extracted, turned into products, used briefly, and then discarded. Global plastic output now exceeds <strong>400</strong> million tonnes a year, yet only a small fraction is collected for recycling in most countries. Campaigners increasingly argue that the linear "take-make-dispose" approach is structurally unable to keep pace with rising consumption, and that plastic waste — visible in oceans, landfills, and incinerators — has become the clearest public symbol of a wider resource problem.</p>

<p><strong>B</strong><br>
The circular economy offers an alternative framework built on three broad principles: eliminating waste and pollution by design, keeping materials and products in use for as long as possible, and regenerating natural systems rather than depleting them. Rather than treating a used bottle or container as rubbish, a circular model treats it as a resource to be collected, reprocessed, and returned to the supply chain. Advocates argue that this requires rethinking product design from the outset — a shift described by some economists as moving business away from selling volume towards selling <strong>durability</strong> and service.</p>

<p><strong>C</strong><br>
Chemical recycling — breaking plastic polymers down into their basic molecular building blocks so they can be reassembled into new material — is often presented as a technological solution to plastics that mechanical recycling cannot easily process. Supporters claim it can handle mixed or contaminated plastic waste that would otherwise be landfilled or burned. Critics, however, warn that some chemical recycling processes consume large amounts of energy and that a portion of processed material is ultimately burned as fuel rather than turned into new plastic, raising concerns that some claims of a fully closed loop amount to little more than <strong>greenwashing</strong>.</p>

<p><strong>D</strong><br>
Regulation has increasingly pushed responsibility for plastic waste back onto the companies that produce packaging in the first place. Under extended producer responsibility, or <strong>EPR</strong>, schemes now adopted across much of the European Union and in a growing number of other countries, manufacturers pay fees scaled to the volume and recyclability of packaging they place on the market. These fees are used to fund collection and sorting infrastructure. Supporters argue EPR gives companies a direct financial incentive to redesign packaging for easier recycling, rather than leaving the cost of disposal entirely with local governments and taxpayers.</p>

<p><strong>E</strong><br>
Some businesses have gone further, piloting reusable packaging and refill systems that avoid single-use plastic altogether. Refill schemes for household products, for instance, ask customers to return containers for cleaning and reuse rather than buying a new bottle each time. Early trials suggest genuine environmental benefits, but scaling reuse systems is logistically demanding: collecting, washing, and redistributing containers requires reverse logistics networks that are far more complex than one-way distribution. Consumer habits present a further obstacle, since convenience-driven shopping behaviour often favours single-use formats even when reusable alternatives are available nearby.</p>

<p><strong>F</strong><br>
In many developing countries, informal waste pickers already perform much of the practical work of a circular economy, sorting and collecting recyclable plastic that would otherwise be discarded. Researchers estimate that this <strong>informal</strong> sector recovers a substantial share of the plastic that is currently recycled worldwide, despite workers typically receiving low and unstable pay and facing significant health hazards from unsorted waste. Development economists argue that formalising this workforce — through fair contracts, safety equipment, and stable income — could strengthen circular-economy outcomes while improving working conditions, though implementation has been slow and uneven across regions.</p>

<p><strong>G</strong><br>
International negotiations toward a binding global <strong>treaty</strong> on plastic pollution have repeatedly stalled over disagreements between countries that favour mandatory production limits and those that prefer voluntary national commitments. Economists estimate that shifting to a genuinely circular plastics economy at global scale would require enormous upfront investment in collection, sorting, and reprocessing infrastructure, particularly in lower-income regions. Despite this uncertainty, investment in circular-economy start-ups and corporate sustainability commitments has continued to grow, suggesting that momentum toward reducing plastic waste is unlikely to reverse even where formal international agreement remains elusive.</p>
"""

INSTRUCTIONS = {
    1: "Part 1: Read three short texts about museum visitor information (A, B, C). Q1–5: Matching. Q6–9: True/False/Not Given. Q10–14: Sentence completion.",
    2: "Part 2: Read the passage on remote learning at universities. Q15–19: Yes/No/Not Given. Q20–22: Sentence completion. Q23–27: Multiple choice.",
    3: "Part 3: Read the article on the circular economy and plastic waste. Q28–32: Matching paragraphs (A–G). Q33–36: Multiple choice. Q37–40: Summary completion.",
}

PART_META = {
    1: {"label": "Part 1", "subtitle": "Museum visitor information", "q_start": 1, "q_end": 14},
    2: {"label": "Part 2", "subtitle": "Remote learning at universities", "q_start": 15, "q_end": 27},
    3: {"label": "Part 3", "subtitle": "Circular economy & plastic waste", "q_start": 28, "q_end": 40},
}

TOPIC_CHIPS = [
    {"icon": "building", "color": "navy", "label": "Museum visitor information"},
    {"icon": "laptop", "color": "blue", "label": "Remote learning (universities)"},
    {"icon": "leaf", "color": "green", "label": "Circular economy & plastic waste"},
]

QUESTIONS = [
    q(
        1,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a requirement to book a visit at least four weeks ahead",
        ["A", "B", "C"],
        "C",
        None,
        "Text C requires schools to book workshops at least four weeks in advance.",
    ),
    q(
        2,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "free entry to the permanent galleries for visitors below a certain age",
        ["A", "B", "C"],
        "A",
        None,
        "Text A states under-18s are admitted free at any time.",
    ),
    q(
        3,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "an additional fee for a guided tour, with a limit on how many people may join",
        ["A", "B", "C"],
        "B",
        None,
        "Text B charges £5 extra for guided tours, capped at twenty visitors.",
    ),
    q(
        4,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a session held once a month for children who are not in mainstream schooling",
        ["A", "B", "C"],
        "C",
        None,
        "Text C holds homeschool sessions on the first Wednesday of every month.",
    ),
    q(
        5,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a shorter window of time for entering before the venue closes for the day",
        ["A", "B", "C"],
        "A",
        None,
        "Text A gives last admission as forty-five minutes before closing.",
    ),
    q(
        6,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "The museum is open to visitors every day of the week.",
        ["True", "False", "Not Given"],
        "False",
        None,
        "Text A says the museum is closed on Mondays except bank holidays.",
    ),
    q(
        7,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "Visitors may photograph objects in the permanent galleries as long as they do not use flash.",
        ["True", "False", "Not Given"],
        "True",
        None,
        "Text A permits non-flash photography in the permanent galleries.",
    ),
    q(
        8,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "Visitors to the special exhibition must buy the exhibition guidebook separately from their ticket.",
        ["True", "False", "Not Given"],
        "False",
        None,
        "Text B says the guidebook is included free with every ticket.",
    ),
    q(
        9,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "Family workshops must be booked in advance.",
        ["True", "False", "Not Given"],
        "False",
        None,
        "Text C says family workshops require no advance booking.",
    ),
    q(
        10,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "Audio guides at the museum are available in _____ languages.",
        None,
        "eight",
        ["eight", "8"],
        "Text A states audio guides are available in eight languages.",
    ),
    q(
        11,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "The special exhibition closes on 7 _____.",
        None,
        "September",
        ["september"],
        "Text B says the exhibition runs until 7 September.",
    ),
    q(
        12,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "A guided tour of the special exhibition costs an extra £_____ per person.",
        None,
        "5",
        ["5"],
        "Text B states guided tours cost an additional £5 per person.",
    ),
    q(
        13,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "School workshops led by education officers last _____ minutes.",
        None,
        "90",
        ["90", "ninety"],
        "Text C states school workshops last ninety minutes.",
    ),
    q(
        14,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "Schools must give _____ working days' notice to receive a refund for a cancelled workshop booking.",
        None,
        "5",
        ["5", "five"],
        "Text C requires five working days' notice for a refund.",
    ),
    q(
        15,
        2,
        "ynng",
        "Questions 15–19",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "Universities regard remote learning as simply a temporary compromise now that campuses have reopened.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 1: administrators describe it as a structural redesign, not a temporary compromise.",
    ),
    q(
        16,
        2,
        "ynng",
        "Questions 15–19",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "Widening participation is one of the strongest arguments for keeping remote learning options permanently.",
        ["Yes", "No", "Not Given"],
        "Yes",
        None,
        "Paragraph 2 presents widening participation as one of the strongest arguments for permanent remote options.",
    ),
    q(
        17,
        2,
        "ynng",
        "Questions 15–19",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "The Open University research found that structure and tutor contact make little difference to online exam results.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 3: comparable results occurred only when courses had structured checkpoints and tutor contact.",
    ),
    q(
        18,
        2,
        "ynng",
        "Questions 15–19",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "The writer suggests that digital poverty affects students of all income levels equally.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 4: the gap falls disproportionately on lower-income and rural households.",
    ),
    q(
        19,
        2,
        "ynng",
        "Questions 15–19",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "The writer suggests that employers now judge online-taught degrees only by how they were delivered.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 6: recruiters increasingly judge graduates on skills and institutional reputation, not delivery mode alone.",
    ),
    q(
        20,
        2,
        "gap",
        "Questions 20–22",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "More than _____% of surveyed universities retained some remote elements after campuses fully reopened.",
        None,
        "90",
        ["90"],
        "Paragraph 1 gives more than 90%.",
    ),
    q(
        21,
        2,
        "gap",
        "Questions 20–22",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "Researchers describe gradual disengagement without structure as silent _____.",
        None,
        "withdrawal",
        ["withdrawal"],
        "Paragraph 3 names this pattern silent withdrawal.",
    ),
    q(
        22,
        2,
        "gap",
        "Questions 20–22",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "Several institutions reported technology budgets rising by more than _____% since remote teaching became routine.",
        None,
        "30",
        ["30"],
        "Paragraph 5 gives more than 30%.",
    ),
    q(
        23,
        2,
        "mc",
        "Questions 23–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "According to Paragraph 3, which group of students is most at risk of dropping out of remote courses?",
        [
            "A. Mature students",
            "B. First-year students",
            "C. Rural students",
            "D. Part-time academic staff",
        ],
        "B",
        None,
        "Paragraph 3 states completion rates fell most sharply among first-year students.",
    ),
    q(
        24,
        2,
        "mc",
        "Questions 23–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "What does the writer identify as a cause of \"digital poverty\"?",
        [
            "A. Universities charging higher tuition fees",
            "B. Unequal access to broadband and devices",
            "C. Employer bias against online graduates",
            "D. A lack of assessment-integrity systems",
        ],
        "B",
        None,
        "Paragraph 4 links digital poverty to unequal access to broadband and devices.",
    ),
    q(
        25,
        2,
        "mc",
        "Questions 23–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "Why do some lecturers feel remote seminars are \"flatter\" than in-person ones?",
        [
            "A. Students ask fewer difficult questions overall",
            "B. Video calls remove spontaneous questions and exchanges",
            "C. Learning-management platforms are too expensive",
            "D. Online lecture content is always shorter",
        ],
        "B",
        None,
        "Paragraph 5 explains that video calls remove spontaneous exchanges.",
    ),
    q(
        26,
        2,
        "mc",
        "Questions 23–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "What is suggested about laboratory work and clinical training in Paragraph 6?",
        [
            "A. They are being phased out of university teaching entirely",
            "B. They can be fully replaced by video-call sessions",
            "C. In-person contact remains valuable for them",
            "D. They no longer require identity-verification systems",
        ],
        "C",
        None,
        "Paragraph 6 says in-person contact remains valuable for labs, clinical training, and wellbeing.",
    ),
    q(
        27,
        2,
        "mc",
        "Questions 23–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "What is the writer's overall conclusion about the future of university teaching?",
        [
            "A. Institutions will return fully to campus-based teaching",
            "B. A durable hybrid model is the most likely outcome",
            "C. Online-only degrees will become the standard model",
            "D. Technology budgets will fall sharply in coming years",
        ],
        "B",
        None,
        "Paragraph 6 concludes with a durable hybrid model shaped by subject, cost, and student need.",
    ),
    q(
        28,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "a criticism that a recycling technology may not deliver the fully closed loop it claims",
        ["A", "B", "C", "D", "E", "F", "G"],
        "C",
        None,
        "Paragraph C warns that some claims of a closed loop amount to greenwashing.",
    ),
    q(
        29,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "an estimate of how much plastic is produced worldwide each year",
        ["A", "B", "C", "D", "E", "F", "G"],
        "A",
        None,
        "Paragraph A gives global plastic output as over 400 million tonnes a year.",
    ),
    q(
        30,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "an example of regulation that requires manufacturers to help fund packaging disposal",
        ["A", "B", "C", "D", "E", "F", "G"],
        "D",
        None,
        "Paragraph D describes extended producer responsibility (EPR) schemes.",
    ),
    q(
        31,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "a description of the practical difficulties involved in scaling systems that reuse containers",
        ["A", "B", "C", "D", "E", "F", "G"],
        "E",
        None,
        "Paragraph E discusses the logistical demands of reuse and refill systems.",
    ),
    q(
        32,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "a mention of workers who informally collect recyclable plastic in lower-income countries",
        ["A", "B", "C", "D", "E", "F", "G"],
        "F",
        None,
        "Paragraph F discusses informal waste pickers in developing countries.",
    ),
    q(
        33,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "According to Paragraph B, the circular economy shifts business models toward",
        [
            "A. selling higher volumes of disposable goods",
            "B. selling durability and service rather than volume",
            "C. exporting waste to other countries",
            "D. increasing single-use packaging",
        ],
        "B",
        None,
        "Paragraph B describes a shift from selling volume to selling durability and service.",
    ),
    q(
        34,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "What is the writer's main criticism of chemical recycling in Paragraph C?",
        [
            "A. It cannot process any plastic waste at all",
            "B. It always produces new plastic with zero waste",
            "C. Some processes are energy-intensive and may not be a truly closed loop",
            "D. It has been banned across the European Union",
        ],
        "C",
        None,
        "Paragraph C raises concerns about energy use and claims of a fully closed loop.",
    ),
    q(
        35,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "According to Paragraph E, what is a major obstacle to reuse and refill systems?",
        [
            "A. Governments prohibit refill packaging",
            "B. Customers refuse to return containers under any circumstance",
            "C. Reverse logistics for washing and redistributing containers is complex",
            "D. Refill systems always cost less than single-use packaging",
        ],
        "C",
        None,
        "Paragraph E highlights the complexity of reverse logistics for reuse systems.",
    ),
    q(
        36,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "What do development economists argue in Paragraph F?",
        [
            "A. Informal waste pickers should be replaced by machines",
            "B. Formalising the informal waste sector could improve outcomes and conditions",
            "C. Waste pickers already receive high and stable pay",
            "D. The informal sector recovers a negligible share of recycled plastic",
        ],
        "B",
        None,
        "Paragraph F argues formalising the workforce could strengthen outcomes and conditions.",
    ),
    q(
        37,
        3,
        "summary",
        "Questions 37–40",
        "Summary completion",
        "Complete the summary. Choose NO MORE THAN ONE WORD from the passage for each answer.",
        "",
        None,
        "EPR",
        ["epr"],
        "Paragraph D names extended producer responsibility schemes as EPR.",
        None,
    ),
    q(
        38,
        3,
        "summary",
        "Questions 37–40",
        "Summary completion",
        "Complete the summary. Choose NO MORE THAN ONE WORD from the passage for each answer.",
        "",
        None,
        "greenwashing",
        ["greenwashing"],
        "Paragraph C warns claims of a closed loop can amount to greenwashing.",
        None,
    ),
    q(
        39,
        3,
        "summary",
        "Questions 37–40",
        "Summary completion",
        "Complete the summary. Choose NO MORE THAN ONE WORD from the passage for each answer.",
        "",
        None,
        "informal",
        ["informal"],
        "Paragraph F refers to the informal sector recovering plastic.",
        None,
    ),
    q(
        40,
        3,
        "summary",
        "Questions 37–40",
        "Summary completion",
        "Complete the summary. Choose NO MORE THAN ONE WORD from the passage for each answer.",
        "",
        None,
        "treaty",
        ["treaty"],
        "Paragraph G discusses a stalled global treaty on plastic pollution.",
        None,
    ),
]

SUMMARY_INTRO_HTML = """
<p class="art-sum-intro">Under extended producer responsibility schemes, sometimes shortened to <span class="art-sum-slot" data-q="37" tabindex="0">37</span>, manufacturers help fund the collection of packaging waste. Critics of some chemical recycling processes warn that claims of a fully closed loop can amount to little more than <span class="art-sum-slot" data-q="38" tabindex="0">38</span>. In many lower-income countries, the <span class="art-sum-slot" data-q="39" tabindex="0">39</span> sector already recovers a large share of the plastic that is currently recycled worldwide. Meanwhile, a binding global <span class="art-sum-slot" data-q="40" tabindex="0">40</span> on plastic pollution has repeatedly stalled amid disagreement between countries.</p>
"""


def get_payload() -> dict:
    return build_payload(
        test_number=3,
        title_bar="IELTS Academic Reading · Test 3",
        part1_html=PART1_HTML,
        part2_html=PART2_HTML,
        part3_html=PART3_HTML,
        instructions=INSTRUCTIONS,
        part_meta=PART_META,
        questions=QUESTIONS,
        summary_intro_html=SUMMARY_INTRO_HTML,
    )
