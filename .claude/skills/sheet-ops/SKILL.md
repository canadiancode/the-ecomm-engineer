---
name: sheet-ops
description: Exact read/write rules for the Content Hub Google Sheet (tab and column maps, status transitions, ID formats, protected formula columns, append-don't-overwrite). Use before ANY read or write to the Sheet.
---

# Sheet ops

**Spreadsheet:** `the_ecomm_engineer Content Hub`, ID `1HVSdkA4jfSirk1lTcrUO5qfzVbmHvXsUbULw7Mudsc4`.
Tools: `mcp__Google_Sheets__get_values`, `update_values`, `append_values`.

## The rules

1. **Read before you act.** Re-read the rows you'll touch right before writing. Kevin edits on his phone, so never trust a value you read earlier in the session.
2. **Write status back after every step.** One step = one write. If a step fails, write what happened to Notes and stop.
3. **Append, don't overwrite.** New rows go on the first empty row (find it by reading column A). Never rewrite a row you didn't create unless the step is a status change or filling a blank cell. Never clear a cell Kevin filled. To change Notes, keep the old text and add to it: `<old> | YYYY-MM-DD: <new>`.
4. **Protected formula columns. Never write to them, not even blanks:**
   - `Ideas!H1` holds `={"Views per follower";ARRAYFORMULA(...)}`, which fills **all of H2:H**. Any value in H2:H breaks the whole column (#REF!).
   - `Analytics!K1:M1` hold array formulas that fill **K2:M**. Same rule.
   - So: Ideas writes go in two ranges, `A{n}:G{n}` and `I{n}:P{n}`. Analytics writes go in `A{n}:J{n}` only. Don't use `append_values` across those columns.
5. **Settings live in `'Start here'!B5:B7`.** Read them each run. Don't hardcode.
6. **Show, then write**, when a command says so (`/inspo`, `/script` dry runs): print the exact rows and ranges first.
7. Numbers go in as plain numbers (no "x", no commas). Dates are `YYYY-MM-DD`. Never put the employer's name or client data in any cell (`brand/off-limits.md`).

## 'Start here' settings

| Cell | Setting | Current |
| --- | --- | --- |
| B5 | Winner threshold (× platform average views) | 5 |
| B6 | Outlier minimum views | 700,000 |
| B7 | Outlier minimum views per follower | 5 |

## Ideas (16 columns, A–P)

| Col | Header | Who writes | Notes |
| --- | --- | --- | --- |
| A | ID | agent | `I-NNN`, `G-YYYYMMDD-NN`, `G-YYYYMMDD-N01`, `C-YYYYMMDD-NN`, `K-YYYYMMDD-NN` |
| B | Date found | agent | YYYY-MM-DD |
| C | Platform | agent | Instagram, TikTok, YouTube, X, Reddit, Shopify Community, News |
| D | Account | agent | `@handle`, subreddit, or publication |
| E | Link | agent | |
| F | Views | agent | number, only if seen on the source. Blank if unknown. Never estimate. |
| G | Followers | agent | number, same rule |
| **H** | Views per follower | **FORMULA, never write** | |
| I | Spoken hook | agent | verbatim from the source |
| J | Text hook | agent | verbatim on-screen text |
| K | Visual hook | agent | what you see in the first 2s |
| L | Hook type | agent | one of the 7 (pbl-method) |
| M | Structure | agent | one of the 11 (pbl-method) |
| N | Formula | agent | fill-in-the-blank with `[brackets]` |
| O | Status | **Kevin** sets Try/Reject; agents set Posted | |
| P | Notes | agent | why it worked, outlier math, source context |

**Ideas status:** blank = not reviewed · `Try` = pushed to Pipeline · `Posted` = our version is live · `Reject` = not a fit.
Agents never set Try or Reject. The publisher sets Posted. A Try idea is "pending" if no Pipeline row has its ID in column B.

## Pipeline (20 columns, A–T)

| Col | Header | Notes |
| --- | --- | --- |
| A | Video ID | `V001`, `V002`… (3 digits; Kevin says it on camera) |
| B | Idea ID | Ideas ID, or `Story ep N`, `Building in public #N`, or the original `V###` for a re-film |
| C | Topic | |
| D | Pillar | one of the 8 in `brand/strategy.md` |
| E | Hook type | |
| F | Structure | |
| G | Spoken hook | |
| H | Text hook | |
| I | Visual hook | |
| J | Script (shot by shot) | script-writing skill format |
| K | Caption | |
| L | CTA keyword | ≤7 letters, caps, or `Follow` |
| M | Format | Talking head / Talking head + screen / Voiceover + B-roll / Whiteboard / Two-person |
| N | Status | see below |
| O | Shoot date | YYYY-MM-DD |
| P | Raw clips | Drive folder link `Raw Footage/V###` |
| Q | Edited video | Descript share link |
| R | Post date | YYYY-MM-DD |
| S | Platforms posted | e.g. `Instagram, TikTok, YouTube Shorts, LinkedIn` |
| T | Notes | append only |

No formula columns. Still write explicit ranges (`Pipeline!A{n}:T{n}` for a new row, single cells for updates).

**Pipeline status flow:**

```
Scripted → Approved to film → Filmed → Ready for review → Approved → Scheduled → Posted
                         (Killed from any stage)
```

| Status | Set by | Next action |
| --- | --- | --- |
| Scripted | scriptwriter | Kevin reviews the script |
| Approved to film | **Kevin** | Kevin films |
| Filmed | Kevin (or editor, once raw clips are in Drive) | `/edit` |
| Ready for review | editor | Kevin watches |
| Approved | **Kevin only** | `/publish` (hook-enforced) |
| Scheduled | publisher | Upload-Post queued it |
| Posted | publisher | analyst tracks it |
| Killed | Kevin | none |

Agents never set `Approved to film`, `Approved` or `Killed`. Never skip a status. Never move a row backwards without writing why in Notes.

## Analytics (13 columns, A–M)

| Col | Header | Notes |
| --- | --- | --- |
| A | Video ID | |
| B | Platform | Instagram / TikTok / YouTube Shorts / LinkedIn (one row per video per platform) |
| C | Post date | |
| D | Views | |
| E | Likes | |
| F | Comments | |
| G | Shares | |
| H | Saves | |
| I | Follows gained | |
| J | Keyword comments | comments containing the CTA keyword |
| **K** | Platform average views | **FORMULA** |
| **L** | Times platform average | **FORMULA** |
| **M** | Winner | **FORMULA** (`Winner` when L ≥ `'Start here'!B5`) |

Weekly: update the existing row for a video+platform (`A{n}:J{n}`) if it exists, otherwise add a new row. Blank if a metric isn't available. Never estimate.

## ID rules

| Format | Meaning | How to make the next one |
| --- | --- | --- |
| `V001` | Pipeline video | max existing `V###` in Pipeline!A + 1, zero-padded to 3 |
| `I-001` | a found video | max existing `I-###` in Ideas!A + 1 |
| `G-YYYYMMDD-NN` | research idea (pain point, trend) | today's date, NN = next for that date, from 01 |
| `G-YYYYMMDD-N01` | research news item | `N` + 2 digits, separate counter |
| `C-YYYYMMDD-NN` | Claude's own idea | same pattern |
| `K-YYYYMMDD-NN` | Kevin's idea | same pattern (only when Kevin gives the idea) |

IDs are never reused, even for Killed or Rejected rows. Dates use America/Vancouver.

## Drive map (folder IDs)

| Folder | ID |
| --- | --- |
| `the_ecomm_engineer` (root) | `15lsTTApOdwUTN-qk0SxikW9mgYSShJG8` |
| Raw Footage (one subfolder per Video ID, e.g. `V001`) | `1puBaDwBZoNiUSQ3quir8sGcaKgzJMQ7s` |
| Raw Footage/V001 | `10LY-xsF9hRrBIUeqVh8oPhPgpkzzEOC1` |
| Ready for Review (edited renders) | `1AlVpG0Laa0xmFjtrVRzmtVOSRP-yvz8t` |
| Posted | `1fppiND8VpV6sGbfQAyVkTaDySWV6ZNh6` |
| B-Roll | `1RCnDwaf8PfUPqfpx_O0KMMhxNp8HTDLq` |
| B-Roll/Story | `1of3RMyuBQ_7MO8NuVQd5ypIz5qFrp_v-` |
| B-Roll/Lifestyle | `1ArpIHNzWok0oB7Fe-D_i_tdrLflR9ZbP` |
| B-Roll/Working | `18i_Hg2VF83flSjlpoc26TB8BrGmsIPqi` |
| B-Roll/Screen Recordings | `1_-0iExgFSN2FdAG_z_zQzQ9_WDKTXK60` |
| Grok Research | `1QFSw0FyM2PPVhProBlrGljfjOFnK4xo-` |
