"""
Hardcoded payload for IELTS Academic Reading Test 1 (client + server scoring).
"""
from __future__ import annotations

from .academic_result_meta import RESULT_META_BY_ID

PART1_HTML = """
<p class="art-pass__kicker">Part 1 · Materials science history</p>
<h1 class="art-pass__title">Roman concrete and the durability of ancient structures</h1>

<p><strong>A</strong><br>
Concrete is often regarded as a modern industrial material, yet Roman builders developed a related technology more than two thousand years ago. Their construction mixture was used in buildings, bridges, aqueducts and harbour works across a vast empire. Many surviving structures have endured earthquakes, salt spray and long periods of abandonment, prompting scientists to reconsider assumptions about ancient engineering. Roman concrete was not identical to modern Portland-cement concrete, whose manufacture depends on precisely controlled heating and standardized ingredients. Instead, it emerged from practical knowledge of local geology, repeated experimentation and the demands of ambitious public construction. Historians of technology now treat these projects as evidence that large-scale materials innovation can arise outside laboratory settings, provided craft communities share and refine successful practices over generations.</p>

<p><strong>B</strong><br>
The essential dry component was a volcanic ash called <strong>pozzolan</strong>, named after deposits near the Italian town of Pozzuoli. Builders combined this powder with lime produced by heating limestone, then added water and fragments of stone, brick or ceramic. These larger fragments formed the mixture's <strong>aggregate</strong>, giving bulk to the material while the lime-and-ash paste bound everything together. Contemporary writers, including Vitruvius, described the value of certain volcanic soils, although they did not possess a modern account of the chemical reactions involved. The ash was especially useful because it reacted with lime in water, gradually creating durable mineral compounds.</p>

<p><strong>C</strong><br>
Roman engineers did not rely upon one universal recipe. Material choices varied according to the purpose of a structure and the resources available nearby. In ordinary walls, builders often used rubble selected for convenience, whereas monumental projects could incorporate carefully graded stones and layers of brick. Research on the dome of the Pantheon suggests that its upper sections contained lighter volcanic rock, reducing the load carried by the supporting walls. Archaeological sampling elsewhere shows similar layering strategies in vaults and terraces, reinforcing the view that weight was managed deliberately. Such variation indicates that Roman construction was neither crude nor accidental. It involved choices about weight, strength and workability, even when those choices were expressed through craft traditions rather than formal scientific theory.</p>

<p><strong>D</strong><br>
Marine structures have attracted particular attention because several Roman harbours remain stable after centuries of contact with waves. For these works, builders placed a lime-and-ash mixture into wooden forms beneath the surface, where it hardened in contact with <strong>seawater</strong>. Modern analyses indicate that dissolved minerals entered the concrete and encouraged the formation of interlocking <strong>crystals</strong>. Rather than merely resisting water, the material may have changed beneficially during prolonged exposure. This finding contrasts with many modern concretes, in which saltwater can penetrate small openings, corrode reinforcing steel and eventually cause visible cracking.</p>

<p><strong>E</strong><br>
One influential investigation examined Roman samples containing conspicuous white particles known as lime clasts. Earlier researchers sometimes interpreted these fragments as evidence that mixing had been incomplete. However, a newer explanation proposes that they may result from the deliberate use of quicklime at high temperatures. When a crack develops, water can reach these reactive pieces, allowing dissolved lime to move into the damaged area and form new mineral material. Laboratory studies have shown that some reconstructed mixtures can close narrow fractures, though this does not mean that every Roman structure automatically repaired itself. The evidence instead suggests a potentially useful mechanism whose effectiveness depended on composition and environmental conditions.</p>

<p><strong>F</strong><br>
The long life of Roman concrete should therefore not be reduced to a single secret ingredient. Its performance reflected the interaction of ash, lime, aggregate, placement methods and the setting in which a building stood. It also benefited from the absence of steel reinforcement, which is often the weak point in contemporary coastal structures. Researchers are now investigating whether lower-temperature cements and locally available industrial by-products could reproduce selected features of the ancient material. Such work is unlikely to replace modern concrete entirely, but it may help reduce the environmental cost of construction, since cement manufacture currently accounts for roughly <strong>8</strong>% of global carbon-dioxide emissions. Even modest gains in durability would matter for bridges, ports and housing that must remain serviceable for decades under harsh conditions.</p>
"""

