# Working in this repository

Notes for anyone (human or agent) changing the course.

## The one rule

Every number quoted in a lesson must be the output of that
lesson's code on the bundled fixtures. If you change code,
fixtures, or the ctx toolkit, rerun the affected lessons and
update the quoted numbers in the README, the exercise solution,
the root README scorecard, and the visuals, in the same change.
A number that no longer reproduces is a bug, whatever file it
sits in.

## House standards

- Standard library only, everywhere. No new dependencies.
- No em dashes in any file. Check before committing.
- The stand-in reader and any stand-in classifier or summarizer
  must be labelled as stand-ins wherever their results are
  quoted. Never describe a stand-in measurement as a model's
  behaviour.
- Honest negatives stay. If a change makes a technique measure
  worse somewhere it previously measured better, that is
  content, not a regression to hide.
- Gates in 29-capstone-spec/capstone/gates.json do not move. If
  the pipeline fails one, the pipeline changes (see Lesson 31).

## Verification before a change lands

```bash
python3 tools/validate_course.py
python3 tools/check_links.py
# every lesson smoke test:
for d in [0-9]*-*/; do (cd "$d" && python3 smoke_test.py) || echo "FAIL $d"; done
```

Exercise solutions quote variant runs. If you change a lesson's
code or data, re-derive its exercise's variant numbers too; the
build history of this repo includes a full verification pass
over every exercise claim, and the standard is that yours
reproduce as well.
