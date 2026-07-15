"""Business and work topic word bank, balanced by part of speech."""

BEGINNER_NOUNS = (
    "profit", "revenue", "employee", "employer", "salary", "wage", "investment",
    "customer", "product", "service", "industry", "market", "economy", "budget",
    "management", "workforce", "productivity", "competition", "entrepreneur",
    "corporation", "job satisfaction", "working hours", "career path",
    "small business", "job market", "work-life balance", "remote work",
    "customer service", "supply and demand", "business owner", "company profit",
    "economic growth", "employment rate", "trade agreement", "consumer demand",
    "job security", "labour market", "business strategy", "market share",
    "financial loss",
)
BEGINNER_VERBS = (
    "invest", "manage", "employ", "recruit", "produce", "sell", "purchase",
    "compete", "negotiate", "earn", "expand", "advertise", "budget", "outsource",
    "supervise", "collaborate", "profit", "market", "trade", "deliver",
)
BEGINNER_ADJECTIVES = (
    "commercial", "financial", "economic", "profitable", "competitive",
    "corporate", "professional", "productive", "efficient", "lucrative",
    "affordable", "innovative", "entrepreneurial", "flexible", "reliable",
    "skilled", "unemployed", "self-employed", "prosperous", "marketable",
)
BEGINNER_ADVERBS = (
    "financially", "commercially", "increasingly", "professionally", "efficiently",
    "globally",
)

STANDARD_NOUNS = (
    "entrepreneurship", "globalisation", "outsourcing", "monopoly",
    "market share", "profit margin", "corporate culture", "job automation",
    "economic downturn", "consumer behaviour", "brand loyalty", "start-up",
    "stock market", "supply chain", "business model", "cash flow",
    "return on investment", "market demand", "labour force", "trade deficit",
    "economic recession", "gig economy", "workplace diversity", "career progression",
    "corporate responsibility", "market fluctuation", "employee retention",
    "financial incentive", "business venture", "economic policy",
    "workforce productivity", "consumer confidence", "competitive advantage",
    "occupational stress", "income inequality",
)
STANDARD_VERBS = (
    "allocate", "generate", "diversify", "streamline", "implement", "maximise",
    "minimise", "outsource", "restructure", "undermine", "capitalise",
    "incentivise", "monopolise", "forecast", "downsize", "innovate", "expand",
    "prioritise", "subsidise", "leverage", "sustain", "commercialise",
    "privatise", "nationalise", "franchise",
)
STANDARD_ADJECTIVES = (
    "lucrative", "profitable", "competitive", "sustainable", "cost-effective",
    "viable", "prevalent", "beneficial", "detrimental", "substantial",
    "flourishing", "stagnant", "volatile", "monopolistic", "strategic",
    "prosperous", "recessionary", "scalable", "innovative", "widespread",
    "prohibitive", "market-driven", "profit-oriented",
)
STANDARD_ADVERBS = (
    "consequently", "notably", "significantly", "considerably", "arguably",
    "whereas", "thereby", "subsequently", "predominantly",
)

ADVANCED_NOUNS = (
    "market saturation", "economic stagnation", "fiscal policy", "monetary policy",
    "corporate governance", "vertical integration", "economies of scale",
    "market volatility", "capital investment", "productivity growth",
    "labour exploitation", "wealth distribution", "economic disparity",
    "market equilibrium", "disruptive innovation", "corporate accountability",
    "occupational mobility", "financial sustainability", "trade liberalisation",
    "workforce automation", "profit maximisation", "economic resilience",
    "consumerism", "entrepreneurial ecosystem", "structural unemployment",
)
ADVANCED_VERBS = (
    "capitalise", "consolidate", "monopolise", "underpin", "exacerbate",
    "mitigate", "spearhead", "revolutionise", "destabilise", "circumvent",
    "engender", "curtail", "bolster", "perpetuate", "counteract", "expedite",
    "reinvest", "liquidate", "amortise", "reinforce", "diversify",
)
ADVANCED_ADJECTIVES = (
    "lucrative", "unprecedented", "volatile", "systemic", "far-reaching",
    "monopolistic", "recessionary", "profound", "disproportionate", "negligible",
    "cumulative", "indispensable", "salient", "multifaceted", "inextricable",
    "burgeoning", "exploitative", "resilient", "entrenched", "prohibitive",
    "nascent",
)
ADVANCED_ADVERBS = (
    "arguably", "ostensibly", "invariably", "markedly", "conversely",
    "nonetheless", "disproportionately", "substantially", "fundamentally",
)

BEGINNER = BEGINNER_NOUNS + BEGINNER_VERBS + BEGINNER_ADJECTIVES + BEGINNER_ADVERBS
STANDARD = STANDARD_NOUNS + STANDARD_VERBS + STANDARD_ADJECTIVES + STANDARD_ADVERBS
ADVANCED = ADVANCED_NOUNS + ADVANCED_VERBS + ADVANCED_ADJECTIVES + ADVANCED_ADVERBS

NOUNS = BEGINNER_NOUNS + STANDARD_NOUNS + ADVANCED_NOUNS
VERBS = BEGINNER_VERBS + STANDARD_VERBS + ADVANCED_VERBS
ADJECTIVES = BEGINNER_ADJECTIVES + STANDARD_ADJECTIVES + ADVANCED_ADJECTIVES
ADVERBS = BEGINNER_ADVERBS + STANDARD_ADVERBS + ADVANCED_ADVERBS
