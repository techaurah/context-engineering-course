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

import re

from ctx.tokenizer import approx_tokens

# The stand-in classifier for this lesson: it labels a message
# with the intent of the example whose wording overlaps it most
# (ties break to the earliest example). It is a labelled teaching
# stand-in for a model's in-context learning, nothing more.

EXAMPLES = [
    ("When does my order arrive?", "delivery"),
    ("Can I send this plant back?", "returns"),
    ("The driver never showed up, this is a disgrace", "complaint"),
    ("Book me a place on the pruning workshop", "booking"),
    ("Do you sell gift cards?", "other"),
    ("Where is my delivery today?", "delivery"),
    ("I want a refund for the damaged pot", "returns"),
    ("Your cafe staff were rude to my mother", "complaint"),
    ("Two places on the compost workshop please", "booking"),
    ("What are your opening hours on Sunday?", "other"),
]
TEST = [
    ("Has my delivery arrived yet?", "delivery"),
    ("Can I return a spade I bought last week?", "returns"),
    ("Nobody answered the phone all morning, furious", "complaint"),
    ("Please book two workshop places for Saturday", "booking"),
    ("Do you allow dogs in the cafe garden?", "other"),
    ("When will the van bring my compost?", "delivery"),
    ("The plant died in a week, I want my money back", "returns"),
    ("I would like to book a wedding flower consultation", "booking"),
]


def words(text):
    return set(re.findall(r"[a-z]+", text.lower()))


def classify(message, examples):
    if not examples:
        return "delivery"  # the majority label in the pool
    mw = words(message)
    best, best_score = None, -1
    for text, label in examples:
        score = len(mw & words(text))
        if score > best_score:
            best, best_score = label, score
    return best


def evaluate():
    curve = {}
    for k in (0, 2, 4, 6, 8, 10):
        ex = EXAMPLES[:k]
        correct = sum(1 for msg, label in TEST
                      if classify(msg, ex) == label)
        prompt = "\n".join(f"{t} -> {l}" for t, l in ex)
        curve[k] = {"accuracy": round(correct / len(TEST), 4),
                    "correct": correct, "of": len(TEST),
                    "example_tokens": approx_tokens(prompt)}
    return {"curve": curve,
            "accuracy_0_examples": curve[0]["accuracy"],
            "accuracy_10_examples": curve[10]["accuracy"],
            "best_k": max(curve, key=lambda k: curve[k]["accuracy"])}


if __name__ == "__main__":
    r = evaluate()
    for k, v in r["curve"].items():
        print(f"examples {k:2d}: accuracy {v['accuracy']}, "
              f"tokens {v['example_tokens']}")
    print("best k:", r["best_k"])
