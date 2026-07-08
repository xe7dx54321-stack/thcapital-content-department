"""
Phase36: Production Readiness Gate
评估是否可以进入真实观察
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime
import json


@dataclass
class GateCheckItem:
    check_id: str
    name: str
    description: str
    expected: str
    actual: str = ""
    status: str = "pending"
    is_blocking: bool = True
    cloud_mode_warn_only: bool = False


@dataclass
class ProductionReadinessGateResult:
    schema_version: str = "v1"
    generated_at: str = ""
    
    gate_checks: List[GateCheckItem] = field(default_factory=list)
    
    pass_count: int = 0
    warn_count: int = 0
    fail_count: int = 0
    blocking_failures: int = 0
    
    overall_status: str = "pending"
    ready_for_observation: bool = False
    
    next_steps: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "gate_checks": [
                {
                    "check_id": c.check_id,
                    "name": c.name,
                    "description": c.description,
                    "expected": c.expected,
                    "actual": c.actual,
                    "status": c.status,
                    "is_blocking": c.is_blocking,
                    "cloud_mode_warn_only": c.cloud_mode_warn_only
                }
                for c in self.gate_checks
            ],
            "pass_count": self.pass_count,
            "warn_count": self.warn_count,
            "fail_count": self.fail_count,
            "blocking_failures": self.blocking_failures,
            "overall_status": self.overall_status,
            "ready_for_observation": self.ready_for_observation,
            "next_steps": self.next_steps
        }


def run_production_readiness_gate(
    phase35_pass: bool = True,
    phase34b_pass: bool = True,
    phase34a_pass: bool = True,
    phase33b_pass: bool = True,
    usage_boundary_pass: bool = True,
    no_secret_leak: bool = True,
    no_openclaw_mod: bool = True,
    auto_publish_disabled: bool = True,
    workbench_ok: bool = True,
    local_rss_smoke_done: bool = False,
    runtime_observation_done: bool = False,
    cloud_mode: bool = True
) -> ProductionReadinessGateResult:
    """运行 Production Readiness Gate"""
    
    result = ProductionReadinessGateResult(
        generated_at=datetime.now().isoformat()
    )
    
    result.gate_checks = [
        # Cloud pipeline checks
        GateCheckItem(
            check_id="phase33b_workbench",
            name="Phase33B Workbench",
            description="Workbench 运营控制台可用",
            expected="PASS",
            actual="PASS" if phase33b_pass else "FAIL",
            status="PASS" if phase33b_pass else "FAIL",
            is_blocking=True,
            cloud_mode_warn_only=False
        ),
        GateCheckItem(
            check_id="phase34a_rss",
            name="Phase34A RSS 情报层",
            description="RSS 情报层工程通过",
            expected="PASS",
            actual="PASS" if phase34a_pass else "FAIL",
            status="PASS" if phase34a_pass else "FAIL",
            is_blocking=True,
            cloud_mode_warn_only=False
        ),
        GateCheckItem(
            check_id="phase34b_diversity",
            name="Phase34B Topic Diversity",
            description="Topic diversity 工程通过",
            expected="PASS",
            actual="PASS" if phase34b_pass else "FAIL",
            status="PASS" if phase34b_pass else "FAIL",
            is_blocking=True,
            cloud_mode_warn_only=False
        ),
        GateCheckItem(
            check_id="phase35_editorial",
            name="Phase35 Editorial Quality",
            description="编辑质量 pipeline 工程通过",
            expected="PASS",
            actual="PASS" if phase35_pass else "FAIL",
            status="PASS" if phase35_pass else "FAIL",
            is_blocking=True,
            cloud_mode_warn_only=False
        ),
        GateCheckItem(
            check_id="usage_boundary",
            name="Usage Boundary Gate",
            description="使用边界 gate 通过",
            expected="PASS",
            actual="PASS" if usage_boundary_pass else "FAIL",
            status="PASS" if usage_boundary_pass else "FAIL",
            is_blocking=True,
            cloud_mode_warn_only=False
        ),
        # Safety checks
        GateCheckItem(
            check_id="no_secret_leak",
            name="No RSS Secret Leak",
            description="RSS secret 未入库",
            expected="no_secret",
            actual="no_secret" if no_secret_leak else "secret_detected",
            status="PASS" if no_secret_leak else "FAIL",
            is_blocking=True,
            cloud_mode_warn_only=False
        ),
        GateCheckItem(
            check_id="no_openclaw_mod",
            name="No OpenClaw Modification",
            description="OpenClaw 未被修改",
            expected="no_modification",
            actual="no_modification" if no_openclaw_mod else "modified",
            status="PASS" if no_openclaw_mod else "FAIL",
            is_blocking=True,
            cloud_mode_warn_only=False
        ),
        GateCheckItem(
            check_id="auto_publish",
            name="Auto Publish Disabled",
            description="自动发布已禁用",
            expected="disabled",
            actual="disabled" if auto_publish_disabled else "enabled",
            status="PASS" if auto_publish_disabled else "FAIL",
            is_blocking=True,
            cloud_mode_warn_only=False
        ),
        GateCheckItem(
            check_id="workbench_status",
            name="Workbench Status",
            description="Workbench 可显示今日稿件/质量/系统状态",
            expected="visible",
            actual="visible" if workbench_ok else "not_visible",
            status="PASS" if workbench_ok else "FAIL",
            is_blocking=True,
            cloud_mode_warn_only=False
        ),
        # Local-only checks (warn only in cloud mode)
        GateCheckItem(
            check_id="local_rss_smoke",
            name="Local RSS Smoke Test",
            description="本地 RSS smoke test 已执行",
            expected="done",
            actual="done" if local_rss_smoke_done else "pending",
            status="PASS" if local_rss_smoke_done else ("WARN" if cloud_mode else "FAIL"),
            is_blocking=False if cloud_mode else True,
            cloud_mode_warn_only=True
        ),
        GateCheckItem(
            check_id="runtime_observation",
            name="Runtime Observation",
            description="Mac Runtime 观察已执行",
            expected="done",
            actual="done" if runtime_observation_done else "pending",
            status="PASS" if runtime_observation_done else ("WARN" if cloud_mode else "FAIL"),
            is_blocking=False if cloud_mode else True,
            cloud_mode_warn_only=True
        )
    ]
    
    # 统计
    for check in result.gate_checks:
        if check.status == "PASS":
            result.pass_count += 1
        elif check.status == "WARN":
            result.warn_count += 1
        else:
            result.fail_count += 1
            if check.is_blocking:
                result.blocking_failures += 1
    
    # 决定整体状态
    if result.blocking_failures > 0:
        result.overall_status = "FAIL"
        result.ready_for_observation = False
        result.next_steps = ["修复阻断性问题后再进入观察"]
    elif result.warn_count > 0:
        result.overall_status = "ACTIONABLE"
        result.ready_for_observation = True
        result.next_steps = [
            "云端 pipeline 已通过",
            "可在本地执行 RSS smoke test 和 Runtime 观察",
            "建议先阅读 docs/LOCAL_RSS_ENV_SETUP.md"
        ]
    else:
        result.overall_status = "PASS"
        result.ready_for_observation = True
        result.next_steps = [
            "所有检查通过",
            "可以进入真实观察阶段"
        ]
    
    return result


def save_readiness_gate(result: ProductionReadinessGateResult, output_dir: Path) -> Dict[str, str]:
    """保存 Readiness Gate 结果"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON
    dated_json = output_dir / f"{result.generated_at[:10].replace('-', '')}__production-readiness-gate.json"
    latest_json = output_dir / "latest_production_readiness_gate.json"
    
    json_data = result.to_dict()
    
    with open(dated_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    with open(latest_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    # Markdown
    md_content = _generate_readiness_gate_md(result)
    
    dated_md = output_dir / f"{result.generated_at[:10].replace('-', '')}__production-readiness-gate.md"
    latest_md = output_dir / "latest_production_readiness_gate.md"
    
    with open(dated_md, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    with open(latest_md, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return {
        "dated_json": str(dated_json),
        "latest_json": str(latest_json),
        "dated_md": str(dated_md),
        "latest_md": str(latest_md)
    }


def _generate_readiness_gate_md(result: ProductionReadinessGateResult) -> str:
    """生成 Markdown 报告"""
    
    md = f"""# Production Readiness Gate

## 概述

- **生成时间**: {result.generated_at}
- **整体状态**: {result.overall_status}
- **可进入观察**: {result.ready_for_observation}

## 检查结果统计

| 状态 | 数量 |
|------|------|
| ✅ PASS | {result.pass_count} |
| ⚠️ WARN | {result.warn_count} |
| ❌ FAIL | {result.fail_count} |
| 阻断性失败 | {result.blocking_failures} |

## 检查项详情

| ID | 名称 | 描述 | 期望 | 实际 | 状态 | 阻断 |
|----|------|------|------|------|------|------|
"""
    
    for check in result.gate_checks:
        md += f"| {check.check_id} | {check.name} | {check.description} | {check.expected} | {check.actual} | {check.status} | {check.is_blocking} |\n"
    
    md += "\n## 下一步建议\n\n"
    for step in result.next_steps:
        md += f"- {step}\n"
    
    md += """
---

**Phase36** | Production Readiness Gate
"""
    
    return md