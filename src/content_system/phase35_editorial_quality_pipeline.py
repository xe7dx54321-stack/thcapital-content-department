import json
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from .editorial_style_guide import validate_editorial_style_guide
from .narrative_frameworks import validate_narrative_frameworks
from .topic_framework_selector import select_topic_framework, FrameworkSelectionResult
from .title_generator import generate_title_candidates, TitleGenerationResult
from .opening_hook_guidance import generate_opening_hook, OpeningHookGuidance
from .ai_taste_guard import detect_ai_taste, AITasteGuardResult
from .draft_style_quality_scorer import score_draft_quality, DraftStyleQualityResult
from .version_comparison_gate import compare_versions, VersionComparisonResult


@dataclass
class PipelineStep:
    name: str
    script: str
    status: str
    returncode: int

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Phase35PipelineResult:
    status: str
    run_date: str
    style_guide_valid: bool
    frameworks_valid: bool
    framework_count: int
    title_candidate_count: int
    compliant_title_count: int
    ai_taste_passed: bool
    draft_style_score: float
    draft_style_grade: str
    version_gate_decision: str
    steps: List[PipelineStep]
    outputs: Dict

    def to_dict(self) -> Dict:
        return {
            "status": self.status,
            "run_date": self.run_date,
            "style_guide_valid": self.style_guide_valid,
            "frameworks_valid": self.frameworks_valid,
            "framework_count": self.framework_count,
            "title_candidate_count": self.title_candidate_count,
            "compliant_title_count": self.compliant_title_count,
            "ai_taste_passed": self.ai_taste_passed,
            "draft_style_score": self.draft_style_score,
            "draft_style_grade": self.draft_style_grade,
            "version_gate_decision": self.version_gate_decision,
            "steps": [s.to_dict() for s in self.steps],
            "outputs": self.outputs,
        }


