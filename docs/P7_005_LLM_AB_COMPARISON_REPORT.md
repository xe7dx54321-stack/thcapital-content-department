# P7-005 LLM Agent A/B Comparison Report

## 本轮目标

比较规则型 agent、mock/dry-run agent、live pilot agent 的输出差异。

## 新增能力

- rule judge 与 LLM judge decision match rate。
- critic severity difference。
- live attempted / succeeded / fallback count。
- rewrite suggestion count。
- estimated cost 与 human spot-check items。

## 新增命令

```bash
make llm-ab-comparison
```

## 输出产物

- `10_logs/*llm-ab-comparison*.json`
- `10_logs/*llm-ab-comparison*.md`
- `11_frontstage/*llm-ab-comparison-board.md`

## 当前限制

- v1 只比较结构化字段，不做语义评分。
- 冲突只提示 human spot check，不自动改结果。
