# 开发任务清单

## 当前阶段

Phase 0：工程化底座与采集稳定性基础。

目标：先让项目可检查、可审计、可迁移，并逐步建立采集稳定性所需的 source registry、source health、runtime adapter、runtime manifest、retry/fallback 基础，再推进结构化信息层、价值评分、内容生成和学习系统。

## 已完成

### P0-001：项目状态与健康检查底座

状态：Done。

验收：`scripts/doctor.py`、`src/content_system/paths.py`、`make doctor` 已入库并可用于检查关键路径和写入能力。

### P0-002：路径硬编码审计工具

状态：Done。

验收：`scripts/audit_hardcoded_paths.py` 与 `make path-audit` 已入库，可输出 Markdown/JSON 审计报告。

### P0-002b：清理 path audit 生成产物入库问题

状态：Done。

验收：`同行资本市场内容系统/10_logs/*path-hardcode-audit*` 不再被 Git 跟踪，`.gitignore` 已忽略 path audit 生成报告。

### P0-003：路径配置化第一刀

状态：Done。

验收：`src/content_system/paths.py` 提供统一路径解析；控制台脚本支持环境变量与仓库相对路径 fallback；`make doctor` 和 `bash -n 内容工厂控制台/*.sh` 通过。

### P0-003b：修复/确认核心路径配置文件格式与验收链路

状态：Done。

验收：后续格式和可运行性主要以 `wc -l`、`py_compile`、`bash -n`、`make doctor`、`make path-audit` 和用户本地/commit 对象验证为准。

### P0-004：HIGH 风险路径配置化第二刀

状态：Done。

验收：运行脚本中的 HIGH 风险路径进一步下降，path audit HIGH 从 P0-003/P0-003b 后约 74 降到 56。

### P0-005：采集稳定性工程第一步 —— Source Registry v1

状态：Done。

目标：新增 `config/sources.yaml`、source registry 读取与校验模块、`make sources-validate`。

验收：17 个 source 全部校验通过，ERROR 0 / WARN 0。

### P0-006：Source Health v1

状态：Done。

目标：基于 `config/sources.yaml` 建立静态 source health / coverage 报告。

验收：`make source-health` 可生成 JSON/Markdown 报告和 frontstage board，生成产物不进入 Git。

### P0-007：Source Health Runtime Adapter v1

状态：Done。

目标：基于现有运行产物、source packet 和 manifest，建立 registry ↔ runtime artifact 的对齐层。

验收：`make source-runtime-health` 已入库，可生成运行态 source health 报告，不重写 fetcher、不新增数据库、不改调度。

### P0-007b：补齐 Source Runtime Health 状态文档

状态：Done。

目标：补齐 P0-007 的 `PROJECT_STATE` / `DEVELOPMENT_TASKS` 状态记录和模块导出。

### P0-008：Runtime Manifest Contract v1

状态：Done。

目标：定义 runtime manifest JSON 合约、示例文件、校验模块和 `make manifest-validate`。

验收：`config/runtime_manifest_example.json` 可通过 `scripts/validate_runtime_manifest.py` 校验；`runtime_manifest.py` 提供解析、校验和摘要能力。

### P0-009：Runtime Manifest Writer v1

状态：Done。

目标：

- 新增 `src/content_system/runtime_manifest_writer.py`。
- 新增 `scripts/write_runtime_manifest_from_packets.py`。
- 新增 `make manifest-write-from-packets`。
- 从现有 source packet JSON 产物生成 P0-008 runtime manifest。
- 不执行 fetcher、不改变既有输出格式、不新增数据库。

验收：

- `python3 -m py_compile src/content_system/runtime_manifest_writer.py` 通过。
- `python3 -m py_compile scripts/write_runtime_manifest_from_packets.py` 通过。
- `make manifest-validate` 通过。
- `make manifest-write-from-packets` 可运行；如无 source packet，则应安全退出。
- 生成的 runtime manifest 不进入 Git。

## 下一步

### P0-010：Runtime Manifest Pilot Integration v1

状态：Todo。

目标：

- 选择一个风险最低的活跃抓取脚本，优先考虑 `market_official_update_lane.py`。
- 在不改变原有 packet/top20/manifest 输出格式的前提下，额外生成 P0-008 合约 runtime manifest。
- 不重写 fetcher、不改评分逻辑、不改旧 Markdown manifest。
- 运行结束后可以通过 `make manifest-validate` 或 `scripts/validate_runtime_manifest.py` 校验新 manifest。

建议验收：

- 被改脚本 `py_compile` 通过。
- 原有输出文件仍保持。
- 新增 runtime manifest JSON 输出到 `同行资本市场内容系统/10_logs/`。
- 新输出被 `.gitignore` 忽略。
- `make source-runtime-health` 后续可逐步读取更稳定的 manifest 证据。
