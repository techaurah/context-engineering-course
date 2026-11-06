# Lesson 18: Ordering: what the edges strategy actually buys, measured on all facts

Time: ~50 min | Difficulty: Intermediate | Prerequisites: Lesson 17

Ordering advice is usually given as folklore: put the best document first, or sandwich it, edges are prime real estate. This lesson tests the folklore with a metric most ordering advice never faces: not 'did the one needed fact survive' (its home turf, Lesson 05) but 'how much of everything you paid to include gets used at all', the mean stand-in use rate over every fact in the context. Three orderings race on full 18 document contexts per task: relevance descending, relevance ascending, and the edges strategy (best first, second best last, rest between).

Folklore should brace itself. The U curve rewards the edges, but a strategy that rearranges the middle also decides which documents get taxed, and when every document's facts count equally, the arithmetic is not kind to tricks.

## Run it

```bash
python3 ordering_lab.py
```

## What the code measures

Across the 8 tasks on full corpus contexts: relevance descending uses 0.7689 of included facts, ascending 0.7682 (the symmetry Lesson 05 predicts), and the edges strategy 0.7498, the worst of the three. Edges did not fail because position stopped mattering; it failed because it pushed ranks 3 and 4 into the exact middle to buy rank 2 a better seat. Ordering redistributes the position tax. It does not repeal it. Spend edges on the few facts that must survive (Lesson 19), not as a general arrangement.

## Common failures

- Applying edges ordering as a default layout. On the all facts metric it is a small, real loss.
- Testing orderings on small contexts. At 8 documents the three strategies were within 0.002 of each other here; only full size contexts separate them.
- Reporting ordering wins on the hero fact only. The other 68 facts in the context also paid rent.

## Recap checklist

- [ ] You can state all three strategies' all fact use rates
- [ ] You can explain why descending and ascending tie, and why edges loses
- [ ] You know the legitimate use of the edges (a few named facts, Lesson 19)

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