PART2_HTML = """
<p class="art-pass__kicker">Part 2 · Workplace studies</p>
<h1 class="art-pass__title">Flexible working in the modern workplace</h1>

<p><strong>1</strong><br>
Flexible working describes arrangements that alter when, where or how employees perform their duties. It may include compressed hours, part-time schedules, remote work, job sharing and employee-controlled start and finish times. Although the expression is frequently associated with digital occupations, it also applies to manufacturing, retail and public services, where flexibility may be organised through shift exchanges or predictable rotas. Its expansion has been encouraged by improved communication technology, demographic change and growing recognition that a standard office-based timetable does not suit every worker or every task.</p>

<p><strong>2</strong><br>
Advocates often argue that adaptable schedules can improve recruitment and retention. Employees with caring responsibilities, lengthy commutes or health conditions may find conventional attendance requirements unnecessarily restrictive. Surveys commonly report higher <strong>satisfaction</strong> among staff who have some influence over their working pattern, although such findings do not establish that flexibility alone produces this outcome. Organisations that introduce these policies may already possess supportive management cultures, making simple comparisons difficult. Nevertheless, many employers view flexible arrangements as one means of widening the pool of potential applicants.</p>

<p><strong>3</strong><br>
The legal position has also shaped discussion. In the United Kingdom, employees have a statutory right to request flexible working after <strong>26</strong> weeks of continuous employment. A request does not create an entitlement to the preferred arrangement: employers can refuse for specified business reasons, such as excessive additional cost or an inability to reorganise work. They must consider applications seriously, yet managers retain discretion. Critics argue that uneven application of that discretion produces inconsistent outcomes across teams. Even so, the formal right has altered expectations by encouraging managers to explain decisions rather than treating conventional hours as the unquestioned default.</p>

<p><strong>4</strong><br>
Difficulties are not confined to managerial resistance. Informal contact can be reduced when colleagues rarely share the same workplace or hours, and newer employees may find it harder to observe professional practices that are usually learned through proximity. Some managers also report uncertainty about evaluating contribution when they cannot rely on physical presence as a visible signal of effort. These concerns do not necessarily demonstrate lower performance, but they suggest that successful hybrid systems require clear objectives, dependable communication and deliberate opportunities for collaboration.</p>

<p><strong>5</strong><br>
Evidence about productivity remains mixed partly because the term covers very different arrangements. A software engineer completing focused coding away from the office faces conditions unlike those of a hospital nurse exchanging shifts with colleagues. Several studies find modest gains where workers have autonomy and suitable equipment, whereas others identify longer working days, blurred boundaries and unequal access to desirable arrangements. The principal issue may therefore be design rather than location. Policies that appear generous on paper can create resentment if senior staff receive discretion while customer-facing employees have little practical choice.</p>

<p><strong>6</strong><br>
For employers, the most credible approach may be to treat flexibility as a continuing organisational process rather than a single benefit. Managers need to identify which duties require simultaneous presence, consult affected teams and review whether opportunities are distributed fairly. The Chartered Institute of Personnel and Development (CIPD) has argued that requests should be considered constructively, but it also notes that implementation requires training and reliable systems. Flexible working is consequently neither a universal remedy nor a temporary concession; its value depends on how carefully it is matched to operational needs and individual circumstances.</p>
"""

