# Lesson 17: Pruning and deduplication: near copies, and the fact the short copy lost

Time: ~45 min | Difficulty: Intermediate | Prerequisites: Lesson 16

Retrieval in the wild returns near copies: the same document from two crawls, an old version beside the new one, a mirror with a different wrapper. Admitting all of them pays tokens for zero new facts and shoves everything else toward the middle. This lesson builds the standard defence, shingle based near duplicate detection with a Jaccard threshold, over a working set of the 18 fixture documents plus 3 lightly reworded copies, one of which is a stale cafe page that predates the dog policy fact.

The subtle part is not detection; it is the keep policy. When two near copies collide, which one survives decides which facts survive, and the two obvious policies (keep first, keep longest) measure differently in exactly the way that matters.

## Run it

```bash
python3 dedup.py
```

## What the code measures

The working set starts at 21 documents and 2,582 tokens. Both policies prune to 18 documents. Keep first (the stale copies surfaced first in retrieval order) saves 382 tokens and loses 1 unique fact: fh-cafe-dogs, the dog policy the stale copy predates. Keep longest saves 369 tokens and loses nothing. Thirteen tokens is the entire price of keeping the complete copy; the fact was worth more.

## Common failures

- Keeping the first copy retrieval returns. Retrieval order is not a freshness signal; here it was actively stale.
- Deduplicating on titles or URLs. The copies here share neither exactly; shingles on content catch what metadata misses.
- Reporting dedup savings without a fact loss count. Saving 382 tokens while losing a policy fact is a bad trade wearing a good number.

## Recap checklist

- [ ] You can explain how shingle Jaccard detects a near copy
- [ ] You can state both keep policies' savings and fact losses
- [ ] You know the name and content of the fact the wrong policy lost

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
