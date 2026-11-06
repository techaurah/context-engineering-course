"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "anchors.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['rule_at_start']['rule_use_rate'] == 1.0
    assert r['rule_in_middle']['rule_use_rate'] == 0.0
    assert r['rule_middle_and_repeated_at_end']['rule_use_rate'] == 1.0
    assert r['extra_tokens_for_repeat'] == 19
    print("smoke ok:", "19-anchors-and-repetition")


if __name__ == "__main__":
    main()
