"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "format_lab.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['prose']['fields_correct'] == 16
    assert r['list']['fields_correct'] == 20
    assert r['list']['tokens'] == 128
    assert r['tagged']['fields_correct'] == 20
    assert r['tagged']['tokens'] == 220
    print("smoke ok:", "07-structured-formats")


if __name__ == "__main__":
    main()
