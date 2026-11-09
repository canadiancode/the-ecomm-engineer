---
description: Post/schedule an Approved video to Instagram, TikTok, YouTube Shorts and LinkedIn via Upload-Post
argument-hint: <Video ID, e.g. V002>
---

Use the **publisher** subagent to publish video $ARGUMENTS, following `.claude/agents/publisher.md` and the `upload-post` skill.

This only works when the Pipeline Status for $ARGUMENTS is exactly `Approved`. The `require-approved` hook checks the live Sheet and blocks every Upload-Post posting call otherwise. If it's blocked, report why and stop. Never look for a way around it.

Reply in 3 lines: what was scheduled/posted (platforms + time), what was written to the Sheet, and anything that failed.
