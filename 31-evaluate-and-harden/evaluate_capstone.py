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

import importlib.util

PIPE = os.path.join(ROOT, "30-build-the-capstone-pipeline",
                    "context_pipeline.py")
GATES = os.path.join(ROOT, "29-capstone-spec", "capstone",
                     "gates.json")


def load_pipeline():
    spec = importlib.util.spec_from_file_location("pipeline", PIPE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check(metrics, gates):
    return {
        "mean_required_fact_recall_min": metrics["mean_recall"]
        >= gates["mean_required_fact_recall_min"],
        "fact_coverage_min": metrics["mean_coverage"]
        >= gates["fact_coverage_min"],
        "worst_task_recall_min": metrics["worst_task_recall"]
        >= gates["worst_task_recall_min"],
        "mean_total_tokens_max": metrics["mean_total_tokens"]
        <= gates["mean_total_tokens_max"],
        "mean_precision_min": metrics["mean_precision"]
        >= gates["mean_precision_min"],
    }


def baseline():
    """The pre-course assembly: wall prompt, every document,
    question last. Measured with the same harness."""
    from ctx import standin
    from ctx.assemble import segment
    from ctx.tokenizer import approx_tokens
    docs = load("documents.json")
    tasks = load("tasks.json")
    wall = ("You are the Fernhill support assistant and you should "
            "answer questions from the knowledge base and be "
            "helpful and keep in mind all the policies in the "
            "documents that follow and never invent anything.")
    rows = []
    for task in tasks:
        segs = [segment("system", wall, kind="instruction")]
        segs += [segment(d["id"], d["text"],
                         [f["id"] for f in d["facts"]]) for d in docs]
        segs.append(segment("user", task["question"],
                            kind="instruction"))
        r = standin.recall(segs, task["required_facts"], trials=20)
        rel = sum(approx_tokens(d["text"]) for d in docs
                  if d["id"] in task["relevant_docs"])
        rows.append({"recall": r["recall"],
                     "total_tokens": r["total_tokens"],
                     "precision": rel / r["total_tokens"]})
    n = len(rows)
    return {"mean_recall": round(sum(r["recall"] for r in rows) / n, 4),
            "mean_total_tokens": round(sum(r["total_tokens"]
                                           for r in rows) / n),
            "mean_precision": round(sum(r["precision"] for r in rows)
                                    / n, 4)}


def evaluate():
    with open(GATES) as f:
        gates = json.load(f)["capstone_pipeline"]["gates"]
    pipe = load_pipeline()
    v_as_built = pipe.evaluate(order="desc", score_floor_ratio=0.0)
    checks_as_built = check(v_as_built, gates)
    # Hardening, driven by the as-built failure: a relevance floor
    # on selection (Lesson 30 documents it). Both orderings are
    # re-measured with the floor in place; nothing is hidden, the
    # as-built numbers stay in this output.
    v_desc = pipe.evaluate(order="desc", score_floor_ratio=0.25)
    v_edges = pipe.evaluate(order="edges", score_floor_ratio=0.25)
    checks_desc = check(v_desc, gates)
    checks_edges = check(v_edges, gates)
    winner = "edges" if sum(checks_edges.values()) \
        > sum(checks_desc.values()) else "desc"
    winning = v_edges if winner == "edges" else v_desc
    winning_checks = checks_edges if winner == "edges" else checks_desc
    slim = lambda v: {k: x for k, x in v.items() if k != "per_task"}
    return {"gates": gates,
            "as_built": slim(v_as_built),
            "as_built_gate_results": checks_as_built,
            "as_built_gates_passed": sum(checks_as_built.values()),
            "variant_desc": slim(v_desc),
            "variant_edges": slim(v_edges),
            "winning_variant": winner,
            "gate_results": winning_checks,
            "gates_passed": sum(winning_checks.values()),
            "gates_total": len(winning_checks),
            "baseline": baseline(),
            "ship": all(winning_checks.values())}


if __name__ == "__main__":
    r = evaluate()
    print("baseline:", r["baseline"])
    print("as built (no relevance floor):", r["as_built"])
    print("as-built gates passed:", r["as_built_gates_passed"],
          "of", r["gates_total"])
    print("desc:   ", r["variant_desc"])
    print("edges:  ", r["variant_edges"])
    print("winner:", r["winning_variant"])
    for k, v in r["gate_results"].items():
        print(("PASS" if v else "FAIL"), k)
    print(f"gates passed: {r['gates_passed']} of {r['gates_total']}")
    print("ship:", r["ship"])
