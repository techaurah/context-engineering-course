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


def stems(text):
    return {w[:5] for w in re.findall(r"[a-z]+", text.lower())
            if len(w) >= 4}


def build_index(docs, enriched):
    index = []
    for d in docs:
        keys = stems(d["title"] + " " + d["slug"])
        if enriched:
            content = Counter_words(d["text"])
            keys |= {w[:5] for w, _c in content.most_common(12)}
        index.append({"doc": d["id"], "keys": keys,
                      "line": f"{d['id']}: {d['title']}"})
    return index


def Counter_words(text):
    from collections import Counter
    stop = {"the", "a", "an", "and", "or", "of", "to", "in", "is",
            "are", "on", "for", "at", "fernhill"}
    return Counter(w for w in re.findall(r"[a-z]+", text.lower())
                   if len(w) >= 4 and w not in stop)


def jit_load(index, question, top=2):
    q = stems(question)
    scored = sorted(index, key=lambda e: -len(q & e["keys"]))
    return [e for e in scored[:top] if len(q & e["keys"]) >= 1]


def evaluate():
    docs = load("documents.json")
    tasks = load("tasks.json")
    by_id = {d["id"]: d for d in docs}
    preload_tokens = sum(approx_tokens(d["text"]) for d in docs)
    out = {"preload_all_tokens": preload_tokens}
    for name, enriched in (("title_index", False),
                           ("keyword_index", True)):
        index = build_index(docs, enriched)
        index_tokens = approx_tokens(
            "\n".join(e["line"] for e in index)) if not enriched else \
            approx_tokens("\n".join(
                e["line"] + " " + " ".join(sorted(e["keys"]))
                for e in index))
        hits, total, spent = 0, 0, []
        for task in tasks:
            loaded = jit_load(index, task["question"])
            spent.append(index_tokens + sum(
                approx_tokens(by_id[e["doc"]]["text"]) for e in loaded))
            have = {f["id"] for e in loaded
                    for f in by_id[e["doc"]]["facts"]}
            hits += len(set(task["required_facts"]) & have)
            total += len(task["required_facts"])
        out[name] = {"mean_tokens_per_task": round(
            sum(spent) / len(spent)),
            "fact_coverage": round(hits / total, 4),
            "facts_found": hits, "facts_total": total}
    return out


if __name__ == "__main__":
    r = evaluate()
    print("preload all:", r["preload_all_tokens"], "tokens, coverage 1.0")
    for name in ("title_index", "keyword_index"):
        print(name, r[name])
