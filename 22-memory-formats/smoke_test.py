"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "memory_formats.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['prose']['lookups_correct'] == 6
    assert r['csv_naive_reader']['lookups_correct'] == 0
    assert r['csv_unquoted_proper_reader']['lookups_correct'] == 0
    assert r['csv_quoted']['lookups_correct'] == 6
    assert r['csv_quoted']['tokens'] == 92
    assert r['json']['tokens'] == 217
    print("smoke ok:", "22-memory-formats")


if __name__ == "__main__":
    main()
