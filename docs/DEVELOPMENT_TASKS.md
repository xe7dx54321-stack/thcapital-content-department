# 后续开发任务清单

## 任务原则

- 小步提交，每个任务可独立验收。
- 优先修稳定性，再做智能化。
- 先旁路新增，再逐步替换旧脚本。
- 每个任务完成后更新 `docs/PROJECT_STATE.md`。

## Phase 0：工程地基修复

### P0-001 项目状态与健康检查底座

状态：待应用 / 待验收

改动：

- 新增 `.env.example`
- 新增 `Makefile`
- 新增 `scripts/doctor.py`
- 新增 `src/content_system/paths.py`
- 新增 `docs/PROJECT_STATE.md`
- 新增 `docs/DEVELOPMENT_TASKS.md`

验收：

```bash
make doctor
```

完成标准：

- 能打印关键路径与脚本状态。
- 能检查 frontstage 和 logs 写权限。
- 能写出 `latest_doctor_report.json`。

### P0-002 统一路径配置第一轮

状态：未开始

目标：

- 让后续新增代码全部从 `content_system.paths` 获取路径。
- 梳理现有硬编码路径清单。
- 暂不大规模改旧脚本，只输出迁移清单。

验收：

```bash
python3 scripts/doctor.py
```

并生成：

```text
10_logs/path-hardcode-audit.md
```

## Phase 1：采集稳定性工程

### P1-001 信源注册表初版

状态：未开始

目标：

- 新增 `config/sources.yaml`。
- 把官方源、开发者源、论文源、中文媒体源、社交源分层。
- 不要求一次接入所有 fetcher，只先建立配置结构。

### P1-002 Source Health Report

状态：未开始

目标：

- 每天输出每个信源的抓取状态。
- 标记 OK / DEGRADED / FAILED / STALE / NOISY。
- 输出 Markdown + JSON。

### P1-003 Retry Queue

状态：未开始

目标：

- 抓取失败的源进入 retry queue。
- 支持单独重试失败源。

## Phase 2：结构化信息层

### P2-001 SQLite 状态库初版

状态：未开始

核心表：

- sources
- source_runs
- raw_items
- normalized_items

### P2-002 Normalized Item Schema

状态：未开始

目标：

- 统一 title、url、source_id、published_at、summary、event_type、entities、domain_tags、evidence_claims。

### P2-003 Topic Cluster

状态：未开始

目标：

- 把散乱信息聚合成 topic cluster。
- 支持 24h / 72h / 7d 三个窗口。

## Phase 3：价值判断系统

### P3-001 多维规则评分器

状态：未开始

评分维度：

- source_authority
- freshness
- novelty
- strategic_relevance
- market_impact
- technical_substance
- narrative_potential
- evidence_strength

### P3-002 LLM Judge

状态：未开始

目标：

- 对高分 topic 做结构化复核。
- 输出是否值得写、推荐角度、风险、缺失证据。

## Phase 4：内容生产系统升级

### P4-001 Content Brief Builder

状态：未开始

目标：

- 不再直接从信息生成文章。
- 先生成 content brief。

### P4-002 Outline + Draft

状态：未开始

目标：

- brief → outline → draft。

### P4-003 Editor + Fact Check

状态：未开始

目标：

- 生成质量报告。
- 低于阈值不进入发布队列。

## Phase 5：自我迭代与学习闭环

### P5-001 Head Media Pattern Library

状态：未开始

目标：

- 从头部内容中提取标题模式、开头模式、结构模式、证据模式。

### P5-002 人工反馈闭环

状态：未开始

目标：

- 记录每篇内容的人工评分和问题标签。
- 每周生成复盘报告。
