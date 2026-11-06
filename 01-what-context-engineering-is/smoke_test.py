"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "anatomy.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['total_tokens'] == 668
    assert r['shares']['retrieval'] == 0.56
    assert r['retrieval_is_largest']
    assert r['parts'] == 6
    print("smoke ok:", "01-what-context-engineering-is")


if __name__ == "__main__":
    main()
