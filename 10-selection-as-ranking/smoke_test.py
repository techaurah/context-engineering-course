"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "ranking.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['tasks'] == 8
    assert r['relevant_in_top_k'][1] == 7
    assert r['relevant_in_top_k'][2] == 8
    assert r['recall_at_3'] == 1.0
    print("smoke ok:", "10-selection-as-ranking")


if __name__ == "__main__":
    main()
