# RSS Live Smoke Test Plan

## 概述

- **生成时间**: 2026-07-08T02:48:13.922713
- **启用状态**: False
- **需要真实执行**: False
- **状态**: plan_generated

## 配置限制

| 参数 | 值 | 说明 |
|------|---|------|
| `max_sources` | 2 | 最多启用 RSS 源数 |
| `max_articles_per_source` | 20 | 每源最多文章数 |

## 环境变量白名单

- `GEEKPARK_RSS_URL`
- `OFFICIAL_AI_RSS_URL`

## Smoke Test 步骤

| Step | 名称 | 命令 | 本地执行 | 云端安全 | 验证字段 |
|------|------|------|----------|----------|----------|
| enable_sources | 启用 RSS 源 | `设置环境变量` | True | False | sources_enabled |
| validate_sources | 验证 RSS 源配置 | `make wechat-rss-sources-validate` | False | True | source_validation_status |
| ingest | 抓取 RSS 文章 | `make wechat-rss-ingest` | True | False | fetched_source_count |
| clean | 清洗去重 | `make wechat-rss-clean` | False | True | cleaned_count |
| intelligence | 提取情报 | `make wechat-article-intelligence` | False | True | intelligence_article_count |
| coverage | 竞品覆盖分析 | `make competitive-coverage-analysis` | False | True | coverage_count |
| boundary | 使用边界检查 | `make wechat-rss-usage-boundary-gate` | False | True | boundary_gate_status |
| workbench | 查看 Workbench | `make wechat-workbench` | False | True | workbench_panel_visible |
| record | 记录结果 | `手动记录` | True | False | record_complete |

## 验证字段

| 字段 | 说明 |
|------|------|
| `fetched_source_count` | 抓取的 RSS 源数量 |
| `article_count` | 抓取的文章总数 |
| `cleaned_count` | 清洗后的文章数 |
| `duplicate_count` | 去重的文章数 |
| `intelligence_article_count` | 提取情报的文章数 |
| `coverage_count` | 竞品覆盖分析数 |
| `style_pattern_count` | 风格 pattern 数 |
| `boundary_gate_status` | 使用边界 gate 状态 |
| `workbench_panel_visible` | Workbench 面板是否可见 |

## 安全规则

- no_secret_in_output
- no_fulltext_in_git
- no_auto_publish
- max_2_sources
- max_20_articles_per_source

## 统计

- **步骤总数**: 9

---

**Phase36** | RSS Live Smoke Test Plan
