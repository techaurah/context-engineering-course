"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "run_ledger.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['raw_results']['total_tokens'] == 13488
    assert r['compact_results']['total_tokens'] == 9750
    assert r['raw_results']['dominant_component'] == 'history_replay'
    assert r['saving_units'] == 3.738
    assert r['saving_ratio'] == 0.7229
    print("smoke ok:", "27-cost-and-latency-accounting")


if __name__ == "__main__":
    main()
