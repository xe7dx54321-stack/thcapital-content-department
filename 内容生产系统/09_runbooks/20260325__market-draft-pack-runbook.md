# 同行资本市场内容系统｜2026-03-25｜Draft Pack 生成与状态推进

## 1. 这份 runbook 的作用

这份 runbook 用来承接已经确认的 `approved_topic`，并把它推进成多平台 `Draft Pack`。

它解决的是：

> 老板已经拍板了，现在系统如何把这个题变成 7 平台能力范围内、按平台束选择的可编辑稿件包？

## 2. 当前 owner

- 对外唯一前台 bot：`market-editor`

当前阶段：

- `market-editor` 负责从 `approved_topic` 生成 `Draft Pack`
- 仍然不自动发布
- 先生成可编辑、可继续打磨的内容包

## 3. 输入

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/04_approved_topics/YYYYMMDD_HHMMSS__topic_key__approved-topic.md`

没有 `approved_topic`，不允许直接起草正式内容包。

## 4. 执行步骤

1. 读取：
   - `th-draft-pack`
   - `08_brand_assets/20260324_平台定位与表达规范.md`
   - `market_draft_pack_manifest_template.md`
   - 各平台模板
   - 对应 `approved_topic`

2. 先运行 builder 建 pack 骨架：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_draft_pack_builder.py \
  --approved-topic-path <approved_topic_path> \
  --status drafting \
  --write
```

3. builder 完成后，确认以下文件都已落盘：
   - `00_draft-pack-card.md`
   - 已请求平台对应稿件
   - `packaging-bundle.md`
   - `context-bridge-notes.md`
   - `audience-notes.md`
   - `platform-render-plan.md`
   - `title-options.md`
   - `summary-options.md`
   - `citation-block.md`
   - `visual-notes.md`
   - `revision-notes.md`

4. 按平台模板补齐或优化正文。

5. 当所有 requested platforms 都达到可编辑 / 可继续打磨的完成度后，更新状态：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_draft_pack_builder.py \
  --approved-topic-path <approved_topic_path> \
  --status ready \
  --write
```

这一步会：

- 更新 `00_draft-pack-card.md` 为 `ready`
- 把源 `approved_topic` 状态推进到 `draft_ready`
- 补一条 Draft Pack execution log

## 5. 标准产出

输出目录：

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/{topic_key}/`

标准文件：

- `00_draft-pack-card.md`
- `wechat.md`
- `xiaohongshu.md`
- `zhihu.md`
- `x.md`
- `bilibili.md`
- `toutiao.md`
- `baijiahao.md`
- `packaging-bundle.md`
- `context-bridge-notes.md`
- `audience-notes.md`
- `platform-render-plan.md`
- `title-options.md`
- `summary-options.md`
- `citation-block.md`
- `visual-notes.md`
- `revision-notes.md`

说明：

- 只生成 `approved_topic.requested_platforms` 中要求的平台稿件
- 不是每次都必须七个平台全出

## 6. 状态纪律

- 刚建包：`drafting`
- 可交给人继续打磨 / 排队前：`ready`

状态映射：

- `draft_pack.drafting` 对应 `approved_topic.drafting`
- `draft_pack.ready` 对应 `approved_topic.draft_ready`

## 7. 对外回报方式

`market-editor` 对创始人的回报要尽量短，只说：

- 哪个题已经进入 Draft Pack
- 先生成了哪些平台版本
- Draft Pack 目录路径
- 当前状态是 `drafting` 还是 `ready`

## 8. 关键边界

- 不得把同一篇长文机械裁切成所有平台版本
- 不得省略冷启动背景桥接
- 不得丢掉 source refs 与 risk note
- 不得直接越级进入 `publish_queue`
