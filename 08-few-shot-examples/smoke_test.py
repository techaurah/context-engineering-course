"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "fewshot_lab.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['accuracy_0_examples'] == 0.25
    assert r['accuracy_10_examples'] == 1.0
    assert r['best_k'] == 6
    assert r['curve'][6]['example_tokens'] == 82
    assert r['curve'][10]['example_tokens'] == 141
    print("smoke ok:", "08-few-shot-examples")


if __name__ == "__main__":
    main()
