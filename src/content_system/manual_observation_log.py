"""
P37A-004: Manual Observation Log
1-2天人工观察记录模板
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime, timedelta
from pathlib import Path
import json


@dataclass
class DailyObservationRecord:
    date: str = ""
    workbench_openable: bool = True
    runtime_heartbeat_normal: bool = True
    today_final_candidate_count: int = 0
    main_topic_duplicate_free: bool = True
    has_differentiated_angle: bool = True
    title_like_wechat: bool = True
    ai_taste_noticeable: bool = False
    evidence_needs_confirmation: bool = False
    article_worth_editing: bool = True
    recommend_publish: bool = False
    main_issues: str = ""
    calibration_items: str = ""


@dataclass
class ManualObservationLog:
    schema_version: str = "v1"
    generated_at: str = ""
    
    day_slots: int = 2
    day_records: List[DailyObservationRecord] = field(default_factory=list)
    
    checklist_count: int = 0
    status: str = "template_generated"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "day_slots": self.day_slots,
            "day_records": [
                {
                    "date": r.date,
                    "workbench_openable": r.workbench_openable,
                    "runtime_heartbeat_normal": r.runtime_heartbeat_normal,
                    "today_final_candidate_count": r.today_final_candidate_count,
                    "main_topic_duplicate_free": r.main_topic_duplicate_free,
                    "has_differentiated_angle": r.has_differentiated_angle,
                    "title_like_wechat": r.title_like_wechat,
                    "ai_taste_noticeable": r.ai_taste_noticeable,
                    "evidence_needs_confirmation": r.evidence_needs_confirmation,
                    "article_worth_editing": r.article_worth_editing,
                    "recommend_publish": r.recommend_publish,
                    "main_issues": r.main_issues,
                    "calibration_items": r.calibration_items
                }
                for r in self.day_records
            ],
            "checklist_count": self.checklist_count,
            "status": self.status
        }


def build_manual_observation_log(day_slots: int = 2) -> ManualObservationLog:
    """构建人工观察日志模板"""
    
    result = ManualObservationLog(
        generated_at=datetime.now().isoformat(),
        day_slots=day_slots
    )
    
    # Generate empty day record templates
    today = datetime.now().date()
    for i in range(day_slots):
        date_str = (today + timedelta(days=i)).isoformat()
        record = DailyObservationRecord(date=date_str)
        result.day_records.append(record)
    
    # Count checklist items per day
    per_day_checks = 11  # boolean items per day
    result.checklist_count = len(result.day_records) * per_day_checks
    result.status = "template_generated"
    
    return result


def save_manual_observation_log(result: ManualObservationLog, output_dir: Path) -> Dict[str, str]:
    """保存人工观察日志"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON
    dated_json = output_dir / f"{result.generated_at[:10].replace('-', '')}__manual-observation-log.json"
    latest_json = output_dir / "latest_manual_observation_log.json"
    
    json_data = result.to_dict()
    
    with open(dated_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    with open(latest_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    # Markdown
    md_content = _generate_manual_observation_md(result)
    
    dated_md = output_dir / f"{result.generated_at[:10].replace('-', '')}__manual-observation-log.md"
    latest_md = output_dir / "latest_manual_observation_log.md"
    
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


def _generate_manual_observation_md(log: ManualObservationLog) -> str:
    """生成 Markdown 观察日志"""
    
    md = f"""# Manual Observation Log

## 概述

- **生成时间**: {log.generated_at}
- **观察天数槽位**: {log.day_slots}
- **每日检查项**: {int(log.checklist_count / max(log.day_slots, 1))}
- **状态**: {log.status}

---

"""
    
    for i, record in enumerate(log.day_records, 1):
        md += f"## 第 {i} 天 ({record.date})\n\n"
        md += f"""
### 系统状态

- [ ] Workbench 可打开: {record.workbench_openable}
- [ ] Runtime heartbeat 正常: {record.runtime_heartbeat_normal}
- [ ] 今日 final candidate 数量: {record.today_final_candidate_count}

### 内容质量

- [ ] 主选题无重复: {record.main_topic_duplicate_free}
- [ ] 有差异化角度: {record.has_differentiated_angle}
- [ ] 标题像公众号标题: {record.title_like_wechat}
- [ ] AI 味不明显: {not record.ai_taste_noticeable}
- [ ] 证据不需要人工确认: {not record.evidence_needs_confirmation}

### 发布判断

- [ ] 稿件值得人工修改: {record.article_worth_editing}
- [ ] 建议发布: {record.recommend_publish}

### 备注

**主要问题**: {record.main_issues if record.main_issues else "(待填写)"}

**建议校准项**: {record.calibration_items if record.calibration_items else "(待填写)"}

---

"""
    
    md += """
## 使用说明

1. 每天运行 `make phase37a-daily` 和 `make wechat-workbench`
2. 打开 Workbench 查看生产验证面板
3. 逐项填写检查项
4. 记录主要问题和校准建议
5. 观察期结束后汇总到 Closeout Report

---

**Phase37A** | Manual Observation Log
"""
    
    return md