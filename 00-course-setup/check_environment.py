"""Lesson 00 artifact: verify the environment and survey the
shared instruments. Offline, standard library only.
Run: python3 check_environment.py
"""

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


def evaluate():
    docs = load("documents.json")
    tasks = load("tasks.json")
    conv = load("conversation.json")
    budgets = load("budgets.json")
    facts = sum(len(d["facts"]) for d in docs)
    required = sum(len(t["required_facts"]) for t in tasks)
    return {
        "python_ok": sys.version_info >= (3, 11),
        "python_version": "%d.%d" % sys.version_info[:2],
        "documents": len(docs),
        "facts": facts,
        "tasks": len(tasks),
        "required_fact_slots": required,
        "conversation_turns": len(conv["turns"]),
        "pinned_facts": len(conv["pinned_facts"]),
        "window_tokens": budgets["window_tokens"],
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
