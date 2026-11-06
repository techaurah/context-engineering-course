# Lesson 24: The cost of tool definitions: tokens, overlap, and the twin problem

Time: ~50 min | Difficulty: Advanced | Prerequisites: Lesson 23

Tool definitions are context: they sit in the window on every turn, before the conversation starts. Anthropic's advanced tool use writing gives a five server example at about 55K tokens of definitions (RESEARCH.md), and advises minimal, non overlapping tools. This lesson miniaturises the problem to two Fernhill catalogues: a verbose 8 tool set that grew by accretion, with descriptions that repeat each other, and a trimmed 5 tool set written against the advice. A stand-in chooser (word overlap between request and description) does the picking, and a dedicated twin probe aims requests at the most overlapped pair.

Three measurements: definition tokens, general choice accuracy, and the twin probe. The middle one refuses to flatter the trimmed catalogue, and the lesson keeps that refusal in print.

## Run it

```bash
python3 tool_catalog.py
```

## What the code measures

The verbose catalogue costs 428 definition tokens; the trimmed one 187, a 56 percent saving on every turn of every session. Worst pair overlap falls from 0.529 (lookup_order vs lookup_delivery, the twins) to 0.154. The twin probe improves from 4 of 6 to 5 of 6, with merging making one confusion class impossible by construction. But general choice accuracy is 4 of 8 for BOTH catalogues: the remaining misses are vocabulary mismatches between how customers ask and how descriptions are written, and no amount of trimming fixes that. Definitions are a budget line and a confusion surface, not a substitute for matching user language.

## Common failures

- Letting the catalogue grow by accretion. Every added tool is a per turn tax plus a new overlap surface.
- Keeping twin tools because two teams own them. lookup_order and lookup_delivery at 0.529 overlap is one tool wearing two names.
- Expecting trimming to fix vocabulary mismatch. The 4 of 8 tie says otherwise; that failure wants description rewriting toward customer words, measured separately.

## Recap checklist

- [ ] You can state both catalogues' definition tokens and worst pair overlaps
- [ ] You can state the twin probe scores and the honest tie on general choices
- [ ] You can name the two different diseases (overlap, vocabulary mismatch) and which cure treats which

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
