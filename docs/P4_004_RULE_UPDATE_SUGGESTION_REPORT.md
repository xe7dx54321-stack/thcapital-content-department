# P4-004 Rule Update Suggestion v1 Report

## 目标

- 基于 review outcome memory 和 human feedback 生成规则调整建议。
- 不自动修改任何规则文件。

## 新增文件

- `src/content_system/rule_update_suggestion.py`
- `scripts/build_rule_update_suggestions.py`

## 新增命令

```bash
make rule-update-suggestions
```

## 验收

- 无人工反馈时也能生成 monitor 建议。
- `auto_apply` 始终为 `false`。
