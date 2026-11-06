# Lesson 22: Memory formats: the reader is part of the format

Time: ~45 min | Difficulty: Intermediate | Prerequisites: Lesson 21

Lesson 21 wrote the notes; this lesson asks what shape they should be stored in, and refuses to answer without a reader in the room. The same six order records (with surnames like 'Shah, Priya', commas included, the way real names arrive) are stored four ways and queried six times: as prose, as CSV read by a naive split, as the same CSV read by a proper parser, and as quoted CSV, plus JSON. Some of these combinations fail completely, and the failures are the curriculum.

Two distinct morals hide in the table. One is about writers: unquoted CSV with commas inside values is broken at write time, and no reader, however proper, can rescue it; the parser faithfully reads the wrong columns. The other is about price: the most robust format costs two and a half times the tokens of the cheapest correct one.

## Run it

```bash
python3 memory_formats.py
```

## What the code measures

Prose: 6 of 6 lookups at 90 tokens. CSV with a naive reader: 0 of 6, every surname comma shifts the status column. The same unquoted CSV with a proper CSV reader: still 0 of 6, because the file itself is malformed. Quoted CSV with the proper reader: 6 of 6 at 92 tokens. JSON: 6 of 6 at 217 tokens. The robust and cheap winner is quoted CSV; JSON's premium buys schema strictness that six flat records do not need, the Lesson 07 result wearing a memory costume.

## Common failures

- Blaming the reader for a writer's bug. The unquoted file fails under both readers; the defect was committed at write time.
- Storing memory in whatever the model emitted. The model will emit commas in names forever; the format must survive its own data.
- Defaulting to JSON for flat state. It measured 217 tokens against quoted CSV's 92 for identical lookup accuracy.

## Recap checklist

- [ ] You can state all five combinations' lookup scores and token costs
- [ ] You can explain why the proper reader could not save the unquoted file
- [ ] You know the flat state ranking this lesson measured (quoted CSV, then prose, then JSON on price)

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
