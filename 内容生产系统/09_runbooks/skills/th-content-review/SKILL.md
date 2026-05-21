---
name: th-content-review
description: Use when published content needs a structured performance review that captures platform metrics, title learnings, source learnings, and concrete next actions without pretending placeholder data is real.
---

# th-content-review

Use this skill for Step 8 review work:

- post-publish review scaffolding
- performance review card generation
- weekly / monthly review scaffolding
- source and title learning capture

## Important boundary

- This skill works **after** there are queue items and at least some publish outcomes.
- It does **not** fabricate metrics.
- It does **not** treat guesswork as review.

Its job is:

> 把“发完了什么、效果如何、下次怎么改”收束成一份可积累经验的复盘卡。

## Load order

1. Read `../../../00_planning/20260324_对象字典与命名规范.md`
2. Read `../../../00_planning/20260324_状态流转规范.md`
3. If available, read `../../../08_brand_assets/latest__head-media-learning-rulebook-v1.md`
4. Read `../th-market-postmortem-optimizer/SKILL.md`
5. Read `../../../09_runbooks/20260325__market-publish-and-review-runbook.md`
6. Read `../../../09_runbooks/templates/market_performance_review_template.md`
7. Read related publish queue items

## Core workflow

1. Resolve the review scope:
   - one topic / one review window
   - multiple queue items allowed

2. Separate fact from placeholder:
   - real publish URLs
   - real timestamps
   - real metrics if available
   - placeholder fields only where data is still missing

3. Capture learnings in four buckets:
   - title / packaging learnings
   - context / audience learnings
   - platform render learnings
   - source learnings
   - next actions

4. Update review state honestly:
   - `scheduled`
   - `collecting`
   - `ready`
   - `closed`

5. Only mark `ready` or `closed` if there is enough real publish evidence.

## Hard constraints

- No fabricated metrics.
- No “review completed” if nothing was published.
- Do not collapse platform-specific learnings into generic platitudes.

## Output guidance

Output:

1. performance review card
2. platform metric placeholders or real metrics
3. concrete next actions
4. enough structured learnings that `th-market-postmortem-optimizer` can diagnose the next-round fix
