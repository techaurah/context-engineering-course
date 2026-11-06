"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "result_schemas.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['verbose']['mean_tokens_per_task'] == 614
    assert r['compact']['mean_tokens_per_task'] == 224
    assert r['verbose']['fact_coverage'] == 1.0
    assert r['compact']['fact_coverage'] == 1.0
    assert r['tasks'] == 8
    print("smoke ok:", "25-token-efficient-tool-results")


if __name__ == "__main__":
    main()
