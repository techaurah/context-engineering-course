"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "budget_ledger.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['history_allowance'] == 800
    assert r['allowance_breaks_at_turn'] == 30
    assert r['history_after_48_turns'] == 1354
    assert r['over_budget']
    print("smoke ok:", "03-the-context-budget")


if __name__ == "__main__":
    main()
