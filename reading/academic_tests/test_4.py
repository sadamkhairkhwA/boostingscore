"""
Hardcoded payload for IELTS Academic Reading Test 4 (client + server scoring).
"""
from __future__ import annotations

from .common import build_payload, q

PART1_HTML = """
<p class="art-pass__kicker">Part 1 · Notices</p>
<h1 class="art-pass__title">Public transport smart cards</h1>

<h2 class="art-pass__sub">Text A — Registering your smart card</h2>
<p>Registering your card takes less than five minutes online or at any staffed kiosk. You will need to provide your full name, date of birth and a valid email address when you sign up. Once registered, if your card is lost or stolen, any remaining balance is protected and will be transferred free of charge to a replacement card within ten working days. Unregistered cards can hold a maximum balance of <strong>£50</strong> and receive no refund if lost or stolen. Registered users can also view up to twelve months of journey history online and can set up automatic top-up, so that £10 is added automatically whenever the balance falls below <strong>£5</strong>. Concession status — child, student or senior — must be applied for separately and requires proof of age or eligibility to be uploaded before it is approved, which usually takes three working days.</p>

<h2 class="art-pass__sub">Text B — Zone fares and daily capping</h2>
<p>The network is divided into <strong>four</strong> fare zones, numbered 1 to 4, radiating out from the city centre. The fare for any journey depends on which zones you travel through, not simply the distance covered. Peak fares apply on weekdays between 6:30 and 9:30 in the morning and between 16:00 and 19:00 in the evening; all other times, including weekends, are charged at the cheaper off-peak rate. To protect frequent travellers, the system automatically applies a daily cap: once your tapped fares in a single day reach the price of an all-zone day pass, £8.40, no further fares are charged for the rest of that day. A weekly cap, worth <strong>five</strong> times the daily cap, applies from Monday to Sunday. Children under 11 travel free at all times when accompanied by a fare-paying adult. Children aged 11 to 15 must apply for a photocard and then travel at half the adult fare.</p>

<h2 class="art-pass__sub">Text C — Park-and-ride</h2>
<p>Five park-and-ride sites operate around the edge of the city, each linked to the centre by a dedicated shuttle bus every ten minutes at peak times. Parking is free for anyone who taps their smart card on both the car park barrier and the shuttle bus on the same day; drivers who park but do not use the shuttle are charged the standard £6 all-day parking rate. Passengers who tap in before 8:00 receive a discount of <strong>20%</strong> on the shuttle fare as an early-bird incentive. Season tickets covering parking and unlimited shuttle travel for one calendar month are available for £45 and must be bought in advance online; they cannot be purchased on the bus. Two of the five sites, Elmfield and Harborough, offer a limited number of electric vehicle charging bays, which must be booked in advance.</p>
"""

