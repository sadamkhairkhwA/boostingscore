"""
Hardcoded payload for IELTS Academic Reading Test 2 (client + server scoring).
"""
from __future__ import annotations

from .common import q, build_payload

PART1_HTML = """
<p class="art-pass__kicker">Part 1 · Urban food</p>
<h1 class="art-pass__title">Growing and selling food in the city</h1>

<h2 class="art-pass__sub">Text A — Riverside Community Garden</h2>
<p>Riverside Community Garden offers allotment-style growing space to residents of the borough who are aged <strong>eighteen</strong> or over. The site currently has <strong>forty</strong> individual plots, each measuring four metres by five metres, available on an annual basis for a rental fee of <strong>£45</strong>. The fee covers access to a shared toolshed, a mains water supply, and three communal compost bins near the main entrance. Anyone who signs up must attend a half-day <strong>induction</strong> session, at which they are shown how to use the shared equipment safely before being given a key to the site. A plot that is left uncultivated for more than <strong>eight</strong> weeks may be withdrawn from its holder and offered to someone on the waiting list, which currently runs to more than thirty names. Gardeners may add most kitchen and garden waste to the compost bins, but cooked food and meat must never be included, since they attract pests. On the first Saturday of every month, plot-holders are invited to bring surplus vegetables to a collection point by the gate, from where they are delivered to a local food bank. The garden committee, made up of volunteer plot-holders, meets every other month to review the waiting list and to organise seasonal events such as a spring seed swap and an autumn harvest lunch. New applicants who cannot yet be offered a full plot are welcome to join a shared "starter bed," where several beginners divide a single plot between them and learn basic growing skills before applying for a plot of their own.</p>

<h2 class="art-pass__sub">Text B — GreenLeaf Hydroponics Facility</h2>
<p>GreenLeaf Hydroponics Facility is a commercial indoor farm that supplies supermarkets and restaurants within fifty miles of the city centre. Crops are grown without soil, in trays fed by a closed-loop system that recycles water and nutrients; as a result, the facility uses roughly <strong>90%</strong> less water than an equivalent outdoor farm growing the same crops. Under banks of LED lighting, staff cultivate leafy greens such as lettuce and spinach, along with fresh herbs and <strong>strawberries</strong>, all year round regardless of the weather outside. No pesticides are used, since pests are largely excluded from the sealed growing rooms; nutrients are instead delivered directly to the plant roots through the water supply. The facility produces around two tonnes of produce every week. Members of the public may join a guided tour on Wednesday afternoons, but visitors who want a private tour outside the regular slot must book at least <strong>three</strong> days in advance and must form a group of at least <strong>six</strong> people, since smaller groups are simply combined with the standing Wednesday tour instead. School groups are charged a reduced rate and are given a short talk on how hydroponic growing differs from traditional farming before walking through the growing rooms behind a glass viewing corridor. The facility also runs a small research corner where university students test new crop varieties under slightly different light and nutrient combinations, feeding results back to the main growing team.</p>

<h2 class="art-pass__sub">Text C — Saturday Farmers' Market: Rules for Stallholders</h2>
<p>Stallholders wishing to trade at the Saturday Farmers' Market, held on Elm Street from 8am to 1pm every week of the year except public holidays, must agree to a short set of rules before they are accepted. Vendors must grow, rear, or make at least <strong>80%</strong> of what they sell themselves, and all produce must be sourced from within <strong>40</strong> miles of the market square, so that customers can be confident they are buying genuinely local goods. The standard stall fee is <strong>£15</strong> per week, although vendors who commit to the whole ten-week season in advance pay a reduced rate of <strong>£120</strong> for the full run. Any stallholder who cancels less than <strong>48</strong> hours before market day forfeits that week's fee, since the space cannot usually be reallocated at short notice. Single-use plastic bags are banned at every stall, and customers are encouraged to bring their own reusable bags. New applicants are first offered a trial period of <strong>four</strong> weeks, during which a small committee reviews feedback from customers and neighbouring stallholders before granting a permanent pitch. Stallholders are responsible for their own weighing scales, price labels, and card payment machines, and each must display a laminated certificate confirming that their produce meets the market's local-sourcing rule. A market manager patrols the site each week to check that stalls are set up safely and that walkways between rows remain clear for wheelchair users and pushchairs.</p>
"""

