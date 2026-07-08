"""
Phase36: RSS Live Smoke Test Plan
生成真实 RSS 小规模验证流程计划
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime
import json


@dataclass
class SmokeTestStep:
    step_id: str
    name: str
    command: str
    description: str
    local_only: bool
    cloud_safe: bool
    validation_field: str = ""
    expected_result: str = ""


@dataclass
class SmokeTestPlanResult:
    schema_version: str = "v1"
    generated_at: str = ""
    
    enabled: bool = False
    requires_real_execution: bool = False
    
    max_sources: int = 2
    max_articles_per_source: int = 20
    
    env_allowlist: List[str] = field(default_factory=list)
    steps: List[SmokeTestStep] = field(default_factory=list)
    validation_fields: List[str] = field(default_factory=list)
    
    safety_rules: List[str] = field(default_factory=list)
    
    status: str = "plan_generated"
    step_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "enabled": self.enabled,
            "requires_real_execution": self.requires_real_execution,
            "max_sources": self.max_sources,
            "max_articles_per_source": self.max_articles_per_source,
            "env_allowlist": self.env_allowlist,
            "steps": [
                {
                    "step_id": s.step_id,
                    "name": s.name,
                    "command": s.command,
                    "description": s.description,
                    "local_only": s.local_only,
                    "cloud_safe": s.cloud_safe,
                    "validation_field": s.validation_field,
                    "expected_result": s.expected_result
                }
                for s in self.steps
            ],
            "validation_fields": self.validation_fields,
            "safety_rules": self.safety_rules,
            "status": self.status,
            "step_count": self.step_count
        }


def build_rss_live_smoke_plan() -> SmokeTestPlanResult:
    """构建 RSS Smoke Test 计划"""
    
    result = SmokeTestPlanResult(
        generated_at=datetime.now().isoformat(),
        enabled=False,
        requires_real_execution=False
    )
    
    result.max_sources = 2
    result.max_articles_per_source = 20
    
    result.env_allowlist = [
        "GEEKPARK_RSS_URL",
        "OFFICIAL_AI_RSS_URL"
    ]
    
    result.steps = [
        SmokeTestStep(
            step_id="enable_sources",
            name="启用 RSS 源",
            command="设置环境变量",
            description="在 .env.rss 中设置 RSS URL",
            local_only=True,
            cloud_safe=False,
            validation_field="sources_enabled",
            expected_result="1-2 sources"
        ),
        SmokeTestStep(
            step_id="validate_sources",
            name="验证 RSS 源配置",
            command="make wechat-rss-sources-validate",
            description="验证 RSS 源配置格式",
            local_only=False,
            cloud_safe=True,
            validation_field="source_validation_status",
            expected_result="PASS"
        ),
        SmokeTestStep(
            step_id="ingest",
            name="抓取 RSS 文章",
            command="make wechat-rss-ingest",
            description="抓取 RSS feed 文章",
            local_only=True,
            cloud_safe=False,
            validation_field="fetched_source_count",
            expected_result="1-2"
        ),
        SmokeTestStep(
            step_id="clean",
            name="清洗去重",
            command="make wechat-rss-clean",
            description="清洗并去重文章",
            local_only=False,
            cloud_safe=True,
            validation_field="cleaned_count",
            expected_result="<= 40"
        ),
        SmokeTestStep(
            step_id="intelligence",
            name="提取情报",
            command="make wechat-article-intelligence",
            description="从文章中提取情报",
            local_only=False,
            cloud_safe=True,
            validation_field="intelligence_article_count",
            expected_result=">= 1"
        ),
        SmokeTestStep(
            step_id="coverage",
            name="竞品覆盖分析",
            command="make competitive-coverage-analysis",
            description="分析竞品覆盖情况",
            local_only=False,
            cloud_safe=True,
            validation_field="coverage_count",
            expected_result=">= 0"
        ),
        SmokeTestStep(
            step_id="boundary",
            name="使用边界检查",
            command="make wechat-rss-usage-boundary-gate",
            description="检查使用边界合规",
            local_only=False,
            cloud_safe=True,
            validation_field="boundary_gate_status",
            expected_result="PASS"
        ),
        SmokeTestStep(
            step_id="workbench",
            name="查看 Workbench",
            command="make wechat-workbench",
            description="查看公众号情报面板",
            local_only=False,
            cloud_safe=True,
            validation_field="workbench_panel_visible",
            expected_result="true"
        ),
        SmokeTestStep(
            step_id="record",
            name="记录结果",
            command="手动记录",
            description="记录验证结果到 calibration checklist",
            local_only=True,
            cloud_safe=False,
            validation_field="record_complete",
            expected_result="true"
        )
    ]
    
    result.validation_fields = [
        "fetched_source_count",
        "article_count",
        "cleaned_count",
        "duplicate_count",
        "intelligence_article_count",
        "coverage_count",
        "style_pattern_count",
        "boundary_gate_status",
        "workbench_panel_visible"
    ]
    
    result.safety_rules = [
        "no_secret_in_output",
        "no_fulltext_in_git",
        "no_auto_publish",
        "max_2_sources",
        "max_20_articles_per_source"
    ]
    
    result.step_count = len(result.steps)
    result.status = "plan_generated"
    
    return result


def save_smoke_test_plan(result: SmokeTestPlanResult, output_dir: Path) -> Dict[str, str]:
    """保存 Smoke Test 计划"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON
    dated_json = output_dir / f"{result.generated_at[:10].replace('-', '')}__rss-live-smoke-test-plan.json"
    latest_json = output_dir / "latest_rss_live_smoke_test_plan.json"
    
    json_data = result.to_dict()
    
    with open(dated_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    with open(latest_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    # Markdown
    md_content = _generate_smoke_test_plan_md(result)
    
    dated_md = output_dir / f"{result.generated_at[:10].replace('-', '')}__rss-live-smoke-test-plan.md"
    latest_md = output_dir / "latest_rss_live_smoke_test_plan.md"
    
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


def _generate_smoke_test_plan_md(result: SmokeTestPlanResult) -> str:
    """生成 Markdown 报告"""
    
    md = f"""# RSS Live Smoke Test Plan

## 概述

- **生成时间**: {result.generated_at}
- **启用状态**: {result.enabled}
- **需要真实执行**: {result.requires_real_execution}
- **状态**: {result.status}

## 配置限制

| 参数 | 值 | 说明 |
|------|---|------|
| `max_sources` | {result.max_sources} | 最多启用 RSS 源数 |
| `max_articles_per_source` | {result.max_articles_per_source} | 每源最多文章数 |

## 环境变量白名单

"""
    
    for env in result.env_allowlist:
        md += f"- `{env}`\n"
    
    md += "\n## Smoke Test 步骤\n\n"
    md += "| Step | 名称 | 命令 | 本地执行 | 云端安全 | 验证字段 |\n"
    md += "|------|------|------|----------|----------|----------|\n"
    
    for step in result.steps:
        md += f"| {step.step_id} | {step.name} | `{step.command}` | {step.local_only} | {step.cloud_safe} | {step.validation_field} |\n"
    
    md += "\n## 验证字段\n\n"
    md += "| 字段 | 说明 |\n"
    md += "|------|------|\n"
    
    field_descriptions = {
        "fetched_source_count": "抓取的 RSS 源数量",
        "article_count": "抓取的文章总数",
        "cleaned_count": "清洗后的文章数",
        "duplicate_count": "去重的文章数",
        "intelligence_article_count": "提取情报的文章数",
        "coverage_count": "竞品覆盖分析数",
        "style_pattern_count": "风格 pattern 数",
        "boundary_gate_status": "使用边界 gate 状态",
        "workbench_panel_visible": "Workbench 面板是否可见"
    }
    
    for field in result.validation_fields:
        desc = field_descriptions.get(field, field)
        md += f"| `{field}` | {desc} |\n"
    
    md += "\n## 安全规则\n\n"
    for rule in result.safety_rules:
        md += f"- {rule}\n"
    
    md += f"""
## 统计

- **步骤总数**: {result.step_count}

---

**Phase36** | RSS Live Smoke Test Plan
"""
    
    return md