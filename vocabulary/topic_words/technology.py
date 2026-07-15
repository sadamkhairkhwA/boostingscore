"""Technology topic word bank, balanced by part of speech."""

BEGINNER_NOUNS = (
    "internet", "software", "device", "application", "network", "data", "user",
    "website", "gadget", "innovation", "automation", "database", "hardware",
    "connectivity", "platform", "interface", "algorithm", "password", "browser",
    "server", "smartphone", "search engine", "social media", "digital device",
    "online platform", "data storage", "screen time", "tech industry",
    "digital skill", "video call", "cloud storage", "mobile app", "operating system",
    "digital tool", "information technology", "user experience", "digital content",
    "wireless network", "digital divide", "tech company",
)
BEGINNER_VERBS = (
    "connect", "download", "upload", "install", "update", "browse", "automate",
    "program", "access", "store", "share", "stream", "innovate", "operate",
    "process", "monitor", "enhance", "replace", "simplify", "transmit",
)
BEGINNER_ADJECTIVES = (
    "digital", "online", "automated", "virtual", "wireless", "electronic",
    "innovative", "efficient", "interactive", "portable", "advanced",
    "user-friendly", "outdated", "reliable", "accessible", "technical",
    "high-tech", "compatible", "remote", "smart",
)
BEGINNER_ADVERBS = (
    "digitally", "instantly", "remotely", "increasingly", "automatically", "widely",
)

STANDARD_NOUNS = (
    "cybersecurity", "artificial intelligence", "encryption", "bandwidth",
    "innovation hub", "digital literacy", "data breach", "machine learning",
    "cloud computing", "digital transformation", "automation technology",
    "virtual reality", "augmented reality", "biometrics", "data privacy",
    "surveillance", "e-commerce", "digital economy", "screen addiction",
    "tech dependency", "information overload", "data analytics", "user interface",
    "software update", "technological advancement", "digital footprint",
    "online security", "smart device", "remote working", "digital citizenship",
    "technological progress", "computing power", "network infrastructure",
    "data protection", "digital platform",
)
STANDARD_VERBS = (
    "implement", "integrate", "optimise", "automate", "encrypt", "innovate",
    "streamline", "facilitate", "enhance", "revolutionise", "digitise",
    "safeguard", "undermine", "disrupt", "harness", "deploy", "regulate",
    "outsource", "customise", "accelerate", "monitor",
)
STANDARD_ADJECTIVES = (
    "innovative", "disruptive", "sophisticated", "cutting-edge", "scalable",
    "obsolete", "vulnerable", "seamless", "pervasive", "revolutionary",
    "cost-effective", "intuitive", "autonomous", "encrypted", "interconnected",
    "data-driven", "adaptive", "widespread", "prevalent", "detrimental",
    "beneficial",
)
STANDARD_ADVERBS = (
    "consequently", "increasingly", "significantly", "notably", "seamlessly",
    "whereas", "thereby", "subsequently", "considerably",
)

ADVANCED_NOUNS = (
    "cryptography", "blockchain", "quantum computing", "neural network",
    "digital surveillance", "technological singularity", "data sovereignty",
    "algorithmic bias", "digital ecosystem", "computational power",
    "interoperability", "obsolescence", "technological disruption",
    "artificial general intelligence", "predictive analytics",
    "digital infrastructure", "cyber warfare", "automation displacement",
    "technological determinism", "digital exclusion", "information asymmetry",
    "technological convergence", "data commodification", "surveillance capitalism",
    "innovation ecosystem",
)
ADVANCED_VERBS = (
    "revolutionise", "augment", "circumvent", "proliferate", "supersede",
    "underpin", "exacerbate", "mitigate", "engender", "expedite", "commodify",
    "decentralise", "exploit", "leverage", "curtail", "reinforce", "displace",
    "spearhead", "counteract", "perpetuate", "amplify",
)
ADVANCED_ADJECTIVES = (
    "ubiquitous", "unprecedented", "autonomous", "algorithmic", "decentralised",
    "exponential", "invasive", "transformative", "insidious", "negligible",
    "systemic", "far-reaching", "indispensable", "networked", "immersive",
    "disproportionate", "profound", "nascent", "cumulative", "salient",
    "inextricable",
)
ADVANCED_ADVERBS = (
    "arguably", "exponentially", "predominantly", "invariably", "ostensibly",
    "markedly", "conversely", "nonetheless", "fundamentally",
)

BEGINNER = BEGINNER_NOUNS + BEGINNER_VERBS + BEGINNER_ADJECTIVES + BEGINNER_ADVERBS
STANDARD = STANDARD_NOUNS + STANDARD_VERBS + STANDARD_ADJECTIVES + STANDARD_ADVERBS
ADVANCED = ADVANCED_NOUNS + ADVANCED_VERBS + ADVANCED_ADJECTIVES + ADVANCED_ADVERBS

NOUNS = BEGINNER_NOUNS + STANDARD_NOUNS + ADVANCED_NOUNS
VERBS = BEGINNER_VERBS + STANDARD_VERBS + ADVANCED_VERBS
ADJECTIVES = BEGINNER_ADJECTIVES + STANDARD_ADJECTIVES + ADVANCED_ADJECTIVES
ADVERBS = BEGINNER_ADVERBS + STANDARD_ADVERBS + ADVANCED_ADVERBS
