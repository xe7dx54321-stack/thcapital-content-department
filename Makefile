.PHONY: doctor path-audit sources-validate source-health status

PYTHON ?= python3

# 项目健康检查：路径、目录、关键脚本、写入权限、可选网络检查。
doctor:
	$(PYTHON) scripts/doctor.py

# 扫描仓库中的本机路径硬编码。
path-audit:
	$(PYTHON) scripts/audit_hardcoded_paths.py

# 校验采集信源注册表。
sources-validate:
	$(PYTHON) scripts/validate_sources.py

# 基于 Source Registry 生成静态 source health / coverage 报告。
source-health:
	$(PYTHON) scripts/build_source_health.py

# 兼容内容工厂控制台已有 status.sh。
status:
	bash 内容工厂控制台/status.sh