PART2_HTML = """
<p class="art-pass__kicker">Part 2 · Science &amp; environment</p>
<h1 class="art-pass__title">Vertical farming: growing food indoors</h1>

<p class="art-pass__sub">List of Headings</p>
<p><strong>i.</strong> The rising energy demands of climate-controlled growing systems<br>
<strong>ii.</strong> Crops for which vertical farming is not yet commercially practical<br>
<strong>iii.</strong> A brief history of skyscraper agriculture<br>
<strong>iv.</strong> Why urban buildings are being converted for new industries<br>
<strong>v.</strong> Defining a new way of growing food indoors<br>
<strong>vi.</strong> The role of government subsidies in funding new farms<br>
<strong>vii.</strong> Reduced water use and freedom from pest damage<br>
<strong>viii.</strong> Water conservation technologies used in traditional farming</p>

<p><strong>Paragraph 1</strong><br>
Vertical farming refers to the practice of growing crops in stacked layers, often inside repurposed warehouses, shipping containers or purpose-built towers, using artificial lighting and carefully controlled temperature and humidity rather than natural sunlight and soil. Most commercial systems rely on hydroponics, where roots sit in nutrient-rich water, or aeroponics, where roots are misted with a fine nutrient spray. Because the growing environment is entirely indoors, crops can be produced close to the cities where they will be sold, regardless of the season or the weather outside.</p>

<p><strong>Paragraph 2</strong><br>
Advocates highlight substantial resource savings. Because water is recirculated within a closed system rather than draining into the surrounding soil, vertical farms typically use up to <strong>95%</strong> less water than the same crop grown in an open field. The sealed growing environment also excludes most insects and airborne fungal spores, so many operators report that they can grow crops without any synthetic <strong>pesticides</strong> at all. Yields, measured per square metre of floor space, can be many times higher than conventional agriculture because plants are stacked in multiple layers and harvested continuously throughout the year.</p>

<p><strong>Paragraph 3</strong><br>
These benefits come at a cost. Growing food indoors means replacing free sunlight with banks of LED lights, which, together with the heating, cooling and dehumidifying systems needed to keep conditions stable, can make electricity the single largest ongoing expense for a vertical farm. Several high-profile companies, including AeroFarms in the United States, expanded rapidly on the promise of low running costs before struggling to make projected savings materialise, and both AeroFarms and other well-funded start-ups later filed for bankruptcy protection or scaled back operations. Analysts now generally agree that energy prices, not construction costs, will determine whether vertical farming becomes broadly profitable.</p>

<p><strong>Paragraph 4</strong><br>
Not every crop suits this style of production. Leafy greens such as lettuce and spinach, along with herbs like basil, grow quickly, weigh little and can be sold soon after harvest, making them well suited to vertical systems and a relatively quick return on investment. Staple crops such as wheat, rice and potatoes present a very different picture: they need far more growing space and sunlight-equivalent light per calorie produced, and their low market price per kilogram makes it difficult for indoor growers to recover the electricity costs involved. For this reason, most vertical farms currently in operation concentrate on high-value salad crops and herbs rather than staple foods.</p>

<p><strong>Paragraph 5</strong><br>
Beyond economics, supporters point to social and environmental advantages that go beyond the farm itself. Because produce is grown near the point of sale, the distance food must travel before reaching a supermarket shelf, sometimes called "food miles", can be cut dramatically, which in turn lowers the emissions associated with refrigerated transport. Disused urban buildings, from former factories to underground car parks, have been converted into growing facilities in cities such as London and Singapore, bringing new employment to areas that had lost their original industries. Critics counter that the number of jobs created is often modest relative to the capital invested and that many roles are highly automated.</p>

<p><strong>Paragraph 6</strong><br>
Looking ahead, some vertical farming companies are pairing their operations with renewable energy, installing solar panels or negotiating direct contracts with wind farms to offset electricity costs, while others are trialling artificial intelligence systems that adjust light, temperature and nutrient delivery automatically to reduce waste. Sceptics maintain that, even with these improvements, vertical farming will remain a niche supplement to, rather than a replacement for, conventional field agriculture, which still supplies the overwhelming majority of the world's calories. Most researchers in the field agree that the technology's long-term role will depend heavily on the future cost of clean electricity.</p>
"""

