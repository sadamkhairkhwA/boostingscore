"""
Hardcoded payload for IELTS Academic Reading Test 6.
"""
from __future__ import annotations

from .common import build_payload, q

PART1_HTML = """
<p class="art-pass__kicker">Part 1 · Notices</p>
<h1 class="art-pass__title">Community renewable energy schemes — resident information</h1>

<h2 class="art-pass__sub">Text A — Community Solar Co-operative</h2>
<p>Local residents can buy shares, starting from <strong>£50</strong>, in the community-owned solar array installed on the roof of the sports centre in <strong>2019</strong>. The array generates enough electricity to power around 150 homes at peak output. Membership is open to anyone living within <strong>15 miles</strong> of the sports centre. Shareholders receive an annual return of up to 4%, and shares must be held for a minimum of <strong>two</strong> years before they can be resold to another member. Surplus electricity is sold back to the national grid, and the profits fund a local community grant of £10,000 per year for school and village hall improvements.</p>

<h2 class="art-pass__sub">Text B — Neighbourhood Wind Fund</h2>
<p>The two turbines on Hartley Ridge, commissioned in <strong>2021</strong>, are jointly owned by the parish council and 340 local investors. Investors can commit any amount from £100 to £5,000, and returns are paid annually according to how much electricity the turbines generate that year. A community benefit fund of <strong>£8,000</strong> per turbine is set aside every year and distributed by a grant committee to local charities and youth groups. To invest, an applicant must live within the parish boundary or an adjoining parish.</p>

<h2 class="art-pass__sub">Text C — Home Battery &amp; Storage Grant Scheme</h2>
<p>Homeowners installing a battery storage system alongside solar panels can apply to the council for a grant covering up to <strong>30%</strong> of installation costs, capped at £1,200 per household. Applications open twice a year, in March and September. Priority is given to households that are already receiving a solar subsidy from an earlier council scheme. Systems must be installed by an approved contractor and must have a minimum capacity of <strong>5</strong> kWh to qualify.</p>
"""

PART2_HTML = """
<p class="art-pass__kicker">Part 2 · History of technology</p>
<h1 class="art-pass__title">How the printing press changed the world</h1>

<p><strong>Paragraph 1</strong><br>
Johannes Gutenberg's printing press, developed in Mainz in the 1440s, combined metal movable type, oil-based ink and a modified <strong>wine</strong> press into a single practical system. It is often described as the turning point in the history of European printing, although movable type had already been used earlier in China, where Bi Sheng experimented with it in the eleventh century, and in Korea.</p>

<p><strong>Paragraph 2</strong><br>
Gutenberg's most famous production, the 42-line Bible, was completed around 1455 after roughly three years of work and produced about <strong>180</strong> copies. This was a dramatic improvement on hand-copied manuscripts, which could take a single scribe a year or more to complete just one Bible, making printed books far cheaper and faster to produce in any meaningful quantity.</p>

<p><strong>Paragraph 3</strong><br>
Printing spread rapidly across Europe. Within fifty years of Gutenberg's press, printing had reached more than 200 cities, and print runs allowed far greater duplication than manuscript copying ever could. This new capacity for mass duplication is widely credited with accelerating the spread of Reformation ideas across sixteenth-century Europe, as pamphlets could be produced and distributed far more quickly than handwritten texts.</p>

<p><strong>Paragraph 4</strong><br>
Printing also encouraged more standardised spelling and grammar in vernacular languages, because typesetting required consistent forms that handwriting had never demanded. At the same time, it allowed scholars in different countries to refer precisely to the same edition and page of a scientific work, supporting more reliable collaboration and citation across long distances.</p>

<p><strong>Paragraph 5</strong><br>
As printed material such as pamphlets, almanacs and early newspapers became more affordable, literacy rates gradually rose across much of Europe. Printing presses also became significant commercial enterprises in their own right. At the same time, several European governments introduced early censorship laws once they recognised how quickly the new technology could spread political and religious ideas.</p>

<p><strong>Paragraph 6</strong><br>
The fundamental mechanical process behind printing changed remarkably little for roughly 350 years. It was only with the introduction of <strong>steam</strong>-powered rotary presses in the nineteenth century that printing speed increased dramatically, a development that made mass-circulation newspapers possible for the first time.</p>
"""

