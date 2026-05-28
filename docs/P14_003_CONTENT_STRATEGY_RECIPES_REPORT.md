# P14-003 Content Strategy Recipes Report

## 本轮目标

建立系统级内容类型打法，让选题、结构、标题、开头和证据要求按照内容类型组织。

## 修改文件

- `config/content_strategy_recipes.json`
- `docs/CONTENT_STRATEGY_RECIPES.md`
- `src/content_system/content_strategy_recipes.py`
- `scripts/validate_content_strategy_recipes.py`

## 核心能力

- 定义 6 类 recipe：趋势判断型、产业链预期型、公司/项目拆解型、技术路线型、产品战略型、投资框架型。
- 每个 recipe 包含适用/不适用场景、结构、证据要求、标题/开头模式、常见失败和质量门槛。
- 作为 title/opening/structure/pattern adapter 的上层选择策略。

## 边界

recipe 是策略配置，不自动替换历史 pattern，也不自动应用到生成链路。
