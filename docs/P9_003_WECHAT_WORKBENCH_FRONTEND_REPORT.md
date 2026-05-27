# P9-003 WeChat Workbench Frontend v1 Report

## 本轮目标

生成极简本地内容工作台 HTML：左侧今日选题，中间公众号文章预览，底部 Chief Editor Agent 输入区。

## 新增文件

- `src/content_system/wechat_workbench_frontend.py`
- `scripts/build_wechat_workbench_frontend.py`
- `scripts/serve_wechat_workbench.py`

## 新增命令

```bash
make wechat-workbench
make serve-wechat-workbench
```

## 页面边界

前台是静态 HTML，不登录、不联网、不自动执行 action。底部输入框只生成本地命令提示。
