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

## 下一步建议

### P0-004：HIGH 风险路径配置化第二刀

目标：

- 基于 path audit 结果，处理 `同行资本市场内容系统/09_runbooks/scripts/` 中仍参与运行的主路径常量。
- 不处理历史 planning 文档、归档素材、旧日志。
- 为后续采集稳定性工程打基础。

范围建议：

- `同行资本市场内容系统/09_runbooks/scripts/` 中仍参与运行的主路径常量。
- 当前仍被生产或控制台间接调用的脚本。
- 必要时补充统一配置读取策略，但不要重写抓取主链路。

验收标准：

- 核心运行路径优先从环境变量或统一配置读取。
- 未设置环境变量时，使用仓库内相对路径作为 fallback。
- `make doctor` 通过。
- `make path-audit` 的 HIGH 项数量继续下降。

## 暂不开始

### P1-001：source registry 初版

目标：把主要信源从脚本内常量抽到 `config/sources.yaml`。

等待 Phase 0 路径和审计稳定后再做。
