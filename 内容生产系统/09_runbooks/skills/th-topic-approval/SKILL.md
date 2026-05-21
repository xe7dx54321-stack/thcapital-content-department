---
name: th-topic-approval
description: Use when a founder has explicitly picked a topic candidate or holdout item and market-editor must turn that instruction into a normalized approved topic card with angle, platform scope, carried citations, and next-step draft handoff.
---

# th-topic-approval

Use this skill for Step 5 work:

- founder topic confirmation intake
- `Top 5` / `Holdout 3` selection normalization
- approved topic card creation
- post-selection scope clarification
- draft handoff preparation

## Important boundary

- This skill works **after** Topic Radar board generation.
- It does **not** generate the Draft Pack itself.
- It does **not** auto-publish.
- It does **not** invent approval where the founder has not clearly confirmed.

Its job is:

> 把“老板已经明确拍板了什么题、怎么写、做哪些平台”收束成一张标准化 `approved_topic` 卡。

补充纪律：

- 如果创始人**明确指定平台**，按人工指定执行。
- 如果创始人**没有指定平台**，系统要基于题目属性、board 平台提示和 source refs 自动推荐一个平台束，并把理由写进 `approved_topic`。

## Load order

1. Read `../../../00_planning/20260324_对象字典与命名规范.md`
2. Read `../../../00_planning/20260324_状态流转规范.md`
3. Read `../../../00_planning/20260324_目录结构规范.md`
4. If available, read `../../../08_brand_assets/latest__head-media-learning-rulebook-v1.md`
5. If available, read `../../../08_brand_assets/learning_knowledge_assets/latest__style-router.md`
6. Read `../../../09_runbooks/20260325__market-topic-approval-runbook.md`
7. Read `../../../09_runbooks/templates/market_approved_topic_template.md`
8. Read the relevant board file in `../../../03_topic_candidates/`

## Valid founder instructions

Treat the following as valid explicit confirmation:

- `选第 2 个`
- `选第 7 个，捞回来`
- `第 3 个改成机构视角`
- `第 1 个只做微信和知乎`
- `选第 4 个，角度收敛到商业闭环`

Do **not** create `approved_topic` when the founder only says:

- `这个还行`
- `再看看`
- `先别动`
- `我想想`

## Core workflow

1. Resolve which board is being referenced.
   - Prefer the board explicitly referenced by the user.
   - Otherwise use the latest daily board.

2. Resolve selection target.
   - Support Top 1-5 items.
   - Support holdout restore 6-8 items.
   - Support candidate key when available.

3. Normalize approval scope.
   - `approved_angle`
   - `requested_platforms`
   - `special_instructions`
   - whether this is a holdout restore
   - if founder gave no explicit platform scope, recommend a platform bundle and explain why

4. Carry forward the source grounding.
   - Keep original links
   - Keep source packet paths
   - Keep original risk note
   - Keep the board path

5. Build a standard `approved_topic`.
   - status must start as `approved`
   - include future draft pack target dir
   - make downstream writing scope explicit enough that the founder does not need to repeat themselves
   - include platform decision metadata:
     - `platform_selection_mode`
     - `platform_bundle`
     - `platform_selection_reason`

5A. If the topic clearly matches a route in `latest__style-router.md`:
   - carry a short style route note into `special_instructions`
   - format: `style_route=<route>; primary_overlay=<creator>; overlay_skill=<skill>; borrowed_layers=<x/y/z>`
   - this is not a full draft instruction; it is a downstream routing hint

6. Persist with the builder script:

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_approved_topic_builder.py \
  --board-path <board_path> \
  --rank <rank> \
  --approved-angle "<angle>" \
  --special-instructions "<instructions>" \
  --selection-instruction "<original founder instruction>" \
  --approved-by 老板 \
  --write
```

如果创始人没有明确指定平台，上面这条命令可以**不传 `--platform`**，builder 会自动推荐平台束。

7. Reply to the founder briefly.
   - Say which topic has been locked
   - Say which platforms will be produced
   - Say where the approved topic card was written
   - Say the next step is Draft Pack generation

## Hard constraints

- No explicit founder confirmation, no `approved_topic`.
- Do not skip citations.
- Do not lose the original board path.
- Do not auto-upgrade directly to publish queue.
- Do not turn vague founder preference into strong instructions without saying it is an assumption.

## Output guidance

When the task is **approval intake**, output:

1. approval resolution
2. normalized angle
3. normalized platform scope
4. approved topic path
5. next step

When the task is **holdout restore**, also output:

1. why the holdout was restored
2. what changed in the angle
3. what risk remains
