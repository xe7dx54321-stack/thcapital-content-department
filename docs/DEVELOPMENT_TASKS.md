# 开发任务清单

## 当前阶段

Phase 0：工程化底座。

目标：先让项目可检查、可审计、可迁移，再推进采集稳定性、结构化信息层、价值评分、内容生成和学习系统。

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

本轮新增/修改：

- `scripts/audit_hardcoded_paths.py`
- `Makefile`
- `docs/PROJECT_STATE.md`
- `docs/DEVELOPMENT_TASKS.md`
- `docs/P0_002_PATH_AUDIT_REPORT.md`
- `src/content_system/__init__.py`
- `src/content_system/paths.py`

验收命令：

```bash
python3 -m py_compile scripts/audit_hardcoded_paths.py
python3 scripts/audit_hardcoded_paths.py
make path-audit
```

预期产物：

```text
同行资本市场内容系统/10_logs/YYYYMMDD__path-hardcode-audit.md
同行资本市场内容系统/10_logs/YYYYMMDD__path-hardcode-audit.json
同行资本市场内容系统/10_logs/latest_path_hardcode_audit.md
同行资本市场内容系统/10_logs/latest_path_hardcode_audit.json
```

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

- 修复状态文档多行 Markdown 格式。
- 建立统一路径配置策略。
- 配置化 doctor 和内容工厂控制台入口。
- 减少运行入口中的 HIGH 风险硬编码路径。

验收：

- `make doctor` 通过。
- `bash 内容工厂控制台/status.sh` 不再依赖本机绝对路径。
- `内容工厂控制台/open.sh` 不再写死 `server.json` 绝对路径。
- `make path-audit` 可运行。
- HIGH 风险项数量较 P0-002 有下降，或至少运行入口相关 HIGH 项减少。

### P0-003b：修复 P0-003 文件物理换行与验收链路

状态：Done。

目标：

- 修复 P0-003 中 Python、shell、Markdown 文件的物理换行问题。
- 保留 P0-003 的路径配置化能力。
- 补充 `bash -n` 和 `wc -l` 验收，避免再次出现 raw 文件物理单行问题。

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
- HIGH 风险项较 P0-003 后继续下降，或剩余 HIGH 已明确属于非当前运行入口。
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

## 下一步建议

### P0-006：Source Health v1

目标：

- 基于 `config/sources.yaml` 建立 source health report。
- 统计每个 source 的 enabled/tier/category、最近运行状态、预期频率、是否缺失。
- 先做静态 health/coverage 报告，不改现有 fetcher。
- 为后续 retry/fallback 做准备。

范围建议：

- 新增只读报告命令，不改变现有抓取脚本输出。
- 读取 registry 和现有日志/产物目录，先做 coverage 视角。
- 不引入数据库、不做 retry queue。

验收标准：

- source health report 可生成。
- registry 中 source 覆盖状态可统计。
- `make doctor` 通过。
- `make path-audit` 通过且不引入新的 HIGH 路径。

## 暂不开始

### P1-001：内容生成链路工程化

目标：在 Phase 0 采集稳定性、路径和状态底座完成后，再推进内容生成链路的配置化和质量评估。

等待 Phase 0 采集稳定性工程稳定后再做。
