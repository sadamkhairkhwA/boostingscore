"""
Bundled IELTS-style vocabulary for Boosting Score (all topics × levels).
Loaded by data migration and by `manage.py seed_words`.
"""

# Each row: word, topic, level, definition, example_sentence, collocations, part_of_speech, phonetic

INITIAL_WORD_ROWS = [
    # --- environment ---
    ("pollution", "environment", 1, "harmful substances in air, water, or soil", "Air pollution affects urban residents.", ["reduce pollution", "water pollution"], "noun", "/pəˈluːʃn/"),
    ("recycle", "environment", 1, "to process used materials to make new products", "We should recycle plastic bottles.", ["recycle waste"], "verb", "/riːˈsaɪkl/"),
    ("climate", "environment", 1, "the general weather conditions in an area", "Climate change is a global issue.", ["climate crisis"], "noun", "/ˈklaɪmət/"),
    ("renewable", "environment", 1, "energy that can be replaced naturally", "Solar power is a renewable source.", ["renewable energy"], "adjective", "/rɪˈnjuːəbl/"),
    ("wildlife", "environment", 2, "wild animals and plants in natural habitats", "The road threatened local wildlife.", ["protect wildlife"], "noun", "/ˈwaɪldlaɪf/"),
    ("deforestation", "environment", 2, "the clearing of forests for other uses", "Deforestation raises carbon levels.", ["tackle deforestation"], "noun", "/diːˌfɒrɪˈsteɪʃn/"),
    ("carbon footprint", "environment", 2, "total greenhouse gases from an activity", "Flying increases your carbon footprint.", ["reduce carbon footprint"], "noun phrase", "/ˈkɑːbən ˈfʊtprɪnt/"),
    ("ecosystem", "environment", 3, "a community of living things and their environment", "Pollution disrupted the river ecosystem.", ["marine ecosystem"], "noun", "/ˈiːkəʊsɪstəm/"),
    ("mitigation", "environment", 3, "action to make something less harmful", "Mitigation measures were costly but necessary.", ["climate mitigation"], "noun", "/ˌmɪtɪˈɡeɪʃn/"),
    ("sustainability", "environment", 3, "using resources without depleting them", "The company published a sustainability report.", ["environmental sustainability"], "noun", "/səˌsteɪnəˈbɪləti/"),
    ("biodiversity", "environment", 3, "the variety of species in an area", "Farming threatened regional biodiversity.", ["loss of biodiversity"], "noun", "/ˌbaɪəʊdaɪˈvɜːsəti/"),
    ("emission", "environment", 3, "gas or radiation released into the air", "The factory cut emissions by 20%.", ["carbon emissions"], "noun", "/ɪˈmɪʃn/"),
    # --- health ---
    ("exercise", "health", 1, "physical activity to stay fit", "Regular exercise improves sleep.", ["do exercise"], "noun", "/ˈeksəsaɪz/"),
    ("diet", "health", 1, "the food someone eats", "A balanced diet reduces risk of illness.", ["healthy diet"], "noun", "/ˈdaɪət/"),
    ("stress", "health", 1, "mental or emotional pressure", "Work stress affected her health.", ["reduce stress"], "noun", "/stres/"),
    ("treatment", "health", 1, "medical care for an illness", "Early treatment saves lives.", ["receive treatment"], "noun", "/ˈtriːtmənt/"),
    ("obesity", "health", 2, "being very overweight in a harmful way", "Childhood obesity is rising.", ["tackle obesity"], "noun", "/əʊˈbiːsəti/"),
    ("epidemic", "health", 2, "a disease spreading quickly among many people", "The epidemic overwhelmed hospitals.", ["flu epidemic"], "noun", "/ˌepɪˈdemɪk/"),
    ("mental health", "health", 2, "psychological and emotional well-being", "Employers now address mental health.", ["mental health services"], "noun phrase", "/ˈmentl helθ/"),
    ("vaccination", "health", 2, "giving a vaccine to prevent disease", "Vaccination rates improved nationally.", ["child vaccination"], "noun", "/ˌvæksɪˈneɪʃn/"),
    ("chronic", "health", 3, "lasting a long time (illness)", "Chronic pain limits daily activity.", ["chronic disease"], "adjective", "/ˈkrɒnɪk/"),
    ("healthcare", "health", 3, "the organized provision of medical services", "Healthcare costs are debated worldwide.", ["public healthcare"], "noun", "/ˈhelθkeə(r)/"),
    ("longevity", "health", 3, "long life; length of life", "Diet is linked to longevity.", ["increase longevity"], "noun", "/lɒnˈdʒevəti/"),
    ("sedentary", "health", 3, "involving much sitting and little exercise", "A sedentary lifestyle raises risk.", ["sedentary behaviour"], "adjective", "/ˈsedntri/"),
    # --- technology ---
    ("internet", "technology", 1, "a global computer network", "The internet changed communication.", ["internet access"], "noun", "/ˈɪntənet/"),
    ("software", "technology", 1, "programs used by a computer", "The company sells accounting software.", ["install software"], "noun", "/ˈsɒftweə(r)/"),
    ("device", "technology", 1, "a piece of electronic equipment", "Each student had a mobile device.", ["handheld device"], "noun", "/dɪˈvaɪs/"),
    ("online", "technology", 1, "connected to or available on the internet", "Many courses are now online.", ["online learning"], "adjective", "/ˈɒnlaɪn/"),
    ("digital", "technology", 2, "using computer technology", "Digital skills are essential for jobs.", ["digital economy"], "adjective", "/ˈdɪdʒɪtl/"),
    ("cybersecurity", "technology", 2, "protection of systems from digital attacks", "Cybersecurity budgets have increased.", ["cybersecurity threat"], "noun", "/ˌsaɪbəsɪˈkjʊərəti/"),
    ("algorithm", "technology", 2, "a set of rules for solving a problem", "The app uses a simple algorithm.", ["search algorithm"], "noun", "/ˈælɡərɪðəm/"),
    ("artificial intelligence", "technology", 2, "computer systems that mimic human reasoning", "Artificial intelligence raises ethical questions.", ["AI system"], "noun phrase", "/ˌɑːtɪfɪʃl ɪnˈtelɪdʒəns/"),
    ("encryption", "technology", 3, "encoding data so only authorised users read it", "Encryption protects user messages.", ["end-to-end encryption"], "noun", "/ɪnˈkrɪpʃn/"),
    ("scalability", "technology", 3, "ability to grow without losing performance", "Scalability matters for startups.", ["cloud scalability"], "noun", "/ˌskeɪləˈbɪləti/"),
    ("disruptive", "technology", 3, "radically changing an industry or market", "Disruptive innovation reshaped retail.", ["disruptive technology"], "adjective", "/dɪsˈrʌptɪv/"),
    ("bandwidth", "technology", 3, "data capacity of a network connection", "Rural areas lack sufficient bandwidth.", ["network bandwidth"], "noun", "/ˈbændwɪdθ/"),
    # --- education ---
    ("compulsory schooling", "education", 1, "education that children are required by law to receive", "Compulsory schooling improves basic literacy nationwide.", ["compulsory schooling age"], "noun phrase", ""),
    ("educator", "education", 1, "a person who provides instruction or training", "Skilled educators can narrow attainment gaps.", ["qualified educator"], "noun", ""),
    ("exam", "education", 1, "a formal test of knowledge", "High-stakes exams shape university admissions.", ["pass an exam"], "noun", "/ɪɡˈzæm/"),
    ("coursework", "education", 1, "written or practical work completed during a course", "Coursework allows teachers to assess progress continuously.", ["submit coursework"], "noun", ""),
    ("scholarship", "education", 2, "money to support a student's studies", "She won a scholarship to university.", ["merit scholarship"], "noun", "/ˈskɒləʃɪp/"),
    ("enrolment", "education", 2, "the act of joining a course or school", "Enrolment numbers rose this year.", ["student enrolment"], "noun", "/ɪnˈrəʊlmənt/"),
    ("literacy", "education", 2, "ability to read and write", "Literacy rates improved in rural areas.", ["digital literacy"], "noun", "/ˈlɪtərəsi/"),
    ("tuition", "education", 2, "money paid for teaching", "Tuition fees worry many families.", ["tuition fees"], "noun", "/tjuˈɪʃn/"),
    ("pedagogy", "education", 3, "the method and practice of teaching", "Modern pedagogy emphasises collaboration.", ["innovative pedagogy"], "noun", "/ˈpedəɡɒdʒi/"),
    ("curriculum", "education", 3, "the full set of subjects taught", "The curriculum was updated nationally.", ["national curriculum"], "noun", "/kəˈrɪkjələm/"),
    ("extracurricular", "education", 3, "activities outside normal classes", "Sports are popular extracurricular activities.", ["extracurricular activities"], "adjective", "/ˌekstrəkəˈrɪkjələ(r)/"),
    ("accreditation", "education", 3, "official approval of quality standards", "The programme gained accreditation.", ["institutional accreditation"], "noun", "/əˌkredɪˈteɪʃn/"),
    # --- society ---
    ("family", "society", 1, "a group of related people", "Family support helps young people.", ["nuclear family"], "noun", "/ˈfæməli/"),
    ("community", "society", 1, "people living in one area or sharing interests", "The community organised a clean-up.", ["local community"], "noun", "/kəˈmjuːnəti/"),
    ("employment", "society", 1, "paid work; the state of having a job", "Youth employment remains a policy priority.", ["gain employment"], "noun", ""),
    ("crime", "society", 1, "illegal activity", "Street crime fell last year.", ["violent crime"], "noun", "/kraɪm/"),
    ("inequality", "society", 2, "unfair differences between groups", "Income inequality widened.", ["social inequality"], "noun", "/ˌɪnɪˈkwɒləti/"),
    ("welfare", "society", 2, "government support for people in need", "Welfare reform was controversial.", ["welfare benefits"], "noun", "/ˈwelfeə(r)/"),
    ("migration", "society", 2, "movement of people to a new place", "Rural migration increased city populations.", ["internal migration"], "noun", "/maɪˈɡreɪʃn/"),
    ("urbanisation", "society", 2, "growth of cities and movement to them", "Urbanisation changed land use.", ["rapid urbanisation"], "noun", "/ˌɜːbənaɪˈzeɪʃn/"),
    ("social cohesion", "society", 3, "unity and trust within a community", "Cuts to services threatened social cohesion.", ["promote social cohesion"], "noun phrase", "/ˈsəʊʃl kəʊˈhiːʒn/"),
    ("demographic", "society", 3, "relating to population structure", "Demographic shifts affect pensions.", ["demographic change"], "adjective", "/ˌdeməˈɡræfɪk/"),
    ("marginalised", "society", 3, "treated as unimportant or excluded", "Policies aimed to help marginalised groups.", ["marginalised communities"], "adjective", "/ˈmɑːdʒɪnəlaɪzd/"),
    ("gentrification", "society", 3, "wealthier people moving in and changing an area", "Gentrification raised rents sharply.", ["urban gentrification"], "noun", "/ˌdʒentrɪfɪˈkeɪʃn/"),
    # --- travel ---
    ("accommodation", "travel", 1, "a place where travellers can stay", "Affordable accommodation is scarce in peak season.", ["book accommodation"], "noun", ""),
    ("border control", "travel", 1, "official checks at national borders", "Stricter border control reduced irregular migration.", ["border control policy"], "noun phrase", ""),
    ("tourist", "travel", 1, "a person travelling for pleasure", "Tourist numbers peaked in summer.", ["foreign tourist"], "noun", "/ˈtʊərɪst/"),
    ("passport", "travel", 1, "an official document for international travel", "Check your passport expiry date.", ["valid passport"], "noun", "/ˈpɑːspɔːt/"),
    ("destination", "travel", 2, "the place someone is going to", "Bali is a popular destination.", ["tourist destination"], "noun", "/ˌdestɪˈneɪʃn/"),
    ("hospitality", "travel", 2, "friendly treatment of guests", "The region relies on hospitality jobs.", ["hospitality industry"], "noun", "/ˌhɒspɪˈtæləti/"),
    ("infrastructure", "travel", 2, "basic systems like transport and power", "Airport infrastructure was upgraded.", ["transport infrastructure"], "noun", "/ˈɪnfrəstrʌktʃə(r)/"),
    ("visa", "travel", 2, "permission to enter a country", "She applied for a student visa.", ["tourist visa"], "noun", "/ˈviːzə/"),
    ("overtourism", "travel", 3, "too many visitors harming a place", "Overtourism damaged historic centres.", ["combat overtourism"], "noun", "/ˌəʊvəˈtʊərɪzəm/"),
    ("sustainable tourism", "travel", 3, "tourism that protects environment and culture", "Sustainable tourism benefits locals.", ["promote sustainable tourism"], "noun phrase", "/səˈsteɪnəbl ˈtʊərɪzəm/"),
    ("connectivity", "travel", 3, "how well places are linked by transport", "Better connectivity boosted regional trade.", ["air connectivity"], "noun", "/ˌkɒnekˈtɪvəti/"),
    ("itinerary", "travel", 3, "a planned route or schedule for a trip", "The itinerary included three cities.", ["travel itinerary"], "noun", "/aɪˈtɪnərəri/"),
    # --- science ---
    ("experiment", "science", 1, "a test done to discover something", "The experiment showed clear results.", ["conduct an experiment"], "noun", "/ɪkˈsperɪmənt/"),
    ("research", "science", 1, "careful study to discover facts", "Medical research takes years.", ["scientific research"], "noun", "/rɪˈsɜːtʃ/"),
    ("discovery", "science", 1, "finding something new", "The discovery was published in Nature.", ["make a discovery"], "noun", "/dɪˈskʌvəri/"),
    ("laboratory", "science", 1, "a room for scientific work", "Samples were tested in the laboratory.", ["research laboratory"], "noun", "/ləˈbɒrətri/"),
    ("hypothesis", "science", 2, "an idea tested by experiments", "The hypothesis was later confirmed.", ["test a hypothesis"], "noun", "/haɪˈpɒθəsɪs/"),
    ("evidence", "science", 2, "facts that show something is true", "There is strong evidence for climate change.", ["scientific evidence"], "noun", "/ˈevɪdəns/"),
    ("peer review", "science", 2, "evaluation of research by other experts", "The paper passed peer review.", ["peer-reviewed journal"], "noun phrase", "/ˌpɪə rɪˈvjuː/"),
    ("methodology", "science", 2, "a system of methods used in research", "The methodology was clearly explained.", ["research methodology"], "noun", "/ˌmeθəˈdɒlədʒi/"),
    ("replicate", "science", 3, "to repeat a study and obtain similar results", "Other teams failed to replicate the findings.", ["replicate results"], "verb", "/ˈreplɪkeɪt/"),
    ("empirical", "science", 3, "based on observation or experiment", "The study provided empirical support.", ["empirical evidence"], "adjective", "/ɪmˈpɪrɪkl/"),
    ("paradigm", "science", 3, "a typical model or pattern of thought", "The discovery shifted the scientific paradigm.", ["research paradigm"], "noun", "/ˈpærədaɪm/"),
    ("quantify", "science", 3, "to measure or express as a quantity", "It is hard to quantify happiness.", ["quantify the impact"], "verb", "/ˈkwɒntɪfaɪ/"),
    # --- business ---
    ("company", "business", 1, "a business organisation", "The company hired fifty staff.", ["start a company"], "noun", "/ˈkʌmpəni/"),
    ("customer", "business", 1, "a person who buys goods or services", "Customer feedback improved the product.", ["loyal customer"], "noun", "/ˈkʌstəmə(r)/"),
    ("pricing", "business", 1, "the process of deciding how much to charge", "Dynamic pricing can increase revenue in peak demand.", ["competitive pricing"], "noun", ""),
    ("profit", "business", 1, "money gained after costs are paid", "The shop made a small profit.", ["make a profit"], "noun", "/ˈprɒfɪt/"),
    ("revenue", "business", 2, "income from business activities", "Revenue grew by 8% last year.", ["annual revenue"], "noun", "/ˈrevənjuː/"),
    ("competition", "business", 2, "rivalry between businesses", "Competition lowered consumer prices.", ["market competition"], "noun", "/ˌkɒmpəˈtɪʃn/"),
    ("investment", "business", 2, "money put in to gain profit later", "Foreign investment created jobs.", ["foreign investment"], "noun", "/ɪnˈvestmənt/"),
    ("entrepreneur", "business", 2, "a person who starts a business", "The entrepreneur launched a tech firm.", ["young entrepreneur"], "noun", "/ˌɒntrəprəˈnɜː(r)/"),
    ("merger", "business", 3, "when two companies combine into one", "The merger reduced operating costs.", ["merger and acquisition"], "noun", "/ˈmɜːdʒə(r)/"),
    ("liquidity", "business", 3, "availability of cash or assets that can be sold quickly", "The bank faced a liquidity crisis.", ["market liquidity"], "noun", "/lɪˈkwɪdəti/"),
    ("shareholder", "business", 3, "an owner of shares in a company", "Shareholders voted against the plan.", ["majority shareholder"], "noun", "/ˈʃeəˌhəʊldə(r)/"),
    ("diversification", "business", 3, "adding variety to reduce risk", "Diversification protected the firm from losses.", ["business diversification"], "noun", "/daɪˌvɜːsɪfɪˈkeɪʃn/"),
]


