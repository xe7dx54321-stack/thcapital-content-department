# Publish Queue Item Template

## 作用

记录某一个平台维度的待发布 / 已发布状态。

## 必备字段

- `queue_id`
- `queue_key`
- `topic_id`
- `draft_id`
- `platform`
- `content_path`
- `publish_owner`
- `planned_publish_at`
- `actual_publish_at`
- `publish_url`
- `primary_handoff_path`
- `supporting_asset_paths`
- `manual_gate`
- `human_action_required`
- `frontstage_summary`
- `status`
- `notes`

## 推荐格式

```markdown
# Publish Queue Item

- `queue_id`: `queue__YYYYMMDD_HHMMSS__topic_key__wechat`
- `queue_key`: `topic_key__wechat`
- `topic_id`: `topic__...`
- `draft_id`: `draft__...`
- `platform`: `wechat`
- `content_path`: `/Users/apple/Documents/.../wechat.md`
- `publish_owner`: `老板`
- `planned_publish_at`: `YYYY-MM-DD HH:MM:SS CST`
- `actual_publish_at`: `n/a`
- `publish_url`: `n/a`
- `primary_handoff_path`: `/Users/apple/Documents/.../wechat-html-handoff.md`
- `supporting_asset_paths`: `/Users/apple/Documents/.../platform-render-handoff.md, /Users/apple/Documents/.../publish-readiness.md, /Users/apple/Documents/.../inline-visual-plan.md, /Users/apple/Documents/.../visual-asset-sourcing.md`
- `manual_gate`: `human_publish_required`
- `human_action_required`: `按 handoff 完成人工发布，发完回填 publish_url`
- `frontstage_summary`: `wechat 已待人工发布，owner=老板`
- `status`: `queued`
- `notes`: `n/a`
```
