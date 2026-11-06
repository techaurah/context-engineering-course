# Lesson 29: Capstone spec: the pipeline and its gates, fixed in advance

Time: ~40 min | Difficulty: Advanced | Prerequisites: Lesson 28

The capstone is a context pipeline for the Fernhill support agent: given any of the 8 fixture tasks, assemble a context from the 18 document knowledge base, inside the standard window, that a reader can actually use. This lesson builds nothing. Following the discipline of the whole course (and of Course 6, where the test suite's gates were fixed before the suite), it writes the specification and the gates into `capstone/gates.json` and validates them, before a single line of pipeline code exists.

Five gates, each traceable to a lesson: mean required fact recall at least 0.90 (Lessons 04, 05, 28), fact coverage at least 0.95 (Lesson 11), worst task recall at least 0.50 so no task is sacrificed to the mean (Lesson 28), mean total tokens at most 1,000 (Lessons 03 and 12), and mean precision at least 0.15 (Lesson 28). The definitions in the gates file pin every term to a course instrument, so Lesson 31's verdict is arithmetic, not opinion.

## Run it

```bash
python3 capstone_spec.py
```

## What the code measures

The spec validates: 5 gates named, the scenario bound to the 8 fixture tasks and 18 documents, and the fixed before build date recorded in the gates file itself. If the pipeline in Lesson 30 fails a gate, Lesson 31 reports the failure and hardens the pipeline; the gates do not move. That immovability is the entire point of writing them first.

## Common failures

- Writing gates after seeing results. A gate fitted to the outcome certifies the outcome, not the pipeline.
- Gating on the mean alone. The worst task gate exists because a pipeline that aces 7 tasks and abandons 1 is a support incident with good averages.
- Leaving a term undefined. Every gate term here names its instrument (stand-in, tokenizer, gold set), so the verdict can be recomputed by a stranger.

## Recap checklist

- [ ] You can list the five gates and the lesson each one comes from
- [ ] You know where the gates live and what 'fixed in advance' is dated
- [ ] You can explain the worst task gate's purpose in one sentence

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
