"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "cache_sim.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['stable_layout']['cached_tokens'] == 1449
    assert r['churned_layout']['cached_tokens'] == 0
    assert r['stable_layout']['cost_units'] == 6.671
    assert r['churned_layout']['cost_units'] == 8.119
    assert r['cost_ratio_churned_over_stable'] == 1.217
    print("smoke ok:", "26-prefix-stability-and-caching")


if __name__ == "__main__":
    main()
