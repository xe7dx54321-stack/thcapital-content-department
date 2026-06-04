# P17-007 Workbench Image Asset Panel Report

## 本轮目标

把 Phase 17 live promotion、图片任务、图片资产库、图文预览和视觉审查接入工作台。

## 已完成能力

- `wechat_workbench_data` 新增 `image_asset_panel`。
- `wechat_workbench_frontend` 审稿模式新增图片资产链路卡片。
- 右侧 insight panel 展示 task / asset / wechat-ready 摘要。
- 支持复制 image prompt、design brief、expected asset path 和 CLI 命令。

## 边界

- 阅读模式保持干净。
- 页面只复制内容或命令，不自动执行发布或图片生成。
