# Phase 33B Closeout

## 目标

将 Workbench 从工程调试型页面重构为内容工厂运营控制台。

## 新信息架构

- 今日总览
- 今日稿件
- 质量检查
- 历史回放
- 系统运维

## View Model

新增 `workbench_view_model`，前端只基于五个清晰区域渲染。

## 安全边界

- 不自动发布。
- 不接公众号 API。
- 不抓全文。
- 不调用图片模型。
- 不修改 OpenClaw jobs / gateway / cron。
- 不提交运行产物。

## 当前限制

部分操作按钮仍是安全占位，避免伪装成已执行。

