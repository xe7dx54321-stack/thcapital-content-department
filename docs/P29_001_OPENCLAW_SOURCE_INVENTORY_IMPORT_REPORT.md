# P29-001 OpenClaw Source Inventory Import Report

## Scope

Imports OpenClaw source and job metadata into a read-only inventory sidecar.

## Inputs

- `/Users/apple/.openclaw/cron/jobs.json`
- `/Users/apple/Library/LaunchAgents/ai.openclaw.gateway.plist`
- `docs/OPENCLAW_SOURCE_INVENTORY_NOTES.md` as optional fallback context

## Outputs

- `latest_openclaw_source_inventory.json`
- `latest_openclaw_source_inventory.md`
- `latest_openclaw_source_inventory_board.md`

## Boundary

No gateway start, no cron migration, no full-text fetch, no publishing.