class Phase35EditorialQualityPipeline:
    def __init__(self):
        self.logs_root = self._get_logs_root()
        self.run_date = self._get_run_date()

    def _get_logs_root(self) -> str:
        candidates = [
            "同行资本市场内容系统/10_logs",
            os.path.join(os.path.dirname(__file__), "..", "..", "同行资本市场内容系统", "10_logs"),
        ]
        for candidate in candidates:
            if os.path.exists(candidate):
                return candidate
        return "/tmp/logs"

    def _get_run_date(self) -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d")

    def _save_json(self, data: Dict, filename_prefix: str) -> str:
        dated_path = os.path.join(self.logs_root, f"{self.run_date}__{filename_prefix}.json")
        latest_path = os.path.join(self.logs_root, f"latest_{filename_prefix.replace('-', '_')}.json")

        os.makedirs(self.logs_root, exist_ok=True)

        with open(dated_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        with open(latest_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return dated_path

    def run_pipeline(
        self,
        topic_id: str = "topic_001",
        topic_title: str = "AI芯片市场格局变化",
        topic_type: str = "news_event",
        angle_type: str = "产业影响",
        draft_text: str = "AI芯片市场正在发生深刻变化。NVIDIA发布了新的GPU产品，这对整个AI芯片产业产生了重大影响。",
        original_version: str = "AI芯片市场正在发生深刻变化。值得关注的是，这一趋势未来可期。",
        new_version: str = "AI芯片市场正在发生深刻变化。根据最新数据，NVIDIA发布新GPU，我们认为这重新定义了AI芯片竞争格局，关键在于其性能提升幅度超过市场预期。这对投资者意味着实际的配置调整机会，但需要注意供应链风险。",
    ) -> Phase35PipelineResult:
        steps: List[PipelineStep] = []
        outputs: Dict = {}

        try:
            style_guide_result = validate_editorial_style_guide()
            steps.append(PipelineStep("validate_editorial_style_guide", "validate_editorial_style_guide.py", "OK", 0))
            outputs["style_guide_validation"] = style_guide_result
            self._save_json(style_guide_result, "editorial-style-guide-validation")
            style_guide_valid = style_guide_result.get("valid", False)
        except Exception as e:
            steps.append(PipelineStep("validate_editorial_style_guide", "validate_editorial_style_guide.py", "FAILED", 1))
            style_guide_valid = False

        try:
            frameworks_result = validate_narrative_frameworks()
            steps.append(PipelineStep("validate_narrative_frameworks", "validate_narrative_frameworks.py", "OK", 0))
            outputs["frameworks_validation"] = frameworks_result
            self._save_json(frameworks_result, "narrative-frameworks-validation")
            frameworks_valid = frameworks_result.get("valid", False)
            framework_count = frameworks_result.get("framework_count", 0)
        except Exception as e:
            steps.append(PipelineStep("validate_narrative_frameworks", "validate_narrative_frameworks.py", "FAILED", 1))
            frameworks_valid = False
            framework_count = 0

        try:
            framework_selection = select_topic_framework(
                topic_id=topic_id,
                topic_type=topic_type,
                angle_type=angle_type,
            )
            steps.append(PipelineStep("select_topic_framework", "select_topic_narrative_framework.py", "OK", 0))
            outputs["framework_selection"] = framework_selection.to_dict()
            self._save_json(framework_selection.to_dict(), "topic-framework-selection")
        except Exception as e:
            steps.append(PipelineStep("select_topic_framework", "select_topic_narrative_framework.py", "FAILED", 1))

        try:
            title_result = generate_title_candidates(topic_title=topic_title)
            steps.append(PipelineStep("generate_editorial_titles", "generate_editorial_titles.py", "OK", 0))
            outputs["title_generation"] = title_result.to_dict()
            self._save_json(title_result.to_dict(), "editorial-title-candidates")
            title_candidate_count = title_result.compliant_count
            compliant_title_count = title_result.compliant_count
        except Exception as e:
            steps.append(PipelineStep("generate_editorial_titles", "generate_editorial_titles.py", "FAILED", 1))
            title_candidate_count = 0
            compliant_title_count = 0

        try:
            framework_name = framework_selection.selected_framework.name if framework_selection.selected_framework else None
            opening_guidance = generate_opening_hook(topic_title=topic_title, framework_name=framework_name)
            steps.append(PipelineStep("generate_opening_hook", "generate_opening_hook_guidance.py", "OK", 0))
            outputs["opening_hook"] = opening_guidance.to_dict()
            self._save_json(opening_guidance.to_dict(), "opening-hook-guidance")
        except Exception as e:
            steps.append(PipelineStep("generate_opening_hook", "generate_opening_hook_guidance.py", "FAILED", 1))

        try:
            ai_taste_result = detect_ai_taste(draft_text)
            steps.append(PipelineStep("run_ai_taste_guard", "run_ai_taste_guard.py", "OK", 0))
            outputs["ai_taste_guard"] = ai_taste_result.to_dict()
            self._save_json(ai_taste_result.to_dict(), "ai-taste-guard")
            ai_taste_passed = ai_taste_result.ai_taste_score >= 0.6
        except Exception as e:
            steps.append(PipelineStep("run_ai_taste_guard", "run_ai_taste_guard.py", "FAILED", 1))
            ai_taste_passed = False

        try:
            draft_score_result = score_draft_quality(draft_text=draft_text)
            steps.append(PipelineStep("score_draft_style_quality", "score_draft_style_quality.py", "OK", 0))
            outputs["draft_style_quality"] = draft_score_result.to_dict()
            self._save_json(draft_score_result.to_dict(), "draft-style-quality-score")
            draft_style_score = draft_score_result.overall_style_score
            draft_style_grade = draft_score_result.grade
        except Exception as e:
            steps.append(PipelineStep("score_draft_style_quality", "score_draft_style_quality.py", "FAILED", 1))
            draft_style_score = 0.0
            draft_style_grade = "F"

        try:
            version_result = compare_versions(
                original_text=original_version,
                rewritten_text=new_version,
            )
            steps.append(PipelineStep("run_version_comparison_gate", "run_version_comparison_gate.py", "OK", 0))
            outputs["version_comparison"] = version_result.to_dict()
            self._save_json(version_result.to_dict(), "version-comparison-gate")
            version_gate_decision = "accept" if version_result.accept_rewrite else "reject"
        except Exception as e:
            steps.append(PipelineStep("run_version_comparison_gate", "run_version_comparison_gate.py", "FAILED", 1))
            version_gate_decision = "reject"

        status = "SUCCESS" if all(s.status == "OK" for s in steps) else "FAILED"

        pipeline_result = Phase35PipelineResult(
            status=status,
            run_date=self.run_date,
            style_guide_valid=style_guide_valid,
            frameworks_valid=frameworks_valid,
            framework_count=framework_count,
            title_candidate_count=title_candidate_count,
            compliant_title_count=compliant_title_count,
            ai_taste_passed=ai_taste_passed,
            draft_style_score=draft_style_score,
            draft_style_grade=draft_style_grade,
            version_gate_decision=version_gate_decision,
            steps=steps,
            outputs=outputs,
        )

        self._save_json(pipeline_result.to_dict(), "phase35-editorial-quality-pipeline")

        return pipeline_result


def run_phase35_pipeline(
    topic_id: str = "topic_001",
    topic_title: str = "AI芯片市场格局变化",
    topic_type: str = "news_event",
    angle_type: str = "产业影响",
    draft_text: str = "AI芯片市场正在发生深刻变化。NVIDIA发布了新的GPU产品，这对整个AI芯片产业产生了重大影响。",
    original_version: str = "AI芯片市场正在发生深刻变化。值得关注的是，这一趋势未来可期。",
    new_version: str = "AI芯片市场正在发生深刻变化。根据最新数据，NVIDIA发布新GPU，我们认为这重新定义了AI芯片竞争格局，关键在于其性能提升幅度超过市场预期。这对投资者意味着实际的配置调整机会，但需要注意供应链风险。",
) -> Phase35PipelineResult:
    pipeline = Phase35EditorialQualityPipeline()
    return pipeline.run_pipeline(
        topic_id=topic_id,
        topic_title=topic_title,
        topic_type=topic_type,
        angle_type=angle_type,
        draft_text=draft_text,
        original_version=original_version,
        new_version=new_version,
    )
