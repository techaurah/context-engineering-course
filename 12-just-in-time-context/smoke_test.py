"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "jit_lab.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['preload_all_tokens'] == 2212
    assert r['title_index']['mean_tokens_per_task'] == 344
    assert r['title_index']['fact_coverage'] == 0.8889
    assert r['keyword_index']['fact_coverage'] == 1.0
    assert r['keyword_index']['mean_tokens_per_task'] == 832
    print("smoke ok:", "12-just-in-time-context")


if __name__ == "__main__":
    main()
