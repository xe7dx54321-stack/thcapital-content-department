# Phase 1 Daily Pipeline 报告

## 本轮目标

- 新增 `make phase1-daily` 作为 Phase 1 v1 日常总入口。
- 串联 official daily full run、runtime baseline、source coverage、evidence packets、topic clusters、value scores 和 high-value candidates。
- 输出 pipeline JSON/Markdown summary 和 frontstage board。

## 新增文件

- `scripts/run_phase1_daily_pipeline.py`

## 新增命令

```bash
make phase1-daily
```

## 执行步骤

1. `scripts/run_official_daily_full_run.py`
2. `scripts/update_official_runtime_baseline.py`
3. `scripts/build_source_coverage_alignment.py`
4. `scripts/build_evidence_packets.py`
5. `scripts/build_topic_clusters.py`
6. `scripts/score_topic_clusters.py`
7. `scripts/build_high_value_candidate_pool.py`

## 输出产物

- `同行资本市场内容系统/10_logs/YYYYMMDD__phase1-daily-pipeline.json`
- `同行资本市场内容系统/10_logs/YYYYMMDD__phase1-daily-pipeline.md`
- `同行资本市场内容系统/10_logs/latest_phase1_daily_pipeline.json`
- `同行资本市场内容系统/10_logs/latest_phase1_daily_pipeline.md`
- `同行资本市场内容系统/11_frontstage/YYYYMMDD__phase1-daily-pipeline-board.md`
- `同行资本市场内容系统/11_frontstage/latest_phase1_daily_pipeline_board.md`

## 状态规则

- 任一步骤非 0 退出：`FAILED`。
- evidence / cluster 不足但脚本正常：`DEGRADED`。
- official full run 成功且结构化链路有有效输出：`SUCCESS`。

## 未做事项

- 不做内容生成。
- 不接入新信源。
- 不做 retry/fallback。
- 不引入第三方依赖。
