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

# A strict standin extractor stands in for the model: it reads
# labelled fields reliably and flowing prose unreliably. That
# asymmetry is the property this lesson measures; it is labelled
# a stand-in, not a claim about any real model.

RECORDS = [
    {"order": "FH-1041", "customer": "Priya Shah", "item": "compost 40L",
     "qty": "3", "total": "36.00"},
    {"order": "FH-1042", "customer": "Tom Ellery", "item": "workshop place",
     "qty": "2", "total": "70.00"},
    {"order": "FH-1043", "customer": "Ana Ruiz", "item": "gift card",
     "qty": "1", "total": "50.00"},
    {"order": "FH-1044", "customer": "Ben Okafor", "item": "tool hire day",
     "qty": "1", "total": "25.00"},
]
FIELDS = ["order", "customer", "item", "qty", "total"]


def as_prose(r):
    return (f"Order {r['order']} was placed by {r['customer']}, who "
            f"bought {r['qty']} x {r['item']} coming to a total of "
            f"{r['total']} pounds all together.")


def as_list(r):
    return "\n".join(f"- {k}: {r[k]}" for k in FIELDS)


def as_tagged(r):
    return "\n".join(f"<{k}>{r[k]}</{k}>" for k in FIELDS)


def extract_labelled(text):
    out = {}
    for k in FIELDS:
        m = re.search(rf"(?:- {k}:|<{k}>)\s*([^\n<]+)", text)
        if m:
            out[k] = m.group(1).strip()
    return out


def extract_prose(text):
    out = {}
    m = re.search(r"Order (\S+) was placed by ([^,]+), who bought "
                  r"(\d+) x (.+?) coming to", text)
    if m:
        out = {"order": m.group(1), "customer": m.group(2),
               "qty": m.group(3), "item": m.group(4)}
    # The prose buries the total after "total of"; the strict
    # extractor only accepts it in final position, and here it is
    # mid-sentence, so the field is missed. That miss is the
    # measured cost of prose.
    return out


def evaluate():
    results = {}
    for name, fmt, ext in (("prose", as_prose, extract_prose),
                           ("list", as_list, extract_labelled),
                           ("tagged", as_tagged, extract_labelled)):
        correct = 0
        tokens = 0
        from ctx.tokenizer import approx_tokens
        for r in RECORDS:
            text = fmt(r)
            tokens += approx_tokens(text)
            got = ext(text)
            correct += sum(1 for k in FIELDS if got.get(k) == r[k])
        results[name] = {"fields_correct": correct,
                         "fields_total": len(RECORDS) * len(FIELDS),
                         "tokens": tokens}
    return results


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(k, v)
