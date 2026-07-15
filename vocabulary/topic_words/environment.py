"""Environment topic word bank, balanced by part of speech.

Each tier mixes nouns / verbs / adjectives / adverbs so every level has a spread.
NOUNS/VERBS/ADJECTIVES/ADVERBS aggregates drive deterministic part-of-speech
tagging (see vocabulary/pos_overrides.py). BEGINNER/STANDARD/ADVANCED are the
lemma lists consumed by the sync pipeline.
"""

BEGINNER_NOUNS = (
    "climate", "pollution", "habitat", "drought", "fossil fuel", "deforestation",
    "wildlife", "conservation", "flood", "glacier", "atmosphere", "species",
    "natural disaster", "ecosystem", "landfill", "erosion", "acid rain", "ozone layer",
    "smog", "pesticide", "fertiliser", "sewage", "emissions", "biodiversity",
    "renewable energy", "carbon footprint", "greenhouse gas", "waste management",
    "air quality", "wetland", "food chain", "rainforest", "coral reef", "solar power",
    "wind farm", "natural resource", "carbon dioxide", "sea level", "drinking water",
    "environmental protection",
)
BEGINNER_VERBS = (
    "pollute", "recycle", "conserve", "preserve", "reduce", "reuse", "emit",
    "consume", "restore", "dispose", "threaten", "contaminate", "damage",
    "protect", "dump", "replant", "purify", "harm", "overuse", "safeguard",
)
BEGINNER_ADJECTIVES = (
    "sustainable", "renewable", "toxic", "endangered", "extinct", "polluted",
    "harmful", "organic", "environmental", "ecological", "wasteful", "scarce",
    "abundant", "fragile", "fertile", "arid", "hazardous", "eco-friendly",
    "biodegradable", "clean",
)
BEGINNER_ADVERBS = (
    "environmentally", "globally", "naturally", "increasingly", "worldwide", "heavily",
)

STANDARD_NOUNS = (
    "depletion", "contamination", "reforestation", "habitat loss", "global warming",
    "water scarcity", "solar panel", "wind turbine", "overpopulation",
    "industrialisation", "carbon offset", "urban sprawl", "soil degradation",
    "ocean acidification", "coral bleaching", "wildfire", "carbon cycle",
    "food security", "plastic waste", "e-waste", "conservation area",
    "invasive species", "mitigation strategy", "green infrastructure",
    "circular economy", "sustainable development", "carbon tax", "waste disposal",
    "land use", "environmental impact", "energy efficiency", "climate change",
    "net zero", "greenhouse effect", "fossil fuel dependency",
)
STANDARD_VERBS = (
    "mitigate", "deplete", "offset", "curb", "alleviate", "degrade", "exploit",
    "replenish", "regulate", "monitor", "discharge", "foster", "hinder",
    "implement", "allocate", "undermine", "generate", "phase out", "conserve",
    "harness", "reinforce",
)
STANDARD_ADJECTIVES = (
    "detrimental", "adverse", "prevalent", "viable", "substantial", "considerable",
    "non-renewable", "finite", "widespread", "irreversible", "alarming", "drastic",
    "unprecedented", "significant", "beneficial", "feasible", "extensive",
    "pervasive", "degradable", "unsustainable", "man-made",
)
STANDARD_ADVERBS = (
    "consequently", "considerably", "subsequently", "notably", "drastically",
    "adversely", "whereas", "thereby", "significantly",
)

ADVANCED_NOUNS = (
    "sequestration", "desertification", "eutrophication", "microplastics",
    "particulate matter", "permafrost", "carbon sink", "tipping point", "biomass",
    "aquifer", "bioaccumulation", "ecological footprint", "hydrological cycle",
    "biosphere", "trophic level", "carrying capacity", "afforestation", "rewilding",
    "precautionary principle", "intergenerational equity",
    "environmental externalities", "remediation", "anthropogenic emissions",
    "planetary boundary", "ecological resilience",
)
ADVANCED_VERBS = (
    "sequester", "ameliorate", "remediate", "jeopardise", "precipitate", "aggravate",
    "decarbonise", "acidify", "destabilise", "engender", "exert", "incur", "impede",
    "bolster", "diminish", "perpetuate", "counteract", "forestall", "attenuate",
    "exacerbate", "spearhead",
)
ADVANCED_ADJECTIVES = (
    "anthropogenic", "negligible", "profound", "inexorable", "deleterious",
    "catastrophic", "cumulative", "systemic", "resilient", "ubiquitous",
    "precarious", "insidious", "endemic", "latent", "acute", "disproportionate",
    "marginal", "tenuous", "salient", "far-reaching", "indispensable",
)
ADVANCED_ADVERBS = (
    "arguably", "ostensibly", "invariably", "predominantly", "markedly",
    "conversely", "nonetheless", "disproportionately", "inexorably",
)

BEGINNER = BEGINNER_NOUNS + BEGINNER_VERBS + BEGINNER_ADJECTIVES + BEGINNER_ADVERBS
STANDARD = STANDARD_NOUNS + STANDARD_VERBS + STANDARD_ADJECTIVES + STANDARD_ADVERBS
ADVANCED = ADVANCED_NOUNS + ADVANCED_VERBS + ADVANCED_ADJECTIVES + ADVANCED_ADVERBS

NOUNS = BEGINNER_NOUNS + STANDARD_NOUNS + ADVANCED_NOUNS
VERBS = BEGINNER_VERBS + STANDARD_VERBS + ADVANCED_VERBS
ADJECTIVES = BEGINNER_ADJECTIVES + STANDARD_ADJECTIVES + ADVANCED_ADJECTIVES
ADVERBS = BEGINNER_ADVERBS + STANDARD_ADVERBS + ADVANCED_ADVERBS
