"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "rot_experiment.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['recall_no_padding'] == 1.0
    assert r['recall_max_padding'] == 0.0
    assert r['rot_drop'] == 1.0
    assert r['monotone_nonincreasing']
    assert r['curve'][2000]['recall'] == 0.1833
    print("smoke ok:", "04-context-rot")


if __name__ == "__main__":
    main()
