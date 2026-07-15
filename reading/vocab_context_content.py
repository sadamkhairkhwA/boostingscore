"""Reading — vocabulary in context practice (data-driven).

Add excerpts to VOCAB_CONTEXT_EXCERPTS. Each item: passage with {{word}} marker,
options, answer value, explanation with context clues.
"""

VOCAB_CONTEXT_EXCERPTS = [
    {
        "id": "vc-1",
        "topic": "Environment",
        "passage_html": (
            "Municipal planners argue that green corridors can "
            '<span class="rs-hl-blue">mitigate</span> urban heat by shading streets '
            "and improving airflow between buildings."
        ),
        "target_word": "mitigate",
        "prompt": "What does mitigate most likely mean in this context?",
        "options": [
            {"value": "a", "label": "make less severe"},
            {"value": "b", "label": "measure precisely"},
            {"value": "c", "label": "ignore completely"},
            {"value": "d", "label": "celebrate publicly"},
        ],
        "answer": "a",
        "explanation": (
            "Clues: green corridors reduce urban heat — the word describes lessening a problem, "
            "not measuring or ignoring it."
        ),
    },
    {
        "id": "vc-2",
        "topic": "Health",
        "passage_html": (
            "The trial was halted when several participants reported "
            '<span class="rs-hl-blue">adverse</span> reactions, including dizziness and nausea, '
            "within hours of the first dose."
        ),
        "target_word": "adverse",
        "prompt": "What does adverse mean here?",
        "options": [
            {"value": "a", "label": "harmful or negative"},
            {"value": "b", "label": "unexpected but mild"},
            {"value": "c", "label": "beneficial"},
            {"value": "d", "label": "rare and harmless"},
        ],
        "answer": "a",
        "explanation": (
            "Clues: dizziness and nausea after a dose signal harmful side effects — "
            "adverse contrasts with beneficial."
        ),
    },
    {
        "id": "vc-3",
        "topic": "Technology",
        "passage_html": (
            "Engineers found that the new chip design could "
            '<span class="rs-hl-blue">bolster</span> battery life without increasing the '
            "physical size of the device."
        ),
        "target_word": "bolster",
        "prompt": "Choose the best meaning of bolster.",
        "options": [
            {"value": "a", "label": "strengthen or support"},
            {"value": "b", "label": "drain or reduce"},
            {"value": "c", "label": "replace entirely"},
            {"value": "d", "label": "delay temporarily"},
        ],
        "answer": "a",
        "explanation": (
            "Clues: battery life improves — bolster means support or strengthen, "
            "not drain or replace."
        ),
    },
    {
        "id": "vc-4",
        "topic": "Education",
        "passage_html": (
            "Critics claim the reform is merely "
            '<span class="rs-hl-blue">cosmetic</span>, changing appearances in reports '
            "without altering how funding reaches classrooms."
        ),
        "target_word": "cosmetic",
        "prompt": "What does cosmetic suggest about the reform?",
        "options": [
            {"value": "a", "label": "superficial — only on the surface"},
            {"value": "b", "label": "medically necessary"},
            {"value": "c", "label": "widely celebrated"},
            {"value": "d", "label": "financially generous"},
        ],
        "answer": "a",
        "explanation": (
            "Clues: changing appearances without altering funding — cosmetic means "
            "surface-level, not deep change."
        ),
    },
    {
        "id": "vc-5",
        "topic": "Science",
        "passage_html": (
            "Because the sample size was small, the authors "
            '<span class="rs-hl-blue">caution</span> against drawing firm conclusions '
            "from the preliminary figures."
        ),
        "target_word": "caution",
        "prompt": "What are the authors doing when they caution?",
        "options": [
            {"value": "a", "label": "warning readers to be careful"},
            {"value": "b", "label": "proving the results are wrong"},
            {"value": "c", "label": "refusing to publish"},
            {"value": "d", "label": "celebrating a breakthrough"},
        ],
        "answer": "a",
        "explanation": (
            "Clues: small sample + preliminary figures — they warn against overconfidence, "
            "not disprove or refuse publication."
        ),
    },
]
