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

BUDGET = 400


def words(text):
    return re.findall(r"[a-z]+", text.lower())


def tfidf_vectors(docs):
    df = Counter()
    tfs = []
    for d in docs:
        w = words(d["text"])
        tfs.append(Counter(w))
        df.update(set(w))
    n = len(docs)
    vecs = []
    for tf in tfs:
        vecs.append({w: (1 + math.log(c)) * math.log(n / df[w])
                     for w, c in tf.items()})
    return vecs


def cosine(a, b):
    dot = sum(v * b.get(w, 0.0) for w, v in a.items())
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def select(docs, scores, budget):
    chosen, used = [], 0
    for d in sorted(docs, key=lambda d: -scores[d["id"]]):
        cost = approx_tokens(d["text"])
        if used + cost <= budget:
            chosen.append(d)
            used += cost
    return chosen, used


def run(docs, tasks, scorer):
    fact_hits, fact_total, recalls = 0, 0, []
    for task in tasks:
        scores = {d["id"]: scorer(task, d) for d in docs}
        chosen, _used = select(docs, scores, BUDGET)
        have = {f["id"] for d in chosen for f in d["facts"]}
        fact_hits += len(set(task["required_facts"]) & have)
        fact_total += len(task["required_facts"])
        segs = [segment(d["id"], d["text"],
                        [f["id"] for f in d["facts"]]) for d in chosen]
        recalls.append(standin.recall(
            segs, task["required_facts"], trials=20)["recall"])
    return {"fact_coverage": round(fact_hits / fact_total, 4),
            "mean_standin_recall": round(sum(recalls) / len(recalls), 4)}


def evaluate():
    docs = load("documents.json")
    tasks = load("tasks.json")
    vecs = {d["id"]: v for d, v in zip(docs, tfidf_vectors(docs))}

    def overlap(task, d):
        qw = set(words(task["question"]))
        return len(qw & set(words(d["text"])))

    def tfidf(task, d):
        qw = Counter(words(task["question"]))
        qv = {w: 1.0 for w in qw}
        return cosine(qv, vecs[d["id"]])

    return {"budget_tokens": BUDGET,
            "overlap": run(docs, tasks, overlap),
            "tfidf": run(docs, tasks, tfidf)}


if __name__ == "__main__":
    r = evaluate()
    print("budget:", r["budget_tokens"])
    print("overlap:", r["overlap"])
    print("tfidf:  ", r["tfidf"])
