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

RULES = [
    ("rule-source", "Answer only from the knowledge base provided."),
    ("rule-unknown", "If the knowledge base does not say, say so plainly."),
    ("rule-prices", "Never invent prices, times, or policies."),
    ("rule-tone", "Keep answers short and in plain English."),
    ("rule-escalate", "Escalate anger or legal threats to a human."),
    ("rule-privacy", "Never reveal another customer's details."),
]
FILLER = ("The assistant role exists so that customers get "
          "consistent answers at any hour, and the team reviews "
          "answers weekly for tone and accuracy, and the knowledge "
          "base is updated whenever a policy changes, and new staff "
          "read a sample of past answers before they reply alone.")


def wall_prompt():
    # The same six rules, dissolved into one rambling paragraph.
    text = FILLER + " " + " ".join(
        f"Also note that you should keep in mind: {r[1]}"
        for r in RULES) + " " + FILLER
    return text


def structured_prompt():
    lines = ["# Role", "Fernhill support assistant.", "", "# Rules"]
    lines += [f"- RULE: {text}" for _fid, text in RULES]
    return "\n".join(lines)


def extract_rules(text):
    """A mechanical checker: rules must appear verbatim, one per
    line, behind the RULE: marker, or they do not count."""
    found = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("- RULE:"):
            found.append(line[len("- RULE:"):].strip())
    return found


def evaluate():
    docs = load("documents.json")
    tail = [segment(d["id"], d["text"], [f["id"] for f in d["facts"]])
            for d in docs[:6]]
    results = {}
    for name, prompt in (("wall", wall_prompt()),
                         ("structured", structured_prompt())):
        segs = [segment("system", prompt,
                        [fid for fid, _t in RULES])] + tail
        r = standin.recall(segs, [fid for fid, _t in RULES], trials=20)
        results[name] = {
            "prompt_tokens": approx_tokens(prompt),
            "rules_extracted_verbatim": len(extract_rules(prompt)),
            "rule_recall_in_context": r["recall"],
        }
    return {"wall": results["wall"], "structured": results["structured"],
            "rules_total": len(RULES),
            "token_saving": results["wall"]["prompt_tokens"]
            - results["structured"]["prompt_tokens"]}


if __name__ == "__main__":
    r = evaluate()
    for name in ("wall", "structured"):
        print(name, r[name])
    print("token saving:", r["token_saving"])
