---
name: th-source-capture-and-citation
description: Use when building or maintaining TH Capital's AI content watchlists, capturing source materials, normalizing them into source packets, preserving citations, and preparing multilingual raw inputs for topic radar. This skill keeps source intake broad inside the AI universe, preserves original links and quotes, and turns scattered materials into reusable source packets.
---

# th-source-capture-and-citation

Use this skill for Step 3 work:

- adding or reviewing watchlist sources
- building platform source registries
- capturing raw source materials
- normalizing articles, posts, threads, transcripts, and videos
- preserving citation chains
- preparing `source_packet` objects for topic radar

## Important boundary

- This skill governs **source intake and source packet preparation**
- It does **not** decide final topic priority
- It does **not** demote sources just because they are not directly in the main battlefield
- Inside the AI universe, source intake stays broad and fair

Final topic preference belongs to the later radar / recommendation stage.

## Load order

1. Read `../../../00_planning/20260324_对象字典与命名规范.md`
2. Read `../../../00_planning/20260324_状态流转规范.md`
3. Read `../../../00_planning/20260324_市场内容系统详细施工方案.md`
4. Read `../../../08_brand_assets/20260324_主战场与邻接选题判定框架.md`
5. If available, read `../../../08_brand_assets/latest__head-media-learning-rulebook-v1.md`
6. Read `../../20260324_信源抓取与引用落盘规范.md`
7. If normal capture is blocked by dynamic pages / login walls / media evidence needs, read `../th-web-access-fallback/SKILL.md`

## Core workflow

1. Confirm the task:
   - add source
   - update registry
   - capture raw material
   - normalize packet
   - citation cleanup

2. If the task is source intake, judge the source with source-level criteria:
   - signal quality
   - trust level
   - topic production ability
   - platform relevance
   - capture feasibility
   - citation usefulness

3. Choose the correct registry file by platform.

4. Capture the raw material.
   - Preserve original URL
   - Preserve source identity
   - Preserve capture timestamp
   - Preserve title in the original language
   - Preserve whether this is primary / secondary / mirror / community / fallback

5. Normalize into a `source_packet`.
   - keep the raw path
   - keep the raw-capture / distilled-body split
   - create a short summary
   - extract quote candidates
   - record visual evidence and screenshot candidates when available
   - mark content type
   - mark translation need if relevant
   - mark `source_type / primary_source / verification_status`

6. Preserve citation quality.
   - distinguish official / media / community / aggregator sources
   - do not turn discussion heat into factual proof
   - keep lower-reliability sources visible but clearly labeled
   - prefer primary source links whenever they are reachable

7. Move status correctly:
   - `captured` after initial intake
   - `normalized` after packet preparation
   - `clustered` only after later radar grouping

## Fallback escalation

- Default order stays:
  - RSS / API
  - direct HTML
  - stable Jina snapshot
- If those paths fail or lose key evidence, escalate to `th-web-access-fallback`.
- Browser fallback should recover the target, but the long-term goal is to turn repeated recoveries back into stable automated parsers whenever possible.

## Source-level rules

- Do not use “main battlefield / adjacent battlefield” to suppress a source upstream.
- A source can be valuable because it is fast, noisy-but-early, or strong at surfacing breakout topics.
- A source is not valuable if it creates constant noise and rarely produces reusable topics.

## Packet output rules

Every normalized packet should make later work easier. At minimum include:

1. original title
2. original link
3. source name / author
4. published time
5. captured time
6. `source_type`
7. `primary_source`
8. `verification_status`
9. raw capture path
10. distilled body
11. short summary
12. quote candidates
13. notes on trust / citation caveats
14. visual evidence / screenshot hints when available

## Translation rules

- Translation is allowed to help later Chinese workflows
- Never replace the original title or original link
- When translating, keep both:
  - original title
  - Chinese working summary

## Hard constraints

- Do not keep only summaries without original links.
- Do not delete the original-language context after translation.
- Do not treat community chatter as the same as primary-source evidence.
- Do not classify sources by battlefield importance at the intake layer.

## Output guidance

When the task is **source intake**, output:

1. source basic info
2. why this source is worth tracking
3. suggested registry
4. capture method
5. source quality notes

When the task is **packet preparation**, output:

1. source packet header
2. summary
3. quote candidates
4. raw path
5. citation notes
