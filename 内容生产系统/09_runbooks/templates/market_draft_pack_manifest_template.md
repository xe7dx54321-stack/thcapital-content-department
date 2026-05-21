# Draft Pack Manifest Template

## 使用场景

这张卡是一个 `Draft Pack` 的总索引。

它的作用是把一个选题对应的：

- 平台稿件
- 标题备选
- 摘要备选
- 引用块
- 视觉建议
- 修订说明

统一收束在同一个地方，便于后续继续打磨和进入发布队列。

## 必备字段

- `draft_id`
- `draft_key`
- `topic_id`
- `approved_topic_path`
- `requested_platforms`
- `status`
- `created_at`
- `updated_at`

## 建议补充字段

- `wechat_path`
- `xiaohongshu_path`
- `zhihu_path`
- `x_path`
- `bilibili_path`
- `toutiao_path`
- `baijiahao_path`
- `title_options_path`
- `summary_options_path`
- `packaging_bundle_path`
- `context_bridge_path`
- `audience_notes_path`
- `render_plan_path`
- `citation_block_path`
- `visual_notes_path`
- `inline_visual_plan_path`
- `revision_notes_path`
- `core_judgment`
- `approved_angle`
- `risk_note`

## 推荐格式

```markdown
# Draft Pack Card

- `draft_id`: `draft__YYYYMMDD_HHMMSS__topic_key`
- `draft_key`: `topic_key`
- `topic_id`: `topic__...`
- `approved_topic_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/04_approved_topics/...`
- `requested_platforms`: `wechat, zhihu`
- `status`: `drafting`
- `created_at`: `YYYY-MM-DD HH:MM:SS CST`
- `updated_at`: `YYYY-MM-DD HH:MM:SS CST`

## Pack Paths

- `wechat_path`: `/Users/apple/Documents/.../wechat.md`
- `xiaohongshu_path`: `n/a`
- `zhihu_path`: `/Users/apple/Documents/.../zhihu.md`
- `x_path`: `n/a`
- `bilibili_path`: `n/a`
- `toutiao_path`: `n/a`
- `baijiahao_path`: `n/a`
- `title_options_path`: `/Users/apple/Documents/.../title-options.md`
- `summary_options_path`: `/Users/apple/Documents/.../summary-options.md`
- `packaging_bundle_path`: `/Users/apple/Documents/.../packaging-bundle.md`
- `context_bridge_path`: `/Users/apple/Documents/.../context-bridge-notes.md`
- `audience_notes_path`: `/Users/apple/Documents/.../audience-notes.md`
- `render_plan_path`: `/Users/apple/Documents/.../platform-render-plan.md`
- `citation_block_path`: `/Users/apple/Documents/.../citation-block.md`
- `visual_notes_path`: `/Users/apple/Documents/.../visual-notes.md`
- `inline_visual_plan_path`: `/Users/apple/Documents/.../inline-visual-plan.md`
- `revision_notes_path`: `/Users/apple/Documents/.../revision-notes.md`

## Carried Core

- `core_judgment`: `...`
- `approved_angle`: `...`
- `risk_note`: `...`

## Next Step

- `next_step`: `drafting -> ready`
- `publish_gate`: `not allowed yet`
```
