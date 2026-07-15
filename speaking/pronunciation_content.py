"""Pronunciation study content for the Speaking section."""


def _w(word: str, phonetic: str, mistake: str) -> dict:
    return {
        "word": word,
        "phonetic": phonetic,
        "mistake": mistake,
        "audio": f"pronunciation_audio/{word.lower()}.mp3",
    }


MISPRONOUNCED_WORDS = [
    _w("access", "AK-ses", "Confused with excess; stress is on the first syllable with a short a."),
    _w("analysis", "uh-NAL-uh-sis", "Stress on the first syllable (AN-uh-lisis) instead of the second."),
    _w("architecture", "AR-ki-tek-chur", "Stress errors: ar-ki-TEK-ture or ar-KI-tek-chur."),
    _w("asked", "ahskt", "Pronounced ask-ed as two syllables; the e is silent and the ending is /t/."),
    _w("business", "BIZ-nis", "Pronounced BUS-i-ness with four syllables instead of two."),
    _w("category", "KAT-uh-gor-ee", "Stress on the second syllable: ca-TE-gor-ee."),
    _w("chaos", "KAY-os", "Pronounced CHA-os with ch as in church; it starts with a k sound."),
    _w("chaotic", "kay-OT-ik", "Pronounced cha-OT-ic; related words keep the k sound from chaos."),
    _w("choir", "KWYR", "Pronounced CHOY-er; the ch here sounds like k."),
    _w("clothes", "klohz", "Pronounced klo-thes with an audible th; it rhymes with nose."),
    _w("colleague", "KOL-eeg", "Pronounced co-LEAGUE; soft g and only two syllables."),
    _w("colonel", "KUR-nl", "Pronounced co-lo-NEL; it sounds like kernel."),
    _w("comfortable", "KUMF-tuh-bl", "Stress on the wrong syllable: kom-for-TAY-bul."),
    _w("cupboard", "KUB-urd", "Pronounced cup-board with a p sound; the p is silent."),
    _w("debt", "det", "Pronounced deb-t; the b is silent."),
    _w("determine", "di-TUR-min", "Stress on the first syllable (DE-ter-mine) instead of the second."),
    _w("determination", "di-tur-muh-NAY-shuhn", "Stress stays on the wrong syllable when forming the noun."),
    _w("develop", "di-VEL-up", "Stress on the first syllable (DE-vel-op) instead of the second."),
    _w("development", "di-VEL-up-muhnt", "Stress on the first syllable (DE-vel-op-ment) instead of the second."),
    _w("entrepreneur", "on-truh-pruh-NUR", "Wrong stress and vowels; final syllable is -NUR, not -NYUR."),
    _w("environment", "in-VY-ruhn-muhnt", "Missing syllable or wrong stress: en-VY-ment or en-VI-run-ment."),
    _w("February", "FEB-roo-er-ee", "First r is often dropped: FEB-yoo-ary."),
    _w("genre", "ZHAHN-ruh", "Pronounced GEN-ree or JEN-ruh; the g is soft like the s in measure."),
    _w("height", "hyt", "Pronounced hee-GHT with a hard gh; the gh is silent."),
    _w("hierarchy", "HY-uh-rahr-kee", "Pronounced HY-ar-kee; four syllables with stress on the first."),
    _w("interesting", "IN-truh-sting", "Four syllables in-TRES-ting; standard form has three."),
    _w("island", "EYE-luhnd", "Pronounced IS-land with an audible s; the s is silent."),
    _w("jewellery", "JOO-uhl-ree", "Four syllables jew-EL-er-ee with wrong stress (BrE spelling)."),
    _w("library", "LY-brer-ee", "Pronounced li-BRARY with stress on the second syllable."),
    _w("mischievous", "MIS-chuh-vuhs", "Pronounced mis-CHEE-vee-us with four syllables."),
    _w("months", "munths", "Pronounced mon-ths as two syllables; th blends with the final consonant."),
    _w("niche", "neesh", "Pronounced NY-chee or NITCH inconsistently; BrE exam answers favour neesh."),
    _w("often", "OFF-en", "Off-TEN with a hard t (hypercorrection); BrE learners often keep the t silent."),
    _w("particularly", "puh-TIK-yuh-luhr-lee", "Wrong stress and vowels: par-TIK-yoo-lar-lee."),
    _w("photograph", "FOH-tuh-graf", "Stress on the third syllable (fo-to-GRAF) in the noun form."),
    _w("photography", "fuh-TOG-ruh-fee", "Keeps photograph stress; stress shifts to the second syllable."),
    _w("pronunciation", "pruh-nun-see-AY-shuhn", "Ironically pro-NOUN-ci-ation; it follows pronounce, not pronoun."),
    _w("queue", "kyoo", "Pronounced kway or kyoo-ee; the ue sounds like oo in food."),
    _w("receipt", "ri-SEET", "Pronounced re-CEIPT with a p sound; the p is silent."),
    _w("recipe", "RES-uh-pee", "Stress on the first syllable; often misread as re-CIPE."),
    _w("rural", "ROOR-uhl", "Pronounced RUR-al; the first syllable sounds like cure."),
    _w("salmon", "SAM-un", "Pronounced SAL-mon with an l sound; the l is silent."),
    _w("schedule", "SHED-yool (BrE) / SKED-jool (AmE)", "Mixing BrE and AmE in one answer; pick one and stay consistent."),
    _w("specific", "spuh-SIF-ik", "Pronounced SPE-si-fik; stress is on the second syllable."),
    _w("squirrel", "SKWIR-uhl", "Pronounced skwuh-REL with the wrong vowel in the second syllable."),
    _w("subtle", "SUT-ul", "Pronounced SUB-tul with a b sound; the b is silent."),
    _w("successful", "suk-SES-fl", "Double c as two k sounds or stress on the first syllable."),
    _w("suite", "sweet", "Pronounced soo-ITE; it rhymes with sweet."),
    _w("thorough", "THUR-uh", "Pronounced thor-OUGH like through; the -ough sounds like uh."),
    _w("vehicle", "VEE-uh-kul", "Three syllables VEH-hi-cle instead of two."),
    _w("vegetable", "VEJ-tuh-bl", "Extra syllables: vej-e-TAY-bul; the middle vowel is often dropped."),
    _w("Wednesday", "WENZ-day", "Pronounced Wed-NES-day with a d sound; the d is silent."),
    _w("women", "WIM-in", "Pronounced WOH-men like the singular woman."),
    _w("world", "wurld", "Pronounced wor-ld as two clear syllables; the l is barely heard."),
    _w("yacht", "yot", "Pronounced yatch-t; the ch is silent."),
]

