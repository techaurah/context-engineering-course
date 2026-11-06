# Lesson 08: Few-shot examples: buying accuracy with tokens

Time: ~45 min | Difficulty: Intermediate | Prerequisites: Lesson 07

Examples are context too, and they are bought by the token like everything else. This lesson treats few-shot prompting as a purchasing decision: a stand-in classifier (nearest example by word overlap, labelled as such) labels support messages, and the artifact varies the number of examples in the prompt from 0 to 10, measuring accuracy and example tokens at each step. The curve, not any single point, is the lesson.

The zero example baseline is not magic either: with no examples the stand-in falls back to the majority label in the pool, which is what a model with no signal effectively does, guess the common case. Watch where the curve bends, and what the last four examples buy.

## Run it

```bash
python3 fewshot_lab.py
```

## What the code measures

Accuracy climbs from 0.25 with no examples to 0.5 at 2, 0.875 at 4, and 1.0 at 6 examples (82 tokens). Examples 8 and 10 keep accuracy at 1.0 while raising the cost to 111 and 141 tokens. The best purchase on this task set is 6 examples; the last 59 tokens buy exactly nothing. Every example past the bend is a recurring per request cost for zero measured gain.

## Common failures

- Copying a fixed example count from a tutorial. The right count is where YOUR curve bends, measured on YOUR task set.
- Adding examples to fix a classification the examples do not cover. Coverage of the label space matters more than count.
- Forgetting examples are paid on every request. A one time accuracy gain can be a permanent cost line.

## Recap checklist

- [ ] You can read the measured accuracy curve and name the bend (6 examples, 82 tokens)
- [ ] You can state what examples 8 and 10 bought (nothing, for 59 more tokens)
- [ ] You know the zero example baseline's behaviour and why it scores 0.25

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
