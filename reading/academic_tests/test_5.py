"""
Hardcoded payload for IELTS Academic Reading Test 5.
"""
from __future__ import annotations

from .common import build_payload, q

PART1_HTML = """
<p class="art-pass__kicker">Part 1 · Notices</p>
<h1 class="art-pass__title">Staff wellness programme — information for employees</h1>

<h2 class="art-pass__sub">Text A — Fitness &amp; Movement Scheme</h2>
<p>All permanent staff are entitled to a monthly gym subsidy of up to <strong>£30</strong>, redeemable at any of the <strong>twelve</strong> partner fitness centres listed on the intranet. Employees who complete the online enrolment form within their first month of joining receive a one-off welcome credit of <strong>£50</strong> towards their membership. Staff who prefer to exercise at their desks can request a standing desk through their line manager; a maximum of <strong>two</strong> such requests are approved per team each quarter, since supply is limited. A company-wide step challenge is held every <strong>October</strong>, and the three teams with the highest average daily step count each receive a shared £200 activity voucher to spend on a group outing. Employees who cycle to work can also claim a one-off <strong>£40</strong> contribution towards safety equipment such as helmets and lights.</p>

<h2 class="art-pass__sub">Text B — Employee Assistance Programme</h2>
<p>Confidential counselling is available free of charge for up to <strong>six</strong> sessions per calendar year, arranged through an external provider and unrelated to occupational health records. A helpline staffed by trained counsellors operates <strong>24 hours</strong> a day, seven days a week, and is also open to immediate family members of staff. Employees can be trained as mental health first aiders over a <strong>two</strong>-day course; once qualified, they wear a <strong>green</strong> lanyard so colleagues can identify them easily around the building. Managers are required to complete a shorter half-day awareness session before they can approve a team member's flexible return-to-work plan following a period of mental health leave.</p>

<h2 class="art-pass__sub">Text C — Health Screening &amp; Nutrition</h2>
<p>All staff aged <strong>40</strong> and over are automatically invited to a free annual health screening covering blood pressure, cholesterol and body mass index. Employees under 40 may still request a screening, but only once every <strong>two</strong> years, in order to prioritise higher-risk age groups. Every member of staff receives a healthy-eating voucher worth <strong>£15</strong> per month, redeemable in the staff canteen for salads, fruit and other listed items. Free flu vaccinations are offered on-site every <strong>November</strong>, and staff who have a pre-existing condition that increases their risk may also request a vaccination at any other time of year.</p>
"""

PART2_HTML = """
<p class="art-pass__kicker">Part 2 · Science &amp; health</p>
<h1 class="art-pass__title">The growing threat of antibiotic resistance</h1>

<p><strong>Paragraph 1</strong><br>
When penicillin entered widespread clinical use in the 1940s, it transformed medicine almost overnight, turning infections that had previously killed young and healthy people into conditions that could usually be cured within days. Doctors increasingly expected bacterial disease to be a solvable problem rather than an ever-present threat. Eight decades later, the World Health Organization warns that this expectation is no longer safe to make, because bacteria are adapting faster than the medicines used against them.</p>

<p><strong>Paragraph 2</strong><br>
Resistance arises through ordinary evolutionary pressure. Random mutations occasionally allow a bacterium to survive exposure to a drug that would kill its neighbours, and that individual then reproduces freely once competitors are eliminated. Resistance genes can also move between unrelated bacteria on small loops of DNA called <strong>plasmids</strong>, meaning that a trait which evolves in one species can spread sideways into others without either organism reproducing. The more often a population of bacteria meets an antibiotic, the faster a resistant strain is likely to emerge and dominate.</p>

<p><strong>Paragraph 3</strong><br>
Human use of antibiotics is not the only pressure driving resistance. A substantial proportion of antibiotics manufactured worldwide are administered to livestock, frequently to promote faster <strong>growth</strong> rather than to treat diagnosed illness. Because farm animals are often kept in large, closely packed groups, resistant strains that emerge on a single farm can circulate quickly and, in some cases, reach humans through the food chain or through agricultural run-off into local water supplies. In 2006, the European Union banned the use of antibiotics purely for growth promotion, a policy that several other regions have since debated adopting.</p>

<p><strong>Paragraph 4</strong><br>
Clinically, the consequences are already visible. Methicillin-resistant Staphylococcus aureus, commonly known as MRSA, and drug-resistant strains of tuberculosis have become established in hospitals in many countries, complicating routine procedures such as joint replacements and cancer treatment, both of which rely on antibiotics to prevent infection during recovery. Researchers have estimated that resistant infections already contribute to hundreds of thousands of deaths every year worldwide, and some widely cited projections suggest that figure could rise to around ten million annually by 2050 if current trends continue unchecked.</p>

<p><strong>Paragraph 5</strong><br>
Part of the difficulty is economic rather than purely scientific. Developing a new antibiotic can take over a <strong>decade</strong> and cost hundreds of millions of dollars, yet successful new drugs are typically used sparingly and only as a last resort, precisely to slow the emergence of resistance to them. This makes antibiotics far less profitable for pharmaceutical companies than medicines taken daily for chronic conditions, and several major manufacturers have scaled back or abandoned antibiotic research altogether. Public health specialists increasingly argue that new funding models, separating a company's profit from the volume of a drug sold, will be necessary to keep the development pipeline active.</p>

<p><strong>Paragraph 6</strong><br>
Several responses are already under way. Hospital <strong>stewardship</strong> programmes now monitor and, where appropriate, restrict prescribing, aiming to ensure antibiotics are used only when genuinely needed. Rapid diagnostic tests that distinguish bacterial from viral infections within minutes, rather than the days once required for laboratory culture, are being rolled out to reduce unnecessary prescriptions. Researchers are also revisiting bacteriophage therapy, which uses viruses that attack bacteria specifically, as a possible complement to conventional antibiotics. The WHO's Global Action Plan on antimicrobial resistance, adopted in 2015, continues to coordinate national strategies across member states, though implementation varies considerably between wealthier and lower-income countries.</p>
"""

