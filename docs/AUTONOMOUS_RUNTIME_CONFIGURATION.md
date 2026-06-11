# Autonomous Runtime Configuration

Phase 31 adds three operator-editable runtime configs:

- `config/runtime_schedule.yaml`: daily/weekly slots and runtime tick/heartbeat settings.
- `config/runtime_jobs.yaml`: job registry mapped to existing repository scripts.
- `config/runtime_policies.yaml`: retry, failure, cost, and locking policy.

The runtime uses `system_local` timezone and does not hard-code schedule times in Python. `launchd` only starts `scripts/run_autonomous_runtime.py`; all business scheduling lives in project config and the internal scheduler.

Safety boundaries: no automatic publishing, no WeChat API, no draft box, no image generation by default, no OpenClaw gateway dependency, and no OpenClaw cron migration.
