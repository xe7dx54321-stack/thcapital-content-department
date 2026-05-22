.PHONY: doctor path-audit sources-validate source-health source-runtime-health manifest-validate manifest-write-from-packets official-lane-with-manifest official-lane-health-check official-lane-daily daily-official-lane daily-source-summary official-lane-quality-gate daily-official-quality-gate official-daily-dashboard daily-official-dashboard official-daily-full-run daily-official-full-run runtime-baseline source-coverage evidence-packets topic-clusters value-scores high-value-candidates phase1-daily status

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

daily-source-summary:
	$(PYTHON) scripts/build_daily_source_run_summary.py

official-lane-quality-gate:
	$(PYTHON) scripts/check_official_lane_quality_gate.py

daily-official-quality-gate: official-lane-quality-gate

official-daily-dashboard:
	$(PYTHON) scripts/build_official_daily_dashboard.py

daily-official-dashboard: official-daily-dashboard

official-daily-full-run:
	$(PYTHON) scripts/run_official_daily_full_run.py

daily-official-full-run:
	$(PYTHON) scripts/run_official_daily_full_run.py

runtime-baseline:
	$(PYTHON) scripts/update_official_runtime_baseline.py

source-coverage:
	$(PYTHON) scripts/build_source_coverage_alignment.py

evidence-packets:
	$(PYTHON) scripts/build_evidence_packets.py

topic-clusters:
	$(PYTHON) scripts/build_topic_clusters.py

value-scores:
	$(PYTHON) scripts/score_topic_clusters.py

high-value-candidates:
	$(PYTHON) scripts/build_high_value_candidate_pool.py

phase1-daily:
	$(PYTHON) scripts/run_phase1_daily_pipeline.py

status:
	bash 内容工厂控制台/status.sh
