# P18-001 Visual-approved Final Article Candidate Report

## 目标

把 final article candidate、image asset library、article visual plan 和 final visual review 合并成视觉已审查的最终图文候选稿。

## 已完成

- 新增 `visual_approved_final_candidate.py`。
- 输出 `visual-approved-final-candidates` JSON/Markdown sidecar。
- 记录每个 image slot 的 asset status、visual review status、wechat_ready 与 remaining visual risks。

## 边界

- `would_publish=false`。
- `do_not_publish=true`。
- 视觉就绪不等于自动发布。
