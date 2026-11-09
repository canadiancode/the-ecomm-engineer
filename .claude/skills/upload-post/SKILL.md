---
name: upload-post
description: How to schedule and post approved videos to Instagram, TikTok, YouTube Shorts and LinkedIn through the official Upload-Post MCP, and how the approval hook gates it. Use only from /publish.
---

# Upload-Post

Official MCP: `https://mcp.upload-post.com/mcp` (server name `upload-post` in `.mcp.json`; tools appear as `mcp__upload-post__<tool>`). Auth is the `UPLOAD_POST_API_KEY` env var, sent as `Authorization: ApiKey …`. The key is never written to any file in this repo.

## The gate (hard rule 1)

`.claude/hooks/require-approved.py` runs before every Upload-Post posting tool (`upload_video`, `upload_photos`, `upload_text`, `upload_document`, `edit_scheduled`) and any Bash call that touches `upload-post.com`. It:

1. finds the Video ID (`V###`) in the tool input, or in `.claude/state/publish-target` (written by `/publish` as its first step). If none is found, or they disagree, it blocks.
2. reads the **live** Pipeline row for that ID from the Google Sheets API.
3. allows the call only if Pipeline Status is exactly `Approved`. Otherwise it blocks. It also blocks on any error (fail closed).

Never try to route around it (other tools, curl, a different MCP). If it blocks, stop and tell Kevin why.

DMs and comment replies (`send_dm`, `manage_autodms`, `reply_to_comment`, `public_reply_to_comment`) and account changes (`create_user`, `delete_user`, `update_queue_settings`) are denied in `.claude/settings.json`. Kevin does those by hand or in ManyChat.

## Upload parameters (`upload_video`)

| Param | Value |
| --- | --- |
| `user` | the Upload-Post profile name (TO CONFIRM; stored in `CLAUDE.md` once Kevin creates it) |
| `platforms` | `["instagram", "tiktok", "youtube", "linkedin"]` (or what Kevin asked for) |
| `videoPathOrUrl` | a public/signed HTTPS URL of the final render. Use the Descript `download_url` from a fresh `publish_project` (links expire in 24h), or a Drive file shared by link. |
| `title` | the Pipeline caption, first line. Required for YouTube (≤100 chars). |
| `description` | the full Pipeline caption (column K) |
| `scheduledDate` | ISO 8601. Default: next free daily slot (TO CONFIRM Kevin's posting time). Omit only if Kevin says "post now". |
| `timezone` | `America/Vancouver` |
| `asyncUpload` | `true`; then poll `get_status` with the `request_id` until `success: true` |

Platform notes:
- **Instagram**: Reels. Caption = column K.
- **TikTok**: same caption. Check TikTok's privacy/consent options in `platformOptions` before the first post (TO CONFIRM defaults).
- **YouTube Shorts**: title = first caption line, description = full caption.
- **LinkedIn**: same caption. Plain words, no hashtag walls.
- Never add "link in bio". Never put the Video ID in public text. The gate reads it from `.claude/state/publish-target`.

## After a successful call

1. Pipeline N `Status` = `Scheduled` (or `Posted` if posted now and `get_status` confirms), R `Post date`, S `Platforms posted`, T Notes append the `request_id` / job IDs.
2. When all platforms report posted: Pipeline Status = `Posted`; Ideas row for Pipeline column B (if it's an Ideas ID) → Status `Posted`.
3. Move or copy the render in Drive from `Ready for Review` to `Posted` (`1fppiND8VpV6sGbfQAyVkTaDySWV6ZNh6`).
4. Delete `.claude/state/publish-target`.

## Read-only tools you may use freely

`get_status`, `get_job_status`, `get_history`, `list_scheduled`, `get_analytics`, `get_post_analytics`, `get_platform_metrics`, `get_total_impressions`, `get_account_info`, `list_users`. The analyst uses the analytics ones for `/weekly`.
