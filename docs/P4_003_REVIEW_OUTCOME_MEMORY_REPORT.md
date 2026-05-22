# P4-003 Review Outcome Memory v1 Report

## 目标

- 将 publishing candidate、human feedback、judge/proponent/critic 结果汇总为文件型长期记忆。
- 同一个 publishing candidate 重复出现时更新记录。

## 新增文件

- `src/content_system/review_outcome_memory.py`
- `scripts/update_review_outcome_memory.py`

## 新增命令

```bash
make review-outcome-memory
```

## 输出

- `同行资本市场内容系统/07_publishing/review_outcome_memory.json`
- `同行资本市场内容系统/07_publishing/review_outcome_memory.md`
- `同行资本市场内容系统/11_frontstage/review_outcome_memory_board.md`

## 验收

- `make review-outcome-memory` 可运行。
- 未填写反馈时记录为 `UNREVIEWED` / `PENDING`。