PART3_HTML = """
<p class="art-pass__kicker">Part 3 · Academic reading</p>
<h1 class="art-pass__title">Preserving Pompeii: archaeology after the eruption</h1>

<p><strong>A</strong><br>
When Mount Vesuvius erupted in AD 79, the nearby Roman town of Pompeii was buried within hours under thick layers of ash and pumice. Paradoxically, this catastrophe created an unusually complete record of daily life in a first-century town, preserving buildings, streets, wall paintings and even food, because the town was never rebuilt on top of. The site was rediscovered by chance in the sixteenth century, but systematic excavation did not begin until the eighteenth century.</p>

<p><strong>B</strong><br>
Giuseppe Fiorelli, who directed excavations from 1863, transformed how the site was studied. He introduced a grid-based system for recording each building by district and block, and he pioneered a technique of pouring liquid plaster into the cavities left in the hardened ash by decomposed human bodies. The resulting casts captured the exact posture of victims at the moment they died, a discovery that had a profound effect on public understanding of the disaster's human toll.</p>

<p><strong>C</strong><br>
The preservation of organic material at Pompeii owes everything to the speed and nature of its burial. Rapid burial under several metres of ash and pumice sealed both organic and inorganic remains away from air and moisture almost instantly, preventing the decay that normally destroys wood, cloth and food within a few years at most archaeological sites. This is why loaves of bread, wooden furniture and even fabric survived in recognisable form for nearly two thousand years.</p>

<p><strong>D</strong><br>
Once exposed to the open air during excavation, however, Pompeii's remains face very different pressures. Weathering caused by rain, wind and sunlight gradually erodes plaster casts and frescoes that survived intact underground for centuries. Roots from plants that self-seed in unexcavated walls can also destabilise masonry from within. In addition, the site receives roughly 20,000 visitors on its busiest days, and this volume of foot traffic places further strain on fragile walkways and structures.</p>

<p><strong>E</strong><br>
In response to years of neglect and a partial building collapse in 2010, the European Union helped fund a conservation initiative known as the Great Pompeii Project, launched in 2012 with a budget of roughly 105 million euros. The project stabilised structurally unsound buildings, improved drainage across the site, and restored previously excavated houses that had been left exposed for decades. Temporary roofing was also installed over some unexcavated walls to slow further decay.</p>

<p><strong>F</strong><br>
Excavation continues even today. Work in Regio V, a previously unexcavated northern sector of the site, began in 2018 and has uncovered new frescoes, several complete skeletons, and inscriptions on walls. One piece of charcoal graffiti, dated to a month after the traditionally accepted date of the eruption, led some archaeologists to argue that Vesuvius actually erupted in October rather than August of AD 79.</p>

<p><strong>G</strong><br>
Pompeii has been a UNESCO World Heritage Site since 1997, and it remains one of the richest sources of evidence for everyday Roman economy, diet, art and urban planning available to historians anywhere. Balancing public access, which funds much of the ongoing conservation work, against the long-term preservation needed for future research remains one of the site's central challenges.</p>
"""

