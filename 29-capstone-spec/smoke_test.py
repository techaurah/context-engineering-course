"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "capstone_spec.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['checks']['gates_named'] == 5
    assert r['checks']['has_recall_gate']
    assert r['checks']['has_token_gate']
    assert r['checks']['tasks_in_scenario'] == 8
    assert r['checks']['documents_in_scenario'] == 18
    assert r['gates']['mean_total_tokens_max'] == 1000
    print("smoke ok:", "29-capstone-spec")


if __name__ == "__main__":
    main()
