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

import math
import re
from collections import Counter

from ctx import standin
from ctx.assemble import segment
from ctx.tokenizer import approx_tokens

SYSTEM = ("# Role\nFernhill support assistant.\n\n# Rules\n"
          "- RULE: Answer only from the knowledge base provided.\n"
          "- RULE: If the knowledge base does not say, say so plainly.\n"
          "- RULE: Never invent prices, times, or policies.")
RETRIEVAL_BUDGET = 900


def words(text):
    return re.findall(r"[a-z]+", text.lower())


class Tfidf:
    def __init__(self, docs):
        df = Counter()
        self.tfs = {}
        for d in docs:
            w = words(d["text"])
            self.tfs[d["id"]] = Counter(w)
            df.update(set(w))
        n = len(docs)
        self.idf = {w: math.log(n / c) for w, c in df.items()}

    def score(self, question, doc_id):
        qw = set(words(question))
        tf = self.tfs[doc_id]
        return sum((1 + math.log(tf[w])) * self.idf[w]
                   for w in qw if w in tf)


def select_docs(docs, tfidf, question, budget=RETRIEVAL_BUDGET,
                score_floor_ratio=0.25):
    """Greedy by TF-IDF score under the budget, with a relevance
    floor: a document scoring below score_floor_ratio times the
    top score is not added. The floor is the Lesson 31 hardening:
    as first built (floor 0) the selector spent the whole budget
    on weak documents and failed the precision gate."""
    ranked = sorted(docs, key=lambda d: -tfidf.score(question, d["id"]))
    top = tfidf.score(question, ranked[0]["id"]) if ranked else 0
    chosen, used = [], 0
    for d in ranked:
        if tfidf.score(question, d["id"]) < score_floor_ratio * top:
            continue
        cost = approx_tokens(d["text"])
        if used + cost <= budget:
            chosen.append(d)
            used += cost
    return chosen


def assemble(task, chosen, order="desc"):
    segs = [segment("system", SYSTEM, kind="instruction")]
    docs = list(chosen)
    if order == "edges" and len(docs) >= 3:
        docs = [docs[0]] + docs[2:] + [docs[1]]
    segs += [segment(d["id"], d["text"],
                     [f["id"] for f in d["facts"]]) for d in docs]
    segs.append(segment("user", task["question"], kind="instruction"))
    return segs


def evaluate(order="desc", score_floor_ratio=0.25):
    docs = load("documents.json")
    tasks = load("tasks.json")
    tfidf = Tfidf(docs)
    rows = []
    for task in tasks:
        chosen = select_docs(docs, tfidf, task["question"],
                             score_floor_ratio=score_floor_ratio)
        segs = assemble(task, chosen, order=order)
        r = standin.recall(segs, task["required_facts"], trials=20)
        have = {f["id"] for d in chosen for f in d["facts"]}
        rel = sum(approx_tokens(d["text"]) for d in chosen
                  if d["id"] in task["relevant_docs"])
        rows.append({"task": task["id"], "recall": r["recall"],
                     "coverage": len(set(task["required_facts"])
                                     & have) / len(task["required_facts"]),
                     "total_tokens": r["total_tokens"],
                     "precision": round(rel / r["total_tokens"], 4),
                     "docs_selected": len(chosen)})
    n = len(rows)
    return {"per_task": rows,
            "mean_recall": round(sum(r["recall"] for r in rows) / n, 4),
            "mean_coverage": round(sum(r["coverage"] for r in rows) / n, 4),
            "worst_task_recall": min(r["recall"] for r in rows),
            "mean_total_tokens": round(sum(r["total_tokens"]
                                           for r in rows) / n),
            "mean_precision": round(sum(r["precision"] for r in rows)
                                    / n, 4)}


if __name__ == "__main__":
    r = evaluate()
    for row in r["per_task"]:
        print(row)
    for k, v in r.items():
        if k != "per_task":
            print(k, v)
