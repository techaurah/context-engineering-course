"""A small, deterministic token count approximation.

Real tokenizers (BPE and friends) split text into subword pieces
learned from data. This module implements a documented stand-in
so the course can count tokens offline with no dependencies:

- Text is split into runs of letters, runs of digits, single
  punctuation characters, and whitespace runs.
- A letter run of length L costs ceil(L / 4) tokens: short words
  are usually one piece, long words split into pieces of about
  four characters.
- A digit run of length L costs ceil(L / 3) tokens: tokenizers
  typically split numbers into groups of up to three digits.
- Each punctuation character costs 1 token. Whitespace between
  runs costs nothing (it attaches to the following piece in most
  BPE vocabularies).

This is an APPROXIMATION, labelled as such everywhere it is used.
On the bundled fixtures its counts land within the band Lesson 02
measures against character and word heuristics. Never quote its
output as a real model's token count.
"""

import math
import re

_RUN = re.compile(r"[A-Za-z]+|[0-9]+|[^\sA-Za-z0-9]")


def approx_tokens(text):
    total = 0
    for run in _RUN.findall(text):
        if run[0].isalpha():
            total += max(1, math.ceil(len(run) / 4))
        elif run[0].isdigit():
            total += max(1, math.ceil(len(run) / 3))
        else:
            total += 1
    return total


def word_count(text):
    return len(text.split())


def segments_tokens(segments):
    """segments: iterable of dicts with a 'text' key."""
    return {s["id"]: approx_tokens(s["text"]) for s in segments}


if __name__ == "__main__":
    sample = "Deliveries run Tuesday to Friday, between 9:00 and 17:30."
    print(sample, "->", approx_tokens(sample), "approx tokens,",
          word_count(sample), "words,", len(sample), "chars")
