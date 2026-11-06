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

from ctx.assemble import segment
from ctx.tokenizer import approx_tokens

# A labelled simulation of prefix caching, the mechanism behind
# most providers' prompt cache discounts: if this turn's context
# starts with exactly the same tokens as last turn's, the shared
# prefix is billed at the cached rate. Prices below are local
# illustrative constants (1.00 per 1000 fresh tokens, 0.10 per
# 1000 cached tokens), NOT any provider's price list.
PRICE_FRESH = 1.00
PRICE_CACHED = 0.10

SYSTEM = ("You are the Fernhill support assistant. Answer only "
          "from the knowledge base. Say so when it does not say.")
TOOLS = "Tools: search, order_status, book, stock, escalate."
MEMORY = "Customer: Gold loyalty member, prefers Tuesdays."


def turns(docs, conv, churn):
    history = []
    for i, t in enumerate(conv["turns"]):
        history.append(f"{t['role']}: {t['text']}")
        stamp = f" [session tick {i}]" if churn else ""
        if not churn:
            head = [SYSTEM, TOOLS, MEMORY]
        else:
            # Churn: a per-turn timestamp inside the system text
            # AND a section order that rotates turn by turn, the
            # two habits that break prefix matching in real logs.
            base = [SYSTEM + stamp, TOOLS, MEMORY]
            r = i % 3
            head = base[r:] + base[:r]
        segs = head + ["\n".join(history[-6:]),
                       docs[i % len(docs)]["text"]]
        yield [approx_tokens(s) for s in segs], segs


def run(churn):
    docs = load("documents.json")
    conv = load("conversation.json")
    prev, fresh, cached, cost = None, 0, 0, 0.0
    for sizes, segs in turns(docs, conv, churn):
        hit = 0
        if prev is not None:
            for a, b in zip(segs, prev):
                if a == b:
                    hit += approx_tokens(a)
                else:
                    break
        total = sum(sizes)
        cached += hit
        fresh += total - hit
        cost += (total - hit) / 1000 * PRICE_FRESH \
            + hit / 1000 * PRICE_CACHED
        prev = segs
    return {"fresh_tokens": fresh, "cached_tokens": cached,
            "cost_units": round(cost, 3)}


def evaluate():
    stable = run(False)
    churned = run(True)
    return {"stable_layout": stable, "churned_layout": churned,
            "cost_ratio_churned_over_stable": round(
                churned["cost_units"] / stable["cost_units"], 3)}


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(k, v)
