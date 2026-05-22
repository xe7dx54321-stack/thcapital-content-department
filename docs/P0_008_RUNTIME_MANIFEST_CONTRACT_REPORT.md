# P0-008 Runtime Manifest Contract v1 开发报告

## 本轮目标

P0-008 的目标是为后续采集运行状态标准化建立 runtime manifest 合约。它不重写现有 fetcher，也不改变现有业务输出格式，只定义统一 JSON 结构和验证工具。

## 新增文件

- `src/content_system/runtime_manifest.py`
- `scripts/validate_runtime_manifest.py`
- `config/runtime_manifest_example.json`
- `docs/P0_008_RUNTIME_MANIFEST_CONTRACT_REPORT.md`

## 修改文件

- `Makefile`
- `src/content_system/__init__.py`
- `docs/PROJECT_STATE.md`
- `docs/DEVELOPMENT_TASKS.md`

## Runtime Manifest v1 字段

顶层字段：

- `schema_version`
- `generated_at`
- `run_id`
- `run_date`
- `pipeline_name`
- `script_name`
- `status`
- `notes`
- `sources`

每个 source run record 字段：

- `source_id`
- `status`
- `items_found`
- `items_written`
- `started_at`
- `finished_at`
- `error_type`
- `error_message`
- `artifact_paths`
- `notes`

## 状态枚举

Manifest status：

- `SUCCESS`
- `PARTIAL`
- `FAILED`
- `UNKNOWN`

Source run status：

- `SUCCESS`
- `PARTIAL`
- `FAILED`
- `SKIPPED`
- `UNKNOWN`

## 新增命令

```bash
make manifest-validate
```

也可以直接执行：

```bash
python3 scripts/validate_runtime_manifest.py
python3 scripts/validate_runtime_manifest.py --json
python3 scripts/validate_runtime_manifest.py config/runtime_manifest_example.json
```

## 验收命令

```bash
python3 -m py_compile src/content_system/runtime_manifest.py
python3 -m py_compile scripts/validate_runtime_manifest.py
make manifest-validate
python3 scripts/validate_runtime_manifest.py --json
make sources-validate
make doctor
make path-audit
```

## 本轮未做事项

- 未接入任何真实 fetcher。
- 未改变现有 source packet、manifest、frontstage 输出格式。
- 未新增数据库。
- 未新增 retry/fallback。
- 未新增调度。

## 下一步建议

P0-009：Runtime Manifest Writer v1。

优先给一个活跃抓取脚本接入 manifest writer，让它在保留原输出的同时，额外输出符合 P0-008 合约的 runtime manifest JSON。建议从 `market_topic_capture_round.py` 作为样板开始，不要全量改造。
