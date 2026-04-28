"""
Hardcoded payload for IELTS Academic Reading Test 1 (client + server scoring).
"""
from __future__ import annotations

from .academic_result_meta import RESULT_META_BY_ID

PART1_HTML = """
<p class="art-pass__kicker">Part 1 · Notices</p>
<h1 class="art-pass__title">Local services &amp; accommodation</h1>

<h2 class="art-pass__sub">Text A — Westbridge Public Library</h2>
<p>Standard membership is free for all Westbridge residents. You may borrow up to <strong>eight</strong> items at any time. The loan period is three weeks, with <strong>one</strong> renewal available by phone or online. Premium membership costs <strong>£25</strong> per year and allows you to borrow up to fifteen items, reserve popular titles in advance, access the digital library from home, and receive priority booking for study rooms. Late fines are <strong>20p</strong> per item per day for standard members. Premium members benefit from a seven-day grace period before fines begin. Lost items must be replaced at cost.</p>

<h2 class="art-pass__sub">Text B — Northfield Sports Centre</h2>
<p>All fitness classes last forty-five minutes except HIIT and Boxercise, which run for <strong>sixty</strong> minutes. You may book up to seven days in advance online or at reception. Cancellations must be made at least two hours before the class begins; otherwise a <strong>£3</strong> no-show fee applies. Under-16s are not permitted in HIIT or Boxercise sessions. The weekly timetable is as follows. <strong>Monday:</strong> Yoga 7am · Spinning 9am · Pilates 12pm · Boxercise 6pm. <strong>Tuesday:</strong> Aqua aerobics 8am · Yoga 10am · HIIT 5:30pm · Zumba 7pm. <strong>Wednesday:</strong> Spinning 7am · Pilates 9am · Yoga 12pm · Boxercise 6pm. <strong>Thursday:</strong> Aqua aerobics 8am · HIIT 10am · Zumba 5:30pm · Yoga 7pm. <strong>Friday:</strong> Spinning 7am · Yoga 9am · Pilates 12pm. <strong>Saturday:</strong> Aqua aerobics 9am · HIIT 10am · Zumba 11am. <strong>Sunday:</strong> Yoga 10am · Pilates 11am.</p>

<h2 class="art-pass__sub">Text C — City University Student Accommodation</h2>
<p>First-year undergraduates are guaranteed a place in halls if they apply before <strong>1 August</strong>. Standard rooms include a bed, desk, wardrobe, shared kitchen and shared bathroom facilities. En-suite rooms include a private bathroom and cost <strong>£40</strong> per week more than a standard room. A deposit of <strong>£300</strong> is required; this is refunded within twenty-eight days of vacating the room provided there is no damage. Students who wish to leave before the end of their contract must give <strong>eight</strong> weeks’ written notice. The residences are entirely non-smoking and pets are not allowed.</p>
"""

