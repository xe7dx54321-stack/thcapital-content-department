.PHONY: doctor path-audit sources-validate source-health source-runtime-health manifest-validate manifest-write-from-packets official-lane-with-manifest official-lane-health-check official-lane-daily daily-official-lane daily-source-summary official-lane-quality-gate daily-official-quality-gate status

PYTHON ?= python3

doctor:
	$(PYTHON) scripts/doctor.py

path-audit:
	$(PYTHON) scripts/audit_hardcoded_paths.py

sources-validate:
	$(PYTHON) scripts/validate_sources.py

source-health:
	$(PYTHON) scripts/build_source_health.py

source-runtime-health:
	$(PYTHON) scripts/build_source_runtime_health.py

manifest-validate:
	$(PYTHON) scripts/validate_runtime_manifest.py

manifest-write-from-packets:
	$(PYTHON) scripts/write_runtime_manifest_from_packets.py

official-lane-with-manifest:
	$(PYTHON) scripts/run_official_lane_with_manifest.py

official-lane-health-check:
	$(PYTHON) scripts/run_official_lane_health_check.py

# Recommended daily entry for the official update lane.
official-lane-daily: official-lane-health-check

# Alias for users who search for daily commands first.
daily-official-lane: official-lane-health-check

# Build a compact daily source run summary from runtime manifest + source runtime health.
daily-source-summary:
	$(PYTHON) scripts/build_daily_source_run_summary.py

# Report-only quality gate for the official daily lane. Does not retry or block by default.
official-lane-quality-gate:
	$(PYTHON) scripts/check_official_lane_quality_gate.py

# Alias for daily operation.
daily-official-quality-gate: official-lane-quality-gate

status:
	bash 内容工厂控制台/status.sh
