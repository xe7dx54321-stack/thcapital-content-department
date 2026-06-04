# P18-003 Manual Publishing Checklist with Visual Assets Report

## 目标

在最终发布 checklist 中加入图片检查项，覆盖首图、槽位、手机端可读性、版权说明和 slot marker 删除。

## 已完成

- 新增 `visual_publishing_checklist.py`。
- 输出 `visual-publishing-checklist` JSON/Markdown sidecar。
- 每个 checklist 保留 `final_human_confirmation_required=true` 和 `would_publish=false`。

## 边界

- checklist 只辅助人工发布前检查。
- 不自动把候选稿设为已发布。
