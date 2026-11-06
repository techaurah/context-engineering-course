"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "tool_output_filter.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['raw']['tokens'] == 1231
    assert r['raw']['answer_found']
    assert not r['truncated_first_3']['answer_found']
    assert r['field_selected']['tokens'] == 506
    assert r['filtered_and_fields']['tokens'] == 219
    assert r['filtered_and_fields']['answer_found']
    print("smoke ok:", "13-filtering-tool-outputs")


if __name__ == "__main__":
    main()
