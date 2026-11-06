"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "dedup.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['documents_before'] == 21
    assert r['tokens_before'] == 2582
    assert r['first']['tokens_saved'] == 382
    assert r['first']['unique_facts_lost'] == 1
    assert r['first']['lost_fact_ids'] == ['fh-cafe-dogs']
    assert r['longest']['unique_facts_lost'] == 0
    assert r['longest']['tokens_saved'] == 369
    print("smoke ok:", "17-pruning-and-deduplication")


if __name__ == "__main__":
    main()
