# P3-004 Judge Agent Gate v1 Report

## 本轮目标

- 汇总 queue item、proponent review、critic review、quality review 和 platform package。
- 给出 APPROVED_FOR_QUEUE、NEEDS_REVISION、HOLD、ESCALATE_TO_HUMAN 四类分流。
- 控制人工带宽，只把高价值/高争议/低置信内容交给人看。

## 新增文件

- `src/content_system/judge_gate.py`
- `scripts/build_judge_gate.py`

## 新增命令

```bash
make judge-gate
```

## 输出产物

- `同行资本市场内容系统/06_review_queue/*judge-gate*.json`
- `同行资本市场内容系统/06_review_queue/*judge-gate*.md`

## 验收方式

- `python3 -m py_compile src/content_system/judge_gate.py`
- `python3 -m py_compile scripts/build_judge_gate.py`
- `make judge-gate`

## 注意事项

裁判门仍是规则型模拟，不做自动发布。
