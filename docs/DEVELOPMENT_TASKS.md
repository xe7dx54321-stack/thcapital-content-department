# 开发任务清单

## 当前阶段

Phase 0：工程化底座与采集稳定性基础。

目标：先让项目可检查、可审计、可迁移，并逐步建立采集稳定性所需的 source registry、source health、后续 runtime adapter、retry/fallback 基础，再推进结构化信息层、价值评分、内容生成和学习系统。

## 已完成

### P0-001：项目状态与健康检查底座

状态：Done。

验收：

- `scripts/doctor.py` 已入库。
- `src/content_system/paths.py` 已入库。
- `Makefile` 已包含 `doctor` 目标。
- `make doctor` 可用于检查关键路径和写入能力。

### P0-002：路径硬编码审计工具

状态：Done。

目标：新增路径硬编码审计能力。

验收：

- `scripts/audit_hardcoded_paths.py` 已入库。
- `Makefile` 已包含 `path-audit` 目标。
- `make path-audit` 可生成 Markdown/JSON 审计报告。

### P0-002b：清理 path audit 生成产物入库问题

状态：Done。

目标：移除已提交的 path audit generated artifacts，并更新 `.gitignore`。

验收：

- `同行资本市场内容系统/10_logs/*path-hardcode-audit*` 不再被 Git 跟踪。
- `.gitignore` 已忽略 path audit 生成报告。
- `make path-audit` 仍可运行。

### P0-003：路径配置化第一刀

状态：Done。

目标：建立统一路径配置策略，配置化 `doctor.py` 和内容工厂控制台入口。

验收：

- `src/content_system/paths.py` 提供统一路径解析。
- 控制台脚本支持环境变量与仓库相对路径 fallback。
- `make doctor` 通过。
- `bash -n 内容工厂控制台/*.sh` 通过。

### P0-003b：修复/确认核心路径配置文件格式与验收链路

状态：Done。

目标：确认 P0-003 关键 Python、shell、Markdown 文件在本地和 Git commit 对象中为正常多行，并将后续验收重点转向 `wc -l`、`py_compile`、`bash -n`、`make doctor`、`make path-audit`。

验收：

- `py_compile` 通过。
- `bash -n` 通过。
- `make doctor` 通过。
- `make path-audit` 通过。

### P0-004：HIGH 风险路径配置化第二刀

状态：Done。

目标：基于 path audit HIGH 项，处理仍参与运行的市场/内容生产脚本中的硬编码路径。

验收：

- 被修改的 Python 文件 `py_compile` 通过。
- `make doctor` 通过。
- `make path-audit` 通过。
- HIGH 风险项从 P0-003/P0-003b 后约 74 降到 56。
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
- 新增 `src/content_system/source_health.py`。
- 新增 `scripts/build_source_health.py`。
- 新增 `make source-health`。
- 生成 JSON/Markdown 报告和 frontstage board。
- 不进行网络抓取、不执行 retry、不改变现有 fetcher。

验收：

- `python3 -m py_compile src/content_system/source_health.py` 通过。
- `python3 -m py_compile scripts/build_source_health.py` 通过。
- `make sources-validate` 通过。
- `make source-health` 通过。
- `make doctor` 通过。
- `make path-audit` 通过。
- 生成的 source health 报告不进入 Git。

## 下一步

### P0-007：Source Health Runtime Adapter v1

状态：Todo。

目标：

- 基于 P0-006 的静态 source health，把现有抓取脚本产出的 source packet / manifest / 运行结果纳入 health 报告。
- 不重写现有 fetcher。
- 不新增数据库。
- 不改调度。
- 先做文件系统层面的 runtime adapter：读取 `02_topic_radar/source_packets`、`10_logs/*manifest*` 等现有产物，识别 source 最近是否有产出。
- 为后续 retry/fallback 和采集稳定性评分做准备。

建议验收：

- 新增 runtime adapter 模块。
- `make source-health` 能同时显示 registry coverage 和已有运行产物 coverage。
- 对每个 source 给出 `last_seen_at` / `last_packet_path` / `runtime_status`，没有历史产物时显示 `NO_RUNTIME_DATA`。
- 不破坏 P0-006 的静态报告能力。
