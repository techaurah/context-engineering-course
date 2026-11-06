# Lesson 30: Build the capstone pipeline

Time: ~60 min | Difficulty: Advanced | Prerequisites: Lesson 29

The pipeline assembles each task's context in four moves, one per course module: a structured system prompt with verbatim checkable rules (Lesson 06), TF-IDF selection under a 900 token retrieval budget (Lesson 11), a relevance floor that stops the selector spending the budget on weak documents (the hardening Lesson 31 motivates and this file documents), and a fixed layout: system first, documents by score, question last (Lessons 18 to 20). No step is new; the capstone is the course, composed.

Evaluation is Lesson 28's harness extended with coverage and the worst task, exactly the gate terms. The shipped configuration uses the relevance floor of 0.25 (a document must score at least a quarter of the top document's score to be admitted). Run the artifact and read the per task table before Lesson 31 delivers the verdict, and note the wedding task: only 2 documents selected, 335 tokens, the floor doing visible work.

## Run it

```bash
python3 context_pipeline.py
```

## What the code measures

Shipped configuration, across the 8 tasks: mean recall 1.0, mean coverage 1.0, worst task recall 1.0, mean total tokens 572, mean precision 0.2988. Against Lesson 28's simple overlap top 2 (306 tokens, recall 1.0), the pipeline spends more tokens; what it buys is a budget contract, a relevance rule instead of a fixed count, and a spec it can be gated against, which is the difference between a trick that works on this corpus and an assembly that can be defended on the next one.

## Common failures

- Hardcoding top k because it won Lesson 28. A fixed count is a corpus bet; a budget plus a floor is a policy.
- Tuning the floor on the gate tasks and calling it validation. The floor is documented in the code as a hardening choice with its reason, and the gates were fixed before it existed.
- Skipping the per task table for the means. The worst task gate exists because means hide funerals.

## Recap checklist

- [ ] You can name the pipeline's four moves and the lesson each comes from
- [ ] You can state the shipped configuration's five headline metrics
- [ ] You can explain what the pipeline buys over overlap top 2, honestly, including its token cost

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
