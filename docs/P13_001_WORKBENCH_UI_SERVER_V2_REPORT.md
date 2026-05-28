# P13-001 Workbench UI Server v2 Report

## 本轮目标

把静态工作台升级为本地交互式服务，减少复制命令负担，同时保持“不发布、不接 API、不读取凭证”的安全边界。

## 修改文件

- `src/content_system/workbench_ui_server.py`
- `scripts/serve_workbench_ui.py`
- `Makefile`

## 已完成能力

- 新增 `make serve-workbench-ui`。
- 服务只监听 `127.0.0.1:8767`。
- 支持 `/health`、`/api/workbench-data`、final candidate、version review、pending actions、publish session、metrics、performance memory 等只读接口。
- 支持 Chief Editor、action approval、version review、final review、manual publish session、manual metrics 等白名单 POST 接口。

## 安全边界

- 不执行任意 shell。
- 不调用公众号 API。
- 不进入公众号草稿箱。
- 不处理账号密码。
- 不自动发布。

## 当前限制

第一版是本地 HTTP 服务，不包含登录、云部署、真实平台集成。
