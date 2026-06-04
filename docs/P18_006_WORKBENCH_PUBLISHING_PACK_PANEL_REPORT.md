# P18-006 Workbench Publishing Pack Panel Report

## 目标

把 visual-approved candidate、WeChat copy pack、visual checklist、visual performance 和 visual feedback 接入工作台。

## 已完成

- `wechat_workbench_data.py` 新增 `publishing_pack_panel`。
- `wechat_workbench_frontend.py` 新增图文发布包 panel。
- 支持复制标题、正文、图片槽位说明和人工发布步骤。

## 边界

- 按钮只复制内容。
- 不发布。
- 不调用公众号 API。
