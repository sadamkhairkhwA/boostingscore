"""IELTS-style Listening content for Practice Tests 2-5.

Each TEST*_LISTENING dict uses the same structure as Test 1's listening data:

    {
        "minutes": 30,
        "sections": [
            {
                "number": 1,
                "title": "...",
                "instructions": "...",
                "audio": "testN_sX.mp3",
                "questions": [...]
            },
            ...
        ],
    }

Questions use the listening renderer's supported IELTS-style types:
form/note/sentence/table text completion, map labelling, matching and MCQ.
"""

DISCOVERY_CENTRE_MAP_SVG = """
<svg viewBox="0 0 520 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Science discovery centre map">
  <rect x="14" y="14" width="492" height="272" rx="18" fill="#f7fbff" stroke="#93a4b8" stroke-width="2"/>
  <path d="M70 240 H450" stroke="#9aa8b5" stroke-width="20" stroke-linecap="round"/>
  <path d="M260 240 V70" stroke="#9aa8b5" stroke-width="18" stroke-linecap="round"/>
  <rect x="48" y="188" width="112" height="54" rx="8" fill="#fff" stroke="#345c7a"/><text x="104" y="218" text-anchor="middle" font-size="13">Entrance</text>
  <rect x="190" y="36" width="140" height="56" rx="8" fill="#eaf6ff" stroke="#345c7a"/><text x="260" y="68" text-anchor="middle" font-size="13">Space Gallery</text>
  <rect x="352" y="86" width="118" height="58" rx="8" fill="#fff5e8" stroke="#9b6630"/><text x="411" y="119" text-anchor="middle" font-size="13">Cafe</text>
  <rect x="52" y="82" width="118" height="58" rx="8" fill="#eef8ec" stroke="#3d7a3b"/><text x="111" y="115" text-anchor="middle" font-size="13">Theatre</text>
  <circle cx="260" cy="172" r="38" fill="#f2efff" stroke="#5f4fa3"/><text x="260" y="176" text-anchor="middle" font-size="13">Lab</text>
  <rect x="350" y="192" width="112" height="52" rx="8" fill="#fff" stroke="#345c7a"/><text x="406" y="222" text-anchor="middle" font-size="13">Gift shop</text>
  <text x="55" y="40" font-size="18" font-weight="700">A</text><text x="250" y="32" font-size="18" font-weight="700">B</text>
  <text x="480" y="104" font-size="18" font-weight="700">C</text><text x="128" y="76" font-size="18" font-weight="700">D</text>
  <text x="308" y="166" font-size="18" font-weight="700">E</text><text x="466" y="238" font-size="18" font-weight="700">F</text>
  <text x="176" y="248" font-size="18" font-weight="700">G</text><text x="260" y="270" font-size="18" font-weight="700">H</text>
</svg>
"""

FESTIVAL_MAP_SVG = """
<svg viewBox="0 0 520 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Festival site map">
  <rect x="16" y="16" width="488" height="268" rx="18" fill="#fffdf5" stroke="#bca56c" stroke-width="2"/>
  <path d="M55 238 C170 180 285 250 445 175" fill="none" stroke="#78a6cf" stroke-width="18" stroke-linecap="round"/>
  <rect x="50" y="48" width="105" height="58" rx="8" fill="#fff" stroke="#6f6f6f"/><text x="102" y="82" text-anchor="middle" font-size="13">Main gate</text>
  <rect x="190" y="44" width="120" height="58" rx="8" fill="#fff1e6" stroke="#b36b30"/><text x="250" y="78" text-anchor="middle" font-size="13">Chef stage</text>
  <rect x="360" y="54" width="100" height="58" rx="8" fill="#eef8ec" stroke="#4a8847"/><text x="410" y="88" text-anchor="middle" font-size="13">Picnic area</text>
  <rect x="70" y="150" width="120" height="56" rx="8" fill="#f4f1ff" stroke="#6b5fb5"/><text x="130" y="183" text-anchor="middle" font-size="13">Kids tent</text>
  <rect x="265" y="148" width="112" height="56" rx="8" fill="#fff" stroke="#6f6f6f"/><text x="321" y="181" text-anchor="middle" font-size="13">Info desk</text>
  <text x="36" y="46" font-size="18" font-weight="700">A</text><text x="238" y="35" font-size="18" font-weight="700">B</text>
  <text x="467" y="54" font-size="18" font-weight="700">C</text><text x="48" y="164" font-size="18" font-weight="700">D</text>
  <text x="385" y="164" font-size="18" font-weight="700">E</text><text x="444" y="205" font-size="18" font-weight="700">F</text>
  <text x="210" y="232" font-size="18" font-weight="700">G</text><text x="94" y="256" font-size="18" font-weight="700">H</text>
</svg>
"""

