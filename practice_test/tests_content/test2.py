"""Content for IELTS Practice Test 2.

Module-level literals only (no imports, no functions):

    READING    -> list of 3 passage dicts (40 questions total)
    LISTENING  -> {"minutes": 30, "sections": [4 section dicts]} (40 questions)
    WRITING    -> {"task1": {...}, "task2": {...}}

Shapes mirror Test 1's shipped content exactly so the templates and the
scoring code can render and mark this test without changes.
"""

# ===================== READING =====================
# 3 passages × (13 + 13 + 14) = 40 questions total.

READING = [
    {
        "number": 1,
        "title": "The history and science of tea",
        "paragraphs": [
            "After water, tea is the most widely consumed drink on the planet, with billions of cups poured every day from Tokyo to London. According to a popular Chinese legend, the beverage was discovered by accident in 2737 BCE, when leaves from a wild bush drifted into a pot of water that the emperor Shen Nong was boiling. Whether or not the story is true, it captures an important truth: tea began in East Asia, and for many centuries the rest of the world knew nothing of it. All true tea comes from the leaves of a single evergreen species, Camellia sinensis, and the enormous variety of flavours found in the world's teacups is produced not by different plants but by different ways of treating those leaves.",
            "From its homeland in the forests of south-western China, tea drinking spread slowly across Asia. Buddhist monks valued it because the mild stimulation it provided helped them stay awake during long hours of meditation, and they carried the habit, and sometimes the plant itself, to Japan and Korea. By the Tang dynasty, roughly twelve hundred years ago, tea had become so central to Chinese life that a scholar named Lu Yu composed an entire book about it, The Classic of Tea, describing how the leaves should be grown, prepared and served. Tea had become not merely a drink but a subject of art and philosophy.",
            "Europe did not taste tea until the seventeenth century, when Dutch and Portuguese traders began shipping small, expensive quantities home. The British developed a particular passion for it, and demand soon outstripped what could be bought from China. To reduce their dependence on Chinese suppliers, British merchants established vast plantations in their colonies, especially in the Indian regions of Assam and Darjeeling, where the climate proved ideal. This trade reshaped economies and landscapes, but it also had a darker side: the imbalance in trade with China contributed to the conflicts now remembered as the Opium Wars.",
            "Speed mattered in the tea trade. In the middle of the nineteenth century, sleek sailing ships known as clippers raced from Chinese ports to London, because the first cargo of each season's harvest fetched the highest price. The most famous of these races captured the public imagination much as sporting contests do today. Later, the opening of the Suez Canal and the arrival of steamships made the elegant clippers obsolete almost overnight, a reminder of how quickly new technology can transform an established industry.",
            "The differences between green, black and oolong tea have nothing to do with the type of bush and everything to do with processing. After picking, leaves begin to wilt, or wither, losing moisture. If they are then heated quickly, the natural enzymes are deactivated and the leaf stays green. If instead the leaves are rolled and left exposed to air, a process called oxidation turns them progressively darker and changes their taste; fully oxidised leaves become black tea, while oolong sits somewhere in between. It is this single decision, how far to let oxidation proceed, that creates the spectrum of teas we recognise today.",
            "The flavour of tea is governed by chemistry. Tea leaves are rich in compounds called polyphenols, and a particular group of these, the catechins, give green tea its slightly bitter, astringent character. During oxidation the catechins are transformed into larger molecules known as theaflavins and thearubigins, which lend black tea its deeper colour and brisker taste. Tannins, another class of polyphenol, are responsible for the dry, puckering sensation a strong cup can leave in the mouth. Brewing time and water temperature determine how many of these compounds are drawn out, which is why an over-steeped cup tastes harsh.",
            "Tea also contains caffeine, the same stimulant found in coffee, though usually in smaller amounts per cup. What makes tea unusual is that it pairs caffeine with an amino acid called L-theanine, which appears to promote a calm, focused alertness rather than the jittery energy some people associate with coffee. Researchers continue to investigate whether the polyphenols in tea offer measurable health benefits, and while many studies are encouraging, firm conclusions remain elusive.",
            "Today tea is drunk in strikingly different ways around the world. It may be served plain in a porcelain cup, churned with salt and butter in the Himalayas, brewed strong and sweet over ice in the southern United States, or whisked into a bright green foam in the Japanese tea ceremony. Each of these traditions grew from the same humble leaf, yet each reflects the tastes and history of the place that adopted it. A drink discovered, by legend at least, almost five thousand years ago shows no sign of losing its hold on the world.",
        ],
        "questions": [
            {"type": "tfng", "id": "t2r1q1", "text": "All varieties of true tea come from a single species of plant.", "answer": "TRUE"},
            {"type": "tfng", "id": "t2r1q2", "text": "There is solid historical proof that the emperor Shen Nong discovered tea in 2737 BCE.", "answer": "FALSE"},
            {"type": "gap", "id": "t2r1q3", "text": "Buddhist monks drank tea to help them stay awake during long hours of ____.", "answer": "meditation"},
            {"type": "gap", "id": "t2r1q4", "text": "Lu Yu wrote a book called The ____ of Tea.", "answer": "Classic"},
            {"type": "tfng", "id": "t2r1q5", "text": "Europeans were already drinking tea before the seventeenth century.", "answer": "FALSE"},
            {"type": "gap", "id": "t2r1q6", "text": "British merchants set up large plantations in Assam and ____.", "answer": "Darjeeling"},
            {"type": "tfng", "id": "t2r1q7", "text": "The opening of the Suez Canal helped the clipper ships stay competitive.", "answer": "FALSE"},
            {"type": "gap", "id": "t2r1q8", "text": "After picking, tea leaves begin to wilt, or ____, losing moisture.", "answer": "wither"},
            {"type": "mcq", "id": "t2r1q9", "text": "What determines whether a tea becomes green or black?",
             "options": ["The type of bush the leaves come from", "How far oxidation is allowed to proceed", "The country where it is grown", "The colour of the soil"],
             "answer": "How far oxidation is allowed to proceed"},
            {"type": "mcq", "id": "t2r1q10", "text": "Which compounds give green tea its bitter, astringent character?",
             "options": ["Catechins", "Theaflavins", "Thearubigins", "Caffeine molecules"],
             "answer": "Catechins"},
            {"type": "gap", "id": "t2r1q11", "text": "The dry, puckering sensation of a strong cup is caused by ____.", "answer": "tannins"},
            {"type": "tfng", "id": "t2r1q12", "text": "A cup of tea usually contains more caffeine than a cup of coffee.", "answer": "FALSE"},
            {"type": "mcq", "id": "t2r1q13", "text": "What effect is the amino acid L-theanine said to have?",
             "options": ["A sudden burst of jittery energy", "A calm, focused alertness", "A feeling of drowsiness", "No effect at all"],
             "answer": "A calm, focused alertness"},
        ],
    },
    {
        "number": 2,
        "title": "Biomimicry: learning from nature's designs",
        "paragraphs": [
            "Biomimicry is the practice of looking to the natural world for solutions to human problems. Its central idea is simple but powerful: living things have been refining their designs through billions of years of evolution, and the structures and strategies that survive are, by definition, ones that work. Rather than inventing from scratch, engineers who adopt this philosophy study how plants and animals move, build, capture energy and stay clean, and then translate those biological tricks into technology. The word itself combines the Greek roots for 'life' and 'imitation', and supporters argue that it offers a path to designs that are both efficient and sustainable.",
            "Perhaps the most famous example began with an irritation. In 1941 a Swiss engineer named George de Mestral returned from a walk in the mountains to find his clothes and his dog covered in burrs from a burdock plant. Curious, he examined one under a microscope and saw that it was covered in tiny hooks that caught on the loops of fabric and fur. After years of experimentation he reproduced the effect artificially, pairing a strip of stiff hooks with a strip of soft loops. The result, which he called Velcro, is now used everywhere from children's shoes to spacecraft.",
            "Engineers do not only copy small details; sometimes they borrow an animal's entire shape. When Japan's high-speed Shinkansen, or bullet train, emerged from tunnels, the sudden change in air pressure produced a loud boom that disturbed nearby residents. An engineer who was also a keen birdwatcher noticed that the kingfisher dives from air into water, a much denser medium, with barely a splash, thanks to the streamlined shape of its long beak. By redesigning the front of the train to mimic that beak, the team eliminated the noise, and as a bonus the train used less electricity and travelled faster.",
            "Buildings, too, can learn from nature. In hot climates, keeping interiors cool normally demands energy-hungry air conditioning. Yet termites in Africa maintain a remarkably steady temperature inside their towering mounds without any machinery at all, by channelling air through a network of vents that they constantly open and close. Architects designing the Eastgate Centre in Harare, Zimbabwe, applied the same principle, using carefully placed ducts and chimneys to draw cool night air through the building and expel warm air during the day. The result is a large office and shopping complex that uses a fraction of the energy a conventional building of its size would require.",
            "Some of nature's best ideas are found on surfaces. The skin of fast-swimming sharks is covered in microscopic ridged scales that reduce drag and discourage the growth of barnacles and algae; manufacturers have copied this texture to make swimsuits, ship hulls and even hospital surfaces that resist bacteria. The leaf of the lotus plant offers a different lesson. Its surface is covered in tiny bumps that cause water to bead up and roll away, carrying dirt with it, so the leaf stays remarkably clean. Paints and fabrics that imitate this so-called lotus effect now allow surfaces to clean themselves with nothing more than a shower of rain.",
            "For all its promise, biomimicry is not a magic solution. Nature's designs are the product of compromises shaped by an organism's particular environment, and what works for a kingfisher or a termite may not transfer neatly to a machine built from steel and concrete. Reproducing a biological structure can also be expensive and technically demanding. Even so, as engineers face mounting pressure to use less energy and fewer raw materials, the idea of treating the living world as a vast library of tested designs is increasingly attractive. The challenge, its advocates say, is learning to read that library well.",
        ],
        "questions": [
            {"type": "match", "id": "t2r2q1", "text": "Paragraph A",
             "options": ["i  A chance discovery in nature", "ii  Cooling a building the natural way", "iii  Defining a design philosophy", "iv  Borrowing a bird's shape for speed", "v  Obstacles that remain", "vi  Surfaces inspired by living things"],
             "answer": "iii  Defining a design philosophy"},
            {"type": "match", "id": "t2r2q2", "text": "Paragraph B",
             "options": ["i  A chance discovery in nature", "ii  Cooling a building the natural way", "iii  Defining a design philosophy", "iv  Borrowing a bird's shape for speed", "v  Obstacles that remain", "vi  Surfaces inspired by living things"],
             "answer": "i  A chance discovery in nature"},
            {"type": "match", "id": "t2r2q3", "text": "Paragraph C",
             "options": ["i  A chance discovery in nature", "ii  Cooling a building the natural way", "iii  Defining a design philosophy", "iv  Borrowing a bird's shape for speed", "v  Obstacles that remain", "vi  Surfaces inspired by living things"],
             "answer": "iv  Borrowing a bird's shape for speed"},
            {"type": "match", "id": "t2r2q4", "text": "Paragraph D",
             "options": ["i  A chance discovery in nature", "ii  Cooling a building the natural way", "iii  Defining a design philosophy", "iv  Borrowing a bird's shape for speed", "v  Obstacles that remain", "vi  Surfaces inspired by living things"],
             "answer": "ii  Cooling a building the natural way"},
            {"type": "match", "id": "t2r2q5", "text": "Paragraph E",
             "options": ["i  A chance discovery in nature", "ii  Cooling a building the natural way", "iii  Defining a design philosophy", "iv  Borrowing a bird's shape for speed", "v  Obstacles that remain", "vi  Surfaces inspired by living things"],
             "answer": "vi  Surfaces inspired by living things"},
            {"type": "gap", "id": "t2r2q6", "text": "De Mestral examined a burr under a ____ and saw it was covered in tiny hooks.", "answer": "microscope"},
            {"type": "tfng", "id": "t2r2q7", "text": "Velcro is used in spacecraft as well as in everyday products.", "answer": "TRUE"},
            {"type": "gap", "id": "t2r2q8", "text": "The front of the bullet train was redesigned to copy the beak of a ____.", "answer": "kingfisher"},
            {"type": "tfng", "id": "t2r2q9", "text": "The redesigned bullet train consumed more electricity than the original.", "answer": "FALSE"},
            {"type": "tfng", "id": "t2r2q10", "text": "The Eastgate Centre relies on conventional air conditioning to stay cool.", "answer": "FALSE"},
            {"type": "gap", "id": "t2r2q11", "text": "Surfaces that imitate the so-called ____ effect can clean themselves in the rain.", "answer": "lotus"},
            {"type": "mcq", "id": "t2r2q12", "text": "What benefit of shark skin texture is mentioned?",
             "options": ["Brighter colour", "Reduced drag", "Faster wound healing", "Lower production cost"],
             "answer": "Reduced drag"},
            {"type": "mcq", "id": "t2r2q13", "text": "According to the final paragraph, what is one limitation of biomimicry?",
             "options": ["It is now banned in most countries", "Copying natural designs can be costly and technically demanding", "Nature offers no useful designs", "It always increases energy use"],
             "answer": "Copying natural designs can be costly and technically demanding"},
        ],
    },
    {
        "number": 3,
        "title": "The psychology of decision-making",
        "paragraphs": [
            "Every day each of us makes thousands of decisions, from the trivial choice of what to eat for breakfast to weighty judgements about money, health and relationships. For a long time economists assumed that, at least in important matters, people behave as rational agents who weigh up all the available evidence and choose whatever best serves their interests. Over the past half-century, however, psychologists have gathered overwhelming evidence that human reasoning relies heavily on mental shortcuts, and that these shortcuts, while usually helpful, can lead us astray in predictable ways.",
            "Much of this understanding grew from the work of two psychologists, Daniel Kahneman and Amos Tversky. Kahneman later popularised the idea that the mind contains two distinct systems of thought. System 1 is fast, automatic and effortless; it lets us recognise a friend's face or react to a sudden noise without conscious thought. System 2 is slow, deliberate and demanding; it is the system we use to work out a difficult sum or fill in a tax form. Most of the time System 1 runs the show, and System 2 intervenes only when a problem seems to require careful attention.",
            "The shortcuts that System 1 relies on are called heuristics, and they are remarkably efficient. One of the best known is the availability heuristic, which leads us to judge how likely something is by how easily examples come to mind. Because dramatic events such as plane crashes receive intense media coverage, they are easy to recall, and so many people overestimate the danger of flying while underestimating far more common risks such as car accidents. The heuristic saves effort, but it can distort our sense of probability.",
            "Another well-documented effect is anchoring. When people are asked to estimate an unknown quantity, the first number they encounter, even if it is plainly irrelevant, tends to pull their final answer towards it. In one classic experiment, participants who had just seen a high number gave much larger estimates of an unrelated figure than those who had seen a low number. Skilled negotiators exploit this effect by opening with an ambitious price, knowing that it will shape the discussion that follows.",
            "The way a choice is presented, or framed, can be just as influential as its substance. People tend to react very differently to an option described as offering a ninety per cent chance of success than to the same option described as carrying a ten per cent chance of failure, even though the two statements are identical. This sensitivity is linked to a broader pattern known as loss aversion, the finding that the pain of losing something is felt more strongly than the pleasure of gaining the equivalent amount. As a result, people will often take greater risks to avoid a loss than they would to secure a gain.",
            "Our reasoning is shaped by other biases too. Confirmation bias is the tendency to seek out and remember information that supports what we already believe, while ignoring evidence that contradicts it. Closely related is overconfidence: study after study has shown that people are more certain of their judgements than their accuracy warrants. Together these tendencies can lock individuals, and even whole organisations, into mistaken beliefs that fresh evidence struggles to dislodge.",
            "It would be a mistake, however, to conclude that human thinking is simply flawed. The same shortcuts that occasionally mislead us also allow us to act quickly and sensibly in a complex world where we rarely have the time or information to calculate every option. Recognising how these mechanisms work has practical value. Governments and businesses increasingly design choices, sometimes called 'nudges', so that the easy, automatic option is also a beneficial one. Understanding the quirks of our own minds, it turns out, is the first step towards making better decisions.",
        ],
        "questions": [
            {"type": "tfng", "id": "t2r3q1", "text": "Economists traditionally assumed that people make rational choices in important matters.", "answer": "TRUE"},
            {"type": "tfng", "id": "t2r3q2", "text": "Psychologists have found that mental shortcuts never lead people astray.", "answer": "FALSE"},
            {"type": "gap", "id": "t2r3q3", "text": "Two psychologists central to this field were Daniel Kahneman and Amos ____.", "answer": "Tversky"},
            {"type": "mcq", "id": "t2r3q4", "text": "Which best describes System 1 thinking?",
             "options": ["Slow and deliberate", "Fast and automatic", "Used mainly for tax forms", "Rarely active in daily life"],
             "answer": "Fast and automatic"},
            {"type": "gap", "id": "t2r3q5", "text": "We use ____ 2 to work out a difficult sum or fill in a tax form.", "answer": "System"},
            {"type": "gap", "id": "t2r3q6", "text": "The mental shortcuts that System 1 relies on are called ____.", "answer": "heuristics"},
            {"type": "tfng", "id": "t2r3q7", "text": "Many people overestimate the danger of flying.", "answer": "TRUE"},
            {"type": "mcq", "id": "t2r3q8", "text": "How do skilled negotiators make use of anchoring?",
             "options": ["By staying completely silent", "By opening with an ambitious price", "By refusing to mention numbers", "By always offering the lowest price first"],
             "answer": "By opening with an ambitious price"},
            {"type": "gap", "id": "t2r3q9", "text": "Loss aversion means the pain of losing is felt more strongly than the pleasure of an equivalent ____.", "answer": "gain"},
            {"type": "tfng", "id": "t2r3q10", "text": "Confirmation bias involves ignoring evidence that contradicts our existing beliefs.", "answer": "TRUE"},
            {"type": "gap", "id": "t2r3q11", "text": "Studies show people often display ____, being more certain than their accuracy warrants.", "answer": "overconfidence"},
            {"type": "tfng", "id": "t2r3q12", "text": "The writer concludes that human thinking is fundamentally flawed.", "answer": "FALSE"},
            {"type": "mcq", "id": "t2r3q13", "text": "What is a 'nudge'?",
             "options": ["A type of cognitive bias", "A designed choice that makes the beneficial option the easy one", "A mathematical formula for decisions", "A misleading media report"],
             "answer": "A designed choice that makes the beneficial option the easy one"},
            {"type": "tfng", "id": "t2r3q14", "text": "Understanding how mental shortcuts work can help people make better decisions.", "answer": "TRUE"},
        ],
    },
]


