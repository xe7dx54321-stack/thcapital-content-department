# P3-006 Human Exception Queue v1 Report

## 本轮目标

- 只把真正需要用户判断的内容放入人工例外队列。
- 不把所有 NEEDS_REVISION 项都交给人工。
- 输出 urgency、estimated review minutes、recommended human action 和关键问题。

## 新增文件

- `src/content_system/human_exception_queue.py`
- `scripts/build_human_exception_queue.py`

## 新增命令

```bash
make human-exception-queue
```

## 输出产物

- `同行资本市场内容系统/06_review_queue/*human-exception-queue*.json`
- `同行资本市场内容系统/06_review_queue/*human-exception-queue*.md`

## 验收方式

- `python3 -m py_compile src/content_system/human_exception_queue.py`
- `python3 -m py_compile scripts/build_human_exception_queue.py`
- `make human-exception-queue`

## 注意事项

队列为空是允许状态，表示当天没有需要人工介入的例外项。
