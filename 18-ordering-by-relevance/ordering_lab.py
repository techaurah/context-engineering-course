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

# The metric here is not "did the needed fact survive" (Lesson 05
# covers that) but "how much of what you paid to include gets
# used at all": the mean stand-in use rate over EVERY fact in the
# assembled context. Ordering cannot create signal, but it
# decides which documents' facts land in the cheap seats.


def words(text):
    return set(re.findall(r"[a-z]+", text.lower()))


def order_edges(ranked):
    out, rest = [], list(ranked)
    if rest:
        out.append(rest.pop(0))
    tail = []
    while rest:
        tail.append(rest.pop(0))
        if rest:
            out.append(rest.pop(0))
    return out + tail[::-1]


def evaluate():
    docs = load("documents.json")
    tasks = load("tasks.json")
    strategies = {"relevance_desc": lambda r: r,
                  "relevance_asc": lambda r: r[::-1],
                  "edges": order_edges}
    totals = {name: [] for name in strategies}
    for task in tasks:
        ranked = sorted(
            docs, key=lambda d: -len(words(task["question"])
                                     & words(d["text"])))
        for name, fn in strategies.items():
            ordered = fn(ranked)
            segs = [segment(d["id"], d["text"],
                            [f["id"] for f in d["facts"]])
                    for d in ordered]
            all_facts = [f["id"] for d in ordered for f in d["facts"]]
            r = standin.recall(segs, all_facts, trials=20)
            totals[name].append(r["recall"])
    return {name: round(sum(v) / len(v), 4)
            for name, v in totals.items()} | {"tasks": len(tasks),
                                              "docs_per_context": 18}


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(k, v)
