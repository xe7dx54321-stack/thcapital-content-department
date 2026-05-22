# 开发任务清单

## 当前阶段

Phase 0：工程化底座与采集稳定性基础设施。

目标：先让项目可检查、可审计、可迁移，再推进采集稳定性、结构化信息层、价值评分、内容生成和学习系统。

## 已完成

### P0-001：项目状态与健康检查底座

状态：Done。

目标：

- 建立项目状态文档。
- 建立健康检查脚本。
- 建立 `make doctor` 入口。

验收：

- `scripts/doctor.py` 已入库。
- `src/content_system/paths.py` 已入库。
- `Makefile` 已包含 `doctor` 目标。
- `make doctor` 可用于检查关键路径和写入能力。

### P0-002：路径硬编码审计工具

状态：Done。

目标：

- 新增路径硬编码审计脚本。
- 新增 `make path-audit`。
- 输出 Markdown 和 JSON 审计报告。

验收：

- `scripts/audit_hardcoded_paths.py` 已入库。
- `make path-audit` 可运行。
- 能识别 `/Users/...`、`/Volumes/...`、`D:/...`、`file://...` 等路径。

### P0-002b：清理 path audit 生成产物入库问题

状态：Done。

目标：

- 移除已提交的 path audit generated artifacts。
- 更新 `.gitignore`，避免后续审计报告再次进入 Git。
- 保留 P0-002 的代码能力和开发报告。

验收：

- `scripts/audit_hardcoded_paths.py` 仍在。
- `make path-audit` 仍在。
- `同行资本市场内容系统/10_logs/*path-hardcode-audit*` 不再被 Git 跟踪。
- `.gitignore` 已忽略 path audit 生成报告。

### P0-003：路径配置化第一刀

状态：Done。

目标：

- 建立统一路径配置策略。
- 配置化 doctor 和内容工厂控制台入口。
- 减少运行入口中的 HIGH 风险硬编码路径。

验收：

- `make doctor` 通过。
- `bash 内容工厂控制台/status.sh` 不再依赖本机绝对路径。
- `内容工厂控制台/open.sh` 不再写死 `server.json` 绝对路径。
- `make path-audit` 可运行。

### P0-003b：修复/确认核心路径配置文件格式与验收链路

状态：Done。

目标：

- 确认 P0-003 中 Python、shell、Markdown 文件的物理换行和可运行性。
- 保留 P0-003 的路径配置化能力。
- 补充 `bash -n`、`wc -l`、`py_compile` 验收记录。

验收：

- `python3 -m py_compile src/content_system/paths.py` 通过。
- `python3 -m py_compile scripts/doctor.py` 通过。
- `bash -n 内容工厂控制台/start.sh` 通过。
- `bash -n 内容工厂控制台/open.sh` 通过。
- `bash -n 内容工厂控制台/status.sh` 通过。
- `bash -n 内容工厂控制台/restart.sh` 通过。
- 状态文档为正常多行 Markdown。
- `make doctor` 通过。
- `make path-audit` 通过。

### P0-004：HIGH 风险路径配置化第二刀

状态：Done。

目标：

- 基于 path audit HIGH 项，处理仍参与运行的市场/内容生产脚本中的硬编码路径。
- 复用 `src/content_system/paths.py` 的统一路径配置。
- 不处理历史 planning 文档、归档素材、旧日志。
- 不改变抓取业务逻辑和输出格式。

验收：

- `python3 -m py_compile` 对被修改的 Python 文件全部通过。
- `make doctor` 通过。
- `make path-audit` 通过。
- HIGH 风险项从 P0-003/P0-003b 后的 74 降到 56。
- path audit generated reports 不进入 Git。

### P0-005：采集稳定性工程第一步 —— Source Registry v1

状态：Done。

目标：

- 新增 `config/sources.yaml`。
- 新增 source registry 读取与校验模块。
- 新增 `make sources-validate`。
- 不重写现有 fetcher，不改变业务输出格式。

验收：

