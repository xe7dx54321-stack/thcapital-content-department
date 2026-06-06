# P29-006 OpenClaw Signal Normalization & Hot Material Integration Report

## Scope

Normalizes OpenClaw metadata connector items into `normalized-openclaw-signals` and integrates candidate signals into the daily hot material pool.

## Integration

- `daily-hot-material-pool` reports OpenClaw signal counts.
- `hot-material-quality-gate` recognizes weak signals.
- Weak signals default to `WATCH` or `BACKFILL_REQUIRED`, not direct promotion.

## Boundary

OpenClaw signals remain metadata-only and cannot be used as hard evidence without confirmation.
