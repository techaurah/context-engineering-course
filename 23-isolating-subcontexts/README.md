# Lesson 23: Isolating subcontexts: clean windows, and the question nobody asked

Time: ~50 min | Difficulty: Advanced | Prerequisites: Lesson 22

Isolation, the fourth context operation, splits work across separate windows: sub-agents with clean contexts return condensed summaries, and the coordinator's window stays small (Anthropic's multi agent pattern; RESEARCH.md). This lesson builds the pattern with scripted stand-in sub-agents and then does the unfashionable thing: it sets the final task after the sub-questions were written, the way real requirements arrive, and measures what the summaries cannot answer.

Three sub-agents each read one document (trade, delivery, compost) and answer one sub-question (payment terms, delivery days, bulk format), returning one summary line each carrying only the fact asked about. The coordinator's final task is to price a trade plant order with delivery, which needs the trade discount and the free delivery threshold: two facts that exist in the documents, that a single context holds easily, and that no sub-question mentioned.

## Run it

```bash
python3 isolation.py
```

## What the code measures

In a single 376 token context, the final task's facts score recall 1.0. Isolated, the sub-questions' own facts score 1.0 in the combiner, and the final task's facts score 0.0: they were never written into any summary. The combiner window is tiny (37 tokens) and the total processed is 413 tokens, so isolation delivered its promised efficiency and a total, silent failure on the actual task. The failure is not in the sub-agents, which answered perfectly. It is in the decomposition, which guessed the future wrong.

## Common failures

- Decomposing by topic instead of by the decision the context must support. The sub-questions were tidy; the task was elsewhere.
- Treating summaries as lossless. A summary is a bet on future questions; this lesson is what a lost bet looks like (0.0, no error raised).
- Isolating to save tokens on small problems. The single context cost 376 tokens and was right; isolation processed 413 and was wrong.

## Recap checklist

- [ ] You can state the single context and isolated results for both fact sets
- [ ] You can explain why the failure was silent (every sub-agent succeeded)
- [ ] You know the condition isolation needs (sub-questions that cover the final task's facts)

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
