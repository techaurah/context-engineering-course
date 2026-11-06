# Lesson 19: Anchors and repetition: spending 19 tokens to rescue a rule

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 18

Lesson 18 ended with a legitimate use for the edges: a few named facts that must survive. This lesson is that case, in its purest form. One rule (refunds land three to five working days after the return is scanned) must be used at the end of a roughly 3,000 token context. Three placements race: the rule at the very start, the rule stranded in the middle where long histories naturally leave such instructions, and the middle placement plus a verbatim repeat of the rule at the very end, the sandwich.

Repetition is usually discussed as a smell. Here it is a priced instrument: the repeat costs exactly what it costs, and the stand-in reports exactly what it buys. Decide from the numbers.

## Run it

```bash
python3 anchors.py
```

## What the code measures

The rule at the start is used at rate 1.0 (primacy protects it; the start is the one seat that needs no help). Stranded in the middle, the same rule's use rate is 0.0 across 40 trials: at 3,000 tokens the middle weight minus rot never clears the threshold. Repeating it at the end restores the rate to 1.0. The repeat costs 19 tokens. Nineteen tokens is the measured price of rescuing a rule that position and rot had fully buried.

## Common failures

- Repeating everything, everywhere. Repetition is a targeted spend on named must-survive facts; sprayed around, it becomes the rot it fights.
- Assuming a rule stated once at the start stays in force after 3,000 tokens of history. The middle is where old instructions go to be ignored.
- Sandwiching as superstition. It works here for a stated reason (the second copy sits in the recency seat) and at a stated price.

## Recap checklist

- [ ] You can state the three placements' use rates and the repeat's token price
- [ ] You can explain why the start placement needed no rescue
- [ ] You can name the condition that makes repetition rational (named fact, big context, cheap copy)

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
