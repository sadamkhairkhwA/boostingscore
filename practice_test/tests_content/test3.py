"""Content for IELTS Practice Test 3.

Module-level literals only — no imports, no functions.
  READING    -> list of 3 passage dicts (40 questions total)
  LISTENING  -> {"minutes": 30, "sections": [4 sections]} (40 questions)
  WRITING    -> {"task1": {...}, "task2": {...}}
"""

# ============================================================================
#  READING  — 3 passages, 40 questions total
# ============================================================================
READING = [
    {
        "number": 1,
        "title": "The Art and Science of Mapmaking",
        "paragraphs": [
            "Few human inventions are as quietly indispensable as the map. Long before "
            "writing systems matured, people scratched the outlines of rivers, coasts "
            "and hunting grounds onto bone, clay and cave walls. The oldest surviving "
            "examples, such as the Babylonian clay tablets of the sixth century BCE, "
            "present the world as a flat disc encircled by a cosmic ocean. These early "
            "maps were less concerned with measurable accuracy than with meaning: they "
            "expressed how a community understood its place within a wider, often "
            "sacred, order. To read them is to glimpse a worldview rather than to plan "
            "a journey across unfamiliar territory.",

            "The intellectual leap towards measurement came with the Greeks. In the "
            "second century CE, the astronomer Ptolemy compiled the Geographia, a "
            "treatise that proposed locating every place by two coordinates, a "
            "forerunner of modern latitude and longitude. Ptolemy understood that the "
            "Earth was a sphere, and he wrestled with the central dilemma of all "
            "cartography: how to depict a curved surface on a flat sheet without "
            "distortion. His solutions were imperfect, and many of his distances were "
            "wildly wrong, yet the principle he established — that a map should rest on "
            "systematic observation rather than legend — would shape the discipline "
            "for the next fourteen centuries.",

            "That principle lay dormant in Europe through much of the medieval period, "
            "when the most celebrated maps, the so-called mappae mundi, returned to "
            "symbolic representation, placing Jerusalem at the centre of the world. It "
            "was the demands of long-distance trade and exploration that revived "
            "precision. Portolan charts, drawn for Mediterranean sailors from the "
            "thirteenth century, criss-crossed the sea with rhumb lines radiating from "
            "compass roses, allowing navigators to plot and hold a steady bearing. "
            "Accuracy was no longer a scholarly luxury; it had become a matter of "
            "survival and of profit for the merchant republics that commissioned the "
            "finest charts.",

            "The single most influential breakthrough arrived in 1569, when the Flemish "
            "cartographer Gerardus Mercator published a projection designed expressly "
            "for sailors. On a Mercator map, any line of constant compass bearing "
            "appears as a straight line, an enormous convenience for navigation. The "
            "price of this convenience is severe distortion of area: land masses near "
            "the poles are stretched grotesquely, so that Greenland appears comparable "
            "in size to Africa, although Africa is in reality some fourteen times "
            "larger. For more than four hundred years this familiar image has shaped, "
            "and arguably skewed, the way millions of people picture the relative "
            "importance of nations.",

            "Beyond navigation, maps became powerful instruments of analysis. In 1854 "
            "the London physician John Snow plotted cases of cholera as dots on a "
            "street map of Soho and saw them cluster tightly around a single water pump "
            "on Broad Street. The visual pattern, invisible in a column of figures, "
            "pointed directly to the source of the outbreak and helped to overturn the "
            "prevailing theory that the disease spread through foul air. Snow's "
            "celebrated diagram is now regarded as a founding example of the thematic "
            "map, in which geography is harnessed not merely to show where things are "
            "but to reveal why they happen.",

            "Every flat map is, in the end, a compromise. A projection can preserve "
            "shape, or area, or distance, or direction, but never all of them at once — "
            "a mathematical certainty proved by Carl Friedrich Gauss. Cartographers "
            "therefore choose a projection to suit a purpose. The Gall–Peters "
            "projection, promoted vigorously in the late twentieth century, sacrifices "
            "shape in order to render area faithfully, presenting equatorial regions at "
            "their true proportion. Critics complained that its continents looked "
            "elongated and unnatural, a reminder that no single map can be objectively "
            "'correct'; each one encodes a set of priorities and, sometimes, a "
            "political argument.",

            "The digital era has transformed mapmaking yet again. The Global "
            "Positioning System, a constellation of satellites operated from orbit, "
            "allows a receiver to fix its position to within a few metres by timing "
            "signals from space. Combined with vast databases and satellite imagery, "
            "GPS has placed a personalised, constantly updated map into billions of "
            "pockets. Yet the old dilemmas have not vanished. The flat screens we "
            "consult still rely on projections, the data they display still reflect "
            "choices about what to include and omit, and a society that navigates by "
            "automated directions risks losing the older, richer skill of reading a "
            "landscape for itself.",
        ],
        "questions": [
            {"type": "tfng", "id": "t3r1q1",
             "text": "The earliest known maps were made mainly to help people plan journeys.",
             "answer": "FALSE"},
            {"type": "tfng", "id": "t3r1q2",
             "text": "Ptolemy was aware that the Earth was spherical.",
             "answer": "TRUE"},
            {"type": "tfng", "id": "t3r1q3",
             "text": "Ptolemy travelled widely in order to gather his own measurements.",
             "answer": "NOT GIVEN"},
            {"type": "tfng", "id": "t3r1q4",
             "text": "On a Mercator map, a course of constant compass bearing is shown as a straight line.",
             "answer": "TRUE"},
            {"type": "tfng", "id": "t3r1q5",
             "text": "The Gall–Peters projection accurately preserves the shapes of the continents.",
             "answer": "FALSE"},
            {"type": "gap", "id": "t3r1q6",
             "text": "Maps such as the Babylonian tablets showed the world as a flat disc surrounded by a cosmic ____.",
             "answer": "ocean"},
            {"type": "gap", "id": "t3r1q7",
             "text": "Ptolemy's treatise, the Geographia, proposed locating each place using two ____.",
             "answer": "coordinates"},
            {"type": "gap", "id": "t3r1q8",
             "text": "Portolan charts featured rhumb lines that spread out from compass ____.",
             "answer": "roses"},
            {"type": "gap", "id": "t3r1q9",
             "text": "On a Mercator map, Greenland looks similar in size to ____, which is in fact far larger.",
             "answer": "Africa"},
            {"type": "mcq", "id": "t3r1q10",
             "text": "According to the passage, medieval mappae mundi typically placed which city at the centre of the world?",
             "options": ["Rome", "Jerusalem", "Babylon", "Athens"],
             "answer": "Jerusalem"},
            {"type": "mcq", "id": "t3r1q11",
             "text": "What did Carl Friedrich Gauss prove about flat maps?",
             "options": [
                 "They must always place north at the top",
                 "No projection can preserve shape, area, distance and direction at the same time",
                 "The Mercator projection is the most accurate of all",
                 "Digital maps remove all distortion",
             ],
             "answer": "No projection can preserve shape, area, distance and direction at the same time"},
            {"type": "mcq", "id": "t3r1q12",
             "text": "John Snow's map of cholera cases is considered an early example of:",
             "options": ["a portolan chart", "a thematic map", "a Mercator projection", "a mappa mundi"],
             "answer": "a thematic map"},
            {"type": "mcq", "id": "t3r1q13",
             "text": "What concern about GPS navigation does the writer raise in the final paragraph?",
             "options": [
                 "It is too expensive for most people",
                 "Its satellites frequently fail",
                 "People may lose the skill of reading a landscape for themselves",
                 "It cannot work indoors",
             ],
             "answer": "People may lose the skill of reading a landscape for themselves"},
        ],
    },

    {
        "number": 2,
        "title": "The Remarkable Migration of Monarch Butterflies",
        "paragraphs": [
            "Each autumn, one of the natural world's most astonishing journeys unfolds "
            "across North America. Monarch butterflies, weighing less than a gram, "
            "abandon the cooling fields of Canada and the northern United States and "
            "stream southward, some travelling more than four thousand kilometres to a "
            "handful of mountain forests in central Mexico. What makes the feat almost "
            "unbelievable is that no individual butterfly has ever made the trip "
            "before, nor will any make it twice. The route is not taught by parents or "
            "rehearsed in advance; it is somehow inherited, written into the insect "
            "before it is even born.",

            "The monarch year is, in effect, a relay run by several short-lived "
            "generations. Butterflies that emerge in spring and summer live only a few "
            "weeks, breeding and dying as the population edges steadily northward. The "
            "generation that hatches in late summer, however, is biologically "
            "different. Triggered by shortening days and falling temperatures, these "
            "individuals enter a state called reproductive diapause, postponing "
            "breeding and conserving their energy. This remarkable 'super generation' "
            "can live for up to eight months, long enough to fly all the way south, "
            "overwinter in Mexico and begin the return journey the following spring.",

            "How the insects find their way has fascinated scientists for decades. "
            "Monarchs rely chiefly on what researchers call a time-compensated sun "
            "compass. Specialised cells in their eyes track the position of the sun, "
            "while an internal clock housed partly in their antennae adjusts for the "
            "sun's movement across the sky, so that the butterflies can maintain a "
            "steady south-westerly heading throughout the day. On overcast days they "
            "appear to fall back on the Earth's magnetic field, using a "
            "light-sensitive compass to keep their bearing when the sun is hidden from "
            "view.",

            "The Mexican forests where the monarchs gather are no ordinary refuge. High "
            "in the oyamel fir forests, the butterflies cluster in such numbers that "
            "branches bend beneath their weight, and a single hectare may shelter tens "
            "of millions of insects. The dense canopy acts as both blanket and "
            "umbrella, trapping just enough warmth to prevent the butterflies from "
            "freezing while shielding them from soaking rain. The microclimate is so "
            "finely balanced that even modest thinning of the forest can expose the "
            "clustered colonies to lethal cold, which is why the integrity of these "
            "groves matters so much.",

            "These extraordinary migrations are now in serious jeopardy. The clearing "
            "of the Mexican forests for timber, though officially restricted, continues "
            "to fragment the overwintering grounds. Far to the north, the spread of "
            "intensive agriculture has stripped the landscape of milkweed, the only "
            "plant on which monarch caterpillars feed, while pesticides and a changing "
            "climate compound the pressure at every stage of the journey. The eastern "
            "monarch population, by some estimates, has fallen by more than eighty per "
            "cent over recent decades, and the far smaller western population has "
            "declined even more steeply.",

            "Efforts to reverse the decline now span the entire continent. "
            "Conservationists encourage gardeners to plant native milkweed and nectar "
            "flowers, creating corridors of habitat along the migration route, and "
            "citizen-science programmes recruit thousands of volunteers to tag "
            "butterflies and record sightings. Such tagging has confirmed individual "
            "journeys of extraordinary length and helped to map the precise timing of "
            "the migration. Whether these measures can stabilise the population remains "
            "uncertain, but the monarch has become a powerful symbol of how a single "
            "fragile species can connect distant landscapes and the people who share "
            "them.",
        ],
        "questions": [
            {"type": "match", "id": "t3r2q14",
             "text": "Paragraph A",
             "options": [
                 "i  A journey driven by inheritance, not learning",
                 "ii  The unique long-lived autumn generation",
                 "iii  How monarchs steer by sun and magnetism",
                 "iv  A delicately balanced winter shelter",
                 "v  Mounting dangers to the migration",
                 "vi  Continent-wide attempts to help",
                 "vii  The history of butterfly classification",
                 "viii  The economic value of butterfly tourism",
             ],
             "answer": "i  A journey driven by inheritance, not learning"},
            {"type": "match", "id": "t3r2q15",
             "text": "Paragraph B",
             "options": [
                 "i  A journey driven by inheritance, not learning",
                 "ii  The unique long-lived autumn generation",
                 "iii  How monarchs steer by sun and magnetism",
                 "iv  A delicately balanced winter shelter",
                 "v  Mounting dangers to the migration",
                 "vi  Continent-wide attempts to help",
                 "vii  The history of butterfly classification",
                 "viii  The economic value of butterfly tourism",
             ],
             "answer": "ii  The unique long-lived autumn generation"},
            {"type": "match", "id": "t3r2q16",
             "text": "Paragraph C",
             "options": [
                 "i  A journey driven by inheritance, not learning",
                 "ii  The unique long-lived autumn generation",
                 "iii  How monarchs steer by sun and magnetism",
                 "iv  A delicately balanced winter shelter",
                 "v  Mounting dangers to the migration",
                 "vi  Continent-wide attempts to help",
                 "vii  The history of butterfly classification",
                 "viii  The economic value of butterfly tourism",
             ],
             "answer": "iii  How monarchs steer by sun and magnetism"},
            {"type": "match", "id": "t3r2q17",
             "text": "Paragraph D",
             "options": [
                 "i  A journey driven by inheritance, not learning",
                 "ii  The unique long-lived autumn generation",
                 "iii  How monarchs steer by sun and magnetism",
                 "iv  A delicately balanced winter shelter",
                 "v  Mounting dangers to the migration",
                 "vi  Continent-wide attempts to help",
                 "vii  The history of butterfly classification",
                 "viii  The economic value of butterfly tourism",
             ],
             "answer": "iv  A delicately balanced winter shelter"},
            {"type": "match", "id": "t3r2q18",
             "text": "Paragraph E",
             "options": [
                 "i  A journey driven by inheritance, not learning",
                 "ii  The unique long-lived autumn generation",
                 "iii  How monarchs steer by sun and magnetism",
                 "iv  A delicately balanced winter shelter",
                 "v  Mounting dangers to the migration",
                 "vi  Continent-wide attempts to help",
                 "vii  The history of butterfly classification",
                 "viii  The economic value of butterfly tourism",
             ],
             "answer": "v  Mounting dangers to the migration"},
            {"type": "match", "id": "t3r2q19",
             "text": "Paragraph F",
             "options": [
                 "i  A journey driven by inheritance, not learning",
                 "ii  The unique long-lived autumn generation",
                 "iii  How monarchs steer by sun and magnetism",
                 "iv  A delicately balanced winter shelter",
                 "v  Mounting dangers to the migration",
                 "vi  Continent-wide attempts to help",
                 "vii  The history of butterfly classification",
                 "viii  The economic value of butterfly tourism",
             ],
             "answer": "vi  Continent-wide attempts to help"},
            {"type": "gap", "id": "t3r2q20",
             "text": "The special late-summer generation enters a state known as reproductive ____.",
             "answer": "diapause"},
            {"type": "gap", "id": "t3r2q21",
             "text": "Part of the monarch's internal clock is housed in its ____.",
             "answer": "antennae"},
            {"type": "gap", "id": "t3r2q22",
             "text": "In Mexico the butterflies spend the winter in forests of ____ fir.",
             "answer": "oyamel"},
            {"type": "gap", "id": "t3r2q23",
             "text": "Monarch caterpillars feed only on ____.",
             "answer": "milkweed"},
            {"type": "tfng", "id": "t3r2q24",
             "text": "An individual monarch may complete the round trip to Mexico and back more than once.",
             "answer": "FALSE"},
            {"type": "tfng", "id": "t3r2q25",
             "text": "On cloudy days monarchs may navigate using the Earth's magnetic field.",
             "answer": "TRUE"},
            {"type": "tfng", "id": "t3r2q26",
             "text": "Scientists have identified the exact gene responsible for the monarch's migratory behaviour.",
             "answer": "NOT GIVEN"},
        ],
    },

    {
        "number": 3,
        "title": "Measuring Happiness: The Economics of Well-being",
        "paragraphs": [
            "For most of the twentieth century, the success of a nation was measured "
            "almost entirely by a single figure: Gross Domestic Product, the total "
            "value of the goods and services it produced. GDP is relatively easy to "
            "calculate, internationally comparable and closely tied to employment, so "
            "governments came to treat its growth as the overriding goal of economic "
            "policy. Yet GDP was never designed to measure welfare. Its principal "
            "architect, the economist Simon Kuznets, warned as early as the 1930s that "
            "the prosperity of a nation could not safely be inferred from such an "
            "index.",

            "The limitations are easy to illustrate. GDP rises when a forest is felled "
            "and sold as timber, but records no loss when the forest, and all the "
            "services it once provided, disappears. It counts the money spent cleaning "
            "up an oil spill as a gain, and it ignores unpaid work in the home, much of "
            "it done by women, even though such labour is essential to any functioning "
            "economy. A country can therefore post impressive growth figures while its "
            "citizens grow more anxious, its inequalities widen and its environment "
            "quietly degrades.",

            "Dissatisfaction with GDP has driven a long search for better measures of "
            "how well a society is actually doing. One influential alternative is the "
            "Human Development Index, introduced by the United Nations in 1990, which "
            "combines income with life expectancy and education to give a fuller "
            "picture of human progress. Others have gone further, attempting to measure "
            "subjective well-being directly by asking large samples of people how "
            "satisfied they are with their lives, typically on a scale from zero to "
            "ten. The annual World Happiness Report, which ranks countries on the basis "
            "of such surveys, has brought this approach to a wide global audience.",

            "What, then, actually raises life satisfaction? Research consistently finds "
            "that income matters, but in a particular way. Rising from poverty to a "
            "comfortable standard of living brings a large gain in well-being; beyond "
            "that point, however, additional income yields steadily diminishing "
            "returns. This pattern, sometimes called the Easterlin paradox after the "
            "economist who first described it, helps to explain why the citizens of "
            "wealthy nations are often no happier than they were several decades "
            "earlier, despite substantial and continued economic growth.",

            "If money is not the whole story, what else counts? The data point "
            "repeatedly to the quality of human relationships. People with strong "
            "social connections, supportive families and a sense of belonging report "
            "markedly higher satisfaction, and loneliness has emerged as a powerful "
            "predictor of poor well-being. Health, especially mental health, weighs "
            "heavily too, as does a sense of autonomy — the feeling that one has some "
            "genuine control over the course of one's own life. Trust, both in other "
            "people and in public institutions, appears to lift the well-being of "
            "entire societies at once.",

            "These findings have begun to influence the way governments work. Several "
            "countries now collect official statistics on well-being alongside their "
            "economic accounts, and a small group, including New Zealand and Bhutan, "
            "has experimented with framing national budgets around measures of welfare "
            "rather than growth alone. The tiny Himalayan kingdom of Bhutan famously "
            "adopted 'Gross National Happiness' as a guiding principle decades ago, "
            "treating cultural preservation and environmental protection as explicit "
            "policy goals rather than afterthoughts.",

            "Critics caution that happiness data must be handled with care. Answers to "
            "survey questions can be swayed by passing mood, by the weather on the day, "
            "or by the precise way a question is phrased, and comparing satisfaction "
            "across very different cultures is fraught with difficulty. Few economists "
            "now argue that GDP should be discarded; it remains a vital gauge of "
            "economic activity. The emerging consensus is more modest but significant: "
            "that a single number can never capture the full richness of a good life, "
            "and that what a society chooses to measure tends to shape what it chooses "
            "to pursue.",
        ],
        "questions": [
            {"type": "tfng", "id": "t3r3q27",
             "text": "Simon Kuznets believed that GDP was a reliable measure of national welfare.",
             "answer": "FALSE"},
            {"type": "tfng", "id": "t3r3q28",
             "text": "Money spent dealing with an oil spill adds to a country's GDP.",
             "answer": "TRUE"},
            {"type": "tfng", "id": "t3r3q29",
             "text": "The Human Development Index was created before 1980.",
             "answer": "FALSE"},
            {"type": "tfng", "id": "t3r3q30",
             "text": "The World Happiness Report bases its rankings on people's own assessments of their lives.",
             "answer": "TRUE"},
            {"type": "gap", "id": "t3r3q31",
             "text": "The Human Development Index combines income with education and life ____.",
             "answer": "expectancy"},
            {"type": "gap", "id": "t3r3q32",
             "text": "Surveys of subjective well-being usually ask people to rate their lives on a scale from zero to ____.",
             "answer": "ten"},
            {"type": "gap", "id": "t3r3q33",
             "text": "The tendency for extra income to bring less and less happiness is known as the Easterlin ____.",
             "answer": "paradox"},
            {"type": "gap", "id": "t3r3q34",
             "text": "A feeling of having control over one's life is described in the passage as a sense of ____.",
             "answer": "autonomy"},
            {"type": "gap", "id": "t3r3q35",
             "text": "Bhutan adopted the principle of Gross National ____ several decades ago.",
             "answer": "Happiness"},
            {"type": "mcq", "id": "t3r3q36",
             "text": "According to the passage, one problem with GDP is that it:",
             "options": [
                 "is difficult to calculate",
                 "cannot be compared between countries",
                 "registers the destruction of a forest as economic gain",
                 "excludes the value of manufactured goods",
             ],
             "answer": "registers the destruction of a forest as economic gain"},
            {"type": "mcq", "id": "t3r3q37",
             "text": "The Easterlin paradox helps to explain why:",
             "options": [
                 "poor countries never grow richer",
                 "people in rich countries are often no happier than in the past",
                 "income has no effect on happiness at all",
                 "life expectancy is falling in wealthy nations",
             ],
             "answer": "people in rich countries are often no happier than in the past"},
            {"type": "mcq", "id": "t3r3q38",
             "text": "Which factor does the passage identify as a strong predictor of poor well-being?",
             "options": ["high taxation", "loneliness", "urban living", "long working hours"],
             "answer": "loneliness"},
            {"type": "mcq", "id": "t3r3q39",
             "text": "Which two countries are mentioned as framing budgets around welfare rather than growth alone?",
             "options": [
                 "Bhutan and New Zealand",
                 "Norway and Sweden",
                 "Canada and Japan",
                 "France and Germany",
             ],
             "answer": "Bhutan and New Zealand"},
            {"type": "mcq", "id": "t3r3q40",
             "text": "What is the 'emerging consensus' described in the final paragraph?",
             "options": [
                 "GDP should be abolished immediately",
                 "Happiness surveys are completely unreliable",
                 "No single number can capture the full richness of a good life",
                 "Economic growth should always be the top priority",
             ],
             "answer": "No single number can capture the full richness of a good life"},
        ],
    },
]


