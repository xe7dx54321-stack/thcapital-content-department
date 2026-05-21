---
name: th-topic-radar
description: Use when turning TH Capital market content inputs into ranked topic candidates, Top 8 to Top 5 recommendation boards, and founder-ready daily topic decisions. This skill enforces market-first scoring, brand-fit re-ranking, holdout transparency, and citation-preserving recommendation output.
---

# th-topic-radar

Use this skill for Step 4 work:

- topic clustering review
- candidate ranking
- daily Top 8 → Top 5 board generation
- founder-facing topic recommendation
- holdout explanation
- battlefield-aware re-ranking

## Important boundary

- This skill works **after** source capture.
- It does **not** suppress source intake.
- It does **not** decide final publish draft format.
- It does **not** replace human final topic choice.

Its job is:

> 把“今天抓到很多东西”收束成“今天最值得写什么，以及为什么”。

## Load order

1. Read `../../../00_planning/20260324_市场内容系统详细施工方案.md`
2. Read `../../../00_planning/20260324_同行资本市场内容系统开发计划.md`
3. Read `../../../08_brand_assets/20260324_公域品牌上下文手册.md`
4. Read `../../../08_brand_assets/20260324_平台定位与表达规范.md`
5. Read `../../../08_brand_assets/20260324_主战场与邻接选题判定框架.md`
6. If available, read `../../../08_brand_assets/latest__head-media-learning-rulebook-v1.md`
7. If available, read `../../../08_brand_assets/learning_knowledge_assets/latest__learning-knowledge-index.md`
8. If available, read `../../../08_brand_assets/learning_knowledge_assets/latest__style-router.md`
9. Read `../../../03_topic_candidates/20260324__top8-to-top5-topic-board-template.md`
10. If available, read the latest topic radar brief generated from `../../scripts/market_topic_radar_brief_builder.py`

## Core workflow

1. Confirm the planning scope:
   - founder-facing daily recommendation
   - internal candidate sorting
   - manual board refresh

2. Build a candidate pool from:
   - open topic clusters
   - high-value source packets
   - asset chains that make a topic materially more writable

3. Score topics in two passes.

### Pass 1: market-first scoring

Judge each candidate by:

- market heat
- cross-platform spread
- growth speed
- persistence
- writeability
- hook strength
- clarity of user interest
- factual support level

Important:

- keep `heat signal` and `evidence signal` separate
- high heat can enter Top 8 with weak evidence, but must be labeled honestly
- Top 5 should strongly prefer topics where both heat and evidence are usable

### Pass 2: TH Capital re-ranking

Re-rank the short list by:

- main battlefield fit
- adjacency value
- identity reinforcement
- differentiation space
- competitor landscape
- whether TH Capital can say something sharper than generic media
- drift risk

Important:

- A hot adjacent topic can still stay in the Top 8.
- Do not bury strong adjacent topics just because they are not core.
- The battlefield logic is a **re-ranking layer**, not an upstream censorship layer.

4. Build the final `Top 8`.

Every candidate in the final Top 8 must have:

- a clear angle
- a real reason it matters now
- enough source grounding to support a public recommendation

5. Cut from `Top 8` to `Top 5`.

For the final Top 5, explain:

- why this topic should be written now
- what the heat signal is
- what the evidence signal is
- what TH Capital can uniquely say
- what competitors / adjacent creators are already saying
- where it is already fermenting
- what format / platform is most suitable
- what the main risk is

6. Preserve the holdout 3.

The holdout 3 must never disappear.

For each holdout:

- explain why it made Top 8
- explain why it did not enter Top 5
- mark whether the founder can restore it
- if it can be restored, explain the best rescue angle
- keep the source refs visible enough that a restored holdout can directly enter `approved_topic`

7. Keep citations visible.

Each recommended topic must preserve:

- original links
- source packet paths
- key cluster path if any

8. If there are fewer than 8 strong candidates:

- do not fill with weak noise
- explicitly say supply is insufficient
- state what input gap remains

9. When a topic clearly falls into a known route in `latest__style-router.md`, say so explicitly.
   - Mark the likely `content_route`
   - Name the most relevant `primary_overlay`
   - only recommend overlays whose creator skill packs have already passed the 20-sample gate in the learning index
   - Use this only as a routing hint, not as a reason to over-rank weak topics

## Required output fields

Every Top 5 recommendation must include:

1. title
2. one-line judgment
3. why this is worth doing now
4. market potential
5. heat signal
6. evidence signal
7. brand-fit judgment
8. competitor / why-us judgment
9. platform fermentation
10. raw links / source packet paths
11. recommended angle
12. suggested platforms / formats
13. risk note

Every holdout detail block must also include:

1. raw links / source packet paths
2. best restore angle
3. restore risk note if relevant

## Hard constraints

- Do not output a ranked list without explanations.
- Do not produce Top 5 by pure brand fit and ignore market demand.
- Do not produce Top 5 by pure heat and ignore TH Capital identity.
- Do not hide the dropped 3.
- Do not strip citations.
- Do not turn weak evidence into certainty.

## Output guidance

When the task is **daily board generation**, output:

1. Top 5 board
2. Top 5 detail blocks
3. holdout 3 board
4. holdout detail blocks
5. founder restore notes

Important:

- Holdout detail blocks must preserve source refs too, not just Top 5 blocks.

When the task is **candidate review**, output:

1. keep / drop recommendation
2. why now
3. best angle
4. missing evidence
5. whether it belongs in core / adjacent / park
