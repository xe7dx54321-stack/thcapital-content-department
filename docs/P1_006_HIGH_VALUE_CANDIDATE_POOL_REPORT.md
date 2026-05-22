# P1-006 Daily High-Value Candidate Pool v1 报告

## 本轮目标

- 将 scored topic clusters 转成每日可读的高价值候选池。
- Markdown 展示 summary、top candidates、details、key evidence 和 risks / missing info。
- 作为 Phase 2 content brief 的输入，不直接生成文章。

## 新增文件

- `src/content_system/high_value_candidates.py`
- `scripts/build_high_value_candidate_pool.py`

## 新增命令

```bash
make high-value-candidates
```

## 输出产物

- `同行资本市场内容系统/03_topic_candidates/YYYYMMDD__high-value-candidates.json`
- `同行资本市场内容系统/03_topic_candidates/YYYYMMDD__high-value-candidates.md`
- `同行资本市场内容系统/03_topic_candidates/latest_high_value_candidates.json`
- `同行资本市场内容系统/03_topic_candidates/latest_high_value_candidates.md`
- `同行资本市场内容系统/11_frontstage/YYYYMMDD__high-value-candidates-board.md`
- `同行资本市场内容系统/11_frontstage/latest_high_value_candidates_board.md`

## 未做事项

- 不生成 content brief。
- 不生成 outline。
- 不生成微信公众号或小红书成品内容。
