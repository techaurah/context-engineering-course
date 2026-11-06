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


def evaluate():
    budgets = load("budgets.json")
    conv = load("conversation.json")
    window = budgets["window_tokens"]
    reserve = budgets["reserve_output_tokens"]
    allowance = budgets["components"]
    ledger = BudgetLedger(window)
    for comp in ("system", "tools", "memory", "retrieval"):
        ledger.charge(comp, allowance[comp])
    # History grows turn by turn through the scripted conversation,
    # then cycles it a second time to model a long session.
    turns = conv["turns"] + conv["turns"]
    history_tokens = 0
    allowance_breaks_at = None
    window_breaks_at = None
    for i, t in enumerate(turns):
        history_tokens += approx_tokens(f"{t['role']}: {t['text']}")
        if (allowance_breaks_at is None
                and history_tokens > allowance["history"]):
            allowance_breaks_at = i + 1
        total = ledger.used - ledger.spent.get("history", 0) \
            + history_tokens
        if window_breaks_at is None and total > window - reserve:
            window_breaks_at = i + 1
    ledger.charge("history", history_tokens)
    return {"window": window, "reserve": reserve,
            "history_allowance": allowance["history"],
            "history_after_48_turns": history_tokens,
            "allowance_breaks_at_turn": allowance_breaks_at,
            "window_breaks_at_turn": window_breaks_at,
            "final_report": ledger.report(),
            "over_budget": ledger.over_budget()}


if __name__ == "__main__":
    r = evaluate()
    for k, v in r.items():
        print(k, v)
