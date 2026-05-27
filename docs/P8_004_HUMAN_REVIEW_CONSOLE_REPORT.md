# P8-004 Human Review Console v1 Report

## 本轮目标

提供轻量本地人工审核 console，用 Markdown/JSON 汇总发布候选、人工异常、反馈、dry-run 状态和 Agent 冲突。

## 新增文件

- `src/content_system/human_review_console.py`
- `scripts/run_human_review_console.py`

## 新增命令

```bash
make human-review-console
```

## CLI 能力

```bash
python3 scripts/run_human_review_console.py --summary
python3 scripts/run_human_review_console.py --list-candidates
python3 scripts/run_human_review_console.py --list-exceptions
python3 scripts/run_human_review_console.py --list-feedback
python3 scripts/run_human_review_console.py --json
```

## 边界

Console 只帮助人看和决策，不绕过人工确认，不自动发布。
