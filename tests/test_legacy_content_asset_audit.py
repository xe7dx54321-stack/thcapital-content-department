import hashlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.phase32_content_production import audit_legacy_content_assets


class LegacyContentAssetAuditTest(unittest.TestCase):
    def test_asset_audit_does_not_modify_source_file(self):
        target = ROOT / "config" / "brief_generation_playbook.yaml"
        before = hashlib.sha256(target.read_bytes()).hexdigest()
        payload, _ = audit_legacy_content_assets(get_project_paths(ROOT), ROOT, limit=8)
        after = hashlib.sha256(target.read_bytes()).hexdigest()
        self.assertEqual(before, after)
        self.assertIn("asset_count", payload["summary"])


if __name__ == "__main__":
    unittest.main()
