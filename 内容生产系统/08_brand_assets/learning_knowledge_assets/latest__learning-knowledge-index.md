# 学习知识资产索引 v2

- `generated_at`: `2026-05-09 17:44:21 CST`
- `date`: `2026-05-09`
- `purpose`: `把对标公众号真正蒸馏成可调用的 style skill packs，并把统一封面/正文图审美接进写作生产链。`

## Creator Skill Packs

| 创作者 | 样本门槛 | Skill Card | Text Patterns | Visual Patterns | Style Audit |
| --- | --- | --- | --- | --- | --- |
| 数字生命卡兹克 | 8/20 | [skill-card](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/digitallife-khazix/skill-card.md) | [text-patterns](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/digitallife-khazix/text-patterns.md) | [visual-patterns](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/digitallife-khazix/visual-patterns.md) | [style-audit](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/digitallife-khazix/style-audit.md) |
| 赛博禅心 | 8/20 | [skill-card](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/cyber-zenmind/skill-card.md) | [text-patterns](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/cyber-zenmind/text-patterns.md) | [visual-patterns](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/cyber-zenmind/visual-patterns.md) | [style-audit](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/cyber-zenmind/style-audit.md) |
| 饼干哥哥AGI | 8/20 | [skill-card](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/cookie-brother-agi/skill-card.md) | [text-patterns](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/cookie-brother-agi/text-patterns.md) | [visual-patterns](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/cookie-brother-agi/visual-patterns.md) | [style-audit](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/cookie-brother-agi/style-audit.md) |
| 袋鼠帝AI客栈 | 8/20 | [skill-card](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/kangaroo-ai-inn/skill-card.md) | [text-patterns](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/kangaroo-ai-inn/text-patterns.md) | [visual-patterns](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/kangaroo-ai-inn/visual-patterns.md) | [style-audit](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/kangaroo-ai-inn/style-audit.md) |
| 量子位 | 8/20 | [skill-card](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/qbitai/skill-card.md) | [text-patterns](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/qbitai/text-patterns.md) | [visual-patterns](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/qbitai/visual-patterns.md) | [style-audit](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/qbitai/style-audit.md) |
| 机器之心 | 8/20 | [skill-card](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/jiqizhixin/skill-card.md) | [text-patterns](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/jiqizhixin/text-patterns.md) | [visual-patterns](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/jiqizhixin/visual-patterns.md) | [style-audit](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/jiqizhixin/style-audit.md) |
| 智东西 | 8/20 | [skill-card](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/zhidx/skill-card.md) | [text-patterns](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/zhidx/text-patterns.md) | [visual-patterns](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/zhidx/visual-patterns.md) | [style-audit](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/creator_skill_packs/zhidx/style-audit.md) |

## 运行时调用链

1. `topic-radar / topic-approval` 先选 `content_route`，明确 `primary overlay`。
2. `draft-pack` 按 route 加载对应 `overlay skill -> skill-card -> text-patterns -> visual-patterns`。
3. `hook-title-cover / visual-intelligence` 统一遵守 [图文与封面统一审美 v2](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/visual_playbooks/th_capital_visual_playbook_v2.md)。
4. `content-polish` 出稿前必须过一遍对应创作者的 `style-audit.md`，防止品牌漂移和烂图混入。

## 题材打法页

- [event_explainer__playbook](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/content_type_playbooks/event_explainer__playbook.md)
- [product_experience__playbook](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/content_type_playbooks/product_experience__playbook.md)
- [industry_analysis__playbook](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/content_type_playbooks/industry_analysis__playbook.md)
- [builder_teardown__playbook](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/content_type_playbooks/builder_teardown__playbook.md)
- [opinionated_commentary__playbook](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/content_type_playbooks/opinionated_commentary__playbook.md)

## 通用打法页

- [包装打法页](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/packaging_playbooks/th_capital_packaging_playbook_v2.md)
- [图文与封面统一审美 v2](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/visual_playbooks/th_capital_visual_playbook_v2.md)
- [失败模式页](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/failure_patterns/content_failure_patterns_v2.md)
- [风格路由表](/Users/apple/Documents/同行资本内容部门/内容生产系统/08_brand_assets/learning_knowledge_assets/latest__style-router.md)

## 当前硬规则

- 每个 creator skill pack 都必须基于最近 `20` 篇 distinct deep articles。
- 样本门槛没过，就不允许把该创作者当 `primary overlay`。
- 不允许让外部创作者人格覆盖 TH Capital 品牌人格。
- 不允许用抽象 AI 图替代原始证据或结构说明。
