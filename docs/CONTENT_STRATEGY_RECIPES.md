# Content Strategy Recipes

## 目标

内容策略 recipes 定义不同类型文章的打法：什么题适合什么结构、需要什么证据、标题和开头应如何选择。

recipes 是 title/opening/structure pattern 的上层选择策略，不替代已有 pattern 模块。

## 六类打法

- 趋势判断型：用于连续信号和行业方向变化。
- 产业链预期型：用于价值链、预算流向和上下游影响。
- 公司/项目拆解型：用于头部公司、新项目和产品战略变化。
- 技术路线型：用于模型、Agent 框架和开发者工具路线选择。
- 产品战略型：用于入口变化、分发策略和用户工作流变化。
- 投资框架型：用于可形成投资判断框架的产业变化。

## 使用方式

`config/content_strategy_recipes.json` 是机器可读配置。`make methodology-topic-score` 会推荐 recipe，`make methodology-article-review` 会检查文章是否符合对应打法。

## 边界

recipes 只生成建议和评审信号，不自动改 prompt、rules、brief、outline 或 draft。
