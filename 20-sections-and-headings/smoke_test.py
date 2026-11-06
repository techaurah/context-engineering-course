"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "layout_lab.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['flat']['answers_correct'] == 2
    assert r['headed']['answers_correct'] == 6
    assert r['flat_tokens'] == 216
    assert r['headed_tokens'] == 186
    print("smoke ok:", "20-sections-and-headings")


if __name__ == "__main__":
    main()
