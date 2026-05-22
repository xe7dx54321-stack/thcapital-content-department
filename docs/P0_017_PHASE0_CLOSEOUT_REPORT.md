# P0-017 Phase 0 Closeout Report

## Phase 0 目标

Phase 0 的目标是把一个本地脚本和历史素材混合的内容生产项目，整理成可检查、可审计、可配置、可运行、可交接的工程底座。重点不是重写业务链路，而是建立后续 Phase 1/2 所需的状态、路径、source registry、runtime manifest、health report 和 official lane 日常入口。

## 已完成能力

- 项目健康检查：`make doctor`。
- 路径硬编码审计：`make path-audit`。
- 路径配置化：`src/content_system/paths.py`。
- Source Registry：`config/sources.yaml` 与 `make sources-validate`。
- Source Health：`make source-health`。
- Source Runtime Health：`make source-runtime-health`。
- Runtime Manifest Contract：`make manifest-validate`。
- Runtime Manifest Writer：`make manifest-write-from-packets`。
- Official lane runtime manifest wrapper：`make official-lane-with-manifest`。
- Official lane health check：`make official-lane-health-check`。
- Daily source summary：`make daily-source-summary`。
- Official lane quality gate：`make official-lane-quality-gate`。
- Official daily dashboard：`make official-daily-dashboard`。
- Official daily full run：`make official-daily-full-run`。
- Generated artifacts ignore 策略：运行产物默认不进入 Git。

## 当前官方 lane 日常入口

推荐命令：

```bash
make official-daily-full-run
```

兼容别名：

```bash
make daily-official-full-run
```

## 关键命令清单

```bash
make doctor
make path-audit
make sources-validate
make source-health
make source-runtime-health
make manifest-validate
make manifest-write-from-packets
make official-lane-with-manifest
make official-lane-health-check
make official-lane-daily
make daily-source-summary
make official-lane-quality-gate
make official-daily-dashboard
make official-daily-full-run
```

## 生成产物与 ignore 策略

Phase 0 期间新增的审计、health、runtime manifest、daily summary、quality gate、dashboard、official full run 等产物均属于运行生成产物。它们默认写入：

```text
同行资本市场内容系统/10_logs/
同行资本市场内容系统/11_frontstage/
```

这些产物已由 `.gitignore` 覆盖，后续不应作为源码提交。需要共享时，应提取小型摘要或报告，而不是提交完整运行 JSON。

## 已知限制

- official lane 已有完整 daily wrapper，但其他 lane 尚未全部接入 runtime manifest。
- Source Runtime Health 对非 official lane 的观测仍有限。
- 当前仍不包含 retry/fallback。
- 当前仍不包含数据库或调度系统。
- 当前不做 LLM 写稿、内容生成质量判断或平台发布自动化。
- 剩余 HIGH 路径主要位于旧版内容生产脚本和历史素材抓取脚本，未在 Phase 0 收口继续扩大清理。

## Phase 1 入口建议

- P1-001：Official Lane Runtime Baseline 7-day Observation。
- P1-002：Source Registry Coverage Alignment。
- P1-003：Evidence Packet v1。
- P1-004：Topic Cluster v1。
- P1-005：Value Scoring v1。

Phase 1 应继续保持小步交付：先观察 official lane 的真实运行基线，再扩大 registry/manifest 覆盖，最后进入 evidence packet 和结构化价值判断。

## 验收命令

```bash
python3 -m py_compile scripts/run_official_daily_full_run.py
make official-daily-full-run
make doctor
make path-audit
make sources-validate
make manifest-validate
git ls-files | grep -E 'official-daily-full-run|daily-source-run-summary|official-lane-quality-gate|official-daily-dashboard|source-runtime-health|runtime-manifest|path-hardcode-audit' || true
git status --short --branch
```
