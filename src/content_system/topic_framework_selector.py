from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from .narrative_frameworks import NarrativeFramework, NarrativeFrameworksManager


@dataclass
class FrameworkSelectionResult:
    topic_id: str
    selected_framework: Optional[NarrativeFramework]
    reason: str
    confidence: float
    fallback_used: bool

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["selected_framework"] = self.selected_framework.to_dict() if self.selected_framework else None
        return result


class TopicFrameworkSelector:
    def __init__(self):
        self.manager = NarrativeFrameworksManager()
        self.manager.load()

    def select_best_framework(
        self,
        topic_id: str,
        topic_type: str,
        event_type: Optional[str] = None,
        angle_type: Optional[str] = None,
        differentiated_angle: Optional[str] = None,
        evidence_strength: float = 0.5,
    ) -> FrameworkSelectionResult:
        applicable = self.manager.get_applicable_frameworks(topic_type)

        if not applicable:
            fallback = self.manager.get_framework_by_id("news_explainer")
            return FrameworkSelectionResult(
                topic_id=topic_id,
                selected_framework=fallback,
                reason=f"No applicable framework for topic_type '{topic_type}', using fallback",
                confidence=0.3,
                fallback_used=True,
            )

        if len(applicable) == 1:
            return FrameworkSelectionResult(
                topic_id=topic_id,
                selected_framework=applicable[0],
                reason=f"Only one applicable framework: {applicable[0].name}",
                confidence=0.9,
                fallback_used=False,
            )

        scores = []
        for fw in applicable:
            score = self._score_framework(fw, angle_type, differentiated_angle, evidence_strength)
            scores.append((fw, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        best_fw, best_score = scores[0]

        reason = f"Selected based on angle_type='{angle_type}', evidence_strength={evidence_strength}"

        return FrameworkSelectionResult(
            topic_id=topic_id,
            selected_framework=best_fw,
            reason=reason,
            confidence=min(0.95, best_score),
            fallback_used=False,
        )

    def _score_framework(
        self,
        framework: NarrativeFramework,
        angle_type: Optional[str],
        differentiated_angle: Optional[str],
        evidence_strength: float,
    ) -> float:
        score = 0.5

        if angle_type:
            angle_keywords = {
                "反常识": ["investment_framework", "industry_trend_analysis"],
                "产业影响": ["industry_trend_analysis", "competitive_landscape_analysis"],
                "产品策略": ["product_strategy_analysis"],
                "投资判断": ["investment_framework"],
                "方法论": ["investment_framework", "technical_route_analysis"],
                "风险提示": ["investment_framework", "news_explainer"],
            }
            for keyword, fws in angle_keywords.items():
                if keyword in (angle_type or "") and framework.framework_id in fws:
                    score += 0.2
                    break

        if evidence_strength > 0.7:
            if framework.framework_id in ["investment_framework", "technical_route_analysis"]:
                score += 0.15

        if differentiated_angle and "竞争" in differentiated_angle:
            if framework.framework_id == "competitive_landscape_analysis":
                score += 0.1

        return min(1.0, score)


def select_topic_framework(
    topic_id: str,
    topic_type: str,
    event_type: Optional[str] = None,
    angle_type: Optional[str] = None,
    differentiated_angle: Optional[str] = None,
    evidence_strength: float = 0.5,
) -> FrameworkSelectionResult:
    selector = TopicFrameworkSelector()
    return selector.select_best_framework(
        topic_id=topic_id,
        topic_type=topic_type,
        event_type=event_type,
        angle_type=angle_type,
        differentiated_angle=differentiated_angle,
        evidence_strength=evidence_strength,
    )
