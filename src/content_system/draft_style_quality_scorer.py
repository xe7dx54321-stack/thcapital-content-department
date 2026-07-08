from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from .ai_taste_guard import AITasteGuard, AITasteGuardResult


@dataclass
class DimensionScore:
    dimension: str
    score: float
    max_score: float
    weight: float

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class DraftStyleQualityResult:
    overall_style_score: float
    grade: str
    dimension_scores: List[DimensionScore]
    blocking_issues: List[str]
    revision_suggestions: List[str]

    def to_dict(self) -> Dict:
        return {
            "overall_style_score": self.overall_style_score,
            "grade": self.grade,
            "dimension_scores": [d.to_dict() for d in self.dimension_scores],
            "blocking_issues": self.blocking_issues,
            "revision_suggestions": self.revision_suggestions,
        }


class DraftStyleQualityScorer:
    def __init__(self):
        self.dimensions = [
            {"id": "judgment_strength", "name": "判断强度", "weight": 0.20, "min_acceptable": 0.6},
            {"id": "evidence_density", "name": "证据密度", "weight": 0.15, "min_acceptable": 0.5},
            {"id": "narrative_flow", "name": "叙事流畅度", "weight": 0.15, "min_acceptable": 0.5},
            {"id": "title_quality", "name": "标题质量", "weight": 0.15, "min_acceptable": 0.5},
            {"id": "opening_quality", "name": "开头质量", "weight": 0.10, "min_acceptable": 0.5},
            {"id": "risk_clarity", "name": "风险清晰度", "weight": 0.10, "min_acceptable": 0.5},
            {"id": "ai_taste", "name": "AI味评分", "weight": 0.10, "min_acceptable": 0.6},
            {"id": "readability", "name": "可读性", "weight": 0.05, "min_acceptable": 0.5},
        ]
        self.ai_taste_guard = AITasteGuard()

    def _score_judgment_strength(self, text: str) -> float:
        judgment_keywords = ["我们认为", "核心判断", "关键在于", "本质是", "结论是"]
        score = 0.3
        for kw in judgment_keywords:
            if kw in text:
                score += 0.15
        return min(1.0, score)

    def _score_evidence_density(self, text: str) -> float:
        evidence_keywords = ["根据", "数据显示", "报告指出", "调研发现", "来源"]
        score = 0.2
        for kw in evidence_keywords:
            if kw in text:
                score += 0.12
        return min(1.0, score)

    def _score_narrative_flow(self, text: str) -> float:
        transition_keywords = ["首先", "其次", "然后", "最后", "然而", "此外"]
        score = 0.3
        for kw in transition_keywords:
            if kw in text:
                score += 0.1
        return min(1.0, score)

    def _score_title_quality(self, title: str) -> float:
        if not title:
            return 0.5
        if len(title) >= 15 and len(title) <= 35:
            return 0.8
        return 0.5

    def _score_opening_quality(self, text: str) -> float:
        first_sentence = text.split("\n")[0][:100] if text else ""
        marketing_patterns = ["震惊", "你绝对想不到", "深度解析", "独家"]
        if any(p in first_sentence for p in marketing_patterns):
            return 0.3
        if "我们认为" in first_sentence or len(first_sentence) > 20:
            return 0.7
        return 0.5

    def _score_risk_clarity(self, text: str) -> float:
        risk_keywords = ["风险", "挑战", "不确定性", "可能", "需要注意"]
        score = 0.2
        for kw in risk_keywords:
            if kw in text:
                score += 0.15
        return min(1.0, score)

    def _score_readability(self, text: str) -> float:
        if not text:
            return 0.5
        avg_sentence_len = sum(len(s) for s in text.replace("。", "\n").split("\n") if s.strip()) / max(1, text.count("。"))
        if avg_sentence_len < 30:
            return 0.9
        elif avg_sentence_len < 50:
            return 0.7
        return 0.4

    def score_draft_quality(
        self,
        draft_text: str,
        title: str = "",
    ) -> DraftStyleQualityResult:
        dimension_scores: List[DimensionScore] = []
        blocking_issues: List[str] = []
        revision_suggestions: List[str] = []

        scores = {
            "judgment_strength": self._score_judgment_strength(draft_text),
            "evidence_density": self._score_evidence_density(draft_text),
            "narrative_flow": self._score_narrative_flow(draft_text),
            "title_quality": self._score_title_quality(title),
            "opening_quality": self._score_opening_quality(draft_text),
            "risk_clarity": self._score_risk_clarity(draft_text),
            "ai_taste": self.ai_taste_guard.detect_ai_taste(draft_text).ai_taste_score,
            "readability": self._score_readability(draft_text),
        }

        total_weight = 0.0
        weighted_score = 0.0

        for dim in self.dimensions:
            dim_score = scores.get(dim["id"], 0.5)
            dimension_scores.append(DimensionScore(
                dimension=dim["name"],
                score=round(dim_score, 2),
                max_score=1.0,
                weight=dim["weight"],
            ))

            weighted_score += dim_score * dim["weight"]
            total_weight += dim["weight"]

            if dim_score < dim["min_acceptable"]:
                blocking_issues.append(f"{dim['name']}不足（{round(dim_score, 2)} < {dim['min_acceptable']}）")
                revision_suggestions.append(self._get_suggestion(dim["id"]))

        overall_score = weighted_score / total_weight if total_weight > 0 else 0.5
        grade = self._get_grade(overall_score)

        return DraftStyleQualityResult(
            overall_style_score=round(overall_score, 2),
            grade=grade,
            dimension_scores=dimension_scores,
            blocking_issues=blocking_issues,
            revision_suggestions=revision_suggestions,
        )

    def _get_grade(self, score: float) -> str:
        if score >= 0.8:
            return "A"
        elif score >= 0.7:
            return "B"
        elif score >= 0.6:
            return "C"
        elif score >= 0.5:
            return "D"
        return "F"

    def _get_suggestion(self, dimension_id: str) -> str:
        suggestions = {
            "judgment_strength": "增加明确的核心判断，使用'我们认为'等表达",
            "evidence_density": "增加数据来源和证据引用",
            "narrative_flow": "增加逻辑连接词，改善段落衔接",
            "title_quality": "优化标题，确保包含核心事件和差异化角度",
            "opening_quality": "修改开头，避免营销号表达方式",
            "risk_clarity": "明确表达风险因素和不确定性",
            "ai_taste": "删除AI味表达，使用更专业的语言",
            "readability": "缩短句子长度，提高可读性",
        }
        return suggestions.get(dimension_id, "优化该维度")


def score_draft_quality(
    draft_text: str,
    title: str = "",
) -> DraftStyleQualityResult:
    scorer = DraftStyleQualityScorer()
    return scorer.score_draft_quality(draft_text, title)
