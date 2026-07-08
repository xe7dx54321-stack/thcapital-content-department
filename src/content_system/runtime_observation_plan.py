"""
Phase36: Runtime Observation Plan
生成 Mac mini Runtime/LaunchAgent 观察流程
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime
import json


@dataclass
class RuntimeCheckItem:
    check_id: str
    name: str
    command: str
    expected_result: str
    cloud_mode_note: str = ""


@dataclass
class RuntimeObservationPlanResult:
    schema_version: str = "v1"
    generated_at: str = ""
    
    requires_mac_runtime: bool = False
    observation_days: int = 2
    
    runtime_checks: List[RuntimeCheckItem] = field(default_factory=list)
    commands_reference: List[str] = field(default_factory=list)
    
    status: str = "plan_generated"
    step_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "requires_mac_runtime": self.requires_mac_runtime,
            "observation_days": self.observation_days,
            "runtime_checks": [
                {
                    "check_id": c.check_id,
                    "name": c.name,
                    "command": c.command,
                    "expected_result": c.expected_result,
                    "cloud_mode_note": c.cloud_mode_note
                }
                for c in self.runtime_checks
            ],
            "commands_reference": self.commands_reference,
            "status": self.status,
            "step_count": self.step_count
        }


def build_runtime_observation_plan() -> RuntimeObservationPlanResult:
    """构建 Runtime 观察计划"""
    
    result = RuntimeObservationPlanResult(
        generated_at=datetime.now().isoformat(),
        requires_mac_runtime=False,
        observation_days=2
    )
    
    result.runtime_checks = [
        RuntimeCheckItem(
            check_id="runtime_status",
            name="检查 Runtime status",
            command="python3 scripts/runtime_control.py status",
            expected_result="running_or_idle",
            cloud_mode_note="云端不要求真实 Runtime"
        ),
        RuntimeCheckItem(
            check_id="launchagent_status",
            name="检查 LaunchAgent status",
            command="launchctl list | grep thcapital",
            expected_result="loaded_or_not_required",
            cloud_mode_note="云端不要求 launchd"
        ),
        RuntimeCheckItem(
            check_id="heartbeat_age",
            name="检查 heartbeat age",
            command="检查 heartbeat 文件时间戳",
            expected_result="within_24h",
            cloud_mode_note="云端不要求真实 heartbeat"
        ),
        RuntimeCheckItem(
            check_id="next_scheduled",
            name="检查下次定时运行",
            command="检查 cron 或 launchd 配置",
            expected_result="configured",
            cloud_mode_note="云端不要求定时配置"
        ),
        RuntimeCheckItem(
            check_id="today_capture",
            name="检查今日采集任务",
            command="make phase34a-daily",
            expected_result="success",
            cloud_mode_note="云端可执行"
        ),
        RuntimeCheckItem(
            check_id="today_topic_to_article",
            name="检查今日 topic-to-article",
            command="make phase32-daily",
            expected_result="success_or_empty",
            cloud_mode_note="云端可执行"
        ),
        RuntimeCheckItem(
            check_id="today_workbench",
            name="检查今日 Workbench",
            command="make wechat-workbench",
            expected_result="visible",
            cloud_mode_note="云端可执行"
        ),
        RuntimeCheckItem(
            check_id="retry_queue",
            name="检查 retry queue",
            command="检查 retry 状态",
            expected_result="empty_or_managed",
            cloud_mode_note="云端不要求真实 queue"
        ),
        RuntimeCheckItem(
            check_id="missed_run",
            name="检查 missed-run catch-up",
            command="检查遗漏任务",
            expected_result="none_or_recovered",
            cloud_mode_note="云端不要求真实 catch-up"
        ),
        RuntimeCheckItem(
            check_id="observation_period",
            name="观察 1-2 天",
            command="每日运行 phase36-daily",
            expected_result="stable",
            cloud_mode_note="建议本地执行"
        )
    ]
    
    result.commands_reference = [
        "make runtime-go-live-validate",
        "make runtime-go-live-observation",
        "make runtime-go-live-acceptance",
        "make phase36-daily",
        "make wechat-workbench",
        "python3 scripts/runtime_control.py status",
        "python3 scripts/runtime_control.py pause",
        "python3 scripts/runtime_control.py resume"
    ]
    
    result.step_count = len(result.runtime_checks)
    result.status = "plan_generated"
    
    return result


def save_runtime_observation_plan(result: RuntimeObservationPlanResult, output_dir: Path) -> Dict[str, str]:
    """保存 Runtime 观察计划"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON
    dated_json = output_dir / f"{result.generated_at[:10].replace('-', '')}__runtime-observation-plan.json"
    latest_json = output_dir / "latest_runtime_observation_plan.json"
    
    json_data = result.to_dict()
    
    with open(dated_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    with open(latest_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    # Markdown
    md_content = _generate_runtime_observation_plan_md(result)
    
    dated_md = output_dir / f"{result.generated_at[:10].replace('-', '')}__runtime-observation-plan.md"
    latest_md = output_dir / "latest_runtime_observation_plan.md"
    
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


def _generate_runtime_observation_plan_md(result: RuntimeObservationPlanResult) -> str:
    """生成 Markdown 报告"""
    
    md = f"""# Runtime Observation Plan

## 概述

- **生成时间**: {result.generated_at}
- **需要 Mac Runtime**: {result.requires_mac_runtime}
- **观察天数**: {result.observation_days}
- **状态**: {result.status}

## Runtime 检查清单

| Check | 名称 | 命令 | 期望结果 | 云端说明 |
|-------|------|------|----------|----------|
"""
    
    for check in result.runtime_checks:
        md += f"| {check.check_id} | {check.name} | `{check.command}` | {check.expected_result} | {check.cloud_mode_note} |\n"
    
    md += "\n## 命令参考\n\n"
    for cmd in result.commands_reference:
        md += f"- `{cmd}`\n"
    
    md += f"""
## 观察流程

### 1. 启动观察

```bash
make runtime-go-live-observation
make phase36-daily
```

### 2. 每日检查

每日运行以下命令检查系统状态：

```bash
make phase34a-daily
make phase32-daily
make wechat-workbench
python3 scripts/runtime_control.py status
```

### 3. 观察期结束验收

```bash
make runtime-go-live-acceptance
```

## 统计

- **检查项总数**: {result.step_count}

---

**Phase36** | Runtime Observation Plan
"""
    
    return md