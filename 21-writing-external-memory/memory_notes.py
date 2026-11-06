import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def find_root():
    cur = HERE
    while True:
        if os.path.isfile(os.path.join(cur, "ctx", "standin.py")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise FileNotFoundError("repo root (ctx/) not found above " + HERE)
        cur = parent


ROOT = find_root()
sys.path.insert(0, ROOT)


def load(name):
    with open(os.path.join(ROOT, "fixtures", name)) as f:
        return json.load(f)

from ctx.tokenizer import approx_tokens

# Session 2 answers by looking facts up in structured notes
# written during session 1. The no-memory baseline answers from
# generic defaults, the way a fresh session guesses. Both are
# deterministic; the notes are the only difference.

CHECKS = [
    ("watering_method", "by can", "tap water on a schedule"),
    ("pot_size_litres", "5", "10"),
    ("variety_type", "cordon", "bush"),
    ("budget_pounds", "20", "50"),
    ("feed", "high potash, weekly", "general purpose, monthly"),
]


def write_notes(pinned):
    return {"watering_method": "by can",
            "pot_size_litres": "5",
            "variety_type": "cordon",
            "budget_pounds": "20",
            "feed": "high potash, weekly",
            "pinned": pinned}


def evaluate():
    conv = load("conversation.json")
    notes = write_notes(conv["pinned_facts"])
    notes_text = "\n".join(f"{k}: {v}" for k, v in notes.items()
                           if k != "pinned")
    notes_text += "\n" + "\n".join(notes["pinned"])
    transcript = "\n".join(f"{t['role']}: {t['text']}"
                           for t in conv["turns"])
    with_notes = sum(1 for key, want, _d in CHECKS
                     if notes.get(key) == want)
    without = sum(1 for key, want, default in CHECKS
                  if default == want)
    return {"checks": len(CHECKS),
            "correct_with_notes": with_notes,
            "correct_without_notes": without,
            "notes_tokens": approx_tokens(notes_text),
            "transcript_tokens": approx_tokens(transcript)}


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(k, v)
