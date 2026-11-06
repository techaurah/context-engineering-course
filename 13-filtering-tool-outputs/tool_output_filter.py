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

import json

from ctx.tokenizer import approx_tokens

# A simulated verbose search-tool result: 12 products, 9 fields
# each, the way a real catalogue API answers when nobody designed
# the result schema. The task: find the cheapest in-stock 40 litre
# compost bag. NEED names the fields the answer depends on.
PRODUCTS = [
    {"sku": "CMP-40-A", "name": "Multi purpose compost 40L", "price": 6.5,
     "stock": 34, "weight_kg": 18, "peat_free": True, "rating": 4.6,
     "warehouse": "North", "supplier_ref": "SUP-991", "bin": "Aisle 3"},
    {"sku": "CMP-40-B", "name": "Premium compost 40L", "price": 8.0,
     "stock": 0, "weight_kg": 18, "peat_free": True, "rating": 4.8,
     "warehouse": "North", "supplier_ref": "SUP-992", "bin": "Aisle 3"},
    {"sku": "CMP-50-A", "name": "Multi purpose compost 50L", "price": 7.5,
     "stock": 12, "weight_kg": 22, "peat_free": False, "rating": 4.4,
     "warehouse": "South", "supplier_ref": "SUP-993", "bin": "Aisle 4"},
    {"sku": "SOIL-25", "name": "Topsoil 25L", "price": 4.0, "stock": 50,
     "weight_kg": 20, "peat_free": True, "rating": 4.1,
     "warehouse": "South", "supplier_ref": "SUP-994", "bin": "Aisle 5"},
    {"sku": "BARK-60", "name": "Bark mulch 60L", "price": 9.0,
     "stock": 20, "weight_kg": 15, "peat_free": True, "rating": 4.5,
     "warehouse": "North", "supplier_ref": "SUP-995", "bin": "Aisle 6"},
    {"sku": "CMP-40-C", "name": "Value compost 40L", "price": 5.5,
     "stock": 8, "weight_kg": 17, "peat_free": False, "rating": 3.9,
     "warehouse": "South", "supplier_ref": "SUP-996", "bin": "Aisle 3"},
    {"sku": "GRIT-20", "name": "Horticultural grit 20kg", "price": 6.0,
     "stock": 15, "weight_kg": 20, "peat_free": True, "rating": 4.3,
     "warehouse": "North", "supplier_ref": "SUP-997", "bin": "Aisle 7"},
    {"sku": "CMP-40-D", "name": "Organic compost 40L", "price": 7.0,
     "stock": 5, "weight_kg": 18, "peat_free": True, "rating": 4.7,
     "warehouse": "North", "supplier_ref": "SUP-998", "bin": "Aisle 3"},
    {"sku": "FEED-1", "name": "Tomato feed 1L", "price": 5.0,
     "stock": 40, "weight_kg": 1, "peat_free": True, "rating": 4.6,
     "warehouse": "South", "supplier_ref": "SUP-999", "bin": "Aisle 8"},
    {"sku": "POT-10", "name": "Terracotta pot 30cm", "price": 11.0,
     "stock": 9, "weight_kg": 3, "peat_free": True, "rating": 4.2,
     "warehouse": "North", "supplier_ref": "SUP-1000", "bin": "Aisle 9"},
    {"sku": "CMP-40-E", "name": "Ericaceous compost 40L", "price": 6.0,
     "stock": 11, "weight_kg": 18, "peat_free": True, "rating": 4.5,
     "warehouse": "South", "supplier_ref": "SUP-1001", "bin": "Aisle 3"},
    {"sku": "SAND-25", "name": "Sharp sand 25kg", "price": 4.5,
     "stock": 22, "weight_kg": 25, "peat_free": True, "rating": 4.0,
     "warehouse": "North", "supplier_ref": "SUP-1002", "bin": "Aisle 5"},
]
NEED = ["sku", "name", "price", "stock"]
ANSWER_SKU = "CMP-40-C"  # cheapest in-stock 40L compost


def find_answer(rows):
    cands = [r for r in rows
             if "stock" in r and "price" in r and r.get("stock", 0) > 0
             and "40L" in r.get("name", "")
             and "compost" in r.get("name", "")]
    if not cands:
        return None
    return min(cands, key=lambda r: r["price"])["sku"]


def strategy(name, rows):
    text = json.dumps(rows, indent=1)
    return {"tokens": approx_tokens(text),
            "answer_found": find_answer(rows) == ANSWER_SKU}


def evaluate():
    raw = PRODUCTS
    truncated = PRODUCTS[:3]
    field_selected = [{k: r[k] for k in NEED} for r in PRODUCTS]
    filtered = [{k: r[k] for k in NEED} for r in PRODUCTS
                if "compost" in r["name"] and "40L" in r["name"]]
    return {"raw": strategy("raw", raw),
            "truncated_first_3": strategy("trunc", truncated),
            "field_selected": strategy("fields", field_selected),
            "filtered_and_fields": strategy("filt", filtered),
            "answer_sku": ANSWER_SKU}


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(k, v)
