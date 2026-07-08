"""
P37A-005: Production Observation Dashboard
整合 readiness gate 和观察结果
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path
import json


@dataclass
class ProductionObservationDashboard:
    schema_version: str = "v1"
    generated_at: str = ""
    
    mode: str = "CLOUD_DEVELOPMENT"
    
    readiness_status: str = "ACTIONABLE"
    rss_status: str = "PENDING_LOCAL_EXECUTION"
    runtime_status: str = "PENDING_LOCAL_EXECUTION"
    
    last_observation_date: str = ""
    today_final_candidate_count: int = 0
    
    blocking_issues: List[str] = field(default_factory=list)
    warning_issues: List[str] = field(default_factory=list)
    
    next_action: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "mode": self.mode,
            "readiness_status": self.readiness_status,
            "rss_status": self.rss_status,
            "runtime_status": self.runtime_status,
            "last_observation_date": self.last_observation_date,
            "today_final_candidate_count": self.today_final_candidate_count,
            "blocking_issues": self.blocking_issues,
            "warning_issues": self.warning_issues,
            "next_action": self.next_action
        }


def build_production_observation_dashboard(
    mode: str = "CLOUD_DEVELOPMENT",
    auto_publish_enabled: bool = False,
    secret_leak_detected: bool = False,
    openclaw_modified: bool = False,
    fulltext_committed: bool = False
) -> ProductionObservationDashboard:
    """构建生产观察仪表盘"""
    
    result = ProductionObservationDashboard(
        generated_at=datetime.now().isoformat(),
        mode=mode
    )
    
    # Evaluate blocking issues first
    if auto_publish_enabled:
        result.blocking_issues.append("auto_publish 已启用，必须禁用")
        result.readiness_status = "FAIL"
    if secret_leak_detected:
        result.blocking_issues.append("RSS secret 泄漏，必须清理")
        result.readiness_status = "FAIL"
    if openclaw_modified:
        result.blocking_issues.append("OpenClaw 被修改，必须回滚")
        result.readiness_status = "FAIL"
    if fulltext_committed:
        result.blocking_issues.append("RSS 全文被提交，必须从 Git 移除")
        result.readiness_status = "FAIL"
    
    # Cloud mode defaults
    if mode == "CLOUD_DEVELOPMENT" and not result.blocking_issues:
        result.readiness_status = "ACTIONABLE"
        result.rss_status = "PENDING_LOCAL_EXECUTION"
        result.runtime_status = "PENDING_LOCAL_EXECUTION"
        result.warning_issues = [
            "RSS smoke test 待本地执行",
            "Runtime 观察待本地执行"
        ]
        result.next_action = "在本地 Mac mini 执行 Phase37B 生产验证"
    elif not result.blocking_issues:
        result.readiness_status = "PASS"
        result.rss_status = "PASS"
        result.runtime_status = "PASS"
        result.next_action = "可以进入生产观察验收"
    
    return result


def save_dashboard(result: ProductionObservationDashboard, output_dir: Path) -> Dict[str, str]:
    """保存仪表盘"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON
    dated_json = output_dir / f"{result.generated_at[:10].replace('-', '')}__production-observation-dashboard.json"
    latest_json = output_dir / "latest_production_observation_dashboard.json"
    
    json_data = result.to_dict()
    
    with open(dated_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    with open(latest_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    # Markdown
    md_content = _generate_dashboard_md(result)
    
    dated_md = output_dir / f"{result.generated_at[:10].replace('-', '')}__production-observation-dashboard.md"
    latest_md = output_dir / "latest_production_observation_dashboard.md"
    
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


def _generate_dashboard_md(dashboard: ProductionObservationDashboard) -> str:
    """生成 Markdown 仪表盘"""
    
    md = f"""# Production Observation Dashboard

## 总览

- **生成时间**: {dashboard.generated_at}
- **当前模式**: {dashboard.mode}
- **Readiness Gate**: {dashboard.readiness_status}
- **RSS Smoke**: {dashboard.rss_status}
- **Runtime 观察**: {dashboard.runtime_status}

## 关键指标

| 指标 | 值 |
|------|----|
| 最近观察日期 | {dashboard.last_observation_date or '(待本地执行)'} |
| 今日 Final Candidate | {dashboard.today_final_candidate_count} |
| 阻断性问题 | {len(dashboard.blocking_issues)} |
| 警告性问题 | {len(dashboard.warning_issues)} |

## 阻断性问题

"""
    
    if dashboard.blocking_issues:
        for issue in dashboard.blocking_issues:
            md += f"- ❌ {issue}\n"
    else:
        md += "- 无阻断性问题\n"
    
    md += "\n## 警告性问题\n\n"
    
    if dashboard.warning_issues:
        for issue in dashboard.warning_issues:
            md += f"- ⚠️ {issue}\n"
    else:
        md += "- 无警告\n"
    
    md += f"""
## 下一步

{dashboard.next_action}

---

**Phase37A** | Production Observation Dashboard
"""
    
    return md