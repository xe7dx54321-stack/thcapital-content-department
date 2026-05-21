# Top20 Stage-Gate Scorecard — 2026-05-16

**pipeline**: day_mainline
**stage**: top20_score
**scorecard_version**: 20260516__top20__stage-gate-scorecard.md
**generated_at**: 2026-05-16T08:06:00Z (16:06 CST)

---

## Pre-flight Check Results

| Artifact | Path | State | Expected | Result |
|---|---|---|---|---|
| top20-screening-pack | 03_topic_candidates/20260516__top20-screening-pack.md | empty/header-only (10 lines, no list body) | final | ❌ NOT FINAL |
| redteam-review | 10_logs/20260516__top20__redteam-review.md | absent (only platform-task-sheet redteam exists, wrong stage) | final | ❌ NOT FOUND |

**WAITING_ON_TOP20_INPUTS**: `true`

---

## Continuity Decision

- **status**: no-op
- **continuity_decision**: wait_for_inputs
- **continuity_output**: no-op — inputs not ready

---

## Root Cause (who owes what)

| Owner | Missing Artifact | Required Action |
|---|---|---|
| `market-scout` / `signal-scout` | 03_topic_candidates/20260516__top20-screening-pack.md — no body | Populate full Top20 list with scoring + signal_reasons |
| `redteam-reviewer` | 10_logs/20260516__top20__redteam-review.md — file absent | After pack is final, produce redteam review of candidate pool |

> 红队骂的是候选对象池，不是只骂 market-scout。若红队指出证据/覆盖/热度验证不足，返工责任须拆到 `signal-scout / market-scout + topic-planner`，不是整段打回 Top20。

---

## No-op

> 任一前置未达 final，scorecard 无法输出正式评分结论。
> 前置就绪后需重新运行本裁判逻辑，不得沿用旧结论。