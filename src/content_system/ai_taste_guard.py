import yaml
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional


@dataclass
class TasteViolation:
    phrase: str
    category: str
    severity: str
    suggestion: str
    paragraph_id: int

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class AITasteGuardResult:
    checked_text: str
    hit_count: int
    high_severity_count: int
    violations: List[TasteViolation]
    ai_taste_score: float

    def to_dict(self) -> Dict:
        return {
            "checked_text": self.checked_text,
            "hit_count": self.hit_count,
            "high_severity_count": self.high_severity_count,
            "violations": [v.to_dict() for v in self.violations],
            "ai_taste_score": self.ai_taste_score,
        }


class AITasteGuard:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._find_config()
        self.config = self._load_config()

    def _find_config(self) -> str:
        candidates = [
            "config/ai_taste_guard.yaml",
            os.path.join(os.path.dirname(__file__), "..", "..", "config", "ai_taste_guard.yaml"),
        ]
        for candidate in candidates:
            if os.path.exists(candidate):
                return candidate
        raise FileNotFoundError("ai_taste_guard.yaml not found")

    def _load_config(self) -> Dict:
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _get_severity_penalty(self, severity: str) -> float:
        for level in self.config.get("severity_levels", []):
            if level.get("level") == severity:
                return level.get("score_penalty", 0.1)
        return 0.05

    def detect_ai_taste(self, text: str) -> AITasteGuardResult:
        paragraphs = text.split("\n")
        violations: List[TasteViolation] = []
        high_severity_count = 0

        categories = [
            ("discouraged_phrases", "discouraged_phrase", "high"),
            ("empty_expressions", "empty_expression", "medium"),
            ("marketing_expressions", "marketing_expression", "high"),
            ("excessive_adjectives", "excessive_adjective", "medium"),
        ]

        for para_idx, paragraph in enumerate(paragraphs):
            if not paragraph.strip():
                continue

            for category_key, category_name, default_severity in categories:
                phrases = self.config.get(category_key, [])
                for phrase in phrases:
                    if phrase in paragraph:
                        violation = TasteViolation(
                            phrase=phrase,
                            category=category_name,
                            severity=default_severity,
                            suggestion=self._get_suggestion(phrase, category_name),
                            paragraph_id=para_idx,
                        )
                        violations.append(violation)
                        if default_severity == "high":
                            high_severity_count += 1

        base_score = 1.0
        for violation in violations:
            penalty = self._get_severity_penalty(violation.severity)
            base_score = max(0, base_score - penalty)

        return AITasteGuardResult(
            checked_text=text,
            hit_count=len(violations),
            high_severity_count=high_severity_count,
            violations=violations,
            ai_taste_score=round(base_score, 2),
        )

    def _get_suggestion(self, phrase: str, category: str) -> str:
        suggestions = {
            "discouraged_phrase": f"用具体判断替代'{phrase}'",
            "empty_expression": f"'{phrase}'过于空泛，提供具体依据",
            "marketing_expression": f"删除'{phrase}'营销号表达",
            "excessive_adjective": f"减少'{phrase}'等过度形容词",
        }
        return suggestions.get(category, f"修改'{phrase}'")

    def get_rule_count(self) -> int:
        return (
            len(self.config.get("discouraged_phrases", [])) +
            len(self.config.get("empty_expressions", [])) +
            len(self.config.get("marketing_expressions", [])) +
            len(self.config.get("excessive_adjectives", []))
        )


def detect_ai_taste(text: str, config_path: Optional[str] = None) -> AITasteGuardResult:
    guard = AITasteGuard(config_path)
    return guard.detect_ai_taste(text)


def get_ai_taste_rule_count(config_path: Optional[str] = None) -> int:
    guard = AITasteGuard(config_path)
    return guard.get_rule_count()
