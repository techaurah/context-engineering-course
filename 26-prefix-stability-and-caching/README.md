# Lesson 26: Prefix stability and caching: layout decisions with a price tag

Time: ~50 min | Difficulty: Advanced | Prerequisites: Lesson 25

Most providers offer a prompt cache: if this turn's context begins with exactly the tokens last turn began with, the shared prefix is billed at a steep discount (Anthropic's advanced tool use writing reports on demand loading and caching changing real bills; RESEARCH.md). That makes layout a pricing decision: anything that changes early in the context (a timestamp in the system prompt, a rotating section order, a fresh summary pasted at the top) invalidates the prefix for everything after it. This lesson simulates the mechanism over the 24 turn fixture conversation, with labelled illustrative prices (1.00 per 1,000 fresh tokens, 0.10 per 1,000 cached), not any provider's price list.

Two layouts race. Stable: system, tools, memory, then growing history, identical order every turn. Churned: a per turn session tick inside the system text and a section order that rotates turn by turn, the two habits real codebases have by accident. The simulator credits a turn with cached tokens up to the longest exactly matching prefix, segment by segment.

## Run it

```bash
python3 cache_sim.py
```

## What the code measures

Over 24 turns the stable layout processes 1,449 cached tokens and 6,526 fresh, for a cost of 6.671 units. The churned layout gets 0 cached tokens and pays 8.119 units, 1.217 times the stable cost, for identical content and identical answers. Nothing about the model changed; the bill moved 22 percent on layout alone. The stable layout's cache hits are modest (only the fixed head is reusable while history grows), which is the honest second half of the lesson: stability is necessary for caching, not sufficient for a big discount.

## Common failures

- Putting timestamps, request ids, or dates in the system prompt. Each one is a cache invalidator wearing a label.
- Reordering sections per turn (alphabetical sorts, hash order, freshest first). Rotation measured here cost 22 percent.
- Pasting the newest content at the top for recency and paying for it twice: once in cache loss, once in rot position. Put volatile content late.

## Recap checklist

- [ ] You can state both layouts' cached tokens and costs, and the ratio
- [ ] You can name the two churn habits and why each breaks the prefix
- [ ] You know the layout rule (stable and boring first, volatile last) and its limit

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
