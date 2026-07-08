"""
Phase36: Real Data Calibration Checklist
生成真实数据校准清单
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime
import json


@dataclass
class CalibrationCheckItem:
    item_id: str
    category: str
    name: str
    observation_question: str
    pass_criteria: str
    fail_indication: str
    record_field: str
    calibration_notes: str = ""


@dataclass
class CalibrationChecklistResult:
    schema_version: str = "v1"
    generated_at: str = ""
    
    checklist_items: List[CalibrationCheckItem] = field(default_factory=list)
    
    rss_items: List[str] = field(default_factory=list)
    topic_items: List[str] = field(default_factory=list)
    editorial_items: List[str] = field(default_factory=list)
    workbench_items: List[str] = field(default_factory=list)
    
    status: str = "checklist_generated"
    checklist_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "checklist_items": [
                {
                    "item_id": i.item_id,
                    "category": i.category,
                    "name": i.name,
                    "observation_question": i.observation_question,
                    "pass_criteria": i.pass_criteria,
                    "fail_indication": i.fail_indication,
                    "record_field": i.record_field,
                    "calibration_notes": i.calibration_notes
                }
                for i in self.checklist_items
            ],
            "rss_items": self.rss_items,
            "topic_items": self.topic_items,
            "editorial_items": self.editorial_items,
            "workbench_items": self.workbench_items,
            "status": self.status,
            "checklist_count": self.checklist_count
        }


def build_real_data_calibration_checklist() -> CalibrationChecklistResult:
    """构建真实数据校准清单"""
    
    result = CalibrationChecklistResult(
        generated_at=datetime.now().isoformat()
    )
    
    result.checklist_items = [
        # RSS 相关
        CalibrationCheckItem(
            item_id="rss_stability",
            category="RSS",
            name="RSS ingest 稳定性",
            observation_question="RSS 抓取是否稳定运行？",
            pass_criteria="连续 3 次成功，无超时或错误",
            fail_indication="频繁超时、失败、或返回空",
            record_field="rss_ingest_success_rate",
            calibration_notes="可调整 timeout 和 retry 参数"
        ),
        CalibrationCheckItem(
            item_id="rss_clean_quality",
            category="RSS",
            name="正文清洗质量",
            observation_question="清洗后的正文是否干净？",
            pass_criteria="无明显 HTML 残留、广告、乱码",
            fail_indication="正文含 HTML tag、广告文字、截断",
            record_field="clean_quality_score",
            calibration_notes="可调整清洗规则"
        ),
        CalibrationCheckItem(
            item_id="rss_duplicate",
            category="RSS",
            name="去重有效性",
            observation_question="去重是否有效减少重复？",
            pass_criteria="重复文章 < 5%",
            fail_indication="重复文章 > 20%",
            record_field="duplicate_rate",
            calibration_notes="可调整去重阈值"
        ),
        CalibrationCheckItem(
            item_id="rss_intelligence",
            category="RSS",
            name="情报抽取准确性",
            observation_question="情报抽取是否准确？",
            pass_criteria="核心信息提取正确，无幻觉",
            fail_indication="关键信息遗漏或错误",
            record_field="intelligence_accuracy",
            calibration_notes="可调整 LLM prompt"
        ),
        CalibrationCheckItem(
            item_id="rss_coverage",
            category="RSS",
            name="竞品覆盖价值",
            observation_question="竞品覆盖分析是否有价值？",
            pass_criteria="能识别竞品角度和空白",
            fail_indication="分析空洞或无效",
            record_field="coverage_value_score",
            calibration_notes="可调整覆盖分析规则"
        ),
        # Topic 相关
        CalibrationCheckItem(
            item_id="topic_diversity",
            category="Topic",
            name="选题去重效果",
            observation_question="选题去重是否减少重复？",
            pass_criteria="同日选题相似度 < 0.7",
            fail_indication="同日选题高度相似",
            record_field="topic_similarity_avg",
            calibration_notes="可调整相似度阈值"
        ),
        CalibrationCheckItem(
            item_id="topic_differentiated",
            category="Topic",
            name="差异化角度可用性",
            observation_question="差异化角度推荐是否可用？",
            pass_criteria="推荐角度有实质差异",
            fail_indication="推荐角度雷同或空洞",
            record_field="differentiated_angle_count",
            calibration_notes="可调整角度推荐规则"
        ),
        # Editorial 相关
        CalibrationCheckItem(
            item_id="title_quality",
            category="Editorial",
            name="标题生成质量",
            observation_question="标题是否更像公众号标题？",
            pass_criteria="标题符合长度、角度、价值要求",
            fail_indication="标题过长、营销号风格、空洞",
            record_field="title_quality_avg",
            calibration_notes="可调整标题生成规则"
        ),
        CalibrationCheckItem(
            item_id="ai_taste_effect",
            category="Editorial",
            name="AI 味拦截效果",
            observation_question="AI 味拦截是否有效？",
            pass_criteria="拦截 > 70% discouraged phrases",
            fail_indication="大量 AI 味表达未拦截",
            record_field="ai_taste_hit_rate",
            calibration_notes="可扩展 discouraged phrase 列表"
        ),
        CalibrationCheckItem(
            item_id="style_score_match",
            category="Editorial",
            name="Draft style score 符合直觉",
            observation_question="Draft style score 是否符合人工直觉？",
            pass_criteria="高/低分稿件人工判断一致",
            fail_indication="评分与人工判断相反",
            record_field="style_score_match_rate",
            calibration_notes="可调整评分权重"
        ),
        CalibrationCheckItem(
            item_id="version_gate",
            category="Editorial",
            name="Version comparison 防退化",
            observation_question="Version comparison 是否防止退化？",
            pass_criteria="改写退化时 reject",
            fail_indication="退化改写被 accept",
            record_field="version_gate_accuracy",
            calibration_notes="可调整退化检测阈值"
        ),
        # Workbench 相关
        CalibrationCheckItem(
            item_id="workbench_clarity",
            category="Workbench",
            name="Workbench 清晰度",
            observation_question="Workbench 是否清晰呈现状态？",
            pass_criteria="状态一目了然，无 raw JSON",
            fail_indication="信息混乱或显示 raw JSON",
            record_field="workbench_clarity_score",
            calibration_notes="可调整 Workbench 展示逻辑"
        ),
        CalibrationCheckItem(
            item_id="workbench_production",
            category="Workbench",
            name="生产验证面板",
            observation_question="生产验证面板是否可用？",
            pass_criteria="显示正确状态，无 secret",
            fail_indication="显示错误状态或 secret",
            record_field="production_panel_visible",
            calibration_notes="确保不显示敏感信息"
        )
    ]
    
    # 分类
    result.rss_items = [i.item_id for i in result.checklist_items if i.category == "RSS"]
    result.topic_items = [i.item_id for i in result.checklist_items if i.category == "Topic"]
    result.editorial_items = [i.item_id for i in result.checklist_items if i.category == "Editorial"]
    result.workbench_items = [i.item_id for i in result.checklist_items if i.category == "Workbench"]
    
    result.checklist_count = len(result.checklist_items)
    result.status = "checklist_generated"
    
    return result


def save_calibration_checklist(result: CalibrationChecklistResult, output_dir: Path) -> Dict[str, str]:
    """保存校准清单"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON
    dated_json = output_dir / f"{result.generated_at[:10].replace('-', '')}__real-data-calibration-checklist.json"
    latest_json = output_dir / "latest_real_data_calibration_checklist.json"
    
    json_data = result.to_dict()
    
    with open(dated_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    with open(latest_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    # Markdown
    md_content = _generate_calibration_checklist_md(result)
    
    dated_md = output_dir / f"{result.generated_at[:10].replace('-', '')}__real-data-calibration-checklist.md"
    latest_md = output_dir / "latest_real_data_calibration_checklist.md"
    
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


def _generate_calibration_checklist_md(result: CalibrationChecklistResult) -> str:
    """生成 Markdown 报告"""
    
    md = f"""# Real Data Calibration Checklist

## 概述

- **生成时间**: {result.generated_at}
- **状态**: {result.status}
- **清单项总数**: {result.checklist_count}

## RSS 相关 ({len(result.rss_items)} 项)

| ID | 名称 | 观察问题 | 通过标准 | 失败表现 | 记录字段 |
|----|------|----------|----------|----------|----------|
"""
    
    for item in result.checklist_items:
        if item.category == "RSS":
            md += f"| {item.item_id} | {item.name} | {item.observation_question} | {item.pass_criteria} | {item.fail_indication} | `{item.record_field}` |\n"
    
    md += f"""
## Topic 相关 ({len(result.topic_items)} 项)

| ID | 名称 | 观察问题 | 通过标准 | 失败表现 | 记录字段 |
|----|------|----------|----------|----------|----------|
"""
    
    for item in result.checklist_items:
        if item.category == "Topic":
            md += f"| {item.item_id} | {item.name} | {item.observation_question} | {item.pass_criteria} | {item.fail_indication} | `{item.record_field}` |\n"
    
    md += f"""
## Editorial 相关 ({len(result.editorial_items)} 项)

| ID | 名称 | 观察问题 | 通过标准 | 失败表现 | 记录字段 |
|----|------|----------|----------|----------|----------|
"""
    
    for item in result.checklist_items:
        if item.category == "Editorial":
            md += f"| {item.item_id} | {item.name} | {item.observation_question} | {item.pass_criteria} | {item.fail_indication} | `{item.record_field}` |\n"
    
    md += f"""
## Workbench 相关 ({len(result.workbench_items)} 项)

| ID | 名称 | 观察问题 | 通过标准 | 失败表现 | 记录字段 |
|----|------|----------|----------|----------|----------|
"""
    
    for item in result.checklist_items:
        if item.category == "Workbench":
            md += f"| {item.item_id} | {item.name} | {item.observation_question} | {item.pass_criteria} | {item.fail_indication} | `{item.record_field}` |\n"
    
    md += """
## 记录模板

建议使用以下格式记录校准结果：

```json
{
  "date": "YYYY-MM-DD",
  "calibration_records": [
    {
      "item_id": "xxx",
      "result": "PASS/WARN/FAIL",
      "value": "实际值",
      "notes": "备注"
    }
  ]
}
```

---

**Phase36** | Real Data Calibration Checklist
"""
    
    return md