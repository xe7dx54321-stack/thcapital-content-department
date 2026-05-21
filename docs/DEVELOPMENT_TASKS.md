# 后续开发任务清单

> 本文件用于记录项目后续开发任务。每轮小步施工完成后都要更新。

## Phase 0：工程地基修复

### P0-001：项目状态与健康检查底座

状态：进行中

目标：

- 新增项目状态文档。
- 新增任务清单。
- 新增健康检查脚本。
- 新增统一路径解析工具。

验收：

```bash
make doctor
```

预期输出：

- 控制台打印健康检查结果。
- 生成 `同行资本市场内容系统/10_logs/latest_doctor_report.json`。

### P0-002：路径硬编码审计

状态：待开发

目标：

- 扫描仓库中所有 `/Users/apple/Documents/...` 等本机硬编码路径。
- 输出 Markdown 审计报告。
- 为后续配置化改造建立问题地图。

预期输出：

- `同行资本市场内容系统/10_logs/path-hardcode-audit.md`

### P0-003：项目配置文件初版

状态：待开发

目标：

- 新增 `config/project.yaml`。
- 把活跃系统根目录、日志目录、前台目录等纳入配置。
- 新增配置加载器。

## Phase 1：采集稳定性工程

### P1-001：信源注册表初版

状态：待开发

目标：

- 新增 `config/sources.yaml`。
- 将官方源、开发者源、论文源、中文媒体源、弱信号源分层管理。

### P1-002：Source Health Report

状态：待开发

目标：

- 每日输出每个源的成功/失败/抓取数量/异常原因。
- 生成 JSON 和 Markdown 两类报告。

### P1-003：采集失败重试队列

状态：待开发

目标：

- 对失败源生成 retry queue。
- 支持手动或定时重试。

## Phase 2：结构化信息层

### P2-001：SQLite schema 初版

状态：待开发

目标：

- 建立 `sources`、`source_runs`、`raw_items`、`normalized_items` 等基础表。

### P2-002：Normalized Item Schema

状态：待开发

目标：

- 将原始抓取结果转化为统一信息对象。

### P2-003：Topic Cluster 初版

状态：待开发

目标：

- 将相似信息聚合成 topic cluster，支持后续评分和内容生产。

## Phase 3：价值判断系统

### P3-001：多维评分规则

状态：待开发

目标：

- 建立 source authority、freshness、novelty、strategic relevance、market impact 等评分维度。

### P3-002：高价值选题池

状态：待开发

目标：

- 每天输出 3-8 个高价值 topic。

## Phase 4：内容生产系统升级

### P4-001：Content Brief Builder

状态：待开发

目标：

- 每个选题先生成 brief，不直接写文章。

### P4-002：Outline → Draft 两阶段生成

状态：待开发

目标：

- 先产出大纲，再产出平台草稿。

### P4-003：质量检查器

状态：待开发

目标：

- 检查事实、证据、结构、原创判断、平台适配度。

## Phase 5：自我迭代与头部内容学习

### P5-001：Head Media Pattern Library

状态：待开发

目标：

- 从头部内容中提取标题模式、开头模式、结构模式、叙事模式。

### P5-002：人工反馈闭环

状态：待开发

目标：

- 记录人工评价和发布表现，反哺选题评分和写作策略。
