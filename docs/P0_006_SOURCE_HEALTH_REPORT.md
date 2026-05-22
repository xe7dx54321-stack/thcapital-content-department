# P0-006 Source Health v1 开发报告

## 本轮目标

P0-006 的目标是基于 P0-005 建立的 `config/sources.yaml`，生成第一版静态 source health / coverage 报告。

这一步只做 registry coverage 和结构化健康快照，不进行网络抓取、不执行 retry、不改变现有 fetcher、不新增数据库。

## 新增文件

- `src/content_system/source_health.py`
- `scripts/build_source_health.py`
- `docs/P0_006_SOURCE_HEALTH_REPORT.md`

## 修改文件

- `Makefile`
- `.gitignore`
- `src/content_system/__init__.py`
- `docs/PROJECT_STATE.md`
- `docs/DEVELOPMENT_TASKS.md`

## 新增命令

```bash
make source-health
```

等价于：

```bash
python3 scripts/build_source_health.py
```

## 输出产物

默认生成：

```text
同行资本市场内容系统/10_logs/YYYYMMDD__source-health.json
同行资本市场内容系统/10_logs/YYYYMMDD__source-health.md
同行资本市场内容系统/10_logs/latest_source_health.json
同行资本市场内容系统/10_logs/latest_source_health.md
同行资本市场内容系统/11_frontstage/YYYYMMDD__source-health-board.md
同行资本市场内容系统/11_frontstage/latest_source_health_board.md
```

这些产物属于运行生成文件，已加入 `.gitignore`，默认不进入 Git。

## Source Health 字段

每个 source health record 包括：

- `source_id`
- `label`
- `tier`
- `category`
- `language`
- `enabled`
- `fetch_method`
- `primary_url`
- `fallback_methods`
- `expected_frequency`
- `expected_min_items_per_run`
- `health_status`
- `health_reason`
- `registry_warnings`

## 状态定义

- `READY`：source 已启用且 registry 结构完整。
- `WATCH`：source 已启用，但存在需要关注的 registry 层提示，例如 fallback 缺失。
- `DISABLED`：source 在 registry 中禁用。

P0-006 暂不定义 live fetch 成功/失败状态，因为尚未接入现有抓取运行结果。

## 验收命令

```bash
python3 -m py_compile src/content_system/source_health.py
python3 -m py_compile scripts/build_source_health.py
python3 -m py_compile src/content_system/sources.py
python3 -m py_compile scripts/validate_sources.py
make sources-validate
make source-health
make doctor
make path-audit
git ls-files | grep 'source-health' || true
git status --short
```

## 未做事项

- 未接入网络抓取。
- 未执行 retry/fallback。
- 未重写现有 fetcher。
- 未新增数据库。
- 未改变现有 source packet / manifest 输出格式。

## 下一步建议

进入 P0-007：Source Health Runtime Adapter v1。

P0-007 应读取现有运行产物，例如 `02_topic_radar/source_packets` 和 `10_logs/*manifest*`，为每个 source 补充：

- `last_seen_at`
- `last_packet_path`
- `runtime_status`
- `items_seen_recently`

仍然不重写 fetcher、不新增数据库、不改调度。
