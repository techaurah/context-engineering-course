# Lesson 28: Measuring context quality: recall, precision, and cost per success

Time: ~50 min | Difficulty: Advanced | Prerequisites: Lesson 27

Every lesson has measured one decision at a time. Real assembly is all of them at once, so the course needs one harness that scores whole assemblies on the three numbers a context engineer actually trades: recall (of the facts a task needs, how many does the reader use), precision (of the tokens you paid for, how many were relevant), and cost (tokens per task). This lesson builds that harness and scores three assemblies of increasing sophistication: preload everything, overlap top 3, overlap top 2.

The results set the table for the capstone. Preload's recall is the surprise in the row: the assembly with every fact present scores worst on facts used, because presence is not use, and its precision is dismal. Selection wins on all three axes here, which raises the capstone question properly: can a principled pipeline beat these quick selections against gates fixed in advance?

## Run it

```bash
python3 quality_harness.py
```

## What the code measures

Preload all: recall 0.8875, 2,268 mean tokens, precision 0.0556. Overlap top 3: recall 0.9906, 432 tokens, precision 0.2919. Overlap top 2: recall 1.0, 306 tokens, precision 0.4123. Read the preload row twice: it contains every required fact (coverage 1.0) and still loses a ninth of them to position and rot. That single row is the course in miniature, and it is why the capstone's gates are written against recall and precision, not coverage alone.

## Common failures

- Scoring assemblies on coverage. Coverage says the fact was in the building; recall says it was in the room.
- Scoring on recall alone. Top 2 wins recall here, but on a corpus where tasks need 3 documents it would fail coverage; the capstone gates therefore include both.
- Comparing assemblies measured on different task sets. The harness is only a referee because all three rows faced the same 8 tasks.

## Recap checklist

- [ ] You can state all three assemblies' recall, tokens, and precision
- [ ] You can explain preload's paradox (coverage 1.0, recall 0.8875) in one sentence
- [ ] You know the three metrics the capstone gates are built from

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
