# P0-002 开发报告：路径硬编码审计工具

## 本轮目标

新增路径硬编码审计工具，扫描仓库中的本机绝对路径、旧路径和运行态路径，形成结构化 JSON 报告和 Markdown 报告。目标是为 P0-003 路径配置化提供优先级依据，本轮不直接批量替换历史路径。

## 新增文件

```text
scripts/audit_hardcoded_paths.py
src/content_system/__init__.py
src/content_system/paths.py
docs/P0_002_PATH_AUDIT_REPORT.md
```

## 修改文件

```text
Makefile
docs/PROJECT_STATE.md
docs/DEVELOPMENT_TASKS.md
```

## 新增命令

```bash
make path-audit
```

等价于：

```bash
python3 scripts/audit_hardcoded_paths.py
```

可选参数：

```bash
python3 scripts/audit_hardcoded_paths.py --fail-on-high
python3 scripts/audit_hardcoded_paths.py --max-md-items 100
python3 scripts/audit_hardcoded_paths.py --root <path> --output-dir <path>
```

## 输出产物

```text
同行资本市场内容系统/10_logs/YYYYMMDD__path-hardcode-audit.md
同行资本市场内容系统/10_logs/YYYYMMDD__path-hardcode-audit.json
同行资本市场内容系统/10_logs/latest_path_hardcode_audit.md
同行资本市场内容系统/10_logs/latest_path_hardcode_audit.json
```

## 验收方式

在仓库根目录运行：

```bash
python3 -m py_compile scripts/audit_hardcoded_paths.py
python3 scripts/audit_hardcoded_paths.py
make path-audit
test -f 同行资本市场内容系统/10_logs/latest_path_hardcode_audit.md
test -f 同行资本市场内容系统/10_logs/latest_path_hardcode_audit.json
```

如果发现大量 HIGH / MEDIUM / LOW，是正常现象。本轮目标是完整发现和报告，不要求清零。

## 后续建议

进入 P0-003：路径配置化第一刀。优先处理 HIGH 风险路径，尤其是运行脚本、控制台入口、配置文件中的路径；历史文档和归档里的路径暂不批量清理。

## 注意事项

- 不要大规模修改现有业务脚本。
- 不要重写 `market_topic_capture_round.py`。
- 不要移动顶层中文目录。
- 不要把所有 hardcoded path 一次性替换成环境变量。
- 不要引入第三方依赖或数据库。
- 每轮开发都必须维护 `docs/PROJECT_STATE.md` 和 `docs/DEVELOPMENT_TASKS.md`。
