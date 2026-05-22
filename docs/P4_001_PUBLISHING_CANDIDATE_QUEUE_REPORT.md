# P4-001 Publishing Candidate Queue v1 Report

## 目标

- 将 Judge Gate 中 `APPROVED_FOR_QUEUE` 的内容转成发布候选队列。
- 保持人工确认必需，不自动发布。

## 新增文件

- `src/content_system/publishing_candidate_queue.py`
- `scripts/build_publishing_candidate_queue.py`

## 新增命令

```bash
make publishing-candidates
```

## 输出

- `同行资本市场内容系统/07_publishing/*publishing-candidate-queue*.json`
- `同行资本市场内容系统/07_publishing/*publishing-candidate-queue*.md`

## 验收

- `make publishing-candidates` 可运行。
- generated artifacts 已被 `.gitignore` 覆盖。
