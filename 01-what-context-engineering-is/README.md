# Lesson 01: What context engineering is: the anatomy of a window

Time: ~30 min | Difficulty: Beginner | Prerequisites: Lesson 00

Prompt engineering is the craft of one component: the instruction text. Context engineering is the discipline of the whole window: everything the model receives on a given turn, who put it there, what it costs, and whether it earns its place. Anthropic's applied AI team defines it as the set of strategies for curating and maintaining the optimal set of tokens during inference (Effective context engineering for AI agents, 29 September 2025; see RESEARCH.md). This lesson makes that definition physical by dissecting one assembled context.

The artifact builds a realistic support context for the first fixture task: a system prompt, tool definitions, a memory note, six turns of history, three retrieved documents, and the user's question. It then measures each component with the course tokenizer. The finding generalises: the parts teams argue about (system prompt wording) are usually the small parts. The parts nobody argues about (retrieval, history) are where the tokens, and the failures, live.

## Run it

```bash
python3 anatomy.py
```

## What the code measures

The assembled context totals 668 approx tokens. Retrieval is 374 of them (56.0 percent), history 156 (23.4 percent), the system prompt 50 (7.5 percent), tools 41 (6.1 percent), the user question 30 (4.5 percent), and the memory note 17 (2.5 percent). The component you write most carefully is 7.5 percent of what the model reads.

## Common failures

- Counting only the prompt. The prompt is one line item; the window is the budget.
- Assuming the user question is the main event. Here it is 30 of 668 tokens.
- Forgetting that history and retrieval grow on their own unless something engineers them.

## Recap checklist

- [ ] You can name the six components of an assembled context and their measured shares
- [ ] You can state the difference between prompt engineering and context engineering in one sentence
- [ ] You know which component dominates a typical support context, from measurement

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
