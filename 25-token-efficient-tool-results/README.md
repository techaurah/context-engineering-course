# Lesson 25: Token-efficient tool results: design the answer, not the dump

Time: ~45 min | Difficulty: Advanced | Prerequisites: Lesson 24

Lesson 13 filtered one tool result by hand. This lesson makes it a schema decision, applied by the tool itself across all 8 fixture tasks: a search tool that can answer in a verbose schema (full document text plus seven metadata fields per hit) or a compact schema (the document id plus only the fact lines whose words match the question). The metric pair is the course's standard: mean tokens per task and required fact coverage.

The compact schema carries a risk Lesson 13's single job could not show: a required fact whose wording shares no words with the question would be filtered out by its own tool. Across 8 tasks, does that happen? The coverage number answers, and it is the number that decides whether the schema ships.

## Run it

```bash
python3 result_schemas.py
```

## What the code measures

The verbose schema costs 614 tokens per task at coverage 1.0. The compact schema costs 224 tokens per task, a 64 percent saving, also at coverage 1.0: on this corpus no required fact was worded so differently from its question that the filter dropped it. That is a corpus property, not a law, and the lesson's deliverable is the harness that would catch the day it stops being true: run the coverage check on every task set change, the way you would run a test.

## Common failures

- Returning full documents from a search tool because the caller 'might need them'. The caller pays for might on every task.
- Filtering inside the tool with no coverage harness. A filter without a gold set is a hope with a schema.
- Confusing compact with truncated. Compact selects by the question; truncating selects by position (Lesson 13's failure, again).

## Recap checklist

- [ ] You can state both schemas' tokens per task and coverage
- [ ] You can name the risk the compact schema runs and the harness that guards it
- [ ] You know the saving (614 to 224 tokens) is per task, recurring

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