PART2_HTML = """
<p class="art-pass__kicker">Part 2 · History &amp; business</p>
<h1 class="art-pass__title">The Penny Post: reforming Britain's mail</h1>

<p class="art-pass__sub">List of Headings</p>
<p><strong>i.</strong> A civil servant challenges the existing system<br>
<strong>ii.</strong> Complicated and costly charges before reform<br>
<strong>iii.</strong> A single fixed price replaces distance-based fees<br>
<strong>iv.</strong> The launch of the first adhesive stamp<br>
<strong>v.</strong> Rapid growth in letter volumes after the reform<br>
<strong>vi.</strong> Other countries copy the British model<br>
<strong>vii.</strong> Complaints about delays in sorting and handling<br>
<strong>viii.</strong> A modern electronic service replaces paper letters</p>

<p><strong>Paragraph 1</strong><br>
Before 1840, sending a letter in Britain was complicated and expensive. Charges depended on the distance a letter travelled and the number of sheets of paper used, so a short note sent a long distance could cost several shillings — a sum well beyond the daily wage of a labourer. Postage was usually paid by the recipient rather than the sender, and postal clerks referred to elaborate rate tables to calculate each charge. Because the cost fell on the person receiving the letter, many poorer households simply refused delivery, and the Post Office lost revenue on items that were never collected. Merchants and families alike devised ways around the expense, sometimes writing coded messages on the outside of a folded sheet so that a recipient could glean the gist of the news without paying to accept the letter at all.</p>

<p><strong>Paragraph 2</strong><br>
The reform movement is closely associated with Rowland Hill, a schoolteacher and civil servant from Kidderminster. In 1837 Hill published a pamphlet titled <em>Post Office Reform: Its Importance and Practicability</em>, arguing that the cost of moving a letter between two towns was almost entirely the cost of handling and sorting it, not the physical distance it travelled. He proposed a single, low, prepaid charge that would apply no matter how far a letter travelled within the United Kingdom. Officials at the Post Office were initially sceptical, warning that the change would slash revenue, but Hill's arguments won support in Parliament and among reform-minded newspapers. A parliamentary committee examined his figures line by line before recommending the scheme for adoption, and Hill himself was later given a temporary post at the Treasury to help oversee the change he had championed.</p>

<p><strong>Paragraph 3</strong><br>
Following an official inquiry, the government adopted Hill's scheme, and on <strong>10 January</strong> 1840 the Uniform Penny Post came into force across Britain. Any letter weighing up to half an ounce could now be sent to any address in the country for a single fee of one penny, provided the postage was paid in advance by the sender rather than collected from the recipient. The reform immediately overturned the old system of location-based charges, and the public responded with enthusiasm: local post offices reported queues of customers eager to send letters that they had previously judged too costly to post.</p>

<p><strong>Paragraph 4</strong><br>
To make prepayment simple and verifiable, the Post Office issued the world's first adhesive postage stamp on <strong>1 May</strong> 1840, valid for use from 6 May. Known today as the Penny Black, it carried an engraved profile of the young <strong>Queen Victoria</strong> and cost one penny, matching the new uniform rate. Customers could buy sheets of stamps in advance, lick the gum on the back, and affix a stamp to a letter without visiting a post office counter for every item they wished to send. The design proved so effective that other countries soon issued their own adhesive stamps modelled on the British example.</p>

<p><strong>Paragraph 5</strong><br>
The effects of the reform were dramatic. In the year before the change, the Post Office had carried around eighty-two million letters; within a decade, the figure had risen to more than three hundred million. Businesses used the cheaper, predictable postage to send invoices, catalogues, and circulars across the country, while ordinary families exchanged letters far more frequently than before. Historians generally credit the Penny Post with helping to knit together an increasingly literate and mobile population, supporting the growth of mail-order commerce and long-distance correspondence between friends and relatives separated by industrial-era migration to the cities. Newspapers of the period reported that clerks in the largest sorting offices were soon working through the night to keep pace with the volume of mail passing through the capital alone.</p>

<p><strong>Paragraph 6</strong><br>
Rowland Hill's model was widely imitated abroad. The United States, several European states, and colonies across the British Empire introduced their own uniform, prepaid postage systems within a few decades, often citing the British reform explicitly as a template. Hill was knighted for his services to the Post Office, and today collectors around the world still prize surviving examples of the Penny Black as founding artefacts of modern philately. The basic principle he championed — a flat rate that depends on weight rather than distance — remains at the heart of standard domestic postal pricing in many countries. Museums and philatelic societies continue to mark the anniversary of the reform each January, treating it as a milestone in the wider history of communication.</p>
"""

