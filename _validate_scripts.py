"""Check every Listening answer for Tests 2-5 is actually spoken in its script."""
import re
import importlib.util
from pathlib import Path

BASE = Path(__file__).resolve().parent / "practice_test" / "tests_content"


def load(name):
    spec = importlib.util.spec_from_file_location(name, BASE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


variety = load("listening_variety")
scripts = load("listening_scripts").SCRIPTS

TESTS = {
    2: variety.TEST2_LISTENING,
    3: variety.TEST3_LISTENING,
    4: variety.TEST4_LISTENING,
    5: variety.TEST5_LISTENING,
}

TEXT_TYPES = {"form", "note", "sentence", "table", "gap"}


def norm(s):
    return re.sub(r"[^a-z0-9 ]", " ", s.lower())


problems = []
for n, data in TESTS.items():
    for sec in data["sections"]:
        snum = sec["number"]
        lines = scripts.get((n, snum))
        if not lines:
            problems.append(f"T{n} S{snum}: NO SCRIPT")
            continue
        text = norm(" ".join(t for _, t in lines))
        for q in sec["questions"]:
            qt = q["type"]
            ans = q.get("answer")
            if qt in TEXT_TYPES:
                cands = ans if isinstance(ans, list) else [ans]
                ok = False
                numeric = False
                for c in cands:
                    cs = str(c)
                    if re.search(r"\d|:", cs):
                        numeric = True
                    if norm(cs).strip() and norm(cs).strip() in text:
                        ok = True
                        break
                if not ok and not numeric:
                    problems.append(f"T{n} S{snum} {q['id']} [{qt}]: MISSING '{ans}'")
                elif not ok and numeric:
                    problems.append(f"T{n} S{snum} {q['id']} [{qt}]: numeric/time '{ans}' (verify manually)")
            elif qt == "short":
                kws = q.get("answer_keywords", [])
                if not any(norm(k).strip() in text for k in kws):
                    problems.append(f"T{n} S{snum} {q['id']} [short]: no keyword present {kws}")
            elif qt in {"mcq", "matching", "map"}:
                # best-effort cue check on the descriptive part of the option
                opt = re.sub(r"^[A-H]\s+", "", str(ans)).strip()
                words = [w for w in norm(opt).split() if len(w) > 3]
                hit = sum(1 for w in words if w in text)
                if qt != "map" and words and hit == 0:
                    problems.append(f"T{n} S{snum} {q['id']} [{qt}]: option cue not found '{ans}'")

if problems:
    print("ISSUES FOUND:")
    for p in problems:
        print("  -", p)
else:
    print("ALL ANSWERS ANSWERABLE from scripts.")
print(f"\nTotal issues: {len(problems)}")
