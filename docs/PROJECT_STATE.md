# 项目状态记录

## 项目定位

`thcapital-content-department` 是同行资本 AI/Agent 领域内容生产 Agent 系统的工程仓库。系统目标是每天自动化获取 AI 和 Agent 领域的一手高价值信息，对信息进行结构化、价值判断、选题筛选，并生成微信公众号文章、小红书推文等内容；同时持续学习头部自媒体文章的选题、结构、标题和呈现方式，形成自我迭代能力。

## 当前阶段

Phase 0 工程化底座。

当前阶段目标不是重写业务链路，而是先建立后续开发需要的工程基础、状态文档、检查工具和审计工具。

## 已完成

- P0-001 项目状态与健康检查底座。
- P0-002 路径硬编码审计工具。
- P0-002b 清理 path audit 生成产物入库问题。
- P0-003 路径配置化第一刀。
- P0-003b 修复 P0-003 文件物理换行与验收链路。
- P0-004 HIGH 风险路径配置化第二刀。

## 当前活跃主线

- 先工程化底座。
- 再路径配置化。
- 再采集稳定性。
- 再结构化信息层和价值评分。

## 最新 checkpoint

P0-004。

## P0-002 交付状态

本轮新增路径硬编码审计能力：

```bash
make path-audit
```

等价于：

```bash
python3 scripts/audit_hardcoded_paths.py
```

输出产物位置：

```text
同行资本市场内容系统/10_logs/YYYYMMDD__path-hardcode-audit.md
同行资本市场内容系统/10_logs/YYYYMMDD__path-hardcode-audit.json
同行资本市场内容系统/10_logs/latest_path_hardcode_audit.md
同行资本市场内容系统/10_logs/latest_path_hardcode_audit.json
```

审计工具只发现问题，不直接修改历史路径。

## P0-002b 交付状态

P0-002 的审计工具已保留；审计运行产物已从 Git 跟踪中移除，并由 `.gitignore` 忽略。后续运行 `make path-audit` 会在本地生成报告，但完整 JSON/Markdown 审计结果默认不进入 Git。

## P0-003 交付状态

P0-003 已完成第一批路径配置化：`doctor` 和内容工厂控制台入口优先从环境变量读取路径，未配置时使用仓库内相对路径 fallback。

本轮新增和维护的配置入口：

```bash
THCAP_MARKET_CONTENT_ROOT
THCAP_LEGACY_CONTENT_ROOT
THCAP_CONTENT_CONSOLE_ROOT
CONTENT_FACTORY_DASHBOARD_HOST
CONTENT_FACTORY_DASHBOARD_PORT
```

统一路径策略位于：

```text
src/content_system/paths.py
```

本轮只处理工程入口和控制台入口，不批量清理历史文档，不重写市场内容抓取主链路。

## P0-003b 交付状态

P0-003 的路径配置化能力已保留；P0-003b 修复了关键 Python、shell、Markdown 文件的物理换行问题，并补充 `bash -n` / `wc -l` 验收。

本轮检查确认当前本地文件和 Git 对象中的关键文件均为正常多行文本。线上 raw 看到的单行展示更可能来自抓取或显示链路，但后续仍以本地 `wc -l`、`py_compile`、`bash -n` 作为验收依据。

## P0-004 交付状态

P0-004 已基于 path audit HIGH 项继续处理仍参与运行的脚本路径硬编码问题。当前优先清理运行脚本，不处理历史文档、归档素材和旧日志。

本轮重点处理：

- 活跃市场内容系统 `09_runbooks/scripts/` 中的主运行脚本根路径常量。
- 内容工厂控制台会直接或间接加载的旧版内容生产系统看板、学习池和任务单模块。
- 动态本地文件链接生成中的 `file` scheme 字面量，避免被审计误判为固定本机路径。

## 当前目录判断

- `同行资本市场内容系统/`：当前活跃主线系统。
- `内容生产系统/`：旧版生产系统和历史生产资产，后续仅按需迁移。
- `内容工厂控制台/`：本地展示台和控制台入口。
- `内容素材库/`：素材沉淀与人工整理内容。
- `_archive/`：历史归档，不作为当前改造主线。

## 开发原则

1. 每次只做一个小 checkpoint，避免一次性大改。
2. 每个 checkpoint 必须说明目标、变更文件、验收方式和下一步建议。
3. 每轮开发必须维护本文件和 `docs/DEVELOPMENT_TASKS.md`。
4. 不直接重写现有业务主链路，尤其不要破坏 `同行资本市场内容系统/09_runbooks/scripts/` 下已经能跑的生产脚本。
5. 当前优先级是工程化、可维护性、可迁移性，而不是马上新增大量信源或文章生成功能。

## 下一步建议

下一步进入：

```text
P0-005：采集稳定性工程第一步 —— Source Registry v1
```

目标是建立统一 `config/sources.yaml`，为后续 source health、retry、fallback 做准备。不重写现有 fetcher，先建立 registry 和读取能力。
