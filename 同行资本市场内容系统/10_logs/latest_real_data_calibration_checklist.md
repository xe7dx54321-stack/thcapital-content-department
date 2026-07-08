# Real Data Calibration Checklist

## 概述

- **生成时间**: 2026-07-08T03:14:54.135487
- **状态**: checklist_generated
- **清单项总数**: 13

## RSS 相关 (5 项)

| ID | 名称 | 观察问题 | 通过标准 | 失败表现 | 记录字段 |
|----|------|----------|----------|----------|----------|
| rss_stability | RSS ingest 稳定性 | RSS 抓取是否稳定运行？ | 连续 3 次成功，无超时或错误 | 频繁超时、失败、或返回空 | `rss_ingest_success_rate` |
| rss_clean_quality | 正文清洗质量 | 清洗后的正文是否干净？ | 无明显 HTML 残留、广告、乱码 | 正文含 HTML tag、广告文字、截断 | `clean_quality_score` |
| rss_duplicate | 去重有效性 | 去重是否有效减少重复？ | 重复文章 < 5% | 重复文章 > 20% | `duplicate_rate` |
| rss_intelligence | 情报抽取准确性 | 情报抽取是否准确？ | 核心信息提取正确，无幻觉 | 关键信息遗漏或错误 | `intelligence_accuracy` |
| rss_coverage | 竞品覆盖价值 | 竞品覆盖分析是否有价值？ | 能识别竞品角度和空白 | 分析空洞或无效 | `coverage_value_score` |

## Topic 相关 (2 项)

| ID | 名称 | 观察问题 | 通过标准 | 失败表现 | 记录字段 |
|----|------|----------|----------|----------|----------|
| topic_diversity | 选题去重效果 | 选题去重是否减少重复？ | 同日选题相似度 < 0.7 | 同日选题高度相似 | `topic_similarity_avg` |
| topic_differentiated | 差异化角度可用性 | 差异化角度推荐是否可用？ | 推荐角度有实质差异 | 推荐角度雷同或空洞 | `differentiated_angle_count` |

## Editorial 相关 (4 项)

| ID | 名称 | 观察问题 | 通过标准 | 失败表现 | 记录字段 |
|----|------|----------|----------|----------|----------|
| title_quality | 标题生成质量 | 标题是否更像公众号标题？ | 标题符合长度、角度、价值要求 | 标题过长、营销号风格、空洞 | `title_quality_avg` |
| ai_taste_effect | AI 味拦截效果 | AI 味拦截是否有效？ | 拦截 > 70% discouraged phrases | 大量 AI 味表达未拦截 | `ai_taste_hit_rate` |
| style_score_match | Draft style score 符合直觉 | Draft style score 是否符合人工直觉？ | 高/低分稿件人工判断一致 | 评分与人工判断相反 | `style_score_match_rate` |
| version_gate | Version comparison 防退化 | Version comparison 是否防止退化？ | 改写退化时 reject | 退化改写被 accept | `version_gate_accuracy` |

## Workbench 相关 (2 项)

| ID | 名称 | 观察问题 | 通过标准 | 失败表现 | 记录字段 |
|----|------|----------|----------|----------|----------|
| workbench_clarity | Workbench 清晰度 | Workbench 是否清晰呈现状态？ | 状态一目了然，无 raw JSON | 信息混乱或显示 raw JSON | `workbench_clarity_score` |
| workbench_production | 生产验证面板 | 生产验证面板是否可用？ | 显示正确状态，无 secret | 显示错误状态或 secret | `production_panel_visible` |

## 记录模板

建议使用以下格式记录校准结果：

```json
{
  "date": "YYYY-MM-DD",
  "calibration_records": [
    {
      "item_id": "xxx",
      "result": "PASS/WARN/FAIL",
      "value": "实际值",
      "notes": "备注"
    }
  ]
}
```

---

**Phase36** | Real Data Calibration Checklist
