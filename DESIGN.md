# Course design: Context Engineering

Written before the lessons, from the scan in RESEARCH.md
(2026-11-06). This is the fixed spec the repo was built and
verified against.

## Title and promise

**Context Engineering.** A reference-shaped course on the
context window itself: what goes in, in what order, at what
cost, and how you know it helped. Precise definitions, measured
comparisons, reusable patterns. Every number is the output of
the lesson's own code on the bundled fixtures, measured against
a gold set, and the capstone is graded against gates fixed in
Lesson 29 before the pipeline was built.

## Audience

Engineers who build or operate LLM agents and already know what
a prompt is: Course 1 graduates meeting production context
problems, agent developers whose bills and failure modes are
both growing, and technical leads who need a shared vocabulary
(write, select, compress, isolate) with measurements behind it.
The tone is plain and reference-like; no statistics background
is assumed.

## Prerequisites

- Python 3.11 or newer, standard library only for the whole
  course.
- Course 1 (Agentic AI for Beginners) or equivalent experience
  assembling an LLM context.
- Helpful but not required: Course 5 (Agentic RAG) for the
  selection module's retrieval background, and Course 6
  (Testing AI Agents) for the gates discipline the capstone
  borrows. Both are taught self contained here.

## The instruments

`ctx/` is the shared toolkit: a labelled token count
approximation (`tokenizer.py`), a deterministic stand-in reader
implementing the published position effect (Liu et al., TACL
2024) and context rot (Chroma, 2025) as open rules
(`standin.py`), and assembly plus budget ledger helpers
(`assemble.py`). The stand-in never generates text and is never
described as a model; it compares assembly decisions.

`fixtures/` holds the gold set: 18 Fernhill Garden Centres
knowledge base documents carrying 72 checkable facts, 8 tasks
each naming its required facts and relevant documents, a 24
turn conversation with 5 pinned facts, 3 prose guides with key
facts listed, and the standard budget (a deliberately small
4,000 token window, so pressure is real).

## The arc

Ten modules. Module 0 defines the field and the counting
instruments. Module 1 budgets the window and measures the two
forces that tax it (rot, position). Module 2 writes context:
structure, formats, examples, and the instruction/data channel.
Modules 3 and 4 select and compress (LangChain's operations),
each method raced against the gold set. Module 5 orders and
lays out, and prints the fashionable strategy's honest loss.
Module 6 writes memory and isolates subcontexts, including
isolation's silent failure. Module 7 prices tools and their
results. Module 8 prices layout itself (caching) and teaches
run accounting. Module 9 builds the measurement harness, fixes
the capstone gates, builds the pipeline, and evaluates it in
the open, failure included.

## Lesson map: 32 lessons, 10 modules

### Module 0: Foundations
- 00 Course setup: what you need, and how this course works
- 01 What context engineering is: the anatomy of a window
- 02 Counting tokens: the approximation, and when it is good enough

### Module 1: The window as a budget
- 03 The context budget: accounting for a finite window
- 04 Context rot: the cost of length itself
- 05 Lost in the middle: position effects, measured

### Module 2: Writing context
- 06 The system prompt: structure, altitude, and the verbatim test
- 07 Structured formats: prose, lists, and tags, priced
- 08 Few-shot examples: buying accuracy with tokens
- 09 Instructions vs data: the channel is the control

### Module 3: Selecting context
- 10 Selection as a ranking problem
- 11 TF-IDF selection under a budget
- 12 Just-in-time context: identifiers first, content on demand
- 13 Filtering tool outputs: the cheapest tokens are the ones you never admit

### Module 4: Compressing context
- 14 Extractive compression: keep the sentences that carry the facts
- 15 The stand-in summarizer: what a query-free summary quietly drops
- 16 Compacting conversation history: truncation, notes, and pinned facts
- 17 Pruning and deduplication: near copies, and the fact the short copy lost

### Module 5: Ordering and layout
- 18 Ordering: what the edges strategy actually buys, measured on all facts
- 19 Anchors and repetition: spending 19 tokens to rescue a rule
- 20 Sections and headings: layout as a retrieval surface

### Module 6: Memory and isolation
- 21 Writing external memory: notes that outlive the window
- 22 Memory formats: the reader is part of the format
- 23 Isolating subcontexts: clean windows, and the question nobody asked

### Module 7: Tools in context
- 24 The cost of tool definitions: tokens, overlap, and the twin problem
- 25 Token-efficient tool results: design the answer, not the dump

### Module 8: Caching and cost
- 26 Prefix stability and caching: layout decisions with a price tag
- 27 Cost accounting: read a run like a ledger

### Module 9: Measurement and the capstone
- 28 Measuring context quality: recall, precision, and cost per success
- 29 Capstone spec: the pipeline and its gates, fixed in advance
- 30 Build the capstone pipeline
- 31 Evaluate and harden: the verdict, the failure, and the fix

## The honesty rules

- No invented statistics, no borrowed benchmarks. Field numbers
  appear only in RESEARCH.md and lesson framing, attributed.
- Honest negatives are part of the design, not accidents:
  TF-IDF's near tie with overlap (Lesson 11), the edges strategy
  losing on the all facts metric (Lesson 18), the trimmed tool
  catalogue tying on general choices (Lesson 24), isolation's
  0.0 on the unasked question (Lesson 23), and the capstone's
  first build failing its precision gate (Lesson 31). Exercises'
  worked solutions were themselves verified by running the
  variant code before publication.
