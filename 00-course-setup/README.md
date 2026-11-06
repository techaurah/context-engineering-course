# Lesson 00: Course setup: what you need, and how this course works

Time: ~20 min | Difficulty: Beginner | Prerequisites: None

This course teaches context engineering by measuring it. Every claim it makes about selection, ordering, compression, or cost is the output of code in the lesson, run on the fixtures bundled in this repository, with a deterministic stand-in standing in for the model. If a technique measures badly here, the lesson prints the bad number and explains it. There are no borrowed benchmarks, no market statistics, and no certificate at the end.

Everything runs offline on the Python standard library. The shared instruments live in `ctx/` (a token counting approximation, a stand-in reader, assembly helpers) and the data lives in `fixtures/` (18 knowledge base documents carrying 72 checkable facts, 8 customer tasks, one 24 turn conversation, 3 prose guides, and a standard window budget). This lesson verifies your environment and counts the instruments, so later surprises are about ideas, not setup.

## Run it

```bash
python3 check_environment.py
```

## What the code measures

The check confirms Python 3.11 or newer and counts the fixtures: 18 documents, 72 facts, 8 tasks with 18 required fact slots between them, a 24 turn conversation with 5 pinned facts, and the standard 4,000 token teaching window from `fixtures/budgets.json`.

## Common failures

- Running a lesson's code from the repository root instead of its own folder. Each artifact finds the repo root by walking up from its own file, so it works from anywhere, but the smoke tests expect to run from the lesson folder.
- Expecting to install something. There is nothing to install; if you reach for pip, you have taken a wrong turn.
- Treating the stand-in reader as a real model. It is a labelled scoring rule (see `ctx/README.md`); lessons compare assembly decisions with it, never model behaviour.

## Recap checklist

- [ ] `python3 check_environment.py` runs and prints documents: 18 and facts: 72
- [ ] You can name the four fixture files and what each is for
- [ ] You know the course rule: every number comes from running the code

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
