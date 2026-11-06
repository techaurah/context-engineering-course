# Lesson 07: Structured formats: prose, lists, and tags, priced

Time: ~40 min | Difficulty: Intermediate | Prerequisites: Lesson 06

Data reaches the model in some format, and the format is a context engineering decision with a price and a failure mode. This lesson measures the same four order records three ways: as flowing prose, as a labelled list, and as tagged blocks. A strict stand-in extractor stands in for the reader: it reads labelled fields reliably and prose unreliably. That asymmetry is the property under test, and it is labelled a stand-in property, not a claim about any real model.

The extractor's prose path is deliberately honest about why prose fails: the total is buried mid sentence, in a position the strict reader does not accept, so the field is missed. Watch which format wins on accuracy, and then look at what it costs, because the winner on accuracy is not the winner the tag enthusiasts expect.

## Run it

```bash
python3 format_lab.py
```

## What the code measures

Prose extracts 16 of 20 fields correctly at 152 tokens. The labelled list extracts 20 of 20 at 128 tokens, the cheapest of the three. Tagged blocks also extract 20 of 20 but cost 220 tokens, 72 percent more than the list for the same accuracy. Tags buy unambiguous nesting for complex data; for flat records, the list wins outright and the tags are pure overhead.

## Common failures

- Reaching for tags by default. On flat data they cost 220 tokens against the list's 128 for identical accuracy.
- Writing data as prose because it reads nicely to humans. The reader is not skimming; it is extracting, and prose hides fields mid sentence.
- Judging a format on accuracy alone. Every format decision is accuracy per token.

## Recap checklist

- [ ] You can state the measured accuracy and token cost of prose, list, and tagged formats on the same records
- [ ] You know when tags earn their overhead (nested, ambiguous data) and when they do not (flat records)
- [ ] You can explain the strict extractor's prose failure in one sentence

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
