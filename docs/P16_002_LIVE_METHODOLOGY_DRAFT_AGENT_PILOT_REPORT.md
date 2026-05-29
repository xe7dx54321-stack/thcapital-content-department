# P16-002 Live Methodology Draft Agent Pilot Report

## 本轮目标

为 methodology-aware draft 增加 live sidecar，验证高智力模型能否生成更像公众号成品的稿件。

## 已完成

- 新增 `live_methodology_draft_agent`。
- 输出 `latest_live_methodology_draft_pilot.json/md`。
- 保留 `do_not_overwrite_original=true`。
- visual placeholders 只作为占位，不生成图片。

## 安全边界

- 不覆盖 methodology draft。
- 不自动发布。
- 默认 dry-run。