# ============================================================================
#  LISTENING  — 4 sections, 10 questions each, 40 total
# ============================================================================
LISTENING = {
    "minutes": 30,
    "sections": [
        {
            "number": 1,
            "title": "Section 1 — Joining the community library",
            "instructions": "Questions 1–10. Complete the notes and answer the "
                            "multiple-choice questions below. Write NO MORE THAN "
                            "THREE WORDS AND/OR A NUMBER for each gap answer.",
            "audio": "test3_s1.mp3",
            "questions": [
                {"type": "gap", "id": "t3l1q1",
                 "text": "Caller's full name: Megan ____", "answer": "Fletcher"},
                {"type": "gap", "id": "t3l1q2",
                 "text": "Home address: 14 ____ Road", "answer": "Maple"},
                {"type": "mcq", "id": "t3l1q3",
                 "text": "Which type of membership does Megan choose?",
                 "options": ["Standard adult card", "Student card", "Family card"],
                 "answer": "Family card"},
                {"type": "gap", "id": "t3l1q4",
                 "text": "Annual fee for the chosen card: £ ____", "answer": "12"},
                {"type": "gap", "id": "t3l1q5",
                 "text": "To register she must bring photo ID and a recent ____ bill.",
                 "answer": "electricity"},
                {"type": "mcq", "id": "t3l1q6",
                 "text": "How many items can be borrowed at one time?",
                 "options": ["Up to 8", "Up to 12", "Up to 20"],
                 "answer": "Up to 12"},
                {"type": "gap", "id": "t3l1q7",
                 "text": "Standard loan period: ____ weeks.", "answer": "three"},
                {"type": "gap", "id": "t3l1q8",
                 "text": "On weekdays the library stays open until ____ pm.",
                 "answer": "8"},
                {"type": "mcq", "id": "t3l1q9",
                 "text": "On which day is the library closed?",
                 "options": ["Sunday", "Monday", "Tuesday"],
                 "answer": "Sunday"},
                {"type": "gap", "id": "t3l1q10",
                 "text": "Children's story time takes place every ____ morning.",
                 "answer": "Saturday"},
            ],
        },
        {
            "number": 2,
            "title": "Section 2 — Radio announcement: the Riverside Food Festival",
            "instructions": "Questions 11–20. Complete the notes and answer the "
                            "multiple-choice questions below. Write NO MORE THAN "
                            "THREE WORDS AND/OR A NUMBER for each gap answer.",
            "audio": "test3_s2.mp3",
            "questions": [
                {"type": "gap", "id": "t3l2q1",
                 "text": "The event is called the ____ Food Festival.",
                 "answer": "Riverside"},
                {"type": "gap", "id": "t3l2q2",
                 "text": "It takes place on the ____ weekend of June.",
                 "answer": "second"},
                {"type": "mcq", "id": "t3l2q3",
                 "text": "Where is the festival held?",
                 "options": ["In the town hall", "In Victoria Park", "On the high street"],
                 "answer": "In Victoria Park"},
                {"type": "gap", "id": "t3l2q4",
                 "text": "There will be more than ____ food stalls.", "answer": "60"},
                {"type": "gap", "id": "t3l2q5",
                 "text": "The main stage features live ____ throughout the day.",
                 "answer": "music"},
                {"type": "gap", "id": "t3l2q6",
                 "text": "A standard adult ticket costs £ ____.", "answer": "8"},
                {"type": "mcq", "id": "t3l2q7",
                 "text": "Children below which age may enter free of charge?",
                 "options": ["under 5", "under 10", "under 12"],
                 "answer": "under 12"},
                {"type": "gap", "id": "t3l2q8",
                 "text": "Free parking is available at the ____ car park.",
                 "answer": "station"},
                {"type": "gap", "id": "t3l2q9",
                 "text": "Visitors are advised to arrive before ____ am to avoid the queues.",
                 "answer": "11"},
                {"type": "mcq", "id": "t3l2q10",
                 "text": "What does the announcer suggest visitors bring?",
                 "options": ["A reusable cup", "An umbrella", "A picnic blanket"],
                 "answer": "A reusable cup"},
            ],
        },
        {
            "number": 3,
            "title": "Section 3 — Tutorial: planning a dissertation",
            "instructions": "Questions 21–30. Complete the notes and answer the "
                            "multiple-choice questions below. Write NO MORE THAN "
                            "THREE WORDS AND/OR A NUMBER for each gap answer.",
            "audio": "test3_s3.mp3",
            "questions": [
                {"type": "gap", "id": "t3l3q1",
                 "text": "The dissertation examines the impact of ____ on local rivers.",
                 "answer": "microplastics"},
                {"type": "mcq", "id": "t3l3q2",
                 "text": "The tutor advises the student first to narrow down the:",
                 "options": ["research question", "budget", "word count"],
                 "answer": "research question"},
                {"type": "gap", "id": "t3l3q3",
                 "text": "The literature review should be finished by the end of ____.",
                 "answer": "October"},
                {"type": "gap", "id": "t3l3q4",
                 "text": "The student will collect water samples from ____ different sites.",
                 "answer": "five"},
                {"type": "gap", "id": "t3l3q5",
                 "text": "Sampling will continue over a period of ____ months.",
                 "answer": "three"},
                {"type": "mcq", "id": "t3l3q6",
                 "text": "What method will the student mainly use to analyse the data?",
                 "options": ["Interviews", "Laboratory testing", "Questionnaires"],
                 "answer": "Laboratory testing"},
                {"type": "gap", "id": "t3l3q7",
                 "text": "The first full draft is due in ____.", "answer": "February"},
                {"type": "gap", "id": "t3l3q8",
                 "text": "They agree to meet once a ____ to review progress.",
                 "answer": "fortnight"},
                {"type": "mcq", "id": "t3l3q9",
                 "text": "What is the tutor most concerned about?",
                 "options": ["The student's time management", "The cost of equipment", "Finding participants"],
                 "answer": "The student's time management"},
                {"type": "gap", "id": "t3l3q10",
                 "text": "The complete dissertation must be submitted by the ____ of May.",
                 "answer": "tenth"},
            ],
        },
        {
            "number": 4,
            "title": "Section 4 — Lecture: life in the deep sea",
            "instructions": "Questions 31–40. Complete the notes and answer the "
                            "multiple-choice questions below. Write NO MORE THAN "
                            "THREE WORDS AND/OR A NUMBER for each gap answer.",
            "audio": "test3_s4.mp3",
            "questions": [
                {"type": "gap", "id": "t3l4q1",
                 "text": "The sunlit surface layer of the ocean is called the ____ zone.",
                 "answer": "epipelagic"},
                {"type": "gap", "id": "t3l4q2",
                 "text": "The twilight zone is also known as the ____ zone.",
                 "answer": "mesopelagic"},
                {"type": "mcq", "id": "t3l4q3",
                 "text": "What is the main source of food for many deep-sea creatures?",
                 "options": ["Photosynthesis", "Marine snow", "Hydrothermal plants"],
                 "answer": "Marine snow"},
                {"type": "gap", "id": "t3l4q4",
                 "text": "Many deep-sea animals make their own light through a process called ____.",
                 "answer": "bioluminescence"},
                {"type": "gap", "id": "t3l4q5",
                 "text": "Pressure rises by about one atmosphere for every ____ metres of depth.",
                 "answer": "10"},
                {"type": "gap", "id": "t3l4q6",
                 "text": "The deepest part of the ocean is the ____ Trench.",
                 "answer": "Mariana"},
                {"type": "mcq", "id": "t3l4q7",
                 "text": "Hydrothermal vent communities depend on bacteria that use:",
                 "options": ["sunlight", "chemicals", "oxygen"],
                 "answer": "chemicals"},
                {"type": "gap", "id": "t3l4q8",
                 "text": "Scientists explore the deep sea using remotely operated ____.",
                 "answer": "vehicles"},
                {"type": "gap", "id": "t3l4q9",
                 "text": "The Mariana Trench reaches a depth of almost ____ thousand metres.",
                 "answer": "eleven"},
                {"type": "mcq", "id": "t3l4q10",
                 "text": "According to the lecturer, what is the biggest threat now reaching the deep sea?",
                 "options": ["Plastic pollution", "Overfishing", "Noise"],
                 "answer": "Plastic pollution"},
            ],
        },
    ],
}


