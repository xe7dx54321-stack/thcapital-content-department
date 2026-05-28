# P11-003 Article Version Memory Report

## 本轮目标

将候选版本、自动评分和人工决策沉淀为本地版本记忆。

## 已完成能力

- 记录版本来源 action、score delta、推荐动作和人工决策。
- 根据结果生成 lessons。
- 输出前台 memory board。

## 边界

- 文件型记忆，不替代 SQLite runtime store。
- 不自动改变 prompt、规则或原稿。
