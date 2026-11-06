# Security policy

## Scope

- This is a teaching repository. The company (Fernhill Garden
  Centres), its documents, customers, and conversations are
  fictional and invented for the lessons; learners are told
  repeatedly never to put real customer data in a fork.
- Lesson 09 teaches the instruction/data channel discipline:
  untrusted content is data, never instructions. A lesson or PR
  that weakens that discipline in the course's own examples
  (for example, merging retrieved text into the instruction
  channel without labelling it) will be treated as a security
  problem, not a style choice.
- The course code makes no network calls and reads no
  environment secrets. A change that adds either is out of
  scope for this repository.

## Reporting

Report a security problem in the course material (for example,
an example that teaches an unsafe assembly as the recommended
one) through GitHub's private vulnerability reporting on this
repository, or by opening an issue if the problem is not
sensitive. Teaching the failure modes is deliberate and
labelled; presenting one as best practice is a bug.
