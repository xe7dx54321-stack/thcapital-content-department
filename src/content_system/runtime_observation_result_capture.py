"""
P37A-003: Runtime Observation Result Capture
Runtime 观察结果记录能力
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path
import json


@dataclass
class RuntimeObservationResult:
    schema_version: str = "v1"
    generated_at: str = ""
    
    status: str = "PENDING_LOCAL_EXECUTION"
    requires_mac_runtime: bool = False
    blocking_failures: int = 0
    
    runtime_status: str = "PENDING_LOCAL"
    launchagent_status: str = "PENDING_LOCAL"
    heartbeat_age_seconds: int = 0
    next_scheduled_run: str = "PENDING_LOCAL"
    today_jobs_success: int = 0
    today_jobs_failed: int = 0
    retry_queue_count: int = 0
    missed_run_catchup_count: int = 0
    final_candidate_count: int = 0
    workbench_visible: bool = True
    observation_days: int = 0
    
    observation_checks: List[str] = field(default_factory=list)
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "status": self.status,
            "requires_mac_runtime": self.requires_mac_runtime,
            "blocking_failures": self.blocking_failures,
            "runtime_status": self.runtime_status,
            "launchagent_status": self.launchagent_status,
            "heartbeat_age_seconds": self.heartbeat_age_seconds,
            "next_scheduled_run": self.next_scheduled_run,
            "today_jobs_success": self.today_jobs_success,
            "today_jobs_failed": self.today_jobs_failed,
            "retry_queue_count": self.retry_queue_count,
            "missed_run_catchup_count": self.missed_run_catchup_count,
            "final_candidate_count": self.final_candidate_count,
            "workbench_visible": self.workbench_visible,
            "observation_days": self.observation_days,
            "observation_checks": self.observation_checks,
            "notes": self.notes
        }


def build_runtime_observation_result(
    cloud_mode: bool = True,
    observation_days: int = 0
) -> RuntimeObservationResult:
    """构建 Runtime 观察结果"""
    
    result = RuntimeObservationResult(
        generated_at=datetime.now().isoformat()
    )
    
    if cloud_mode:
        result.status = "PENDING_LOCAL_EXECUTION"
        result.requires_mac_runtime = False
        result.blocking_failures = 0
    else:
        result.requires_mac_runtime = True
        result.observation_days = observation_days
        # Evaluate status
        if result.today_jobs_failed > 3:
            result.status = "FAIL"
            result.blocking_failures = 1
        elif observation_days >= 2 and result.final_candidate_count > 0:
            result.status = "PASS"
            result.blocking_failures = 0
        else:
            result.status = "IN_PROGRESS"
            result.blocking_failures = 0
    
    result.observation_checks = [
        "runtime_status_check",
        "launchagent_status_check",
        "heartbeat_age_check",
        "next_scheduled_check",
        "today_jobs_check",
        "retry_queue_check",
        "missed_run_check",
        "workbench_check"
    ]
    
    return result


def save_runtime_observation_result(result: RuntimeObservationResult, output_dir: Path) -> Dict[str, str]:
    """保存 Runtime 观察结果"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    dated_json = output_dir / f"{result.generated_at[:10].replace('-', '')}__runtime-observation-result.json"
    latest_json = output_dir / "latest_runtime_observation_result.json"
    
    json_data = result.to_dict()
    
    with open(dated_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    with open(latest_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    return {
        "dated_json": str(dated_json),
        "latest_json": str(latest_json)
    }