# Lesson 12: Just-in-time context: identifiers first, content on demand

Time: ~50 min | Difficulty: Intermediate | Prerequisites: Lesson 11

Anthropic's guidance favours just-in-time retrieval: keep lightweight identifiers in the window and load content only when a step needs it, the way a person uses a filing cabinet instead of memorising it. The opposite is preload: put the whole knowledge base in every context and pay for all of it on every task. This lesson prices both honestly, then prices the thing JIT actually depends on and courses usually skip: the quality of the index the agent navigates by.

Three assemblies race across the 8 tasks. Preload: all 18 documents, always. JIT with a title only index: the agent sees 18 titles and loads the top matches. JIT with a keyword enriched index: titles plus each document's most common content words. The metric pair is mean tokens per task and fact coverage, and the trade between them is the entire lesson.

## Run it

```bash
python3 jit_lab.py
```

## What the code measures

Preload costs 2,212 tokens per task at coverage 1.0. The title index cuts that to 344 tokens per task but coverage falls to 0.8889 (16 of 18 required facts): at least one task's question shares no vocabulary with any title, so the agent loads the wrong documents confidently. The keyword index restores coverage to 1.0 at 832 tokens per task, still 62 percent cheaper than preload. JIT works, and its failure mode is not the loading; it is the map.

## Common failures

- Shipping JIT with a title only index and blaming retrieval when coverage drops. The index is the product.
- Comparing JIT to preload on tokens alone. The title index is cheapest and worst; the pair of metrics is the decision.
- Letting the index drift from the corpus. An index entry that no longer matches its document is a wrong turn the agent will take every time.

## Recap checklist

- [ ] You can state all three assemblies' tokens per task and coverage
- [ ] You can explain the title index's failure in vocabulary terms
- [ ] You know the keyword index's saving against preload (832 vs 2,212 tokens)

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
