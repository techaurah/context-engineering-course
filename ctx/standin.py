"""The stand-in reader: a deterministic teaching model of how a
real LLM uses the context it is given.

This is NOT a language model and it never generates text. It is a
scoring rule that implements, in the open, two effects the field
has measured on real models:

1. Position effect ("lost in the middle", Liu et al., TACL 2024):
   information near the start and the end of the context is used
   more reliably than information in the middle. Implemented as a
   U-shaped position weight: 1.00 at the edges, 0.66 in the exact
   middle.
2. Context rot (Chroma, 2025): as total context grows, use of any
   single fact degrades, even far below the window limit.
   Implemented as a linear penalty of 0.045 per 1000 tokens.

A fact is "used" on a trial when its score clears a fixed
threshold of 0.60. Trials differ only by a small deterministic
jitter derived from the fact id and the trial seed, so every
number in this course reproduces exactly from the seeds.

Use it to compare ASSEMBLY DECISIONS (selection, ordering,
compression), never to claim what a real model would do.
"""

import hashlib

THRESHOLD = 0.60
ROT_PER_1000 = 0.045


def position_weight(rel_pos):
    """U-shaped weight for a relative position in [0, 1]."""
    return 0.66 + 0.34 * (abs(2 * rel_pos - 1) ** 1.6)


def _jitter(fact_id, seed):
    digest = hashlib.sha256(f"{fact_id}:{seed}".encode()).hexdigest()
    return (int(digest[:6], 16) % 1000) / 1000.0 * 0.10 - 0.05


def fact_score(rel_pos, total_tokens, fact_id, seed=0):
    return (position_weight(rel_pos)
            - ROT_PER_1000 * (total_tokens / 1000.0)
            + _jitter(fact_id, seed))


def layout_facts(segments):
    """Place every fact at the token midpoint of its occurrence.

    segments: list of dicts {id, text, facts: [fact_id, ...]} in
    context order. Returns (positions, total_tokens) where
    positions maps fact_id -> relative position of its midpoint.
    """
    from .tokenizer import approx_tokens
    total = sum(approx_tokens(s["text"]) for s in segments)
    positions = {}
    cursor = 0
    for seg in segments:
        n = approx_tokens(seg["text"])
        facts = seg.get("facts", [])
        for i, fid in enumerate(facts):
            # Spread a segment's facts evenly across its span.
            frac = (i + 0.5) / max(1, len(facts))
            positions[fid] = (cursor + frac * n) / total if total else 0.5
        cursor += n
    return positions, total


def recall(segments, required_facts, trials=20):
    """Mean fraction of required facts the stand-in uses.

    Runs `trials` seeded trials and returns a dict with the mean
    recall, the per-fact use rate, and the total token count.
    """
    positions, total = layout_facts(segments)
    per_fact = {}
    hits = 0
    for fid in required_facts:
        if fid not in positions:
            per_fact[fid] = 0.0
            continue
        used = sum(
            1 for t in range(trials)
            if fact_score(positions[fid], total, fid, seed=t) >= THRESHOLD
        )
        per_fact[fid] = used / trials
        hits += per_fact[fid]
    mean = hits / len(required_facts) if required_facts else 1.0
    return {"recall": round(mean, 4), "per_fact": per_fact,
            "total_tokens": total}
