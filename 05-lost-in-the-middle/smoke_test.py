"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "position_sweep.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['recall_position_1'] == 1.0
    assert r['recall_position_10'] == 1.0
    assert r['recall_middle_min'] == 0.65
    assert r['u_shape_gap'] == 0.35
    print("smoke ok:", "05-lost-in-the-middle")


if __name__ == "__main__":
    main()
