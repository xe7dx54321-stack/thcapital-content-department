# 后续开发任务清单

> 本文件用于维护小步施工计划。每完成一步，都更新状态，避免丢失上下文。

## Phase 0：工程地基修复

### P0-001：项目状态与健康检查底座

状态：进行中

目标：

- 新增项目状态文档。
- 新增任务清单。
- 新增基础路径解析工具。
- 新增 `make doctor` 健康检查入口。

交付文件：

- `docs/PROJECT_STATE.md`
- `docs/DEVELOPMENT_TASKS.md`
- `env.example`
- `Makefile`
- `scripts/doctor.py`
- `src/content_system/__init__.py`
- `src/content_system/paths.py`

验收：

```bash
make doctor
```

### P0-002：路径硬编码审计工具

状态：未开始

目标：

- 扫描仓库中所有本机绝对路径。
- 输出路径硬编码审计报告。
- 不改核心业务脚本，只先建立问题地图。

计划交付：

- `scripts/audit_hardcoded_paths.py`
- `同行资本市场内容系统/10_logs/path-hardcode-audit.md`
- `同行资本市场内容系统/10_logs/path-hardcode-audit.json`

## Phase 1：采集稳定性

### P1-001：信源注册表初版

状态：未开始

目标：

- 新增 `config/sources.yaml`。
- 将官方源、开发者源、论文源、中文媒体源、社交信号源分层管理。

### P1-002：Source Health Report

状态：未开始

目标：

- 每日输出每个 source 的成功/失败、抓取数量、异常原因、fallback 使用情况。
- 生成 Markdown 和 JSON 两种报告。

## Phase 2：结构化信息层

### P2-001：SQLite Schema 初版

状态：未开始

目标：

- 新增轻量状态库。
- 记录 sources、source_runs、raw_items、normalized_items、topic_clusters。

## Phase 3：价值判断系统

### P3-001：多维评分器初版

状态：未开始

目标：

- 从 source authority、freshness、novelty、strategic relevance、market impact、technical substance、narrative potential、evidence strength 多维评分。

## Phase 4：内容生产链路升级

### P4-001：Content Brief Builder

状态：未开始

目标：

- 高价值 topic 先生成 brief，再进入 outline 和 draft。
