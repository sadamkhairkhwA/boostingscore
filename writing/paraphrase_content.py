"""IELTS Task 2-style source sentences for paraphrase practice, grouped by topic."""

from __future__ import annotations

import random

PARAPHRASE_TOPICS: list[tuple[str, str]] = [
    ("all", "All topics"),
    ("environment", "Environment"),
    ("health", "Health"),
    ("education", "Education"),
    ("technology", "Technology"),
    ("work", "Work"),
    ("globalisation", "Globalisation"),
    ("crime", "Crime"),
    ("media", "Media"),
    ("transport", "Transport"),
    ("culture", "Culture"),
    ("government", "Government"),
]

TOPIC_LABELS = dict(PARAPHRASE_TOPICS)

SENTENCES: dict[str, list[str]] = {
    "environment": [
        "Many governments are investing in public transport in order to reduce traffic congestion in cities.",
        "Climate change is widely regarded as one of the most pressing challenges facing humanity in the twenty-first century.",
        "The rapid destruction of rainforests has accelerated biodiversity loss across several tropical regions.",
        "Renewable energy sources are becoming increasingly affordable, which has encouraged wider adoption by households.",
        "Industrial pollution continues to contaminate rivers and coastal waters in densely populated areas.",
        "Some policymakers argue that economic growth should not come at the expense of environmental protection.",
        "Urban sprawl has placed considerable pressure on green spaces and wildlife habitats near major cities.",
        "Carbon emissions from aviation have risen sharply as international travel has become more accessible.",
        "Strict recycling schemes have helped many municipalities reduce the volume of waste sent to landfill.",
        "Scientists warn that failure to limit global warming could lead to more frequent extreme weather events.",
    ],
    "health": [
        "Sedentary lifestyles have contributed to a significant rise in obesity rates among young adults.",
        "Public healthcare systems often struggle to meet demand as populations age and chronic illness increases.",
        "Many experts believe that prevention programmes are more cost-effective than treating disease at a late stage.",
        "Mental health services remain underfunded in several countries despite growing awareness of psychological stress.",
        "Vaccination campaigns have played a crucial role in controlling the spread of infectious diseases.",
        "Poor diet and excessive sugar consumption are linked to long-term cardiovascular problems.",
        "Work-related stress has become a major cause of absenteeism in high-pressure corporate environments.",
        "Access to clean water and sanitation is still limited in some rural communities worldwide.",
        "Governments are debating whether junk food advertising should be restricted to protect children.",
        "Regular physical activity is associated with improved cognitive function and emotional wellbeing.",
    ],
    "education": [
        "Universities are under pressure to prepare graduates for a labour market that changes rapidly.",
        "Some parents believe that homework places unnecessary stress on primary school children.",
        "Online learning has expanded access to higher education for students in remote areas.",
        "Critics argue that standardised testing encourages rote memorisation rather than critical thinking.",
        "Funding inequalities between schools in wealthy and deprived areas remain a serious concern.",
        "Many employers now expect job applicants to demonstrate digital literacy alongside formal qualifications.",
        "Bilingual education programmes can strengthen cultural identity while improving language proficiency.",
        "Student loan debt has discouraged some young people from pursuing postgraduate study.",
        "Teacher training reforms are needed to raise classroom standards in underperforming regions.",
        "Extracurricular activities are thought to develop teamwork skills that formal lessons may not provide.",
    ],
    "technology": [
        "Artificial intelligence is transforming industries ranging from healthcare to financial services.",
        "Social media platforms have fundamentally altered how people consume news and form opinions.",
        "Concerns about data privacy have intensified as companies collect ever larger amounts of personal information.",
        "Automation threatens to displace workers in routine manufacturing and administrative roles.",
        "Remote working technology has enabled many employees to balance professional and family commitments.",
        "Cybersecurity breaches can cause severe financial damage to both businesses and public institutions.",
        "Some educators worry that excessive screen time may harm children's concentration and social skills.",
        "Governments are exploring regulations to ensure that algorithmic decisions are transparent and fair.",
        "Digital divide issues persist where rural communities lack reliable high-speed internet access.",
        "Technological innovation has accelerated medical research but also raised complex ethical questions.",
    ],
    "work": [
        "Flexible working arrangements have become more common since the widespread adoption of remote technology.",
        "Many young professionals prioritise job satisfaction over salary when choosing an employer.",
        "Gender pay gaps persist in several sectors despite decades of equal opportunity legislation.",
        "Automation may create new roles, but workers will need retraining to adapt to changing demands.",
        "High levels of job insecurity can undermine employee morale and productivity.",
        "Some companies offer mentorship programmes to help staff develop leadership capabilities.",
        "The gig economy provides flexibility for workers but often lacks stable benefits and protections.",
        "Workplace diversity initiatives aim to ensure that recruitment processes are fair and inclusive.",
        "Burnout has increased among healthcare staff working long shifts under intense pressure.",
        "Skilled migration is sometimes used to address labour shortages in specialised industries.",
    ],
    "globalisation": [
        "Global trade has lowered consumer prices but has also increased competition for domestic manufacturers.",
        "Multinational corporations often relocate production to countries with lower labour costs.",
        "Cultural exchange through travel and media has made societies more aware of international diversity.",
        "Some communities fear that globalisation erodes local traditions and languages over time.",
        "International supply chains can be disrupted by political conflict or natural disasters.",
        "Developing nations may benefit from foreign investment but risk economic dependency.",
        "Global migration has reshaped demographic patterns in many European and North American cities.",
        "Free trade agreements are frequently criticised for prioritising corporate interests over workers.",
        "International cooperation is essential to address problems such as climate change and pandemics.",
        "Tourism revenue supports local economies but can also damage fragile ecosystems if poorly managed.",
    ],
    "crime": [
        "CCTV surveillance is often promoted as an effective deterrent against street crime in urban centres.",
        "Many criminologists argue that poverty and unemployment are root causes of offending behaviour.",
        "Harsher prison sentences do not always lead to lower reoffending rates after release.",
        "Cybercrime has grown rapidly as more financial transactions are conducted online.",
        "Community policing initiatives aim to build trust between residents and law enforcement agencies.",
        "Some governments favour rehabilitation programmes over long-term incarceration for minor offences.",
        "Youth crime may be linked to a lack of constructive activities outside school hours.",
        "International cooperation is required to combat trafficking and organised criminal networks.",
        "Victims of crime often need psychological support as well as legal assistance.",
        "Debates continue over whether capital punishment serves as an effective deterrent.",
    ],
    "media": [
        "Traditional newspapers have lost readers as audiences migrate to digital news platforms.",
        "Misinformation can spread rapidly on social media before fact-checkers can respond.",
        "Advertising revenue largely funds free online content consumed by billions of users daily.",
        "Some critics believe that sensational reporting undermines public trust in journalism.",
        "Public broadcasters are expected to provide balanced coverage of political debates.",
        "Reality television programmes remain popular despite concerns about their social impact.",
        "Influencers now shape consumer behaviour in ways that challenge conventional marketing.",
        "Press freedom is considered essential to holding powerful institutions accountable.",
        "Children may be exposed to inappropriate content without effective parental controls online.",
        "Documentary filmmaking can raise awareness of social issues that receive little political attention.",
    ],
    "transport": [
        "Investment in high-speed rail could reduce reliance on short-haul domestic flights.",
        "Traffic congestion costs urban economies billions of dollars each year in lost productivity.",
        "Electric vehicles are becoming more viable as battery technology improves and prices fall.",
        "Cycling infrastructure encourages healthier commuting habits while lowering emissions.",
        "Airport expansion projects often face opposition from residents concerned about noise pollution.",
        "Reliable public transport is vital for people who cannot afford to own a private car.",
        "Road safety campaigns have helped reduce fatalities, though speeding remains a persistent problem.",
        "Freight transport emissions contribute significantly to a country's carbon footprint.",
        "Ride-sharing apps have changed how people travel in cities with limited taxi services.",
        "Poorly maintained rural roads can isolate communities and restrict access to essential services.",
    ],
    "culture": [
        "Museums play an important role in preserving national heritage for future generations.",
        "Global entertainment industries have made English-language films dominant in many markets.",
        "Some communities fear that tourism commodifies sacred traditions and cultural rituals.",
        "Arts funding is frequently cut during economic downturns despite its social value.",
        "Multicultural cities benefit from diverse cuisines, festivals, and creative collaboration.",
        "Language loss accelerates when younger generations prefer internationally dominant languages.",
        "Public libraries remain valuable spaces for learning and community engagement.",
        "Cultural stereotypes in media can reinforce prejudice and limit social integration.",
        "Historic buildings are sometimes demolished to make way for modern commercial development.",
        "International sporting events can foster national pride and cross-cultural understanding.",
    ],
    "government": [
        "Democratic elections are intended to ensure that leaders remain accountable to citizens.",
        "Corruption undermines public trust and diverts resources away from essential services.",
        "Some argue that smaller government reduces bureaucracy and encourages private enterprise.",
        "Welfare programmes are designed to protect vulnerable groups during periods of unemployment.",
        "Transparency laws allow journalists and citizens to scrutinise official decision-making.",
        "Tax reform remains politically sensitive because it affects income distribution directly.",
        "National security policies must balance civil liberties with the need to prevent terrorism.",
        "Local councils are responsible for delivering many services that affect daily life.",
        "Referendums give voters a direct say on major constitutional or policy questions.",
        "International aid is sometimes criticised for creating dependency rather than sustainable development.",
    ],
}


def all_sentences() -> list[tuple[str, str]]:
    """Return (topic_code, sentence) pairs across every topic."""
    out: list[tuple[str, str]] = []
    for topic, sentences in SENTENCES.items():
        for sentence in sentences:
            out.append((topic, sentence))
    return out


def pick_sentence(*, topic: str = "all", exclude: str | None = None) -> dict[str, str]:
    """Pick a random sentence; optionally exclude the current one (case-insensitive match)."""
    topic = (topic or "all").strip().lower()
    if topic == "all":
        pool = all_sentences()
    else:
        sentences = SENTENCES.get(topic, [])
        pool = [(topic, s) for s in sentences]
    if not pool:
        pool = all_sentences()
    exclude_norm = (exclude or "").strip().lower()
    if exclude_norm:
        filtered = [(t, s) for t, s in pool if s.strip().lower() != exclude_norm]
        if filtered:
            pool = filtered
    topic_code, sentence = random.choice(pool)
    return {
        "topic": topic_code,
        "topic_label": TOPIC_LABELS.get(topic_code, topic_code.title()),
        "sentence": sentence,
    }
