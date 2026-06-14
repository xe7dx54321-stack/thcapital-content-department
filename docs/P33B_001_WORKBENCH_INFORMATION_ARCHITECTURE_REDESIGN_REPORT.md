# P33B-001 Workbench Information Architecture Redesign Report

## 目标

将 Workbench 从工程调试面板堆叠重构为内容工厂运营控制台。

## 新结构

- 今日总览
- 今日稿件
- 质量检查
- 历史回放
- 系统运维

## 数据边界

前端只消费 `workbench_view_model` 的五个区域，不再在模板中直接拼接 Runtime、OpenClaw、Replay、稿件正文等原始面板。