PART2_HTML = """
<p class="art-pass__kicker">Part 2 · Workplace</p>
<h1 class="art-pass__title">Flexible working in the modern workplace</h1>

<p><strong>Paragraph 1</strong><br>
Flexible and hybrid working arrangements have moved from marginal experiments to mainstream policy in many organisations. Managers now balance employee preferences, operational coverage, and legal duties when designing rosters, while workers negotiate boundaries between home and office in ways that would have seemed radical a generation ago.</p>

<p><strong>Paragraph 2</strong><br>
Research by the Chartered Institute of Personnel and Development (CIPD) has repeatedly linked flexible working patterns with lower absenteeism and higher job satisfaction, especially where employees can choose start and finish times within agreed windows. The effect is strongest in knowledge-based sectors where output is measured by results rather than physical presence.</p>

<p><strong>Paragraph 3</strong><br>
A widely cited McKinsey survey found that more than <strong>80%</strong> of employees who had worked remotely during major office closures wished to continue with at least partial remote work once restrictions eased. Employers interpreted this as pressure to retain talent, though some also worried about collaboration and mentoring for junior staff.</p>

<p><strong>Paragraph 4</strong><br>
In the United Kingdom, employees have a statutory right to <em>request</em> flexible working after <strong>26</strong> weeks of continuous employment; however, employers are not legally obligated to grant every request. They must consider requests seriously and may refuse only where there is a clear business reason. Critics argue that uneven managerial discretion produces inconsistent outcomes across teams.</p>

<p><strong>Paragraph 5</strong><br>
Alongside benefits, commentators highlight risks of an “always-on” culture, where blurred boundaries lengthen working hours and increase stress. Some organisations have introduced “right to disconnect” guidance, but enforcement remains informal compared with stronger regulatory approaches seen in several <strong>Scandinavian</strong> countries, where employers often face stricter obligations to accommodate flexible schedules.</p>

<p><strong>Paragraph 6</strong><br>
Few analysts expect a full return to rigid nine-to-five routines for every role. Instead, hybrid models are likely to persist, shaped by sector norms, office costs, and evolving legal frameworks. International comparisons suggest that cultural attitudes to trust and measurement will remain as influential as formal legislation.</p>
"""

PART3_HTML = """
<p class="art-pass__kicker">Part 3 · Academic reading</p>
<h1 class="art-pass__title">The cognitive benefits of bilingualism</h1>

<p><strong>A</strong><br>
For much of the twentieth century, bilingualism was often portrayed as a cognitive burden. Early studies suggested that children who grew up with two languages might be slower to acquire vocabulary in each language and might perform less well on standardised tests. Later research questioned these conclusions, pointing to methodological flaws and to the social disadvantages that many bilingual children faced rather than language processing itself.</p>

<p><strong>B</strong><br>
Ellen Bialystok and colleagues at York University in Canada reported that bilingual adults often outperform monolingual peers on tasks that measure <strong>executive</strong> function — the mental skills involved in switching attention, inhibiting irrelevant information, and holding information in working memory. Bilinguals must constantly manage two active language systems, and this everyday practice may strengthen cognitive control circuits.</p>

<p><strong>C</strong><br>
Longitudinal studies in Canada, Spain, and India have claimed that lifelong bilingualism may delay the onset of dementia symptoms by around four to five years compared with monolingual individuals matched for education and other risk factors. The proposed mechanism is that managing two languages builds “cognitive reserve,” allowing the brain to cope longer with neurodegenerative change.</p>

<p><strong>D</strong><br>
Not all findings align. Large-scale analyses, including studies drawing on Scottish health records, have sometimes failed to replicate the dementia-delay effect. Some researchers argue that <strong>publication</strong> bias — the tendency for statistically significant or dramatic results to be published more often — may have inflated early claims. Others note that bilingualism is entangled with migration, education, and socioeconomic variables that are difficult to disentangle fully.</p>

<p><strong>E</strong><br>
Neuroimaging studies have reported greater <strong>grey</strong> matter density in the inferior parietal cortex among bilinguals relative to monolinguals in some samples, although effect sizes vary. Such structural differences are suggestive rather than conclusive, and it remains unclear how directly they translate into everyday cognitive performance.</p>

<p><strong>F</strong><br>
Economists at the University of Guelph have estimated that, in parts of Canada, bilingual employees enjoy a wage <strong>premium</strong> of roughly three to seven percent compared with otherwise similar monolingual workers, depending on industry and the languages involved. The premium may reflect productivity, access to broader markets, or employer perceptions of flexibility.</p>

<p><strong>G</strong><br>
Educational systems in Canada, Spain, and the United States have expanded <strong>immersion</strong> programmes in which children study academic subjects through a second language. Reviews generally suggest that, when programmes are well resourced, students achieve comparable academic outcomes to peers in single-language tracks while gaining high proficiency in two languages — outcomes that policymakers increasingly view as economically and socially valuable.</p>
"""

