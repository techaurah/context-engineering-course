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

# A labelled standin reader for layout: asked a question naming a
# topic, it looks for a heading matching that topic and reads the
# section under it. In a flat wall of text it falls back to the
# first sentence mentioning the topic word, which may be the
# wrong fact entirely. The asymmetry is the lesson.

SECTIONS = [
    ("delivery", "Deliveries run Tuesday to Friday, 9:00 to 17:30, "
                 "free over 75 pounds."),
    ("returns", "Plants come back within 14 days, goods within 30 "
                "days, refunds in three to five working days."),
    ("loyalty", "Members earn 2 points per pound, each point worth "
                "1 penny, points expire after 12 months."),
    ("cafe", "The cafe opens 8:30 to 16:00, Sundays 10:00 to 15:30, "
             "groups of 8 or more must book."),
    ("workshops", "Workshops cost 35 pounds, capped at 12 people, "
                  "booked at least 48 hours ahead."),
    ("trade", "Trade accounts get 15 percent off plants, invoices "
              "due in 30 days, no minimum spend."),
]
QUESTIONS = [
    ("delivery", "free over 75 pounds"),
    ("returns", "three to five working days"),
    ("loyalty", "expire after 12 months"),
    ("cafe", "10:00 to 15:30"),
    ("workshops", "48 hours ahead"),
    ("trade", "15 percent off plants"),
]
FILLER = ("Fernhill runs two centres with a cafe, a glasshouse, "
          "and a large outdoor plant area at each. ")


def flat_text():
    body = " ".join(text for _h, text in SECTIONS)
    return FILLER + body + " " + FILLER


def headed_text():
    return "\n".join(f"## {h}\n{text}" for h, text in SECTIONS)


def read_flat(text, topic):
    for sent in re.split(r"(?<=[.!?])\s+", text):
        if topic in sent.lower() and "," in sent:
            return sent
    return ""


def read_headed(text, topic):
    m = re.search(rf"## {topic}\n([^\n]+)", text)
    return m.group(1) if m else ""


def evaluate():
    flat, headed = flat_text(), headed_text()
    out = {}
    for name, text, reader in (("flat", flat, read_flat),
                               ("headed", headed, read_headed)):
        correct = 0
        for topic, expected in QUESTIONS:
            if expected in reader(text, topic):
                correct += 1
        out[name] = {"answers_correct": correct,
                     "of": len(QUESTIONS)}
    from ctx.tokenizer import approx_tokens
    out["flat_tokens"] = approx_tokens(flat)
    out["headed_tokens"] = approx_tokens(headed)
    return out


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(k, v)
