# P13-002 Interactive Final Review Actions Report

## 本轮目标

为 final article candidate 增加本地人工状态记录，让用户可以标记 ready、needs edit、hold。

## 修改文件

- `src/content_system/final_review_actions.py`
- `scripts/update_final_review_status.py`
- `Makefile`

## 已完成能力

- 支持 `python3 scripts/update_final_review_status.py --list`。
- 支持 `--mark-ready`、`--mark-needs-edit`、`--mark-hold`。
- 新增 `make final-review-actions` 只读入口。
- 所有记录都包含 `do_not_publish=true`。

## 安全边界

- copy 类操作只在前端完成，不写发布状态。
- mark 类操作只记录本地状态，不触发发布。

## 当前限制

本阶段不把 final review 状态自动提升为发布状态。
