"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "extractive.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['compression_ratio'] == 0.4207
    assert r['key_fact_retention'] == 1.0
    assert r['key_facts_kept'] == 10
    assert r['key_facts_total'] == 10
    assert r['per_text']['text-watering-guide']['sentences_kept'] == 6
    print("smoke ok:", "14-extractive-compression")


if __name__ == "__main__":
    main()
