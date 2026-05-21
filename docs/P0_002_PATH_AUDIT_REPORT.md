# P0-002 交付报告：路径硬编码审计工具

## 本轮目标

建立一个稳定的审计工具，用来扫描仓库中所有本机绝对路径和不可迁移路径。先生成问题地图，不直接大规模修改业务脚本。

## 本轮新增/修改

```text
Makefile
scripts/audit_hardcoded_paths.py
docs/PROJECT_STATE.md
docs/DEVELOPMENT_TASKS.md
docs/P0_002_PATH_AUDIT_REPORT.md
```

## 新增命令

```bash
make path-audit
```

等价于：

```bash
python3 scripts/audit_hardcoded_paths.py --write
```

## 审计范围

默认扫描仓库内常见文本/代码文件，包括：

- Python / shell / command
- Markdown / text
- JSON / YAML / TOML
- HTML / JS / CSS
- Makefile / env example

默认跳过：

- `.git`
- 缓存目录
- 虚拟环境
- `node_modules`
- `runtime`
- `_archive` 等归档目录

如果需要包含归档目录，可运行：

```bash
python3 scripts/audit_hardcoded_paths.py --write --include-archive
```

## 检测类型

- macOS 用户目录：`/Users/...`
- macOS 卷路径：`/Volumes/...`
- Windows 盘符路径：`D:\...`、`D:/...`
- 本地 file URL：`file://...`

## 输出产物

```text
同行资本市场内容系统/10_logs/YYYYMMDD__path-hardcode-audit.md
同行资本市场内容系统/10_logs/YYYYMMDD__path-hardcode-audit.json
同行资本市场内容系统/10_logs/latest_path_hardcode_audit.md
同行资本市场内容系统/10_logs/latest_path_hardcode_audit.json
```

## 下一步

根据审计报告中的 HIGH 项，进入 P0-003：路径配置化第一刀。
