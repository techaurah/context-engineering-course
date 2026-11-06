"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "context_pipeline.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['mean_recall'] == 1.0
    assert r['mean_coverage'] == 1.0
    assert r['worst_task_recall'] == 1.0
    assert r['mean_total_tokens'] == 572
    assert r['mean_precision'] == 0.2988
    assert len(r['per_task']) == 8
    print("smoke ok:", "30-build-the-capstone-pipeline")


if __name__ == "__main__":
    main()