# ============================================================================
#  WRITING  — Task 1 (table) + Task 2 (essay)
# ============================================================================
WRITING = {
    "task1": {
        "kind": "task1",
        "title": "Writing — Task 1",
        "minutes": 20,
        "min_words": 150,
        "instructions": (
            "The table below shows the percentage of the population in three age "
            "groups (0–14, 15–64 and 65 and over) in four countries — Japan, Brazil, "
            "Nigeria and the UK — in 2020. "
            "Summarise the information by selecting and reporting the main features, "
            "and make comparisons where relevant."
        ),
        "chart_svg": (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 260" '
            'font-family="Arial, sans-serif">'
            '<rect x="0" y="0" width="520" height="260" fill="#ffffff"/>'
            '<text x="260" y="22" text-anchor="middle" font-size="15" '
            'font-weight="bold" fill="#1a2433">Population by age group (%), 2020</text>'
            # header row background
            '<rect x="10" y="34" width="140" height="32" fill="#2c3e50"/>'
            '<rect x="150" y="34" width="90" height="32" fill="#2c3e50"/>'
            '<rect x="240" y="34" width="90" height="32" fill="#2c3e50"/>'
            '<rect x="330" y="34" width="90" height="32" fill="#2c3e50"/>'
            '<rect x="420" y="34" width="90" height="32" fill="#2c3e50"/>'
            '<text x="80" y="55" text-anchor="middle" font-size="13" fill="#ffffff">Age group</text>'
            '<text x="195" y="55" text-anchor="middle" font-size="13" fill="#ffffff">Japan</text>'
            '<text x="285" y="55" text-anchor="middle" font-size="13" fill="#ffffff">Brazil</text>'
            '<text x="375" y="55" text-anchor="middle" font-size="13" fill="#ffffff">Nigeria</text>'
            '<text x="465" y="55" text-anchor="middle" font-size="13" fill="#ffffff">UK</text>'
            # row 1 (0-14)
            '<rect x="10" y="66" width="140" height="40" fill="#eef2f7"/>'
            '<rect x="150" y="66" width="90" height="40" fill="#f7fafc"/>'
            '<rect x="240" y="66" width="90" height="40" fill="#f7fafc"/>'
            '<rect x="330" y="66" width="90" height="40" fill="#f7fafc"/>'
            '<rect x="420" y="66" width="90" height="40" fill="#f7fafc"/>'
            '<text x="80" y="91" text-anchor="middle" font-size="13" fill="#1a2433">0–14</text>'
            '<text x="195" y="91" text-anchor="middle" font-size="13" fill="#1a2433">12</text>'
            '<text x="285" y="91" text-anchor="middle" font-size="13" fill="#1a2433">21</text>'
            '<text x="375" y="91" text-anchor="middle" font-size="13" fill="#1a2433">43</text>'
            '<text x="465" y="91" text-anchor="middle" font-size="13" fill="#1a2433">18</text>'
            # row 2 (15-64)
            '<rect x="10" y="106" width="140" height="40" fill="#eef2f7"/>'
            '<rect x="150" y="106" width="90" height="40" fill="#ffffff"/>'
            '<rect x="240" y="106" width="90" height="40" fill="#ffffff"/>'
            '<rect x="330" y="106" width="90" height="40" fill="#ffffff"/>'
            '<rect x="420" y="106" width="90" height="40" fill="#ffffff"/>'
            '<text x="80" y="131" text-anchor="middle" font-size="13" fill="#1a2433">15–64</text>'
            '<text x="195" y="131" text-anchor="middle" font-size="13" fill="#1a2433">59</text>'
            '<text x="285" y="131" text-anchor="middle" font-size="13" fill="#1a2433">70</text>'
            '<text x="375" y="131" text-anchor="middle" font-size="13" fill="#1a2433">54</text>'
            '<text x="465" y="131" text-anchor="middle" font-size="13" fill="#1a2433">64</text>'
            # row 3 (65+)
            '<rect x="10" y="146" width="140" height="40" fill="#eef2f7"/>'
            '<rect x="150" y="146" width="90" height="40" fill="#f7fafc"/>'
            '<rect x="240" y="146" width="90" height="40" fill="#f7fafc"/>'
            '<rect x="330" y="146" width="90" height="40" fill="#f7fafc"/>'
            '<rect x="420" y="146" width="90" height="40" fill="#f7fafc"/>'
            '<text x="80" y="171" text-anchor="middle" font-size="13" fill="#1a2433">65 and over</text>'
            '<text x="195" y="171" text-anchor="middle" font-size="13" fill="#1a2433">29</text>'
            '<text x="285" y="171" text-anchor="middle" font-size="13" fill="#1a2433">9</text>'
            '<text x="375" y="171" text-anchor="middle" font-size="13" fill="#1a2433">3</text>'
            '<text x="465" y="171" text-anchor="middle" font-size="13" fill="#1a2433">18</text>'
            # grid lines
            '<g stroke="#c5cfda" stroke-width="1">'
            '<line x1="10" y1="34" x2="510" y2="34"/>'
            '<line x1="10" y1="66" x2="510" y2="66"/>'
            '<line x1="10" y1="106" x2="510" y2="106"/>'
            '<line x1="10" y1="146" x2="510" y2="146"/>'
            '<line x1="10" y1="186" x2="510" y2="186"/>'
            '<line x1="10" y1="34" x2="10" y2="186"/>'
            '<line x1="150" y1="34" x2="150" y2="186"/>'
            '<line x1="240" y1="34" x2="240" y2="186"/>'
            '<line x1="330" y1="34" x2="330" y2="186"/>'
            '<line x1="420" y1="34" x2="420" y2="186"/>'
            '<line x1="510" y1="34" x2="510" y2="186"/>'
            '</g>'
            '<text x="10" y="206" font-size="11" fill="#5a6675">All figures are '
            'percentages of the total national population and are rounded to the '
            'nearest whole number.</text>'
            '</svg>'
        ),
    },
    "task2": {
        "kind": "task2",
        "title": "Writing — Task 2",
        "minutes": 40,
        "min_words": 250,
        "instructions": (
            "Some people think that university education should be free for all "
            "students, while others believe that students should pay their own "
            "tuition fees. Discuss both these views and give your own opinion. "
            "Give reasons for your answer and include any relevant examples from "
            "your own knowledge or experience."
        ),
    },
}
