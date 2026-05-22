# P3-005 Revision Instruction Builder v1 Report

## 本轮目标

- 对 NEEDS_REVISION 和 ESCALATE_TO_HUMAN 项生成明确修改指令。
- 将修改方向拆成标题、开头、逻辑、证据、风险和平台适配。

## 新增文件

- `src/content_system/revision_instruction.py`
- `scripts/build_revision_instructions.py`

## 新增命令

```bash
make revision-instructions
```

## 输出产物

- `同行资本市场内容系统/06_review_queue/*revision-instructions*.json`
- `同行资本市场内容系统/06_review_queue/*revision-instructions*.md`

## 验收方式

- `python3 -m py_compile src/content_system/revision_instruction.py`
- `python3 -m py_compile scripts/build_revision_instructions.py`
- `make revision-instructions`

## 注意事项

该模块只生成修改指令，不直接改写文章。
