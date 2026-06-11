# P31-002 Persistent Scheduler State & Execution Ledger Report

Adds a SQLite-backed autonomous runtime state store with runtime instance, scheduled run, job run, job attempt, checkpoint, artifact reference, heartbeat, runtime event, and control state tables. Database files are ignored and are never committed.
