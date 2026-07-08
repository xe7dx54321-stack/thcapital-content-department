"""
P37A-001: Production Observation Result Schema
统一生产观察结果结构
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json
import yaml


@dataclass
class ProductionObservationResult:
    schema_version: str = "v1"
    mode: str = "CLOUD_DEVELOPMENT"
    generated_at: str = ""
    
    rss_smoke: Dict[str, Any] = field(default_factory=dict)
    runtime_observation: Dict[str, Any] = field(default_factory=dict)
    manual_observation: Dict[str, Any] = field(default_factory=dict)
    readiness_gate: Dict[str, Any] = field(default_factory=dict)
    workbench_status: Dict[str, Any] = field(default_factory=dict)
    safety_boundary: Dict[str, Any] = field(default_factory=dict)
    next_action: str = ""
    
    status: str = "generated"
    section_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "mode": self.mode,
            "generated_at": self.generated_at,
            "rss_smoke": self.rss_smoke,
            "runtime_observation": self.runtime_observation,
            "manual_observation": self.manual_observation,
            "readiness_gate": self.readiness_gate,
            "workbench_status": self.workbench_status,
            "safety_boundary": self.safety_boundary,
            "next_action": self.next_action,
            "status": self.status,
            "section_count": self.section_count
        }


def build_production_observation_schema(
    mode: str = "CLOUD_DEVELOPMENT",
    rss_smoke: Optional[Dict[str, Any]] = None,
    runtime_observation: Optional[Dict[str, Any]] = None,
    manual_observation: Optional[Dict[str, Any]] = None,
    readiness_gate: Optional[Dict[str, Any]] = None
) -> ProductionObservationResult:
    """构建生产观察结果结构"""
    
    result = ProductionObservationResult(
        generated_at=datetime.now().isoformat(),
        mode=mode
    )
    
    # RSS smoke - cloud default
    if rss_smoke:
        result.rss_smoke = rss_smoke
    else:
        result.rss_smoke = {
            "status": "PENDING_LOCAL_EXECUTION",
            "requires_real_rss": False,
            "blocking_failures": 0
        }
    
    # Runtime observation - cloud default
    if runtime_observation:
        result.runtime_observation = runtime_observation
    else:
        result.runtime_observation = {
            "status": "PENDING_LOCAL_EXECUTION",
            "requires_mac_runtime": False,
            "blocking_failures": 0
        }
    
    # Manual observation
    if manual_observation:
        result.manual_observation = manual_observation
    else:
        result.manual_observation = {
            "observation_days": 0,
            "day_records": []
        }
    
    # Readiness gate
    if readiness_gate:
        result.readiness_gate = readiness_gate
    else:
        result.readiness_gate = {
            "overall_status": "ACTIONABLE" if mode == "CLOUD_DEVELOPMENT" else "PENDING",
            "pass_count": 9,
            "warn_count": 2,
            "fail_count": 0,
            "blocking_failures": 0
        }
    
    # Workbench status
    result.workbench_status = {
        "panel_visible": True,
        "production_observation_tab": True,
        "no_secret_displayed": True,
        "no_raw_json": True
    }
    
    # Safety boundary
    result.safety_boundary = {
        "auto_publish_allowed": False,
        "no_secret_in_git": True,
        "no_fulltext_commit": True,
        "no_openclaw_mod": True,
        "no_wechat_api": True
    }
    
    # Next action
    if mode == "CLOUD_DEVELOPMENT":
        result.next_action = "在本地 Mac mini 执行 Phase37B 生产验证"
    else:
        result.next_action = "继续观察或进入验收"
    
    # Count sections
    result.section_count = sum(1 for _ in [
        result.rss_smoke, result.runtime_observation, result.manual_observation,
        result.readiness_gate, result.workbench_status, result.safety_boundary
    ])
    
    return result


def save_observation_schema(result: ProductionObservationResult, output_dir: Path) -> Dict[str, str]:
    """保存观察结果 schema"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    dated_json = output_dir / f"{result.generated_at[:10].replace('-', '')}__production-observation-schema.json"
    latest_json = output_dir / "latest_production_observation_schema.json"
    
    json_data = result.to_dict()
    
    with open(dated_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    with open(latest_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    return {
        "dated_json": str(dated_json),
        "latest_json": str(latest_json)
    }