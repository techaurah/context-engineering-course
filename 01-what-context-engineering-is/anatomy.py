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

from ctx.assemble import segment, total_tokens
from ctx.tokenizer import approx_tokens

SYSTEM = ("You are the Fernhill support assistant. Answer from the "
          "knowledge base only. If the knowledge base does not say, "
          "say so plainly. Never invent prices, times, or policies.")
TOOLS = ("Tools: lookup_order(order_id), book_workshop(name, date), "
         "check_stock(item), escalate(reason).")
MEMORY = "Customer: loyalty Gold member. Prefers Tuesday deliveries."


def evaluate():
    docs = {d["id"]: d for d in load("documents.json")}
    conv = load("conversation.json")
    task = load("tasks.json")[0]
    history_text = "\n".join(
        f"{t['role']}: {t['text']}" for t in conv["turns"][:6])
    parts = {
        "system": SYSTEM,
        "tools": TOOLS,
        "memory": MEMORY,
        "history": history_text,
        "retrieval": "\n".join(docs[d]["text"] for d in
                               ["doc-delivery", "doc-orders", "doc-cafe"]),
        "user": task["question"],
    }
    tokens = {k: approx_tokens(v) for k, v in parts.items()}
    total = sum(tokens.values())
    shares = {k: round(v / total, 3) for k, v in tokens.items()}
    return {"tokens": tokens, "total_tokens": total, "shares": shares,
            "retrieval_is_largest": max(tokens, key=tokens.get) == "retrieval",
            "parts": len(parts)}


if __name__ == "__main__":
    r = evaluate()
    for k, v in r["tokens"].items():
        print(f"{k:10s} {v:5d} tokens  {r['shares'][k]:.1%}")
    print("total", r["total_tokens"])
