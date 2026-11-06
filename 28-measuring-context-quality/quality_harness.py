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

from ctx import standin
from ctx.assemble import segment
from ctx.tokenizer import approx_tokens

SYSTEM = ("You are the Fernhill support assistant. Answer only "
          "from the knowledge base. Say so when it does not say.")


def words(text):
    return set(re.findall(r"[a-z]+", text.lower()))


def assemble(task, chosen):
    segs = [segment("system", SYSTEM, kind="instruction")]
    segs += [segment(d["id"], d["text"],
                     [f["id"] for f in d["facts"]]) for d in chosen]
    segs.append(segment("user", task["question"], kind="instruction"))
    return segs


def measure(task, chosen):
    segs = assemble(task, chosen)
    r = standin.recall(segs, task["required_facts"], trials=20)
    rel_tokens = sum(approx_tokens(d["text"]) for d in chosen
                     if d["id"] in task["relevant_docs"])
    return {"recall": r["recall"], "total_tokens": r["total_tokens"],
            "precision": round(rel_tokens / r["total_tokens"], 4)}


def evaluate():
    docs = load("documents.json")
    tasks = load("tasks.json")
    strategies = {
        "preload_all": lambda t: docs,
        "overlap_top3": lambda t: sorted(
            docs, key=lambda d: -len(words(t["question"])
                                     & words(d["text"])))[:3],
        "overlap_top2": lambda t: sorted(
            docs, key=lambda d: -len(words(t["question"])
                                     & words(d["text"])))[:2],
    }
    out = {}
    for name, pick in strategies.items():
        rows = [measure(t, pick(t)) for t in tasks]
        out[name] = {
            "mean_recall": round(sum(r["recall"] for r in rows)
                                 / len(rows), 4),
            "mean_tokens": round(sum(r["total_tokens"] for r in rows)
                                 / len(rows)),
            "mean_precision": round(sum(r["precision"] for r in rows)
                                    / len(rows), 4)}
    return out


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(k, v)
