# Lesson 15: The stand-in summarizer: what a query-free summary quietly drops

Time: ~50 min | Difficulty: Intermediate | Prerequisites: Lesson 14

Real summarization is abstractive and model written, which this course cannot run offline. So this lesson builds a labelled stand-in summarizer with the habits real summarizers have: it keeps the opening sentence, any sentence carrying a number, and the closing sentence, and drops the rest. It does not understand the text. The point is not to imitate a model's prose; it is to measure the structural risk of summarizing without a question in hand, which is when most production compaction happens.

The opponent is Lesson 14's query driven extractor on the same text (the watering guide) at a similar spirit of budget. The stand-in summary is far shorter. Watch what the shortness costs, fact by named fact.

## Run it

```bash
python3 summarizer_lab.py
```

## What the code measures

The stand-in summary keeps 2 of 4 key facts in 45 tokens. It drops the mulch depth fact and the water the soil not the leaves fact, both mid text, neither carrying a digit in the form the heuristic wants (five centimetres is spelled out). The query driven extractor keeps 3 of 4 in 149 tokens. Neither is free: the summary is 3.3 times cheaper and loses twice as much. Which one is right depends on whether anyone can state the question at compression time, and in long running agents, usually nobody can.

## Common failures

- Summarizing a conversation or document 'for later' with no question in hand, then being surprised the later question's fact is gone.
- Trusting numbers as a keep signal. The mulch fact's quantity is spelled out in words and the heuristic walked past it.
- Comparing summarizers on length alone. The honest comparison is facts kept per token, per method, on the same text.

## Recap checklist

- [ ] You can name the two facts the stand-in summary dropped and why the heuristic missed them
- [ ] You can state both methods' tokens and facts kept on the watering guide
- [ ] You know the condition that decides between them (whether a query exists at compression time)

## Resources

- [README.md](../../README.md): the course map and the capstone scorecard
- [RESEARCH.md](../../RESEARCH.md): the field scan this course is built on
- [DESIGN.md](../../DESIGN.md): the spec this course was built to
- [exercise.md](exercise.md) and [solution/SOLUTION.md](solution/SOLUTION.md): this lesson's exercise and worked solution
