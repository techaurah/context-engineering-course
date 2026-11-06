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

RULE = ("rule-refund-window", "Refunds land three to five working "
        "days after the return is scanned.")
PAD_TO = 3000


def pad(docs, tokens, tag):
    segs, used, i = [], 0, 0
    while used < tokens:
        d = docs[i % len(docs)]
        segs.append(segment("%s%d" % (tag, i), d["text"],
                            [f["id"] for f in d["facts"]]))
        used += approx_tokens(d["text"])
        i += 1
    return segs


def evaluate():
    docs = load("documents.json")
    rule_seg = segment("rule", RULE[1], [RULE[0]], kind="instruction")
    variants = {
        "rule_at_start": [rule_seg] + pad(docs, PAD_TO, "p"),
        "rule_in_middle": pad(docs, PAD_TO // 2, "a") + [rule_seg]
        + pad(docs, PAD_TO // 2, "b"),
        "rule_middle_and_repeated_at_end":
            pad(docs, PAD_TO // 2, "a") + [rule_seg]
            + pad(docs, PAD_TO // 2, "b")
            + [segment("rule-repeat", RULE[1], [RULE[0]],
                       kind="instruction")],
    }
    out = {}
    for name, segs in variants.items():
        r = standin.recall(segs, [RULE[0]], trials=40)
        out[name] = {"rule_use_rate": r["per_fact"][RULE[0]],
                     "total_tokens": r["total_tokens"]}
    out["extra_tokens_for_repeat"] = (
        out["rule_middle_and_repeated_at_end"]["total_tokens"]
        - out["rule_in_middle"]["total_tokens"])
    return out


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(k, v)
