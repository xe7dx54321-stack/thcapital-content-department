"""
P37A-002: RSS Smoke Result Capture
RSS smoke 结果记录能力
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path
import json


@dataclass
class RssSmokeResult:
    schema_version: str = "v1"
    generated_at: str = ""
    
    status: str = "PENDING_LOCAL_EXECUTION"
    requires_real_rss: bool = False
    blocking_failures: int = 0
    
    enabled_source_count: int = 0
    fetched_source_count: int = 0
    article_count: int = 0
    cleaned_count: int = 0
    duplicate_count: int = 0
    intelligence_article_count: int = 0
    competitive_coverage_count: int = 0
    style_pattern_count: int = 0
    boundary_gate_status: str = "PASS"
    workbench_panel_visible: bool = True
    secret_leak_count: int = 0
    fulltext_committed_count: int = 0
    
    safety_checks: List[str] = field(default_factory=list)
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "status": self.status,
            "requires_real_rss": self.requires_real_rss,
            "blocking_failures": self.blocking_failures,
            "enabled_source_count": self.enabled_source_count,
            "fetched_source_count": self.fetched_source_count,
            "article_count": self.article_count,
            "cleaned_count": self.cleaned_count,
            "duplicate_count": self.duplicate_count,
            "intelligence_article_count": self.intelligence_article_count,
            "competitive_coverage_count": self.competitive_coverage_count,
            "style_pattern_count": self.style_pattern_count,
            "boundary_gate_status": self.boundary_gate_status,
            "workbench_panel_visible": self.workbench_panel_visible,
            "secret_leak_count": self.secret_leak_count,
            "fulltext_committed_count": self.fulltext_committed_count,
            "safety_checks": self.safety_checks,
            "notes": self.notes
        }


def build_rss_smoke_result(
    cloud_mode: bool = True,
    enabled_source_count: int = 0,
    article_count: int = 0
) -> RssSmokeResult:
    """构建 RSS smoke 结果"""
    
    result = RssSmokeResult(
        generated_at=datetime.now().isoformat()
    )
    
    if cloud_mode:
        result.status = "PENDING_LOCAL_EXECUTION"
        result.requires_real_rss = False
        result.blocking_failures = 0
    else:
        result.enabled_source_count = enabled_source_count
        result.article_count = article_count
        result.requires_real_rss = True
        # Evaluate status
        if result.secret_leak_count > 0 or result.fulltext_committed_count > 0:
            result.status = "FAIL"
            result.blocking_failures = 1
        elif article_count > 0:
            result.status = "PASS"
            result.blocking_failures = 0
        else:
            result.status = "ACTIONABLE"
            result.blocking_failures = 0
    
    result.safety_checks = [
        "no_secret_in_output",
        "no_fulltext_in_git",
        "no_auto_publish",
        "max_2_sources",
        "max_20_articles_per_source"
    ]
    
    return result


def save_rss_smoke_result(result: RssSmokeResult, output_dir: Path) -> Dict[str, str]:
    """保存 RSS smoke 结果"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    dated_json = output_dir / f"{result.generated_at[:10].replace('-', '')}__rss-smoke-result-capture.json"
    latest_json = output_dir / "latest_rss_smoke_result_capture.json"
    
    json_data = result.to_dict()
    
    with open(dated_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    with open(latest_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    return {
        "dated_json": str(dated_json),
        "latest_json": str(latest_json)
    }