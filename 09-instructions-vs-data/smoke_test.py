"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "channel_separation.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['unsafe_compromised']
    assert not r['safe_compromised']
    assert r['safe_action'] == 'answer_from_policy'
    assert r['tasks_checked'] == 3
    print("smoke ok:", "09-instructions-vs-data")


if __name__ == "__main__":
    main()