PART3_HTML = """
<p class="art-pass__kicker">Part 3 · Academic reading</p>
<h1 class="art-pass__title">Dark matter: the universe's missing mass</h1>

<p><strong>A</strong><br>
Astronomers have long known that the matter we can see — stars, planets, gas, and dust — cannot account for the total mass inferred from the gravitational behaviour of galaxies and galaxy clusters. Observations repeatedly detect far more gravitational pull than the visible material could produce, leading physicists to propose the existence of "dark matter": an invisible substance that neither emits nor absorbs light but exerts gravitational influence on its surroundings. Unlike black holes or cold gas clouds, dark matter cannot be detected by conventional telescopes; its presence must instead be inferred indirectly, through its gravitational effects on the motion of stars, galaxies, and light itself.</p>

<p><strong>B</strong><br>
The first serious hint of missing mass came in 1933, when the Swiss astronomer Fritz Zwicky studied the Coma Cluster, a group of galaxies bound together by mutual gravity. By measuring how fast individual galaxies within the cluster were moving, Zwicky calculated that the cluster's total mass had to be several hundred times greater than the mass suggested by its visible starlight. He coined the term <em>dunkle Materie</em>, or "dark matter," to describe this unseen mass, though his conclusions attracted little attention for several decades.</p>

<p><strong>C</strong><br>
Zwicky's claim was largely overlooked until the 1970s, when the American astronomer Vera Rubin, working with Kent Ford, measured the rotation speeds of stars within spiral galaxies. Newtonian physics predicts that stars far from a galaxy's centre should orbit more slowly than stars closer in, much as outer planets orbit the Sun more slowly than inner ones. Instead, Rubin and Ford found that rotation speeds remained roughly constant at all distances from the galactic centre, a pattern now known as a flat <strong>rotation</strong> curve. The observation strongly implied that each galaxy is embedded in a much larger, invisible halo of matter extending well beyond its visible disc.</p>

<p><strong>D</strong><br>
Physicists distinguish dark matter from dark energy, a separate and even less understood phenomenon associated with the accelerating expansion of the universe. Because dark matter interacts through gravity but produces no detectable light, most researchers assume it consists of particles unlike any found in ordinary atoms; leading candidates include weakly interacting massive particles, commonly called WIMPs, and hypothetical light particles known as axions. Crucially, dark matter is not simply matter that is too faint to see: precise calculations based on the cosmic microwave background indicate that ordinary, or "baryonic," matter cannot supply nearly enough mass to explain the observed gravitational effects, regardless of how much of it remains unobserved.</p>

<p><strong>E</strong><br>
Some of the most persuasive evidence for dark matter comes from gravitational lensing, the bending of light around massive objects predicted by general relativity. In the Bullet Cluster, a system formed by the collision of two galaxy clusters, astronomers mapped the distribution of mass using lensing effects and compared it with maps of hot, glowing gas made using X-ray telescopes. The two maps did not match: most of the mass, revealed through lensing, was offset from the visible gas, which had been slowed by the collision. This separation is difficult to explain without invoking an invisible component that passed through the collision largely unaffected, exactly as dark matter would be expected to behave.</p>

<p><strong>F</strong><br>
Not every physicist accepts the dark matter explanation. In the 1980s, the Israeli physicist Mordehai Milgrom proposed Modified Newtonian Dynamics, or MOND, which suggests that the law of gravity itself behaves differently at the extremely weak accelerations found at galactic edges, removing the need for unseen mass. MOND can reproduce flat rotation curves for many individual galaxies without invoking dark matter, but it has struggled to account for cluster-scale observations such as the Bullet Cluster and for the detailed pattern of fluctuations seen in the cosmic microwave background. For these reasons, the great majority of cosmologists continue to favour particle-based dark matter over modified gravity, although the debate has not been entirely settled.</p>

<p><strong>G</strong><br>
Detecting dark matter particles directly remains one of the great unsolved challenges in physics. Experiments such as the <strong>XENON</strong> series, housed deep underground to shield sensitive detectors from cosmic radiation, search for the extremely rare collisions that a WIMP might have with ordinary atomic nuclei. <strong>Particle</strong> accelerators, including the Large Hadron Collider, attempt to create dark matter candidates in high-energy collisions. According to current cosmological models, dark matter makes up roughly twenty-seven percent of the universe's total mass-energy content, compared with around five percent for ordinary matter, with the remainder attributed to dark energy. Until a dark matter particle is detected directly in a laboratory, its precise identity will remain one of the central open questions in modern cosmology.</p>
"""

