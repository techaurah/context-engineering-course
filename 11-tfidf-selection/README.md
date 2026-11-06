# Lesson 11: TF-IDF selection under a budget

Time: ~50 min | Difficulty: Intermediate | Prerequisites: Lesson 10

TF-IDF fixes overlap's known flaw: a word that appears in every document (the, Fernhill, customer) carries no selection signal, while a rare word (peat, hosepipe, wisteria) carries a lot. This lesson implements TF-IDF from scratch on the fixture corpus, then races it against raw overlap under a hard constraint neither faced in Lesson 10: a 400 token retrieval budget, filled greedily by score. Two metrics decide: fact coverage (are the needed facts inside the selected set at all) and stand-in recall (does the reader use them from where they landed).

The honest expectation management: on a small, clean, single topic corpus, overlap is already good, and weighting may buy little. The lesson measures whether that is true here rather than assuming the textbook method wins.

## Run it

```bash
python3 tfidf_lab.py
```

## What the code measures

Under the 400 token budget, both rankers reach fact coverage of 1.0 across the 8 tasks. Stand-in recall separates them slightly: TF-IDF 0.9969 against overlap 0.9906. The textbook method wins, by less than one percentage point, at the cost of implementing it. On this corpus that is the truth; on a larger, noisier corpus the gap usually widens, and the lesson's point is that you now own the harness that can tell you which world you are in.

## Common failures

- Adopting TF-IDF (or embeddings) on faith. The measured gap here is 0.0063 of recall; faith is not a measurement.
- Selecting without a budget. An unbounded selector is a preload with extra steps (Lesson 12 prices preload honestly).
- Judging selection on coverage alone. A fact can be covered and still land where the reader misses it; that is why recall is the second metric.

## Recap checklist

- [ ] You can explain in one sentence what the IDF half of TF-IDF does
- [ ] You can state both metrics and both scores under the 400 token budget
- [ ] You know when the heavier method is worth it (when your harness says so)

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
