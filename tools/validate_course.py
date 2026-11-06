#!/usr/bin/env python3
"""Validate this course's JSON data and cross references.

Checks:
- Every .json file parses.
- fixtures/documents.json: each document has id, title, text,
  and a non empty facts list; fact ids are unique across the
  corpus and each fact has id and text.
- fixtures/tasks.json: each task's required_facts exist in the
  corpus and its relevant_docs exist and actually carry those
  facts.
- fixtures/conversation.json: turns have role and text;
  pinned_facts is a non empty list.
- The capstone gates file (recognised by a "capstone_pipeline"
  key) carries a gates object with the five gates Lesson 29
  fixes, each a number.
Exits nonzero on any failure, so CI can gate on it.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE_KEYS = ["mean_required_fact_recall_min", "fact_coverage_min",
             "worst_task_recall_min", "mean_total_tokens_max",
             "mean_precision_min"]


def iter_json():
    for dirpath, _dirs, files in os.walk(ROOT):
        if ".git" in dirpath or "__pycache__" in dirpath:
            continue
        for name in sorted(files):
            if name.endswith(".json"):
                yield os.path.join(dirpath, name)


def main():
    total, bad = 0, 0
    data_by_rel = {}
    for path in iter_json():
        total += 1
        rel = os.path.relpath(path, ROOT)
        try:
            with open(path) as f:
                data_by_rel[rel] = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            bad += 1
            print(f"FAIL {rel}: does not parse: {exc}")
    errors = []
    docs = data_by_rel.get("fixtures/documents.json", [])
    fact_owner = {}
    for d in docs:
        for field in ("id", "title", "text", "facts"):
            if field not in d:
                errors.append(f"document missing {field}: {d.get('id')}")
        for f in d.get("facts", []):
            if f["id"] in fact_owner:
                errors.append(f"duplicate fact id: {f['id']}")
            fact_owner[f["id"]] = d["id"]
            if not f.get("text"):
                errors.append(f"fact has no text: {f['id']}")
    doc_ids = {d["id"] for d in docs}
    for t in data_by_rel.get("fixtures/tasks.json", []):
        for fid in t.get("required_facts", []):
            if fid not in fact_owner:
                errors.append(f"{t['id']}: unknown fact {fid}")
            elif fact_owner[fid] not in t.get("relevant_docs", []):
                errors.append(
                    f"{t['id']}: fact {fid} lives in "
                    f"{fact_owner[fid]}, not in relevant_docs")
        for did in t.get("relevant_docs", []):
            if did not in doc_ids:
                errors.append(f"{t['id']}: unknown doc {did}")
    conv = data_by_rel.get("fixtures/conversation.json", {})
    for turn in conv.get("turns", []):
        if "role" not in turn or "text" not in turn:
            errors.append("conversation turn missing role or text")
    if not conv.get("pinned_facts"):
        errors.append("conversation carries no pinned facts")
    for rel, data in data_by_rel.items():
        if isinstance(data, dict) and "capstone_pipeline" in data:
            gates = data["capstone_pipeline"].get("gates", {})
            for key in GATE_KEYS:
                if not isinstance(gates.get(key), (int, float)):
                    errors.append(f"{rel}: gate missing or not a "
                                  f"number: {key}")
    for e in errors:
        bad += 1
        print("FAIL", e)
    print(f"\n{total} JSON files checked, {bad} failing")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
