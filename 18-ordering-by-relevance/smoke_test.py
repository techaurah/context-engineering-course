"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "ordering_lab.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['relevance_desc'] == 0.7689
    assert r['relevance_asc'] == 0.7682
    assert r['edges'] == 0.7498
    assert r['docs_per_context'] == 18
    print("smoke ok:", "18-ordering-by-relevance")


if __name__ == "__main__":
    main()
