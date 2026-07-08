"""
Phase36: Cloud-to-Local Production Validation Plan
生成从云端开发能力迁移到本地验证的计划
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from pathlib import Path
import yaml
import json


@dataclass
class ValidationStep:
    step_id: str
    name: str
    description: str
    required: bool
    local_only: bool = False
    cloud_safe: bool = True
    status: str = "pending"


@dataclass
class ValidationPlanResult:
    schema_version: str = "v1"
    generated_at: str = ""
    mode: str = "cloud_development"
    
    cloud_completed_capabilities: List[str] = field(default_factory=list)
    local_validation_required: List[str] = field(default_factory=list)
    runtime_validation_required: List[str] = field(default_factory=list)
    dry_run_only: List[str] = field(default_factory=list)
    
    validation_sequence: List[ValidationStep] = field(default_factory=list)
    pass_criteria: List[str] = field(default_factory=list)
    warn_criteria: List[str] = field(default_factory=list)
    block_criteria: List[str] = field(default_factory=list)
    
    status: str = "pending"
    checklist_count: int = 0
    local_only_items: int = 0
    cloud_safe_items: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "mode": self.mode,
            "cloud_completed_capabilities": self.cloud_completed_capabilities,
            "local_validation_required": self.local_validation_required,
            "runtime_validation_required": self.runtime_validation_required,
            "dry_run_only": self.dry_run_only,
            "validation_sequence": [
                {
                    "step_id": s.step_id,
                    "name": s.name,
                    "description": s.description,
                    "required": s.required,
                    "local_only": s.local_only,
                    "cloud_safe": s.cloud_safe,
                    "status": s.status
                }
                for s in self.validation_sequence
            ],
            "pass_criteria": self.pass_criteria,
            "warn_criteria": self.warn_criteria,
            "block_criteria": self.block_criteria,
            "status": self.status,
            "checklist_count": self.checklist_count,
            "local_only_items": self.local_only_items,
            "cloud_safe_items": self.cloud_safe_items
        }


def build_local_production_validation_plan() -> ValidationPlanResult:
    """生成云到本地验证计划"""
    
    from datetime import datetime
    
    result = ValidationPlanResult(
        generated_at=datetime.now().isoformat(),
        mode="cloud_development"
    )
    
    # 云端已完成能力清单
    result.cloud_completed_capabilities = [
        "Phase33B: Workbench 运营控制台",
        "Phase34A: WeChat RSS 全文情报层工程能力",
        "Phase34B: 选题去重、差异化角度、主选题 rerank",
        "Phase35: 编辑风格手册、叙事框架、标题生成、AI 味拦截"
    ]
    
    # 需要本地真实 RSS 验证的能力
    result.local_validation_required = [
        "RSS ingest 稳定性",
        "正文清洗效果",
        "情报抽取准确性",
        "竞品覆盖价值"
    ]
    
    # 需要 Mac mini Runtime 验证的能力
    result.runtime_validation_required = [
        "LaunchAgent 定时运行",
        "Heartbeat 监控",
        "Retry queue 处理",
        "Missed-run catch-up"
    ]
    
    # 只需要 dry-run 的能力
    result.dry_run_only = [
        "编辑风格手册验证",
        "叙事框架选择",
        "标题生成规则",
        "AI 味拦截",
        "Draft style score",
        "Version comparison gate"
    ]
    
    # 验证顺序
    result.validation_sequence = [
        ValidationStep(
            step_id="cloud_regression",
            name="云端回归验证",
            description="验证所有 Phase35/34B/34A/33B pipeline 在云端通过",
            required=True,
            local_only=False,
            cloud_safe=True,
            status="pending"
        ),
        ValidationStep(
            step_id="rss_smoke_test",
            name="RSS Smoke Test",
            description="本地启用 1-2 个 RSS 源进行小规模验证",
            required=False,
            local_only=True,
            cloud_safe=False,
            status="pending"
        ),
        ValidationStep(
            step_id="runtime_observation",
            name="Runtime 观察",
            description="Mac mini Runtime/LaunchAgent 观察 1-2 天",
            required=False,
            local_only=True,
            cloud_safe=False,
            status="pending"
        ),
        ValidationStep(
            step_id="data_calibration",
            name="真实数据校准",
            description="记录真实数据校准结果",
            required=False,
            local_only=True,
            cloud_safe=False,
            status="pending"
        ),
        ValidationStep(
            step_id="workbench_panel",
            name="Workbench 生产验证面板",
            description="Workbench 显示生产验证状态",
            required=True,
            local_only=False,
            cloud_safe=True,
            status="pending"
        ),
        ValidationStep(
            step_id="readiness_gate",
            name="Production Readiness Gate",
            description="评估是否可以进入真实观察",
            required=True,
            local_only=False,
            cloud_safe=True,
            status="pending"
        )
    ]
    
    # 通过/警告/阻断标准
    result.pass_criteria = [
        "所有云端 pipeline 通过",
        "Usage boundary gate 通过",
        "无 secret 入 Git",
        "无 OpenClaw 修改",
        "auto_publish 已禁用"
    ]
    
    result.warn_criteria = [
        "RSS smoke test 待本地执行",
        "Runtime 观察待本地执行",
        "真实数据校准待执行"
    ]
    
    result.block_criteria = [
        "云端 pipeline 失败",
        "Secret 泄漏检测",
        "auto_publish 已启用",
        "OpenClaw 被修改"
    ]
    
    # 统计
    result.checklist_count = len(result.validation_sequence)
    result.local_only_items = sum(1 for s in result.validation_sequence if s.local_only)
    result.cloud_safe_items = sum(1 for s in result.validation_sequence if s.cloud_safe)
    result.status = "generated"
    
    return result


def save_validation_plan(result: ValidationPlanResult, output_dir: Path) -> Dict[str, str]:
    """保存验证计划"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存 JSON
    dated_json = output_dir / f"{result.generated_at[:10].replace('-', '')}__local-production-validation-plan.json"
    latest_json = output_dir / "latest_local_production_validation_plan.json"
    
    json_data = result.to_dict()
    
    with open(dated_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    with open(latest_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    # 生成 Markdown
    md_content = _generate_validation_plan_md(result)
    
    dated_md = output_dir / f"{result.generated_at[:10].replace('-', '')}__local-production-validation-plan.md"
    latest_md = output_dir / "latest_local_production_validation_plan.md"
    
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


def _generate_validation_plan_md(result: ValidationPlanResult) -> str:
    """生成 Markdown 报告"""
    
    md = f"""# Cloud-to-Local Production Validation Plan

## 概述

- **生成时间**: {result.generated_at}
- **当前模式**: {result.mode}
- **状态**: {result.status}

## 云端已完成能力

"""
    
    for cap in result.cloud_completed_capabilities:
        md += f"- {cap}\n"
    
    md += "\n## 需要本地真实 RSS 验证的能力\n\n"
    for item in result.local_validation_required:
        md += f"- {item}\n"
    
    md += "\n## 需要 Mac mini Runtime 验证的能力\n\n"
    for item in result.runtime_validation_required:
        md += f"- {item}\n"
    
    md += "\n## 仅需 dry-run 的能力\n\n"
    for item in result.dry_run_only:
        md += f"- {item}\n"
    
    md += "\n## 验证顺序\n\n"
    md += "| Step | 名称 | 描述 | 必须 | 本地执行 | 云端安全 |\n"
    md += "|------|------|------|------|----------|----------|\n"
    
    for step in result.validation_sequence:
        md += f"| {step.step_id} | {step.name} | {step.description} | {step.required} | {step.local_only} | {step.cloud_safe} |\n"
    
    md += "\n## 通过标准\n\n"
    for criterion in result.pass_criteria:
        md += f"- ✅ {criterion}\n"
    
    md += "\n## 警告标准\n\n"
    for criterion in result.warn_criteria:
        md += f"- ⚠️ {criterion}\n"
    
    md += "\n## 阻断标准\n\n"
    for criterion in result.block_criteria:
        md += f"- ❌ {criterion}\n"
    
    md += f"""
## 统计

- **检查项总数**: {result.checklist_count}
- **本地执行项**: {result.local_only_items}
- **云端安全项**: {result.cloud_safe_items}

---

**Phase36** | Cloud-to-Local Production Validation Plan
"""
    
    return md