"""Society topic word bank (crime, media, culture, family, government, globalisation)."""

BEGINNER_NOUNS = (
    "crime", "poverty", "inequality", "community", "tradition", "custom", "culture",
    "society", "citizen", "government", "law", "media", "generation", "diversity",
    "immigration", "population", "welfare", "charity", "religion", "identity",
    "social media", "human rights", "gender equality", "public opinion",
    "social class", "crime rate", "cultural heritage", "family structure",
    "social norm", "peer pressure", "mass media", "news outlet", "urban area",
    "rural area", "civil society", "social change", "cost of living",
    "standard of living", "public service", "voluntary work",
)
BEGINNER_VERBS = (
    "commit", "punish", "protest", "integrate", "discriminate", "influence",
    "support", "volunteer", "migrate", "reform", "obey", "enforce", "unite",
    "divide", "isolate", "adapt", "belong", "contribute", "respect", "tolerate",
)
BEGINNER_ADJECTIVES = (
    "social", "cultural", "traditional", "modern", "diverse", "multicultural",
    "wealthy", "impoverished", "unequal", "civil", "criminal", "ethical",
    "religious", "influential", "prejudiced", "tolerant", "urban", "rural",
    "collective", "widespread",
)
BEGINNER_ADVERBS = (
    "socially", "culturally", "increasingly", "traditionally", "widely", "equally",
)

STANDARD_NOUNS = (
    "globalisation", "urbanisation", "discrimination", "assimilation",
    "social cohesion", "civil liberty", "cultural identity", "social mobility",
    "juvenile delinquency", "law enforcement", "rehabilitation", "censorship",
    "propaganda", "surveillance", "misinformation", "social inequality",
    "wealth gap", "gender gap", "public policy", "welfare state", "social justice",
    "cultural diversity", "ethnic minority", "gender role", "family values",
    "moral standard", "crime prevention", "social integration",
    "generational divide", "media bias", "freedom of speech", "civic engagement",
    "social stigma", "collective identity", "cultural assimilation",
)
STANDARD_VERBS = (
    "marginalise", "assimilate", "integrate", "alienate", "perpetuate",
    "undermine", "reinforce", "prohibit", "regulate", "prosecute", "deter",
    "advocate", "empower", "segregate", "stigmatise", "mobilise", "foster",
    "implement", "curb", "polarise", "erode",
)
STANDARD_ADJECTIVES = (
    "prevalent", "marginalised", "affluent", "underprivileged", "cohesive",
    "discriminatory", "authoritarian", "democratic", "controversial",
    "conservative", "progressive", "detrimental", "systemic", "widespread",
    "divisive", "inclusive", "patriarchal", "secular", "hierarchical", "punitive",
    "substantial",
)
STANDARD_ADVERBS = (
    "consequently", "notably", "significantly", "arguably", "considerably",
    "whereas", "thereby", "subsequently", "predominantly",
)

ADVANCED_NOUNS = (
    "social stratification", "cultural homogenisation", "socioeconomic disparity",
    "civic participation", "moral relativism", "collective consciousness",
    "social fragmentation", "institutional discrimination", "cultural imperialism",
    "demographic shift", "recidivism", "penal system", "media manipulation",
    "echo chamber", "identity politics", "social capital", "welfare dependency",
    "meritocracy", "intergenerational mobility", "cultural assimilationism",
    "structural inequality", "social alienation", "moral panic",
    "civil disobedience", "social solidarity",
)
ADVANCED_VERBS = (
    "exacerbate", "engender", "homogenise", "disenfranchise", "galvanise",
    "entrench", "subvert", "ostracise", "perpetuate", "mitigate", "reconcile",
    "polarise", "assimilate", "vilify", "marginalise", "consolidate",
    "destabilise", "counteract", "spearhead", "underpin", "curtail",
)
ADVANCED_ADJECTIVES = (
    "systemic", "entrenched", "pervasive", "insidious", "disenfranchised",
    "cosmopolitan", "xenophobic", "egalitarian", "meritocratic", "profound",
    "far-reaching", "disproportionate", "inextricable", "multifaceted",
    "unprecedented", "polarising", "marginal", "salient", "endemic",
    "indispensable", "nuanced",
)
ADVANCED_ADVERBS = (
    "ostensibly", "invariably", "markedly", "conversely", "nonetheless",
    "disproportionately", "fundamentally", "inherently", "arguably",
)

BEGINNER = BEGINNER_NOUNS + BEGINNER_VERBS + BEGINNER_ADJECTIVES + BEGINNER_ADVERBS
STANDARD = STANDARD_NOUNS + STANDARD_VERBS + STANDARD_ADJECTIVES + STANDARD_ADVERBS
ADVANCED = ADVANCED_NOUNS + ADVANCED_VERBS + ADVANCED_ADJECTIVES + ADVANCED_ADVERBS

NOUNS = BEGINNER_NOUNS + STANDARD_NOUNS + ADVANCED_NOUNS
VERBS = BEGINNER_VERBS + STANDARD_VERBS + ADVANCED_VERBS
ADJECTIVES = BEGINNER_ADJECTIVES + STANDARD_ADJECTIVES + ADVANCED_ADJECTIVES
ADVERBS = BEGINNER_ADVERBS + STANDARD_ADVERBS + ADVANCED_ADVERBS