INSTRUCTIONS = {
    1: "Part 1: Read three short texts about growing and selling food in the city (A, B, C). Q1–5: Matching. Q6–9: True/False/Not Given. Q10–14: Sentence completion.",
    2: "Part 2: Read the passage on the 1840 Penny Post reform. Q15–18: Matching headings. Q19–22: Yes/No/Not Given. Q23–24: Sentence completion. Q25–27: Multiple choice.",
    3: "Part 3: Read the academic article on dark matter. Q28–32: Matching paragraphs (A–G). Q33–36: Multiple choice. Q37–40: Summary completion.",
}

PART_META = {
    1: {"label": "Part 1", "subtitle": "Growing & selling food in the city", "q_start": 1, "q_end": 14},
    2: {"label": "Part 2", "subtitle": "The Penny Post reform", "q_start": 15, "q_end": 27},
    3: {"label": "Part 3", "subtitle": "Dark matter", "q_start": 28, "q_end": 40},
}

TOPIC_CHIPS = ["Urban food systems", "Postal history", "Dark matter cosmology"]

QUESTIONS = [
    q(
        1,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a rule that stallholders lose their payment if they cancel at short notice",
        ["A", "B", "C"],
        "C",
        None,
        "Text C: cancelling less than 48 hours before market day forfeits that week's fee.",
    ),
    q(
        2,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a facility that uses far less water than conventional growing methods",
        ["A", "B", "C"],
        "B",
        None,
        "Text B: the facility uses roughly 90% less water than an equivalent outdoor farm.",
    ),
    q(
        3,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a waiting list for people wanting their own growing space",
        ["A", "B", "C"],
        "A",
        None,
        "Text A: a waiting list of more than thirty names for plots.",
    ),
    q(
        4,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a minimum group size required to book a private visit",
        ["A", "B", "C"],
        "B",
        None,
        "Text B: private tours need a group of at least six people.",
    ),
    q(
        5,
        1,
        "match",
        "Questions 1–5",
        "Matching",
        "Which text (A, B, or C) contains the following information?",
        "a requirement that goods sold must be mostly produced by the seller",
        ["A", "B", "C"],
        "C",
        None,
        "Text C: vendors must grow, rear, or make at least 80% of what they sell.",
    ),
    q(
        6,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "Riverside Community Garden plots may only be rented by people aged eighteen or over.",
        ["True", "False", "Not Given"],
        "True",
        None,
        "Text A: growing space is offered to residents aged eighteen or over.",
    ),
    q(
        7,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "GreenLeaf Hydroponics Facility relies on pesticides to keep pests off its crops.",
        ["True", "False", "Not Given"],
        "False",
        None,
        "Text B: no pesticides are used because pests are largely excluded from the sealed rooms.",
    ),
    q(
        8,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "The Saturday Farmers' Market allows stallholders to source all of their produce from anywhere in the country.",
        ["True", "False", "Not Given"],
        "False",
        None,
        "Text C: produce must be sourced from within 40 miles of the market square.",
    ),
    q(
        9,
        1,
        "tfng",
        "Questions 6–9",
        "True / False / Not Given",
        "Do the following statements agree with the information in the texts?",
        "GreenLeaf Hydroponics Facility was established in 2015.",
        ["True", "False", "Not Given"],
        "Not Given",
        None,
        "Text B never states a founding date for the facility.",
    ),
    q(
        10,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "Riverside Community Garden currently has _____ individual plots.",
        None,
        "forty",
        ["forty", "40"],
        "Text A states there are forty individual plots.",
    ),
    q(
        11,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "New members of the community garden must attend a half-day _____ session before receiving a key.",
        None,
        "induction",
        ["induction"],
        "Text A: a half-day induction session is required before a key is issued.",
    ),
    q(
        12,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "GreenLeaf Hydroponics Facility uses LED lighting to grow crops such as leafy greens, herbs and _____.",
        None,
        "strawberries",
        ["strawberries"],
        "Text B lists strawberries among the crops grown year round.",
    ),
    q(
        13,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "Vendors at the Saturday Farmers' Market must source their produce from within _____ miles of the market square.",
        None,
        "40",
        ["40", "forty"],
        "Text C requires produce to be sourced from within 40 miles.",
    ),
    q(
        14,
        1,
        "gap",
        "Questions 10–14",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the texts for each answer.",
        "A full ten-week season stall fee at the farmers' market costs £_____.",
        None,
        "120",
        ["120"],
        "Text C: the full-season rate is £120.",
    ),
    q(
        15,
        2,
        "para_match",
        "Questions 15–18",
        "Matching headings",
        "The passage has six numbered paragraphs, 1–6. Choose the correct heading for paragraphs 1–4 from the List of Headings above the passage. Write the correct number, i–viii.",
        "Paragraph 1",
        ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii"],
        "ii",
        None,
        "Paragraph 1 describes the complicated, distance-based charges before reform.",
    ),
    q(
        16,
        2,
        "para_match",
        "Questions 15–18",
        "Matching headings",
        "The passage has six numbered paragraphs, 1–6. Choose the correct heading for paragraphs 1–4 from the List of Headings above the passage. Write the correct number, i–viii.",
        "Paragraph 2",
        ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii"],
        "i",
        None,
        "Paragraph 2 describes Rowland Hill challenging the existing system.",
    ),
    q(
        17,
        2,
        "para_match",
        "Questions 15–18",
        "Matching headings",
        "The passage has six numbered paragraphs, 1–6. Choose the correct heading for paragraphs 1–4 from the List of Headings above the passage. Write the correct number, i–viii.",
        "Paragraph 3",
        ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii"],
        "iii",
        None,
        "Paragraph 3 introduces the single fixed price replacing distance-based fees.",
    ),
    q(
        18,
        2,
        "para_match",
        "Questions 15–18",
        "Matching headings",
        "The passage has six numbered paragraphs, 1–6. Choose the correct heading for paragraphs 1–4 from the List of Headings above the passage. Write the correct number, i–viii.",
        "Paragraph 4",
        ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii"],
        "iv",
        None,
        "Paragraph 4 describes the launch of the Penny Black adhesive stamp.",
    ),
    q(
        19,
        2,
        "ynng",
        "Questions 19–22",
        "Yes / No / Not Given",
        "Do the following statements agree with the claims of the writer in the passage?",
        "Before 1840, postage costs were usually paid by the person receiving the letter, not the sender.",
        ["Yes", "No", "Not Given"],
        "Yes",
        None,
        "Paragraph 1: postage was usually paid by the recipient rather than the sender.",
    ),
    q(
        20,
        2,
        "ynng",
        "Questions 19–22",
        "Yes / No / Not Given",
        "Do the following statements agree with the claims of the writer in the passage?",
        "Rowland Hill argued that the distance a letter travelled was the main factor in the cost of delivering it.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 2: Hill argued the cost was mainly handling and sorting, not distance.",
    ),
    q(
        21,
        2,
        "ynng",
        "Questions 19–22",
        "Yes / No / Not Given",
        "Do the following statements agree with the claims of the writer in the passage?",
        "The Penny Black stamp featured an image of Rowland Hill.",
        ["Yes", "No", "Not Given"],
        "No",
        None,
        "Paragraph 4: the stamp carried a profile of Queen Victoria, not Rowland Hill.",
    ),
    q(
        22,
        2,
        "ynng",
        "Questions 19–22",
        "Yes / No / Not Given",
        "Do the following statements agree with the claims of the writer in the passage?",
        "Rowland Hill received a monetary reward from Parliament for his proposal.",
        ["Yes", "No", "Not Given"],
        "Not Given",
        None,
        "Paragraph 6 mentions Hill was knighted, but no monetary reward is mentioned.",
    ),
    q(
        23,
        2,
        "gap",
        "Questions 23–24",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "Before the Penny Post reform, postage charges depended on distance and the number of _____ of paper used.",
        None,
        "sheets",
        ["sheets"],
        "Paragraph 1: charges depended on distance and the number of sheets of paper used.",
    ),
    q(
        24,
        2,
        "gap",
        "Questions 23–24",
        "Sentence completion",
        "Complete the sentences. Write ONE WORD AND/OR A NUMBER from the passage for each answer.",
        "The Penny Black adhesive stamp was issued on 1 _____ 1840.",
        None,
        "May",
        ["May"],
        "Paragraph 4: the stamp was issued on 1 May 1840.",
    ),
    q(
        25,
        2,
        "mc",
        "Questions 25–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "According to Paragraph 1, why did some households refuse to accept letters?",
        [
            "A. They could not read the address on the envelope",
            "B. They did not want to pay the postage on delivery",
            "C. The letters were often damaged in transit",
            "D. Post office clerks refused to deliver them",
        ],
        "B",
        None,
        "Paragraph 1: because the cost fell on the recipient, many poorer households refused delivery.",
    ),
    q(
        26,
        2,
        "mc",
        "Questions 25–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "What was Rowland Hill's main argument in his 1837 pamphlet?",
        [
            "A. Postage rates should rise significantly for everyone",
            "B. The cost of delivering a letter mainly resulted from handling, not distance",
            "C. Letters should be delivered completely free of charge",
            "D. The Post Office should be closed down entirely",
        ],
        "B",
        None,
        "Paragraph 2: Hill argued the cost was almost entirely handling and sorting, not distance.",
    ),
    q(
        27,
        2,
        "mc",
        "Questions 25–27",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "What does the passage suggest about the effect of the Penny Post on business?",
        [
            "A. Businesses avoided using the new postal system",
            "B. Businesses used cheaper postage to send materials such as invoices and catalogues",
            "C. Businesses were charged a higher rate than private individuals",
            "D. Businesses stopped using paper correspondence entirely",
        ],
        "B",
        None,
        "Paragraph 5: businesses used the cheaper, predictable postage to send invoices, catalogues, and circulars.",
    ),
    q(
        28,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "a description of an experiment designed to detect dark matter particles deep underground",
        ["A", "B", "C", "D", "E", "F", "G"],
        "G",
        None,
        "Paragraph G describes the XENON detectors housed deep underground.",
    ),
    q(
        29,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "an explanation of why dark matter is considered distinct from dark energy",
        ["A", "B", "C", "D", "E", "F", "G"],
        "D",
        None,
        "Paragraph D distinguishes dark matter from dark energy.",
    ),
    q(
        30,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "an early calculation suggesting a galaxy cluster's mass was far greater than its visible stars indicated",
        ["A", "B", "C", "D", "E", "F", "G"],
        "B",
        None,
        "Paragraph B describes Zwicky's 1933 calculation of the Coma Cluster's mass.",
    ),
    q(
        31,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "a comparison between two different maps of mass in a colliding pair of galaxy clusters",
        ["A", "B", "C", "D", "E", "F", "G"],
        "E",
        None,
        "Paragraph E compares lensing and X-ray maps of the Bullet Cluster.",
    ),
    q(
        32,
        3,
        "para_match",
        "Questions 28–32",
        "Matching paragraphs",
        "Which paragraph contains the following information? Choose A–G.",
        "an alternative theory that modifies the law of gravity instead of proposing unseen particles",
        ["A", "B", "C", "D", "E", "F", "G"],
        "F",
        None,
        "Paragraph F describes Milgrom's Modified Newtonian Dynamics (MOND).",
    ),
    q(
        33,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "What did Vera Rubin and Kent Ford discover about spiral galaxies?",
        [
            "A. Stars at the edge of galaxies move much more slowly than predicted",
            "B. Rotation speeds stay roughly the same regardless of distance from the centre",
            "C. Only the central regions of galaxies rotate at all",
            "D. Galaxies contain no invisible matter whatsoever",
        ],
        "B",
        None,
        "Paragraph C: rotation speeds remained roughly constant at all distances from the centre.",
    ),
    q(
        34,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "According to Paragraph D, why do most physicists think dark matter is not made of ordinary matter?",
        [
            "A. Ordinary matter has never been detected anywhere in space",
            "B. Calculations based on the cosmic microwave background show ordinary matter cannot supply enough mass",
            "C. WIMPs have already been directly observed in laboratories",
            "D. Dark energy has been proven not to exist",
        ],
        "B",
        None,
        "Paragraph D: cosmic microwave background calculations show baryonic matter cannot supply enough mass.",
    ),
    q(
        35,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "What made the Bullet Cluster observation significant?",
        [
            "A. It showed that gas and mass were located in exactly the same place",
            "B. It showed a mismatch between the location of visible gas and the location of most of the mass",
            "C. It disproved the existence of gravitational lensing",
            "D. It confirmed that MOND fully explains cluster collisions",
        ],
        "B",
        None,
        "Paragraph E: most of the mass was offset from the visible gas.",
    ),
    q(
        36,
        3,
        "mc",
        "Questions 33–36",
        "Multiple choice",
        "Choose the correct letter, A, B, C, or D.",
        "What is one limitation of MOND mentioned in the passage?",
        [
            "A. It cannot reproduce the rotation curve of any individual galaxy",
            "B. It has struggled to account for cluster-scale observations and cosmic microwave background patterns",
            "C. It requires more dark matter than the standard model does",
            "D. It has been abandoned by every physicist who once supported it",
        ],
        "B",
        None,
        "Paragraph F: MOND has struggled with cluster-scale observations and CMB fluctuations.",
    ),
    q(
        37,
        3,
        "summary",
        "Questions 37–40",
        "Summary completion",
        "Complete the summary. Choose NO MORE THAN ONE WORD from the passage for each answer.",
        "",
        None,
        "XENON",
        ["xenon"],
        "Paragraph G names the XENON series of underground detectors.",
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
        "particle",
        ["particle"],
        "Paragraph G refers to particle accelerators such as the Large Hadron Collider.",
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
        "Cluster",
        ["cluster"],
        "Paragraph B: Zwicky studied the Coma Cluster in 1933.",
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
        "rotation",
        ["rotation"],
        "Paragraph C: Rubin and Ford found flat rotation curves.",
        None,
    ),
]

