import yaml
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional


@dataclass
class ReaderProfile:
    core_readers: List[str]
    reader_needs: List[str]


@dataclass
class Tone:
    preferred: List[str]
    discouraged: List[str]


@dataclass
class EditorialStyleGuide:
    schema_version: str
    reader_profile: ReaderProfile
    writing_principles: List[str]
    tone: Tone
    must_have_sections: List[str]

    def to_dict(self) -> Dict:
        return asdict(self)


class EditorialStyleGuideLoader:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._find_config()
        self.style_guide: Optional[EditorialStyleGuide] = None

    def _find_config(self) -> str:
        candidates = [
            "config/editorial_style_guide.yaml",
            os.path.join(os.path.dirname(__file__), "..", "..", "config", "editorial_style_guide.yaml"),
        ]
        for candidate in candidates:
            if os.path.exists(candidate):
                return candidate
        raise FileNotFoundError("editorial_style_guide.yaml not found")

    def load(self) -> EditorialStyleGuide:
        with open(self.config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self.style_guide = EditorialStyleGuide(
            schema_version=data.get("schema_version", "v1"),
            reader_profile=ReaderProfile(
                core_readers=data.get("reader_profile", {}).get("core_readers", []),
                reader_needs=data.get("reader_profile", {}).get("reader_needs", []),
            ),
            writing_principles=data.get("writing_principles", []),
            tone=Tone(
                preferred=data.get("tone", {}).get("preferred", []),
                discouraged=data.get("tone", {}).get("discouraged", []),
            ),
            must_have_sections=data.get("must_have_sections", []),
        )
        return self.style_guide

    def validate(self) -> Dict:
        if not self.style_guide:
            self.load()

        errors = []
        warnings = []

        if not self.style_guide.reader_profile.core_readers:
            errors.append("reader_profile.core_readers is empty")
        if not self.style_guide.reader_profile.reader_needs:
            errors.append("reader_profile.reader_needs is empty")
        if not self.style_guide.writing_principles:
            errors.append("writing_principles is empty")
        if not self.style_guide.tone.preferred:
            warnings.append("tone.preferred is empty")
        if not self.style_guide.tone.discouraged:
            warnings.append("tone.discouraged is empty")
        if not self.style_guide.must_have_sections:
            errors.append("must_have_sections is empty")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "style_guide": self.style_guide.to_dict(),
        }


def load_editorial_style_guide(config_path: Optional[str] = None) -> EditorialStyleGuide:
    loader = EditorialStyleGuideLoader(config_path)
    return loader.load()


def validate_editorial_style_guide(config_path: Optional[str] = None) -> Dict:
    loader = EditorialStyleGuideLoader(config_path)
    return loader.validate()
