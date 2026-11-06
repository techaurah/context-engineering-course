# Lesson 04: Context rot: the cost of length itself

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 03

A bigger window does not mean the model uses all of it equally well. Chroma's 2025 context rot study (18 models; see RESEARCH.md) found performance degrading steadily as input grows, even on simple tasks, well inside the advertised window. The stand-in reader implements that finding as an explicit rule: every fact's use score drops by 0.045 per 1,000 tokens of total context. This lesson measures the rule so later lessons can budget against it.

The design isolates size from position: the target document sits in the middle of the context, half the padding before it and half after, and padding cycles the other fixture documents the way real contexts repeat boilerplate and old tool output. Only the total changes. Watch what happens to the same three required facts as the total climbs.

## Run it

```bash
python3 rot_experiment.py
```

## What the code measures

Recall of the delivery task's facts starts at 1.0 with the document alone (124 tokens), falls to 0.7 at 1,161 tokens, 0.1833 at 2,212 tokens, and 0.0 from 4,300 tokens upward. The drop is monotone and totals a full 1.0 across the sweep. Nothing about the facts changed; only the amount of other text did. That is rot, measured on the stand-in's published rule.

## Common failures

- Reading rot as a cliff. It is a gradient: the damage at 2,000 tokens is already most of the story.
- Padding with irrelevant text to look thorough. Every padded token taxes every fact already present.
- Blaming the document. The same document scores 1.0 alone and 0.0 in a crowd.

## Recap checklist

- [ ] You can state the stand-in's rot rule and the measured recall at 124, 2,212, and 4,300 tokens
- [ ] You can explain why this experiment holds position constant
- [ ] You know why 'the window allows it' is not an argument for including something

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