NATURE_RESERVE_MAP_SVG = """
<svg viewBox="0 0 520 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Nature reserve route map">
  <rect x="15" y="15" width="490" height="270" rx="18" fill="#f6fbf2" stroke="#7fa56b" stroke-width="2"/>
  <path d="M65 235 C120 135 230 245 310 120 S430 75 455 175" fill="none" stroke="#8b6d42" stroke-width="12" stroke-dasharray="12 9" stroke-linecap="round"/>
  <ellipse cx="185" cy="82" rx="82" ry="38" fill="#b9d9ff" stroke="#4d7aa3"/><text x="185" y="86" text-anchor="middle" font-size="13">Lake</text>
  <rect x="50" y="205" width="102" height="50" rx="8" fill="#fff" stroke="#56724b"/><text x="101" y="235" text-anchor="middle" font-size="13">Car park</text>
  <rect x="315" y="190" width="116" height="50" rx="8" fill="#fff8e8" stroke="#9b773c"/><text x="373" y="220" text-anchor="middle" font-size="13">Bird hide</text>
  <circle cx="355" cy="72" r="36" fill="#eaf6df" stroke="#5c874d"/><text x="355" y="76" text-anchor="middle" font-size="13">Oak wood</text>
  <text x="42" y="206" font-size="18" font-weight="700">A</text><text x="255" y="72" font-size="18" font-weight="700">B</text>
  <text x="390" y="68" font-size="18" font-weight="700">C</text><text x="445" y="170" font-size="18" font-weight="700">D</text>
  <text x="300" y="225" font-size="18" font-weight="700">E</text><text x="205" y="232" font-size="18" font-weight="700">F</text>
  <text x="130" y="142" font-size="18" font-weight="700">G</text><text x="73" y="270" font-size="18" font-weight="700">H</text>
</svg>
"""

COMMUNITY_CENTRE_MAP_SVG = """
<svg viewBox="0 0 520 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Community centre plan">
  <rect x="18" y="20" width="484" height="260" rx="16" fill="#fbfbff" stroke="#9090aa" stroke-width="2"/>
  <path d="M82 225 H445 M255 225 V58" stroke="#b5b5c8" stroke-width="18" stroke-linecap="round"/>
  <rect x="50" y="190" width="105" height="54" rx="8" fill="#fff" stroke="#555"/><text x="102" y="222" text-anchor="middle" font-size="13">Reception</text>
  <rect x="190" y="52" width="130" height="56" rx="8" fill="#eef8ff" stroke="#406d91"/><text x="255" y="85" text-anchor="middle" font-size="13">Studio</text>
  <rect x="350" y="72" width="112" height="56" rx="8" fill="#f5f0ff" stroke="#6b5ca9"/><text x="406" y="105" text-anchor="middle" font-size="13">Computer room</text>
  <rect x="185" y="148" width="140" height="55" rx="8" fill="#fff8e8" stroke="#9b7130"/><text x="255" y="181" text-anchor="middle" font-size="13">Cafe</text>
  <rect x="348" y="194" width="112" height="50" rx="8" fill="#eef8ec" stroke="#4c8148"/><text x="404" y="224" text-anchor="middle" font-size="13">Garden</text>
  <text x="36" y="190" font-size="18" font-weight="700">A</text><text x="252" y="45" font-size="18" font-weight="700">B</text>
  <text x="466" y="80" font-size="18" font-weight="700">C</text><text x="328" y="180" font-size="18" font-weight="700">D</text>
  <text x="465" y="226" font-size="18" font-weight="700">E</text><text x="260" y="250" font-size="18" font-weight="700">F</text>
  <text x="145" y="150" font-size="18" font-weight="700">G</text><text x="82" y="265" font-size="18" font-weight="700">H</text>
</svg>
"""

MAP_OPTIONS = [
    "A", "B", "C", "D", "E", "F", "G", "H",
]


