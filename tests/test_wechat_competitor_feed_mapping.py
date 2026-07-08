import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from content_system.wechat_competitor_feed_mapping import apply_competitor_feed_mapping
from content_system.wechat_feed_discovery import build_discovery_payload
from test_wechat_feed_discovery import rss_fixture


class TestWechatCompetitorFeedMapping(unittest.TestCase):
    def test_missing_local_mapping_does_not_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "同行资本市场内容系统" / "10_logs").mkdir(parents=True)
            payload, _outputs = apply_competitor_feed_mapping(root, build_discovery_payload(rss_fixture(2), limit=2))
            self.assertEqual(payload["status"], "LOCAL_MAPPING_MISSING")
            self.assertEqual(payload["summary"]["target_competitor_count"], 7)

    def test_feed_id_mapping_matches_competitor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config").mkdir()
            (root / "同行资本市场内容系统" / "10_logs").mkdir(parents=True)
            (root / "config" / "wechat_competitor_feed_map.local.yaml").write_text(
                """
schema_version: v1
competitors:
  - name: 智东西
    feed_ids:
      - "1111111111"
    aliases:
      - 智东西
  - name: 36氪
    feed_ids: []
    aliases:
      - 36氪
""".strip()
                + "\n",
                encoding="utf-8",
            )
            payload, _outputs = apply_competitor_feed_mapping(root, build_discovery_payload(rss_fixture(4), limit=4))
            self.assertEqual(payload["status"], "PARTIAL")
            self.assertEqual(payload["summary"]["matched_competitor_count"], 1)
            self.assertEqual(payload["summary"]["articles_by_competitor"]["智东西"], 2)
            self.assertIn("36氪", payload["summary"]["missing_competitors"])

    def test_alias_mapping_can_match_without_feed_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config").mkdir()
            (root / "同行资本市场内容系统" / "10_logs").mkdir(parents=True)
            (root / "config" / "wechat_competitor_feed_map.local.yaml").write_text(
                """
schema_version: v1
competitors:
  - name: 智东西
    feed_ids: []
    aliases:
      - 智东西
""".strip()
                + "\n",
                encoding="utf-8",
            )
            payload, _outputs = apply_competitor_feed_mapping(root, build_discovery_payload(rss_fixture(1), limit=1))
            self.assertEqual(payload["status"], "PASS")
            self.assertEqual(payload["summary"]["matched_competitors"], ["智东西"])


if __name__ == "__main__":
    unittest.main()
