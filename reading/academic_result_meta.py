"""
Per-question UI metadata for IELTS Academic Reading Test 1 results (why_wrong tags,
passage quotes, optional common_mistake). Does not affect scoring.
"""

from __future__ import annotations

RESULT_META_BY_ID: dict[int, dict[str, str]] = {
    1: {
        "why_wrong": "You chose the wrong paragraph entirely",
        "passage_ref": "Modern analyses indicate that dissolved minerals entered the concrete and encouraged the formation of interlocking crystals. Rather than merely resisting water, the material may have changed beneficially during prolonged exposure.",
        "common_mistake": "Match the idea (beneficial change during marine exposure), not a single keyword like 'harbour'.",
    },
    2: {
        "why_wrong": "You chose the wrong paragraph entirely",
        "passage_ref": "The long life of Roman concrete should therefore not be reduced to a single secret ingredient. Its performance reflected the interaction of ash, lime, aggregate, placement methods and the setting in which a building stood.",
        "common_mistake": "",
    },
    3: {
        "why_wrong": "You chose the wrong paragraph entirely",
        "passage_ref": "Roman engineers did not rely upon one universal recipe. Material choices varied according to the purpose of a structure and the resources available nearby.",
        "common_mistake": "",
    },
    4: {
        "why_wrong": "You missed the reinterpretation of lime clasts",
        "passage_ref": "Earlier researchers sometimes interpreted these fragments as evidence that mixing had been incomplete. However, a newer explanation proposes that they may result from the deliberate use of quicklime at high temperatures.",
        "common_mistake": "",
    },
    5: {
        "why_wrong": "You chose the wrong paragraph entirely",
        "passage_ref": "The essential dry component was a volcanic ash called pozzolan, named after deposits near the Italian town of Pozzuoli.",
        "common_mistake": "",
    },
    6: {
        "why_wrong": "The passage says the opposite",
        "passage_ref": "Roman engineers did not rely upon one universal recipe. Material choices varied according to the purpose of a structure and the resources available nearby.",
        "common_mistake": "Absolute words like 'exactly the same' are often False when the passage describes variation.",
    },
    7: {
        "why_wrong": "The passage says the opposite",
        "passage_ref": "Contemporary writers, including Vitruvius, described the value of certain volcanic soils, although they did not possess a modern account of the chemical reactions involved.",
        "common_mistake": "",
    },
    8: {
        "why_wrong": "You missed the laboratory evidence",
        "passage_ref": "Laboratory studies have shown that some reconstructed mixtures can close narrow fractures.",
        "common_mistake": "",
    },
    9: {
        "why_wrong": "You inferred something the passage never states",
        "passage_ref": "Paragraph B names Italian deposits near Pozzuoli but does not say ash was shipped to every province.",
        "common_mistake": "Not Given means the idea is absent — not merely unspecified in detail.",
    },
    10: {
        "why_wrong": "You used a similar but different word",
        "passage_ref": "The essential dry component was a volcanic ash called pozzolan.",
        "common_mistake": "Gap answers must be the exact word from the passage.",
    },
    11: {
        "why_wrong": "You used a word not in the passage",
        "passage_ref": "These larger fragments formed the mixture's aggregate, giving bulk to the material.",
        "common_mistake": "",
    },
    12: {
        "why_wrong": "You recalled the wrong number",
        "passage_ref": "Cement manufacture currently accounts for roughly 8% of global carbon-dioxide emissions.",
        "common_mistake": "",
    },
    13: {
        "why_wrong": "You used a similar but different word",
        "passage_ref": "It hardened in contact with seawater.",
        "common_mistake": "",
    },
    14: {
        "why_wrong": "You used a similar but different word",
        "passage_ref": "Dissolved minerals entered the concrete and encouraged the formation of interlocking crystals.",
        "common_mistake": "",
    },
    15: {
        "why_wrong": "The passage says the opposite",
        "passage_ref": "Although the expression is frequently associated with digital occupations, it also applies to manufacturing, retail and public services.",
        "common_mistake": "",
    },
    16: {
        "why_wrong": "You treated correlation as proof of cause",
        "passage_ref": "Surveys commonly report higher satisfaction among staff who have some influence over their working pattern, although such findings do not establish that flexibility alone produces this outcome.",
        "common_mistake": "Yes/No/Not Given tests the writer's view — hedged claims are often No when the statement is absolute.",
    },
    17: {
        "why_wrong": "The passage says the opposite",
        "passage_ref": "A request does not create an entitlement to the preferred arrangement: employers can refuse for specified business reasons.",
        "common_mistake": "",
    },
    18: {
        "why_wrong": "You overstated the writer's claim",
        "passage_ref": "Some managers also report uncertainty about evaluating contribution when they cannot rely on physical presence as a visible signal of effort. These concerns do not necessarily demonstrate lower performance.",
        "common_mistake": "",
    },
    19: {
        "why_wrong": "The passage says the opposite",
        "passage_ref": "Evidence about productivity remains mixed partly because the term covers very different arrangements.",
        "common_mistake": "",
    },
    20: {
        "why_wrong": "You overstated what CIPD requires",
        "passage_ref": "The Chartered Institute of Personnel and Development (CIPD) has argued that requests should be considered constructively, but it also notes that implementation requires training and reliable systems.",
        "common_mistake": "",
    },
    21: {
        "why_wrong": "You recalled the wrong number",
        "passage_ref": "In the United Kingdom, employees have a statutory right to request flexible working after 26 weeks of continuous employment.",
        "common_mistake": "",
    },
    22: {
        "why_wrong": "You used a word not in the passage",
        "passage_ref": "Surveys commonly report higher satisfaction among staff who have some influence over their working pattern.",
        "common_mistake": "",
    },
    23: {
        "why_wrong": "You used a word not in the passage",
        "passage_ref": "A software engineer completing focused coding away from the office faces conditions unlike those of a hospital nurse exchanging shifts with colleagues.",
        "common_mistake": "",
    },
    24: {
        "why_wrong": "You missed the writer's explanation for mixed evidence",
        "passage_ref": "Evidence about productivity remains mixed partly because the term covers very different arrangements.",
        "common_mistake": "",
    },
    25: {
        "why_wrong": "You missed the writer's concern about informal learning",
        "passage_ref": "Newer employees may find it harder to observe professional practices that are usually learned through proximity.",
        "common_mistake": "",
    },
    26: {
        "why_wrong": "You missed the writer's conclusion",
        "passage_ref": "Managers need to identify which duties require simultaneous presence, consult affected teams and review whether opportunities are distributed fairly.",
        "common_mistake": "",
    },
    27: {
        "why_wrong": "You missed the cause of resentment",
        "passage_ref": "Policies that appear generous on paper can create resentment if senior staff receive discretion while customer-facing employees have little practical choice.",
        "common_mistake": "",
    },
    28: {
        "why_wrong": "You chose the wrong paragraph entirely",
        "passage_ref": "Instead of asking whether bilingualism creates one universal mental benefit, they investigate which forms of language experience are associated with which outcomes.",
        "common_mistake": "",
    },
    29: {
        "why_wrong": "You chose the wrong paragraph entirely",
        "passage_ref": "Bilingual participants have frequently differed from comparison groups in education, immigration history or cultural experience.",
        "common_mistake": "",
    },
    30: {
        "why_wrong": "You chose the wrong paragraph entirely",
        "passage_ref": "A narrow focus on reaction times may therefore overlook forms of adaptability that are meaningful outside the laboratory.",
        "common_mistake": "",
    },
    31: {
        "why_wrong": "You missed the diagnosis/disease distinction",
        "passage_ref": "Yet delayed diagnosis is not identical to delayed disease, and it remains uncertain whether language experience changes underlying pathology.",
        "common_mistake": "",
    },
    32: {
        "why_wrong": "You chose the wrong paragraph entirely",
        "passage_ref": "Bilingualism is commonly understood as the regular use of two languages, but this apparently simple definition conceals considerable variation.",
        "common_mistake": "",
    },
    33: {
        "why_wrong": "You missed the central early claim",
        "passage_ref": "A person who must select one linguistic system while preventing intrusion from another may receive repeated practice in regulating competing information.",
        "common_mistake": "",
    },
    34: {
        "why_wrong": "You missed why publication practices are mentioned",
        "passage_ref": "Publication practices may also have amplified positive findings, since striking outcomes are more likely to appear in journals than null results.",
        "common_mistake": "",
    },
    35: {
        "why_wrong": "You chose an option stronger than the passage allows",
        "passage_ref": "One explanation is that sustained linguistic activity contributes to cognitive reserve, allowing individuals to cope with neurological change for longer before impairment becomes apparent.",
        "common_mistake": "",
    },
    36: {
        "why_wrong": "You missed the writer's balanced conclusion",
        "passage_ref": "Bilingualism should not be marketed as a guaranteed route to a cognitive premium, but neither should mixed findings be interpreted as evidence that language learning lacks intellectual value.",
        "common_mistake": "",
    },
    37: {
        "why_wrong": "You used a similar but different word",
        "passage_ref": "Early research suggested that bilingual speakers might possess superior executive control.",
        "common_mistake": "Summary gaps must be exact words from the passage.",
    },
    38: {
        "why_wrong": "You used a similar but different word",
        "passage_ref": "Publication practices may also have amplified positive findings.",
        "common_mistake": "",
    },
    39: {
        "why_wrong": "You used a similar but different word",
        "passage_ref": "Daily switching, for example, may impose a different cognitive burden from maintaining separate languages in separate environments.",
        "common_mistake": "",
    },
    40: {
        "why_wrong": "You used a similar but different word",
        "passage_ref": "Bilingualism should not be marketed as a guaranteed route to a cognitive premium.",
        "common_mistake": "",
    },
}