TEST2_LISTENING = {
    "minutes": 30,
    "sections": [
        {
            "number": 1,
            "title": "Section 1 - Holiday cottage enquiry",
            "instructions": "Questions 1-10. Complete the booking form and choose the correct answers. Write ONE WORD AND/OR A NUMBER for each answer.",
            "audio": "test2_s1.mp3",
            "questions": [
                {"type": "form", "id": "t2l1q1", "text": "Name of cottage: ____ Cottage", "answer": "Rose"},
                {"type": "form", "id": "t2l1q2", "text": "Village: ____", "answer": "Ashford"},
                {"type": "form", "id": "t2l1q3", "text": "Number of bedrooms: ____", "answer": "three"},
                {"type": "mcq", "id": "t2l1q4", "text": "Which facility is included in the rent?", "options": ["A  a swimming pool", "B  free Wi-Fi", "C  a private sauna"], "answer": "B  free Wi-Fi"},
                {"type": "form", "id": "t2l1q5", "text": "Low-season price per week: GBP ____", "answer": "450"},
                {"type": "form", "id": "t2l1q6", "text": "Available from the ____ of June", "answer": "12th"},
                {"type": "mcq", "id": "t2l1q7", "text": "What is the rule about pets?", "options": ["A  They are not allowed.", "B  A deposit is required.", "C  They are free of charge."], "answer": "B  A deposit is required."},
                {"type": "form", "id": "t2l1q8", "text": "Nearest railway station: ____", "answer": "Bridgwater"},
                {"type": "form", "id": "t2l1q9", "text": "Owner's surname: Mrs ____", "answer": "Patterson"},
                {"type": "mcq", "id": "t2l1q10", "text": "To confirm the booking, the customer must", "options": ["A  pay a 20% deposit", "B  send photo identification", "C  call the owner tomorrow"], "answer": "A  pay a 20% deposit"},
            ],
        },
        {
            "number": 2,
            "title": "Section 2 - Science discovery centre tour",
            "instructions": "Questions 11-20. Label the map and complete the notes.",
            "audio": "test2_s2.mp3",
            "map": {"svg": DISCOVERY_CENTRE_MAP_SVG},
            "questions": [
                {"type": "map", "id": "t2l2q1", "text": "Space Gallery", "options": MAP_OPTIONS, "answer": "B"},
                {"type": "map", "id": "t2l2q2", "text": "Demonstration Theatre", "options": MAP_OPTIONS, "answer": "D"},
                {"type": "map", "id": "t2l2q3", "text": "Experiment Lab", "options": MAP_OPTIONS, "answer": "E"},
                {"type": "map", "id": "t2l2q4", "text": "Gift Shop", "options": MAP_OPTIONS, "answer": "F"},
                {"type": "note", "id": "t2l2q5", "text": "The centre is closed every ____.", "answer": "Monday"},
                {"type": "note", "id": "t2l2q6", "text": "The first planetarium show starts at ____.", "answer": "10:30"},
                {"type": "mcq", "id": "t2l2q7", "text": "Visitors are asked not to", "options": ["A  bring food into the galleries", "B  take photographs anywhere", "C  use the lockers"], "answer": "A  bring food into the galleries"},
                {"type": "note", "id": "t2l2q8", "text": "School groups should gather near the ____ desk.", "answer": "information"},
                {"type": "note", "id": "t2l2q9", "text": "The workshop on rockets costs GBP ____ per child.", "answer": "3"},
                {"type": "mcq", "id": "t2l2q10", "text": "The speaker recommends booking the workshop", "options": ["A  at least a week ahead", "B  on arrival", "C  after lunch"], "answer": "A  at least a week ahead"},
            ],
        },
        {
            "number": 3,
            "title": "Section 3 - Geography field-trip planning",
            "instructions": "Questions 21-30. Match the tasks to the people and choose the correct answers.",
            "audio": "test2_s3.mp3",
            "questions": [
                {"type": "matching", "id": "t2l3q1", "text": "Prepare the risk assessment", "options": ["A  Maya", "B  Daniel", "C  both students"], "answer": "A  Maya"},
                {"type": "matching", "id": "t2l3q2", "text": "Check the tide times", "options": ["A  Maya", "B  Daniel", "C  both students"], "answer": "B  Daniel"},
                {"type": "matching", "id": "t2l3q3", "text": "Borrow the GPS units", "options": ["A  Maya", "B  Daniel", "C  both students"], "answer": "B  Daniel"},
                {"type": "matching", "id": "t2l3q4", "text": "Write the methods section", "options": ["A  Maya", "B  Daniel", "C  both students"], "answer": "C  both students"},
                {"type": "mcq", "id": "t2l3q5", "text": "Why does the tutor reject the first site?", "options": ["A  It is too far from campus.", "B  It has already been studied too often.", "C  Access is unsafe at high tide."], "answer": "C  Access is unsafe at high tide."},
                {"type": "note", "id": "t2l3q6", "text": "The students will collect samples along a ____ transect.", "answer": "shoreline"},
                {"type": "note", "id": "t2l3q7", "text": "Their main measurement will be sediment ____.", "answer": "size"},
                {"type": "mcq", "id": "t2l3q8", "text": "What does the tutor say about photographs?", "options": ["A  They must include a scale.", "B  They should be taken only at the end.", "C  They are not necessary."], "answer": "A  They must include a scale."},
                {"type": "note", "id": "t2l3q9", "text": "The draft report is due on ____.", "answer": "Friday"},
                {"type": "mcq", "id": "t2l3q10", "text": "The students need to improve their", "options": ["A  literature review", "B  statistical analysis", "C  presentation slides"], "answer": "B  statistical analysis"},
            ],
        },
        {
            "number": 4,
            "title": "Section 4 - Lecture on renewable energy storage",
            "instructions": "Questions 31-40. Complete the table and sentences. Write ONE WORD AND/OR A NUMBER for each answer.",
            "audio": "test2_s4.mp3",
            "table": {
                "title": "Energy storage technologies",
                "columns": ["Technology", "Main advantage", "Limitation"],
                "rows": [
                    [{"text": "Lithium-ion batteries"}, {"q": "t2l4q1"}, {"q": "t2l4q2"}],
                    [{"text": "Pumped hydro"}, {"q": "t2l4q3"}, {"text": "needs suitable geography"}],
                    [{"text": "Hydrogen"}, {"q": "t2l4q4"}, {"q": "t2l4q5"}],
                ],
            },
            "questions": [
                {"type": "table", "id": "t2l4q1", "text": "Lithium-ion batteries: main advantage", "answer": "rapid response"},
                {"type": "table", "id": "t2l4q2", "text": "Lithium-ion batteries: limitation", "answer": "cost"},
                {"type": "table", "id": "t2l4q3", "text": "Pumped hydro: main advantage", "answer": "large capacity"},
                {"type": "table", "id": "t2l4q4", "text": "Hydrogen: main advantage", "answer": "seasonal storage"},
                {"type": "table", "id": "t2l4q5", "text": "Hydrogen: limitation", "answer": "efficiency"},
                {"type": "sentence", "id": "t2l4q6", "text": "Grid operators must balance supply and ____ every second.", "answer": "demand"},
                {"type": "sentence", "id": "t2l4q7", "text": "Storage becomes more important when electricity comes from ____ sources.", "answer": "variable"},
                {"type": "mcq", "id": "t2l4q8", "text": "What does the lecturer say about batteries?", "options": ["A  They are best for short-term balancing.", "B  They have solved seasonal storage.", "C  They are now cheaper than all alternatives."], "answer": "A  They are best for short-term balancing."},
                {"type": "sentence", "id": "t2l4q9", "text": "Future systems will probably use a ____ of technologies.", "answer": "portfolio"},
                {"type": "mcq", "id": "t2l4q10", "text": "The lecturer's main conclusion is that storage policy should focus on", "options": ["A  one dominant technology", "B  matching storage to different time scales", "C  reducing electricity demand only"], "answer": "B  matching storage to different time scales"},
            ],
        },
    ],
}


