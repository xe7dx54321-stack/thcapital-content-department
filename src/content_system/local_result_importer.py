"""
P37A-007: Local Result Importer
本地执行结果导入与摘要
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json


@dataclass
class LocalResultImportSummary:
    schema_version: str = "v1"
    generated_at: str = ""
    
    status: str = "NO_LOCAL_RESULTS_FOUND"
    
    local_result_count: int = 0
    missing_file_count: int = 0
    
    rss_smoke_status: str = "NOT_FOUND"
    runtime_observation_status: str = "NOT_FOUND"
    manual_observation_days: int = 0
    readiness_status: str = "NOT_FOUND"
    
    blocking_failures: int = 0
    imported_files: List[str] = field(default_factory=list)
    missing_files: List[str] = field(default_factory=list)
    
    recommended_next_action: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "status": self.status,
            "local_result_count": self.local_result_count,
            "missing_file_count": self.missing_file_count,
            "rss_smoke_status": self.rss_smoke_status,
            "runtime_observation_status": self.runtime_observation_status,
            "manual_observation_days": self.manual_observation_days,
            "readiness_status": self.readiness_status,
            "blocking_failures": self.blocking_failures,
            "imported_files": self.imported_files,
            "missing_files": self.missing_files,
            "recommended_next_action": self.recommended_next_action
        }


def import_local_results(results_dir: Path) -> LocalResultImportSummary:
    """导入本地观察结果"""
    
    result = LocalResultImportSummary(
        generated_at=datetime.now().isoformat()
    )
    
    expected_files = [
        "latest_rss_live_smoke_result.json",
        "latest_runtime_observation_result.json",
        "latest_manual_observation_log.json",
        "latest_production_readiness_gate.json"
    ]
    
    for filename in expected_files:
        filepath = results_dir / filename
        if filepath.exists():
            result.imported_files.append(filename)
            result.local_result_count += 1
            
            # Try to parse and extract key info
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "rss_smoke" in filename or "smoke_result" in filename:
                    result.rss_smoke_status = data.get("status", "UNKNOWN")
                    if data.get("blocking_failures", 0) > 0:
                        result.blocking_failures += 1
                elif "runtime_observation" in filename:
                    result.runtime_observation_status = data.get("status", "UNKNOWN")
                    if data.get("blocking_failures", 0) > 0:
                        result.blocking_failures += 1
                elif "manual_observation" in filename:
                    result.manual_observation_days = data.get("day_slots", 0)
                elif "readiness" in filename:
                    result.readiness_status = data.get("overall_status", "UNKNOWN")
            except Exception:
                pass
        else:
            result.missing_files.append(filename)
            result.missing_file_count += 1
    
    # Determine overall status
    if result.local_result_count == 0:
        result.status = "NO_LOCAL_RESULTS_FOUND"
        result.recommended_next_action = "在本地执行后将结果文件复制到 logs 目录"
    elif result.blocking_failures > 0:
        result.status = "BLOCKING_ISSUES_FOUND"
        result.recommended_next_action = "先解决阻断性问题，再继续观察"
    elif result.local_result_count < len(expected_files):
        result.status = "PARTIAL_RESULTS_IMPORTED"
        result.recommended_next_action = "补齐缺失的结果文件后重新导入"
    else:
        result.status = "ALL_RESULTS_IMPORTED"
        result.recommended_next_action = "查看生产验证面板，准备验收"
    
    return result


def save_import_summary(result: LocalResultImportSummary, output_dir: Path) -> Dict[str, str]:
    """保存导入摘要"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON
    dated_json = output_dir / f"{result.generated_at[:10].replace('-', '')}__local-observation-import-summary.json"
    latest_json = output_dir / "latest_local_observation_import_summary.json"
    
    json_data = result.to_dict()
    
    with open(dated_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    with open(latest_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    # Markdown
    md_content = _generate_import_summary_md(result)
    
    dated_md = output_dir / f"{result.generated_at[:10].replace('-', '')}__local-observation-import-summary.md"
    latest_md = output_dir / "latest_local_observation_import_summary.md"
    
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


def _generate_import_summary_md(summary: LocalResultImportSummary) -> str:
    """生成 Markdown 导入摘要"""
    
    md = f"""# Local Result Import Summary

## 总览

- **生成时间**: {summary.generated_at}
- **状态**: {summary.status}
- **导入结果数**: {summary.local_result_count}
- **缺失文件数**: {summary.missing_file_count}
- **阻断性问题**: {summary.blocking_failures}

## 各模块状态

| 模块 | 状态 |
|------|------|
| RSS Smoke | {summary.rss_smoke_status} |
| Runtime Observation | {summary.runtime_observation_status} |
| Manual Observation Days | {summary.manual_observation_days} |
| Readiness Gate | {summary.readiness_status} |

## 已导入文件

"""
    
    if summary.imported_files:
        for f in summary.imported_files:
            md += f"- ✅ {f}\n"
    else:
        md += "- (无)\n"
    
    md += "\n## 缺失文件\n\n"
    
    if summary.missing_files:
        for f in summary.missing_files:
            md += f"- ❌ {f}\n"
    else:
        md += "- (无)\n"
    
    md += f"""
## 下一步建议

{summary.recommended_next_action}

---

**Phase37A** | Local Result Import Summary
"""
    
    return md