"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "tool_catalog.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['verbose']['definition_tokens'] == 428
    assert r['trimmed']['definition_tokens'] == 187
    assert r['verbose']['choices_correct'] == 4
    assert r['trimmed']['choices_correct'] == 4
    assert r['verbose']['twin_probe_correct'] == 4
    assert r['trimmed']['twin_probe_correct'] == 5
    assert r['verbose']['worst_overlap_pair'][2] == 0.529
    print("smoke ok:", "24-the-cost-of-tool-definitions")


if __name__ == "__main__":
    main()
