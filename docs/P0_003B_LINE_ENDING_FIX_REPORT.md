# P0-003b 文件物理换行修复报告

## 背景

P0-003 提交后，线上 raw 文件显示多个关键文件仍为物理单行或少数超长行。为避免把显示问题误判为代码问题，本轮同时检查了本地工作区文件和当前 Git commit 对象中的物理行数。

检查结果显示，P0-003 的关键 Python、shell、Markdown、配置示例文件在本地和 Git 对象中均为正常多行文本，且没有 CRLF 或孤立 CR。线上 raw 单行现象更可能来自抓取或展示链路。

## 本轮修复

- 保留 P0-003 的路径配置化能力。
- 保留 `THCAP_MARKET_CONTENT_ROOT`、`THCAP_LEGACY_CONTENT_ROOT`、`THCAP_CONTENT_CONSOLE_ROOT`、`CONTENT_FACTORY_DASHBOARD_HOST`、`CONTENT_FACTORY_DASHBOARD_PORT` 配置入口。
- 保留控制台脚本基于 `SCRIPT_DIR` / `REPO_ROOT` / 环境变量推导路径的实现。
- 补充 P0-003b 状态文档和任务清单记录。
- 新增本报告，明确后续用 `wc -l`、`py_compile`、`bash -n` 验收物理换行和语法。

## 验收命令

```bash
python3 -m py_compile src/content_system/paths.py
python3 -m py_compile scripts/doctor.py
python3 -m py_compile scripts/audit_hardcoded_paths.py
bash -n 内容工厂控制台/start.sh
bash -n 内容工厂控制台/open.sh
bash -n 内容工厂控制台/status.sh
bash -n 内容工厂控制台/restart.sh
make doctor
make path-audit
bash 内容工厂控制台/status.sh || true
bash 内容工厂控制台/open.sh || true
git status --short
git ls-files | grep 'path-hardcode-audit' || true
```

## wc -l 检查结果

```text
79  src/content_system/paths.py
161 scripts/doctor.py
134 内容工厂控制台/start.sh
28  内容工厂控制台/open.sh
63  内容工厂控制台/status.sh
6   内容工厂控制台/restart.sh
106 docs/PROJECT_STATE.md
118 docs/DEVELOPMENT_TASKS.md
75  docs/P0_003_PATH_CONFIG_REPORT.md
18  env.example
17  config/ENV_EXAMPLE.txt
15  Makefile
```

这些文件均不是单个物理长行。`restart.sh` 只有 6 行是因为它本身只是停止再启动的薄包装脚本，内容足够短。

## 路径检查说明

`env.example`、`config/ENV_EXAMPLE.txt`、P0-003 涉及的控制台入口脚本和状态文档没有新增真实本机 Documents 绝对路径示例。

当前真实路径检查仍会命中 `内容工厂控制台/runtime/` 和 `内容工厂控制台/logs/` 中的既有运行态文件。本轮不扩大到清理 runtime/logs 历史文件，也不进入 P0-004。

## 后续建议

下一步仍然进入 P0-004：HIGH 风险路径配置化第二刀。

P0-004 应聚焦仍参与运行的 `同行资本市场内容系统/09_runbooks/scripts/` 主路径常量，不处理历史 planning 文档、归档素材和旧日志。
