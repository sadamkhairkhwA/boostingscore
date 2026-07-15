"""Education topic word bank, balanced by part of speech."""

BEGINNER_NOUNS = (
    "curriculum", "literacy", "tuition", "scholarship", "enrolment", "coursework",
    "educator", "assessment", "qualification", "discipline", "knowledge", "skill",
    "syllabus", "lecture", "seminar", "textbook", "learner", "motivation",
    "attendance", "achievement", "compulsory education", "higher education",
    "primary school", "secondary school", "distance learning", "online learning",
    "critical thinking", "learning outcome", "academic performance", "school system",
    "teaching method", "student loan", "exam pressure", "class size",
    "learning environment", "study habit", "peer pressure", "career prospect",
    "lifelong learning", "educational institution",
)
BEGINNER_VERBS = (
    "educate", "learn", "teach", "study", "graduate", "enrol", "assess",
    "memorise", "revise", "motivate", "instruct", "acquire", "attain", "excel",
    "specialise", "comprehend", "encourage", "attend", "supervise", "grasp",
)
BEGINNER_ADJECTIVES = (
    "academic", "educational", "compulsory", "vocational", "practical",
    "theoretical", "knowledgeable", "literate", "disciplined", "motivated",
    "competent", "capable", "diligent", "attentive", "inclusive", "affordable",
    "intellectual", "rigorous", "elective", "formal",
)
BEGINNER_ADVERBS = (
    "academically", "intellectually", "increasingly", "effectively", "formally",
    "critically",
)

STANDARD_NOUNS = (
    "pedagogy", "accreditation", "extracurricular activity", "attainment gap",
    "student engagement", "learning disability", "academic integrity",
    "standardised testing", "educational reform", "vocational training",
    "teaching quality", "dropout rate", "class participation", "grade inflation",
    "educational equity", "school funding", "digital classroom", "blended learning",
    "continuous assessment", "cognitive development", "learning curve",
    "academic achievement", "educational attainment", "study skill",
    "knowledge economy", "educational policy", "teacher training", "school curriculum",
    "learning outcome", "academic rigour", "student welfare", "tuition fee",
    "educational opportunity", "skills gap", "academic pressure",
)
STANDARD_VERBS = (
    "cultivate", "foster", "facilitate", "implement", "reinforce", "prioritise",
    "undermine", "hinder", "allocate", "broaden", "instil", "nurture",
    "stimulate", "enhance", "streamline", "assess", "evaluate", "integrate",
    "equip", "empower", "mentor",
)
STANDARD_ADJECTIVES = (
    "rigorous", "holistic", "prestigious", "selective", "comprehensive",
    "interactive", "student-centred", "meritocratic", "beneficial", "detrimental",
    "engaging", "demanding", "accessible", "well-rounded", "innovative",
    "collaborative", "flexible", "prevalent", "substantial", "outdated",
    "rote-based",
)
STANDARD_ADVERBS = (
    "consequently", "notably", "significantly", "considerably", "arguably",
    "whereas", "thereby", "subsequently", "predominantly",
)

ADVANCED_NOUNS = (
    "pedagogical approach", "cognitive load", "differentiated instruction",
    "educational disparity", "intellectual autonomy", "meta-cognition",
    "socioeconomic background", "academic discourse", "formative assessment",
    "summative assessment", "epistemology", "curriculum framework",
    "educational marginalisation", "scholastic achievement", "andragogy",
    "critical pedagogy", "knowledge acquisition", "intellectual curiosity",
    "educational infrastructure", "credential inflation", "learning analytics",
    "academic autonomy", "pedagogical innovation", "cognitive scaffolding",
    "educational stratification",
)
ADVANCED_VERBS = (
    "engender", "underpin", "consolidate", "augment", "disseminate", "inculcate",
    "galvanise", "exacerbate", "mitigate", "perpetuate", "curtail", "bolster",
    "impede", "spearhead", "reconcile", "synthesise", "internalise",
    "counteract", "expedite", "reinforce", "diversify",
)
ADVANCED_ADJECTIVES = (
    "meritocratic", "autonomous", "scholarly", "multifaceted",
    "profound", "systemic", "inclusive", "elitist", "prohibitive", "nuanced",
    "far-reaching", "indispensable", "cumulative", "disproportionate", "salient",
    "pervasive", "unprecedented", "inextricable", "formative", "transformative",
    "negligible",
)
ADVANCED_ADVERBS = (
    "ostensibly", "invariably", "markedly", "conversely", "nonetheless",
    "disproportionately", "fundamentally", "substantially", "inherently",
)

BEGINNER = BEGINNER_NOUNS + BEGINNER_VERBS + BEGINNER_ADJECTIVES + BEGINNER_ADVERBS
STANDARD = STANDARD_NOUNS + STANDARD_VERBS + STANDARD_ADJECTIVES + STANDARD_ADVERBS
ADVANCED = ADVANCED_NOUNS + ADVANCED_VERBS + ADVANCED_ADJECTIVES + ADVANCED_ADVERBS

NOUNS = BEGINNER_NOUNS + STANDARD_NOUNS + ADVANCED_NOUNS
VERBS = BEGINNER_VERBS + STANDARD_VERBS + ADVANCED_VERBS
ADJECTIVES = BEGINNER_ADJECTIVES + STANDARD_ADJECTIVES + ADVANCED_ADJECTIVES
ADVERBS = BEGINNER_ADVERBS + STANDARD_ADVERBS + ADVANCED_ADVERBS
