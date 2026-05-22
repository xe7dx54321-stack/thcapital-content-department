# 项目状态记录

## 项目定位

`thcapital-content-department` 是同行资本 AI/Agent 领域内容生产 Agent 系统的工程仓库。

系统目标是：每天自动化获取 AI 和 Agent 领域的一手高价值信息，对信息进行结构化、价值判断、选题筛选，并生成微信公众号文章、小红书推文等内容；同时持续学习头部自媒体文章的选题、结构、标题和呈现方式，形成自我迭代能力。

## 当前阶段

Phase 0：工程化底座与采集稳定性基础。

当前阶段目标不是重写业务链路，而是先建立后续开发需要的工程基础、路径配置、状态文档、检查工具、审计工具、source registry 和 source health 报告能力。

## 当前活跃主线

1. 先工程化底座。
2. 再路径配置化。
3. 再采集稳定性。
4. 再结构化信息层和价值评分。
5. 最后推进内容生成质量和自我学习闭环。

## 当前目录判断

- `同行资本市场内容系统/`：当前活跃主线系统。
- `内容生产系统/`：旧版生产系统和历史生产资产，后续仅按需迁移。
- `内容工厂控制台/`：本地展示台和控制台入口。
- `内容素材库/`：素材沉淀与人工整理内容。
- `_archive/`：历史归档，不作为当前改造主线。

## 已完成 checkpoint

- P0-001：项目状态与健康检查底座。
- P0-002：路径硬编码审计工具。
- P0-002b：清理 path audit 生成产物入库问题。
- P0-003：路径配置化第一刀。
- P0-003b：修复/确认核心路径配置文件格式与验收链路。
- P0-004：HIGH 风险路径配置化第二刀。
- P0-005：采集稳定性工程第一步 —— Source Registry v1。
- P0-006：Source Health v1。

## 最新 checkpoint

P0-006：Source Health v1。

## 当前能力状态

### 工程检查

可用命令：

```bash
make doctor
```

用于检查项目路径、关键目录、关键脚本和写入能力。

### 路径硬编码审计

可用命令：

```bash
make path-audit
```

用于扫描仓库内本机绝对路径、file URL 等硬编码风险。生成报告属于运行产物，默认不进入 Git。

### Source Registry

可用命令：

```bash
make sources-validate
python3 scripts/validate_sources.py --list
python3 scripts/validate_sources.py --tier A
python3 scripts/validate_sources.py --category official
```

P0-005 已建立 `config/sources.yaml`、`src/content_system/sources.py` 和 `scripts/validate_sources.py`。当前 registry v1 包含 17 个 source，覆盖 A/B/C/D/E 五类信源。

### Source Health

可用命令：

```bash
make source-health
```

P0-006 已基于 Source Registry 建立静态 source health / coverage 报告能力。该能力暂不进行网络抓取、不执行 retry、不改变现有 fetcher，只把 registry 转换为每日 health snapshot。

默认生成：

```text
同行资本市场内容系统/10_logs/YYYYMMDD__source-health.json
同行资本市场内容系统/10_logs/YYYYMMDD__source-health.md
同行资本市场内容系统/10_logs/latest_source_health.json
同行资本市场内容系统/10_logs/latest_source_health.md
同行资本市场内容系统/11_frontstage/YYYYMMDD__source-health-board.md
同行资本市场内容系统/11_frontstage/latest_source_health_board.md
```

这些报告属于运行生成产物，默认由 `.gitignore` 忽略。

## 开发原则

1. 每次只做一个小 checkpoint，避免一次性大改。
2. 每个 checkpoint 必须说明目标、变更文件、验收方式和下一步建议。
3. 每轮开发必须维护本文件和 `docs/DEVELOPMENT_TASKS.md`。
4. 不直接重写现有业务主链路，尤其不要破坏 `同行资本市场内容系统/09_runbooks/scripts/` 下已经能跑的生产脚本。
5. 当前优先级是工程化、可维护性、可迁移性和采集稳定性基础，而不是马上新增大量信源或文章生成功能。
6. 生成型日志、审计报告、source health 运行产物默认不进入 Git。

## 下一步建议

下一步进入：

```text
P0-007：Source Health Runtime Adapter v1
```

目标是：基于现有 `config/sources.yaml` 和 P0-006 source health 报告，开始把现有抓取脚本的 source packet / manifest / 运行结果纳入 source health，但仍不重写 fetcher、不新增数据库、不改调度。
