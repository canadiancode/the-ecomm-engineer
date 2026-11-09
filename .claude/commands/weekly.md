---
description: Weekly loop. Stats into Analytics, winners flagged, what-worked note, and next week's slate of ~10 scripts for Saturday batch filming
argument-hint: [dry]
---

Run the weekly loop in two parts.

**1. Stats.** Use the **analyst** subagent (`.claude/agents/analyst.md`): pull last week's per-post stats into Analytics (columns A–J only), read the Winner flags, write the what-worked note and re-film suggestions.

**2. Slate.** Then use the **scriptwriter** subagent to write about **10 scripts** for Saturday's batch shoot:
- every winner re-film the analyst suggested (new hook type, new format),
- all Ideas with Status `Try` that have no Pipeline row,
- the next unscripted Story series episodes (see `brand/strategy.md`), and the next `Building in public #N`,
- if that's under ~10, don't script anything else. List the best unreviewed Ideas (outliers that pass the rule, strongest pain points) as suggestions for Kevin to mark `Try`. Agents never set Try.
- Keep the mix around 40% story / 40% value / 20% news. Group the slate by setup (same framing / location) so Kevin can film straight through.

If the arguments include `dry`, show everything but write nothing. Otherwise write Analytics rows and new Pipeline rows (Status `Scripted`).

Reply with: the what-worked note, the winners, and the slate as a table (Video ID, topic, pillar, hook type, setup, length, TO CONFIRMs), plus a Saturday shot order. Arguments: $ARGUMENTS
