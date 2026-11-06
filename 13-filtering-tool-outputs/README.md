# Lesson 13: Filtering tool outputs: the cheapest tokens are the ones you never admit

Time: ~45 min | Difficulty: Intermediate | Prerequisites: Lesson 12

Tool results are the least designed text in most agents: a catalogue API answers with every field it has, and the agent pastes the whole thing into the window, where it taxes every later fact through rot and shoves better content toward the middle. This lesson takes one simulated verbose search result (12 products, 9 fields each) and one concrete job (find the cheapest in stock 40 litre compost) and races four admission policies against it.

The policies: admit raw; truncate to the first 3 rows; select the 4 fields the job needs; and filter rows to the job plus select fields. Truncation is what most agents do under pressure, and its result here is the cautionary tale.

## Run it

```bash
python3 tool_output_filter.py
```

## What the code measures

Raw admission costs 1,231 tokens and finds the answer (CMP-40-C, the 5.50 value compost). Truncating to 3 rows costs 315 tokens and loses the answer entirely: the right row was sixth. Field selection keeps the answer at 506 tokens. Filtering plus field selection keeps it at 219 tokens, an 82 percent saving on raw with the same correct answer. The order of operations matters: filter by relevance first, then strip fields; never truncate by position and call it filtering.

## Common failures

- Truncating tool output by length or row count. Position is not relevance; the answer was row 6 of 12.
- Admitting fields nobody reads. Nine fields per row down to four is half the cost gone, before any cleverness.
- Filtering after admission. The saving only exists if the tokens never enter the window.

## Recap checklist

- [ ] You can state all four policies' token costs and which ones kept the answer
- [ ] You can explain why truncation failed in positional terms
- [ ] You know the order: filter rows, then select fields

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
