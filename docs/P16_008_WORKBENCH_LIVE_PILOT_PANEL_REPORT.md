# P16-008 Workbench Live Pilot Panel Report

## 本轮目标

把 live pilot 输出、quality comparison 和 image generation approval queue 接入微信公众号工作台。

## 已完成

- 工作台数据新增 `live_pilot_panel`。
- 审稿模式新增 Live Pilot 面板。
- 右侧系统判断面板新增 live comparison / image approval 摘要。

## 当前限制

- 阅读模式保持干净，不展示内部 live pilot 细节。
- 浏览器不直接触发 live 调用。
