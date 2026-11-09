# The Ecomm Engineer: content system

Kevin Heids (@the_ecomm_engineer, BC, Canada) makes one short video a day for Shopify owners doing $5K–$100K/month: **make more, spend less, ship faster**, told through his forestry → Shopify → dev lead story. This repo is the orchestrator. Agents do the work. The Google Sheet holds the state.

## Hard rules (override everything else)

1. **Nothing gets posted without Kevin's approval.** Publishing only runs when the Pipeline Status for that Video ID is exactly `Approved`. Enforced by the `.claude/hooks/require-approved.py` PreToolUse hook, which checks the live Sheet and fails closed. Never work around it.
2. **Never name Kevin's current employer, its clients or the agency** in any content, file, caption, Sheet cell, filename or commit. Say "the stores I work on". This brand is fully separate from the day job.
3. **Only demo-store numbers on screen.** No real revenue claims. No client data.
4. **The Google Sheet is the single source of truth.** Read it before acting. Write status back after every step.
5. **Never overwrite formula header cells `Ideas!H1` and `Analytics!K1:M1`**, and never write anywhere in `Ideas!H2:H` or `Analytics!K2:M` (array formulas fill them).
6. **No zip files and no extra scaffolding** Kevin didn't ask for.

Also: never invent facts about Kevin's life (mark `(TO CONFIRM)`), never say "link in bio", read `brand/corrections.md` first.

## System map

```
/research (daily) ─► Ideas ──Kevin sets Try──► /script ─► Pipeline: Scripted
/inspo <link> ─────► Ideas                         Kevin ─► Approved to film ─► films
                                                    raw clips ─► Drive Raw Footage/V###  (Filmed)
                                     /edit V### ─► Descript ─► Ready for review (share link)
                                                    Kevin ─► Approved
                                  /publish V### ─► [hook checks Sheet] ─► Upload-Post ─► Scheduled ─► Posted
/weekly ─► Analytics + winners ─► ~10 scripts for Saturday
```

| System | Where | Access |
| --- | --- | --- |
| Content Hub (Sheet) | `the_ecomm_engineer Content Hub`, ID `1HVSdkA4jfSirk1lTcrUO5qfzVbmHvXsUbULw7Mudsc4` | Google Sheets connector (`mcp__Google_Sheets__*`) |
| Drive root | `the_ecomm_engineer`, `15lsTTApOdwUTN-qk0SxikW9mgYSShJG8` | Google Drive connector (`mcp__Google_Drive__*`) |
| Editing | Descript, Agent Underlord | Descript connector (`mcp__Descript__*`) |
| Posting | Upload-Post (IG, TikTok, YouTube Shorts, LinkedIn) | `upload-post` in `.mcp.json`, key in env `UPLOAD_POST_API_KEY` |
| Comment → DM | ManyChat (not set up yet) | manual |

### Drive folders

| Folder | ID |
| --- | --- |
| Raw Footage (subfolder per Video ID, e.g. `V001`) | `1puBaDwBZoNiUSQ3quir8sGcaKgzJMQ7s` |
| Ready for Review (edited renders `V###_final.mp4`) | `1AlVpG0Laa0xmFjtrVRzmtVOSRP-yvz8t` |
| Posted | `1fppiND8VpV6sGbfQAyVkTaDySWV6ZNh6` |
| B-Roll | `1RCnDwaf8PfUPqfpx_O0KMMhxNp8HTDLq` |
| B-Roll/Story (named photos for cutaways) | `1of3RMyuBQ_7MO8NuVQd5ypIz5qFrp_v-` |
| B-Roll/Lifestyle | `1ArpIHNzWok0oB7Fe-D_i_tdrLflR9ZbP` |
| B-Roll/Working | `18i_Hg2VF83flSjlpoc26TB8BrGmsIPqi` |
| B-Roll/Screen Recordings | `1_-0iExgFSN2FdAG_z_zQzQ9_WDKTXK60` |
| Grok Research | `1QFSw0FyM2PPVhProBlrGljfjOFnK4xo-` |

Descript only imports Drive files shared "Anyone with the link".

## IDs

| ID | Meaning |
| --- | --- |
| `V001` | Pipeline video. Kevin says it on camera at the start of each take. |
| `I-001` | a found video |
| `G-YYYYMMDD-NN` / `G-YYYYMMDD-N01` | research idea / research news |
| `C-YYYYMMDD-NN` | Claude's idea |
| `K-YYYYMMDD-NN` | Kevin's idea |

Pipeline column B can also hold `Story ep N`, `Building in public #N`, or a winner's `V###` (re-film).

## Statuses

- **Ideas:** blank = not reviewed · `Try` = pushed to Pipeline (Kevin) · `Posted` = our version is live · `Reject` = not a fit (Kevin)
- **Pipeline:** `Scripted` → `Approved to film` (Kevin) → `Filmed` → `Ready for review` → `Approved` (Kevin) → `Scheduled` → `Posted`, or `Killed` (Kevin)
- Agents never set `Try`, `Reject`, `Approved to film`, `Approved` or `Killed`.

Exact column maps and write rules: `.claude/skills/sheet-ops/SKILL.md`. Settings: `'Start here'!B5` winner ×, `B6` outlier min views, `B7` outlier min views/follower.

## Who does what

| Command | Agent | Does | Writes |
| --- | --- | --- | --- |
| `/research` (daily, scheduled) | researcher | news, pain points (Shopify Community, Reddit, X), outlier videos | new Ideas rows |
| `/inspo <link\|ID> [dry]` | inspo-analyst | 3-layer hook, hook type, structure, formula | Ideas row |
| `/script <IDs> [dry]` | scriptwriter | Try ideas → filmable scripts | Pipeline rows (`Scripted`) |
| `/edit <V###>` | editor | Drive raw clips → Descript (one Underlord prompt) → review link | Pipeline Q, N=`Ready for review`, T |
| `/publish <V###>` | publisher | `Approved` → Upload-Post | Pipeline N/R/S/T, Ideas O=`Posted` |
| `/weekly [dry]` | analyst + scriptwriter | stats, winners, what-worked note, ~10-script slate | Analytics A–J, Pipeline rows |

Only `/research` runs on a schedule. `/edit` and `/publish` are always run by hand.

## Read before working

- `brand/corrections.md`: **first, always**
- `brand/profile.md`: who Kevin is, what he can film, proof rules
- `brand/story.md`: chapters, story rules, B-Roll/Story filenames
- `brand/audience.md`: who it's for, their words, jargon to avoid
- `brand/voice.md`: chill builder, no hype, no money flexing
- `brand/off-limits.md`: never name / never claim
- `brand/strategy.md`: pillars, mix, series, CTA ladder, lead magnets, winners
- `brand/launch-plan.md`: full source plan (these rules win if it conflicts)

Skills: `pbl-method`, `script-writing`, `descript-house-style`, `upload-post`, `sheet-ops` in `.claude/skills/`.

## Upkeep

- When Kevin corrects anything, add a row to `brand/corrections.md` in the same turn.
- When new Story photos land in Drive, refresh the table in `brand/story.md`.
- The Upload-Post profile name (`user`) is TO CONFIRM. Add it here once created.
- `.claude/hooks/**` and `.claude/settings.json` are deny-listed for Claude's Edit/Write. Kevin changes them by hand.
