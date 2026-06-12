# P31C-003 Lane-specific Cadence Migration Report

`config/acquisition_cadence.yaml` migrates the useful OpenClaw early/midday/evening acquisition rhythm into lane-specific cadence. The Runtime still executes batched lane slots and shared connector runs, rather than copying OpenClaw jobs.

Cadence includes timezone, catch-up policy, rationale, network requirement, grouping window, source dedup, and rate-limit policy.
