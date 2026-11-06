"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "memory_notes.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['checks'] == 5
    assert r['correct_with_notes'] == 5
    assert r['correct_without_notes'] == 0
    assert r['notes_tokens'] == 111
    assert r['transcript_tokens'] == 677
    print("smoke ok:", "21-writing-external-memory")


if __name__ == "__main__":
    main()
