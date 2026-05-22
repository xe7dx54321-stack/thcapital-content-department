# P0-003 路径配置化第一刀开发报告

## 本轮目标

- 修复状态文档的 Markdown 多行维护格式。
- 建立统一路径配置策略，为后续脚本复用提供稳定入口。
- 优先配置化 `doctor` 和内容工厂控制台入口中的本机绝对路径。
- 让核心工程入口默认使用仓库内相对路径，并允许环境变量覆盖。

## 修改文件

- `src/content_system/paths.py`
- `scripts/doctor.py`
- `内容工厂控制台/start.sh`
- `内容工厂控制台/open.sh`
- `内容工厂控制台/status.sh`
- `内容工厂控制台/restart.sh`
- `内容工厂控制台/README.md`
- `env.example`
- `config/ENV_EXAMPLE.txt`
- `.gitignore`
- `docs/PROJECT_STATE.md`
- `docs/DEVELOPMENT_TASKS.md`

## 新增配置

```bash
THCAP_MARKET_CONTENT_ROOT
THCAP_LEGACY_CONTENT_ROOT
THCAP_CONTENT_CONSOLE_ROOT
CONTENT_FACTORY_DASHBOARD_HOST
CONTENT_FACTORY_DASHBOARD_PORT
```

`.env` 已加入忽略规则，`env.example` 只保留占位路径，不写入真实本机路径。

## 路径解析规则

`src/content_system/paths.py` 提供 `ProjectPaths` 和 `get_project_paths()`：

- `repo_root`：由传入 root 或路径模块位置推导。
- `market_content_root`：优先读取 `THCAP_MARKET_CONTENT_ROOT`，否则使用 `repo_root/同行资本市场内容系统`。
- `legacy_content_root`：优先读取 `THCAP_LEGACY_CONTENT_ROOT`，否则使用 `repo_root/内容生产系统`。
- `console_root`：优先读取 `THCAP_CONTENT_CONSOLE_ROOT`，否则使用 `repo_root/内容工厂控制台`。
- `scripts_root`、`frontstage_root`、`logs_root`：基于 `market_content_root` 推导。

内容工厂控制台入口脚本默认基于脚本所在目录和仓库根目录推导路径；如需迁移到其他机器，可以通过环境变量覆盖。

## 验收命令

```bash
python3 -m py_compile scripts/doctor.py
python3 -m py_compile scripts/audit_hardcoded_paths.py
python3 -m py_compile src/content_system/paths.py
make doctor
make path-audit
bash 内容工厂控制台/status.sh || true
bash 内容工厂控制台/open.sh || true
git status --short
git ls-files | grep 'path-hardcode-audit' || true
```

## 风险与未处理范围

- 本轮只改工程入口和控制台入口。
- 不批量清理历史文档中的路径。
- 不重写市场内容抓取主链路。
- 不处理旧日志、归档素材和 planning 文档中的历史路径。
- `同行资本市场内容系统/09_runbooks/scripts/` 内部仍可能存在参与运行的路径常量，后续单独处理。

## 下一步建议

进入 P0-004：HIGH 风险路径配置化第二刀。

下一轮应基于 `make path-audit` 结果，优先处理 `同行资本市场内容系统/09_runbooks/scripts/` 中仍参与运行的主路径常量，同时保持抓取主链路的小步改造和可回滚。
