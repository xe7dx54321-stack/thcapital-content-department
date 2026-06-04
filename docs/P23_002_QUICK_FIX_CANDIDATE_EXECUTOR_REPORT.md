# P23-002 Quick Fix Candidate Executor Report

## 目标

针对 quick fix candidates 生成安全的 sidecar 修复结果，将可行动事项从“记录问题”推进到“可执行提示”。

## 实现

- 新增 `src/content_system/quick_fix_candidate_executor.py`。
- 新增 `scripts/execute_quick_fix_candidates.py`。
- 支持 operator action、queue status note、visual asset reminder、readiness explanation、monitoring note。

## 边界

- `auto_apply_to_config=false`。
- `overwrites_mainline=false`。
- 不能人工处理的事项标记 `NEEDS_MANUAL`。
