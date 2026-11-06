# Glossary

The course's definitions, as used in its measurements. Where a
term has a canonical source, the source is RESEARCH.md.

- **Context**: everything the model receives on one turn:
  system prompt, tool definitions, memory, retrieved content,
  history, and the current input.
- **Context engineering**: the discipline of deciding what the
  context contains, in what form and order, at what cost, and
  verifying the effect. Distinct from prompt engineering, which
  concerns the instruction component alone.
- **Context window**: the maximum tokens a model accepts on one
  turn. A capacity, not a recommendation.
- **Context rot**: degradation in the use of information as
  total context grows, well inside the window (Chroma, 2025).
- **Position effect (lost in the middle)**: information near the
  start and end of the context is used more reliably than
  information in the middle (Liu et al., 2024).
- **Stand-in reader**: this course's deterministic scoring rule
  implementing the position effect and rot so assemblies can be
  compared offline. A teaching instrument, not a model.
- **Gold set**: the fixture tasks, each naming the facts a
  correct answer requires. All recall and coverage numbers in
  the course are measured against it.
- **Coverage**: the fraction of required facts present anywhere
  in the assembled context.
- **Recall (stand-in)**: the mean rate at which the stand-in
  reader uses the required facts from where they were placed.
  Coverage is presence; recall is use.
- **Precision**: relevant tokens divided by total tokens in an
  assembled context.
- **Write / select / compress / isolate**: LangChain's four
  context operations (2025): save outside the window, pull in
  what the step needs, keep only fact carrying tokens, split
  work across windows.
- **Just-in-time context**: keeping identifiers in the window
  and loading content on demand, rather than preloading.
- **Compaction**: replacing older context with a shorter form
  (notes, summaries, pins) so work can continue inside budget.
- **Pinned fact**: a fact a compaction must preserve verbatim,
  named in advance.
- **Relevance floor**: a selection rule admitting only items
  scoring at least a fixed fraction of the top item's score.
- **Prefix cache**: a provider mechanism billing a repeated
  context prefix at a discount; it makes layout a pricing
  decision.
- **Gate**: a pass/fail threshold fixed in writing before the
  thing it judges is built. Gates do not move after results.
