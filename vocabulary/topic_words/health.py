"""Health topic word bank, balanced by part of speech."""

BEGINNER_NOUNS = (
    "disease", "illness", "diet", "nutrition", "obesity", "symptom", "treatment",
    "vaccine", "immunity", "hygiene", "wellbeing", "lifestyle", "fitness", "calorie",
    "disorder", "infection", "therapy", "remedy", "diagnosis", "prevention",
    "healthcare", "addiction", "fatigue", "allergy", "deficiency", "epidemic",
    "mental health", "blood pressure", "immune system", "life expectancy",
    "public health", "balanced diet", "physical activity", "medical care",
    "health service", "chronic illness", "side effect", "eating habit",
    "stress level", "sleep pattern",
)
BEGINNER_VERBS = (
    "cure", "heal", "prevent", "treat", "recover", "diagnose", "strengthen",
    "boost", "suffer", "infect", "vaccinate", "prescribe", "maintain", "consume",
    "avoid", "relieve", "nourish", "exhaust", "worsen", "recuperate",
)
BEGINNER_ADJECTIVES = (
    "healthy", "unhealthy", "chronic", "infectious", "contagious", "nutritious",
    "obese", "sedentary", "physical", "mental", "medical", "fatal", "harmful",
    "addictive", "immune", "balanced", "hygienic", "overweight", "preventable",
    "fit",
)
BEGINNER_ADVERBS = (
    "regularly", "physically", "mentally", "medically", "increasingly", "adversely",
)

STANDARD_NOUNS = (
    "vaccination", "malnutrition", "dehydration", "immunisation", "rehabilitation",
    "health policy", "sedentary lifestyle", "chronic disease", "mental illness",
    "health awareness", "preventive medicine", "primary care", "obesity epidemic",
    "health outcome", "risk factor", "dietary supplement", "health screening",
    "medical intervention", "healthcare system", "health inequality",
    "ageing population", "communicable disease", "mental wellbeing",
    "health promotion", "self-medication", "drug abuse", "substance abuse",
    "health infrastructure", "patient care", "clinical trial", "nutritional value",
    "wellbeing programme", "health expenditure", "care provision", "life quality",
)
STANDARD_VERBS = (
    "mitigate", "alleviate", "exacerbate", "rehabilitate", "immunise",
    "hospitalise", "screen", "implement", "promote", "undermine", "foster",
    "curb", "deteriorate", "transmit", "contract", "combat", "regulate",
    "allocate", "prioritise", "administer", "monitor",
)
STANDARD_ADJECTIVES = (
    "detrimental", "beneficial", "adverse", "prevalent", "acute", "nutritional",
    "terminal", "debilitating", "hereditary", "communicable", "therapeutic",
    "holistic", "malnourished", "sanitary", "susceptible", "widespread",
    "life-threatening", "curable", "incurable", "reversible", "psychological",
)
STANDARD_ADVERBS = (
    "consequently", "considerably", "notably", "subsequently", "significantly",
    "whereas", "thereby", "drastically", "chronically",
)

ADVANCED_NOUNS = (
    "comorbidity", "pathogen", "epidemiology", "morbidity", "mortality rate",
    "antibiotic resistance", "health disparity", "immunisation programme",
    "therapeutic intervention", "palliative care", "cognitive decline",
    "metabolic disorder", "cardiovascular disease", "psychological resilience",
    "preventive healthcare", "socioeconomic determinant", "health literacy",
    "sanitation infrastructure", "disease surveillance", "nutritional deficiency",
    "mental health crisis", "healthcare expenditure", "longevity",
    "public health intervention", "chronic condition",
)
ADVANCED_VERBS = (
    "ameliorate", "eradicate", "precipitate", "predispose", "incur", "jeopardise",
    "engender", "succumb", "aggravate", "avert", "forestall", "bolster", "impede",
    "undergo", "exert", "curtail", "offset", "reinforce", "spearhead",
    "counteract", "detect",
)
ADVANCED_ADJECTIVES = (
    "negligible", "profound", "insidious", "endemic", "latent", "asymptomatic",
    "degenerative", "systemic", "cumulative", "deleterious", "disproportionate",
    "palliative", "immunocompromised", "multifaceted", "inextricable", "salient",
    "marginal", "ubiquitous", "precarious", "far-reaching", "indispensable",
)
ADVANCED_ADVERBS = (
    "arguably", "ostensibly", "invariably", "predominantly", "markedly",
    "conversely", "nonetheless", "disproportionately", "substantially",
)

BEGINNER = BEGINNER_NOUNS + BEGINNER_VERBS + BEGINNER_ADJECTIVES + BEGINNER_ADVERBS
STANDARD = STANDARD_NOUNS + STANDARD_VERBS + STANDARD_ADJECTIVES + STANDARD_ADVERBS
ADVANCED = ADVANCED_NOUNS + ADVANCED_VERBS + ADVANCED_ADJECTIVES + ADVANCED_ADVERBS

NOUNS = BEGINNER_NOUNS + STANDARD_NOUNS + ADVANCED_NOUNS
VERBS = BEGINNER_VERBS + STANDARD_VERBS + ADVANCED_VERBS
ADJECTIVES = BEGINNER_ADJECTIVES + STANDARD_ADJECTIVES + ADVANCED_ADJECTIVES
ADVERBS = BEGINNER_ADVERBS + STANDARD_ADVERBS + ADVANCED_ADVERBS