INSTRUCTIONS = {
    1: "Part 1: Read three short texts (A, B, C). Q1–5: Matching. Q6–9: True/False/Not Given. Q10–14: Sentence completion.",
    2: "Part 2: Read the passage on flexible working. Q15–20: Yes/No/Not Given. Q21–23: Sentence completion. Q24–27: Multiple choice.",
    3: "Part 3: Read the academic article on bilingualism. Q28–32: Matching paragraphs (A–G). Q33–36: Multiple choice. Q37–40: Summary completion.",
}

PART_META = {
    1: {"label": "Part 1", "subtitle": "Notices & accommodation", "q_start": 1, "q_end": 14},
    2: {"label": "Part 2", "subtitle": "Flexible working", "q_start": 15, "q_end": 27},
    3: {"label": "Part 3", "subtitle": "Bilingualism", "q_start": 28, "q_end": 40},
}


def _q(
    qid: int,
    part: int,
    qtype: str,
    section_heading: str,
    section_subtype: str,
    instruction: str,
    prompt: str,
    options: list[str] | None,
    correct: str,
    accepted: list[str] | None = None,
    explanation: str = "",
    summary_html: str | None = None,
):
    return {
        "id": qid,
        "part": part,
        "type": qtype,
        "section_heading": section_heading,
        "section_subtype": section_subtype,
        "instruction": instruction,
        "prompt": prompt,
        "options": options or [],
        "correct": correct,
        "accepted": accepted or [correct],
        "explanation": explanation,
        "summary_html": summary_html,
    }


