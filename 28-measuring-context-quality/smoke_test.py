"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "quality_harness.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['preload_all']['mean_recall'] == 0.8875
    assert r['preload_all']['mean_precision'] == 0.0556
    assert r['overlap_top3']['mean_tokens'] == 432
    assert r['overlap_top2']['mean_recall'] == 1.0
    assert r['overlap_top2']['mean_tokens'] == 306
    assert r['overlap_top2']['mean_precision'] == 0.4123
    print("smoke ok:", "28-measuring-context-quality")


if __name__ == "__main__":
    main()
