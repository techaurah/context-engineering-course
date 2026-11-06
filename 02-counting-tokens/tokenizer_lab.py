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

from ctx.tokenizer import approx_tokens, word_count


def evaluate():
    texts = load("texts.json")
    docs = load("documents.json")
    corpus = [t["text"] for t in texts] + [d["text"] for d in docs]
    rows = []
    for text in corpus:
        approx = approx_tokens(text)
        rows.append({
            "approx": approx,
            "words": word_count(text),
            "chars_div_4": round(len(text) / 4),
            "tokens_per_word": round(approx / word_count(text), 3),
        })
    tpw = [r["tokens_per_word"] for r in rows]
    # How far the chars/4 heuristic strays from the approximation,
    # as a ratio, worst case across the corpus.
    worst = max(abs(r["chars_div_4"] - r["approx"]) / r["approx"]
                for r in rows)
    return {"texts_measured": len(rows),
            "total_approx_tokens": sum(r["approx"] for r in rows),
            "min_tokens_per_word": min(tpw),
            "max_tokens_per_word": max(tpw),
            "chars4_worst_relative_error": round(worst, 3),
            "first_text": rows[0]}


if __name__ == "__main__":
    r = evaluate()
    print("first text:", r["first_text"])
    for k, v in r.items():
        if k != "first_text":
            print(k, v)
