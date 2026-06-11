# P31-005 Retry / Backoff / Checkpoint / Idempotency Report

Adds error classification, retry queue generation, checkpoint helpers, and idempotency keys for daily, slot, weekly, and artifact-version scopes. Safety gate, cost block, and validation errors are not blindly retried.
