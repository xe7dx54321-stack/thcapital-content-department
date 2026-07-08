"""
P37A: Phase37A Observation Pipeline
运行生产观察 pipeline
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
    error_message: str = ""


@dataclass
class Phase37APipelineResult:
    schema_version: str = "v1"
    generated_at: str = ""
    
    dry_run: bool = True
    cloud_mode: bool = True
    
    total_steps: int = 0
    success_steps: int = 0
    failed_steps: int = 0
    
    steps: List[PipelineStepResult] = field(default_factory=list)
    
    schema_status: str = "pending"
    rss_smoke_status: str = "pending"
    runtime_status: str = "pending"
    manual_log_status: str = "pending"
    dashboard_status: str = "pending"
    import_status: str = "pending"
    
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
                    "error_message": s.error_message
                }
                for s in self.steps
            ],
            "schema_status": self.schema_status,
            "rss_smoke_status": self.rss_smoke_status,
            "runtime_status": self.runtime_status,
            "manual_log_status": self.manual_log_status,
            "dashboard_status": self.dashboard_status,
            "import_status": self.import_status,
            "overall_status": self.overall_status
        }


def run_phase37a_pipeline(dry_run: bool = True) -> Phase37APipelineResult:
    """运行 Phase37A 观察 pipeline"""
    
    result = Phase37APipelineResult(
        generated_at=datetime.now().isoformat(),
        dry_run=dry_run,
        cloud_mode=True
    )
    
    steps_config = [
        ("schema", "生成观察结果Schema", "scripts/build_production_observation_schema.py"),
        ("rss_smoke", "RSS Smoke结果记录", "scripts/capture_rss_smoke_result.py"),
        ("runtime_observation", "Runtime观察结果记录", "scripts/capture_runtime_observation_result.py"),
        ("manual_log", "生成人工观察日志", "scripts/build_manual_observation_log.py"),
        ("dashboard", "构建生产观察仪表盘", "scripts/build_production_observation_dashboard.py"),
        ("import_summary", "本地结果导入摘要", "scripts/import_local_observation_results.py"),
    ]
    
    result.total_steps = len(steps_config)
    
    for step_id, name, script in steps_config:
        step_result = _run_step(step_id, name, script)
        result.steps.append(step_result)
        
        if step_result.status == "SUCCESS":
            result.success_steps += 1
        else:
            result.failed_steps += 1
        
        # Update module statuses
        if step_id == "schema":
            result.schema_status = step_result.status
        elif step_id == "rss_smoke":
            result.rss_smoke_status = step_result.status
        elif step_id == "runtime_observation":
            result.runtime_status = step_result.status
        elif step_id == "manual_log":
            result.manual_log_status = step_result.status
        elif step_id == "dashboard":
            result.dashboard_status = step_result.status
        elif step_id == "import_summary":
            result.import_status = step_result.status
    
    # Overall status
    if result.failed_steps == 0:
        result.overall_status = "SUCCESS"
    elif result.success_steps > result.failed_steps:
        result.overall_status = "PARTIAL_SUCCESS"
    else:
        result.overall_status = "FAILURE"
    
    return result


def _run_step(step_id: str, name: str, script: str) -> PipelineStepResult:
    """执行单个步骤"""
    
    try:
        proc = subprocess.run(
            ["python3", script],
            capture_output=True,
            text=True,
            cwd="/workspace"
        )
        
        if proc.returncode == 0:
            return PipelineStepResult(
                step_id=step_id,
                name=name,
                script=script,
                status="SUCCESS",
                returncode=0
            )
        else:
            return PipelineStepResult(
                step_id=step_id,
                name=name,
                script=script,
                status="FAILURE",
                returncode=proc.returncode,
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


def save_pipeline_result(result: Phase37APipelineResult, output_dir: Path) -> Dict[str, str]:
    """保存 pipeline 结果"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    dated_json = output_dir / f"{result.generated_at[:10].replace('-', '')}__phase37a-observation-pipeline.json"
    latest_json = output_dir / "latest_phase37a_observation_pipeline.json"
    
    json_data = result.to_dict()
    
    with open(dated_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    with open(latest_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    return {
        "dated_json": str(dated_json),
        "latest_json": str(latest_json)
    }