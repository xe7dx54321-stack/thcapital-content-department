# Official Lane Daily Runbook

## Purpose

This runbook defines the recommended daily entry for the AI/Agent official update lane.

The official lane is the highest-authority ingestion lane for official updates from AI labs, model companies, infra companies, and related first-party sources. It should remain conservative, observable, and easy to validate.

## Recommended command

Run from the repository root:

```bash
make official-lane-daily
```

Equivalent commands:

```bash
make daily-official-lane
make official-lane-health-check
python3 scripts/run_official_lane_health_check.py
```

## What the daily entry does

`make official-lane-daily` delegates to `make official-lane-health-check`, which runs three steps:

1. `scripts/run_official_lane_with_manifest.py`
   - Runs the existing official update lane wrapper.
   - Preserves existing official lane outputs.
   - Writes an official runtime manifest.

2. `scripts/validate_runtime_manifest.py`
   - Validates the latest official runtime manifest against the P0-008 runtime manifest contract.

3. `scripts/build_source_runtime_health.py`
   - Refreshes source runtime health using structured runtime manifest evidence when available.

## Expected successful output

A successful run should show:

```text
Official Lane Health Check
====================================
status: SUCCESS
manifest_status: SUCCESS
source_count: <number>
total_items_found: <number>

Steps:
- official_lane_with_manifest: OK (0)
- validate_official_runtime_manifest: OK (0)
- build_source_runtime_health: OK (0)
```

## Generated artifacts

The daily entry can generate local runtime artifacts such as:

```text
同行资本市场内容系统/02_topic_radar/raw/official_<YYYYMMDD>/
同行资本市场内容系统/02_topic_radar/source_packets/<YYYYMMDD>__official_lane/
同行资本市场内容系统/03_topic_candidates/<YYYYMMDD>__official-top20.md
同行资本市场内容系统/10_logs/<YYYYMMDD>__official-source-manifest.md
同行资本市场内容系统/10_logs/<YYYYMMDD>__official-runtime-manifest.json
同行资本市场内容系统/10_logs/latest_official_runtime_manifest.json
同行资本市场内容系统/10_logs/latest_source_runtime_health.json
同行资本市场内容系统/10_logs/latest_source_runtime_health.md
```

These are generated runtime artifacts and should not be committed to Git.

## Post-run verification

After running the daily entry, run:

```bash
git status --short --branch
```

Expected result:

```text
## main...origin/main
```

If generated artifacts appear as untracked files, update `.gitignore` before committing anything.

## When to use lower-level commands

Use `make official-lane-with-manifest` when you only want to run the official lane wrapper and write the official runtime manifest.

Use `make manifest-validate` when you only want to validate the example runtime manifest contract.

Use `make source-runtime-health` when you only want to refresh runtime source health from existing artifacts.

## Current design boundary

This daily entry intentionally does not:

- modify `market_official_update_lane.py` directly;
- change official lane output formats;
- add retry/fallback;
- add a scheduler;
- add a database;
- publish content automatically.

The wrapper route is the current stable default. Direct integration into the official lane script can be considered later if the wrapper remains stable.
