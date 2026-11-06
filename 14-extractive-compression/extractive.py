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

QUERIES = {
    "text-watering-guide": "water morning mulch soil leaves disease check damp",
    "text-pruning-guide": "prune flowering shrubs third wisteria january july",
    "text-compost-guide": "green brown three parts heap damp food meat dairy",
}


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text)
            if s.strip()]


def words(text):
    return set(re.findall(r"[a-z]+", text.lower()))


def compress(text, query, budget_ratio=0.45):
    sents = sentences(text)
    qw = words(query)
    scored = sorted(range(len(sents)),
                    key=lambda i: -len(qw & words(sents[i])))
    total = approx_tokens(text)
    budget = int(total * budget_ratio)
    chosen, used = [], 0
    for i in scored:
        cost = approx_tokens(sents[i])
        if used + cost <= budget:
            chosen.append(i)
            used += cost
    return [sents[i] for i in sorted(chosen)], used, total


def evaluate():
    texts = load("texts.json")
    per_text = {}
    kept_all, total_all, facts_kept, facts_all = 0, 0, 0, 0
    for t in texts:
        chosen, used, total = compress(t["text"], QUERIES[t["id"]])
        joined = " ".join(chosen)
        kept = sum(1 for f in t["key_facts"] if f in joined)
        per_text[t["id"]] = {"sentences_kept": len(chosen),
                             "sentences_total": len(sentences(t["text"])),
                             "tokens_kept": used, "tokens_total": total,
                             "key_facts_kept": kept,
                             "key_facts_total": len(t["key_facts"])}
        kept_all += used
        total_all += total
        facts_kept += kept
        facts_all += len(t["key_facts"])
    return {"per_text": per_text,
            "compression_ratio": round(kept_all / total_all, 4),
            "key_fact_retention": round(facts_kept / facts_all, 4),
            "key_facts_kept": facts_kept, "key_facts_total": facts_all}


if __name__ == "__main__":
    r = evaluate()
    for k, v in r["per_text"].items():
        print(k, v)
    print("compression ratio:", r["compression_ratio"],
          "| key fact retention:", r["key_fact_retention"])
