"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "compaction.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['keep_all']['tokens'] == 677
    assert r['truncate_last_8']['tokens'] == 267
    assert r['truncate_last_8']['probes_survived'] == 3
    assert r['rolling_notes']['tokens'] == 528
    assert r['rolling_notes']['probes_survived'] == 5
    assert r['rolling_notes']['pinned_survived'] == 5
    print("smoke ok:", "16-compacting-conversation-history")


if __name__ == "__main__":
    main()
