import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.wechat_feed_discovery import build_discovery_payload, parse_all_feed


def rss_fixture(count: int = 6) -> str:
    items = []
    for index in range(count):
        feed_id = "1111111111" if index % 2 == 0 else "2222222222"
        title = "智东西：AI 芯片观察" if index == 0 else f"普通文章 {index}"
        tail_marker = f"FULLTEXT_SECRET_TAIL_{index}"
        long_content = ("正文摘要 " * 40) + tail_marker
        items.append(
            f"""
            <item>
              <id>{feed_id}-224790{index}_1</id>
              <title><![CDATA[{title}]]></title>
              <link>https://example.test/articles/{feed_id}/{index}</link>
              <guid>{feed_id}-guid-{index}</guid>
              <pubDate>Wed, 08 Jul 2026 10:0{index}:00 GMT</pubDate>
              <description><![CDATA[短描述 {index}]]></description>
              <content:encoded><![CDATA[{long_content}]]></content:encoded>
            </item>
            """
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/">'
        "<channel>"
        + "".join(items)
        + "</channel></rss>"
    )


class TestWechatFeedDiscovery(unittest.TestCase):
    def test_all_feed_items_can_be_grouped(self) -> None:
        payload = build_discovery_payload(rss_fixture(50), limit=50)
        self.assertEqual(payload["summary"]["all_feed_item_count"], 50)
        self.assertEqual(payload["summary"]["cleaned_count"], 50)
        self.assertEqual(payload["summary"]["duplicate_count"], 0)
        self.assertEqual(payload["summary"]["intelligence_article_count"], 50)
        self.assertEqual(payload["summary"]["feed_group_count"], 2)
        self.assertEqual(payload["groups"][0]["item_count"], 25)

    def test_alias_warning_is_detected_from_item_text(self) -> None:
        items = parse_all_feed(rss_fixture(2), limit=2)
        self.assertIn("智东西", items[0]["matched_target_aliases"])

    def test_does_not_persist_rss_full_text(self) -> None:
        payload = build_discovery_payload(rss_fixture(3), limit=3)
        dumped = json.dumps(payload, ensure_ascii=False)
        self.assertNotIn("FULLTEXT_SECRET_TAIL", dumped)
        self.assertIn("content_excerpt", dumped)

    def test_metadata_title_issue_is_recorded(self) -> None:
        payload = build_discovery_payload(rss_fixture(1), limit=1)
        self.assertTrue(payload["metadata_title_issue"]["metadata_title_issue_detected"])
        self.assertEqual(payload["metadata_title_issue"]["example_title"], "Finsmes Ai Gnews")


if __name__ == "__main__":
    unittest.main()
