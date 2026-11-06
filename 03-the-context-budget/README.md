# Lesson 03: The context budget: accounting for a finite window

Time: ~40 min | Difficulty: Beginner | Prerequisites: Lesson 02

A context window is finite, and everything in Lesson 01's anatomy competes for the same tokens. A budget turns that competition into accounting: each component gets an allowance, a reserve is held back for the answer, and growth in one component is a visible decision instead of a surprise. `fixtures/budgets.json` holds the course's standard budget: a 4,000 token teaching window (deliberately small, so pressure is real) split into system 350, tools 450, memory 300, retrieval 1,600, history 800, and a 500 token output reserve.

The artifact charges the fixed components at their allowances, then grows history turn by turn through the scripted conversation, twice over to model a long session. It reports the exact turn where history breaks its own allowance and the turn where the whole window, reserve included, breaks. The two turns are close, and that closeness is the lesson: an unbudgeted component does not grow into empty space, it grows into everyone else's allowance.

## Run it

```bash
python3 budget_ledger.py
```

## What the code measures

History breaks its 800 token allowance at turn 30, and the window net of reserve breaks at the same turn. After 48 turns history alone is 1,354 tokens and the ledger totals 4,054 against the 4,000 window: over budget by 54 tokens with retrieval still at its allowance. Nothing failed loudly; the budget simply ran out, which is how real context failures arrive.

## Common failures

- Budgeting the window as one number. Component allowances are what make growth visible and negotiable.
- Spending the output reserve on input. A window full of context and no room to answer is a failed turn, not a full one.
- Letting history grow by default. Every long running agent needs an explicit history policy (Lesson 16) chosen before the budget forces one.

## Recap checklist

- [ ] You can read a budget ledger and name which component is over allowance
- [ ] You know the measured turn where the scripted conversation breaks the standard budget
- [ ] You can explain why a reserve is part of the budget, not a rounding error

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
