import yaml
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional


@dataclass
class TitleCandidate:
    title: str
    angle_variant: str
    score: float
    reason: str
    forbidden_pattern_hit: bool
    recommended: bool

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class TitleGenerationResult:
    candidates: List[TitleCandidate]
    compliant_count: int
    recommended_count: int
    forbidden_hit_count: int

    def to_dict(self) -> Dict:
        return {
            "candidates": [c.to_dict() for c in self.candidates],
            "compliant_count": self.compliant_count,
            "recommended_count": self.recommended_count,
            "forbidden_hit_count": self.forbidden_hit_count,
        }


class TitleGenerator:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._find_config()
        self.config = self._load_config()

    def _find_config(self) -> str:
        candidates = [
            "config/title_generation_policy.yaml",
            os.path.join(os.path.dirname(__file__), "..", "..", "config", "title_generation_policy.yaml"),
        ]
        for candidate in candidates:
            if os.path.exists(candidate):
                return candidate
        raise FileNotFoundError("title_generation_policy.yaml not found")

    def _load_config(self) -> Dict:
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _check_forbidden_patterns(self, title: str) -> bool:
        forbidden = self.config.get("forbidden_patterns", [])
        for pattern in forbidden:
            if pattern in title:
                return True
        return False

    def _score_title(self, title: str, angle_variant: str) -> float:
        factors = self.config.get("scoring_factors", [])
        score = 0.0
        total_weight = 0.0

        for factor in factors:
            weight = factor.get("weight", 0.0)
            total_weight += weight

            if factor["factor"] == "length_compliance":
                min_len = self.config.get("title_length_min", 16)
                max_len = self.config.get("title_length_max", 32)
                if min_len <= len(title) <= max_len:
                    score += weight
                else:
                    score += weight * max(0, 1 - abs(len(title) - (min_len + max_len) / 2) / 20)

            elif factor["factor"] == "clarity":
                if len(title) >= 15:
                    score += weight * 0.9
                else:
                    score += weight * 0.5

            elif factor["factor"] == "angle_differentiation":
                if angle_variant in self.config.get("angle_variants", []):
                    score += weight * 0.8
                else:
                    score += weight * 0.3

            elif factor["factor"] == "reader_value":
                if any(kw in title for kw in ["影响", "判断", "分析", "启示", "策略", "风险"]):
                    score += weight * 0.8
                else:
                    score += weight * 0.4

            elif factor["factor"] == "forbidden_pattern_check":
                if not self._check_forbidden_patterns(title):
                    score += weight
                else:
                    score += weight * 0.1

            elif factor["factor"] == "tone_appropriateness":
                if not self._check_forbidden_patterns(title):
                    score += weight * 0.8
                else:
                    score += weight * 0.2

        return score / total_weight if total_weight > 0 else 0.0

    def generate_title_candidates(
        self,
        topic_title: str,
        angle_variants: Optional[List[str]] = None,
    ) -> TitleGenerationResult:
        variants = angle_variants or self.config.get("angle_variants", [])[:5]
        candidate_count = self.config.get("candidate_count", 5)

        base_templates = [
            "{topic}：{angle}角度分析",
            "{angle}视角下的{topic}",
            "{topic}背后的{angle}逻辑",
            "{angle}判断：{topic}",
            "{topic}的{angle}影响",
        ]

        candidates = []
        used_angles = []

        for i, angle in enumerate(variants):
            if i >= candidate_count:
                break
            if angle in used_angles:
                continue

            template = base_templates[i % len(base_templates)]
            title = template.format(topic=topic_title, angle=angle)

            forbidden_hit = self._check_forbidden_patterns(title)
            score = self._score_title(title, angle)
            recommended = score >= self.config.get("min_acceptable_score", 0.6) and not forbidden_hit

            candidates.append(TitleCandidate(
                title=title,
                angle_variant=angle,
                score=round(score, 2),
                reason=f"Generated using '{angle}' angle variant",
                forbidden_pattern_hit=forbidden_hit,
                recommended=recommended,
            ))
            used_angles.append(angle)

        return TitleGenerationResult(
            candidates=candidates,
            compliant_count=sum(1 for c in candidates if not c.forbidden_pattern_hit),
            recommended_count=sum(1 for c in candidates if c.recommended),
            forbidden_hit_count=sum(1 for c in candidates if c.forbidden_pattern_hit),
        )


def generate_title_candidates(
    topic_title: str,
    angle_variants: Optional[List[str]] = None,
    config_path: Optional[str] = None,
) -> TitleGenerationResult:
    generator = TitleGenerator(config_path)
    return generator.generate_title_candidates(topic_title, angle_variants)
