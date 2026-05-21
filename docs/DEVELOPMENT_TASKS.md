# 开发任务清单

## 当前阶段

Phase 0：工程地基修复。

目标：先让项目可检查、可审计、可迁移，然后再推进采集、评分、生成和学习系统。

## 已完成

### P0-001：项目状态与健康检查底座

状态：Done。

验收：

- `scripts/doctor.py` 已入库。
- `src/content_system/paths.py` 已入库。
- `Makefile` 已包含 `doctor` 目标。
- GitHub Desktop commit / push 链路已验证。

### P0-002：路径硬编码审计工具

状态：Ready for local apply。

本轮新增/修改：

- `scripts/audit_hardcoded_paths.py`
- `Makefile`
- `docs/PROJECT_STATE.md`
- `docs/DEVELOPMENT_TASKS.md`
- `docs/P0_002_PATH_AUDIT_REPORT.md`

验收命令：

```bash
make path-audit
```

预期产物：

```text
同行资本市场内容系统/10_logs/YYYYMMDD__path-hardcode-audit.md
同行资本市场内容系统/10_logs/YYYYMMDD__path-hardcode-audit.json
同行资本市场内容系统/10_logs/latest_path_hardcode_audit.md
同行资本市场内容系统/10_logs/latest_path_hardcode_audit.json
```

## 下一步候选

### P0-003：路径配置化第一刀

目标：根据 P0-002 审计报告，优先修复 HIGH 级路径硬编码。

范围建议：

1. `内容工厂控制台/start.sh`
2. `内容工厂控制台/open.sh`
3. `内容工厂控制台/status.sh`
4. `同行资本市场内容系统/09_runbooks/scripts/*.py` 中的主路径常量

验收标准：

- 新增或更新 `env.example`。
- 核心运行路径优先从环境变量读取。
- 未设置环境变量时，使用仓库内相对路径作为 fallback。
- `make doctor` 通过。
- `make path-audit` 的 HIGH 项数量下降。

### P1-001：source registry 初版

目标：把主要信源从脚本内常量抽到 `config/sources.yaml`。

暂不开始，等 Phase 0 路径和审计稳定后再做。
