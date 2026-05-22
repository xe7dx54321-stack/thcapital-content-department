# 开发任务记录

## 当前阶段

Phase 0：工程化底座与采集稳定性基础设施。

## 已完成

### P0-001：项目状态与健康检查底座

状态：Done。

目标：建立项目状态文档、健康检查脚本和 `make doctor` 入口。

验收：`scripts/doctor.py` 入库，`make doctor` 可运行。

### P0-002：路径硬编码审计工具

状态：Done。

目标：新增路径硬编码审计脚本和 `make path-audit`。

验收：能识别 `/Users/...`、`/Volumes/...`、`D:/...`、`file://...` 等路径，并输出 Markdown/JSON 报告。

### P0-002b：清理 path audit 生成产物入库问题

状态：Done。

目标：移除已提交的 path audit generated artifacts，并更新 `.gitignore`。

验收：path audit generated artifacts 不再被 Git 跟踪，`make path-audit` 生成产物不进入 Git。

### P0-003：路径配置化第一刀

状态：Done。

目标：建立统一路径配置策略，配置化 doctor 和内容工厂控制台入口。

验收：`make doctor` 通过，控制台入口不再依赖本机绝对路径。

### P0-003b：修复/确认核心路径配置文件格式与验收链路

状态：Done。

目标：确认 P0-003 的 Python、shell、Markdown 文件在本地和 Git commit 对象中正常，并将后续验收重点转向 `wc -l`、`py_compile`、`bash -n`、`make doctor`、`make path-audit`。

验收：`py_compile`、`bash -n`、`make doctor`、`make path-audit` 均通过。

### P0-004：HIGH 风险路径配置化第二刀

状态：Done。

目标：基于 path audit HIGH 项，处理仍参与运行的市场/内容生产脚本中的硬编码路径。

验收：被修改的 Python 文件 `py_compile` 通过，`make doctor` 和 `make path-audit` 通过，HIGH 数量下降到 56 左右。

### P0-005：采集稳定性工程第一步 —— Source Registry v1

状态：Done。

目标：新增 `config/sources.yaml`、source registry 读取与校验模块、`make sources-validate`。

验收：17 个 sources，ERROR/WARN 为 0，`make sources-validate` 通过。

### P0-006：Source Health v1

状态：Done。

目标：基于 `config/sources.yaml` 建立静态 source health/coverage 报告。

验收：`make source-health` 可生成本地报告，generated reports 被 `.gitignore` 忽略。

### P0-007：Source Health Runtime Adapter v1

状态：Done。

目标：把现有运行产物、manifest、source packets 与 Source Registry 对齐，形成 runtime health 报告。

验收：`make source-runtime-health` 可生成本地报告，generated reports 被 `.gitignore` 忽略。

### P0-007b：补齐 Source Runtime Health 状态文档

状态：Done。

目标：补齐 P0-007 状态文档和模块导出。

验收：`docs/PROJECT_STATE.md`、`docs/DEVELOPMENT_TASKS.md` 记录 P0-007/P0-007b。

### P0-008：Runtime Manifest Contract v1

状态：Done。

目标：

- 定义 runtime manifest JSON 合约。
- 新增 runtime manifest 读取、校验和摘要模块。
- 新增 example manifest。
- 新增 `make manifest-validate`。
- 不切换现有 fetcher，不改变现有业务输出格式。

验收：

- `python3 -m py_compile src/content_system/runtime_manifest.py` 通过。
- `python3 -m py_compile scripts/validate_runtime_manifest.py` 通过。
- `make manifest-validate` 通过。
- `python3 scripts/validate_runtime_manifest.py --json` 可输出 JSON 摘要。
- `make sources-validate` 通过。
- `make doctor` 通过。

## 下一步

### P0-009：Runtime Manifest Writer v1

状态：Next。

目标：

- 在不改变现有业务输出格式的前提下，提供轻量 manifest writer。
- 优先给一个活跃抓取脚本接入 manifest writer 作为样板。
- 生成符合 P0-008 合约的 runtime manifest JSON。
- 不做全量 fetcher 重写。
- 不新增数据库。
- 不做 retry/fallback。

建议优先样板脚本：`同行资本市场内容系统/09_runbooks/scripts/market_topic_capture_round.py`。
