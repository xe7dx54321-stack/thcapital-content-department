# P17-002 Live Rewrite Version Promotion Report

## 本轮目标

把人工认可的 live rewrite sidecar 提升为候选 rewrite version。

## 已完成能力

- 新增 `live_rewrite_promotion`。
- 读取 live rewrite pilot、live output comparison、calibration feedback。
- 只生成 promoted live rewrite sidecar。

## 边界

- 不替换 existing rewrite versions。
- 不覆盖原稿。
- 不自动发布。
