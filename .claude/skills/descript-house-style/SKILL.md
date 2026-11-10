---
name: descript-house-style
description: The Ecomm Engineer's Descript editing house style and the single reusable Agent Underlord pre-prompt. Use for every Descript edit (import raw clips, one batched Underlord prompt, publish, write back to the Pipeline).
---

# Descript house style

Editor: Descript (Hobbyist plan, TO CONFIRM it's active). Edits run through **Agent Underlord** via the Descript MCP (`mcp__Descript__*`).

## Credit discipline

- Each Underlord prompt costs about **8–25 credits**. Put **every** instruction for a video into **one** prompt (the pre-prompt below). No exploratory or "check" prompts. Use `get_project` / `export_transcript` (no credits) to inspect.
- A second prompt only to fix something specific the first one missed, and never more than one fix-up prompt per video without asking Kevin.

## Import rules

- Descript can only import Drive files shared as **"Anyone with the link"**. Share each raw clip in `Raw Footage/V###` with `mcp__Google_Drive__share_file` (`permissionId: "anyoneWithLink"`, `role: "reader"`), then import the Drive URLs with `mcp__Descript__import_media`.
- New project name: `V### – <Topic>`. Create with `add_compositions` in **1080×1920** (9:16), clips in filename order (that's shooting order on iPhone).
- After import, note in Pipeline Notes that the raw clips are link-shared (Kevin can turn that off in Drive once the edit is done).

## House style

- 9:16 vertical, 1080×1920.
- Cut slates (Kevin saying the Video ID, e.g. "Video 002"), flubs, false starts and retakes. **Keep the last good take** of each line.
- Tight pacing, but never jump-cut mid-word. Leave a natural breath between sentences.
- Order follows the script's SHOT order, not the recording order.
- Captions: always the saved caption style **"Ecomm Engineer"** (1 line, about 2–4 words / ~15 characters at a time). Underlord can't set words per caption, so apply the saved style by name and don't override its settings.
- **Wrong words in the transcript: transcript-only correction.** Say "correct the transcript text without changing media". Never edit transcript words directly to fix them: that deletes the audio and video (this cut "Whistler" once).
- Story photo cutaways: wherever the script says `Edit: <filename>`, place that file from `B-Roll/Story` (import it too) over the matching line, full screen, for the length of the line.
- Keep swearing unless the script marks `(bleep)`.
- Target 30–60s. If the cut runs long, say so in Notes. Don't cut scripted lines to hit time.
- No music, no stock footage, no AI voice, no filler-word removal that clips words, unless the script asks.

## Manual steps (Underlord can't do these, so always list them for Kevin)

1. Reframe by face / keep face centered in 9:16 (do it in the app).
2. Normalize loudness / Studio Sound check (do it in the app).
3. Anything Underlord reported it couldn't do.
4. Save the final render to Drive `Ready for Review/V###_final.mp4` if the agent couldn't (Descript links expire in 24h).

## The pre-prompt (fill the `<…>`, send once per video)

```
You are editing video <V###> for The Ecomm Engineer. Do ALL of the following in one pass, then reply with a short list of what you did and anything you could not do.

1. Layout: 9:16 vertical, 1080x1920, for Instagram Reels / TikTok / YouTube Shorts.
2. Remove every slate where I say the video ID (for example "Video <0NN>"), plus flubs, false starts, repeated lines and retakes. When a line was recorded more than once, keep the LAST complete good take.
3. Arrange the kept takes in this script order:
<numbered list: one line per SHOT, the exact Say: text>
4. Pacing: tight, remove long pauses (over ~0.4s) between sentences, but never cut in the middle of a word and leave a natural breath between sentences.
5. Transcript fixes: for these words, correct the transcript text WITHOUT changing media (do not delete or cut anything): <list "heard → correct", e.g. "whistle → Whistler", or "none">.
6. Captions: apply my saved caption style named "Ecomm Engineer" to the whole video. Do not change the style's settings.
7. Image cutaways: place these images full screen over the matching line, for the length of that line:
<list: "<filename>" over "<line text>">
8. Keep all swearing<, except bleep: <words> | (omit if none)>.
9. Do not add music, stock media, AI voice, or extra text other than the captions<, and this on-screen text during the first 2 seconds: "<Text hook>">.
Do not export or publish. Reply with: final duration, any scripted line you could not find in the footage, and anything you could not do.
```

## After the edit

1. `mcp__Descript__publish_project` (1080p, `access_level: "unlisted"`) → `share_url` + `download_url`.
2. Save the render to Drive `Ready for Review` (`1AlVpG0Laa0xmFjtrVRzmtVOSRP-yvz8t`) as `V###_final.mp4`. If the file is too big to pass through the Drive connector, add it to the manual steps instead. Never skip silently.
3. Pipeline: Q `Edited video` = share URL; N `Status` = `Ready for review`; T `Notes` append: Descript project URL, duration, lines missing from the footage, manual steps left for Kevin.
4. Share/download links expire in 24h. The Drive copy (or re-running `publish_project`, which refreshes the same share URL) is what Kevin downloads to post.
