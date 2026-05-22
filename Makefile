.PHONY: doctor path-audit sources-validate status

PYTHON ?= python3

# 项目健康检查：路径、目录、关键脚本、写入权限、可选网络检查。
doctor:
	$(PYTHON) scripts/doctor.py

# 扫描仓库中的本机绝对路径/硬编码路径，并生成审计报告。
path-audit:
	$(PYTHON) scripts/audit_hardcoded_paths.py

# 校验采集信源注册表。
sources-validate:
	$(PYTHON) scripts/validate_sources.py

# 兼容内容工厂控制台已有 status.sh。
status:
	bash 内容工厂控制台/status.sh
