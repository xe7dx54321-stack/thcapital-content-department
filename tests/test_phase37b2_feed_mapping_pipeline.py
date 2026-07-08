import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from content_system.phase37b2_feed_mapping_pipeline import run_phase37b2_pipeline
from test_wechat_feed_discovery import rss_fixture


class TestPhase37B2FeedMappingPipeline(unittest.TestCase):
    def test_pipeline_is_actionable_without_local_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload, outputs = run_phase37b2_pipeline(root, limit=6, xml_content=rss_fixture(6))
            self.assertEqual(payload["status"], "ACTIONABLE")
            self.assertEqual(payload["summary"]["all_feed_item_count"], 6)
            self.assertEqual(payload["summary"]["mapping_status"], "LOCAL_MAPPING_MISSING")
            self.assertTrue(outputs["latest_json"].exists())

    def test_pipeline_can_pass_with_local_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config").mkdir()
            (root / "config" / "wechat_competitor_feed_map.local.yaml").write_text(
                """
schema_version: v1
competitors:
  - name: 智东西
    feed_ids:
      - "1111111111"
    aliases:
      - 智东西
  - name: 普通源
    feed_ids:
      - "2222222222"
    aliases: []
""".strip()
                + "\n",
                encoding="utf-8",
            )
            payload, _outputs = run_phase37b2_pipeline(root, limit=4, xml_content=rss_fixture(4))
            self.assertEqual(payload["status"], "SUCCESS")
            self.assertEqual(payload["summary"]["matched_competitor_count"], 2)


if __name__ == "__main__":
    unittest.main()
