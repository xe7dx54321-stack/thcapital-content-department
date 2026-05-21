---
name: th-draft-pack
description: Use when an approved topic must be turned into a multi-platform draft pack for the TH Capital Phase 1 platform set: WeChat, Xiaohongshu, Zhihu, X, Bilibili column, Toutiao, and Baijiahao. Preserve one core judgment, citations, risk notes, and platform-specific rewriting rules without mechanically pushing every topic to all platforms.
---

# th-draft-pack

Use this skill for Step 6 work:

- approved topic to multi-platform draft pack
- platform rewriting
- title / summary / citation / visual asset generation
- draft pack status transition

## Important boundary

- This skill works **after** `approved_topic` exists.
- It does **not** replace explicit topic approval.
- It does **not** auto-publish.
- It does **not** turn every platform into the same article with different length.

Its job is:

> 把一张已经拍板的 `approved_topic` 卡，转成一套可编辑、可继续打磨、可保留引用依据的多平台 Draft Pack。

## Load order

1. Read `../../../00_planning/20260324_对象字典与命名规范.md`
2. Read `../../../00_planning/20260324_状态流转规范.md`
3. Read `../../../00_planning/20260324_目录结构规范.md`
4. Read `../../../08_brand_assets/20260324_平台定位与表达规范.md`
5. If available, read `../../../08_brand_assets/latest__head-media-learning-rulebook-v1.md`
6. If available, read `../../../08_brand_assets/learning_knowledge_assets/latest__learning-knowledge-index.md`
7. If available, read `../../../08_brand_assets/learning_knowledge_assets/latest__style-router.md`
8. If available, read `../../../08_brand_assets/learning_knowledge_assets/visual_playbooks/th_capital_visual_playbook_v2.md`
9. Read `../th-market-hook-title-cover/SKILL.md`
10. Read `../th-market-context-bridge/SKILL.md`
11. Read `../th-market-audience-translator/SKILL.md`
12. Read `../../../09_runbooks/20260325__market-draft-pack-runbook.md`
13. Read `../../../09_runbooks/templates/market_draft_pack_manifest_template.md`
14. Read `../../../09_runbooks/templates/market_wechat_draft_template.md`
15. Read `../../../09_runbooks/templates/market_xiaohongshu_draft_template.md`
16. Read `../../../09_runbooks/templates/market_zhihu_draft_template.md`
17. Read `../../../09_runbooks/templates/market_x_thread_template.md`
18. Read `../../../09_runbooks/templates/market_bilibili_draft_template.md`
19. Read `../../../09_runbooks/templates/market_toutiao_draft_template.md`
20. Read `../../../09_runbooks/templates/market_baijiahao_draft_template.md`
21. Read the selected `approved_topic`

## Core workflow

1. Confirm the source `approved_topic`.
   - No approved topic, no Draft Pack.

2. Carry forward the immutable core:
   - title
   - approved angle
   - requested platforms
   - special instructions
   - carried judgment
   - source refs
   - risk note

3. Recalculate each platform version independently.

Do **not** do one article and then cut it into seven.

3A. Select a style route explicitly before writing.
   - choose one `content_route`
   - choose one `primary_overlay`
   - optionally one `secondary_overlay`
   - load the corresponding `overlay skill`
   - read that creator pack's `skill-card.md`, `text-patterns.md`, and `visual-patterns.md`
   - lock the borrowed layers:
     - title / cover
     - opening hook
     - context bridge
     - evidence placement
     - paragraph rhythm
     - visual pacing
   - never borrow every layer from every creator

For each platform, re-decide:

- user state
- audience layer
- opening hook
- context bridge
- information density
- structure
- CTA
- render rhythm / first-screen structure

4. Build the common support assets:
   - title / cover / opening packaging bundle
   - context bridge notes
   - audience translation notes
   - platform render plan
   - title options
   - summary / lead options
   - citation block
   - visual notes
   - revision notes

5. Use the builder to scaffold or update the pack:

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_draft_pack_builder.py \
  --approved-topic-path <approved_topic_path> \
  --status drafting \
  --write
```

6. Fill requested platform drafts with platform-specific copy.

Phase 1 standard support set:

- `wechat`
- `xiaohongshu`
- `zhihu`
- `x`
- `bilibili`
- `toutiao`
- `baijiahao`

7. When all requested platform drafts are substantially complete:
   - mark draft pack `ready`
   - mark source `approved_topic` as `draft_ready`

## Platform rules

### WeChat

- 半深度主阵地
- 讲清楚，不写成研报
- 结构完整、变量清楚、结尾可带轻 CTA

### Xiaohongshu

- 低门槛入口
- 先抓注意力，再给结论
- 3-5 个点，短句，高信息密度

### Zhihu

- 问题导向
- 先回答，再论证
- 比公众号更直接，比小红书更系统

### X

- 快、准、轻
- 单条或 thread
- 每一条都要有信息增量

### Bilibili

- builder 社区深度补位
- 允许更实操、更像教程 / 复盘
- 必须讲过程、卡点、适用边界

### Toutiao

- 泛流量实验层
- 更口语、更强钩子、更强标题意识
- 不能为了流量把判断写歪

### Baijiahao

- SEO 镜像层
- 问题标题、关键词承接、结构稳定
- 不能写成没有人味的百科堆词稿

## Hard constraints

- No citation stripping.
- No one-size-fits-all rewrite.
- Do not change the approved angle without explicit human instruction.
- Do not bury the risk note.
- Do not silently add platforms not requested.
- Do not interpret “Phase 1 supports 7 platforms” as “every topic must output 7 drafts”.

## Output guidance

When the task is **pack generation**, output:

1. draft pack card
2. requested platform drafts
3. packaging bundle
4. context bridge notes
5. audience notes
6. render plan
7. title options
8. summary options
9. citation block
10. visual notes
11. revision notes

When the task is **pack refinement**, output:

1. changed files
2. revision rationale
3. remaining gaps before `ready`