QUESTIONS = [
    _q(
        1,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a weekly timetable listing named exercise classes",
        ["A", "B", "C"],
        "B",
        None,
        "Text B lists the weekly class schedule.",
    ),
    _q(
        2,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "different membership tiers that change how many items may be borrowed",
        ["A", "B", "C"],
        "A",
        None,
        "Text A contrasts standard and premium borrowing limits.",
    ),
    _q(
        3,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a higher weekly charge for a room with its own bathroom",
        ["A", "B", "C"],
        "C",
        None,
        "Text C states en-suite rooms cost more per week.",
    ),
    _q(
        4,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a rule that younger customers cannot attend certain high-intensity classes",
        ["A", "B", "C"],
        "B",
        None,
        "Text B excludes under-16s from HIIT and Boxercise.",
    ),
    _q(
        5,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a guarantee of housing for new students if they apply by a stated summer date",
        ["A", "B", "C"],
        "C",
        None,
        "Text C guarantees first-years a place if they apply before 1 August.",
    ),
    _q(
        6,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "Premium library members never pay late fines.",
        ["True", "False", "Not Given"],
        "False",
        None,
        "They have a seven-day grace period, not unlimited exemption.",
    ),
    _q(
        7,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "Pilates is offered at Northfield Sports Centre on both Wednesday and Sunday.",
        ["True", "False", "Not Given"],
        "True",
        None,
        "Wednesday lists Pilates 9am; Sunday lists Pilates 11am.",
    ),
    _q(
        8,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "City University refunds the accommodation deposit immediately on the day a student moves out.",
        ["True", "False", "Not Given"],
        "False",
        None,
        "Refund is within twenty-eight days of vacating, not the same day.",
    ),
    _q(
        9,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "Westbridge Public Library charges standard members a joining fee.",
        ["True", "False", "Not Given"],
        "False",
        None,
        "Standard membership is free for residents.",
    ),
    _q(
        10,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "Standard library members may borrow up to _____ items at any time.",
        None,
        "eight",
        ["eight", "8"],
        "Text A specifies up to eight items.",
    ),
    _q(
        11,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "Premium library membership costs £_____ per year.",
        None,
        "25",
        ["25"],
        "Text A states £25 per year.",
    ),
    _q(
        12,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "The accommodation deposit for halls is £_____.",
        None,
        "300",
        ["300"],
        "Text C gives £300.",
    ),
    _q(
        13,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "Students leaving early must give _____ weeks’ written notice.",
        None,
        "eight",
        ["eight", "8"],
        "Text C requires eight weeks’ notice.",
    ),
    _q(
        14,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "The no-show fee for late class cancellation is £_____.",
        None,
        "3",
        ["3"],
        "Text B states a £3 no-show fee.",
    ),
    _q(
        15,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "UK employers must approve every flexible working request they receive.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 4: employers are not obligated to grant every request.",
    ),
    _q(
        16,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "CIPD research has associated flexible working with fewer staff absences.",
        ["Yes", "No", "Not Given"],
        "Yes",
        None,
        "Paragraph 2 links flexible patterns with lower absenteeism.",
    ),
    _q(
        17,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "Fewer than half of surveyed remote workers wanted any remote work to continue.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 3: over 80% wished to continue at least partial remote work.",
    ),
    _q(
        18,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "Scandinavian countries are described as having weaker employer obligations than the UK.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 5 states Scandinavian employers often face stricter obligations.",
    ),
    _q(
        19,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "The writer argues that an “always-on” culture is entirely beneficial for productivity.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 5 presents risks and stress linked to always-on culture.",
    ),
    _q(
        20,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "The writer believes every industry will return to fixed nine-to-five schedules soon.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 6 says few analysts expect a full return for every role.",
    ),
    _q(
        21,
        2,
        "gap",
        "Questions 21–23",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "In the UK, employees may request flexible working after _____ weeks of continuous employment.",
        None,
        "26",
        ["26"],
        "Paragraph 4 gives 26 weeks.",
    ),
    _q(
        22,
        2,
        "gap",
        "Questions 21–23",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "CIPD research linked flexible working with higher job _____.",
        None,
        "satisfaction",
        ["satisfaction"],
        "Paragraph 2 mentions higher job satisfaction.",
    ),
    _q(
        23,
        2,
        "gap",
        "Questions 21–23",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "McKinsey found that more than _____% of remote workers wanted at least partial remote work to continue.",
        None,
        "80",
        ["80"],
        "Paragraph 3 states more than 80%.",
    ),
    _q(
        24,
        2,
        "mc",
        "Questions 24–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "According to the passage, what is one risk linked to flexible and remote working?",
        [
            "A. A guaranteed reduction in overall working hours",
            "B. Junior staff may receive less mentoring",
            "C. Employers lose all legal duties to consider requests",
            "D. CIPD data show higher absenteeism in hybrid models",
        ],
        "B",
        None,
        "Paragraph 3 mentions worries about collaboration and mentoring for junior staff.",
    ),
    _q(
        25,
        2,
        "mc",
        "Questions 24–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "UK employers who refuse a flexible working request must",
        [
            "A. offer the same arrangement to every employee",
            "B. show a clear business reason",
            "C. pay compensation automatically",
            "D. obtain approval from the CIPD",
        ],
        "B",
        None,
        "Paragraph 4: refusal only where there is a clear business reason.",
    ),
    _q(
        26,
        2,
        "mc",
        "Questions 24–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "The writer uses Scandinavian countries mainly to illustrate",
        [
            "A. identical legal rules to the UK",
            "B. weaker trade unions than in the UK",
            "C. stricter expectations on employers in some contexts",
            "D. lower demand for remote work",
        ],
        "C",
        None,
        "Paragraph 5 contrasts stricter regulatory approaches in Scandinavia.",
    ),
    _q(
        27,
        2,
        "mc",
        "Questions 24–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "What does the writer suggest about hybrid models?",
        [
            "A. They will disappear once office rents fall",
            "B. They are likely to continue for many roles",
            "C. They are illegal outside knowledge-based sectors",
            "D. They remove the need for any managerial discretion",
        ],
        "B",
        None,
        "Paragraph 6 states hybrid models are likely to persist.",
    ),
    _q(
        28,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "evidence that bilingual employees in some labour markets earn more than comparable monolinguals",
        ["A", "B", "C", "D", "E", "F", "G"],
        "F",
        None,
        "Paragraph F discusses the wage premium.",
    ),
    _q(
        29,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "a reason some large datasets have not supported an earlier clinical claim",
        ["A", "B", "C", "D", "E", "F", "G"],
        "D",
        None,
        "Paragraph D discusses failed replication and publication bias.",
    ),
    _q(
        30,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "a description of bilingualism once being seen as harmful to children’s thinking",
        ["A", "B", "C", "D", "E", "F", "G"],
        "A",
        None,
        "Paragraph A describes early negative portrayals.",
    ),
    _q(
        31,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "examples of school systems teaching subjects through a second language",
        ["A", "B", "C", "D", "E", "F", "G"],
        "G",
        None,
        "Paragraph G discusses immersion programmes.",
    ),
    _q(
        32,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "neuroimaging findings related to brain structure in bilinguals",
        ["A", "B", "C", "D", "E", "F", "G"],
        "E",
        None,
        "Paragraph E reports grey matter density differences.",
    ),
    _q(
        33,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "According to Bialystok’s line of research (Paragraph B), bilingual adults often perform better on tasks that measure",
        [
            "A. vocabulary size in each language",
            "B. executive function",
            "C. long-term memory for faces",
            "D. simple reaction speed only",
        ],
        "B",
        None,
        "Paragraph B explicitly mentions executive function.",
    ),
    _q(
        34,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "The writer’s main purpose in Paragraph D is to",
        [
            "A. prove bilingualism always delays dementia",
            "B. argue imaging studies are never reliable",
            "C. show that findings about bilingualism and dementia are contested",
            "D. dismiss all non-UK research on bilingualism",
        ],
        "C",
        None,
        "Paragraph D presents conflicting evidence and caveats.",
    ),
    _q(
        35,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "Paragraph E implies that differences in grey matter density",
        [
            "A. guarantee higher IQ scores",
            "B. are observed in every bilingual without exception",
            "C. are suggestive but not conclusive for everyday performance",
            "D. only occur before the age of ten",
        ],
        "C",
        None,
        "Paragraph E says suggestive rather than conclusive.",
    ),
    _q(
        36,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "According to Paragraph G, reviews of well-resourced immersion programmes suggest that students",
        [
            "A. fall permanently behind in academic subjects",
            "B. achieve comparable academic outcomes while gaining two languages",
            "C. must abandon their first language to succeed",
            "D. perform worse than peers in all US states",
        ],
        "B",
        None,
        "Paragraph G states comparable academic outcomes.",
    ),
    _q(
        37,
        3,
        "summary",
        "Questions 37–40",
        "Summary completion",
        "Complete the summary. Choose NO MORE THAN ONE WORD from the passage for each answer.",
        "",
        None,
        "executive",
        ["executive"],
        "Paragraph B highlights executive function.",
        None,
    ),
    _q(
        38,
        3,
        "summary",
        "Questions 37–40",
        "Summary completion",
        "Complete the summary. Choose NO MORE THAN ONE WORD from the passage for each answer.",
        "",
        None,
        "burden",
        ["burden"],
        "Paragraph A describes bilingualism as a cognitive burden.",
        None,
    ),
    _q(
        39,
        3,
        "summary",
        "Questions 37–40",
        "Summary completion",
        "Complete the summary. Choose NO MORE THAN ONE WORD from the passage for each answer.",
        "",
        None,
        "publication",
        ["publication"],
        "Paragraph D mentions publication bias.",
        None,
    ),
    _q(
        40,
        3,
        "summary",
        "Questions 37–40",
        "Summary completion",
        "Complete the summary. Choose NO MORE THAN ONE WORD from the passage for each answer.",
        "",
        None,
        "premium",
        ["premium"],
        "Paragraph F discusses a wage premium.",
        None,
    ),
]

