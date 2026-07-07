import unittest

from content_system.wechat_rss_ingestion import (
    RssEntry,
    RssIngestionReport,
    make_entry_id,
    extract_excerpt,
    mock_rss_entries,
    ingest_source,
    ingest_all_sources,
    parse_rss_feed,
    today_token,
)
from content_system.wechat_rss_source_registry import WechatRssSource


class TestMakeEntryId(unittest.TestCase):
    def test_make_entry_id(self):
        entry_id = make_entry_id("test_source", "Test Title", "https://example.com/article")
        self.assertIsInstance(entry_id, str)
        self.assertTrue(entry_id.startswith("entry_test_source_"))
        self.assertEqual(len(entry_id), len("entry_test_source_") + 12)

    def test_entry_id_consistency(self):
        id1 = make_entry_id("test_source", "Test Title", "https://example.com/article")
        id2 = make_entry_id("test_source", "Test Title", "https://example.com/article")
        self.assertEqual(id1, id2)

    def test_entry_id_different_sources(self):
        id1 = make_entry_id("source1", "Test Title", "https://example.com/article")
        id2 = make_entry_id("source2", "Test Title", "https://example.com/article")
        self.assertNotEqual(id1, id2)


class TestExtractExcerpt(unittest.TestCase):
    def test_short_text(self):
        text = "Short text"
        result = extract_excerpt(text)
        self.assertEqual(result, text)

    def test_long_text_truncated(self):
        text = "x" * 400
        result = extract_excerpt(text)
        self.assertEqual(len(result), 302)
        self.assertTrue(result.endswith("..."))

    def test_text_with_html(self):
        text = "<p>Paragraph 1</p><p>Paragraph 2</p>"
        result = extract_excerpt(text)
        self.assertNotIn("<p>", result)
        self.assertNotIn("</p>", result)


class TestMockRssEntries(unittest.TestCase):
    def test_mock_entries_returns_entries(self):
        source = WechatRssSource(
            schema_version="v1",
            source_id="test_source",
            label="Test Source",
            tier="A",
            language="zh",
            enabled=True,
            is_official=False,
            rss_url="https://example.com/rss",
            owner="test",
            notes="",
        )
        entries = mock_rss_entries(source)
        self.assertEqual(len(entries), 1)
        self.assertTrue(entries[0].title.startswith("[MOCK]"))

    def test_mock_entry_has_do_not_copy_text(self):
        source = WechatRssSource(
            schema_version="v1",
            source_id="test_source",
            label="Test Source",
            tier="A",
            language="zh",
            enabled=True,
            is_official=False,
            rss_url="https://example.com/rss",
            owner="test",
            notes="",
        )
        entries = mock_rss_entries(source)
        self.assertTrue(entries[0].do_not_copy_text)


class TestIngestSource(unittest.TestCase):
    def test_dry_run_does_not_fail(self):
        source = WechatRssSource(
            schema_version="v1",
            source_id="test_source",
            label="Test Source",
            tier="A",
            language="zh",
            enabled=True,
            is_official=False,
            rss_url="https://nonexistent-domain-12345.com/rss",
            owner="test",
            notes="",
        )
        entries, warnings, errors = ingest_source(source, dry_run=True)
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(entries), 1)
        self.assertTrue(any("dry-run" in w for w in warnings))

    def test_dry_run_with_env_variable_url(self):
        source = WechatRssSource(
            schema_version="v1",
            source_id="test_source",
            label="Test Source",
            tier="A",
            language="zh",
            enabled=True,
            is_official=False,
            rss_url="${NONEXISTENT_ENV_VAR}",
            owner="test",
            notes="",
        )
        entries, warnings, errors = ingest_source(source, dry_run=True)
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(entries), 1)


class TestIngestAllSources(unittest.TestCase):
    def test_ingest_all_sources_dry_run(self):
        sources = (
            WechatRssSource(
                schema_version="v1",
                source_id="source1",
                label="Source 1",
                tier="A",
                language="zh",
                enabled=True,
                is_official=False,
                rss_url="https://example.com/rss1",
                owner="test",
                notes="",
            ),
            WechatRssSource(
                schema_version="v1",
                source_id="source2",
                label="Source 2",
                tier="B",
                language="zh",
                enabled=False,
                is_official=True,
                rss_url="https://example.com/rss2",
                owner="test",
                notes="",
            ),
        )
        report = ingest_all_sources(sources, dry_run=True)
        self.assertTrue(report.dry_run)
        self.assertEqual(report.source_count, 2)
        self.assertEqual(report.entry_count, 1)
        self.assertTrue(any("disabled" in w for w in report.warnings))

    def test_ingest_all_sources_empty(self):
        report = ingest_all_sources((), dry_run=True)
        self.assertEqual(report.entry_count, 0)


class TestParseRssFeed(unittest.TestCase):
    def test_parse_valid_rss(self):
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<item>
<title>Test Article</title>
<link>https://example.com/article</link>
<pubDate>2024-01-15</pubDate>
<description>This is a test article description.</description>
</item>
</channel>
</rss>"""
        source = WechatRssSource(
            schema_version="v1",
            source_id="test_source",
            label="Test Source",
            tier="A",
            language="zh",
            enabled=True,
            is_official=False,
            rss_url="https://example.com/rss",
            owner="test",
            notes="",
        )
        entries = parse_rss_feed(xml_content, source)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].title, "Test Article")
        self.assertEqual(entries[0].link, "https://example.com/article")

    def test_parse_empty_rss(self):
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
</channel>
</rss>"""
        source = WechatRssSource(
            schema_version="v1",
            source_id="test_source",
            label="Test Source",
            tier="A",
            language="zh",
            enabled=True,
            is_official=False,
            rss_url="https://example.com/rss",
            owner="test",
            notes="",
        )
        entries = parse_rss_feed(xml_content, source)
        self.assertEqual(len(entries), 0)


if __name__ == "__main__":
    unittest.main()