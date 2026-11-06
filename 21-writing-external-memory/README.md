# Lesson 21: Writing external memory: notes that outlive the window

Time: ~45 min | Difficulty: Intermediate | Prerequisites: Lesson 20

Context engineering's write operation (LangChain's taxonomy, RESEARCH.md) means saving context outside the window so a later window can use it. The alternative is hoping the conversation stays short, which Lesson 03 priced. This lesson runs the two session pattern honestly: session 1 is the fixture tomato conversation; during it, the agent writes structured notes (five fields extracted from the pinned facts). Session 2 starts fresh, reads only the notes, and faces five checks about the customer's constraints. The baseline is a fresh session with no notes, answering from generic defaults, the way real fresh sessions guess.

The checks are the customer's actual constraints (watering by can, 5 litre pots, cordon variety, 20 pound budget, high potash weekly feed). A fresh session that guesses them wrong does not just err; it advises repotting a fruiting plant and blowing the budget, politely and confidently.

## Run it

```bash
python3 memory_notes.py
```

## What the code measures

With the notes, session 2 answers 5 of 5 checks correctly. Without them, 0 of 5: every generic default is wrong for this customer. The notes cost 111 tokens against the 677 token transcript they replace, so the write operation is also the cheapest compaction in the course, with one difference from Lesson 16: these notes are written for a future session's questions, which were knowable in advance (constraints, preferences, decisions), and that knowability is what makes external memory work.

## Common failures

- Writing notes as a prose diary. Session 2 needs fields it can look up, not a story to reread (Lesson 22 prices formats properly).
- Noting what was said instead of what was decided. The checks ask about constraints and decisions, not about the conversation.
- Keeping memory only inside the window. A window is a session; memory that dies with it is just history with ambition.

## Recap checklist

- [ ] You can state the with notes and without notes check scores and both token costs
- [ ] You can name the five fields the notes carried and why those five
- [ ] You know the class of facts worth writing externally (constraints, preferences, decisions)

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
