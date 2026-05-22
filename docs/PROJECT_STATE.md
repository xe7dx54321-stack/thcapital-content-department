# 项目状态记录

## 项目定位

`thcapital-content-department` 是同行资本 AI/Agent 领域内容生产 Agent 系统的工程仓库。

系统目标是每天自动化获取 AI 和 Agent 领域的一手高价值信息，对信息进行结构化、价值判断、选题筛选，并生成微信公众号文章、小红书推文等内容；同时持续学习头部自媒体文章的选题、结构、标题和呈现方式，形成自我迭代能力。

## 当前阶段

Phase 0：工程化底座与采集稳定性基础设施。

当前阶段目标不是重写业务主链路，而是先建立后续开发需要的工程基础、路径配置、信源注册、健康报告和运行态观测能力。

## 当前活跃主线

1. 先工程化底座。
2. 再路径配置化。
3. 再采集稳定性。
4. 再结构化信息层和价值评分。
5. 再内容生成与反馈学习闭环。

## 当前目录判断

- `同行资本市场内容系统/`：当前活跃主线系统。
- `内容生产系统/`：旧版生产系统和历史生产资产，后续仅按需迁移。
- `内容工厂控制台/`：本地展示台和控制台入口。
- `内容素材库/`：素材沉淀与人工整理内容。
- `_archive/`：历史归档，不作为当前改造主线。

## 已完成 checkpoint

### P0-001：项目状态与健康检查底座

状态：Done。

交付：

- 新增 `scripts/doctor.py`。
- 新增 `src/content_system/paths.py`。
- 新增 `make doctor`。
- 建立 `docs/PROJECT_STATE.md` 和 `docs/DEVELOPMENT_TASKS.md` 作为项目长期状态记忆。

### P0-002：路径硬编码审计工具

状态：Done。

交付：

- 新增 `scripts/audit_hardcoded_paths.py`。
- 新增 `make path-audit`。
- 生成路径硬编码审计报告能力。

### P0-002b：清理 path audit 生成产物入库问题

状态：Done。

交付：

- 从当前文件树取消跟踪 path audit generated artifacts。
- 在 `.gitignore` 中忽略 path audit 生成报告。
- 保留 P0-002 代码能力和开发报告。

### P0-003：路径配置化第一刀

状态：Done。

交付：

- 建立统一路径配置策略。
- 配置化 `scripts/doctor.py`。
- 配置化内容工厂控制台入口脚本。
- 新增 `env.example` 和 `config/ENV_EXAMPLE.txt`。

### P0-003b：修复/确认核心路径配置文件格式与验收链路

状态：Done。

交付：

- 确认 P0-003 关键 Python、shell、Markdown 文件在本地和 Git commit 对象中为正常多行。
- 补充 `wc -l`、`py_compile`、`bash -n` 等验收记录。
- 后续不再把 GitHub raw 抓取显示的单行/多行作为主要验收依据。

### P0-004：HIGH 风险路径配置化第二刀

状态：Done。

交付：

- 配置化活跃市场脚本中的运行路径。
- 配置化控制台会加载的旧版模块路径。
- `make path-audit` HIGH 从 P0-003/P0-003b 后的 74 降到 56。
- 剩余 HIGH 主要位于未纳入当前运行链路的旧版脚本和少量历史素材抓取脚本。

### P0-005：采集稳定性工程第一步 —— Source Registry v1

状态：Done。

交付：

- 新增 `config/sources.yaml`。
- 新增 `src/content_system/sources.py`。
- 新增 `scripts/validate_sources.py`。
- 新增 `make sources-validate`。
- 首批 source 总数 17，enabled 17；校验 ERROR 0、WARN 0。

### P0-006：Source Health v1

状态：Done。

交付：

- 新增 `src/content_system/source_health.py`。
- 新增 `scripts/build_source_health.py`。
- 新增 `make source-health`。
- 基于 Source Registry 生成静态 source health / coverage 报告。
- 生成产物已加入 `.gitignore`，不进入 Git。

### P0-007：Source Health Runtime Adapter v1

状态：Done。

交付：

- 新增 `src/content_system/source_runtime_health.py`。
- 新增 `scripts/build_source_runtime_health.py`。
- 新增 `make source-runtime-health`。
- 将 `config/sources.yaml` 与现有运行产物、manifest、source packets 做对齐。
- 识别 registry source 的运行观测状态、缺失状态、error hints 和未匹配 artifacts。
- 不重写 fetcher，不做 retry/fallback，不新增数据库。

### P0-007b：补齐 Source Runtime Health 状态文档

状态：Done。

交付：

- 补齐本文件中的 P0-007 状态记录。
- 补齐 `docs/DEVELOPMENT_TASKS.md` 中的 P0-007 状态和下一步任务。
- 更新 `src/content_system/__init__.py`，将 `source_runtime_health` 纳入模块导出列表。

## 最新 checkpoint

P0-007b：补齐 Source Runtime Health 状态文档。

## 当前可用命令

```bash
make doctor
make path-audit
make sources-validate
make source-health
make source-runtime-health
```

## 当前关键环境变量

- `THCAP_MARKET_CONTENT_ROOT`
- `THCAP_LEGACY_CONTENT_ROOT`
- `THCAP_CONTENT_CONSOLE_ROOT`
- `CONTENT_FACTORY_DASHBOARD_HOST`
- `CONTENT_FACTORY_DASHBOARD_PORT`

## 当前系统状态判断

当前系统已经具备：

- 项目健康检查能力。
- 路径硬编码审计能力。
- 核心路径配置化能力。
- Source Registry v1。
- 静态 Source Health v1。
- Runtime Source Health Adapter v1。

当前系统尚未完成：

- 现有抓取脚本的稳定 manifest 合约。
- 真实 runtime manifest 的统一结构化输出。
- retry/fallback 机制。
- 数据库化状态管理。
- 结构化信息层与价值评分层。
- 内容生成质量控制与反馈学习闭环。

## 下一步建议

下一步进入：

```text
P0-008：Runtime Manifest Contract v1
```

目标是让活跃抓取脚本输出稳定结构化 manifest，减少 P0-007 当前对文本匹配和文件名推断的依赖。

## 开发原则

1. 每次只做一个小 checkpoint，避免一次性大改。
2. 每个 checkpoint 必须说明目标、变更文件、验收方式和下一步建议。
3. 每轮开发必须维护本文件和 `docs/DEVELOPMENT_TASKS.md`。
4. 不直接重写现有业务主链路，尤其不要破坏 `同行资本市场内容系统/09_runbooks/scripts/` 下已经能跑的生产脚本。
5. 当前优先级是工程化、可维护性、可迁移性和采集稳定性，而不是马上新增大量信源或文章生成功能。
6. 生成型日志、运行态报告、source health 产物、path audit 产物默认不进入 Git。
7. 文件格式验收优先看本地/commit 对象中的 `wc -l`、`py_compile`、`bash -n` 和 `make` 命令结果，不再把 GitHub raw 抓取显示作为唯一依据。
