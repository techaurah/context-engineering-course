# Research: the context engineering field, scanned before building

Scanned 2026-11-06. Every claim about a framework, tool, or
publication below carries that date: this field renames itself
quarterly, and undated claims rot. Numbers attributed to other
people's work are labelled with their source; numbers without a
source label in this repo are the course's own measurements.

## Where the term and the canon come from

- Andrej Karpathy argued for "context engineering" over "prompt
  engineering" in a post on X on 25 June 2025, describing the
  move from prompts to "ever more dynamic, programmatically
  synthesized, long, structured contexts." The term circulated
  from mid 2025.
- Anthropic's Applied AI team published "Effective context
  engineering for AI agents" (anthropic.com/engineering, 29
  September 2025), the clearest canonical definition: the set of
  strategies for curating and maintaining the optimal set of
  tokens during inference, including system prompt, tools,
  retrieved data, history, and the agent's own notes. Its
  operating principle: find the smallest set of high-signal
  tokens that maximises the likelihood of the desired outcome.
  It names context rot, the Goldilocks altitude for system
  prompts, just-in-time retrieval with lightweight identifiers,
  compaction, structured note-taking, and sub-agent isolation.
- LangChain's "Context Engineering for Agents" (blog, July 2025)
  contributed the four-word taxonomy this course's middle modules
  are organised by: write, select, compress, isolate.
- Chroma's "Context Rot" report (July 2025; Kelly Hong, Anton
  Troynikov, Jeff Huber) evaluated 18 models from Anthropic,
  OpenAI, Google, and Alibaba and found performance degrading as
  input length grows, even on simple tasks.
- Liu et al., "Lost in the Middle: How Language Models Use Long
  Contexts" (TACL 2024), measured the U-shaped position curve:
  GPT-3.5-Turbo scored 75.8 percent with the answer document
  first in a 20 document set and 53.8 percent with it in the
  middle. The course's Lessons 04 and 05 implement these two
  effects as the stand-in reader's published rules.
- NoLiMa (ICML 2025) minimised literal overlap between question
  and answer; of 13 models claiming at least 128K context, 11
  fell below half their short-context score by 32K tokens.
- Anthropic's multi-agent research write-up (June 2025) reports
  agents using about 4 times the tokens of a chat interaction
  and multi-agent systems about 15 times, with sub-agents
  returning condensed summaries of roughly 1,000 to 2,000 tokens.
- Anthropic's advanced tool use post (November 2025) gives a
  five-server example whose 58 tool definitions consume about
  55K tokens before the conversation starts, and reports on
  demand tool loading cutting upfront context from about 77K to
  about 8.7K tokens on their internal evaluations.

## What already exists (checked 2026-11-06)

- Microsoft's ai-agents-for-beginners (the Course 1 benchmark)
  contains ONE lesson on context engineering (Lesson 12),
  covering definitions, write/select/compress/isolate, and the
  failure modes of context poisoning, distraction, confusion,
  and clash. One lesson inside a general course; no measurement
  harness, no capstone on context itself.
- GitHub's Copilot Academy runs a "Lab: Context Engineering"
  (copilot-academy.github.io), about 2 hours, hands on with real
  token measurement in Copilot CLI. It requires an active
  Copilot subscription and is scoped to coding agents and
  Copilot's own surfaces.
- davidkimai/Context-Engineering on GitHub: a large first
  principles handbook (context formalisation, field theory
  framing), widely forked. Reference prose, not a lesson course:
  no exercises with solutions, no smoke tests, no gated
  capstone.
- AdilShamim8's "Context Engineering Is Not Prompt Engineering"
  (YouTube plus GitHub, 2026): a free structured course, 39
  chapters in 10 parts with 7 labs and 9 projects that run
  locally with no paid APIs, plain Python reference library,
  deterministic tests. The closest competitor in spirit. Its
  centre of gravity is building one research agent's context
  features; it is not organised as definitions plus measured
  comparisons plus a gated assembly capstone, and it does not
  ship a per lesson measured scorecard against a gold set.
- The Daily Dose of Data Science LLMOps course, Part 6 (2026),
  covers context engineering as prompt management, defence, and
  control inside a much larger LLMOps curriculum: one part of a
  paid course, framework oriented.
- Books, all checked 2026-11-06: "Context Engineering for AI
  Agents" on Leanpub (build a Python context engine, ctxkit,
  chapter by chapter; listed at 19 USD); a Manning "Context
  Engineering" title in progress (retrieval and RAG centred);
  Addaly's free "Context Engineering" textbook (9 modules, 87
  lessons, web first); FourWeekMBA's graph engineering volume
  (September 2026). Books are reference shaped but static: none
  executes its claims in front of the reader.
- Long-form explainers (for example ajayk.sh's "Context
  Engineering Explained", 2026) summarise the canon well and
  link the primary sources; they teach reading, not doing.

## The gap this course fills

Nothing found combines all of: (1) a complete lesson course
(32 lessons, exercises with worked solutions, progress
tracking), (2) fully offline and free, standard library only,
no subscription and no API keys, (3) a reference shape: precise
definitions backed by measured comparisons where every number
is produced by the lesson's own code on a bundled gold set,
including the numbers that embarrass the fashionable technique
(edges ordering losing on the all-facts metric, TF-IDF beating
overlap by 0.0063, the trimmed tool catalogue tying on general
choices), and (4) a capstone whose five gates were fixed in
writing before the pipeline was built, with the first build's
gate failure kept in the record. Courses teach pieces of this;
books state pieces of this. The measured, gated, complete
course did not exist in the scan. That is the gap.

## Design consequences taken from the scan

- Organise selection/compression by LangChain's write, select,
  compress, isolate, because the field already shares the words.
- Treat Anthropic's "smallest set of high-signal tokens" as the
  course's definition of good, and make it measurable (recall,
  precision, tokens) in Lesson 28.
- Never quote the field's model numbers as the course's results:
  the stand-in implements the qualitative effects (position,
  rot) as labelled rules, and lessons measure assemblies, not
  models.
- Reference shape first: definitions, tables, and scorecards a
  reader can cite, with the code that produced each table one
  command away.
