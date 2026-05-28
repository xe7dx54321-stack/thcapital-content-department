# P12-006 Workbench Final Review Panel Report

## 本轮目标

把 final article candidate 和 final checklist 接入微信公众号工作台，让用户在审稿模式和右侧面板看到最终候选稿状态。

## 修改文件

- `src/content_system/wechat_workbench_data.py`
- `src/content_system/wechat_workbench_frontend.py`
- `src/content_system/wechat_article_preview.py`

## UI 改进

- 工作台数据新增 `final_review`。
- 审稿模式展示 final candidate id、来源 version、人类评分、score delta、checklist 状态和剩余风险。
- 右侧面板展示 final candidate 总状态。
- 支持复制最终标题、最终正文、人工发布步骤。

## 安全边界

- 按钮只复制内容。
- 不调用发布 API。
- 不提交公众号草稿。
- 不标记为已发布。
