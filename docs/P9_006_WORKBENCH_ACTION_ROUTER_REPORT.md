# P9-006 Workbench Action Router v1 Report

## 本轮目标

把 Chief Editor Agent 的 action plan 写入 pending action queue，供后续人工确认和 Phase 10 执行器使用。

## 新增文件

- `src/content_system/workbench_action_router.py`
- `scripts/route_workbench_actions.py`

## 新增命令

```bash
make workbench-action-router
```

## 硬规则

所有 action 都写入 `do_not_auto_execute = true`，本轮只排队，不执行。
