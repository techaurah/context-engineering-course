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

import os

GATES_PATH = os.path.join(HERE, "capstone", "gates.json")


def evaluate():
    with open(GATES_PATH) as f:
        spec = json.load(f)["capstone_pipeline"]
    gates = spec["gates"]
    tasks = load("tasks.json")
    docs = load("documents.json")
    checks = {
        "gates_named": len(gates),
        "has_recall_gate": "mean_required_fact_recall_min" in gates,
        "has_token_gate": "mean_total_tokens_max" in gates,
        "tasks_in_scenario": len(tasks),
        "documents_in_scenario": len(docs),
        "fixed_before_build": spec["fixed_before_build"],
    }
    return {"gates": gates, "checks": checks}


if __name__ == "__main__":
    r = evaluate()
    print("Gates fixed in advance:")
    for k, v in r["gates"].items():
        print(f"  {k}: {v}")
    for k, v in r["checks"].items():
        print(k, v)
