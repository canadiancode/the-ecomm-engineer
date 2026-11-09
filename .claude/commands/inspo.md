---
description: Break a video/post link (or an Ideas ID) into hooks, hook type, structure and formula, and write it to Ideas
argument-hint: <link or Ideas ID> [dry]
---

Use the **inspo-analyst** subagent on: $ARGUMENTS

- If the arguments include `dry`, do the full breakdown and show the exact Ideas cells and ranges, but **don't write to the Sheet**.
- Otherwise, show the breakdown, then write it per `.claude/agents/inspo-analyst.md`.

Reply with the breakdown (3 hook layers, hook type, structure, formula, outlier math, fit for Kevin) in 6–8 lines, plus anything that couldn't be verified.
