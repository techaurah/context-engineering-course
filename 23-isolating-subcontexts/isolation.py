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

# Each sub-agent stand-in was given ONE sub-question and returns a
# summary line carrying only the fact that sub-question asked
# about. The final task, set by the coordinator afterwards, needs
# two facts nobody's sub-question mentioned. That gap, not the
# isolation itself, is what this lesson measures.

SUBQ = {
    "doc-trade": ("fh-trade-terms",
                  "Trade invoices are due 30 days after the invoice date."),
    "doc-delivery": ("fh-delivery-days",
                     "Deliveries run Tuesday to Friday."),
    "doc-compost": ("fh-compost-bulk",
                    "Bulk compost is sold by the cubic metre."),
}
# The final task: price a trade plant order with delivery. It
# needs the trade discount and the free delivery threshold.
FINAL_FACTS = ["fh-trade-discount", "fh-delivery-fee"]


def evaluate():
    docs = {d["id"]: d for d in load("documents.json")}
    single = [segment(d, docs[d]["text"],
                      [f["id"] for f in docs[d]["facts"]])
              for d in SUBQ]
    r_single = standin.recall(single, FINAL_FACTS, trials=20)
    summaries = [segment("sum-" + d, text, [fid])
                 for d, (fid, text) in SUBQ.items()]
    sub_facts = [fid for fid, _t in SUBQ.values()]
    r_iso_sub = standin.recall(summaries, sub_facts, trials=20)
    r_iso_final = standin.recall(summaries, FINAL_FACTS, trials=20)
    sub_tokens = sum(approx_tokens(docs[d]["text"]) for d in SUBQ)
    return {"single_context_tokens": r_single["total_tokens"],
            "single_final_task_recall": r_single["recall"],
            "isolated_subquestion_recall": r_iso_sub["recall"],
            "isolated_final_task_recall": r_iso_final["recall"],
            "isolated_combiner_tokens": r_iso_final["total_tokens"],
            "isolated_total_tokens_processed": sub_tokens
            + r_iso_final["total_tokens"]}


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(k, v)
