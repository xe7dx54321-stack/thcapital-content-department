# P9-010 WeChat Workbench UI Polish Report

## 本轮目标

将 Phase 9 已跑通的本地微信公众号工作台，从工程样板打磨为可日常审稿、改稿、和 Chief Editor Agent 协作的内容编辑台。

## 修改文件

- `src/content_system/wechat_workbench_data.py`
- `src/content_system/wechat_article_preview.py`
- `src/content_system/wechat_workbench_frontend.py`
- `docs/PROJECT_STATE.md`
- `docs/DEVELOPMENT_TASKS.md`

## UI 改进点

- 使用温暖纸张色背景、白色阅读稿纸、克制绿色强调色和更舒适的中文系统字体。
- 将页面重组为顶部状态栏、左侧选题栏、中间公众号阅读器、右侧系统判断面板和底部 Chief Editor 协作区。
- 左侧选题卡片突出状态、分数、证据数量和推荐理由。
- 右侧面板独立承载质量分、Judge、Critic、Revision 和下一步建议，避免污染正文阅读态。

## 交互改进点

- 支持点击左侧选题切换当前文章。
- 支持阅读模式 / 审稿模式切换。
- 支持快捷指令填充 Chief Editor 输入框。
- 支持基于当前选中文章生成并复制 `chief-editor-agent` 命令。
- 展示当前目标文章、最近一次 AI 理解和 pending action queue。

## 公众号预览改进点

- 强化公众号标题区、作者/日期区和正文阅读宽度。
- 优化正文行高、段落间距、小标题、引用、证据和风险提示样式。
- 阅读模式只展示文章和必要发布前提示，内部审核信息进入审稿模式和右侧面板。

## Chief Editor 区域改进点

- 底部输入区改为主编协作台样式。
- 快捷指令覆盖换选题、投资人视角、补证据、重写标题、重写开头、批准、搁置。
- 命令预览会绑定当前文章标题与 article id。
- 仍保持 `PLAN_ONLY`，不会自动执行 pending actions。

## 验证结果

- 已通过 Python 语法检查。
- 已生成最新 workbench data、article preview 和 workbench HTML。
- 已通过本地静态服务打开页面检查主要交互。

## 当前限制

- 页面仍是静态 HTML，不直接提交表单到后端。
- Chief Editor 命令仍需用户复制到终端执行。
- 不接公众号 API，不进入草稿箱，不自动发布。
- Action Router 只生成 pending actions，不自动改稿。

## 下一步建议

进入 Phase 10：Workbench Action Execution 与稿件自动修订 v1。
