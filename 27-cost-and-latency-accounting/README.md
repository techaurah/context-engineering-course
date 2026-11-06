# Lesson 27: Cost accounting: read a run like a ledger

Time: ~45 min | Difficulty: Advanced | Prerequisites: Lesson 26

By now every component has been priced separately. This lesson puts them in one ledger: a simulated 12 step support run, charged per step for system and tools, replayed history, tool results, and the question, using per result costs taken from Lesson 25's own measurements (205 tokens raw, 75 compact, per result). Prices are again the labelled illustrative constant, 1.00 unit per 1,000 tokens. The point is not the total; it is the shares, because the shares decide which earlier lesson to apply next.

Two runs: raw tool results, and compact ones. The saving is real and worth taking. But read the dominant line in both runs before celebrating: the biggest cost in a long run is not the thing teams usually optimise first.

## Run it

```bash
python3 run_ledger.py
```

## What the code measures

The raw run totals 13,488 tokens (13.488 units): history replay is 66.5 percent, tool results 18.2 percent, system and tools 12.5 percent. The compact run totals 9,750 tokens, saving 3.738 units (27.7 percent), and history replay's share rises to 69.7 percent because everything else shrank around it. The dominant component in both runs is replayed history, which is Lesson 16's compaction problem, not a tool schema problem. Accounting's job is to stop you optimising the 18 percent line while the 66 percent line grows.

## Common failures

- Optimising components in the order you notice them. The ledger orders them by size; work the list top down.
- Counting a run's cost once, at design time. Shares move as runs lengthen; history's share grows with every step, which is the entire plot.
- Reporting cost without the counterfactual. The 3.738 unit saving is only meaningful against the raw run measured the same way.

## Recap checklist

- [ ] You can state both runs' totals and the saving in units and percent
- [ ] You can name the dominant component in both runs and the lesson that treats it
- [ ] You know why shares, not totals, drive the optimisation order

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