SILENT_LETTERS = [
    {"word": "comfortable", "silent": "o", "phonetic": "KUMF-tuh-bl", "note": "Only three syllables — the middle o is not pronounced."},
    {"word": "Wednesday", "silent": "d", "phonetic": "WENZ-day", "note": "Sounds like Wenz-day; the first d is silent."},
    {"word": "island", "silent": "s", "phonetic": "EYE-luhnd", "note": "Not IS-land; the s is never pronounced."},
    {"word": "receipt", "silent": "p", "phonetic": "ri-SEET", "note": "The p is silent, like in doubt and subtle."},
    {"word": "subtle", "silent": "b", "phonetic": "SUT-ul", "note": "The b is silent; same pattern as debt and doubt."},
    {"word": "debt", "silent": "b", "phonetic": "det", "note": "Rhymes with bet; the b is never sounded."},
    {"word": "salmon", "silent": "l", "phonetic": "SAM-un", "note": "The l is silent — SAM-un."},
    {"word": "yacht", "silent": "ch", "phonetic": "yot", "note": "Rhymes with hot; ch is silent."},
    {"word": "colonel", "silent": "lo", "phonetic": "KUR-nl", "note": "Spelling does not match sound; it rhymes with kernel."},
    {"word": "cupboard", "silent": "p", "phonetic": "KUB-urd", "note": "Sounds like cub-urd; the p is silent."},
    {"word": "often", "silent": "t (BrE)", "phonetic": "OFF-en", "note": "In BrE the t is often dropped; saying off-TEN is a common overcorrection."},
    {"word": "clothes", "silent": "th spelling", "phonetic": "klohz", "note": "Rhymes with nose; the th spelling is not pronounced as /θ/."},
]

