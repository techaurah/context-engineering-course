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

import csv
import io
import json
import re

from ctx.tokenizer import approx_tokens

RECORDS = [
    {"order": "FH-1041", "customer": "Shah, Priya", "status": "delivered"},
    {"order": "FH-1042", "customer": "Ellery, Tom", "status": "booked"},
    {"order": "FH-1043", "customer": "Ruiz, Ana", "status": "paid"},
    {"order": "FH-1044", "customer": "Okafor, Ben", "status": "delivered"},
    {"order": "FH-1045", "customer": "Novak, Eva", "status": "refunded"},
    {"order": "FH-1046", "customer": "Smith, Jay", "status": "booked"},
]
QUERIES = ["FH-1041", "FH-1042", "FH-1043", "FH-1044", "FH-1045",
           "FH-1046"]


def as_prose(records):
    return " ".join(
        f"Order {r['order']} for {r['customer']} is {r['status']}."
        for r in records)


def as_csv(records):
    lines = ["order,customer,status"]
    lines += [f"{r['order']},{r['customer']},{r['status']}"
              for r in records]
    return "\n".join(lines)


def as_json(records):
    return json.dumps(records)


def lookup_prose(text, order):
    m = re.search(rf"Order {order} for .+? is (\w+)\.", text)
    return m.group(1) if m else None


def lookup_csv(text, order):
    for line in text.splitlines()[1:]:
        parts = line.split(",")
        if parts[0] == order:
            # Naive split: a comma inside the customer name shifts
            # every later column. That breakage is the measurement.
            return parts[2] if len(parts) > 2 else None
    return None


def lookup_json(text, order):
    for r in json.loads(text):
        if r["order"] == order:
            return r["status"]
    return None


def as_csv_quoted(records):
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["order", "customer", "status"])
    for r in records:
        w.writerow([r["order"], r["customer"], r["status"]])
    return buf.getvalue()


def lookup_csv_proper(text, order):
    for row in csv.DictReader(io.StringIO(text)):
        if row["order"] == order:
            return row["status"]
    return None


def evaluate():
    truth = {r["order"]: r["status"] for r in RECORDS}
    out = {}
    for name, fmt, lookup in (("prose", as_prose, lookup_prose),
                              ("csv_naive_reader", as_csv, lookup_csv),
                              ("csv_unquoted_proper_reader", as_csv,
                               lookup_csv_proper),
                              ("csv_quoted", as_csv_quoted,
                               lookup_csv_proper),
                              ("json", as_json, lookup_json)):
        text = fmt(RECORDS)
        correct = sum(1 for q in QUERIES
                      if lookup(text, q) == truth[q])
        out[name] = {"lookups_correct": correct, "of": len(QUERIES),
                     "tokens": approx_tokens(text)}
    return out


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(k, v)
