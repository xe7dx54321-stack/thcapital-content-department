# P14-006 Chief Editor Methodology Adapter Report

## 本轮目标

让 Chief Editor Agent 理解方法论评分，在解释用户需求和生成 action plan 时能引用选题/文章标准。

## 修改文件

- `src/content_system/chief_editor_methodology_adapter.py`
- `src/content_system/chief_editor_agent.py`
- `scripts/build_chief_editor_methodology_context.py`

## 输出

- `同行资本市场内容系统/10_logs/latest_chief_editor_methodology_context.json`
- `同行资本市场内容系统/10_logs/latest_chief_editor_methodology_context.md`

## 核心能力

- 为 Chief Editor 构建方法论上下文。
- 用户说“太泛了”时，可关联 judgment_density、core_judgment、generic_language_flags。
- 用户要求换题时，可参考 methodology topic score。
- 用户要求改标题/开头时，可参考 recipe 和 article methodology。

## 边界

Chief Editor 仍默认 PLAN_ONLY，不自动执行、不自动改稿。