PART3_HTML = """
<p class="art-pass__kicker">Part 3 · Cognitive science</p>
<h1 class="art-pass__title">The cognitive benefits of bilingualism</h1>

<p><strong>A</strong><br>
Bilingualism is commonly understood as the regular use of two languages, but this apparently simple definition conceals considerable variation. Some people acquire both languages from infancy, while others learn an additional language through schooling, migration or adult study. Proficiency may be balanced across speaking, reading and listening, or it may be strongly shaped by setting and social purpose. Consequently, researchers increasingly avoid treating bilingual speakers as a uniform group. Questions about cognitive advantage must take account of age of acquisition, frequency of use, literacy, socioeconomic background and the extent to which speakers alternate between languages in daily life.</p>

<p><strong>B</strong><br>
Early research suggested that bilingual speakers might possess superior <strong>executive</strong> control: the collection of processes used to direct attention, suppress irrelevant responses and switch between tasks. The proposal was intuitive. A person who must select one linguistic system while preventing intrusion from another may receive repeated practice in regulating competing information. Experiments using conflict tasks sometimes found that bilingual participants responded more efficiently when distracting signals had to be ignored. These results generated considerable interest because such control is associated with planning, problem solving and the management of complex behaviour.</p>

<p><strong>C</strong><br>
However, the initial evidence was not as decisive as popular accounts implied. Studies reporting an advantage were often small, and later investigations with larger samples produced inconsistent results. <strong>Publication</strong> practices may also have amplified positive findings, since striking outcomes are more likely to appear in journals than null results. In addition, bilingual participants have frequently differed from comparison groups in education, immigration history or cultural experience. Such variables can affect test performance independently of language use, making it difficult to attribute a measured difference to bilingualism itself.</p>

<p><strong>D</strong><br>
The most useful contribution of recent work may be methodological rather than celebratory. Researchers now employ longitudinal designs, preregistration and more detailed descriptions of participants' language histories. Instead of asking whether bilingualism creates one universal mental benefit, they investigate which forms of language experience are associated with which outcomes. Daily switching, for example, may impose a different cognitive <strong>burden</strong> from maintaining separate languages in separate environments. This approach has made the field less likely to offer simple conclusions, but more capable of distinguishing genuine effects from artefacts of sampling and measurement.</p>

<p><strong>E</strong><br>
There is also interest in cognitive ageing. Some clinical studies have reported that bilingual patients receive a dementia diagnosis later than monolingual patients with similar symptoms. One explanation is that sustained linguistic activity contributes to cognitive reserve, allowing individuals to cope with neurological change for longer before impairment becomes apparent. Yet delayed diagnosis is not identical to delayed disease, and it remains uncertain whether language experience changes underlying pathology. Education, occupation, social networks and access to healthcare may all influence both cognitive resilience and the point at which someone seeks clinical assessment.</p>

<p><strong>F</strong><br>
Language use may nevertheless matter in ways that conventional laboratory tasks fail to capture. In conversation, bilingual speakers continuously assess their interlocutor, setting and communicative goal. They may choose a language, mix languages strategically or adjust vocabulary for an audience with uneven knowledge. These practices involve social judgement as well as attention. Their consequences may be subtle, context-dependent and difficult to represent through a short computer-based test. A narrow focus on reaction times may therefore overlook forms of adaptability that are meaningful outside the laboratory.</p>

<p><strong>G</strong><br>
The current consensus is cautious. Bilingualism should not be marketed as a guaranteed route to a cognitive <strong>premium</strong>, but neither should mixed findings be interpreted as evidence that language learning lacks intellectual value. Managing more than one language provides access to relationships, education, employment and cultural participation, benefits that cannot be reduced to a single test score. Future research will need larger and more diverse samples, transparent analysis and repeated measurement across the lifespan. Only then will it be possible to identify when, for whom and under what conditions bilingual experience affects cognition.</p>
"""

INSTRUCTIONS = {
    1: "Part 1: Read the passage about Roman concrete. Q1–5: Matching information (paragraphs A–F). Q6–9: True/False/Not Given. Q10–14: Sentence completion.",
    2: "Part 2: Read the passage about flexible working. Q15–20: Yes/No/Not Given. Q21–23: Sentence completion. Q24–27: Multiple choice.",
    3: "Part 3: Read the academic article on bilingualism. Q28–32: Matching information (paragraphs A–G). Q33–36: Multiple choice. Q37–40: Summary completion.",
}

