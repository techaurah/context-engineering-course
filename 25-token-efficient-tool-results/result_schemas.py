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


def words(text):
    return set(re.findall(r"[a-z]+", text.lower()))


def search(docs, question, top=3):
    qw = words(question)
    ranked = sorted(docs, key=lambda d: -len(qw & words(d["text"])))
    return [d for d in ranked[:top] if qw & words(d["text"])]


def verbose_result(doc):
    return {"id": doc["id"], "title": doc["title"], "slug": doc["slug"],
            "full_text": doc["text"], "fact_count": len(doc["facts"]),
            "source": "fernhill-kb", "version": 7, "reviewed": True}


def compact_result(doc, question):
    qw = words(question)
    lines = [f["text"] for f in doc["facts"]
             if words(f["text"]) & qw]
    return {"id": doc["id"], "facts": lines}


def evaluate():
    docs = load("documents.json")
    tasks = load("tasks.json")
    out = {"tasks": len(tasks)}
    for name, fmt in (("verbose", None), ("compact", None)):
        total_tokens, hits, total = 0, 0, 0
        for task in tasks:
            results = search(docs, task["question"])
            if name == "verbose":
                payload = [verbose_result(d) for d in results]
                have = {f["id"] for d in results for f in d["facts"]}
            else:
                payload = [compact_result(d, task["question"])
                           for d in results]
                by_id = {d["id"]: d for d in docs}
                have = set()
                for p in payload:
                    for f in by_id[p["id"]]["facts"]:
                        if f["text"] in p["facts"]:
                            have.add(f["id"])
            total_tokens += approx_tokens(json.dumps(payload))
            hits += len(set(task["required_facts"]) & have)
            total += len(task["required_facts"])
        out[name] = {"mean_tokens_per_task": round(total_tokens
                                                   / len(tasks)),
                     "fact_coverage": round(hits / total, 4)}
    return out


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(k, v)