PART3_HTML = """
<p class="art-pass__kicker">Part 3 · Academic reading</p>
<h1 class="art-pass__title">The psychology of decision-making under uncertainty</h1>

<p><strong>A</strong><br>
For much of the twentieth century, economists modelled human choice using expected utility theory, which assumed that people weigh the probability and value of each possible outcome and select the option with the highest expected payoff. This "rational actor" model dominated policy and finance for decades, even though everyday observation suggested that people often chose in ways the theory could not easily explain. Beginning in the early 1970s, the psychologists Daniel Kahneman and Amos Tversky began a long collaboration examining how people actually make decisions when outcomes are uncertain, work that eventually reshaped economics as much as psychology and earned Kahneman a Nobel Prize in 2002.</p>

<p><strong>B</strong><br>
Kahneman and Tversky proposed that, rather than calculating probabilities precisely, people rely on mental shortcuts, or heuristics, that usually work well but can produce systematic errors. One such shortcut, the availability heuristic, leads people to judge how likely or common something is by how easily examples come to mind. After heavy media coverage of a shark attack, for instance, beach visitors often rate the danger of swimming as far higher than official statistics justify, while more common but less dramatic risks, such as drowning through fatigue, receive comparatively little attention.</p>

<p><strong>C</strong><br>
A second shortcut, anchoring, shows that an initial figure — even one known to be arbitrary — can distort later numerical judgements. In a now-famous 1974 experiment, Tversky and Kahneman asked participants to spin a wheel rigged to stop at either 10 or 65, and then estimate what percentage of African countries belonged to the United Nations. Participants who had spun the higher number gave substantially higher estimates than those who had spun the lower one, even though the wheel had no logical connection to the true answer, demonstrating that irrelevant starting points can anchor subsequent judgements.</p>

<p><strong>D</strong><br>
Perhaps the pair's most influential contribution was prospect theory, published in <strong>1979</strong>, which replaced expected utility theory as the leading account of decision-making under risk. Central to the theory is loss <strong>aversion</strong>: the finding that losing a given amount of money hurts roughly twice as much, psychologically, as gaining the same amount pleases. One consequence is that people tend to be risk-averse when choosing between gains but risk-seeking when choosing between losses, a pattern that can flip depending purely on whether a problem is framed in terms of lives saved or lives lost, even when the underlying statistics are identical.</p>

<p><strong>E</strong><br>
Alongside these shortcuts, researchers have documented widespread overconfidence, in which people overestimate the accuracy of their own knowledge or judgement. Surveys of driving ability consistently find that a large majority of drivers rate their skills as above average, a statistical impossibility for the group as a whole. Overconfidence is not confined to amateurs: studies of professional financial analysts have found that their stated confidence intervals for stock-price forecasts are far narrower than their actual error rates would justify, suggesting that expertise does not automatically protect against this bias.</p>

<p><strong>F</strong><br>
These findings have moved well beyond the laboratory. The economist Richard Thaler and the legal scholar Cass Sunstein popularised the idea of the "<strong>nudge</strong>", a small change in how choices are presented that steers behaviour without removing any option. Automatically enrolling employees in a workplace pension, while still allowing them to opt out, dramatically increases participation rates compared with schemes that require an active decision to join. Similarly, countries that changed organ donation policy from "opt-in", where citizens must register to donate, to "opt-out", where donation is assumed unless a person actively declines, have recorded substantially higher donor registration rates.</p>

<p><strong>G</strong><br>
Not every researcher accepts that these patterns should be labelled as errors. The psychologist Gerd Gigerenzer and others argue that many heuristics are "<strong>ecologically</strong> rational": they may look imperfect on abstract laboratory puzzles but perform well, and demand far less time and information, in the real-world environments where people actually use them. From this perspective, calling a heuristic a bias depends heavily on the task used to test it, and stripping away all context may unfairly make ordinary human judgement look worse than it is. The <strong>debate</strong> between the heuristics-and-biases tradition and its critics continues to shape how psychologists, economists and policymakers understand the limits — and the logic — of everyday decision-making.</p>
"""

INSTRUCTIONS = {
    1: "Part 1: Read three short texts about public transport smart cards (A, B, C). Q1–5: Matching. Q6–9: True/False/Not Given. Q10–14: Sentence completion.",
    2: "Part 2: Read the passage on vertical farming. Q15–18: Matching headings (paragraphs 1–4). Q19–22: Yes/No/Not Given. Q23–24: Sentence completion. Q25–27: Multiple choice.",
    3: "Part 3: Read the academic article on decision-making under uncertainty. Q28–32: Matching paragraphs (A–G). Q33–36: Multiple choice. Q37–40: Summary completion.",
}

PART_META = {
    1: {"label": "Part 1", "subtitle": "Public transport smart cards", "q_start": 1, "q_end": 14},
    2: {"label": "Part 2", "subtitle": "Vertical farming", "q_start": 15, "q_end": 27},
    3: {"label": "Part 3", "subtitle": "Decision-making under uncertainty", "q_start": 28, "q_end": 40},
}

HEADING_OPTIONS = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii"]

