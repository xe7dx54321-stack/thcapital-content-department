# P1-005 Value Scoring v1 报告

## 本轮目标

- 对 topic clusters 进行规则型价值评分。
- 输出 total_score、score_band 和 recommended_action。
- 将评分规则配置化到 `config/value_scoring_rules.json`。

## 新增文件

- `config/value_scoring_rules.json`
- `src/content_system/value_scoring.py`
- `scripts/score_topic_clusters.py`

## 新增命令

```bash
make value-scores
```

## 评分维度

- source_authority
- freshness
- novelty
- strategic_relevance
- market_impact
- technical_substance
- narrative_potential
- evidence_strength

## 输出产物

- `同行资本市场内容系统/03_topic_candidates/YYYYMMDD__topic-cluster-scores.json`
- `同行资本市场内容系统/03_topic_candidates/YYYYMMDD__topic-cluster-scores.md`
- `同行资本市场内容系统/03_topic_candidates/latest_topic_cluster_scores.json`
- `同行资本市场内容系统/03_topic_candidates/latest_topic_cluster_scores.md`

## 注意事项

- 当前评分是启发式规则评分，不代表最终编辑判断。
- novelty 暂不做复杂历史比对。
