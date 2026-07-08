"""
Phase36: Validation Pipeline
运行云到本地验证流程
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime
import json
import subprocess


@dataclass
class PipelineStepResult:
    step_id: str
    name: str
    script: str
    status: str
    returncode: int
    duration_ms: int = 0
    error_message: str = ""


@dataclass
class Phase36PipelineResult:
    schema_version: str = "v1"
    generated_at: str = ""
    
    dry_run: bool = True
    cloud_mode: bool = True
    
    total_steps: int = 0
    success_steps: int = 0
    failed_steps: int = 0
    
    steps: List[PipelineStepResult] = field(default_factory=list)
    
    validation_plan_status: str = "pending"
    smoke_test_status: str = "pending"
    runtime_observation_status: str = "pending"
    calibration_status: str = "pending"
    readiness_gate_status: str = "pending"
    rollback_runbook_status: str = "pending"
    
    overall_status: str = "pending"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "dry_run": self.dry_run,
            "cloud_mode": self.cloud_mode,
            "total_steps": self.total_steps,
            "success_steps": self.success_steps,
            "failed_steps": self.failed_steps,
            "steps": [
                {
                    "step_id": s.step_id,
                    "name": s.name,
                    "script": s.script,
                    "status": s.status,
                    "returncode": s.returncode,
                    "duration_ms": s.duration_ms,
                    "error_message": s.error_message
                }
                for s in self.steps
            ],
            "validation_plan_status": self.validation_plan_status,
            "smoke_test_status": self.smoke_test_status,
            "runtime_observation_status": self.runtime_observation_status,
            "calibration_status": self.calibration_status,
            "readiness_gate_status": self.readiness_gate_status,
            "rollback_runbook_status": self.rollback_runbook_status,
            "overall_status": self.overall_status
        }


def run_phase36_validation_pipeline(dry_run: bool = True) -> Phase36PipelineResult:
    """运行 Phase36 验证 pipeline"""
    
    result = Phase36PipelineResult(
        generated_at=datetime.now().isoformat(),
        dry_run=dry_run,
        cloud_mode=True
    )
    
    steps_config = [
        ("validation_plan", "构建验证计划", "scripts/build_local_production_validation_plan.py"),
        ("smoke_test_plan", "构建 Smoke Test 计划", "scripts/build_rss_live_smoke_test_plan.py"),
        ("runtime_observation", "构建 Runtime 观察计划", "scripts/build_runtime_observation_plan.py"),
        ("calibration_checklist", "构建校准清单", "scripts/build_real_data_calibration_checklist.py"),
        ("readiness_gate", "运行 Readiness Gate", "scripts/run_production_readiness_gate.py"),
        ("rollback_runbook", "构建回滚 Runbook", "scripts/build_rollback_safety_runbook.py"),
    ]
    
    result.total_steps = len(steps_config)
    
    for step_id, name, script in steps_config:
        step_result = _run_step(step_id, name, script)
        result.steps.append(step_result)
        
        if step_result.status == "SUCCESS":
            result.success_steps += 1
        else:
            result.failed_steps += 1
        
        # 更新各模块状态
        if step_id == "validation_plan":
            result.validation_plan_status = step_result.status
        elif step_id == "smoke_test_plan":
            result.smoke_test_status = step_result.status
        elif step_id == "runtime_observation":
            result.runtime_observation_status = step_result.status
        elif step_id == "calibration_checklist":
            result.calibration_status = step_result.status
        elif step_id == "readiness_gate":
            result.readiness_gate_status = step_result.status
        elif step_id == "rollback_runbook":
            result.rollback_runbook_status = step_result.status
    
    # 整体状态
    if result.failed_steps == 0:
        result.overall_status = "SUCCESS"
    elif result.success_steps > result.failed_steps:
        result.overall_status = "PARTIAL_SUCCESS"
    else:
        result.overall_status = "FAILURE"
    
    return result


def _run_step(step_id: str, name: str, script: str) -> PipelineStepResult:
    """执行单个步骤"""
    
    start_time = datetime.now()
    
    try:
        proc = subprocess.run(
            ["python3", script],
            capture_output=True,
            text=True,
            cwd="/workspace"
        )
        
        duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        if proc.returncode == 0:
            return PipelineStepResult(
                step_id=step_id,
                name=name,
                script=script,
                status="SUCCESS",
                returncode=0,
                duration_ms=duration_ms
            )
        else:
            return PipelineStepResult(
                step_id=step_id,
                name=name,
                script=script,
                status="FAILURE",
                returncode=proc.returncode,
                duration_ms=duration_ms,
                error_message=proc.stderr[:500] if proc.stderr else ""
            )
    
    except Exception as e:
        return PipelineStepResult(
            step_id=step_id,
            name=name,
            script=script,
            status="ERROR",
            returncode=-1,
            error_message=str(e)[:500]
        )


def save_pipeline_result(result: Phase36PipelineResult, output_dir: Path) -> Dict[str, str]:
    """保存 pipeline 结果"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON
    dated_json = output_dir / f"{result.generated_at[:10].replace('-', '')}__phase36-validation-pipeline.json"
    latest_json = output_dir / "latest_phase36_validation_pipeline.json"
    
    json_data = result.to_dict()
    
    with open(dated_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    with open(latest_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    return {
        "dated_json": str(dated_json),
        "latest_json": str(latest_json)
    }