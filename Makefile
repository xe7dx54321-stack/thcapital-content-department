.PHONY: doctor path-audit sources-validate source-health source-runtime-health manifest-validate status

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

status:
	bash 内容工厂控制台/status.sh
