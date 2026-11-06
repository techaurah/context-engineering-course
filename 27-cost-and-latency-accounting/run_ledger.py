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

from ctx.assemble import BudgetLedger
from ctx.tokenizer import approx_tokens

# A simulated 12 step support run. Step shapes are taken from the
# course's own measurements: a raw search result costs what
# Lesson 25 measured for the verbose schema, a filtered one what
# it measured for the compact schema. Prices are the Lesson 26
# illustrative constants, labelled again here: 1.00 unit per 1000
# fresh input tokens. This is accounting practice, not a bill.
RAW_RESULT = 205
COMPACT_RESULT = 75
SYSTEM_TOOLS = 141
QUESTION = 30
REPLY = 55


def run(result_cost):
    ledger = BudgetLedger(10 ** 9)
    history = 0
    for step in range(12):
        ledger.charge("system_and_tools", SYSTEM_TOOLS)
        ledger.charge("history_replay", history)
        ledger.charge("tool_results", result_cost)
        ledger.charge("question", QUESTION)
        history += QUESTION + REPLY + result_cost // 4
    report = ledger.report()
    total = report["TOTAL"]
    shares = {k: round(v / total, 3) for k, v in report.items()
              if k not in ("TOTAL", "REMAINING")}
    return {"total_tokens": total, "shares": shares,
            "cost_units": round(total / 1000 * 1.00, 3),
            "dominant_component": max(shares, key=shares.get)}


def evaluate():
    raw = run(RAW_RESULT)
    compact = run(COMPACT_RESULT)
    return {"raw_results": raw, "compact_results": compact,
            "saving_units": round(raw["cost_units"]
                                  - compact["cost_units"], 3),
            "saving_ratio": round(compact["total_tokens"]
                                  / raw["total_tokens"], 4)}


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(k, v)
