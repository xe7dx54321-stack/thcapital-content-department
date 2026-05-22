# P0-004 HIGH 风险路径配置化第二刀报告

## 本轮目标

- 基于 P0-003/P0-003b 后的 path audit HIGH 项，继续处理仍参与运行的脚本路径硬编码。
- 复用 `src/content_system/paths.py` 中的统一路径配置策略。
- 优先处理活跃市场内容系统脚本和内容工厂控制台会加载的旧版内容生产系统模块。
- 不重写抓取主链路，不改变业务输出格式，不处理历史文档、归档素材和旧日志。

## 修改文件

活跃市场内容系统：

- `同行资本市场内容系统/09_runbooks/scripts/market_topic_capture_round.py`
- `同行资本市场内容系统/09_runbooks/scripts/market_official_update_lane.py`
- `同行资本市场内容系统/09_runbooks/scripts/market_wechat_rss_refresh.py`
- `同行资本市场内容系统/09_runbooks/scripts/market_wechat_deep_capture_round.py`
- `同行资本市场内容系统/09_runbooks/scripts/market_learning_memo_builder.py`
- `同行资本市场内容系统/09_runbooks/scripts/market_learning_pool_board_builder.py`
- `同行资本市场内容系统/09_runbooks/scripts/market_top20_pack_guard.py`

内容工厂控制台相关旧版模块：

- `内容生产系统/09_runbooks/scripts/market_content_pack_truth.py`
- `内容生产系统/09_runbooks/scripts/market_frontstage_board_builder.py`
- `内容生产系统/09_runbooks/scripts/market_ops_dashboard_builder.py`
- `内容生产系统/09_runbooks/scripts/market_learning_memo_builder.py`
- `内容生产系统/09_runbooks/scripts/market_learning_knowledge_builder.py`
- `内容生产系统/09_runbooks/scripts/market_learning_pool_board_builder.py`
- `内容生产系统/09_runbooks/scripts/market_platform_task_sheet_to_approved.py`

状态文档：

- `docs/PROJECT_STATE.md`
- `docs/DEVELOPMENT_TASKS.md`
- `docs/P0_004_PATH_CONFIG_SECOND_PASS_REPORT.md`

## 处理的 HIGH 风险路径类型

- 活跃市场系统脚本中的固定 macOS 用户目录根路径。
- 旧版内容生产系统中，内容工厂控制台看板链路会加载的固定项目根路径。
- 控制台学习池和运营看板中动态本地文件链接生成的 `file` scheme 字面量。

处理方式：

- 通过脚本自身位置向上查找仓库根目录。
- 将仓库 `src/` 加入 `sys.path`。
- 复用 `content_system.paths.get_project_paths()`。
- 活跃市场脚本使用 `paths.market_content_root`。
- 旧版内容生产系统模块使用 `paths.legacy_content_root`。

## 保留未处理的范围

- 旧版内容生产系统中未确认属于当前控制台入口的历史/生产脚本。
- 素材库中的历史抓取脚本。
- `_archive/`、旧日志、历史 planning 文档和生成型报告。
- OpenClaw 等用户工具目录常量，后续需要结合真实运行方式单独处理。

## 验收命令

```bash
python3 -m py_compile scripts/doctor.py
python3 -m py_compile scripts/audit_hardcoded_paths.py
python3 -m py_compile src/content_system/paths.py
python3 -m py_compile <本轮修改的 Python 脚本>
bash -n 内容工厂控制台/start.sh
bash -n 内容工厂控制台/open.sh
bash -n 内容工厂控制台/status.sh
bash -n 内容工厂控制台/restart.sh
make doctor
make path-audit
git ls-files | grep 'path-hardcode-audit' || true
git status --short
```

## path-audit 对比

- P0-003/P0-003b 后 HIGH：74。
- P0-004 后 HIGH：56。
- 变化说明：下降 18 项，主要来自活跃市场系统根路径、内容工厂控制台看板链路的旧版根路径，以及动态本地文件链接字面量。

## 风险与下一步

剩余 HIGH 主要分布在旧版内容生产系统的其他脚本和少量素材抓取脚本中。本轮按范围没有无差别批量修改，避免影响尚未梳理清楚的旧生产链路。

下一步建议进入 P0-005：采集稳定性工程第一步 —— Source Registry v1。先建立统一 `config/sources.yaml` 和读取能力，为后续 source health、retry、fallback 做准备。
