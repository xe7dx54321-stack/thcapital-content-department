---
name: th-market-platform-renderer
description: Use when a polished TH Capital master draft must be turned into platform-ready handoff assets for WeChat, Xiaohongshu, Zhihu, X, Bilibili column, Toutiao, or Baijiahao. This skill converts Markdown-like middle drafts into render-ready final structures, emphasis instructions, and publish-safe handoff packs without pretending the content has already been posted.
---

# th-market-platform-renderer

Use this skill when working on:

- final platform rendering before publish queue
- WeChat HTML handoff design
- Xiaohongshu card decomposition
- Zhihu final-structure cleanup
- X thread final layout
- Bilibili / Toutiao / Baijiahao final text rendering
- render QA before human publishing

This skill exists to solve one specific problem:

> 把“已经写好的中间稿”，变成“真正接近可发成品的平台终稿 handoff”。

## Important boundary

- This skill works **after** a platform draft already exists.
- This skill does **not** replace topic choice, hook choice, or context design.
- This skill does **not** auto-post content.
- This skill does **not** pretend HTML / image / card assets are already physically generated when they are not.
- This skill does **not** change the approved angle just to make layout easier.

Its job is:

> 让不同平台的最终呈现方式，真正像这个平台，而不是“同一份 Markdown 换了个文件名”。

Important production note:

- `docx` is a review artifact, not the true publish artifact.
- In real production, prioritize:
  - WeChat HTML handoff
  - Xiaohongshu card brief
  - Zhihu answer-final structure
  - X final thread layout
  - Bilibili / Toutiao / Baijiahao final text cleanup

## Load order

1. Read `../../../00_planning/20260325_内容增长方法论与平台黄金标准.md`
2. Read `../../../08_brand_assets/20260324_平台定位与表达规范.md`
3. Read `../th-market-brand-context/SKILL.md`
4. Read `../th-market-hook-title-cover/SKILL.md`
5. Read `../th-market-context-bridge/SKILL.md`
6. If available, read `../../../08_brand_assets/latest__head-media-learning-rulebook-v1.md`
7. Read `references/render-principles.md`
8. Read `references/platform-render-checklists.md`
9. Read `references/output-contracts.md`
10. If a concrete example helps, read `references/example-deerflow-render-package.md`
11. Read:
   - `../../../09_runbooks/templates/market_wechat_html_handoff_template.md`
   - `../../../09_runbooks/templates/market_cover_visual_brief_template.md`
   - `../../../09_runbooks/templates/market_xiaohongshu_card_brief_template.md`
   - `../../../09_runbooks/templates/market_publish_readiness_template.md`
12. Read the selected Draft Pack card and platform draft

## Core workflow

1. Confirm the source state.

You need:

- a concrete platform draft
- a stable approved angle
- known source refs / risk note

If the draft itself is structurally weak, send it back to drafting / polish instead of faking a render-ready output.

2. Decide whether the draft is still a master draft or already platform-shaped.

Ask:

- Is this just a generic article in Markdown?
- Does the current version already fit the platform’s reading rhythm?
- What is still missing between “readable text” and “publishable handoff”?

3. Re-render by platform, not by file format alone.

For each platform, decide:

- first-screen structure
- line-length rhythm
- subhead density
- which lines deserve emphasis
- where visuals belong
- where quote blocks or key-message blocks belong
- how CTA should appear
- where proof should appear early
- where the first screen should stop

4. Preserve the invariant core.

Always keep:

- approved angle
- core judgment
- real source refs
- real risk note

Rendering may change presentation, but not truth conditions.

5. Produce the right render asset set.

Possible outputs:

- WeChat HTML handoff
- cover / visual brief
- Xiaohongshu card brief
- platform render handoff summary
- Zhihu final rendering notes
- X thread layout notes
- Bilibili final article structure
- Toutiao final article structure
- Baijiahao SEO-safe final structure
- publish-readiness recommendation

6. Mark the platform-specific render delta.

Explicitly state what changed from master draft to render handoff:

- stronger first screen
- shorter paragraphs
- quote block insertion
- image / card placement
- CTA relocation
- source-note placement

7. Run renderer QA.

Check:

- can this be handed to a human publisher without lots of guesswork?
- are key emphasis points obvious?
- is the first screen properly packaged?
- is the context bridge landing early enough?
- are citations / risk signals still preserved?
- does the platform version feel native rather than transplanted?

8. For long-form platforms, render section jobs explicitly.

Long-form platforms:

- WeChat
- Zhihu
- Bilibili
- Baijiahao
- Toutiao

For these, always decide:

- where the reader first understands the event
- where the first proof anchor appears
- what each section is doing
- where the first natural stopping point is
- where visuals reduce fatigue instead of becoming decoration

## Required output format

When this skill is used, output:

1. `target_platform`
2. `source_draft`
3. `render_goal`
4. `render_delta`
5. `first_screen_plan`
6. `emphasis_map`
7. `visual_slots`
8. `section_job_map`
9. `proof_cadence`
10. `cta_plan`
11. `render_handoff`
12. `qa_notes`
13. `remaining_manual_steps`

If multiple handoff assets are needed, also output:

14. `which_files_to_update`

## Platform guidance

### WeChat

- Optimize for: first-screen clarity + longer read-through
- Handoff should specify:
  - title
  - optional subhead / lead
  - paragraph rhythm
  - quote block placement
  - emphasis line placement
  - image insertion zones
  - source/risk retention
  - first-screen stopping point
  - section-by-section job map

### Xiaohongshu

- Optimize for: card-by-card consumption
- Rendering should think in:
  - cover
  - page 1 conclusion
  - page 2-4 breakdown
  - last page interaction / CTA

### Zhihu

- Optimize for: answer-first readability
- Rendering should specify:
  - direct answer block
  - background bridge placement
  - structured lists
  - source-friendly ending
  - which paragraph is the direct answer
  - where the first evidence appears

### X

- Optimize for: thread progression
- Rendering should specify:
  - line 1 claim
  - line 2 context
  - line 3+ breakdown
  - last line follow-up or question

### Bilibili

- Optimize for: builder / community reading rhythm
- Rendering should specify:
  - what practical promise the reader gets
  - where steps / pitfalls / examples appear
  - how to make it feel like a real build log instead of a generic article
  - where practical takeaway appears before abstract discussion

### Toutiao

- Optimize for: faster first-screen payoff
- Rendering should specify:
  - headline punch
  - first 2 short paragraphs
  - section block rhythm
  - where大众表达 replaces abstract wording
  - where the background is cashed without拖沓

### Baijiahao

- Optimize for: search readability + stable structure
- Rendering should specify:
  - keyword-anchored title
  - answer-first opening
  - subheads that match search intent
  - source / risk retention without breaking SEO readability
  - a section map that prevents the article from becoming keyword stuffing

## Hard constraints

- No fake claim that the final HTML / cards / cover are already produced unless they truly are.
- No rendering pass that strips out source refs or hides risk note.
- No “native platform” claim when the output still reads like transplanted long-form Markdown.
- No visually strong package that creates semantic drift.
- No platform render that ignores the user’s reading rhythm.

## Output guidance

When the task is **single-platform render prep**, produce:

1. render goal
2. first-screen plan
3. emphasis map
4. render handoff
5. manual next step
