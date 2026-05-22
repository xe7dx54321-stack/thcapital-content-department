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

## 下一步建议

### P0-003：路径配置化第一刀

目标：

- 基于 P0-002 的审计结果，优先处理 HIGH 风险路径。
- 不一次性修改所有历史文档。
- 先改运行脚本和控制台入口中的硬编码路径。
- 引入统一配置读取策略。

范围建议：

- `内容工厂控制台/start.sh`
- `内容工厂控制台/open.sh`
- `内容工厂控制台/status.sh`
- `同行资本市场内容系统/09_runbooks/scripts/*.py` 中仍参与运行的主路径常量。

验收标准：

- 核心运行路径优先从环境变量或统一配置读取。
- 未设置环境变量时，使用仓库内相对路径作为 fallback。
- `make doctor` 通过。
- `make path-audit` 的 HIGH 项数量下降。

## 暂不开始

### P1-001：source registry 初版

目标：把主要信源从脚本内常量抽到 `config/sources.yaml`。

等待 Phase 0 路径和审计稳定后再做。