TRICKY_WORD_ENDINGS = [
    {
        "key": "ed",
        "title": "-ed endings",
        "intro": "Past tense -ed is pronounced three ways in English. Listen for the final sound of the verb stem.",
        "rules": [
            {
                "sound": "/t/",
                "when": "After voiceless sounds (p, k, f, s, ch, sh)",
                "examples": ["walked", "asked", "finished", "watched"],
            },
            {
                "sound": "/d/",
                "when": "After voiced sounds (vowels, b, g, l, m, n, r, v, z)",
                "examples": ["played", "loved", "cleaned", "called"],
            },
            {
                "sound": "/ɪd/",
                "when": "After /t/ or /d/ — adds a full extra syllable",
                "examples": ["wanted", "needed", "started", "decided"],
            },
        ],
    },
    {
        "key": "s",
        "title": "-s / -es endings",
        "intro": "Plural and third-person -s also follow the final consonant sound of the word.",
        "rules": [
            {
                "sound": "/s/",
                "when": "After voiceless sounds (p, t, k, f)",
                "examples": ["cats", "maps", "books", "graphs"],
            },
            {
                "sound": "/z/",
                "when": "After voiced sounds (most consonants and vowels)",
                "examples": ["dogs", "trees", "jobs", "lives"],
            },
            {
                "sound": "/ɪz/",
                "when": "After sibilant endings (s, z, sh, ch, j, x)",
                "examples": ["buses", "watches", "judges", "boxes"],
            },
        ],
    },
]

MINIMAL_PAIRS = [
    {
        "title": "Short /ɪ/ vs long /iː/",
        "pairs": [
            {"a": "ship", "b": "sheep", "note": "/ɪ/ is shorter and more relaxed; /iː/ is longer and tenser."},
            {"a": "live", "b": "leave", "note": "live (verb) has /ɪ/; leave has /iː/."},
            {"a": "bit", "b": "beat", "note": "A common vowel confusion for many L1 backgrounds."},
        ],
    },
    {
        "title": "Voiceless /θ/ vs voiced /ð/",
        "pairs": [
            {"a": "thin", "b": "then", "note": "/θ/ has no voice; /ð/ vibrates in the throat."},
            {"a": "think", "b": "this", "note": "Many learners replace both with /s/ or /z/ — practise the difference."},
            {"a": "mouth", "b": "mooth (smooth)", "note": "mouth ends with /θ/; smooth has /ð/ in the middle."},
        ],
    },
    {
        "title": "/ɜː/ vs /ɔː/ (work vs walk)",
        "pairs": [
            {"a": "work", "b": "walk", "note": "work has /ɜː/; walk has /ɔː/ — different vowels, not the same sound."},
            {"a": "bird", "b": "board", "note": "bird uses /ɜː/; board uses /ɔː/."},
            {"a": "hurt", "b": "hot", "note": "hurt has /ɜː/; hot has a short /ɒ/ in BrE."},
        ],
    },
    {
        "title": "/æ/ vs /ʌ/ (cat vs cut)",
        "pairs": [
            {"a": "cat", "b": "cut", "note": "/æ/ is more open (cat); /ʌ/ is central and shorter (cut)."},
            {"a": "hat", "b": "hut", "note": "Watch the vowel in fast speech — they are not interchangeable."},
            {"a": "bank", "b": "buck", "note": "Useful for accuracy in common topic words."},
        ],
    },
]