ANCHOR_SYNONYMS: dict[str, list[str]] = {
    "pollution": ["contamination", "impurity", "toxic waste"],
    "recycle": ["reuse", "reprocess", "repurpose"],
    "climate": ["weather patterns", "atmospheric conditions"],
    "renewable": ["sustainable", "regenerative"],
    "wildlife": ["fauna", "wild animals"],
    "deforestation": ["forest clearance", "logging"],
    "carbon footprint": ["emissions profile", "greenhouse impact"],
    "ecosystem": ["habitat system", "biotic community"],
    "mitigation": ["alleviation", "reduction"],
    "sustainability": ["long-term viability", "resource stewardship"],
    "biodiversity": ["species diversity", "ecological variety"],
    "emission": ["discharge", "release"],
    "exercise": ["physical activity", "workout"],
    "diet": ["nutrition", "food intake"],
    "stress": ["pressure", "strain"],
    "treatment": ["therapy", "medical care"],
    "obesity": ["overweight condition", "excess body weight"],
    "epidemic": ["outbreak", "widespread disease"],
    "mental health": ["psychological wellbeing", "emotional health"],
    "vaccination": ["immunisation", "inoculation"],
    "chronic": ["long-term", "persistent"],
    "healthcare": ["medical services", "health system"],
    "longevity": ["life expectancy", "lifespan"],
    "sedentary": ["inactive", "desk-bound"],
    "internet": ["world wide web", "online network"],
    "software": ["application", "program"],
    "device": ["gadget", "equipment"],
    "online": ["digital", "web-based"],
    "digital": ["computerised", "electronic"],
    "cybersecurity": ["information security", "data protection"],
    "algorithm": ["procedure", "computational rule"],
    "artificial intelligence": ["machine intelligence", "AI"],
    "encryption": ["encoding", "data scrambling"],
    "scalability": ["expandability", "growth capacity"],
    "disruptive": ["revolutionary", "game-changing"],
    "bandwidth": ["data capacity", "throughput"],
    "compulsory schooling": ["mandatory education", "required schooling"],
    "educator": ["instructor", "teacher"],
    "exam": ["assessment", "test"],
    "coursework": ["assignments", "written work"],
    "scholarship": ["grant", "bursary"],
    "enrolment": ["registration", "admission"],
    "literacy": ["reading ability", "reading proficiency"],
    "tuition": ["instruction fees", "course fees"],
    "pedagogy": ["teaching method", "instructional practice"],
    "curriculum": ["syllabus", "course of study"],
    "extracurricular": ["non-academic", "after-school"],
    "accreditation": ["certification", "official approval"],
    "family": ["household", "kin"],
    "community": ["society", "local population"],
    "employment": ["work", "labour market participation"],
    "crime": ["offence", "criminal activity"],
    "inequality": ["disparity", "imbalance"],
    "welfare": ["social support", "benefits"],
    "migration": ["relocation", "population movement"],
    "urbanisation": ["city growth", "urban expansion"],
    "social cohesion": ["social unity", "community solidarity"],
    "demographic": ["population-related", "statistical"],
    "marginalised": ["excluded", "disadvantaged"],
    "gentrification": ["urban renewal", "neighbourhood upgrading"],
    "accommodation": ["lodging", "housing"],
    "border control": ["immigration checks", "frontier security"],
    "tourist": ["visitor", "traveller"],
    "passport": ["travel document", "identity papers"],
    "destination": ["location", "travel spot"],
    "hospitality": ["guest services", "tourism services"],
    "infrastructure": ["public works", "facilities"],
    "visa": ["entry permit", "travel authorisation"],
    "overtourism": ["excessive tourism", "visitor overcrowding"],
    "sustainable tourism": ["responsible tourism", "eco-tourism"],
    "connectivity": ["transport links", "accessibility"],
    "itinerary": ["travel plan", "schedule"],
    "experiment": ["trial", "test"],
    "research": ["investigation", "study"],
    "discovery": ["finding", "breakthrough"],
    "laboratory": ["research lab", "testing facility"],
    "hypothesis": ["theory", "proposition"],
    "evidence": ["proof", "data"],
    "peer review": ["scholarly assessment", "expert evaluation"],
    "methodology": ["research method", "approach"],
    "replicate": ["reproduce", "repeat"],
    "empirical": ["evidence-based", "observational"],
    "paradigm": ["model", "framework"],
    "quantify": ["measure", "calculate"],
    "company": ["firm", "corporation"],
    "customer": ["client", "consumer"],
    "pricing": ["price setting", "cost structure"],
    "profit": ["earnings", "gain"],
    "revenue": ["income", "takings"],
    "competition": ["rivalry", "market contest"],
    "investment": ["capital allocation", "funding"],
    "entrepreneur": ["founder", "business starter"],
    "merger": ["consolidation", "amalgamation"],
    "liquidity": ["cash availability", "solvency"],
    "shareholder": ["investor", "stockholder"],
    "diversification": ["variety", "risk spreading"],
}


