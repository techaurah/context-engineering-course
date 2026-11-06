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


def shingles(text, n=3):
    w = re.findall(r"[a-z]+", text.lower())
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 1.0


def variants(docs):
    """Retrieval in the wild returns near copies: same facts,
    lightly reworded wrapper text. One cafe copy is an older,
    shorter version that predates the dog policy fact."""
    out = []
    for d in docs:
        if d["slug"] in ("cafe", "delivery", "returns"):
            text = d["text"].replace("Fernhill", "The centre")
            facts = d["facts"]
            if d["slug"] == "cafe":
                text = text.replace(
                    " Dogs are welcome in the outdoor cafe seating only.", "")
                facts = [f for f in facts if f["id"] != "fh-cafe-dogs"]
            out.append({"id": d["id"] + "-copy", "text": text,
                        "facts": facts})
    return out


def dedup(docs, keep="first"):
    kept = []
    for d in docs:
        dup = None
        for k in kept:
            if jaccard(shingles(d["text"]), shingles(k["text"])) >= 0.5:
                dup = k
                break
        if dup is None:
            kept.append(d)
        elif keep == "longest" and len(d["text"]) > len(dup["text"]):
            kept[kept.index(dup)] = d
    return kept


def evaluate():
    docs = load("documents.json")
    # Retrieval order in the wild: the stale copies surface
    # first, the current documents after them.
    working = variants(docs) + docs
    total_before = sum(approx_tokens(d["text"]) for d in working)
    all_facts = {f["id"] for d in docs for f in d["facts"]}
    out = {"documents_before": len(working),
           "tokens_before": total_before}
    for policy in ("first", "longest"):
        kept = dedup(working, keep=policy)
        facts = {f["id"] for d in kept for f in d["facts"]}
        out[policy] = {
            "documents_after": len(kept),
            "tokens_after": sum(approx_tokens(d["text"]) for d in kept),
            "tokens_saved": total_before - sum(
                approx_tokens(d["text"]) for d in kept),
            "unique_facts_lost": len(all_facts - facts),
            "lost_fact_ids": sorted(all_facts - facts)}
    return out


if __name__ == "__main__":
    r = evaluate()
    print("before:", r["documents_before"], "docs,", r["tokens_before"],
          "tokens")
    for p in ("first", "longest"):
        print(p, r[p])
