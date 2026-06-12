# Phase 31B Closeout

## 目标

Enable and validate the Mac mini autonomous runtime go-live path.

## Go-Live Preflight

Preflight must have zero blocking failures before installation.

## OpenClaw Conflict Resolution

Only safe conflicts may be disabled automatically. Manual-review conflicts remain explicit.

## OpenClaw Backup and Rollback

Backups are stored under `/Users/apple/.openclaw/cron/backups/`; rollback restores the latest apply backup.

## LaunchAgent Installation

The LaunchAgent is user-level and starts `scripts/run_autonomous_runtime.py`.

## Runtime Startup

Runtime PID and LaunchAgent loaded state are validated after install.

## Heartbeat

Heartbeat freshness is part of go-live validation and Workbench display.

## Restart Validation

Graceful shutdown is requested through runtime control, then launchd relaunch is verified.

## Real Scheduler Trigger

One-time validation slot must be executed by `AUTONOMOUS_SCHEDULER`.

## Missed-run Catch-up

Catch-up validation covers recent required jobs and compressed stale acquisition slots.

## Idempotency

Duplicate slot submission must execute once and skip the duplicate.

## Workbench Acceptance

Workbench shows the Autonomous Runtime Control Center without polluting article preview.

## Safety and Cost Observation

Forbidden attempts must remain zero.

## Go-Live Acceptance Gate

Phase32 may start only when the gate is approved or approved with non-blocking warnings.

## 正式运行方式

`launchd -> scripts/run_autonomous_runtime.py -> Workbench Runtime Control Center`

## 人工 fallback

`make stable-daily-ops`

## 当前 warning

OpenClaw conflicts that are not strictly safe remain manual review.

## 回滚方法

1. `python3 scripts/runtime_control.py pause`
2. `python3 scripts/uninstall_macos_runtime_launchd.py --uninstall`
3. `python3 scripts/rollback_openclaw_conflict_resolution.py --latest`
4. `make stable-daily-ops`

## 下一阶段

Phase 32：Autonomous Topic-to-Article Production Activation v1。