PART3_HTML = """
<p class="art-pass__kicker">Part 3 · Academic reading</p>
<h1 class="art-pass__title">Artificial intelligence in medical diagnosis</h1>

<p><strong>A</strong><br>
Machine learning models, particularly deep neural networks, are increasingly used to analyse medical images such as X-rays, CT scans and retinal photographs. On some narrowly defined tasks, these systems can match or even exceed the accuracy of experienced human specialists, prompting growing interest from hospitals and health regulators alike.</p>

<p><strong>B</strong><br>
Such systems are typically trained on large labelled datasets, in which each image has been annotated by expert clinicians. Performance depends heavily on the size, quality and diversity of this <strong>training</strong> data, and a model trained mainly on images from one population can perform less reliably when later applied to patients from a different demographic group.</p>

<p><strong>C</strong><br>
One well-known application is diabetic retinopathy screening. A system approved by the United States Food and Drug Administration in <strong>2018</strong> can assess retinal photographs for signs of the condition without a specialist reviewing every image, expanding access to screening in areas with few ophthalmologists. Related systems have since been developed to flag certain skin cancers from photographs and to detect suspicious patterns in mammograms.</p>

<p><strong>D</strong><br>
A persistent difficulty is that many advanced models behave like a <strong>black</strong> box: clinicians cannot always trace exactly why a particular prediction was made. This complicates efforts to build clinical trust and raises accountability questions whenever an AI-assisted diagnosis later proves to be wrong. Researchers are developing techniques that highlight which regions of an image most influenced a given decision, in an attempt to make these systems more interpretable.</p>

<p><strong>E</strong><br>
Many countries are still developing clear frameworks for approving and monitoring diagnostic AI tools, particularly as such tools continue to be updated after they enter clinical use. Questions remain about how to assign liability when a diagnostic error occurs partly through algorithmic assistance, and about how regulators should audit a system once real-world data begins to drift from the data it was originally trained on.</p>

<p><strong>F</strong><br>
Rather than replacing radiologists and pathologists outright, most researchers expect AI to take over repetitive screening tasks, freeing specialists to concentrate on complex or ambiguous cases and on communicating results to patients. Some hospitals report that clinicians now spend less <strong>time</strong> on routine image review since adopting AI-assisted triage tools.</p>

<p><strong>G</strong><br>
Ongoing research into multimodal models, which combine imaging with patient history, laboratory results and genetic data, may eventually support more holistic diagnostic recommendations. Experts caution, however, that rigorous, large-scale clinical trials, rather than laboratory accuracy figures alone, will be needed before such tools are trusted for routine, independent clinical use.</p>
"""

INSTRUCTIONS = {
    1: "Part 1: Read three short texts on community renewable energy schemes (A, B, C). Q1–5: Matching. Q6–9: True/False/Not Given. Q10–14: Sentence completion.",
    2: "Part 2: Read the passage on the history of the printing press. Q15–20: Yes/No/Not Given. Q21–23: Sentence completion. Q24–27: Multiple choice.",
    3: "Part 3: Read the academic article on AI in medical diagnosis. Q28–32: Matching paragraphs (A–G). Q33–36: Multiple choice. Q37–40: Summary completion.",
}

PART_META = {
    1: {"label": "Part 1", "subtitle": "Community renewable energy schemes", "q_start": 1, "q_end": 14},
    2: {"label": "Part 2", "subtitle": "History of the printing press", "q_start": 15, "q_end": 27},
    3: {"label": "Part 3", "subtitle": "AI in medical diagnosis", "q_start": 28, "q_end": 40},
}

