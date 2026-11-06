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

import re

from ctx.tokenizer import approx_tokens

PROBES = ["midday", "tablespoon per litre", "canes to the railing",
          "5 litre", "cordon"]
PINNED_MARKERS = ["tap drips", "5 litre", "cordon", "20 pounds",
                  "potash"]


def render(turns):
    return "\n".join(f"{t['role']}: {t['text']}" for t in turns)


def keep_all(turns):
    return render(turns)


def truncate_old(turns, keep=8):
    return render(turns[-keep:])


def rolling_notes(turns, pinned):
    """Extractive notes: the first sentence of every turn, plus a
    pinned facts block. The stand-in note taker of this course."""
    notes = []
    for t in turns:
        first = re.split(r"(?<=[.!?])\s+", t["text"])[0]
        notes.append(f"{t['role']}: {first}")
    notes.append("PINNED FACTS:")
    notes += [f"- {p}" for p in pinned]
    return "\n".join(notes)


def survival(text, markers):
    return sum(1 for m in markers if m in text)


def evaluate():
    conv = load("conversation.json")
    turns, pinned = conv["turns"], conv["pinned_facts"]
    out = {}
    for name, fn in (("keep_all", keep_all),
                     ("truncate_last_8", truncate_old),
                     ("rolling_notes", None)):
        text = fn(turns) if fn else rolling_notes(turns, pinned)
        out[name] = {"tokens": approx_tokens(text),
                     "probes_survived": survival(text, PROBES),
                     "probes_total": len(PROBES),
                     "pinned_survived": survival(text, PINNED_MARKERS),
                     "pinned_total": len(PINNED_MARKERS)}
    return out


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(k, v)
