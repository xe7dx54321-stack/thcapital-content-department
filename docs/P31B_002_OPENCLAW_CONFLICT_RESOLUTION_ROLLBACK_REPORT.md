# P31B-002 OpenClaw Conflict Resolution & Rollback Report

The conflict plan is safe-only. Jobs are disabled only when strict replacement coverage is confirmed.

Apply creates a timestamped backup under `/Users/apple/.openclaw/cron/backups/`. Rollback restores the latest backup and verifies hashes.
