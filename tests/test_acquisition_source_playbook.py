from __future__ import annotations

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from content_system.acquisition_source_playbook import load_source_playbooks, validate_source_playbooks


class AcquisitionSourcePlaybookTest(unittest.TestCase):
    def test_source_playbooks_are_safe_metadata(self) -> None:
        payload = validate_source_playbooks(ROOT)
        self.assertEqual(payload["status"], "PASS")
        self.assertGreater(payload["metadata_sources"], 0)

    def test_same_source_primary_lane_unique(self) -> None:
        sources = load_source_playbooks(ROOT)
        self.assertEqual(len(sources), len(set(sources)))
        self.assertTrue(all("lane" in source for source in sources.values() if isinstance(source, dict)))


if __name__ == "__main__":
    unittest.main()
