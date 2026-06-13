import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.phase32_content_production import map_legacy_knowhow


class LegacyKnowhowMethodologyMapperTest(unittest.TestCase):
    def test_mapping_never_auto_applies_legacy_prompt(self):
        payload, _ = map_legacy_knowhow(get_project_paths(ROOT), ROOT)
        self.assertEqual(payload["summary"]["auto_apply"], 0)
        self.assertTrue(all(item["auto_apply"] is False for item in payload["mappings"]))


if __name__ == "__main__":
    unittest.main()