# ===================== LISTENING =====================
# 4 sections × 10 questions = 40. ~7 gap + ~3 mcq per section.

LISTENING = {
    "minutes": 30,
    "sections": [
        {
            "number": 1,
            "title": "Section 1 — Enquiring about renting a holiday cottage",
            "instructions": "Questions 1–10. Complete the notes below. Write ONE WORD AND/OR A NUMBER for each answer.",
            "audio": "test2_s1.mp3",
            "questions": [
                {"type": "gap", "id": "t2l1q1", "text": "Name of the property: ____ Cottage", "answer": "Rose"},
                {"type": "gap", "id": "t2l1q2", "text": "Located in the village of ____", "answer": "Ashford"},
                {"type": "gap", "id": "t2l1q3", "text": "Number of bedrooms: ____", "answer": "three"},
                {"type": "mcq", "id": "t2l1q4", "text": "Which facility is included with the cottage?",
                 "options": ["A  a swimming pool", "B  free Wi-Fi", "C  a sauna"],
                 "answer": "B  free Wi-Fi"},
                {"type": "gap", "id": "t2l1q5", "text": "Price per week in the low season: £____", "answer": "450"},
                {"type": "gap", "id": "t2l1q6", "text": "The cottage is available from the ____ of June.", "answer": "12th"},
                {"type": "mcq", "id": "t2l1q7", "text": "What is the policy on pets?",
                 "options": ["A  not allowed at all", "B  allowed with a deposit", "C  allowed free of charge"],
                 "answer": "B  allowed with a deposit"},
                {"type": "gap", "id": "t2l1q8", "text": "Nearest railway station: ____", "answer": "Bridgwater"},
                {"type": "gap", "id": "t2l1q9", "text": "Owner's name: Mrs ____", "answer": "Patterson"},
                {"type": "mcq", "id": "t2l1q10", "text": "To confirm the booking, the customer must",
                 "options": ["A  pay a 20% deposit", "B  send a photograph of ID", "C  call back tomorrow"],
                 "answer": "A  pay a 20% deposit"},
            ],
        },
        {
            "number": 2,
            "title": "Section 2 — Welcome talk at a new science discovery centre",
            "instructions": "Questions 11–20. Complete the notes and choose the correct answer. Write ONE WORD AND/OR A NUMBER for each answer.",
            "audio": "test2_s2.mp3",
            "questions": [
                {"type": "gap", "id": "t2l2q1", "text": "The centre is built on the site of an old ____.", "answer": "factory"},
                {"type": "gap", "id": "t2l2q2", "text": "The main exhibition is on the ____ floor.", "answer": "ground"},
                {"type": "mcq", "id": "t2l2q3", "text": "Where is the planetarium located?",
                 "options": ["A  next to the café", "B  on the top floor", "C  beside the entrance"],
                 "answer": "B  on the top floor"},
                {"type": "gap", "id": "t2l2q4", "text": "Opening time on weekdays: ____ am", "answer": "9.30"},
                {"type": "gap", "id": "t2l2q5", "text": "The centre closes at ____ pm.", "answer": "5"},
                {"type": "mcq", "id": "t2l2q6", "text": "What are visitors NOT allowed to do?",
                 "options": ["A  take photographs", "B  bring food into the galleries", "C  use the lockers"],
                 "answer": "B  bring food into the galleries"},
                {"type": "gap", "id": "t2l2q7", "text": "Free lockers are available near the main ____.", "answer": "entrance"},
                {"type": "gap", "id": "t2l2q8", "text": "The café is on the ____ floor.", "answer": "first"},
                {"type": "mcq", "id": "t2l2q9", "text": "How long does the guided tour last?",
                 "options": ["A  about 30 minutes", "B  about 45 minutes", "C  about 60 minutes"],
                 "answer": "B  about 45 minutes"},
                {"type": "gap", "id": "t2l2q10", "text": "Tickets for the special show cost £____ each.", "answer": "6"},
            ],
        },
        {
            "number": 3,
            "title": "Section 3 — Planning a geography field trip with a tutor",
            "instructions": "Questions 21–30. Complete the notes and choose the correct answer. Write ONE WORD AND/OR A NUMBER for each answer.",
            "audio": "test2_s3.mp3",
            "questions": [
                {"type": "gap", "id": "t2l3q1", "text": "The field trip will take place in the ____ valley.", "answer": "Dee"},
                {"type": "mcq", "id": "t2l3q2", "text": "What is the main aim of the trip?",
                 "options": ["A  to study river erosion", "B  to study coastal plants", "C  to study urban growth"],
                 "answer": "A  to study river erosion"},
                {"type": "gap", "id": "t2l3q3", "text": "Students must bring waterproof ____.", "answer": "boots"},
                {"type": "gap", "id": "t2l3q4", "text": "The trip will last ____ days.", "answer": "three"},
                {"type": "gap", "id": "t2l3q5", "text": "The group will stay at the ____ Centre.", "answer": "Riverside"},
                {"type": "mcq", "id": "t2l3q6", "text": "What must each student prepare after the trip?",
                 "options": ["A  a presentation", "B  a written report", "C  a poster"],
                 "answer": "B  a written report"},
                {"type": "gap", "id": "t2l3q7", "text": "Data will be collected at ____ different sites.", "answer": "five"},
                {"type": "gap", "id": "t2l3q8", "text": "The tutor recommends working in groups of ____.", "answer": "four"},
                {"type": "mcq", "id": "t2l3q9", "text": "What is the biggest safety risk on the trip?",
                 "options": ["A  slippery rocks", "B  heavy traffic", "C  cold weather"],
                 "answer": "A  slippery rocks"},
                {"type": "gap", "id": "t2l3q10", "text": "The deadline for the report is the ____ of March.", "answer": "20th"},
            ],
        },
        {
            "number": 4,
            "title": "Section 4 — Lecture on renewable energy storage",
            "instructions": "Questions 31–40. Complete the notes and choose the correct answer. Write ONE WORD AND/OR A NUMBER for each answer.",
            "audio": "test2_s4.mp3",
            "questions": [
                {"type": "gap", "id": "t2l4q1", "text": "The main challenge for renewable power is that supply is ____.", "answer": "intermittent"},
                {"type": "gap", "id": "t2l4q2", "text": "The most common battery type today uses ____-ion technology.", "answer": "lithium"},
                {"type": "mcq", "id": "t2l4q3", "text": "What is one drawback of lithium-ion batteries?",
                 "options": ["A  limited raw materials", "B  very large size", "C  extremely slow charging"],
                 "answer": "A  limited raw materials"},
                {"type": "gap", "id": "t2l4q4", "text": "____ hydro storage uses water pumped uphill to store energy.", "answer": "Pumped"},
                {"type": "gap", "id": "t2l4q5", "text": "Pumped hydro currently provides most of the world's grid ____.", "answer": "storage"},
                {"type": "mcq", "id": "t2l4q6", "text": "Flow batteries are mainly suited to",
                 "options": ["A  electric cars", "B  large grid-scale storage", "C  mobile phones"],
                 "answer": "B  large grid-scale storage"},
                {"type": "gap", "id": "t2l4q7", "text": "____ batteries store their energy in two tanks of liquid.", "answer": "Flow"},
                {"type": "gap", "id": "t2l4q8", "text": "Surplus electricity can be used to produce ____ gas.", "answer": "hydrogen"},
                {"type": "mcq", "id": "t2l4q9", "text": "What is the main advantage of hydrogen storage?",
                 "options": ["A  it is very cheap today", "B  it can store energy for long periods", "C  it needs no infrastructure"],
                 "answer": "B  it can store energy for long periods"},
                {"type": "gap", "id": "t2l4q10", "text": "The lecturer concludes that a ____ of technologies will be needed, not a single solution.", "answer": "mix"},
            ],
        },
    ],
}