TOPIC_CHIPS = [
    {"icon": "leaf", "color": "green", "label": "Community renewable energy (three texts)"},
    {"icon": "newspaper", "color": "amber", "label": "History of the printing press (article)"},
    {"icon": "brain", "color": "purple", "label": "AI in medical diagnosis (academic)"},
]

SUMMARY_INTRO_HTML = """
<p class="art-sum-intro">Diagnostic AI systems are usually trained on large collections of images labelled by expert clinicians, and their accuracy depends on how representative this <span class="art-sum-slot" data-q="37" tabindex="0">37</span> data is of the wider patient population. One widely cited example is a retinopathy screening tool approved by regulators in <span class="art-sum-slot" data-q="38" tabindex="0">38</span>, which can operate without a specialist checking every image. A recurring concern is that many models behave like a <span class="art-sum-slot" data-q="39" tabindex="0">39</span> box, making their reasoning difficult for clinicians to trace. Rather than replacing specialists, most researchers expect such tools to change how professionals spend their <span class="art-sum-slot" data-q="40" tabindex="0">40</span>, allowing more focus on complex cases.</p>
"""

QUESTIONS = [
    q(
        1,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a scheme that gives priority to households already receiving support for another renewable technology",
        ["A", "B", "C"],
        "C",
        None,
        "Text C: priority is given to households already receiving an earlier solar subsidy.",
    ),
    q(
        2,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a minimum period that must pass before an investment can be resold",
        ["A", "B", "C"],
        "A",
        None,
        "Text A: shares must be held for a minimum of two years before resale.",
    ),
    q(
        3,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a project owned jointly by a local council and hundreds of individual investors",
        ["A", "B", "C"],
        "B",
        None,
        "Text B: the turbines are jointly owned by the parish council and 340 investors.",
    ),
    q(
        4,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a scheme where financial support is only available during two set periods each year",
        ["A", "B", "C"],
        "C",
        None,
        "Text C: applications open twice a year, in March and September.",
    ),
    q(
        5,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "an eligibility rule expressed as a distance in miles rather than an administrative boundary",
        ["A", "B", "C"],
        "A",
        None,
        "Text A: membership is open to anyone living within 15 miles of the sports centre.",
    ),
    q(
        6,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "Anyone in the country may buy shares in the community solar co-operative, regardless of where they live.",
        ["True", "False", "Not Given"],
        "False",
        None,
        "Text A: membership is restricted to residents within 15 miles of the sports centre.",
    ),
    q(
        7,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "The Hartley Ridge turbines are owned by both a public body and private individuals.",
        ["True", "False", "Not Given"],
        "True",
        None,
        "Text B: jointly owned by the parish council and 340 local investors.",
    ),
    q(
        8,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "The council battery grant can cover the full cost of installing a storage system.",
        ["True", "False", "Not Given"],
        "False",
        None,
        "Text C: the grant covers up to 30% of costs, capped at £1,200.",
    ),
    q(
        9,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "The wind fund's grant committee includes representatives from local schools.",
        ["True", "False", "Not Given"],
        "Not Given",
        None,
        "Text B mentions a grant committee but does not say who sits on it.",
    ),
    q(
        10,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "Shares in the community solar co-operative start from £_____.",
        None,
        "50",
        ["50"],
        "Text A: shares start from £50.",
    ),
    q(
        11,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "The solar array was installed on the roof of the sports centre in _____.",
        None,
        "2019",
        ["2019"],
        "Text A: installed in 2019.",
    ),
    q(
        12,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "Each turbine at Hartley Ridge generates a community benefit fund of £_____ per year.",
        None,
        "8000",
        ["8000", "8,000"],
        "Text B: £8,000 per turbine per year.",
    ),
    q(
        13,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "Homeowners can receive a grant of up to _____% of installation costs for a battery system.",
        None,
        "30",
        ["30"],
        "Text C: up to 30% of installation costs.",
    ),
    q(
        14,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "The minimum battery capacity required to qualify for the grant is _____ kWh.",
        None,
        "5",
        ["5"],
        "Text C: a minimum capacity of 5 kWh.",
    ),
    q(
        15,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "The writer suggests that Gutenberg was the very first person in history to use movable type.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 1: movable type had already been used earlier in China and Korea.",
    ),
    q(
        16,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "According to the writer, the 42-line Bible took less time to produce, per copy, than a hand-copied manuscript.",
        ["Yes", "No", "Not Given"],
        "Yes",
        None,
        "Paragraph 2: printing was far faster than a scribe copying manuscripts by hand.",
    ),
    q(
        17,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "The writer names the specific city where printing first spread to outside Mainz.",
        ["Yes", "No", "Not Given"],
        "Not Given",
        None,
        "Paragraph 3 gives a number of cities but does not name any specific one.",
    ),
    q(
        18,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "The writer implies that Reformation ideas spread more slowly because of the printing press.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 3: printing is credited with accelerating the spread of Reformation ideas.",
    ),
    q(
        19,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "The writer suggests that printed texts had no effect on spelling conventions in vernacular languages.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 4: printing encouraged more standardised spelling and grammar.",
    ),
    q(
        20,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "The writer states that some European governments introduced censorship laws in response to printing.",
        ["Yes", "No", "Not Given"],
        "Yes",
        None,
        "Paragraph 5: governments introduced early censorship laws once they recognised printing's power.",
    ),
    q(
        21,
        2,
        "gap",
        "Questions 21–23",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD from the passage for each answer.",
        "Gutenberg's press combined movable type with a modified _____ press.",
        None,
        "wine",
        ["wine"],
        "Paragraph 1: a modified wine press.",
    ),
    q(
        22,
        2,
        "gap",
        "Questions 21–23",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "The 42-line Bible took around three years to produce about _____ copies.",
        None,
        "180",
        ["180"],
        "Paragraph 2: roughly 180 copies were produced.",
    ),
    q(
        23,
        2,
        "gap",
        "Questions 21–23",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD from the passage for each answer.",
        "The fundamental mechanical printing process changed only when _____-powered rotary presses were introduced in the nineteenth century.",
        None,
        "steam",
        ["steam"],
        "Paragraph 6: steam-powered rotary presses.",
    ),
    q(
        24,
        2,
        "mc",
        "Questions 24–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "According to Paragraph 1, movable type printing existed before Gutenberg in",
        [
            "A. only Germany",
            "B. China and Korea",
            "C. Italy and France",
            "D. England alone",
        ],
        "B",
        None,
        "Paragraph 1: earlier movable type use in China and Korea.",
    ),
    q(
        25,
        2,
        "mc",
        "Questions 24–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "What point does the writer make by comparing the 42-line Bible with hand-copied manuscripts (Paragraph 2)?",
        [
            "A. Manuscripts were more accurate",
            "B. Printing dramatically increased production speed",
            "C. Manuscripts were cheaper to produce",
            "D. Printing required more skilled labour",
        ],
        "B",
        None,
        "Paragraph 2: printing was far faster than hand-copying.",
    ),
    q(
        26,
        2,
        "mc",
        "Questions 24–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "According to Paragraph 4, one effect of printing on written language was that it",
        [
            "A. increased regional dialect variation",
            "B. eliminated the need for standard grammar",
            "C. encouraged more standardised spelling",
            "D. made scientific texts harder to reference precisely",
        ],
        "C",
        None,
        "Paragraph 4: printing encouraged more standardised spelling and grammar.",
    ),
    q(
        27,
        2,
        "mc",
        "Questions 24–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "Why did some European governments introduce censorship laws, according to Paragraph 5?",
        [
            "A. To reduce the cost of paper",
            "B. Because they recognised printing's power to spread ideas quickly",
            "C. Because literacy rates were falling",
            "D. To encourage more commercial printing enterprises",
        ],
        "B",
        None,
        "Paragraph 5: governments responded to the speed at which ideas could spread.",
    ),
    q(
        28,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "an example of a diagnostic AI tool that has received official approval from a national regulator",
        ["A", "B", "C", "D", "E", "F", "G"],
        "C",
        None,
        "Paragraph C: the FDA-approved retinopathy screening system.",
    ),
    q(
        29,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "a description of research aimed at making it clearer why a model reached a particular conclusion",
        ["A", "B", "C", "D", "E", "F", "G"],
        "D",
        None,
        "Paragraph D: techniques that highlight influential regions of an image.",
    ),
    q(
        30,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "a reference to how performance can vary depending on the population represented in the training data",
        ["A", "B", "C", "D", "E", "F", "G"],
        "B",
        None,
        "Paragraph B: models trained on one population may be less reliable on another.",
    ),
    q(
        31,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "an expectation that AI will change how specialists spend their time rather than eliminate their jobs",
        ["A", "B", "C", "D", "E", "F", "G"],
        "F",
        None,
        "Paragraph F: AI is expected to free specialists for complex cases, not replace them.",
    ),
    q(
        32,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "a mention of the kind of evidence considered necessary before wider clinical adoption of newer tools",
        ["A", "B", "C", "D", "E", "F", "G"],
        "G",
        None,
        "Paragraph G: large-scale clinical trials are needed, not accuracy figures alone.",
    ),
    q(
        33,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "According to Paragraph A, deep learning models applied to medical images",
        [
            "A. always outperform every human specialist",
            "B. can match or exceed specialist accuracy on some narrowly defined tasks",
            "C. cannot yet analyse retinal photographs",
            "D. are only used experimentally in laboratories",
        ],
        "B",
        None,
        "Paragraph A: can match or exceed accuracy on narrowly defined tasks.",
    ),
    q(
        34,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "What does Paragraph C suggest about the FDA-approved retinopathy screening system?",
        [
            "A. It requires an ophthalmologist to check every result",
            "B. It can operate without a specialist reviewing each image",
            "C. It is only accurate for skin cancer detection",
            "D. It was withdrawn from use in 2018",
        ],
        "B",
        None,
        "Paragraph C: it can assess images without a specialist reviewing each one.",
    ),
    q(
        35,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "What is identified in Paragraph D as a key challenge with advanced diagnostic models?",
        [
            "A. They are too slow for clinical use",
            "B. Clinicians cannot always trace why a model made a particular prediction",
            "C. They require no training data at all",
            "D. Patients refuse to accept any AI-assisted diagnosis",
        ],
        "B",
        None,
        "Paragraph D: the black-box problem makes reasoning hard to trace.",
    ),
    q(
        36,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "According to Paragraph E, one unresolved issue concerning diagnostic AI is",
        [
            "A. how to assign liability when an error occurs",
            "B. how to train radiologists in basic computing",
            "C. how to reduce the cost of medical imaging equipment",
            "D. how to increase the number of specialists in rural areas",
        ],
        "A",
        None,
        "Paragraph E: questions remain about liability for algorithm-assisted errors.",
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
        "training",
        ["training"],
        "Paragraph B: accuracy depends on the training data used.",
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
        "2018",
        ["2018"],
        "Paragraph C: approved by the FDA in 2018.",
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
        "black",
        ["black"],
        "Paragraph D: many models behave like a black box.",
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
        "time",
        ["time"],
        "Paragraph F: clinicians spend less time on routine review.",
        None,
    ),
]


def get_payload() -> dict:
    return build_payload(
        test_number=6,
        title_bar="IELTS Academic Reading — Test 6",
        part1_html=PART1_HTML,
        part2_html=PART2_HTML,
        part3_html=PART3_HTML,
        instructions=INSTRUCTIONS,
        part_meta=PART_META,
        questions=QUESTIONS,
        summary_intro_html=SUMMARY_INTRO_HTML,
    )