TEST3_LISTENING = {
    "minutes": 30,
    "sections": [
        {
            "number": 1,
            "title": "Section 1 - Joining a public library",
            "instructions": "Questions 1-10. Complete the membership form and choose the correct answers.",
            "audio": "test3_s1.mp3",
            "questions": [
                {"type": "form", "id": "t3l1q1", "text": "Applicant's surname: ____", "answer": "Henderson"},
                {"type": "form", "id": "t3l1q2", "text": "Street address: 48 ____ Road", "answer": "Merton"},
                {"type": "form", "id": "t3l1q3", "text": "Postcode: ____ 7PL", "answer": "BR6"},
                {"type": "mcq", "id": "t3l1q4", "text": "Which membership does the applicant choose?", "options": ["A  adult", "B  student", "C  family"], "answer": "B  student"},
                {"type": "form", "id": "t3l1q5", "text": "Membership fee: GBP ____", "answer": "12"},
                {"type": "form", "id": "t3l1q6", "text": "Proof of address needed: a ____ bill", "answer": "utility"},
                {"type": "mcq", "id": "t3l1q7", "text": "How many items can new members borrow?", "options": ["A  four", "B  six", "C  eight"], "answer": "B  six"},
                {"type": "form", "id": "t3l1q8", "text": "Late charge per day: ____ pence", "answer": "20"},
                {"type": "form", "id": "t3l1q9", "text": "The library closes at ____ on Thursdays.", "answer": "8:00"},
                {"type": "mcq", "id": "t3l1q10", "text": "The computer room must be booked", "options": ["A  online", "B  by telephone", "C  at the reception desk"], "answer": "A  online"},
            ],
        },
        {
            "number": 2,
            "title": "Section 2 - Riverside Food Festival announcement",
            "instructions": "Questions 11-20. Label the festival map and complete the notes.",
            "audio": "test3_s2.mp3",
            "map": {"svg": FESTIVAL_MAP_SVG},
            "questions": [
                {"type": "map", "id": "t3l2q1", "text": "Chef demonstration stage", "options": MAP_OPTIONS, "answer": "B"},
                {"type": "map", "id": "t3l2q2", "text": "Children's cooking tent", "options": MAP_OPTIONS, "answer": "D"},
                {"type": "map", "id": "t3l2q3", "text": "Information desk", "options": MAP_OPTIONS, "answer": "E"},
                {"type": "map", "id": "t3l2q4", "text": "Picnic area", "options": MAP_OPTIONS, "answer": "C"},
                {"type": "note", "id": "t3l2q5", "text": "The festival begins on ____ evening.", "answer": "Friday"},
                {"type": "note", "id": "t3l2q6", "text": "Advance tickets cost GBP ____.", "answer": "8"},
                {"type": "mcq", "id": "t3l2q7", "text": "Visitors arriving by car should use", "options": ["A  the station car park", "B  the school field", "C  the supermarket car park"], "answer": "B  the school field"},
                {"type": "note", "id": "t3l2q8", "text": "Reusable cups require a GBP ____ deposit.", "answer": "2"},
                {"type": "note", "id": "t3l2q9", "text": "The final event on Sunday is a ____ competition.", "answer": "baking"},
                {"type": "mcq", "id": "t3l2q10", "text": "What does the speaker say about dogs?", "options": ["A  They are allowed only on leads.", "B  They are banned from the whole site.", "C  They need a separate ticket."], "answer": "A  They are allowed only on leads."},
            ],
        },
        {
            "number": 3,
            "title": "Section 3 - Dissertation planning tutorial",
            "instructions": "Questions 21-30. Match each issue to the tutor's advice and complete the notes.",
            "audio": "test3_s3.mp3",
            "questions": [
                {"type": "matching", "id": "t3l3q1", "text": "Research question", "options": ["A  narrow the focus", "B  add more recent sources", "C  collect pilot data", "D  change the presentation"], "answer": "A  narrow the focus"},
                {"type": "matching", "id": "t3l3q2", "text": "Literature review", "options": ["A  narrow the focus", "B  add more recent sources", "C  collect pilot data", "D  change the presentation"], "answer": "B  add more recent sources"},
                {"type": "matching", "id": "t3l3q3", "text": "Questionnaire", "options": ["A  narrow the focus", "B  add more recent sources", "C  collect pilot data", "D  change the presentation"], "answer": "C  collect pilot data"},
                {"type": "matching", "id": "t3l3q4", "text": "Final talk", "options": ["A  narrow the focus", "B  add more recent sources", "C  collect pilot data", "D  change the presentation"], "answer": "D  change the presentation"},
                {"type": "mcq", "id": "t3l3q5", "text": "What is the student's main topic?", "options": ["A  online learning habits", "B  part-time employment", "C  library use among first-years"], "answer": "C  library use among first-years"},
                {"type": "note", "id": "t3l3q6", "text": "The sample should include students from ____ faculties.", "answer": "three"},
                {"type": "note", "id": "t3l3q7", "text": "Interviews should last about ____ minutes.", "answer": "20"},
                {"type": "mcq", "id": "t3l3q8", "text": "The tutor warns that email responses may be", "options": ["A  too informal", "B  biased", "C  expensive"], "answer": "B  biased"},
                {"type": "note", "id": "t3l3q9", "text": "The student will submit a revised plan by ____.", "answer": "Wednesday"},
                {"type": "mcq", "id": "t3l3q10", "text": "The tutor suggests putting the timetable in", "options": ["A  an appendix", "B  the abstract", "C  the title page"], "answer": "A  an appendix"},
            ],
        },
        {
            "number": 4,
            "title": "Section 4 - Lecture on deep-sea biology",
            "instructions": "Questions 31-40. Complete the table and sentences.",
            "audio": "test3_s4.mp3",
            "table": {
                "title": "Adaptations in deep-sea organisms",
                "columns": ["Adaptation", "Purpose", "Example"],
                "rows": [
                    [{"text": "Bioluminescence"}, {"q": "t3l4q1"}, {"q": "t3l4q2"}],
                    [{"text": "Slow metabolism"}, {"q": "t3l4q3"}, {"text": "many abyssal fish"}],
                    [{"text": "Pressure-resistant enzymes"}, {"q": "t3l4q4"}, {"q": "t3l4q5"}],
                ],
            },
            "questions": [
                {"type": "table", "id": "t3l4q1", "text": "Bioluminescence: purpose", "answer": "communication"},
                {"type": "table", "id": "t3l4q2", "text": "Bioluminescence: example", "answer": "anglerfish"},
                {"type": "table", "id": "t3l4q3", "text": "Slow metabolism: purpose", "answer": "conserve energy"},
                {"type": "table", "id": "t3l4q4", "text": "Pressure-resistant enzymes: purpose", "answer": "maintain function"},
                {"type": "table", "id": "t3l4q5", "text": "Pressure-resistant enzymes: example", "answer": "microbes"},
                {"type": "sentence", "id": "t3l4q6", "text": "Below 1,000 metres, sunlight is virtually ____.", "answer": "absent"},
                {"type": "sentence", "id": "t3l4q7", "text": "Food often arrives as particles known as marine ____.", "answer": "snow"},
                {"type": "mcq", "id": "t3l4q8", "text": "Why are remotely operated vehicles useful?", "options": ["A  They can stay underwater longer than divers.", "B  They are cheaper than nets.", "C  They replace laboratory analysis."], "answer": "A  They can stay underwater longer than divers."},
                {"type": "sentence", "id": "t3l4q9", "text": "The lecturer says mining could disturb fragile ____.", "answer": "habitats"},
                {"type": "mcq", "id": "t3l4q10", "text": "The lecture mainly argues that the deep sea is", "options": ["A  empty and stable", "B  biologically rich but vulnerable", "C  already well understood"], "answer": "B  biologically rich but vulnerable"},
            ],
        },
    ],
}


