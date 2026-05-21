---
name: th-market-postmortem-optimizer
description: Use when TH Capital published content needs a true postmortem that turns review evidence into reusable operating rules for topic packaging, context clarity, audience fit, platform rendering, and next-round experiments. This skill converts review notes into optimization actions instead of leaving them as vague summaries.
---

# th-market-postmortem-optimizer

Use this skill when working on:

- post-publish diagnosis
- review synthesis
- title / hook failure analysis
- context / audience / render mismatch analysis
- experiment design for the next round
- turning one review into reusable content rules

This skill exists to solve one specific problem:

> 复盘不能只写“效果一般 / 后续优化”，而是要明确：问题出在哪一层、下次具体怎么改。

## Important boundary

- This skill works **after** real review evidence exists.
- This skill does **not** fabricate metrics or user reactions.
- This skill does **not** replace the review card itself.
- This skill does **not** overfit one lucky or unlucky post into universal truth.
- This skill does **not** confuse diagnosis with execution; it outputs optimization instructions, not fake results.

Its job is:

> 把“复盘卡”进一步升级成“下一轮可以直接拿来优化系统的规则和实验”。 

## Load order

1. Read `../../../00_planning/20260325_内容增长方法论与平台黄金标准.md`
2. Read `../th-market-hook-title-cover/SKILL.md`
3. Read `../th-market-context-bridge/SKILL.md`
4. Read `../th-market-audience-translator/SKILL.md`
5. Read `../th-market-platform-renderer/SKILL.md`
6. If available, read `../../../08_brand_assets/latest__head-media-learning-rulebook-v1.md`
7. Read `references/postmortem-dimensions.md`
8. Read `references/diagnosis-matrix.md`
9. Read `references/output-contract.md`
10. If a concrete example helps, read `references/example-minicor-postmortem.md`
11. Read:
   - related `performance_review`
   - related queue items
   - if available, final published URLs / screenshots / comment samples

## Core workflow

1. Confirm the evidence level.

Sort evidence into:

- hard evidence:
  - real publish time
  - real URL
  - real metrics
  - real comments / reactions
- soft evidence:
  - qualitative impression
  - internal judgment
- missing evidence

If the evidence is too thin, output a limited diagnosis instead of fake certainty.

2. Diagnose by funnel layer.

Every postmortem should first ask:

- was this mainly a click problem?
- mainly a cold-start clarity problem?
- mainly a read-through problem?
- mainly an audience mismatch problem?
- mainly a render / packaging execution problem?

3. Diagnose by content system component.

Map the issue to one or more components:

- topic choice
- hook / title / cover
- context bridge
- audience translation
- platform rendering
- timing
- CTA / conversion

4. Separate symptom from root cause.

Example:

- symptom: low read-through
- possible roots:
  - title over-promised
  - context arrived too late
  - paragraph rhythm too heavy

5. Produce reusable learning statements.

Good learning statements look like:

- `When topic X is niche, the object must be named by paragraph 2 on WeChat.`
- `For Layer A audiences, term Y needs plain-language translation before the argument starts.`
- `On X, strong opinions without clear subject naming lose traction fast.`

Bad learning statements look like:

- `Need stronger content next time`
- `Need better writing`
- `Need optimize title`

6. Propose next-round experiments.

For each major issue, define:

- what to change
- where to change it
- what metric or sign to watch next time

7. Write back to the right layer.

The output should explicitly say whether the learning belongs to:

- hook / title / cover
- context bridge
- audience translator
- platform renderer
- topic radar / selection

## Required output format

When this skill is used, output:

1. `evidence_level`
2. `main_failure_or_success_layer`
3. `symptoms`
4. `likely_root_causes`
5. `component_mapping`
6. `reusable_learnings`
7. `next_round_experiments`
8. `what_not_to_overgeneralize`
9. `which_skill_should_be_updated`
10. `short_operator_summary`

## Hard constraints

- No fabricated certainty from weak evidence.
- No postmortem that only repeats metrics without diagnosis.
- No generic learning statements that cannot guide next action.
- No blaming “the platform” when the draft itself likely failed.
- No turning one outlier into a universal law.

## Output guidance

When the task is **single-post review optimization**, produce:

1. funnel diagnosis
2. component mapping
3. 3-5 reusable learnings
4. 1-3 next experiments

When the task is **weekly / batch review optimization**, produce:

1. repeated patterns across posts
2. what seems platform-specific
3. what seems audience-specific
4. which skills need rule updates