# Use the richer IELTS-style listening set (map labelling, matching, tables,
# form/note/sentence completion and MCQ) while keeping Reading/Writing intact.
from .listening_variety import TEST2_LISTENING as LISTENING


# ===================== WRITING =====================

WRITING = {
    "task1": {
        "kind": "task1",
        "title": "Writing — Task 1",
        "minutes": 20,
        "min_words": 150,
        "instructions": (
            "The line graph below shows the percentage of a country's electricity "
            "that was generated from three different sources — coal, natural gas "
            "and renewables — between 1990 and 2020. "
            "Summarise the information by selecting and reporting the main "
            "features, and make comparisons where relevant."
        ),
        "chart_svg": """
<svg viewBox="0 0 520 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Line graph of electricity generation by source from 1990 to 2020">
  <style>
    .ax { stroke:#94a3b8; stroke-width:1.2; }
    .gr { stroke:#e6eae3; stroke-width:1; }
    .lab{ font: 600 11px 'Segoe UI', Arial, sans-serif; fill:#3a4252; }
    .ttl{ font: 700 12px 'Segoe UI', Arial, sans-serif; fill:#1a1f2b; }
    .coal { stroke:#1e3a5f; stroke-width:2.4; fill:none; }
    .gas  { stroke:#2d6a0a; stroke-width:2.4; fill:none; }
    .ren  { stroke:#c2410c; stroke-width:2.4; fill:none; }
  </style>
  <text x="20" y="18" class="ttl">Electricity generation by source (%)</text>

  <!-- Y gridlines + labels (0..100) -->
  <g>
    <line x1="60" y1="30"  x2="500" y2="30"  class="gr"/>
    <line x1="60" y1="68"  x2="500" y2="68"  class="gr"/>
    <line x1="60" y1="106" x2="500" y2="106" class="gr"/>
    <line x1="60" y1="144" x2="500" y2="144" class="gr"/>
    <line x1="60" y1="182" x2="500" y2="182" class="gr"/>
    <line x1="60" y1="220" x2="500" y2="220" class="ax"/>
    <line x1="60" y1="30"  x2="60"  y2="220" class="ax"/>
    <text x="34" y="34"  class="lab">100</text>
    <text x="40" y="72"  class="lab">80</text>
    <text x="40" y="110" class="lab">60</text>
    <text x="40" y="148" class="lab">40</text>
    <text x="40" y="186" class="lab">20</text>
    <text x="46" y="224" class="lab">0</text>
  </g>

  <!-- X axis labels -->
  <g>
    <text x="72"  y="238" class="lab">1990</text>
    <text x="210" y="238" class="lab">2000</text>
    <text x="350" y="238" class="lab">2010</text>
    <text x="478" y="238" class="lab">2020</text>
  </g>

  <!-- Coal: 50, 45, 35, 25 -->
  <polyline class="coal" points="80,125 220,134.5 360,153.5 500,172.5"/>
  <!-- Gas: 20, 25, 30, 30 -->
  <polyline class="gas" points="80,182 220,172.5 360,163 500,163"/>
  <!-- Renewables: 5, 10, 20, 35 -->
  <polyline class="ren" points="80,210.5 220,201 360,182 500,153.5"/>

  <!-- Legend -->
  <g transform="translate(150,12)">
    <line x1="0"   y1="6" x2="22" y2="6" class="coal"/><text x="26"  y="10" class="lab">Coal</text>
    <line x1="80"  y1="6" x2="102" y2="6" class="gas"/><text x="106" y="10" class="lab">Gas</text>
    <line x1="150" y1="6" x2="172" y2="6" class="ren"/><text x="176" y="10" class="lab">Renewables</text>
  </g>
</svg>
""",
    },
    "task2": {
        "kind": "task2",
        "title": "Writing — Task 2",
        "minutes": 40,
        "min_words": 250,
        "instructions": (
            "Some people believe that working from home benefits employees more "
            "than employers, while others disagree. "
            "Discuss both views and give your own opinion."
        ),
    },
}
