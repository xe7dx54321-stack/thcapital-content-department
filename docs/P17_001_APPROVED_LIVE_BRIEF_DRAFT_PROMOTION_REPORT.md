# P17-001 Approved Live Brief/Draft Promotion Report

## 本轮目标

把人工认可的 Phase 16 live brief / live draft sidecar 提升为候选版本。

## 已完成能力

- 新增 `approved_live_output_promotion`。
- 只接受 `ACCEPT_LIVE` / `MERGE` calibration。
- 输出 promoted live content candidates。
- 不覆盖 methodology brief / draft。

## 边界

- `REJECT_LIVE` / `DEFER` / 无人工校准不 promotion。
- promotion 不是 final candidate，也不发布。
