# P9-004 Workbench Context Builder v1 Report

## 本轮目标

为 Chief Editor Agent 构建当天上下文包，使其了解当前文章、可选选题、证据、Agent 审核、source guidance 和系统能力。

## 新增文件

- `src/content_system/workbench_context.py`
- `scripts/build_workbench_context.py`

## 新增命令

```bash
make workbench-context
```

## 输出产物

- `同行资本市场内容系统/10_logs/*workbench-context*.json`
- `同行资本市场内容系统/10_logs/*workbench-context*.md`

## 边界

上下文只用于 plan 和 routing，不自动改稿。
