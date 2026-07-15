"""Science topic word bank, balanced by part of speech."""

BEGINNER_NOUNS = (
    "experiment", "research", "theory", "hypothesis", "evidence", "discovery",
    "laboratory", "data", "analysis", "observation", "method", "result",
    "scientist", "measurement", "variable", "sample", "reaction", "element",
    "compound", "organism", "genetics", "biology", "chemistry", "physics",
    "scientific method", "clinical trial", "peer review", "research paper",
    "data collection", "control group", "natural science", "space exploration",
    "medical research", "scientific breakthrough", "cause and effect",
    "renewable resource", "human genome", "scientific evidence", "research funding",
    "laboratory equipment",
)
BEGINNER_VERBS = (
    "observe", "measure", "analyse", "experiment", "discover", "investigate",
    "test", "prove", "examine", "record", "predict", "conclude", "verify",
    "calculate", "classify", "detect", "demonstrate", "replicate", "hypothesise",
    "quantify",
)
BEGINNER_ADJECTIVES = (
    "scientific", "experimental", "empirical", "theoretical", "chemical",
    "biological", "physical", "accurate", "reliable", "measurable", "systematic",
    "quantitative", "qualitative", "objective", "innovative", "significant",
    "controlled", "observable", "precise", "valid",
)
BEGINNER_ADVERBS = (
    "scientifically", "empirically", "accurately", "systematically", "precisely",
    "objectively",
)

STANDARD_NOUNS = (
    "innovation", "methodology", "correlation", "causation", "phenomenon",
    "breakthrough", "genetic engineering", "clinical study", "data analysis",
    "scientific consensus", "research methodology", "control variable",
    "empirical evidence", "statistical significance", "scientific inquiry",
    "biotechnology", "nanotechnology", "vaccine development", "gene therapy",
    "research ethics", "scientific literacy", "theoretical framework",
    "experimental design", "sample size", "margin of error", "peer-reviewed study",
    "research grant", "scientific advancement", "laboratory analysis",
    "quantitative data", "qualitative data", "scientific rigour",
    "reproducibility", "research outcome", "hypothesis testing",
)
STANDARD_VERBS = (
    "hypothesise", "substantiate", "corroborate", "extrapolate", "synthesise",
    "validate", "refute", "replicate", "quantify", "formulate", "isolate",
    "manipulate", "correlate", "innovate", "undermine", "establish", "derive",
    "assess", "simulate", "postulate", "infer", "calibrate", "theorise", "model",
)
STANDARD_ADJECTIVES = (
    "empirical", "rigorous", "conclusive", "inconclusive", "reproducible",
    "statistical", "methodological", "verifiable", "quantifiable", "robust",
    "credible", "substantial", "prevalent", "innovative", "hypothetical",
    "analytical", "systematic", "unbiased", "peer-reviewed", "cutting-edge",
    "significant",
)
STANDARD_ADVERBS = (
    "consequently", "notably", "significantly", "empirically", "considerably",
    "whereas", "thereby", "subsequently", "statistically",
)

ADVANCED_NOUNS = (
    "epistemology", "paradigm shift", "scientific paradigm", "causal mechanism",
    "meta-analysis", "confounding variable", "statistical inference",
    "genome sequencing", "quantum mechanics", "molecular biology",
    "biochemical pathway", "research reproducibility", "scientific determinism",
    "empirical validation", "theoretical model", "systematic review",
    "experimental replication", "scientific objectivity", "data integrity",
    "interdisciplinary research", "computational modelling", "peer scrutiny",
    "evidentiary basis", "scientific validation", "research integrity",
)
ADVANCED_VERBS = (
    "corroborate", "extrapolate", "elucidate", "delineate", "substantiate",
    "underpin", "invalidate", "reconcile", "synthesise", "postulate",
    "operationalise", "disprove", "converge", "diverge", "attenuate",
    "counteract", "consolidate", "expedite", "engender", "reinforce", "discern",
)
ADVANCED_ADJECTIVES = (
    "axiomatic", "reproducible", "seminal", "rigorous", "definitive",
    "provisional", "counterintuitive", "systemic", "profound", "far-reaching",
    "negligible", "cumulative", "nuanced", "indispensable", "salient",
    "unprecedented", "disproportionate", "multifaceted", "inextricable",
    "tentative", "robust",
)
ADVANCED_ADVERBS = (
    "arguably", "ostensibly", "invariably", "markedly", "conversely",
    "nonetheless", "fundamentally", "substantially", "inherently",
)

BEGINNER = BEGINNER_NOUNS + BEGINNER_VERBS + BEGINNER_ADJECTIVES + BEGINNER_ADVERBS
STANDARD = STANDARD_NOUNS + STANDARD_VERBS + STANDARD_ADJECTIVES + STANDARD_ADVERBS
ADVANCED = ADVANCED_NOUNS + ADVANCED_VERBS + ADVANCED_ADJECTIVES + ADVANCED_ADVERBS

NOUNS = BEGINNER_NOUNS + STANDARD_NOUNS + ADVANCED_NOUNS
VERBS = BEGINNER_VERBS + STANDARD_VERBS + ADVANCED_VERBS
ADJECTIVES = BEGINNER_ADJECTIVES + STANDARD_ADJECTIVES + ADVANCED_ADJECTIVES
ADVERBS = BEGINNER_ADVERBS + STANDARD_ADVERBS + ADVANCED_ADVERBS
