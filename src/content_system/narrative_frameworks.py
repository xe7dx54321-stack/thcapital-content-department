import yaml
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional


@dataclass
class NarrativeFramework:
    framework_id: str
    name: str
    applicable_topic_types: List[str]
    purpose: str
    section_sequence: List[str]
    opening_strategy: str
    evidence_strategy: str
    counterargument_strategy: str
    closing_strategy: str
    title_strategy: str

    def to_dict(self) -> Dict:
        return asdict(self)


class NarrativeFrameworksManager:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._find_config()
        self.frameworks: List[NarrativeFramework] = []

    def _find_config(self) -> str:
        candidates = [
            "config/narrative_frameworks.yaml",
            os.path.join(os.path.dirname(__file__), "..", "..", "config", "narrative_frameworks.yaml"),
        ]
        for candidate in candidates:
            if os.path.exists(candidate):
                return candidate
        raise FileNotFoundError("narrative_frameworks.yaml not found")

    def load(self) -> List[NarrativeFramework]:
        with open(self.config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self.frameworks = []
        for fw_data in data.get("frameworks", []):
            framework = NarrativeFramework(
                framework_id=fw_data.get("framework_id"),
                name=fw_data.get("name"),
                applicable_topic_types=fw_data.get("applicable_topic_types", []),
                purpose=fw_data.get("purpose"),
                section_sequence=fw_data.get("section_sequence", []),
                opening_strategy=fw_data.get("opening_strategy"),
                evidence_strategy=fw_data.get("evidence_strategy"),
                counterargument_strategy=fw_data.get("counterargument_strategy"),
                closing_strategy=fw_data.get("closing_strategy"),
                title_strategy=fw_data.get("title_strategy"),
            )
            self.frameworks.append(framework)
        return self.frameworks

    def get_framework_by_id(self, framework_id: str) -> Optional[NarrativeFramework]:
        for fw in self.frameworks:
            if fw.framework_id == framework_id:
                return fw
        return None

    def get_applicable_frameworks(self, topic_type: str) -> List[NarrativeFramework]:
        return [fw for fw in self.frameworks if topic_type in fw.applicable_topic_types]

    def validate(self) -> Dict:
        if not self.frameworks:
            self.load()

        errors = []
        warnings = []
        validated_count = 0

        for fw in self.frameworks:
            fw_errors = []
            if not fw.framework_id:
                fw_errors.append("missing framework_id")
            if not fw.name:
                fw_errors.append("missing name")
            if not fw.applicable_topic_types:
                fw_errors.append("empty applicable_topic_types")
            if not fw.section_sequence:
                fw_errors.append("empty section_sequence")
            if not fw.opening_strategy:
                fw_errors.append("missing opening_strategy")
            if not fw.evidence_strategy:
                fw_errors.append("missing evidence_strategy")
            if not fw.counterargument_strategy:
                fw_errors.append("missing counterargument_strategy")
            if not fw.closing_strategy:
                fw_errors.append("missing closing_strategy")

            if fw_errors:
                errors.append({"framework_id": fw.framework_id or "unknown", "errors": fw_errors})
            else:
                validated_count += 1

        if len(self.frameworks) < 6:
            warnings.append(f"Only {len(self.frameworks)} frameworks found, expected at least 6")

        return {
            "valid": len(errors) == 0,
            "framework_count": len(self.frameworks),
            "validated_count": validated_count,
            "errors": errors,
            "warnings": warnings,
        }


def load_narrative_frameworks(config_path: Optional[str] = None) -> List[NarrativeFramework]:
    manager = NarrativeFrameworksManager(config_path)
    return manager.load()


def validate_narrative_frameworks(config_path: Optional[str] = None) -> Dict:
    manager = NarrativeFrameworksManager(config_path)
    return manager.validate()


def get_applicable_frameworks(topic_type: str, config_path: Optional[str] = None) -> List[NarrativeFramework]:
    manager = NarrativeFrameworksManager(config_path)
    manager.load()
    return manager.get_applicable_frameworks(topic_type)


def get_framework_by_id(framework_id: str, config_path: Optional[str] = None) -> Optional[NarrativeFramework]:
    manager = NarrativeFrameworksManager(config_path)
    manager.load()
    return manager.get_framework_by_id(framework_id)
