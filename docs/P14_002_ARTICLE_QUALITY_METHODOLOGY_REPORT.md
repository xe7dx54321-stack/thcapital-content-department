# P14-002 Article Quality Methodology Report

## 本轮目标

建立统一的公众号文章质量方法论，定义什么文章算“好”，并为后续评审、改稿和 Chief Editor Agent 提供标准。

## 修改文件

- `config/article_quality_methodology.json`
- `docs/CONTENT_ARTICLE_QUALITY_METHOD.md`
- `src/content_system/article_quality_methodology.py`
- `scripts/validate_article_quality_methodology.py`

## 核心能力

- 定义 10 个文章质量标准：清晰问题、核心判断、逻辑推进、证据匹配、叙事张力、读者相关、判断密度、风险平衡、公众号可读性、可复述性。
- 标记常见空泛表达，用于后续 review 和 rewrite 优先级判断。
- 定义 hook、judgment、evidence_chain、implication、risk、closing_framework 等结构组件。

## 边界

质量方法论只生成评审标准和提示，不自动覆盖文章、不自动修改 prompt/rules。
