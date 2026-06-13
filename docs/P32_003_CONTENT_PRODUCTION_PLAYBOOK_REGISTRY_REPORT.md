# P32-003 Content Production Playbook Registry Report

## 目标

新增内容生产 playbook registry，将旧 know-how 清洗为当前系统可执行的选题评分、brief、大纲、初稿、审稿、重写和最终候选稿规则。

## 新增配置

- `config/content_production_playbooks.yaml`
- `config/topic_scoring_playbook.yaml`
- `config/brief_generation_playbook.yaml`
- `config/outline_generation_playbook.yaml`
- `config/draft_generation_playbook.yaml`
- `config/review_rewrite_playbook.yaml`

## 边界

写作规则配置化；不硬编码关键方法论；不覆盖旧方法论；所有自动稿件保留 `do_not_publish=true` 和人工审阅要求。
