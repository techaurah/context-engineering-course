# Lesson 31: Evaluate and harden: the verdict, the failure, and the fix

Time: ~60 min | Difficulty: Advanced | Prerequisites: Lesson 30

This lesson runs the capstone against the gates fixed in Lesson 29, and it keeps the whole history in its output: the pre course baseline (wall prompt, everything preloaded), the pipeline as first built, the failure that history contains, and the hardened pipeline that Lesson 30 now ships. Nothing is edited out. A gate failed on the first run of a real pipeline in this course, and the correct response to that is what this lesson demonstrates: diagnose the failing term, change the assembly for a stated reason, remeasure everything, and keep the old numbers in print.

The diagnosis, in advance of your run: as built, the selector spent its entire 900 token retrieval budget on every task, admitting seven documents when one carried the facts. Recall and coverage were perfect; precision, the share of paid tokens that were relevant, was starved by the generosity. The fix is a relevance floor (Lesson 30 documents it), and this lesson's gate table is the proof of whether the fix worked or merely helped.

## Run it

```bash
python3 evaluate_capstone.py
```

## What the code measures

Baseline (wall prompt, preload): recall 0.8781, 2,292 tokens, precision 0.055. As built: 4 of 5 gates passed, failing precision at 0.1326 against the gate's 0.15, at 952 mean tokens. Hardened with the relevance floor: 5 of 5 gates pass, recall 1.0, coverage 1.0, worst task 1.0, mean tokens 572, precision 0.2988. Both orderings (descending, edges) tie under the floor, so the simpler descending order ships. The course ends where it began: every number above came from running the code, and the one failure in the run is printed in the same size type as the passes.

## Common failures

- Moving the gate. The precision gate stayed at 0.15; the pipeline moved. That ordering of events is the whole discipline.
- Reporting only the hardened run. The as built failure is the evidence the hardening was necessary; deleting it deletes the reason.
- Declaring victory on the mean. The gate table includes the worst task, and it passed at 1.0, which is a stronger claim than the mean's.

## Recap checklist

- [ ] You can state the baseline, as built, and hardened rows from memory of the table
- [ ] You can name the gate that failed, its value, and its threshold
- [ ] You can explain the relevance floor fix and why descending order shipped over edges

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
