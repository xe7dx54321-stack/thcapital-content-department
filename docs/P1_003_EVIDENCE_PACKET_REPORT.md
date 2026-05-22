# P1-003 Evidence Packet v1 报告

## 本轮目标

- 从 official lane source packets 中抽取标准化 evidence packet。
- 保留 raw item，便于追溯。
- 使用规则型方法抽取 event_type、entities、domain_tags 和基础分值。

## 新增文件

- `src/content_system/evidence_packet.py`
- `scripts/build_evidence_packets.py`

## 新增命令

```bash
make evidence-packets
```

## 输出产物

- `同行资本市场内容系统/03_topic_candidates/YYYYMMDD__evidence-packets.json`
- `同行资本市场内容系统/03_topic_candidates/YYYYMMDD__evidence-packets.md`
- `同行资本市场内容系统/03_topic_candidates/latest_evidence_packets.json`
- `同行资本市场内容系统/03_topic_candidates/latest_evidence_packets.md`

## 规则边界

- 不调用 LLM。
- 不做 embedding。
- 不做成品文章生成。
- 不改变 official lane 的原始输出格式。
