# P14-007 Workbench Methodology Panel Report

## 本轮目标

把方法论评分接入微信公众号工作台，让用户看到系统为什么推荐一个题、为什么认为一篇文章需要修改。

## 修改文件

- `src/content_system/wechat_workbench_data.py`
- `src/content_system/wechat_workbench_frontend.py`

## UI 改进

- 审稿模式新增内容方法论卡片。
- 右侧系统判断面板展示 topic/article methodology score 和 recipe。
- Chief Editor 快捷指令新增按方法论重写、增强核心判断、强化预期差、补产业链影响、提升开头张力、提升判断密度。

## 边界

阅读模式保持干净，方法论评分只出现在审稿/右侧面板。
