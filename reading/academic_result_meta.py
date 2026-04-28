"""
Per-question UI metadata for IELTS Academic Reading Test 1 results (why_wrong tags,
passage quotes, optional common_mistake). Does not affect scoring.
"""

from __future__ import annotations

# why_wrong / passage_ref / common_mistake per question id (1–40).
RESULT_META_BY_ID: dict[int, dict[str, str]] = {
    1: {
        "why_wrong": "You chose the right topic but the wrong text",
        "passage_ref": "The weekly timetable is as follows. Monday: Yoga 7am · Spinning 9am · Pilates 12pm · Boxercise 6pm. Tuesday: Aqua aerobics 8am · Yoga 10am · HIIT 5:30pm · Zumba 7pm.",
        "common_mistake": "For matching, scan each text for the exact idea in the statement—similar topics in two texts are a classic trap.",
    },
    2: {
        "why_wrong": "You chose the wrong text entirely",
        "passage_ref": "Standard membership is free for all Westbridge residents. You may borrow up to eight items at any time. Premium membership costs £25 per year and allows you to borrow up to fifteen items.",
        "common_mistake": "",
    },
    3: {
        "why_wrong": "You missed a key detail in the passage",
        "passage_ref": "En-suite rooms include a private bathroom and cost £40 per week more than a standard room.",
        "common_mistake": "",
    },
    4: {
        "why_wrong": "You chose the wrong text entirely",
        "passage_ref": "Under-16s are not permitted in HIIT or Boxercise sessions.",
        "common_mistake": "",
    },
    5: {
        "why_wrong": "You chose the right topic but the wrong text",
        "passage_ref": "First-year undergraduates are guaranteed a place in halls if they apply before 1 August.",
        "common_mistake": "",
    },
    6: {
        "why_wrong": "Watch for absolute words like all/never/always",
        "passage_ref": "Premium members benefit from a seven-day grace period before fines begin. Late fines are 20p per item per day for standard members.",
        "common_mistake": "IELTS often uses 'never' or 'all'—check whether the passage gives an exception (here, a grace period) before choosing True.",
    },
    7: {
        "why_wrong": "You confused two similar concepts",
        "passage_ref": "Wednesday: Spinning 7am · Pilates 9am · Yoga 12pm · Boxercise 6pm. Sunday: Yoga 10am · Pilates 11am.",
        "common_mistake": "",
    },
    8: {
        "why_wrong": "You missed a key detail — the time frame",
        "passage_ref": "A deposit of £300 is required; this is refunded within twenty-eight days of vacating the room provided there is no damage.",
        "common_mistake": "Phrases like 'the same day' or 'immediately' are often False when the passage gives a specific number of days.",
    },
    9: {
        "why_wrong": "You missed the geographic or age limitation",
        "passage_ref": "Standard membership is free for all Westbridge residents. You may borrow up to eight items at any time.",
        "common_mistake": "IELTS passages often restrict benefits to a specific group. Statements that broaden the group (e.g. 'all UK') are usually False.",
    },
    10: {
        "why_wrong": "You used a number instead of the word from the passage",
        "passage_ref": "You may borrow up to eight items at any time.",
        "common_mistake": "If instructions say ONE WORD AND/OR A NUMBER, both may be acceptable—but when the passage uses a word, examiners often expect that form.",
    },
    11: {
        "why_wrong": "You recalled the wrong number",
        "passage_ref": "Premium membership costs £25 per year and allows you to borrow up to fifteen items.",
        "common_mistake": "",
    },
    12: {
        "why_wrong": "You missed a key detail in the passage",
        "passage_ref": "A deposit of £300 is required; this is refunded within twenty-eight days of vacating the room provided there is no damage.",
        "common_mistake": "",
    },
    13: {
        "why_wrong": "You recalled the wrong number",
        "passage_ref": "Students who wish to leave before the end of their contract must give eight weeks’ written notice.",
        "common_mistake": "",
    },
    14: {
        "why_wrong": "You missed a key detail in the passage",
        "passage_ref": "Cancellations must be made at least two hours before the class begins; otherwise a £3 no-show fee applies.",
        "common_mistake": "",
    },
    15: {
        "why_wrong": "The passage says the opposite",
        "passage_ref": "In the United Kingdom, employees have a statutory right to request flexible working after 26 weeks of continuous employment; however, employers are not legally obligated to grant every request.",
        "common_mistake": "Yes/No/Not Given tests the writer's view—'must approve every request' is stronger than the law described.",
    },
    16: {
        "why_wrong": "You confused facts with the writer's view",
        "passage_ref": "Research by the Chartered Institute of Personnel and Development (CIPD) has repeatedly linked flexible working patterns with lower absenteeism and higher job satisfaction.",
        "common_mistake": "",
    },
    17: {
        "why_wrong": "The passage says the opposite",
        "passage_ref": "A widely cited McKinsey survey found that more than 80% of employees who had worked remotely during major office closures wished to continue with at least partial remote work once restrictions eased.",
        "common_mistake": "Watch the direction of comparisons ('more than half' vs 'fewer than half')—one word can flip Yes to No.",
    },
    18: {
        "why_wrong": "You confused two similar concepts",
        "passage_ref": "Some organisations have introduced 'right to disconnect' guidance, but enforcement remains informal compared with stronger regulatory approaches seen in several Scandinavian countries.",
        "common_mistake": "Scandinavian countries are used here as an example of stricter obligations—not weaker ones than the UK.",
    },
    19: {
        "why_wrong": "Don't confuse facts with opinions",
        "passage_ref": "Commentators highlight risks of an 'always-on' culture, where blurred boundaries lengthen working hours and increase stress.",
        "common_mistake": "",
    },
    20: {
        "why_wrong": "The passage says the opposite",
        "passage_ref": "Few analysts expect a full return to rigid nine-to-five routines for every role.",
        "common_mistake": "",
    },
    21: {
        "why_wrong": "You recalled the wrong number",
        "passage_ref": "In the United Kingdom, employees have a statutory right to request flexible working after 26 weeks of continuous employment.",
        "common_mistake": "",
    },
    22: {
        "why_wrong": "You used a word not in the passage",
        "passage_ref": "Research by the Chartered Institute of Personnel and Development (CIPD) has repeatedly linked flexible working patterns with lower absenteeism and higher job satisfaction.",
        "common_mistake": "",
    },
    23: {
        "why_wrong": "You recalled the wrong number",
        "passage_ref": "A widely cited McKinsey survey found that more than 80% of employees who had worked remotely during major office closures wished to continue with at least partial remote work once restrictions eased.",
        "common_mistake": "",
    },
    24: {
        "why_wrong": "You missed the writer's main concern in that paragraph",
        "passage_ref": "Employers interpreted this as pressure to retain talent, though some also worried about collaboration and mentoring for junior staff.",
        "common_mistake": "",
    },
    25: {
        "why_wrong": "You eliminated the correct option too early",
        "passage_ref": "They must consider requests seriously and may refuse only where there is a clear business reason.",
        "common_mistake": "For MC, rule out distractors that use absolute words ('all', 'never') when the passage is more qualified.",
    },
    26: {
        "why_wrong": "You missed the contrast the writer draws",
        "passage_ref": "Enforcement remains informal compared with stronger regulatory approaches seen in several Scandinavian countries.",
        "common_mistake": "",
    },
    27: {
        "why_wrong": "You missed the writer's conclusion",
        "passage_ref": "Instead, hybrid models are likely to persist, shaped by sector norms, office costs, and evolving legal frameworks.",
        "common_mistake": "",
    },
    28: {
        "why_wrong": "You chose the wrong paragraph entirely",
        "passage_ref": "Economists at the University of Guelph have estimated that, in parts of Canada, bilingual employees enjoy a wage premium of roughly three to seven percent compared with otherwise similar monolingual workers.",
        "common_mistake": "Labour-market evidence is often in a late paragraph—match the idea (wages), not a single keyword in an earlier paragraph.",
    },
    29: {
        "why_wrong": "You missed replication concerns raised in the passage",
        "passage_ref": "Some researchers argue that publication bias — the tendency for statistically significant or dramatic results to be published more often — may have inflated early claims.",
        "common_mistake": "Publication bias and selection bias sound similar but mean different things in methodology questions.",
    },
    30: {
        "why_wrong": "You chose the wrong paragraph entirely",
        "passage_ref": "For much of the twentieth century, bilingualism was often portrayed as a cognitive burden.",
        "common_mistake": "",
    },
    31: {
        "why_wrong": "You chose the wrong paragraph entirely",
        "passage_ref": "Educational systems in Canada, Spain, and the United States have expanded immersion programmes in which children study academic subjects through a second language.",
        "common_mistake": "",
    },
    32: {
        "why_wrong": "You confused two similar concepts",
        "passage_ref": "Neuroimaging studies have reported greater grey matter density in the inferior parietal cortex among bilinguals relative to monolinguals in some samples.",
        "common_mistake": "",
    },
    33: {
        "why_wrong": "You missed the key term in the paragraph",
        "passage_ref": "Bilingual adults often outperform monolingual peers on tasks that measure executive function — the mental skills involved in switching attention, inhibiting irrelevant information, and holding information in working memory.",
        "common_mistake": "",
    },
    34: {
        "why_wrong": "You missed the writer's purpose in that paragraph",
        "passage_ref": "Not all findings align. Large-scale analyses, including studies drawing on Scottish health records, have sometimes failed to replicate the dementia-delay effect.",
        "common_mistake": "When the question asks about the writer's purpose, look for what the paragraph adds to the argument—not isolated vocabulary.",
    },
    35: {
        "why_wrong": "You chose an option stronger than the passage allows",
        "passage_ref": "Such structural differences are suggestive rather than conclusive, and it remains unclear how directly they translate into everyday cognitive performance.",
        "common_mistake": "",
    },
    36: {
        "why_wrong": "You missed the outcome described in the passage",
        "passage_ref": "Reviews generally suggest that, when programmes are well resourced, students achieve comparable academic outcomes to peers in single-language tracks while gaining high proficiency in two languages.",
        "common_mistake": "",
    },
    37: {
        "why_wrong": "You used a similar but different word",
        "passage_ref": "Bilingual adults often outperform monolingual peers on tasks that measure executive function — the mental skills involved in switching attention, inhibiting irrelevant information, and holding information in working memory.",
        "common_mistake": "Summary gaps must be exact words from the passage—check spelling and word form (e.g. executive, not control).",
    },
    38: {
        "why_wrong": "You used a word not in the passage",
        "passage_ref": "Early studies suggested that children who grew up with two languages might be slower to acquire vocabulary in each language and might perform less well on standardised tests.",
        "common_mistake": "",
    },
    39: {
        "why_wrong": "You confused two similar concepts",
        "passage_ref": "Some researchers argue that publication bias — the tendency for statistically significant or dramatic results to be published more often — may have inflated early claims.",
        "common_mistake": "Do not confuse 'selection bias' with 'publication bias'—the passage names publication bias explicitly.",
    },
    40: {
        "why_wrong": "You used a similar but different word",
        "passage_ref": "Bilingual employees enjoy a wage premium of roughly three to seven percent compared with otherwise similar monolingual workers.",
        "common_mistake": "A wage premium is extra pay for the same role; a wage gap compares groups—here the answer is premium.",
    },
}
