"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "check_environment.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['python_ok']
    assert r['documents'] == 18
    assert r['facts'] == 72
    assert r['tasks'] == 8
    assert r['required_fact_slots'] == 18
    assert r['conversation_turns'] == 24
    assert r['pinned_facts'] == 5
    assert r['window_tokens'] == 4000
    print("smoke ok:", "00-course-setup")


if __name__ == "__main__":
    main()
