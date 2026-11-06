"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "tfidf_lab.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['budget_tokens'] == 400
    assert r['overlap']['fact_coverage'] == 1.0
    assert r['tfidf']['fact_coverage'] == 1.0
    assert r['tfidf']['mean_standin_recall'] == 0.9969
    assert r['overlap']['mean_standin_recall'] == 0.9906
    print("smoke ok:", "11-tfidf-selection")


if __name__ == "__main__":
    main()
