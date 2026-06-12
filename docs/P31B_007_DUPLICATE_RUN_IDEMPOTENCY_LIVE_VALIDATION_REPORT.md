# P31B-007 Duplicate-run / Idempotency Live Validation Report

Validation submits the same validation job and slot twice. The second submission must be skipped by idempotency and must not create duplicate artifacts.
