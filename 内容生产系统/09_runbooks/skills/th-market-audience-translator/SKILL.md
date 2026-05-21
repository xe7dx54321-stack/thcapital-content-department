---
name: th-market-audience-translator
description: Use when the same TH Capital topic or draft must be translated for different audience layers such as AI-curious beginners, tech operators / builder-adjacent readers, or business / investment-oriented readers. This skill preserves the same core judgment while changing explanation depth, terminology, user payoff, and reading threshold.
---

# th-market-audience-translator

Use this skill when working on:

- audience-layer rewriting
- turning the same idea into beginner / operator / business-facing versions
- lowering the reading threshold without dumbing down the core judgment
- preserving TH Capital sharpness while making copy more usable to different readers
- repairing drafts that feel “too insider”, “too academic”, or “not relevant enough”

This skill exists to solve one specific problem:

> 同一个结论，对不同人群不能只靠“缩短一点”或“口语一点”解决，而是要真正翻译成他们关心的话。

## Important boundary

- This skill does **not** change the topic or approved angle.
- This skill does **not** replace hook / title packaging.
- This skill does **not** replace context bridging.
- This skill does **not** force every platform to serve every audience equally.
- This skill does **not** flatten TH Capital into generic beginner content.

Its job is:

> 在保留同一核心判断的前提下，让不同人群都能觉得“这和我有关，而且我看得懂”。

## Load order

1. Read `../../../00_planning/20260325_内容增长方法论与平台黄金标准.md`
2. Read `../../../08_brand_assets/20260324_公域品牌上下文手册.md`
3. Read `../../../08_brand_assets/20260324_平台定位与表达规范.md`
4. If available, read `../../../08_brand_assets/latest__head-media-learning-rulebook-v1.md`
5. Read `../th-market-brand-context/SKILL.md`
6. If the opening is also changing, read `../th-market-hook-title-cover/SKILL.md`
7. If cold-start understanding is weak, read `../th-market-context-bridge/SKILL.md`
8. Read `references/audience-layers.md`
9. Read `references/translation-rules.md`
10. If debugging a weak draft, read `references/audience-mismatch-diagnosis.md`
11. If a concrete example helps, read `references/example-agent-commerce-three-layers.md`
12. Read the selected `approved_topic`, `draft_pack`, or live draft

## Core workflow

1. Identify the current implied audience.

Ask:

- Who can already read this easily?
- Who is likely to bounce because the copy assumes too much?
- Who might understand the facts but still not feel any personal stake?

2. Choose one primary audience layer.

Default layers:

- `layer_a`: AI-curious beginner / one-person-company aspirer
- `layer_b`: tech operator / creator / builder-adjacent reader
- `layer_c`: business / investment / strategic reader

3. Preserve the invariant core.

Keep fixed:

- approved angle
- core judgment
- real source refs
- actual risk note

Only translation may change:

- terminology density
- order of explanation
- user payoff framing
- examples
- analogy level

4. Rewrite from the audience’s real question.

### Layer A usually asks:

- 这到底是什么？
- 跟我有什么关系？
- 我为什么要关心？
- 我能怎么用？

### Layer B usually asks:

- 这条线是机会还是噪音？
- 哪个 workflow / skill / product shape 真有用？
- 落地门槛和关键变量是什么？

### Layer C usually asks:

- 这是结构变化还是短期热度？
- 价值会积在哪一层？
- 平台、分发、商业模式会怎么变？

5. Translate terminology honestly.

Do not simply delete terms.

For each important term:

- keep it if it matters
- explain it in audience language
- decide whether the term should appear before or after the plain-language explanation

6. Recalculate the reader payoff.

The same core claim may need a different “why you care” line:

- Layer A: personal leverage / learning / opportunity
- Layer B: execution / workflow / edge
- Layer C: market structure / strategic consequence

7. Run the mismatch check.

Reject any version that:

- talks down to the audience
- becomes generic and empty
- loses the real TH Capital judgment
- confuses simplicity with shallowness
- gives beginner users jargon without translation
- gives advanced readers fluff instead of structure

## Required output format

When this skill is used, output:

1. `target_platform`
2. `target_audience_layer`
3. `core_claim`
4. `reader_primary_question`
5. `terminology_to_translate`
6. `recommended_user_payoff_frame`
7. `translated_opening_or_section`
8. `what_changed_from_base_version`
9. `what_must_not_change`
10. `risks_if_over-translated`

If generating multiple audience versions, also output:

11. `layer_a_version`
12. `layer_b_version`
13. `layer_c_version`

## Platform guidance

### WeChat

- Usually strongest for Layer B or Layer B/C hybrid
- Can still support Layer A if the background and payoff are clearly translated

### Xiaohongshu

- Usually starts from Layer A
- Can carry Layer B insight, but only after threshold is lowered

### Zhihu

- Usually Layer B or Layer C
- Layer A still possible when the topic is highly searched and confusing

### X

- Usually needs one sharp layer at a time
- Do not try to speak to all three layers in one opening

## Hard constraints

- No rewriting that changes the thesis.
- No audience “translation” that removes all useful specificity.
- No beginner version that becomes motivational fluff.
- No operator / investor version that becomes unreadable jargon soup.
- No claiming that different audience versions are different facts; only their framing and explanation depth change.

## Output guidance

When the task is **single-layer rewrite**, produce:

1. target layer
2. reader question
3. translated version
4. terminology notes
5. why this version fits

When the task is **multi-layer translation**, produce:

1. one invariant core block
2. three audience versions
3. a note on which platform each version best fits
