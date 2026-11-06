"""Smoke test for this lesson: run the artifact and check its
measured results. Run from this folder: python3 smoke_test.py
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = os.path.join(HERE, "tokenizer_lab.py")


def main():
    spec = importlib.util.spec_from_file_location("lesson_artifact", ARTIFACT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.evaluate()
    assert r['texts_measured'] == 21
    assert r['total_approx_tokens'] == 3051
    assert r['min_tokens_per_word'] == 1.494
    assert r['max_tokens_per_word'] == 1.776
    assert r['chars4_worst_relative_error'] == 0.156
    print("smoke ok:", "02-counting-tokens")


if __name__ == "__main__":
    main()