PART_META = {
    1: {"label": "Part 1", "subtitle": "Roman concrete", "q_start": 1, "q_end": 14},
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
        "para_match",
        "Questions 1–5",
        "Matching information",
        "Which paragraph contains the following information? Choose A–F.",
        "an account of why coastal structures may become stronger during use",
        ["A", "B", "C", "D", "E", "F"],
        "D",
        None,
        "Paragraph D explains mineral growth after prolonged contact with seawater.",
    ),
    _q(
        2,
        1,
        "para_match",
        "Questions 1–5",
        "Matching information",
        "Which paragraph contains the following information? Choose A–F.",
        "a warning against explaining durability by one component alone",
        ["A", "B", "C", "D", "E", "F"],
        "F",
        None,
        "Paragraph F says long life resulted from several interacting factors.",
    ),
    _q(
        3,
        1,
        "para_match",
        "Questions 1–5",
        "Matching information",
        "Which paragraph contains the following information? Choose A–F.",
        "evidence that construction mixtures were adjusted for a building's location or purpose",
        ["A", "B", "C", "D", "E", "F"],
        "C",
        None,
        "Paragraph C describes different material choices for different projects.",
    ),
    _q(
        4,
        1,
        "para_match",
        "Questions 1–5",
        "Matching information",
        "Which paragraph contains the following information? Choose A–F.",
        "a revised interpretation of features once regarded as mistakes",
        ["A", "B", "C", "D", "E", "F"],
        "E",
        None,
        "Paragraph E reinterprets lime clasts as potentially deliberate.",
    ),
    _q(
        5,
        1,
        "para_match",
        "Questions 1–5",
        "Matching information",
        "Which paragraph contains the following information? Choose A–F.",
        "the identification of the principal powdered ingredient",
        ["A", "B", "C", "D", "E", "F"],
        "B",
        None,
        "Paragraph B identifies pozzolan as the volcanic ash.",
    ),
    _q(
        6,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the passage?",
        "Roman builders used exactly the same formula throughout the empire.",
        ["True", "False", "Not Given"],
        "False",
        None,
        "Paragraph C states that recipes varied according to purpose and local resources.",
    ),
    _q(
        7,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the passage?",
        "Vitruvius explained the chemical processes that made volcanic ash effective.",
        ["True", "False", "Not Given"],
        "False",
        None,
        "Paragraph B says contemporary writers did not possess a modern chemical account.",
    ),
    _q(
        8,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the passage?",
        "Some recreated mixtures have sealed small areas of damage under laboratory conditions.",
        ["True", "False", "Not Given"],
        "True",
        None,
        "Paragraph E reports that reconstructed mixtures can close narrow fractures.",
    ),
    _q(
        9,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the passage?",
        "Roman engineers transported volcanic ash from Italy to every province.",
        ["True", "False", "Not Given"],
        "Not Given",
        None,
        "The passage never states how ash was supplied across provinces.",
    ),
    _q(
        10,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "A powder named _____ was combined with lime by ancient builders.",
        None,
        "pozzolan",
        ["pozzolan"],
        "Paragraph B names the volcanic ash pozzolan.",
    ),
    _q(
        11,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "Fragments of stone or ceramic supplied bulk as the _____.",
        None,
        "aggregate",
        ["aggregate"],
        "Paragraph B calls the larger fragments aggregate.",
    ),
    _q(
        12,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "Making this material contributes roughly _____ percent of planetary carbon dioxide output.",
        None,
        "8",
        ["8", "8%"],
        "Paragraph F gives the figure as roughly 8%.",
    ),
    _q(
        13,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "Harbour mixtures hardened after being placed in contact with _____.",
        None,
        "seawater",
        ["seawater", "sea water"],
        "Paragraph D identifies seawater.",
    ),
    _q(
        14,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "Mineral growth produced interlocking _____ within submerged structures.",
        None,
        "crystals",
        ["crystals"],
        "Paragraph D refers to interlocking crystals.",
    ),
    _q(
        15,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "Digital jobs are the only occupations in which adaptable arrangements are possible.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 1 states the idea also applies to manufacturing, retail and public services.",
    ),
    _q(
        16,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "Reported employee contentment proves that schedule choice causes better morale.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 2 says survey findings do not establish that flexibility alone produces the outcome.",
    ),
    _q(
        17,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "A statutory application must be granted if the employee has a strong personal reason.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 3: employers can refuse for specified business reasons.",
    ),
    _q(
        18,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "Physical visibility is a dependable measure of an individual's contribution.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 4 presents presence only as a signal some managers rely on, not as proof of performance.",
    ),
    _q(
        19,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "Every study of home-based work has found a modest increase in output.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 5 states that evidence about productivity remains mixed.",
    ),
    _q(
        20,
        2,
        "ynng",
        "Questions 15–20",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "The CIPD requires organisations to approve all requests for altered schedules.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 6: CIPD argues requests should be considered constructively, not automatically approved.",
    ),
    _q(
        21,
        2,
        "gap",
        "Questions 21–23",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "Staff become entitled to ask for adaptable schedules once they have been employed for _____ weeks.",
        None,
        "26",
        ["26"],
        "Paragraph 3: statutory right after 26 weeks of continuous employment.",
    ),
    _q(
        22,
        2,
        "gap",
        "Questions 21–23",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "Surveys frequently associate employee choice with higher _____.",
        None,
        "satisfaction",
        ["satisfaction"],
        "Paragraph 2 reports higher satisfaction.",
    ),
    _q(
        23,
        2,
        "gap",
        "Questions 21–23",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "A hospital nurse swapping rotas faces conditions unlike those of a _____ engineer coding remotely.",
        None,
        "software",
        ["software"],
        "Paragraph 5 contrasts a software engineer with a hospital nurse.",
    ),
    _q(
        24,
        2,
        "mc",
        "Questions 24–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C or D.",
        "What does the writer suggest makes evidence on output difficult to interpret?",
        [
            "A. Employees usually overstate the number of hours they work",
            "B. The label covers arrangements with substantially different conditions",
            "C. Remote work has only been studied in technology companies",
            "D. Managers use incompatible methods for recording attendance",
        ],
        "B",
        None,
        "Paragraph 5: the term covers very different arrangements.",
    ),
    _q(
        25,
        2,
        "mc",
        "Questions 24–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C or D.",
        "What concern is raised about staff who rarely work alongside colleagues?",
        [
            "A. They may have fewer opportunities to acquire unspoken professional habits",
            "B. They are likely to reject formal performance reviews",
            "C. They may need more expensive communication equipment",
            "D. They usually prefer customer-facing responsibilities",
        ],
        "A",
        None,
        "Paragraph 4: newer employees may find it harder to observe professional practices learned through proximity.",
    ),
    _q(
        26,
        2,
        "mc",
        "Questions 24–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C or D.",
        "Which approach is most consistent with the writer's conclusion?",
        [
            "A. Apply one identical schedule to every role",
            "B. Leave all timing decisions to individual employees",
            "C. Review arrangements against operational demands and fairness",
            "D. Restrict altered schedules to senior employees",
        ],
        "C",
        None,
        "Paragraph 6 recommends consulting teams and reviewing whether opportunities are distributed fairly.",
    ),
    _q(
        27,
        2,
        "mc",
        "Questions 24–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C or D.",
        "Why might apparently generous schemes create resentment?",
        [
            "A. They can give some groups discretion unavailable to others",
            "B. They require employees to work longer contracted hours",
            "C. They make staff responsible for buying their own equipment",
            "D. They prevent managers from discussing workplace needs",
        ],
        "A",
        None,
        "Paragraph 5: resentment if senior staff receive discretion while others have little choice.",
    ),
    _q(
        28,
        3,
        "para_match",
        "Questions 28–32",
        "Matching information",
        "Which paragraph contains the following information? Choose A–G.",
        "an explanation for replacing a broad question with more specific research questions",
        ["A", "B", "C", "D", "E", "F", "G"],
        "D",
        None,
        "Paragraph D describes investigating which forms of experience link to which outcomes.",
    ),
    _q(
        29,
        3,
        "para_match",
        "Questions 28–32",
        "Matching information",
        "Which paragraph contains the following information? Choose A–G.",
        "a reason why comparisons between participant groups can be misleading",
        ["A", "B", "C", "D", "E", "F", "G"],
        "C",
        None,
        "Paragraph C notes differences in education, immigration history and cultural experience.",
    ),
    _q(
        30,
        3,
        "para_match",
        "Questions 28–32",
        "Matching information",
        "Which paragraph contains the following information? Choose A–G.",
        "a limitation of assessing language experience through short experimental exercises",
        ["A", "B", "C", "D", "E", "F", "G"],
        "F",
        None,
        "Paragraph F argues laboratory tasks may miss meaningful real-world adaptability.",
    ),
    _q(
        31,
        3,
        "para_match",
        "Questions 28–32",
        "Matching information",
        "Which paragraph contains the following information? Choose A–G.",
        "a distinction between postponing symptoms and altering a medical condition",
        ["A", "B", "C", "D", "E", "F", "G"],
        "E",
        None,
        "Paragraph E: delayed diagnosis is not identical to delayed disease.",
    ),
    _q(
        32,
        3,
        "para_match",
        "Questions 28–32",
        "Matching information",
        "Which paragraph contains the following information? Choose A–G.",
        "a description of the variety concealed by a common label",
        ["A", "B", "C", "D", "E", "F", "G"],
        "A",
        None,
        "Paragraph A explains the variation concealed by the term bilingualism.",
    ),
    _q(
        33,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C or D.",
        "What was the central idea behind early claims of an advantage?",
        [
            "A. Selecting between languages may exercise attention-management processes",
            "B. Multilingual households provide consistently better schooling",
            "C. Reading in two scripts increases the speed of visual perception",
            "D. Speakers with two languages avoid demanding social situations",
        ],
        "A",
        None,
        "Paragraph B links selecting one linguistic system to practice in regulating competing information.",
    ),
    _q(
        34,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C or D.",
        "Why does the writer mention publication practices?",
        [
            "A. To show that journals refuse to print studies of language",
            "B. To identify a possible source of an overly positive research record",
            "C. To argue that large samples are less useful than small ones",
            "D. To suggest that researchers deliberately conceal results",
        ],
        "B",
        None,
        "Paragraph C: striking outcomes are more likely to appear than null results.",
    ),
    _q(
        35,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C or D.",
        "What does the writer imply about cognitive reserve?",
        [
            "A. It has been proven to prevent neurological damage",
            "B. It may help explain a later clinical identification of impairment",
            "C. It is found only in people who learned languages in childhood",
            "D. It is measured primarily through reaction-time experiments",
        ],
        "B",
        None,
        "Paragraph E presents cognitive reserve as one explanation for later diagnosis.",
    ),
    _q(
        36,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C or D.",
        "Which statement best reflects the writer's overall position?",
        [
            "A. The strongest findings justify promoting language learning as a mental treatment",
            "B. Inconsistent findings make further investigation unnecessary",
            "C. Claims require caution, but the broader value of language learning remains substantial",
            "D. Only perfectly balanced speakers should be included in future studies",
        ],
        "C",
        None,
        "Paragraph G rejects both overclaiming and dismissing bilingualism's wider value.",
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
        "Paragraph B identifies executive control.",
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
        "publication",
        ["publication"],
        "Paragraph C discusses publication practices.",
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
        "burden",
        ["burden"],
        "Paragraph D contrasts cognitive burden across language settings.",
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
        "Paragraph G rejects an automatic cognitive premium.",
    ),
]