SUMMARY_INTRO_HTML = """
<p class="art-sum-intro">Researchers search for direct evidence of dark matter using underground experiments such as the <span class="art-sum-slot" data-q="37" tabindex="0">37</span> series, as well as high-energy <span class="art-sum-slot" data-q="38" tabindex="0">38</span> accelerators. Zwicky's study of the Coma <span class="art-sum-slot" data-q="39" tabindex="0">39</span> in 1933 first suggested that visible starlight could not explain a galaxy group's total mass, and later work by Rubin and Ford showed that galaxy <span class="art-sum-slot" data-q="40" tabindex="0">40</span> curves remain flat rather than declining with distance from the centre.</p>
"""


def get_payload() -> dict:
    return build_payload(
        test_number=2,
        title_bar="IELTS Academic Reading · Test 2",
        part1_html=PART1_HTML,
        part2_html=PART2_HTML,
        part3_html=PART3_HTML,
        instructions=INSTRUCTIONS,
        part_meta=PART_META,
        questions=QUESTIONS,
        summary_intro_html=SUMMARY_INTRO_HTML,
        results_meta={
            "part1Title": "Part 1 — Growing & selling food in the city",
            "part2Title": "Part 2 — The Penny Post reform",
            "part3Title": "Part 3 — Dark matter",
        },
    )
