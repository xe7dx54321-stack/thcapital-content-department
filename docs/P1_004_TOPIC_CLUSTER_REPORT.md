# P1-004 Topic Cluster v1 报告

## 本轮目标

- 将 evidence packets 聚合为 topic clusters。
- 优先按 company/product/model 实体交集聚类。
- 否则按 event_type 和标题 token 聚类。

## 新增文件

- `src/content_system/topic_cluster.py`
- `scripts/build_topic_clusters.py`

## 新增命令

```bash
make topic-clusters
```

## 输出产物

- `同行资本市场内容系统/03_topic_candidates/YYYYMMDD__topic-clusters.json`
- `同行资本市场内容系统/03_topic_candidates/YYYYMMDD__topic-clusters.md`
- `同行资本市场内容系统/03_topic_candidates/latest_topic_clusters.json`
- `同行资本市场内容系统/03_topic_candidates/latest_topic_clusters.md`

## 未做事项

- 不使用 embedding 或向量库。
- 不做复杂主题建模。
- 不做文章大纲或初稿生成。
