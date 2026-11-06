# Lesson 02: Counting tokens: the approximation, and when it is good enough

Time: ~35 min | Difficulty: Beginner | Prerequisites: Lesson 01

Every decision in this course is denominated in tokens, so the course needs a way to count them offline, with no tokenizer library and no network. `ctx/tokenizer.py` implements a documented approximation: letter runs cost about one token per four characters, digit runs one per three, punctuation one each. It is labelled an approximation everywhere it is used, and this lesson measures how it behaves before you trust it with budgets.

The artifact runs the approximation, a raw word count, and the popular characters divided by 4 heuristic over all 21 bundled texts (3 guides plus 18 documents) and compares them. Two lessons fall out: tokens per word is not a constant, and the cheap heuristic is close until it is not, in a specific direction you can measure.

## Run it

```bash
python3 tokenizer_lab.py
```

## What the code measures

Across the 21 texts (3,051 approx tokens in total), the approximation lands between 1.494 and 1.776 tokens per word depending on the text, a spread wide enough to sink any budget built on a single ratio. The characters/4 heuristic's worst relative error against the approximation is 0.156, about 16 percent under on the worst text. For budgeting with headroom, the approximation is good enough. For billing, it would not be, and the course never uses it for billing.

## Common failures

- Quoting an approx count as a model's real token count. Different tokenizers split differently; the approximation is for decisions, not invoices.
- Using one tokens per word ratio for every text. The measured spread is 1.494 to 1.776 on ordinary prose.
- Counting characters for code or data. Structured text tokenizes differently from prose; measure the actual payload.

## Recap checklist

- [ ] You can explain how the approximation splits text and why digits cost more per character
- [ ] You have seen the measured tokens per word spread across 21 texts
- [ ] You know the two jobs the approximation is fit for (budgeting, comparison) and the one it is not (billing)

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