QUESTIONS = [
    # Part 1 — Questions 1–5: Matching (Text A/B/C)
    q(
        1,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a discount for travellers who tap in before a stated time",
        ["A", "B", "C"],
        "C",
        None,
        "Text C: an early-bird 20% discount applies to those who tap in before 8:00.",
    ),
    q(
        2,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a limit on how much money an unregistered card can hold",
        ["A", "B", "C"],
        "A",
        None,
        "Text A: unregistered cards can hold a maximum balance of £50.",
    ),
    q(
        3,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "free travel at any time for very young children",
        ["A", "B", "C"],
        "B",
        None,
        "Text B: children under 11 travel free at all times with a fare-paying adult.",
    ),
    q(
        4,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a requirement to upload proof before a concession is approved",
        ["A", "B", "C"],
        "A",
        None,
        "Text A: concessions require proof of age or eligibility to be uploaded before approval.",
    ),
    q(
        5,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a charge for parking that applies if the shuttle bus is not used",
        ["A", "B", "C"],
        "C",
        None,
        "Text C: drivers who park but do not use the shuttle pay the standard £6 all-day rate.",
    ),
    # Part 1 — Questions 6–9: True / False / Not Given
    q(
        6,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "A registered card holder whose card is stolen will not lose their remaining balance permanently.",
        ["True", "False", "Not Given"],
        "True",
        None,
        "Text A: a stolen card's balance is protected and transferred to a replacement card.",
    ),
    q(
        7,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "Off-peak fares apply on weekday mornings between 6:30 and 9:30.",
        ["True", "False", "Not Given"],
        "False",
        None,
        "Text B: peak, not off-peak, fares apply on weekday mornings between 6:30 and 9:30.",
    ),
    q(
        8,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "The smart card scheme was introduced before the park-and-ride shuttle service.",
        ["True", "False", "Not Given"],
        "Not Given",
        None,
        "None of the texts gives a date for when either scheme was introduced, so no comparison can be made.",
    ),
    q(
        9,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "Exactly two of the five park-and-ride sites provide electric vehicle charging.",
        ["True", "False", "Not Given"],
        "True",
        None,
        "Text C: Elmfield and Harborough offer electric vehicle charging bays.",
    ),
    # Part 1 — Questions 10–14: Sentence completion
    q(
        10,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "Unregistered smart cards may hold a maximum balance of £_____.",
        None,
        "50",
        ["50", "£50"],
        "Text A specifies a maximum balance of £50 for unregistered cards.",
    ),
    q(
        11,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "The automatic top-up feature adds £10 whenever the balance falls below £_____.",
        None,
        "5",
        ["5", "£5"],
        "Text A: £10 is added whenever the balance falls below £5.",
    ),
    q(
        12,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "The network is divided into _____ fare zones.",
        None,
        "four",
        ["four", "4"],
        "Text B: the network has four fare zones.",
    ),
    q(
        13,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "The weekly fare cap is worth _____ times the daily cap.",
        None,
        "five",
        ["five", "5"],
        "Text B: the weekly cap is worth five times the daily cap.",
    ),
    q(
        14,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "Passengers who tap in before 8:00 at park-and-ride sites receive a discount of _____%.",
        None,
        "20",
        ["20"],
        "Text C: an early-bird discount of 20% applies before 8:00.",
    ),
    # Part 2 — Questions 15–18: Matching headings (paragraphs 1–4)
    q(
        15,
        2,
        "para_match",
        "Questions 15–18",
        "Matching headings",
        "The passage has six numbered paragraphs, 1–6. Choose the correct heading for paragraphs 1–4 from the List of Headings above the passage. Write the correct number, i–viii.",
        "Paragraph 1",
        list(HEADING_OPTIONS),
        "v",
        None,
        "Paragraph 1 defines vertical farming as an indoor way of growing food.",
    ),
    q(
        16,
        2,
        "para_match",
        "Questions 15–18",
        "Matching headings",
        "The passage has six numbered paragraphs, 1–6. Choose the correct heading for paragraphs 1–4 from the List of Headings above the passage. Write the correct number, i–viii.",
        "Paragraph 2",
        list(HEADING_OPTIONS),
        "vii",
        None,
        "Paragraph 2 discusses reduced water use and freedom from pesticides.",
    ),
    q(
        17,
        2,
        "para_match",
        "Questions 15–18",
        "Matching headings",
        "The passage has six numbered paragraphs, 1–6. Choose the correct heading for paragraphs 1–4 from the List of Headings above the passage. Write the correct number, i–viii.",
        "Paragraph 3",
        list(HEADING_OPTIONS),
        "i",
        None,
        "Paragraph 3 focuses on the rising energy demands of lighting and climate control.",
    ),
    q(
        18,
        2,
        "para_match",
        "Questions 15–18",
        "Matching headings",
        "The passage has six numbered paragraphs, 1–6. Choose the correct heading for paragraphs 1–4 from the List of Headings above the passage. Write the correct number, i–viii.",
        "Paragraph 4",
        list(HEADING_OPTIONS),
        "ii",
        None,
        "Paragraph 4 explains why staple crops are not yet commercially viable indoors.",
    ),
    # Part 2 — Questions 19–22: Yes / No / Not Given
    q(
        19,
        2,
        "ynng",
        "Questions 19–22",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "Energy costs are likely to be the key factor in whether vertical farming becomes widely profitable.",
        ["Yes", "No", "Not Given"],
        "Yes",
        None,
        "Paragraph 3: analysts agree energy prices, not construction costs, will determine broad profitability.",
    ),
    q(
        20,
        2,
        "ynng",
        "Questions 19–22",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "AeroFarms successfully achieved the cost savings it had originally predicted.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 3: AeroFarms struggled to make projected savings materialise and later filed for bankruptcy protection.",
    ),
    q(
        21,
        2,
        "ynng",
        "Questions 19–22",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "Most vertical farming companies currently receive government subsidies for renewable energy equipment.",
        ["Yes", "No", "Not Given"],
        "Not Given",
        None,
        "The passage mentions solar panels and wind contracts but says nothing about government subsidies.",
    ),
    q(
        22,
        2,
        "ynng",
        "Questions 19–22",
        "Yes / No / Not Given",
        "Do the following statements agree with the views of the writer in the passage?",
        "The writer argues that vertical farming will soon replace conventional field agriculture as the main source of the world's food.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 6: vertical farming will remain a niche supplement, and field agriculture still supplies most calories.",
    ),
    # Part 2 — Questions 23–24: Sentence completion
    q(
        23,
        2,
        "gap",
        "Questions 23–24",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "Vertical farms can use up to _____% less water than open-field farming of the same crop.",
        None,
        "95",
        ["95"],
        "Paragraph 2: vertical farms typically use up to 95% less water.",
    ),
    q(
        24,
        2,
        "gap",
        "Questions 23–24",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "Many operators say they can avoid the use of any synthetic _____ in their crops.",
        None,
        "pesticides",
        ["pesticides"],
        "Paragraph 2: many operators grow crops without any synthetic pesticides at all.",
    ),
    # Part 2 — Questions 25–27: Multiple choice
    q(
        25,
        2,
        "mc",
        "Questions 25–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "According to Paragraph 3, what does the writer suggest is the biggest financial risk for vertical farms?",
        [
            "A. The high price of purpose-built towers",
            "B. The unpredictable cost of transporting produce",
            "C. The ongoing cost of electricity for lighting and climate control",
            "D. The scarcity of hydroponic growing equipment",
        ],
        "C",
        None,
        "Paragraph 3: electricity is described as the single largest ongoing expense.",
    ),
    q(
        26,
        2,
        "mc",
        "Questions 25–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "Why are leafy greens and herbs particularly suited to vertical farming, according to Paragraph 4?",
        [
            "A. They require no light at all to grow",
            "B. They grow quickly, are lightweight, and can be sold soon after harvest",
            "C. They are the only crops that can be grown hydroponically",
            "D. Governments provide subsidies exclusively for salad crops",
        ],
        "B",
        None,
        "Paragraph 4: leafy greens and herbs grow quickly, weigh little, and sell soon after harvest.",
    ),
    q(
        27,
        2,
        "mc",
        "Questions 25–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "What is the writer's overall assessment of the future of vertical farming, based on Paragraph 6?",
        [
            "A. It will completely replace traditional agriculture within a decade",
            "B. Its future role depends largely on the cost of clean electricity",
            "C. It has already failed as a viable technology",
            "D. It will only succeed if it stops using artificial intelligence",
        ],
        "B",
        None,
        "Paragraph 6: the technology's long-term role will depend heavily on the future cost of clean electricity.",
    ),
    # Part 3 — Questions 28–32: Matching paragraphs
    q(
        28,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "an experiment in which an unrelated number influenced people's numerical estimates",
        ["A", "B", "C", "D", "E", "F", "G"],
        "C",
        None,
        "Paragraph C describes the wheel-spinning anchoring experiment.",
    ),
    q(
        29,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "a description of how a change to a default option increased participation without banning any choice",
        ["A", "B", "C", "D", "E", "F", "G"],
        "F",
        None,
        "Paragraph F discusses pension auto-enrolment and opt-out organ donation.",
    ),
    q(
        30,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "a claim that shortcuts which appear flawed in laboratory tests may work well in real life",
        ["A", "B", "C", "D", "E", "F", "G"],
        "G",
        None,
        "Paragraph G presents the ecological rationality argument.",
    ),
    q(
        31,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "an example of professionals showing a bias usually associated with non-experts",
        ["A", "B", "C", "D", "E", "F", "G"],
        "E",
        None,
        "Paragraph E: professional financial analysts also show overconfidence.",
    ),
    q(
        32,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "the year in which a theory replacing an older model of rational choice was first published",
        ["A", "B", "C", "D", "E", "F", "G"],
        "D",
        None,
        "Paragraph D: prospect theory was published in 1979.",
    ),
    # Part 3 — Questions 33–36: Multiple choice
    q(
        33,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "According to Paragraph A, expected utility theory assumed that people",
        [
            "A. always followed advice from psychologists",
            "B. chose the option with the highest expected payoff",
            "C. were unaware of probability",
            "D. required government regulation to make decisions",
        ],
        "B",
        None,
        "Paragraph A: people select the option with the highest expected payoff.",
    ),
    q(
        34,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "What does the shark-attack example in Paragraph B illustrate?",
        [
            "A. People underestimate all risks after seeing media coverage",
            "B. People judge risk by how easily examples come to mind",
            "C. Drowning is more heavily reported than shark attacks",
            "D. Beach visitors rely on official statistics rather than memory",
        ],
        "B",
        None,
        "Paragraph B: the availability heuristic makes vivid, memorable events seem more likely.",
    ),
    q(
        35,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "In the wheel-spinning experiment described in Paragraph C, participants who spun a higher number",
        [
            "A. refused to give an estimate",
            "B. gave lower estimates than those who spun a lower number",
            "C. gave higher estimates than those who spun a lower number",
            "D. correctly guessed the percentage of African countries in the UN",
        ],
        "C",
        None,
        "Paragraph C: those who spun the higher number gave substantially higher estimates.",
    ),
    q(
        36,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "According to Paragraph E, studies of financial analysts suggest that professional expertise",
        [
            "A. eliminates overconfidence entirely",
            "B. does not automatically prevent overconfidence",
            "C. is unrelated to forecasting accuracy",
            "D. is only useful for short-term forecasts",
        ],
        "B",
        None,
        "Paragraph E: expertise does not automatically protect against overconfidence.",
    ),
    # Part 3 — Questions 37–40: Summary completion
    q(
        37,
        3,
        "summary",
        "Questions 37–40",
        "Summary completion",
        "Complete the summary. Choose NO MORE THAN ONE WORD from the passage for each answer.",
        "",
        None,
        "aversion",
        ["aversion"],
        "Paragraph D names loss aversion as central to prospect theory.",
        None,
    ),
    q(
        38,
        3,
        "summary",
        "Questions 37–40",
        "Summary completion",
        "Complete the summary. Choose NO MORE THAN ONE WORD from the passage for each answer.",
        "",
        None,
        "nudge",
        ["nudge"],
        "Paragraph F: Thaler and Sunstein popularised the idea of the nudge.",
        None,
    ),
    q(
        39,
        3,
        "summary",
        "Questions 37–40",
        "Summary completion",
        "Complete the summary. Choose NO MORE THAN ONE WORD from the passage for each answer.",
        "",
        None,
        "ecologically",
        ["ecologically"],
        "Paragraph G: heuristics are described as ecologically rational.",
        None,
    ),
    q(
        40,
        3,
        "summary",
        "Questions 37–40",
        "Summary completion",
        "Complete the summary. Choose NO MORE THAN ONE WORD from the passage for each answer.",
        "",
        None,
        "debate",
        ["debate"],
        "Paragraph G closes by referring to the ongoing debate between the two camps.",
        None,
    ),
]