- `python3 -m py_compile src/content_system/sources.py` 通过。
- `python3 -m py_compile scripts/validate_sources.py` 通过。
- `make sources-validate` 通过。
- `python3 scripts/validate_sources.py --list` 可输出 source 简表。
- `make doctor` 通过。
- `make path-audit` 通过且不引入新的 HIGH 路径。

### P0-006：Source Health v1

状态：Done。

目标：

- 基于 `config/sources.yaml` 建立静态 source health / coverage 报告。
- 新增 `make source-health`。
- 不改现有 fetcher。
- 不新增数据库。
- 为后续 runtime health、retry、fallback 做准备。

验收：

- `python3 -m py_compile src/content_system/source_health.py` 通过。
- `python3 -m py_compile scripts/build_source_health.py` 通过。
- `make source-health` 可运行。
- 生成 source health JSON、Markdown 和 frontstage board。
- source health generated reports 已被 `.gitignore` 忽略。

### P0-007：Source Health Runtime Adapter v1

状态：Done。

目标：

- 将 `config/sources.yaml` 与现有运行产物、manifest、source packets 对齐。
- 生成 runtime source health 报告。
- 识别哪些 source 已被观测到、哪些 expected source 缺少运行证据、哪些 artifact 未匹配到 registry source。
- 不重写 fetcher，不做 retry/fallback，不新增数据库。

验收：

- `python3 -m py_compile src/content_system/source_runtime_health.py` 通过。
- `python3 -m py_compile scripts/build_source_runtime_health.py` 通过。
- `make source-runtime-health` 可运行。
- 生成 source runtime health JSON、Markdown 和 frontstage board。
- source runtime health generated reports 已被 `.gitignore` 忽略。
- 没有再次把 `information_旧素材库` 或其他大体量本地目录卷入 Git。

### P0-007b：补齐 Source Runtime Health 状态文档

状态：Done。

目标：

- 补齐 P0-007 在 `docs/PROJECT_STATE.md` 和 `docs/DEVELOPMENT_TASKS.md` 中的状态记录。
- 将 `source_runtime_health` 加入 `src/content_system/__init__.py` 的模块导出列表。
- 不修改 P0-007 核心功能逻辑。

验收：

- `docs/PROJECT_STATE.md` 已记录 P0-007 和 P0-007b。
- `docs/DEVELOPMENT_TASKS.md` 已记录 P0-007 和 P0-007b。
- `src/content_system/__init__.py` 已包含 `source_runtime_health`。
- 本轮变更只包含状态文档和必要导出，不引入 generated artifacts。

## 下一步

### P0-008：Runtime Manifest Contract v1

状态：Next。

目标：

- 定义现有抓取脚本的稳定 manifest schema。
- 让活跃抓取脚本输出结构化 runtime manifest。
- 减少 P0-007 当前对文本匹配、文件名推断和宽松 artifact 扫描的依赖。
- 不重写 fetcher，不做 retry/fallback，不新增数据库。

建议范围：

- 新增 `src/content_system/runtime_manifest.py`。
- 新增 `scripts/validate_runtime_manifest.py`。
- 新增或更新 `docs/P0_008_RUNTIME_MANIFEST_CONTRACT_REPORT.md`。
- 小范围适配 1-2 个活跃抓取脚本的 manifest 输出，优先选择 `market_topic_capture_round.py` 和 `market_official_update_lane.py`。

验收方向：

- manifest schema 可被独立校验。
- 新 manifest 与 source registry 中的 source_id 能稳定对齐。
- `make source-runtime-health` 可以优先读取结构化 manifest。
- 不影响现有 source packet / top20 / frontstage 输出。

## 开发注意事项

1. 每轮开发都必须维护 `docs/PROJECT_STATE.md` 和 `docs/DEVELOPMENT_TASKS.md`。
2. 生成型报告、运行态日志、health 产物、path audit 产物不得进入 Git。
3. 不要 force push，不要改写 Git 历史。
4. 不要把本地 `.env`、本机绝对路径、API key、cookie、token 写入仓库。
5. 未经明确指令，不要大规模重写现有抓取主链路。
