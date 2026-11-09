---
description: Turn Ideas marked Try (or Story ep N / winner V### re-films) into Pipeline scripts
argument-hint: <idea IDs, space-separated> [dry]
---

Use the **scriptwriter** subagent to script: $ARGUMENTS

- With no IDs: script every Ideas row with Status `Try` that has no Pipeline row yet.
- If the arguments include `dry`, show each finished Pipeline row but **don't write to the Sheet**.
- Otherwise, show each row, then write it per `.claude/agents/scriptwriter.md` with Status `Scripted`.

Reply with each script as a readable block: Video ID, hook (spoken / text / visual), shot list, caption, CTA, word count and estimated length, and every `(TO CONFIRM)`.
