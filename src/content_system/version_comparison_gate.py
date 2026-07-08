import yaml
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from .draft_style_quality_scorer import DraftStyleQualityScorer, DraftStyleQualityResult


@dataclass
class MetricComparison:
    metric_id: str
    original_score: float
    rewritten_score: float
    delta: float
    regression: bool
    weight: float

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class VersionComparisonResult:
    original_score: float
    rewritten_score: float
    improvement_score: float
    regressions: List[str]
    accept_rewrite: bool
    reason: str
    metric_comparisons: List[MetricComparison]

    def to_dict(self) -> Dict:
        return {
            "original_score": self.original_score,
            "rewritten_score": self.rewritten_score,
            "improvement_score": self.improvement_score,
            "regressions": self.regressions,
            "accept_rewrite": self.accept_rewrite,
            "reason": self.reason,
            "metric_comparisons": [m.to_dict() for m in self.metric_comparisons],
        }


class VersionComparisonGate:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._find_config()
        self.config = self._load_config()
        self.scorer = DraftStyleQualityScorer()

    def _find_config(self) -> str:
        candidates = [
            "config/version_comparison_policy.yaml",
            os.path.join(os.path.dirname(__file__), "..", "..", "config", "version_comparison_policy.yaml"),
        ]
        for candidate in candidates:
            if os.path.exists(candidate):
                return candidate
        raise FileNotFoundError("version_comparison_policy.yaml not found")

    def _load_config(self) -> Dict:
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def compare_versions(
        self,
        original_text: str,
        rewritten_text: str,
        original_title: str = "",
        rewritten_title: str = "",
    ) -> VersionComparisonResult:
        original_result = self.scorer.score_draft_quality(original_text, original_title)
        rewritten_result = self.scorer.score_draft_quality(rewritten_text, rewritten_title)

        metric_comparisons: List[MetricComparison] = []
        regressions: List[str] = []

        metrics_config = self.config.get("metrics", [])
        metric_weights = {m["metric_id"]: m.get("weight", 0.1) for m in metrics_config}

        for dim_score in rewritten_result.dimension_scores:
            original_dim = next((d for d in original_result.dimension_scores if d.dimension == dim_score.dimension), None)
            original_val = original_dim.score if original_dim else 0.5

            delta = dim_score.score - original_val
            regression = delta < -0.05

            metric_comparisons.append(MetricComparison(
                metric_id=self._get_metric_id(dim_score.dimension),
                original_score=round(original_val, 2),
                rewritten_score=round(dim_score.score, 2),
                delta=round(delta, 2),
                regression=regression,
                weight=metric_weights.get(self._get_metric_id(dim_score.dimension), 0.1),
            ))

            if regression:
                regressions.append(dim_score.dimension)

        total_weight = sum(m.weight for m in metric_comparisons)
        if total_weight > 0:
            improvement_score = sum(m.delta * m.weight for m in metric_comparisons) / total_weight
        else:
            improvement_score = 0.0

        min_improvement_required = self.config.get("min_improvement_score", 0.05)

        regression_checks = {}
        required_checks = self.config.get("required_non_regression_checks", [])
        for check in required_checks:
            if isinstance(check, str):
                metric_id = check
            else:
                metric_id = check.get("id") if isinstance(check, dict) else str(check)
            comparison = next((m for m in metric_comparisons if m.metric_id == metric_id), None)
            regression_checks[metric_id] = comparison is not None and not comparison.regression

        any_regression = any(not v for v in regression_checks.values())
        improvement_ok = improvement_score >= min_improvement_required

        decision_rules = self.config.get("decision_rules", [])
        overall_decision = "reject"
        reason = ""

        for rule in decision_rules:
            condition = rule.get("condition")
            action = rule.get("action")
            description = rule.get("description")

            if condition == "improvement_score >= min_improvement_score AND no_regressions":
                if improvement_ok and not any_regression:
                    overall_decision = action
                    reason = description
                    break
            elif condition == "improvement_score < min_improvement_score":
                if not improvement_ok:
                    overall_decision = action
                    reason = description
                    break
            elif condition == "any_regression_in_required_checks":
                if any_regression:
                    overall_decision = action
                    reason = description
                    break
            elif condition == "improvement_score >= min_improvement_score AND minor_regressions":
                if improvement_ok and regressions:
                    overall_decision = action
                    reason = description
                    break

        accept_rewrite = overall_decision in ["accept", "partial_accept"]

        return VersionComparisonResult(
            original_score=round(original_result.overall_style_score, 2),
            rewritten_score=round(rewritten_result.overall_style_score, 2),
            improvement_score=round(improvement_score, 2),
            regressions=regressions,
            accept_rewrite=accept_rewrite,
            reason=reason,
            metric_comparisons=metric_comparisons,
        )

    def _get_metric_id(self, dimension_name: str) -> str:
        mapping = {
            "判断强度": "judgment_strength",
            "证据密度": "evidence_density",
            "叙事流畅度": "narrative_flow",
            "标题质量": "title_quality",
            "AI味评分": "ai_taste_reduction",
            "风险清晰度": "risk_clarity",
            "可读性": "readability",
            "开头质量": "opening_quality",
        }
        return mapping.get(dimension_name, dimension_name)


def compare_versions(
    original_text: str,
    rewritten_text: str,
    original_title: str = "",
    rewritten_title: str = "",
    config_path: Optional[str] = None,
) -> VersionComparisonResult:
    gate = VersionComparisonGate(config_path)
    return gate.compare_versions(original_text, rewritten_text, original_title, rewritten_title)
