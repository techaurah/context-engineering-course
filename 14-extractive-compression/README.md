# Lesson 14: Extractive compression: keep the sentences that carry the facts

Time: ~50 min | Difficulty: Intermediate | Prerequisites: Lesson 13

Compression is the third context operation, and extractive compression is its honest floor: select whole sentences from the source, ranked by overlap with the task, until the token budget runs out. Nothing is rewritten, so nothing can be hallucinated; the only risk is omission. This lesson compresses the three bundled prose guides to 45 percent of their size, each against a realistic query, and measures the only ratio that matters: how many of each text's listed key facts survive.

Extractive selection has a home advantage here and the lesson names it: the queries were written against these texts, the way a real user's question is written against their actual need. Lesson 15 removes that advantage and shows the other side.

## Run it

```bash
python3 extractive.py
```

## What the code measures

Across the three guides, compression keeps 42.07 percent of the tokens and retains 10 of 10 key facts: the watering guide keeps 6 of 14 sentences including all 4 key facts, pruning 5 of 12 sentences with all 3, compost 4 of 10 sentences with all 3. At this aggressiveness, on query matched text, extraction is nearly free. Hold that thought loosely; it is about to meet a query free summarizer.

## Common failures

- Compressing without a query. Extraction ranked by a question keeps question shaped facts; Lesson 15 shows what happens without one.
- Quoting a compression ratio without a retention number. 0.42 of the tokens means nothing until paired with 10 of 10 facts.
- Assuming sentences are atomic. A fact split across two sentences can lose its other half to the budget line.

## Recap checklist

- [ ] You can state the measured compression ratio and key fact retention
- [ ] You can explain the home advantage this method had, in one sentence
- [ ] You know the failure mode extraction cannot have (invention) and the one it can (omission)

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
