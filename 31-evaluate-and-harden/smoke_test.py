"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "evaluate_capstone.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['as_built_gates_passed'] == 4
    assert r['as_built']['mean_precision'] == 0.1326
    assert r['gates_passed'] == 5
    assert r['gates_total'] == 5
    assert r['ship']
    assert r['baseline']['mean_recall'] == 0.8781
    assert r['variant_desc']['mean_total_tokens'] == 572
    assert r['variant_desc']['mean_precision'] == 0.2988
    print("smoke ok:", "31-evaluate-and-harden")


if __name__ == "__main__":
    main()
