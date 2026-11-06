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
from ctx.tokenizer import approx_tokens

# The target document sits in the MIDDLE of the context, half the
# padding before it and half after, so this lesson isolates the
# size effect (rot) from the position effect (Lesson 05). Padding
# cycles the other fixture documents, the way real contexts repeat
# boilerplate, templates, and earlier tool output.


def padded_context(target, others, pad_tokens):
    segs, used, i = [], 0, 0
    before = []
    while used < pad_tokens / 2:
        d = others[i % len(others)]
        before.append(segment("pad-b%d" % i, d["text"],
                              [f["id"] for f in d["facts"]]))
        used += approx_tokens(d["text"])
        i += 1
    segs.extend(before)
    segs.append(segment(target["id"], target["text"],
                        [f["id"] for f in target["facts"]]))
    used_after = 0
    j = 0
    while used_after < pad_tokens / 2:
        d = others[(i + j) % len(others)]
        segs.append(segment("pad-a%d" % j, d["text"],
                            [f["id"] for f in d["facts"]]))
        used_after += approx_tokens(d["text"])
        j += 1
    return segs


def evaluate():
    docs = load("documents.json")
    task = [t for t in load("tasks.json")
            if t["id"] == "task-delivery-cost"][0]
    by_id = {d["id"]: d for d in docs}
    target = by_id["doc-delivery"]
    others = [d for d in docs if d["id"] != "doc-delivery"]
    curve = {}
    for pad in (0, 1000, 2000, 4000, 6000, 8000):
        segs = padded_context(target, others, pad)
        r = standin.recall(segs, task["required_facts"], trials=20)
        curve[pad] = {"total_tokens": r["total_tokens"],
                      "recall": r["recall"]}
    recalls = [curve[p]["recall"] for p in sorted(curve)]
    return {"curve": curve,
            "recall_no_padding": recalls[0],
            "recall_max_padding": recalls[-1],
            "rot_drop": round(recalls[0] - recalls[-1], 4),
            "monotone_nonincreasing": all(
                a >= b for a, b in zip(recalls, recalls[1:]))}


if __name__ == "__main__":
    r = evaluate()
    for pad, v in r["curve"].items():
        print(f"padding {pad:5d}: total {v['total_tokens']:5d} tokens, "
              f"recall {v['recall']}")
    print("rot drop:", r["rot_drop"])
