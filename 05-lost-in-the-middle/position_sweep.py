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

from ctx import standin
from ctx.assemble import segment


def evaluate():
    docs = load("documents.json")
    task = [t for t in load("tasks.json")
            if t["id"] == "task-loyalty-points"][0]
    by_id = {d["id"]: d for d in docs}
    target = by_id["doc-loyalty"]
    others = [d for d in docs if d["id"] != "doc-loyalty"][:9]
    curve = {}
    for pos in range(10):
        ordered = others[:pos] + [target] + others[pos:]
        segs = [segment(d["id"], d["text"],
                        [f["id"] for f in d["facts"]]) for d in ordered]
        r = standin.recall(segs, task["required_facts"], trials=20)
        curve[pos + 1] = r["recall"]
    vals = [curve[p] for p in sorted(curve)]
    middle = vals[4:6]
    return {"curve": curve,
            "recall_position_1": vals[0],
            "recall_position_10": vals[-1],
            "recall_middle_min": min(middle),
            "u_shape_gap": round(min(vals[0], vals[-1]) - min(middle), 4)}


if __name__ == "__main__":
    r = evaluate()
    for p, v in r["curve"].items():
        print(f"position {p:2d}: recall {v}")
    print("U-shape gap:", r["u_shape_gap"])
