import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.phase32_content_production import validate_content_playbooks


class ContentProductionPlaybookTest(unittest.TestCase):
    def test_content_playbook_validation_passes(self):
        payload, _ = validate_content_playbooks(get_project_paths(ROOT), ROOT)
        self.assertEqual(payload["validate_status"], "PASS")
        self.assertGreaterEqual(payload["summary"]["playbook_count"], 6)
        self.assertEqual(payload["summary"]["fail"], 0)


if __name__ == "__main__":
    unittest.main()
