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

# The stand-in summarizer: a labelled, deterministic heuristic
# stand-in for a model written summary. It keeps the first
# sentence of the text, any sentence containing a number, and the
# last sentence, then joins them. It does not understand the
# text. The lesson measures what that costs.

QUERY = "when should I water, and how do I know the soil needs it?"


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text)
            if s.strip()]


def standin_summary(text):
    sents = sentences(text)
    keep = []
    for i, s in enumerate(sents):
        if i == 0 or i == len(sents) - 1 or re.search(r"\d", s):
            keep.append(s)
    return " ".join(keep)


def words(text):
    return set(re.findall(r"[a-z]+", text.lower()))


def extractive_for_query(text, query, budget_ratio=0.45):
    sents = sentences(text)
    qw = words(query)
    scored = sorted(range(len(sents)),
                    key=lambda i: -len(qw & words(sents[i])))
    budget = int(approx_tokens(text) * budget_ratio)
    chosen, used = [], 0
    for i in scored:
        cost = approx_tokens(sents[i])
        if used + cost <= budget:
            chosen.append(i)
            used += cost
    return " ".join(sents[i] for i in sorted(chosen))


def retention(summary, key_facts):
    return sum(1 for f in key_facts if f in summary)


def evaluate():
    t = [x for x in load("texts.json")
         if x["id"] == "text-watering-guide"][0]
    summ = standin_summary(t["text"])
    ext = extractive_for_query(t["text"], QUERY)
    total = len(t["key_facts"])
    return {"key_facts_total": total,
            "summary_tokens": approx_tokens(summ),
            "summary_facts_kept": retention(summ, t["key_facts"]),
            "extractive_tokens": approx_tokens(ext),
            "extractive_facts_kept": retention(ext, t["key_facts"]),
            "original_tokens": approx_tokens(t["text"]),
            "summary_dropped": [f for f in t["key_facts"]
                                if f not in summ]}


if __name__ == "__main__":
    r = evaluate()
    for k, v in r.items():
        print(k, v)
