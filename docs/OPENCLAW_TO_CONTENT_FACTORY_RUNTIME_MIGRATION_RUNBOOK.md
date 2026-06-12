# OpenClaw to Content Factory Runtime Migration Runbook

1. Run `make openclaw-schedule-coexistence`.
2. Run `make openclaw-conflict-resolution-plan`.
3. Run `make openclaw-conflict-resolution-safe-apply`.
4. Verify backup path and changed job ids.
5. If needed, run `make openclaw-conflict-resolution-rollback`.

Do not stop OpenClaw gateway automatically. Do not disable non-safe jobs.
