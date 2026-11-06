# Fixtures

First class data for the whole course, shared by every lesson.

- `documents.json`: 18 Fernhill Garden Centres knowledge base
  documents (a fictional company, invented for this course). Each
  document carries its checkable facts as a list with stable ids
  like `fh-delivery-fee`. Lessons assemble contexts from these
  documents and measure, with the stand-in reader, whether the
  facts a task needs survive the assembly.
- `tasks.json`: 8 customer questions. Each names the fact ids a
  correct answer needs and the documents that carry them. This is
  the course's gold set: recall is always measured against it.
- `conversation.json`: one scripted 24 turn support conversation
  about tomato plants, with 5 pinned facts stated in the turns
  that any compaction of the conversation must preserve.
- `texts.json`: 3 longer prose guides with their key facts listed,
  for the compression lessons.
- `budgets.json`: the course's standard window budget: a 4,000
  token window (a deliberately small teaching window, so budget
  pressure is real) with per component allowances.

All facts are invented for Fernhill and are true only inside
these fixtures. That is the point: a fact is checkable because
the fixture says what it is.
