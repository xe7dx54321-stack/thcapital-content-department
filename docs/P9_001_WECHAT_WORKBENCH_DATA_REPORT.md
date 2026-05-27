# P9-001 WeChat Workbench Data Builder v1 Report

## 本轮目标

把今日选题、公众号稿件、审核结果、发布候选和系统状态整理成前台可用 JSON。

## 新增文件

- `src/content_system/wechat_workbench_data.py`
- `scripts/build_wechat_workbench_data.py`

## 输出产物

- `同行资本市场内容系统/11_frontstage/*wechat-workbench-data*.json`
- `同行资本市场内容系统/10_logs/*wechat-workbench-data-summary*.json`

## 新增命令

```bash
make wechat-workbench-data
```

## 边界

只生成本地数据，不调用公众号 API，不自动发布。
