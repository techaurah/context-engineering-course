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


def words(text):
    return set(re.findall(r"[a-z]+", text.lower()))


def score(question, doc):
    qw = words(question)
    dw = words(doc["title"] + " " + doc["text"])
    return len(qw & dw)


def evaluate():
    docs = load("documents.json")
    tasks = load("tasks.json")
    per_k = {1: 0, 2: 0, 3: 0, 5: 0}
    for task in tasks:
        ranked = sorted(docs, key=lambda d: -score(task["question"], d))
        for k in per_k:
            top = {d["id"] for d in ranked[:k]}
            if set(task["relevant_docs"]) <= top:
                per_k[k] += 1
    n = len(tasks)
    return {"tasks": n,
            "relevant_in_top_k": per_k,
            "recall_at_3": round(per_k[3] / n, 4),
            "recall_at_5": round(per_k[5] / n, 4)}


if __name__ == "__main__":
    r = evaluate()
    print("tasks:", r["tasks"])
    for k, v in r["relevant_in_top_k"].items():
        print(f"top {k}: relevant doc present for {v} tasks")