SUMMARY_INTRO_HTML = """
<p class="art-sum-intro">Modern scholarship has moved away from a simple claim that using two languages gives everyone the same mental advantage. Earlier work linked language management to <span class="art-sum-slot" data-q="37" tabindex="0">37</span> control, but later studies raised concerns about sampling and selective <span class="art-sum-slot" data-q="38" tabindex="0">38</span>. Researchers now examine whether particular communicative settings create a cognitive <span class="art-sum-slot" data-q="39" tabindex="0">39</span>, while cautioning against describing bilingualism as an automatic intellectual <span class="art-sum-slot" data-q="40" tabindex="0">40</span>.</p>
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


def score_answers(answers: dict, test_number: int = 1) -> tuple[int, int, int, int]:
    """Return total score and part1, part2, part3 sub-scores."""
    from .academic_tests import get_questions as registry_questions

    questions = QUESTIONS if test_number == 1 else registry_questions(test_number)
    if not questions:
        return 0, 0, 0, 0
    p1 = p2 = p3 = 0
    for q in questions:
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


def get_client_test_payload(test_number: int = 1) -> dict:
    """Full payload for authenticated test page (includes correct for instant Check UI)."""
    if test_number != 1:
        from .academic_tests import get_client_payload

        payload = get_client_payload(test_number)
        if payload:
            return payload
    return {
        "testTitleBar": "IELTS Academic Reading · Test 1",
        "timeLimitSeconds": 60 * 60,
        "passages": {"1": PART1_HTML.strip(), "2": PART2_HTML.strip(), "3": PART3_HTML.strip()},
        "instructions": INSTRUCTIONS,
        "partMeta": PART_META,
        "summaryIntroHtml": SUMMARY_INTRO_HTML.strip(),
        "questions": [enrich_question_for_client(dict(q)) for q in QUESTIONS],
        "resultsMeta": {
            "part1Title": "Part 1 — Roman concrete",
            "part2Title": "Part 2 — Flexible working",
            "part3Title": "Part 3 — Bilingualism",
        },
    }
