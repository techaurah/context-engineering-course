# Lesson 16: Compacting conversation history: truncation, notes, and pinned facts

Time: ~50 min | Difficulty: Intermediate | Prerequisites: Lesson 15

Lesson 03 showed history breaking the budget at turn 30. Something must be done before then, and the options are the same three every agent framework offers: keep everything and pay, truncate the old turns and forget, or compact: replace the old turns with notes and pin the facts that must survive verbatim. This lesson races all three on the fixture conversation, a 24 turn tomato troubleshooting session whose 5 pinned facts (tap drips, 5 litre pots, cordon variety, budget, potash feed) are exactly the kind of constraints a support agent must not lose.

Survival is measured two ways: 5 probe phrases scattered through the conversation (midday sun, a tablespoon per litre, canes to the railing, plus two pinned markers) and the 5 pinned facts themselves. The strategies differ in what they keep, and the measurements show precisely what each choice forgets.

## Run it

```bash
python3 compaction.py
```

## What the code measures

Keeping everything costs 677 tokens and loses nothing. Truncating to the last 8 turns costs 267 tokens, keeps all 5 pinned facts (the conversation's own recap turn restates them, which real conversations do not always do), but loses 2 of 5 probes: the midday sun detail and the Epsom salt dose are gone. Rolling extractive notes plus a pinned block costs 528 tokens and loses nothing on either measure. Notes are not the cheapest option; they are the cheapest option that forgets nothing measured here.

## Common failures

- Truncating silently. The truncated agent does not know what it forgot; it will answer confidently from a partial history.
- Counting on the user to recap their constraints. This fixture's user did, at turn 22; yours will not.
- Compacting without a pinned list. Notes compress; pins preserve. The facts that must survive verbatim need naming, not hoping.

## Recap checklist

- [ ] You can state all three strategies' tokens and survival counts
- [ ] You can name the two probes truncation lost
- [ ] You know why the pinned facts survived truncation here, and why that was luck, not design

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