def _model_has_field(model, name: str) -> bool:
    try:
        model._meta.get_field(name)
        return True
    except Exception:
        return False


def bulk_create_words(WordModel, skip_if_exists: bool = True):
    """
    WordModel: historical Word from migration or concrete Word model.
    Returns (created_count, skipped_count).

    Idempotent: when ``skip_if_exists`` is True, rows that already match
    (topic, level, word) are left alone (except empty synonyms are backfilled
    when the schema supports it). ``synonyms`` is only set on create when the
    model includes that field (migration 0002 runs before 0013).
    """
    created = 0
    skipped = 0
    supports_synonyms = _model_has_field(WordModel, "synonyms")
    for row in INITIAL_WORD_ROWS:
        word, topic, level, definition, example, collocs, pos, phon = row[:8]
        syns = ANCHOR_SYNONYMS.get(word.lower(), [])
        existing = None
        if skip_if_exists:
            existing = (
                WordModel.objects.filter(topic=topic, level=level, word__iexact=word)
                .order_by("id")
                .first()
            )
        if existing is not None:
            if (
                supports_synonyms
                and syns
                and not (getattr(existing, "synonyms", None) or [])
            ):
                existing.synonyms = list(syns)
                existing.save(update_fields=["synonyms"])
            skipped += 1
            continue
        payload = {
            "word": word[:100],
            "topic": topic,
            "level": level,
            "definition": definition,
            "example_sentence": example,
            "collocations": list(collocs),
            "part_of_speech": pos[:50],
            "phonetic": phon[:100],
        }
        if supports_synonyms:
            payload["synonyms"] = list(syns)
        WordModel.objects.create(**payload)
        created += 1
    return created, skipped
