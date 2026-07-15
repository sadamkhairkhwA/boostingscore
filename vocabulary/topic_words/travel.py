"""Travel and transport topic word bank, balanced by part of speech."""

BEGINNER_NOUNS = (
    "tourism", "destination", "transport", "journey", "accommodation", "itinerary",
    "passenger", "commute", "traffic", "congestion", "airport", "railway",
    "highway", "vehicle", "fare", "sightseeing", "landmark", "excursion",
    "expedition", "voyage", "public transport", "tourist attraction",
    "travel agency", "traffic jam", "rush hour", "cultural exchange",
    "package holiday", "budget airline", "road network", "peak season",
    "local cuisine", "travel insurance", "border control", "carbon emission",
    "fuel consumption", "means of transport", "tourist destination",
    "transport system", "urban transport", "scenic route",
)
BEGINNER_VERBS = (
    "travel", "commute", "explore", "navigate", "depart", "arrive", "board",
    "relocate", "wander", "venture", "transport", "reserve", "cancel", "delay",
    "roam", "embark", "traverse", "discover", "accommodate", "sightsee",
)
BEGINNER_ADJECTIVES = (
    "scenic", "cultural", "adventurous", "affordable", "convenient", "crowded",
    "remote", "exotic", "picturesque", "congested", "accessible", "seasonal",
    "domestic", "international", "eco-friendly", "efficient", "reliable",
    "sustainable", "leisurely", "punctual",
)
BEGINNER_ADVERBS = (
    "abroad", "conveniently", "increasingly", "remotely", "widely", "efficiently",
)

STANDARD_NOUNS = (
    "infrastructure", "urbanisation", "connectivity", "sustainability",
    "mass tourism", "eco-tourism", "carbon footprint", "travel restriction",
    "cultural immersion", "tourist industry", "transport network",
    "traffic congestion", "public transportation", "air travel", "high-speed rail",
    "travel documentation", "seasonal tourism", "over-tourism", "local economy",
    "transport hub", "commuter belt", "fuel efficiency", "travel expenditure",
    "tourism revenue", "cultural heritage", "environmental impact",
    "transport policy", "urban mobility", "road safety", "congestion charge",
    "tourism sector", "travel demand", "transit system", "carbon offset",
    "visitor economy", "airfare", "layover", "transit hub", "visa policy",
    "flight connection", "tourist visa", "road congestion", "flight delay",
)
STANDARD_VERBS = (
    "alleviate", "accommodate", "facilitate", "implement", "regulate", "commute",
    "integrate", "diversify", "boost", "undermine", "streamline", "subsidise",
    "prioritise", "curb", "expand", "invest", "promote", "modernise",
    "decongest", "reroute", "foster", "ferry", "shuttle", "electrify",
    "pedestrianise", "tour", "backpack",
)
STANDARD_ADJECTIVES = (
    "sustainable", "congested", "cost-effective", "environmentally friendly",
    "efficient", "overcrowded", "prevalent", "beneficial", "detrimental",
    "seasonal", "extensive", "integrated", "affordable", "widespread",
    "unspoilt", "accessible", "reliable", "substantial", "lucrative", "far-flung",
    "off-peak", "well-connected", "car-dependent", "pedestrian-friendly",
    "long-haul", "short-haul", "budget-friendly",
)
STANDARD_ADVERBS = (
    "consequently", "notably", "significantly", "increasingly", "considerably",
    "whereas", "thereby", "subsequently", "predominantly",
)

ADVANCED_NOUNS = (
    "sustainable tourism", "carbon-neutral transport", "transport decarbonisation",
    "tourism saturation", "cultural commodification", "seasonal fluctuation",
    "environmental degradation", "mobility infrastructure", "aviation industry",
    "transport emissions", "tourist footprint", "modal shift",
    "congestion pricing", "urban sprawl", "tourism dependency",
    "intermodal transport", "travel deterrent", "destination management",
    "carrying capacity", "ecological impact", "transport equity",
    "commuter density", "tourism externalities", "connectivity deficit",
    "infrastructure investment", "gridlock", "park-and-ride", "slow travel",
    "transport poverty", "aviation emissions", "flight shaming",
)
ADVANCED_VERBS = (
    "exacerbate", "mitigate", "decongest", "revitalise", "underpin", "incentivise",
    "deter", "spearhead", "curtail", "reinvigorate", "engender", "offset",
    "counteract", "bolster", "impede", "reconfigure", "diversify", "expedite",
    "perpetuate", "reinforce", "consolidate",
)
ADVANCED_ADJECTIVES = (
    "unprecedented", "pervasive", "detrimental", "sustainable", "cosmopolitan",
    "profound", "far-reaching", "disproportionate", "unspoiled", "saturated",
    "prohibitive", "negligible", "systemic", "salient", "indispensable",
    "multifaceted", "inextricable", "burgeoning", "lucrative", "ubiquitous",
    "transient",
)
ADVANCED_ADVERBS = (
    "arguably", "ostensibly", "invariably", "markedly", "conversely",
    "nonetheless", "disproportionately", "predominantly", "substantially",
)

BEGINNER = BEGINNER_NOUNS + BEGINNER_VERBS + BEGINNER_ADJECTIVES + BEGINNER_ADVERBS
STANDARD = STANDARD_NOUNS + STANDARD_VERBS + STANDARD_ADJECTIVES + STANDARD_ADVERBS
ADVANCED = ADVANCED_NOUNS + ADVANCED_VERBS + ADVANCED_ADJECTIVES + ADVANCED_ADVERBS

NOUNS = BEGINNER_NOUNS + STANDARD_NOUNS + ADVANCED_NOUNS
VERBS = BEGINNER_VERBS + STANDARD_VERBS + ADVANCED_VERBS
ADJECTIVES = BEGINNER_ADJECTIVES + STANDARD_ADJECTIVES + ADVANCED_ADJECTIVES
ADVERBS = BEGINNER_ADVERBS + STANDARD_ADVERBS + ADVANCED_ADVERBS
