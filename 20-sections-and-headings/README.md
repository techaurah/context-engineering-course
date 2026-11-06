# Lesson 20: Sections and headings: layout as a retrieval surface

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 19

Headings are usually filed under readability, a human concern. For a reader that must find things, layout is a retrieval surface: a heading is an index entry the model can match against the question before reading a word of the section. This lesson uses a labelled stand-in reader that does exactly that: asked about a topic, it looks for a matching heading and reads beneath it; faced with a flat wall, it falls back to the first sentence mentioning the topic, commas and all.

Six sections of Fernhill facts (delivery, returns, loyalty, cafe, workshops, trade) and six questions, one per section, each with one checkable answer. Flat versus headed. The result is not close, and the cost column holds a small surprise.

## Run it

```bash
python3 layout_lab.py
```

## What the code measures

The flat wall answers 2 of 6 questions correctly; the headed version answers 6 of 6. The flat reader kept landing on sentences that mention the topic in passing (the cafe hours are wrong because the first cafe mentioning sentence is about group bookings). Headings also cost less here: 186 tokens against the wall's 216, because the wall needed filler transitions to read as prose at all. Layout bought accuracy and saved tokens on the same run.

## Common failures

- Writing context as flowing prose because it feels professional. The reader is navigating, not appreciating.
- Headings that do not match question vocabulary. A heading is an index entry; 'Our story' indexes nothing a customer asks.
- Burying the one fact a section exists for in its third sentence. Even a headed reader reads the section top down.

## Recap checklist

- [ ] You can state both layouts' accuracy and token costs
- [ ] You can explain the flat reader's characteristic error (first mention wins)
- [ ] You know the heading rule: name sections the way questions are asked

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
