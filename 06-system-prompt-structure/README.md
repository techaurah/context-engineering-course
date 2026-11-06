# Lesson 06: The system prompt: structure, altitude, and the verbatim test

Time: ~45 min | Difficulty: Intermediate | Prerequisites: Lesson 05

Anthropic's guidance puts the system prompt at a Goldilocks altitude: specific enough to give behavioural signals, not so rigid it hardcodes the task, organised into sections, and built up from observed failures. This lesson tests a claim underneath that guidance: structure is first about verifiability. If your rules cannot be extracted and checked mechanically, you cannot regression test them, diff them, or even prove they are in the prompt at all.

The artifact carries the same six rules two ways: dissolved into one rambling paragraph (the wall), and as a headed list with one RULE line each (the structured version). It measures three things: token cost, how many rules a mechanical checker can extract verbatim, and how often the stand-in uses the rules inside a realistic context. Keep all three numbers in view; the honest result is not the one most prompt advice predicts.

## Run it

```bash
python3 prompt_structure.py
```

## What the code measures

The wall costs 288 tokens and yields 0 of 6 rules to the verbatim checker. The structured prompt costs 111 tokens and yields 6 of 6, saving 177 tokens. Rule recall in context is 1.0 for both: at this size, structure did not change what the stand-in used. The measured case for structure is cost and auditability, not magic compliance, and any course that promises more than that is selling something.

## Common failures

- Claiming structure improves obedience without measuring it. Here it did not, at this context size, and the lesson says so.
- Writing rules that cannot be checked. A rule a checker cannot find is a rule you cannot test (Course 6 territory: prompts as data).
- Burying a new rule mid paragraph during an incident fix. It will be neither found nor diffed later.

## Recap checklist

- [ ] You can state the three measured differences between the wall and the structured prompt
- [ ] You know which benefit of structure was NOT measured here (obedience at this size)
- [ ] You can write a rule a mechanical checker can extract

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