INSTRUCTIONS = {
    1: "Part 1: Read three short texts on workplace wellness (A, B, C). Q1–5: Matching. Q6–9: True/False/Not Given. Q10–14: Sentence completion.",
    2: "Part 2: Read the passage on antibiotic resistance. Q15–20: Yes/No/Not Given. Q21–23: Sentence completion. Q24–27: Multiple choice.",
    3: "Part 3: Read the academic article on Pompeii preservation. Q28–32: Matching paragraphs (A–G). Q33–36: Multiple choice. Q37–40: Summary completion.",
}

PART_META = {
    1: {"label": "Part 1", "subtitle": "Workplace wellness programmes", "q_start": 1, "q_end": 14},
    2: {"label": "Part 2", "subtitle": "Antibiotic resistance", "q_start": 15, "q_end": 27},
    3: {"label": "Part 3", "subtitle": "Pompeii preservation", "q_start": 28, "q_end": 40},
}

TOPIC_CHIPS = [
    {"icon": "heartbeat", "color": "green", "label": "Workplace wellness (three texts)"},
    {"icon": "flask", "color": "blue", "label": "Antibiotic resistance (article)"},
    {"icon": "compass", "color": "purple", "label": "Pompeii preservation (academic)"},
]

SUMMARY_INTRO_HTML = """
<p class="art-sum-intro">Rapid burial under thick volcanic ash sealed Pompeii away from air and moisture, which is why organic material decayed so little compared with most archaeological sites. In the nineteenth century, Fiorelli introduced a method of pouring liquid <span class="art-sum-slot" data-q="37" tabindex="0">37</span> into the cavities left by decomposed bodies, producing detailed casts of victims. Since being exposed to the open air, excavated structures have suffered from <span class="art-sum-slot" data-q="38" tabindex="0">38</span> caused by rain, wind and sunlight. A large EU-funded conservation initiative, known as the Great Pompeii <span class="art-sum-slot" data-q="39" tabindex="0">39</span>, was launched to stabilise crumbling buildings. More recently, excavation of a previously untouched sector known as Regio <span class="art-sum-slot" data-q="40" tabindex="0">40</span> has produced new frescoes and inscriptions.</p>
"""

