# P0-009 Runtime Manifest Writer v1 开发报告

## 本轮目标

P0-008 已定义 runtime manifest 合约和校验工具。本轮新增 writer 能力，把现有 source packet JSON 运行产物转换为符合 P0-008 合约的 runtime manifest。

本轮不执行 fetcher、不改变现有抓取脚本输出格式、不新增数据库、不做 retry/fallback。

## 新增文件

- `src/content_system/runtime_manifest_writer.py`
- `scripts/write_runtime_manifest_from_packets.py`
- `docs/P0_009_RUNTIME_MANIFEST_WRITER_REPORT.md`

## 修改文件

- `.gitignore`
- `Makefile`
- `src/content_system/__init__.py`
- `docs/PROJECT_STATE.md`
- `docs/DEVELOPMENT_TASKS.md`

## 新增命令

```bash
make manifest-write-from-packets
python3 scripts/write_runtime_manifest_from_packets.py --json
```

## 输出产物

默认输出：

```text
同行资本市场内容系统/10_logs/YYYYMMDD__runtime-manifest.json
同行资本市场内容系统/10_logs/latest_runtime_manifest.json
```

这些属于运行生成产物，默认由 `.gitignore` 忽略。

## Writer 行为

- 自动发现最新 `同行资本市场内容系统/02_topic_radar/source_packets/*` 目录。
- 读取其中的 JSON packet 文件。
- 提取 `source_id`、`entry_count`、`entries`、`captured_at` 等字段。
- 对已知旧 source id 做 registry alias 映射。
- 写出 P0-008 runtime manifest JSON。
- 写出后可使用 `validate_runtime_manifest` 对照 registry 校验。

## 验收命令

```bash
python3 -m py_compile src/content_system/runtime_manifest_writer.py
python3 -m py_compile scripts/write_runtime_manifest_from_packets.py
make manifest-validate
make manifest-write-from-packets
make sources-validate
make source-health
make source-runtime-health
make doctor
make path-audit
git status --short --branch
```

## 未做事项

- 未修改 `market_topic_capture_round.py`。
- 未修改 `market_official_update_lane.py`。
- 未让任何 fetcher 自动写 runtime manifest。
- 未新增数据库。
- 未做 retry/fallback。

## 下一步建议

P0-010：Runtime Manifest Pilot Integration v1。

建议优先选择 `market_official_update_lane.py`，在保持旧输出不变的前提下，额外写出 runtime manifest JSON。