SUMMARY_INTRO_HTML = """
<p class="art-sum-intro">Kahneman and Tversky's prospect theory, published in 1979, introduced the concept of loss <span class="art-sum-slot" data-q="37" tabindex="0">37</span>, the idea that losses feel more painful than equivalent gains feel pleasant. Building on this behavioural research, Thaler and Sunstein argued that a small "<span class="art-sum-slot" data-q="38" tabindex="0">38</span>" in how choices are presented can steer behaviour without removing any option, as shown by opt-out schemes for pensions and organ donation. However, critics such as Gigerenzer contend that many heuristics are <span class="art-sum-slot" data-q="39" tabindex="0">39</span> rational, performing well in real-world settings even when they appear flawed in the laboratory. This ongoing <span class="art-sum-slot" data-q="40" tabindex="0">40</span> continues to shape how researchers understand everyday judgement.</p>
"""

TOPIC_CHIPS = [
    {"icon": "city", "color": "navy", "label": "Public transport smart cards"},
    {"icon": "leaf", "color": "green", "label": "Vertical farming (science)"},
    {"icon": "brain", "color": "purple", "label": "Decision-making under uncertainty"},
]


def get_payload() -> dict:
    return build_payload(
        test_number=4,
        title_bar="IELTS Academic Reading · Test 4",
        part1_html=PART1_HTML,
        part2_html=PART2_HTML,
        part3_html=PART3_HTML,
        instructions=INSTRUCTIONS,
        part_meta=PART_META,
        questions=QUESTIONS,
        summary_intro_html=SUMMARY_INTRO_HTML,
        results_meta={
            "part1Title": "Part 1 — Public transport smart cards",
            "part2Title": "Part 2 — Vertical farming",
            "part3Title": "Part 3 — Decision-making under uncertainty",
        },
    )
