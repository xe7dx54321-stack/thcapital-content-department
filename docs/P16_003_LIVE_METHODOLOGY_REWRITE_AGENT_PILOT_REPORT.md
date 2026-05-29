# P16-003 Live Methodology Rewrite Agent Pilot Report

## 本轮目标

让 live rewrite agent 根据 methodology article review 的低分项生成重写候选。

## 已完成

- 新增 `live_methodology_rewrite_agent`。
- 输出 `latest_live_methodology_rewrite_pilot.json/md`。
- 优先处理核心判断、开头张力、证据对齐、风险平衡等问题。

## 安全边界

- 不覆盖原稿。
- 不替换 existing methodology rewrite versions。
- live output 只作为 candidate sidecar。