TEST4_LISTENING = {
    "minutes": 30,
    "sections": [
        {
            "number": 1,
            "title": "Section 1 - Enrolling in an evening course",
            "instructions": "Questions 1-10. Complete the enrolment form and choose the correct answers.",
            "audio": "test4_s1.mp3",
            "questions": [
                {"type": "form", "id": "t4l1q1", "text": "Course chosen: ____ cooking", "answer": "Italian"},
                {"type": "form", "id": "t4l1q2", "text": "Classes are held on ____ evenings.", "answer": "Tuesday"},
                {"type": "form", "id": "t4l1q3", "text": "Course length: ____ weeks", "answer": "eight"},
                {"type": "mcq", "id": "t4l1q4", "text": "Why does the caller choose this course?", "options": ["A  It is close to home.", "B  It has a beginner group.", "C  It is the cheapest option."], "answer": "B  It has a beginner group."},
                {"type": "form", "id": "t4l1q5", "text": "Fee: GBP ____", "answer": "96"},
                {"type": "form", "id": "t4l1q6", "text": "Materials fee covers a recipe ____.", "answer": "booklet"},
                {"type": "mcq", "id": "t4l1q7", "text": "What must students bring?", "options": ["A  knives", "B  an apron", "C  their own pans"], "answer": "B  an apron"},
                {"type": "form", "id": "t4l1q8", "text": "Tutor's surname: ____", "answer": "Lombardi"},
                {"type": "form", "id": "t4l1q9", "text": "Payment reference: ____ 417", "answer": "COOK"},
                {"type": "mcq", "id": "t4l1q10", "text": "If the caller cancels, she must do so", "options": ["A  at least 48 hours before the first class", "B  before the final class", "C  by visiting the office"], "answer": "A  at least 48 hours before the first class"},
            ],
        },
        {
            "number": 2,
            "title": "Section 2 - Nature reserve guided walk",
            "instructions": "Questions 11-20. Label the route map and complete the notes.",
            "audio": "test4_s2.mp3",
            "map": {"svg": NATURE_RESERVE_MAP_SVG},
            "questions": [
                {"type": "map", "id": "t4l2q1", "text": "Lake viewpoint", "options": MAP_OPTIONS, "answer": "B"},
                {"type": "map", "id": "t4l2q2", "text": "Oak wood", "options": MAP_OPTIONS, "answer": "C"},
                {"type": "map", "id": "t4l2q3", "text": "Bird hide", "options": MAP_OPTIONS, "answer": "E"},
                {"type": "map", "id": "t4l2q4", "text": "Car park", "options": MAP_OPTIONS, "answer": "A"},
                {"type": "note", "id": "t4l2q5", "text": "The walk lasts about ____ hours.", "answer": "two"},
                {"type": "note", "id": "t4l2q6", "text": "Visitors should wear ____ shoes.", "answer": "waterproof"},
                {"type": "mcq", "id": "t4l2q7", "text": "What wildlife is most likely to be seen today?", "options": ["A  deer", "B  otters", "C  migrating geese"], "answer": "C  migrating geese"},
                {"type": "note", "id": "t4l2q8", "text": "The reserve asks visitors not to pick ____.", "answer": "flowers"},
                {"type": "note", "id": "t4l2q9", "text": "Emergency phone boxes are coloured ____.", "answer": "yellow"},
                {"type": "mcq", "id": "t4l2q10", "text": "At the end of the walk, visitors can", "options": ["A  buy local honey", "B  feed the birds", "C  camp overnight"], "answer": "A  buy local honey"},
            ],
        },
        {
            "number": 3,
            "title": "Section 3 - Sustainable architecture project",
            "instructions": "Questions 21-30. Match features to buildings and complete the notes.",
            "audio": "test4_s3.mp3",
            "questions": [
                {"type": "matching", "id": "t4l3q1", "text": "Green roof", "options": ["A  library", "B  sports centre", "C  student residence"], "answer": "A  library"},
                {"type": "matching", "id": "t4l3q2", "text": "Natural ventilation", "options": ["A  library", "B  sports centre", "C  student residence"], "answer": "B  sports centre"},
                {"type": "matching", "id": "t4l3q3", "text": "Rainwater recycling", "options": ["A  library", "B  sports centre", "C  student residence"], "answer": "C  student residence"},
                {"type": "matching", "id": "t4l3q4", "text": "Solar shading", "options": ["A  library", "B  sports centre", "C  student residence"], "answer": "A  library"},
                {"type": "mcq", "id": "t4l3q5", "text": "What does the tutor criticise about the students' first plan?", "options": ["A  It is too descriptive.", "B  It contains too much data.", "C  It ignores cost completely."], "answer": "A  It is too descriptive."},
                {"type": "note", "id": "t4l3q6", "text": "They need to compare predicted and actual energy ____.", "answer": "use"},
                {"type": "note", "id": "t4l3q7", "text": "The tutor recommends interviewing the building ____.", "answer": "manager"},
                {"type": "mcq", "id": "t4l3q8", "text": "The group decides to remove", "options": ["A  the historical background", "B  the photographs", "C  the cost table"], "answer": "A  the historical background"},
                {"type": "note", "id": "t4l3q9", "text": "Their presentation should last ____ minutes.", "answer": "15"},
                {"type": "mcq", "id": "t4l3q10", "text": "The tutor says the conclusion should focus on", "options": ["A  design principles", "B  personal opinions", "C  future architects"], "answer": "A  design principles"},
            ],
        },
        {
            "number": 4,
            "title": "Section 4 - Lecture on the history of timekeeping",
            "instructions": "Questions 31-40. Complete the table and summary.",
            "audio": "test4_s4.mp3",
            "table": {
                "title": "Developments in measuring time",
                "columns": ["Period/device", "Strength", "Weakness"],
                "rows": [
                    [{"text": "Sundials"}, {"q": "t4l4q1"}, {"q": "t4l4q2"}],
                    [{"text": "Mechanical clocks"}, {"q": "t4l4q3"}, {"q": "t4l4q4"}],
                    [{"text": "Atomic clocks"}, {"q": "t4l4q5"}, {"text": "complex and expensive"}],
                ],
            },
            "questions": [
                {"type": "table", "id": "t4l4q1", "text": "Sundials: strength", "answer": "simple"},
                {"type": "table", "id": "t4l4q2", "text": "Sundials: weakness", "answer": "cloudy weather"},
                {"type": "table", "id": "t4l4q3", "text": "Mechanical clocks: strength", "answer": "independent"},
                {"type": "table", "id": "t4l4q4", "text": "Mechanical clocks: weakness", "answer": "friction"},
                {"type": "table", "id": "t4l4q5", "text": "Atomic clocks: strength", "answer": "accuracy"},
                {"type": "sentence", "id": "t4l4q6", "text": "Early societies used timekeeping to organise farming and ____.", "answer": "religion"},
                {"type": "sentence", "id": "t4l4q7", "text": "Pendulum clocks improved timekeeping by reducing ____.", "answer": "error"},
                {"type": "mcq", "id": "t4l4q8", "text": "Why did railways increase the need for standard time?", "options": ["A  Timetables crossed local time zones.", "B  Trains became slower.", "C  Passengers could not read clocks."], "answer": "A  Timetables crossed local time zones."},
                {"type": "sentence", "id": "t4l4q9", "text": "Modern navigation systems depend on precise ____.", "answer": "signals"},
                {"type": "mcq", "id": "t4l4q10", "text": "The lecturer says accurate timekeeping has become", "options": ["A  less visible but more essential", "B  mainly a scientific curiosity", "C  unnecessary for ordinary life"], "answer": "A  less visible but more essential"},
            ],
        },
    ],
}


