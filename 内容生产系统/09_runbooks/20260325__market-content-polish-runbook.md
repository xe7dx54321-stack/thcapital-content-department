# 同行资本市场内容系统｜2026-03-25｜内容打磨与基础成品化

## 1. 这份 runbook 的作用

这份 runbook 用来承接已经存在的 `Draft Pack`，把它从“可编辑稿件”推进成“更像同行资本、并具备基础成品感”的内容资产。

它解决的是：

> Draft Pack 已经有了，但如何进一步做多轮打磨、去 AI 味、增强品牌表达，并补齐基础成品化 handoff？

## 2. 当前 owner

- 对外唯一前台 bot：`market-editor`

当前阶段：

- `market-editor` 负责做文本打磨
- `market-editor` 负责补基础成品化 handoff
- 仍然不进入 `publish_queue`

## 3. 输入

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/{topic_key}/`

没有 Draft Pack，不允许直接做打磨层。

## 4. 执行步骤

1. 读取：
   - `th-content-polish`
   - `th-content-repurpose`
   - `08_brand_assets/20260324_平台定位与表达规范.md`
   - polishing / readiness / handoff templates
   - 对应 Draft Pack card 与平台稿件

2. 先运行 builder 建立打磨支撑文件：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_content_polish_builder.py \
  --draft-pack-dir <draft_pack_dir> \
  --status needs_revision \
  --write
```

3. 按 `th-content-polish` 进行多轮 sweep，并直接修改平台稿件：
   - context bridge landing
   - clarity
   - de-AI
   - personality consistency
   - stronger judgment
   - hook and title
   - first-screen promise/body match
   - early proof anchor
   - citation retention
   - platform fit

4. 标题点击率优化属于内容业务岗职责，不由总控临场手改：
   - 标题 / 封面 / 首屏钩子必须由 `content-writer / market-editor` 在 polish 阶段自己完成
   - 先读 `th-market-hook-title-cover`
   - 先改当前对象的标题与包装，不要因为标题差就直接换题
   - 优先保证“对象 + 动作 + 读者收益/风险”清楚，而不是追求抽象的高级感
   - 禁止半截标题、内部研究标题、只有数字/技术名词的标题、以及带省略号的糊题面

5. 再按 `th-content-repurpose` 补基础成品化 handoff：
   - WeChat HTML handoff
   - cover / visual brief
   - cover asset assist
   - Xiaohongshu card brief（如相关）

6. 如果打磨后内容已可进入下一阶段，再运行：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_content_polish_builder.py \
  --draft-pack-dir <draft_pack_dir> \
  --status ready \
  --write
```

7. 如果仍有明显缺口，就保留 `needs_revision`，并在 `publish-readiness.md` 明确写出 blocker。

## 5. 标准产出

输出到 Draft Pack 目录：

- `polish-checklist.md`
- `polish-notes.md`
- `publish-readiness.md`
- `voice-consistency-notes.md`
- `platform-render-handoff.md`
- `cover-visual-brief.md`
- `cover-asset-assist.md`
- `wechat-html-handoff.md`（如有微信稿）
- `xiaohongshu-card-brief.md`（如有小红书稿）

并同步落盘 execution log：

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/YYYYMMDD_HHMMSS__topic_key__content-polish-execution.md`

## 6. 状态纪律

- 打磨发现仍不够：`needs_revision`
- 打磨后已达到下一阶段标准：`ready`

这一步更新的是 `draft_pack.status`，不直接进入发布队列。

## 7. 对外回报方式

`market-editor` 对创始人的回报要尽量短，只说：

- 哪个 Draft Pack 已完成打磨
- 当前状态是 `needs_revision` 还是 `ready`
- 如果还没过，主要 blocker 是什么
- 如果已过，哪些 handoff 资产已补齐

## 8. 关键边界

- 不得为了“更顺”把判断磨平
- 不得为了“更像人”丢掉信息密度
- 不得把“去 AI 味”做成空洞口语化
- 不得为了“更好看”去掉 source refs 与风险提示
- 不得假装已经完成 HTML / 图片生产，只能写 handoff 准备情况
