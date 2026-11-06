# Lesson 10: Selection as a ranking problem

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 09

Selection is the first of LangChain's four context operations (write, select, compress, isolate; see RESEARCH.md), and it is a ranking problem before it is anything else: score every candidate against the task, take the top of the ranking, and know what the ranking costs you when it is wrong. This lesson builds the simplest honest ranker, word overlap between the question and each document, and measures it against the fixture gold set, where every task names the documents its facts live in.

The metric is recall at k: for how many of the 8 tasks does the relevant document appear in the top k of the ranking? It is the selection equivalent of a smoke test, and it sets the baseline every cleverer method in the next lessons has to beat.

## Run it

```bash
python3 ranking.py
```

## What the code measures

Word overlap puts the relevant document at rank 1 for 7 of 8 tasks, and inside the top 2 for all 8. On this corpus, the simple ranker is already strong, which is exactly why it is the baseline: any heavier machinery (embeddings, rerankers) must beat top 2 of 8 tasks at 100 percent to justify itself here, and on many real corpora it will instead win on the tasks where vocabulary mismatches, which this corpus has few of.

## Common failures

- Selecting by document order or recency because it is easy. A ranking you cannot score is a selection you cannot defend.
- Measuring selection by vibes. Recall at k against a named gold set is cheap and settles arguments.
- Assuming a fancier ranker is better before it beats the overlap baseline on your own tasks.

## Recap checklist

- [ ] You can state the measured recall at 1 and recall at 2 of the overlap ranker
- [ ] You can explain what a gold set is and why selection needs one
- [ ] You know what any heavier ranker must beat on this corpus

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
