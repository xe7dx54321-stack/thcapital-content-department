# P0-005 Source Registry v1 开发报告

## 本轮目标

- 新增统一信源注册表 `config/sources.yaml`。
- 新增 source registry 读取与校验模块。
- 新增命令行校验入口和 Makefile 命令。
- 不重写现有 fetcher，不改变抓取脚本输出格式。
- 为后续 P0-006 Source Health v1 做准备。

## 新增文件

- `config/sources.yaml`
- `src/content_system/sources.py`
- `scripts/validate_sources.py`
- `docs/P0_005_SOURCE_REGISTRY_REPORT.md`

## 修改文件

- `Makefile`
- `src/content_system/__init__.py`
- `docs/PROJECT_STATE.md`
- `docs/DEVELOPMENT_TASKS.md`

## Source Registry 字段说明

每个 source 必须包含：

- `source_id`：小写字母、数字、下划线组成的唯一 ID。
- `label`：面向人的信源名称。
- `tier`：A/B/C/D/E 分层。
- `category`：信源类别，如 official、research、chinese_media。
- `language`：en/zh/multi。
- `enabled`：是否启用。
- `fetch_method`：当前建议采集方式。
- `primary_url`：主入口 URL。
- `fallback_methods`：后续可用于 fallback 的方法列表。
- `expected_frequency`：预期更新频率。
- `expected_min_items_per_run`：每轮最低预期条数。
- `owner`：配置负责人。
- `notes`：维护说明。

## 首批 source 覆盖

按 tier 统计：

- A：6
- B：3
- C：2
- D：4
- E：2

合计 17 个 source，全部 enabled。

覆盖范围：

- A 类官方源：OpenAI、Anthropic、Google DeepMind、Google AI、Meta AI、NVIDIA。
- B 类开发者/开源社区：GitHub Trending、Hacker News、Hugging Face Papers。
- C 类研究：arXiv AI、Papers with Code。
- D 类中文媒体/头部内容学习：机器之心、新智元、量子位、智东西。
- E 类社交/弱信号：Reddit MachineLearning、YouTube AI Channels。

## 新增命令

```bash
make sources-validate
python3 scripts/validate_sources.py --list
python3 scripts/validate_sources.py --tier A
python3 scripts/validate_sources.py --category official
```

## 验收命令

```bash
python3 -m py_compile src/content_system/sources.py
python3 -m py_compile scripts/validate_sources.py
python3 -m py_compile scripts/doctor.py
python3 -m py_compile scripts/audit_hardcoded_paths.py
make sources-validate
python3 scripts/validate_sources.py --list
python3 scripts/validate_sources.py --tier A
python3 scripts/validate_sources.py --category official
make doctor
make path-audit
git ls-files | grep 'path-hardcode-audit' || true
git status --short --branch
```

## 未做事项

- 未重写现有 fetcher。
- 未改变现有抓取脚本输出格式。
- 未新增数据库、调度系统、retry queue 或 fallback 运行逻辑。
- 未新增 LLM 调用。
- 未处理剩余历史 HIGH 路径。

## 下一步建议

进入 P0-006：Source Health v1。

下一步应基于 `config/sources.yaml` 生成 source health report，先统计 enabled/tier/category、最近运行状态、预期频率和缺失情况，不改变现有 fetcher。
