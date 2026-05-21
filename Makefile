.PHONY: doctor status

PYTHON ?= python3

# 项目健康检查：路径、目录、关键脚本、写入权限、可选网络检查。
doctor:
	$(PYTHON) scripts/doctor.py

# 兼容内容工厂控制台已有 status.sh。
status:
	bash 内容工厂控制台/status.sh