TEST5_LISTENING = {
    "minutes": 30,
    "sections": [
        {
            "number": 1,
            "title": "Section 1 - Hotel reservation",
            "instructions": "Questions 1-10. Complete the booking details and choose the correct answers.",
            "audio": "test5_s1.mp3",
            "questions": [
                {"type": "form", "id": "t5l1q1", "text": "Guest surname: ____", "answer": "Collins"},
                {"type": "form", "id": "t5l1q2", "text": "Arrival date: ____ May", "answer": "14th"},
                {"type": "form", "id": "t5l1q3", "text": "Number of nights: ____", "answer": "three"},
                {"type": "mcq", "id": "t5l1q4", "text": "Which room does the guest book?", "options": ["A  standard double", "B  garden-view double", "C  family suite"], "answer": "B  garden-view double"},
                {"type": "form", "id": "t5l1q5", "text": "Room rate per night: GBP ____", "answer": "118"},
                {"type": "form", "id": "t5l1q6", "text": "Breakfast is served from ____.", "answer": "7:00"},
                {"type": "mcq", "id": "t5l1q7", "text": "What extra service does the guest request?", "options": ["A  airport taxi", "B  laundry", "C  bicycle hire"], "answer": "A  airport taxi"},
                {"type": "form", "id": "t5l1q8", "text": "The taxi should arrive at ____ p.m.", "answer": "6:30"},
                {"type": "form", "id": "t5l1q9", "text": "Email address ends with @____.com", "answer": "northmail"},
                {"type": "mcq", "id": "t5l1q10", "text": "The booking can be cancelled free of charge until", "options": ["A  noon on Monday", "B  24 hours before arrival", "C  the morning of arrival"], "answer": "B  24 hours before arrival"},
            ],
        },
        {
            "number": 2,
            "title": "Section 2 - Refurbished community centre",
            "instructions": "Questions 11-20. Label the centre plan and complete the notes.",
            "audio": "test5_s2.mp3",
            "map": {"svg": COMMUNITY_CENTRE_MAP_SVG},
            "questions": [
                {"type": "map", "id": "t5l2q1", "text": "Reception", "options": MAP_OPTIONS, "answer": "A"},
                {"type": "map", "id": "t5l2q2", "text": "Dance studio", "options": MAP_OPTIONS, "answer": "B"},
                {"type": "map", "id": "t5l2q3", "text": "Computer room", "options": MAP_OPTIONS, "answer": "C"},
                {"type": "map", "id": "t5l2q4", "text": "Community garden", "options": MAP_OPTIONS, "answer": "E"},
                {"type": "note", "id": "t5l2q5", "text": "The centre reopens on ____.", "answer": "Saturday"},
                {"type": "note", "id": "t5l2q6", "text": "New members receive a free ____ session.", "answer": "fitness"},
                {"type": "mcq", "id": "t5l2q7", "text": "The speaker says the cafe will mainly sell", "options": ["A  hot meals", "B  snacks and drinks", "C  local vegetables"], "answer": "B  snacks and drinks"},
                {"type": "note", "id": "t5l2q8", "text": "Evening classes finish at ____ p.m.", "answer": "9"},
                {"type": "note", "id": "t5l2q9", "text": "Volunteers are needed for the ____ club.", "answer": "gardening"},
                {"type": "mcq", "id": "t5l2q10", "text": "People should book the opening day workshops", "options": ["A  online", "B  by post", "C  at the door only"], "answer": "A  online"},
            ],
        },
        {
            "number": 3,
            "title": "Section 3 - Designing a transport survey",
            "instructions": "Questions 21-30. Match survey decisions to reasons and complete the notes.",
            "audio": "test5_s3.mp3",
            "questions": [
                {"type": "matching", "id": "t5l3q1", "text": "Use bus stops for interviews", "options": ["A  gives a wider age range", "B  avoids disturbing drivers", "C  improves response rate", "D  reduces printing costs"], "answer": "C  improves response rate"},
                {"type": "matching", "id": "t5l3q2", "text": "Exclude car drivers from the main sample", "options": ["A  gives a wider age range", "B  avoids disturbing drivers", "C  improves response rate", "D  reduces printing costs"], "answer": "B  avoids disturbing drivers"},
                {"type": "matching", "id": "t5l3q3", "text": "Add a question about cycling", "options": ["A  gives a wider age range", "B  avoids disturbing drivers", "C  improves response rate", "D  reduces printing costs"], "answer": "A  gives a wider age range"},
                {"type": "matching", "id": "t5l3q4", "text": "Use a QR code for follow-up comments", "options": ["A  gives a wider age range", "B  avoids disturbing drivers", "C  improves response rate", "D  reduces printing costs"], "answer": "D  reduces printing costs"},
                {"type": "mcq", "id": "t5l3q5", "text": "What problem does the tutor find in the draft questionnaire?", "options": ["A  Some questions are leading.", "B  It is too short.", "C  It ignores public transport."], "answer": "A  Some questions are leading."},
                {"type": "note", "id": "t5l3q6", "text": "The sample should include at least ____ people.", "answer": "120"},
                {"type": "note", "id": "t5l3q7", "text": "The students will compare weekday and ____ travel.", "answer": "weekend"},
                {"type": "mcq", "id": "t5l3q8", "text": "The tutor suggests presenting results as", "options": ["A  maps", "B  pie charts", "C  interview transcripts"], "answer": "A  maps"},
                {"type": "note", "id": "t5l3q9", "text": "Their ethics form must be signed by ____.", "answer": "Monday"},
                {"type": "mcq", "id": "t5l3q10", "text": "The students agree to pilot the survey in the", "options": ["A  library foyer", "B  bus station", "C  lecture theatre"], "answer": "A  library foyer"},
            ],
        },
        {
            "number": 4,
            "title": "Section 4 - Lecture on volcanic soils and agriculture",
            "instructions": "Questions 31-40. Complete the table and sentences.",
            "audio": "test5_s4.mp3",
            "table": {
                "title": "Volcanic soils",
                "columns": ["Feature", "Effect on farming", "Risk"],
                "rows": [
                    [{"text": "Mineral content"}, {"q": "t5l4q1"}, {"q": "t5l4q2"}],
                    [{"text": "Porous structure"}, {"q": "t5l4q3"}, {"q": "t5l4q4"}],
                    [{"text": "Steep slopes"}, {"q": "t5l4q5"}, {"text": "erosion"}],
                ],
            },
            "questions": [
                {"type": "table", "id": "t5l4q1", "text": "Mineral content: effect on farming", "answer": "high fertility"},
                {"type": "table", "id": "t5l4q2", "text": "Mineral content: risk", "answer": "toxicity"},
                {"type": "table", "id": "t5l4q3", "text": "Porous structure: effect on farming", "answer": "drainage"},
                {"type": "table", "id": "t5l4q4", "text": "Porous structure: risk", "answer": "drought"},
                {"type": "table", "id": "t5l4q5", "text": "Steep slopes: effect on farming", "answer": "microclimates"},
                {"type": "sentence", "id": "t5l4q6", "text": "Ash breaks down into soil through chemical ____.", "answer": "weathering"},
                {"type": "sentence", "id": "t5l4q7", "text": "Farmers often grow coffee and ____ on volcanic slopes.", "answer": "grapes"},
                {"type": "mcq", "id": "t5l4q8", "text": "What does the lecturer say about volcanic areas?", "options": ["A  They combine opportunity and danger.", "B  They should never be farmed.", "C  They are useful only for grazing."], "answer": "A  They combine opportunity and danger."},
                {"type": "sentence", "id": "t5l4q9", "text": "Monitoring systems can give communities more time to ____.", "answer": "evacuate"},
                {"type": "mcq", "id": "t5l4q10", "text": "The main point of the lecture is that volcanic farming depends on", "options": ["A  balancing fertile land with risk management", "B  avoiding all modern technology", "C  using only traditional crops"], "answer": "A  balancing fertile land with risk management"},
            ],
        },
    ],
}
