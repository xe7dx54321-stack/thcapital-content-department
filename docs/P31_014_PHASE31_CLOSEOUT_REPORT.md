# Phase 31 Closeout

## 目标

Phase 31 adds the autonomous runtime layer needed for daily unattended operation.

## 最终 Runtime 架构

macOS launchd keeps one runtime process alive. The project runtime owns schedules, job dependencies, idempotency, retry, network routing, and workbench status.

## Internal Scheduler

The scheduler reads `config/runtime_schedule.yaml` and `config/runtime_jobs.yaml`, writes execution ledger records, and prevents duplicate daily-slot runs.

## Persistent Execution Ledger

Runtime state lives in ignored SQLite files under `同行资本市场内容系统/12_runtime_store/`.

## Daily Pipeline DAG

The daily graph models acquisition, evidence, topic, content, review, final candidate, workbench, and closeout nodes with required/optional/degradable flags.

## Retry / Checkpoint / Idempotency

Retry is policy-driven. Safety gate blocks, cost blocks, and data validation errors are not blindly retried.

## Network / VPN-aware Routing

Network readiness routes domestic, international, offline, and local-only work without attempting to control VPN clients.

## Missed-run Recovery

The recovery planner detects missed slots and compresses stale acquisition windows into consolidated catch-up work.

## Heartbeat / Failure Notification

Heartbeat and local notification artifacts make runtime health visible without a paid notification service.

## Runtime CLI

`scripts/runtime_control.py` provides local status, pause, resume, run, retry, cancel, and shutdown commands.

## Workbench Runtime Control Center

The workbench now shows runtime status, ledger, retry queue, missed runs, network readiness, route plan, and dry-run status.

## macOS launchd Bootstrap

Phase 31 ships a LaunchAgent template and dry-run installer. Actual installation remains an operator action.

## OpenClaw Coexistence Guard

The coexistence report identifies legacy OpenClaw jobs that may duplicate new runtime acquisition or generation.

## Autonomous Dry Run

`make autonomous-runtime-dry-run` exercises the runtime lifecycle without publishing, installing LaunchAgent, generating images, or modifying OpenClaw.

## 安全边界

No automatic publishing, no WeChat API, no draft box, no image generation by default, no full-text scraping, no OpenClaw gateway dependency, and no OpenClaw cron migration.

## 实际安装状态

Only dry-run rendering is performed by default. LaunchAgent installation awaits explicit operator execution.

## 当前限制

The runtime orchestrates the daily system, but Phase 32 is still needed to strengthen autonomous topic-to-article production quality.

## 下一阶段

Phase 32：Autonomous Topic-to-Article Production Activation v1.
