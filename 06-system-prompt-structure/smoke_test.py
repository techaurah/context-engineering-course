"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "prompt_structure.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['wall']['prompt_tokens'] == 288
    assert r['wall']['rules_extracted_verbatim'] == 0
    assert r['structured']['rules_extracted_verbatim'] == 6
    assert r['structured']['prompt_tokens'] == 111
    assert r['token_saving'] == 177
    assert r['structured']['rule_recall_in_context'] == 1.0
    print("smoke ok:", "06-system-prompt-structure")


if __name__ == "__main__":
    main()