SUMMARY_INTRO_HTML = """
<p class="art-sum-intro">Bialystok’s programme of research suggests bilinguals can excel on tasks involving <span class="art-sum-slot" data-q="37" tabindex="0">37</span> control. Historical work in Paragraph A claimed bilingualism could impose a cognitive <span class="art-sum-slot" data-q="38" tabindex="0">38</span>. More recent large-scale analyses in Paragraph D raise concerns about <span class="art-sum-slot" data-q="39" tabindex="0">39</span> bias affecting which studies reach print. Separately, labour-market evidence in Paragraph F links bilingualism to a wage <span class="art-sum-slot" data-q="40" tabindex="0">40</span>.</p>
"""


def band_from_score(score: int) -> str:
    if score >= 39:
        return "9.0"
    if score >= 37:
        return "8.5"
    if score >= 35:
        return "8.0"
    if score >= 33:
        return "7.5"
    if score >= 30:
        return "7.0"
    if score >= 27:
        return "6.5"
    if score >= 23:
        return "6.0"
    if score >= 19:
        return "5.5"
    if score >= 15:
        return "5.0"
    return "Below 5.0"


def _norm_gap(s: str) -> str:
    t = (s or "").strip().lower().replace("£", "")
    return t


def answer_matches(q: dict, raw: str) -> bool:
    if q["type"] in ("match", "tfng", "ynng", "para_match", "mc"):
        return (raw or "").strip().lower() == (q["correct"] or "").strip().lower()
    opts = [_norm_gap(x) for x in (q.get("accepted") or [q["correct"]])]
    return _norm_gap(raw) in opts


