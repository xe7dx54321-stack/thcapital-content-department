# Inline Visual Plan Template

## 作用

把“这篇内容哪里该放图、放什么图、为什么放、优先怎么取图”收束成一张可执行的计划卡。

## 推荐格式

```markdown
# Inline Visual Plan

- `draft_key`: `topic_key`
- `topic_title`: `...`
- `approved_angle`: `...`

## Visual Strategy

- `core_visual_goal`: `...`
- `preferred_asset_order`: `原始截图 > 官方资产 > 解释图 > 外部补图 > AI 生成图`

## Platform Slots

### `WeChat`

- `slot_1`: `首屏后`
- `job`: `原始证据锚点`
- `preferred_asset`: `原始公告 / 推文 / repo 标题区截图`
- `fallback`: `对象 logo + 关键结论图卡`

### `Zhihu`

- `slot_1`: `背景讲清后`
- `job`: `解释对象与问题`
- `preferred_asset`: `对象截图 + 解释型副标题`
- `fallback`: `结构图`

## Source Candidates

- `candidate_1`: `https://...`
- `asset_type`: `原始推文截图`
- `best_use`: `证明原始事件`

## Human QC

- 这张图是不是在证明 / 解释某件具体事情？
- 如果删掉这张图，正文会不会失去一个关键停顿点？
- 这张图会不会误导成别的话题？
```
