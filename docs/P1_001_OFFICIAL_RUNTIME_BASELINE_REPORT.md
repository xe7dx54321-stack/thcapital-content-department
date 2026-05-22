# P1-001 Official Lane Runtime Baseline v1 报告

## 本轮目标

- 将 official daily full run 的关键指标沉淀为日常 baseline。
- 同一 run_date 重复运行时更新同一条记录。
- 为后续 7 天/30 天稳定性观察提供数据基础。

## 新增文件

- `src/content_system/runtime_baseline.py`
- `scripts/update_official_runtime_baseline.py`

## 新增命令

```bash
make runtime-baseline
```

## 输出产物

- `同行资本市场内容系统/10_logs/official_runtime_baseline.json`
- `同行资本市场内容系统/10_logs/official_runtime_baseline.md`
- `同行资本市场内容系统/11_frontstage/official_runtime_baseline_board.md`

以上均为 generated artifacts，默认不进入 Git。

## 验收方式

- `python3 -m py_compile src/content_system/runtime_baseline.py`
- `python3 -m py_compile scripts/update_official_runtime_baseline.py`
- `make runtime-baseline`

## 未做事项

- 不做 retry/fallback。
- 不新增数据库。
- 不修改 official lane fetcher。
