"""Listening — Section 4 note-taking practice (lecture style, plays once)."""

SECTION4_NOTE_LECTURES = [
    {
        "id": "habits-lecture",
        "title": "Lecture: the science of habit formation",
        "audio": "s4_habits.mp3",
        "instructions": (
            "You will hear a university lecture once. Complete the notes below. "
            "Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each gap."
        ),
        "lines": [
            ("NARRATOR", "Section 4. You will hear part of a lecture on habit formation."),
            (
                "LECTURER",
                "Today I want to outline how habits form in the brain. "
                "Researchers describe a three-step loop: cue, routine, and reward. "
                "The cue might be a time of day or an emotional state. "
                "The routine is the behaviour itself, such as checking your phone. "
                "The reward reinforces the loop — often a small dopamine release. "
                "Studies suggest it takes roughly sixty-six days on average to establish "
                "a new automatic habit, though this varies widely. "
                "Keystone habits, like regular exercise, can trigger other positive changes. "
                "Finally, replacing a bad routine while keeping the same cue and reward "
                "is often more effective than trying to eliminate the cue entirely.",
            ),
        ],
        "template": [
            {"id": "n1", "label": "Habit loop steps", "prefix": "Cue → ", "suffix": " → reward", "answer": "routine"},
            {"id": "n2", "label": "Average days to form habit", "prefix": "", "suffix": " days", "answer": "66"},
            {"id": "n3", "label": "Example keystone habit", "prefix": "", "suffix": "", "answer": "exercise"},
            {"id": "n4", "label": "Strategy", "prefix": "Replace the ", "suffix": ", keep cue and reward", "answer": "routine"},
        ],
    },
    {
        "id": "renewable-lecture",
        "title": "Lecture: renewable energy storage",
        "audio": "s4_renewable.mp3",
        "instructions": (
            "Listen once and complete the notes. Write NO MORE THAN TWO WORDS for each answer."
        ),
        "lines": [
            ("NARRATOR", "Section 4. You will hear a lecture about storing renewable energy."),
            (
                "LECTURER",
                "Solar and wind output fluctuates, so grid operators need storage. "
                "Lithium-ion batteries dominate short-term storage but remain expensive at scale. "
                "Pumped hydro accounts for the vast majority of global storage capacity today. "
                "Green hydrogen is attracting investment for longer seasonal storage. "
                "A key challenge is transmission losses when electricity travels long distances. "
                "Policy makers are prioritising hybrid systems that combine batteries with hydro.",
            ),
        ],
        "template": [
            {"id": "r1", "label": "Dominant short-term storage", "prefix": "", "suffix": " batteries", "answer": "lithium-ion"},
            {"id": "r2", "label": "Largest global capacity", "prefix": "Pumped ", "suffix": "", "answer": "hydro"},
            {"id": "r3", "label": "Seasonal storage candidate", "prefix": "Green ", "suffix": "", "answer": "hydrogen"},
            {"id": "r4", "label": "Long-distance issue", "prefix": "", "suffix": " losses", "answer": "transmission"},
        ],
    },
]
