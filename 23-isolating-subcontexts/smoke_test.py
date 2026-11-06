"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "isolation.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['single_context_tokens'] == 376
    assert r['single_final_task_recall'] == 1.0
    assert r['isolated_subquestion_recall'] == 1.0
    assert r['isolated_final_task_recall'] == 0.0
    assert r['isolated_combiner_tokens'] == 37
    assert r['isolated_total_tokens_processed'] == 413
    print("smoke ok:", "23-isolating-subcontexts")


if __name__ == "__main__":
    main()
