# P7-010 Phase 7 Daily Pipeline Report

## 本轮目标

新增 Phase 7 日常总入口。

## 新增命令

```bash
make phase7-daily
```

## 执行链路

1. `run_phase6_daily_agent_pipeline.py`
2. MiniMax / Claude live pilot readiness checks
3. `build_llm_ab_comparison.py`
4. `run_daily_scheduler.py --dry-run`
5. `build_failure_notification_report.py`
6. `run_retry_fallback_runner.py`
7. `build_weekly_content_retro.py`

## 安全边界

- 默认不 live。
- live 必须 env + allowlist。
- judge live 旁路。
- rewrite live suggestion-only。
