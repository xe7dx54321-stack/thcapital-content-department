# P12-004 Final Candidate Memory Report

## 本轮目标

记录 final article candidate 的来源版本、质量状态、checklist 状态和 lessons，形成最终候选稿历史。

## 修改文件

- `src/content_system/final_candidate_memory.py`
- `scripts/update_final_candidate_memory.py`
- `Makefile`

## Memory 内容

- final candidate id。
- 来源 version / article / action。
- quality status 和 checklist status。
- human score 与 version score delta。
- lessons 与当前状态。
- `do_not_publish=true`。

## 输出

- `同行资本市场内容系统/07_publishing/final_candidate_memory.json`
- `同行资本市场内容系统/07_publishing/final_candidate_memory.md`
- `同行资本市场内容系统/11_frontstage/final_candidate_memory_board.md`

## 当前限制

memory 是本地文件型记忆，不代表正式发布记录。