QUESTIONS = [
    q(
        1,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a reward given to the teams that walk the most during a fixed period each year",
        ["A", "B", "C"],
        "A",
        None,
        "Text A: the three teams with the highest average step count win a voucher.",
    ),
    q(
        2,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a way of recognising an employee trained to support colleagues' mental health",
        ["A", "B", "C"],
        "B",
        None,
        "Text B: qualified first aiders wear a green lanyard.",
    ),
    q(
        3,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a benefit that is offered automatically once an employee reaches a certain age",
        ["A", "B", "C"],
        "C",
        None,
        "Text C: staff aged 40 and over are automatically invited to a screening.",
    ),
    q(
        4,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a helpline that can also be used by people who are not employed by the company",
        ["A", "B", "C"],
        "B",
        None,
        "Text B: the helpline is also open to immediate family members.",
    ),
    q(
        5,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a one-off payment intended to encourage a particular form of commuting",
        ["A", "B", "C"],
        "A",
        None,
        "Text A: a one-off £40 contribution towards cycling safety equipment.",
    ),
    q(
        6,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "Every member of staff can claim the same maximum gym subsidy, whichever partner centre they choose.",
        ["True", "False", "Not Given"],
        "True",
        None,
        "Text A: the £30 monthly subsidy applies at any of the twelve partner centres.",
    ),
    q(
        7,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "There is no limit to the number of standing desks a single team may request in one quarter.",
        ["True", "False", "Not Given"],
        "False",
        None,
        "Text A: a maximum of two requests are approved per team each quarter.",
    ),
    q(
        8,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "Employees who cycle to work receive a discount on public transport season tickets.",
        ["True", "False", "Not Given"],
        "Not Given",
        None,
        "Text A mentions a cycling contribution but says nothing about season tickets.",
    ),
    q(
        9,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "Managers must complete a two-day training course before approving a colleague's return-to-work plan.",
        ["True", "False", "Not Given"],
        "False",
        None,
        "Text B: managers complete a half-day session; the two-day course is for first aiders.",
    ),
    q(
        10,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "New starters who enrol within their first month receive a welcome credit of £_____.",
        None,
        "50",
        ["50"],
        "Text A states a one-off welcome credit of £50.",
    ),
    q(
        11,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "Confidential counselling is available free of charge for up to _____ sessions per year.",
        None,
        "six",
        ["six", "6"],
        "Text B: up to six sessions per calendar year.",
    ),
    q(
        12,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "Employees can train as mental health first aiders on a _____-day course.",
        None,
        "two",
        ["two", "2"],
        "Text B: a two-day training course.",
    ),
    q(
        13,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "Staff under 40 may request a health screening only once every _____ years.",
        None,
        "two",
        ["two", "2"],
        "Text C: once every two years for under-40s.",
    ),
    q(
        14,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "Free flu vaccinations are offered on-site every _____.",
        None,
        "November",
        ["November"],
        "Text C: flu vaccinations every November.",
    ),
    q(
        15,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "The writer suggests that doctors in the mid-twentieth century assumed bacterial infections would remain a permanent medical challenge.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 1: doctors increasingly expected bacterial disease to be solvable, the opposite view.",
    ),
    q(
        16,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "According to the writer, a resistance trait can spread into a different bacterial species without that species reproducing.",
        ["Yes", "No", "Not Given"],
        "Yes",
        None,
        "Paragraph 2: resistance genes move between species via plasmids.",
    ),
    q(
        17,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "The writer states that farm animals are given antibiotics only when they have a diagnosed illness.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 3: antibiotics are often given to livestock to promote growth, not to treat diagnosed illness.",
    ),
    q(
        18,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "The writer names the specific scientist who first discovered penicillin.",
        ["Yes", "No", "Not Given"],
        "Not Given",
        None,
        "No individual scientist is named anywhere in the passage.",
    ),
    q(
        19,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "The writer implies that pharmaceutical companies have a strong financial incentive to develop new antibiotics under current market conditions.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 5: antibiotics are less profitable, and several manufacturers have scaled back research.",
    ),
    q(
        20,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "The writer believes that rapid diagnostic tests could help reduce the number of unnecessary antibiotic prescriptions.",
        ["Yes", "No", "Not Given"],
        "Yes",
        None,
        "Paragraph 6: rapid tests are being rolled out to reduce unnecessary prescriptions.",
    ),
    q(
        21,
        2,
        "gap",
        "Questions 21–23",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD from the passage for each answer.",
        "In 2006, the European Union banned the use of antibiotics purely for _____ promotion.",
        None,
        "growth",
        ["growth"],
        "Paragraph 3: banned antibiotics used purely for growth promotion.",
    ),
    q(
        22,
        2,
        "gap",
        "Questions 21–23",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD from the passage for each answer.",
        "Developing a new antibiotic can take over a _____ and cost hundreds of millions of dollars.",
        None,
        "decade",
        ["decade"],
        "Paragraph 5: development can take over a decade.",
    ),
    q(
        23,
        2,
        "gap",
        "Questions 21–23",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD from the passage for each answer.",
        "Hospital _____ programmes monitor and restrict prescribing so antibiotics are used only when needed.",
        None,
        "stewardship",
        ["stewardship"],
        "Paragraph 6: hospital stewardship programmes.",
    ),
    q(
        24,
        2,
        "mc",
        "Questions 24–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "According to Paragraph 2, resistance genes can spread between different species of bacteria mainly by",
        [
            "A. random mutation during reproduction",
            "B. exposure to penicillin in the 1940s",
            "C. movement on small loops of DNA called plasmids",
            "D. contact with contaminated hospital equipment",
        ],
        "C",
        None,
        "Paragraph 2: resistance genes move between species on plasmids.",
    ),
    q(
        25,
        2,
        "mc",
        "Questions 24–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "The writer refers to farm animals mainly in order to show that",
        [
            "A. livestock rarely receive antibiotics at all",
            "B. human medicine is the only source of resistance pressure",
            "C. agricultural antibiotic use can also contribute to resistant strains",
            "D. the EU banned all antibiotic use in farming",
        ],
        "C",
        None,
        "Paragraph 3: agricultural use is a further pressure driving resistance.",
    ),
    q(
        26,
        2,
        "mc",
        "Questions 24–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "Why does the writer say new antibiotics are typically used \"sparingly\" (Paragraph 5)?",
        [
            "A. To keep prices low for patients",
            "B. To slow the development of resistance to them",
            "C. Because governments restrict their sale",
            "D. Because they are less effective than older drugs",
        ],
        "B",
        None,
        "Paragraph 5: used sparingly precisely to slow the emergence of resistance.",
    ),
    q(
        27,
        2,
        "mc",
        "Questions 24–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "What does the writer suggest about the WHO's Global Action Plan?",
        [
            "A. It has ended global antimicrobial resistance",
            "B. Its implementation is uneven across different countries",
            "C. It applies only to European Union member states",
            "D. It replaced the need for stewardship programmes",
        ],
        "B",
        None,
        "Paragraph 6: implementation varies between wealthier and lower-income countries.",
    ),
    q(
        28,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "a description of a technique that revealed the exact posture of victims at the moment they died",
        ["A", "B", "C", "D", "E", "F", "G"],
        "B",
        None,
        "Paragraph B describes Fiorelli's plaster-cast technique.",
    ),
    q(
        29,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "a reference to inscriptions that led some archaeologists to reconsider the traditional date of the eruption",
        ["A", "B", "C", "D", "E", "F", "G"],
        "F",
        None,
        "Paragraph F discusses graffiti pointing to an October eruption date.",
    ),
    q(
        30,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "an explanation of why organic material survived so much better here than at most archaeological sites",
        ["A", "B", "C", "D", "E", "F", "G"],
        "C",
        None,
        "Paragraph C explains the rapid, sealing effect of the ash burial.",
    ),
    q(
        31,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "a mention of the large number of people who visit the site on its busiest days",
        ["A", "B", "C", "D", "E", "F", "G"],
        "D",
        None,
        "Paragraph D mentions roughly 20,000 visitors on busy days.",
    ),
    q(
        32,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "a description of an international scheme to repair buildings left in poor condition for decades",
        ["A", "B", "C", "D", "E", "F", "G"],
        "E",
        None,
        "Paragraph E describes the EU-funded Great Pompeii Project.",
    ),
    q(
        33,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "According to Paragraph A, one reason Pompeii is unusually valuable to historians is that",
        [
            "A. its buildings were rebuilt after the eruption",
            "B. the eruption preserved an unusually complete record of daily life",
            "C. it was never rediscovered until the twentieth century",
            "D. its excavation began immediately after the eruption",
        ],
        "B",
        None,
        "Paragraph A: the burial preserved a detailed snapshot of daily life.",
    ),
    q(
        34,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "What was significant about Fiorelli's approach, according to Paragraph B?",
        [
            "A. He excavated the site for the first time in history",
            "B. He combined systematic recording with a method for capturing victims' final postures",
            "C. He proved the eruption occurred in October rather than August",
            "D. He removed all previous excavation records",
        ],
        "B",
        None,
        "Paragraph B: grid-based recording plus the plaster-cast technique.",
    ),
    q(
        35,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "According to Paragraph D, one threat to the site's fragile remains comes from",
        [
            "A. a shortage of visitors",
            "B. plants growing in unexcavated areas",
            "C. the original volcanic ash layer",
            "D. the excavation method used in 1863",
        ],
        "B",
        None,
        "Paragraph D: roots from self-seeded plants can destabilise masonry.",
    ),
    q(
        36,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "The writer refers to the Regio V excavations mainly to illustrate that",
        [
            "A. Pompeii has now been completely excavated",
            "B. new discoveries can still revise established historical assumptions",
            "C. earlier archaeologists ignored the northern sector deliberately",
            "D. graffiti is more valuable evidence than frescoes",
        ],
        "B",
        None,
        "Paragraph F: new graffiti led to reconsidering the traditional eruption date.",
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
        "plaster",
        ["plaster"],
        "Paragraph B: liquid plaster poured into cavities left by decomposed bodies.",
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
        "weathering",
        ["weathering"],
        "Paragraph D: weathering from rain, wind and sunlight erodes remains.",
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
        "Project",
        ["Project", "project"],
        "Paragraph E: the Great Pompeii Project.",
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
        "V",
        ["V"],
        "Paragraph F: excavation of Regio V.",
        None,
    ),
]


def get_payload() -> dict:
    return build_payload(
        test_number=5,
        title_bar="IELTS Academic Reading — Test 5",
        part1_html=PART1_HTML,
        part2_html=PART2_HTML,
        part3_html=PART3_HTML,
        instructions=INSTRUCTIONS,
        part_meta=PART_META,
        questions=QUESTIONS,
        summary_intro_html=SUMMARY_INTRO_HTML,
    )
