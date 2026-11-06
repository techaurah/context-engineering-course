# Lesson 05: Lost in the middle: position effects, measured

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 04

Liu et al. (Lost in the Middle, TACL 2024) moved one answer bearing document through a fixed set and found a U-shaped curve: models use information at the start and the end of the context far more reliably than information in the middle. The stand-in implements that as its position weight, 1.00 at the edges and 0.66 in the exact middle. This lesson reproduces the experiment shape on the fixture corpus so you can see the curve your later ordering decisions are up against.

The loyalty document, carrying the two facts the loyalty task needs, is placed at each of the 10 positions in a fixed 10 document context. Everything else is identical. Only the position changes, so only position can explain the curve.

## Run it

```bash
python3 position_sweep.py
```

## What the code measures

Recall is 1.0 at positions 1, 2, 3, 9, and 10, dips to 0.7 at position 5 and 0.65 at position 6, and recovers toward the end. The U-shape gap between the weaker edge and the middle minimum is 0.35. The effect on the stand-in is smaller than the paper's worst cases and larger than zero, which is the honest shape of it: position is a tax, not a death sentence, and later lessons spend it deliberately.

## Common failures

- Concluding the middle is unusable. At 0.65 the middle fact is used two trials in three; the tax is real but payable when the content matters.
- Testing orderings on tiny contexts. At a few hundred tokens the curve flattens and every ordering looks equal (Lesson 18 hits this honestly).
- Fixing position by repeating everything everywhere. Repetition costs tokens and adds rot; Lesson 19 spends it on one rule, deliberately.

## Recap checklist

- [ ] You can sketch the measured U curve and name its minimum and gap
- [ ] You can name the paper and the stand-in rule that implements it
- [ ] You know the two positions worth spending on purpose

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