def score_answers(answers: dict) -> tuple[int, int, int, int]:
    """Return total score and part1, part2, part3 sub-scores."""
    p1 = p2 = p3 = 0
    for q in QUESTIONS:
        qid = str(q["id"])
        raw = answers.get(qid, "")
        ok = answer_matches(q, raw)
        if not ok:
            continue
        if q["part"] == 1:
            p1 += 1
        elif q["part"] == 2:
            p2 += 1
        else:
            p3 += 1
    return p1 + p2 + p3, p1, p2, p3


def default_skill_for_question(q: dict) -> str:
    """Maps question type → reading skill label (results breakdown)."""
    t = q["type"]
    if t == "tfng":
        return "Identifying T/F/NG"
    if t == "ynng":
        return "Identifying writer's view"
    if t in ("gap", "summary"):
        return "Recognising paraphrase"
    if t == "mc":
        return "Reading for gist (MC)"
    return "Scanning for detail"


def enrich_question_for_client(q: dict) -> dict:
    """Attach skill + results-only strings; does not change scoring keys."""
    d = dict(q)
    meta = RESULT_META_BY_ID.get(int(q["id"]), {})
    d["skill"] = meta.get("skill") or default_skill_for_question(q)
    d["why_wrong"] = (meta.get("why_wrong") or "You missed a key detail in the passage").strip()
    d["passage_ref"] = (meta.get("passage_ref") or d.get("explanation") or "").strip()
    d["common_mistake"] = (meta.get("common_mistake") or "").strip()
    return d


def get_client_test_payload() -> dict:
    """Full payload for authenticated test page (includes correct for instant Check UI)."""
    return {
        "testTitleBar": "IELTS Academic Reading · Test 1",
        "timeLimitSeconds": 60 * 60,
        "passages": {"1": PART1_HTML.strip(), "2": PART2_HTML.strip(), "3": PART3_HTML.strip()},
        "instructions": INSTRUCTIONS,
        "partMeta": PART_META,
        "summaryIntroHtml": SUMMARY_INTRO_HTML.strip(),
        "questions": [enrich_question_for_client(dict(q)) for q in QUESTIONS],
        "resultsMeta": {
            "part1Title": "Part 1 — Notices & accommodation",
            "part2Title": "Part 2 — Flexible working",
            "part3Title": "Part 3 — Bilingualism",
        },
    }
