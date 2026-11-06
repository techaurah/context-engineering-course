"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "summarizer_lab.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['summary_facts_kept'] == 2
    assert r['extractive_facts_kept'] == 3
    assert r['summary_tokens'] == 45
    assert r['extractive_tokens'] == 149
    assert r['original_tokens'] == 357
    assert len(r['summary_dropped']) == 2
    print("smoke ok:", "15-the-standin-summarizer")


if __name__ == "__main__":
    main()
