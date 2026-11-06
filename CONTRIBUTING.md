# Contributing to Context Engineering

Contributions are welcome: corrections, clearer explanations,
new exercises, translations, and measured challenges to any
lesson conclusion.

## Ground rules

- **Big changes start with an issue.** A new lesson, a rewritten
  lesson, a change to the ctx toolkit, the fixtures, or the
  capstone gates: open an issue first so a maintainer can agree
  the shape with you before you invest hours. Toolkit, fixture,
  and gates changes are big by definition, because every
  lesson's quoted numbers derive from them.
- **Numbers must reproduce.** Any change that alters a quoted
  number must update every place that number appears (lesson
  README, exercise solution, root README, llms.txt, visuals) in
  the same pull request, and the new number must come from
  running the code, not from estimating.
- **Standard library only.** No new dependencies, no network
  calls, no API keys. The course runs offline, everywhere.
- **No em dashes** anywhere in the repository, prose or code.
- **Stand-ins stay labelled.** Results from the stand-in reader
  or any stand-in component are described as stand-in results.
- **Honest negatives stay.** A pull request that removes a
  measured failure, near tie, or losing strategy because it
  reads badly will be declined. One that measures a better
  result and updates the lesson honestly will be celebrated.

## Before you open a pull request

Run the full local verification:

```bash
python3 tools/validate_course.py
python3 tools/check_links.py
for d in [0-9]*-*/; do (cd "$d" && python3 smoke_test.py) || echo "FAIL $d"; done
```

If you changed a lesson's code, re-derive its exercise's
variant numbers as well; solutions quote them exactly.

## Lesson bugs

Open an issue with the lesson number, the command you ran, the
output you got, and the output the lesson quotes. Mismatches
between quoted and reproduced numbers are treated as bugs in
the lesson, full stop.
