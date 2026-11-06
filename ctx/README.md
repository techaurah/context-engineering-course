# The ctx toolkit

Shared instruments for every lesson, the way a real project would
share them. Three modules, standard library only:

- `tokenizer.py` counts tokens with a documented approximation.
  It is not a real tokenizer; Lesson 02 measures how far its
  counts sit from word and character heuristics and teaches when
  an approximation is good enough (budgeting) and when it is not
  (billing).
- `standin.py` is the stand-in reader: a deterministic scoring
  rule implementing two measured effects, the U-shaped position
  effect (Liu et al., TACL 2024) and context rot (Chroma, 2025).
  It never generates text. Lessons use it to compare assembly
  decisions, not to imitate a specific model.
- `assemble.py` builds contexts as ordered segment lists and
  tracks spending with a budget ledger.

Every number a lesson quotes is computed by that lesson's code
from these modules and the fixtures in `fixtures/`.
