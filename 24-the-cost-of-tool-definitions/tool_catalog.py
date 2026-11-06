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

import itertools
import json
import re

from ctx.tokenizer import approx_tokens

# Two catalogues for the same job. The verbose one grew the way
# real catalogues grow: every team added a tool, descriptions
# repeat each other, and two tools overlap almost completely.
# The stand-in chooser picks the tool whose description overlaps
# the request most; confusion is measured, not asserted.
VERBOSE = [
    ("search_knowledge_base", "Search the knowledge base for information to answer questions about policies, products, prices, opening times, deliveries, returns, and anything else a customer might ask about."),
    ("search_products", "Search products for information about items, prices, stock, and product questions a customer might ask about."),
    ("lookup_order", "Look up an order to find order status, order delivery details, and order items for a customer order."),
    ("lookup_delivery", "Look up delivery details for an order, including delivery day, delivery window, and delivery status."),
    ("book_workshop", "Book a workshop place, reserve a workshop seat, or register a customer for a workshop session."),
    ("book_cafe", "Book a cafe table, reserve cafe seating, or register a group booking for the cafe."),
    ("check_stock", "Check stock levels for a product item at a garden centre."),
    ("escalate", "Escalate the conversation to a human member of staff when the customer is angry or the request is unusual."),
]
TRIMMED = [
    ("search", "Search the knowledge base and product catalogue; returns matching entries with prices and stock."),
    ("order_status", "Order status and delivery day for one order id."),
    ("book", "Book a workshop place or a cafe table; say which in the request."),
    ("stock", "Stock level for one product at one centre."),
    ("escalate", "Hand the conversation to a human."),
]
REQUESTS = [
    ("What time does the cafe open on Sunday?", "search"),
    ("Where is my order FH-1041?", "order_status"),
    ("Book two places on the pruning workshop", "book"),
    ("Is the 40 litre compost in stock?", "stock"),
    ("I am furious, get me a person", "escalate"),
    ("When will my delivery arrive?", "order_status"),
    ("Reserve a cafe table for eight people", "book"),
    ("Do you have any water butts left?", "stock"),
]
ALIASES = {"search_knowledge_base": "search", "search_products": "search",
           "lookup_order": "order_status", "lookup_delivery": "order_status",
           "book_workshop": "book", "book_cafe": "book",
           "check_stock": "stock", "escalate": "escalate"}


def words(text):
    return set(re.findall(r"[a-z]+", text.lower()))


def choose(request, catalog):
    rw = words(request)
    best, best_score = None, -1
    for name, desc in catalog:
        s = len(rw & words(desc))
        if s > best_score:
            best, best_score = name, s
    return best


def overlap(a, b):
    wa, wb = words(a), words(b)
    return len(wa & wb) / max(1, len(wa | wb))


TWIN_REQUESTS = [
    ("Has my order been dispatched?", "lookup_order"),
    ("Which day is the delivery coming?", "lookup_delivery"),
    ("What is the status of my order?", "lookup_order"),
    ("What window will the delivery arrive in?", "lookup_delivery"),
    ("Show me the delivery status for my order", "lookup_delivery"),
    ("Track my order please", "lookup_order"),
]


def run(name, catalog):
    text = json.dumps([{"name": n, "description": d} for n, d in catalog])
    correct = 0
    for req, want in REQUESTS:
        got = choose(req, catalog)
        if ALIASES.get(got, got) == want:
            correct += 1
    pairs = [(a[0], b[0], round(overlap(a[1], b[1]), 3))
             for a, b in itertools.combinations(catalog, 2)]
    worst = max(pairs, key=lambda p: p[2])
    # Twin probe: in the trimmed catalogue the two overlapping
    # tools were merged into one, so a twin confusion is
    # impossible by construction; counted correct and labelled.
    twin_correct = 0
    for req, want in TWIN_REQUESTS:
        got = choose(req, catalog)
        if got == want or (name == "trimmed" and got == "order_status"):
            twin_correct += 1
    return {"tools": len(catalog), "definition_tokens": approx_tokens(text),
            "choices_correct": correct, "of": len(REQUESTS),
            "twin_probe_correct": twin_correct,
            "twin_probe_of": len(TWIN_REQUESTS),
            "worst_overlap_pair": worst}


def evaluate():
    return {"verbose": run("verbose", VERBOSE),
            "trimmed": run("trimmed", TRIMMED)}


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(k, v)
