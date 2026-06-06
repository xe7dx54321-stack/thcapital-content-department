# P29-009 Phase 29 Daily Migration Pipeline Report

## Scope

Adds `make phase29-daily` as the Phase 29 pipeline entry.

## Pipeline

1. Import OpenClaw source inventory.
2. Classify source risk.
3. Build P0/P1 migration plan.
4. Run selected metadata connectors.
5. Run weak signal safety gate.
6. Normalize OpenClaw signals.
7. Rebuild daily hot material pool.
8. Run hot material quality gate.
9. Run stable daily ops.
10. Rebuild workbench data and frontend.

## Boundary

No auto publishing, WeChat API, image generation, full-text fetch, OpenClaw gateway, OpenClaw cron migration, login/paywall bypass, or config mutation.
