import unittest

from content_system.wechat_article_cleaner import (
    CleanedArticle,
    ArticleCleanerReport,
    clean_excerpt,
    clean_article,
    clean_all_articles,
    remove_html_tags,
    remove_ads,
    extract_paragraphs,
)
from content_system.wechat_rss_ingestion import RssEntry


class TestRemoveHtmlTags(unittest.TestCase):
    def test_remove_tags(self):
        text = "<script><div><p>Hello <b>world</b></p></div></script>"
        result = remove_html_tags(text)
        self.assertIn("<div>", result)
        self.assertIn("<p>", result)
        self.assertIn("<b>world</b>", result)
        self.assertNotIn("<script>", result)

    def test_remove_all_tags(self):
        text = "<script>alert('xss')</script><p>Content</p>"
        result = remove_html_tags(text, preserve={})
        self.assertNotIn("<script>", result)
        self.assertNotIn("</script>", result)
        self.assertNotIn("<p>", result)
        self.assertNotIn("</p>", result)

    def test_preserve_specific_tags(self):
        text = "<p>Paragraph</p><span>Span</span><div>Div</div>"
        result = remove_html_tags(text, preserve={"p", "span"})
        self.assertEqual(result, "<p>Paragraph</p><span>Span</span>Div")


class TestRemoveAds(unittest.TestCase):
    def test_remove_ad_keyword(self):
        text = "这是内容。广告时间。更多内容。"
        result, has_ad = remove_ads(text)
        self.assertTrue(has_ad)
        self.assertNotIn("广告时间", result)

    def test_remove_multiple_ads(self):
        text = "关注公众号获取更多信息。下载App体验更佳。"
        result, has_ad = remove_ads(text)
        self.assertTrue(has_ad)
        self.assertNotIn("关注公众号", result)
        self.assertNotIn("下载App", result)

    def test_no_ad(self):
        text = "这是一篇普通文章内容。"
        result, has_ad = remove_ads(text)
        self.assertFalse(has_ad)
        self.assertEqual(result, text)


class TestExtractParagraphs(unittest.TestCase):
    def test_extract_from_p_tags(self):
        text = "<p>First paragraph</p><p>Second paragraph</p>"
        result = extract_paragraphs(text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "First paragraph")

    def test_extract_from_br_tags(self):
        text = "<p>This is paragraph 1 with enough length</p><p>This is paragraph 2 with enough length</p><p>This is paragraph 3 with enough length</p>"
        result = extract_paragraphs(text)
        self.assertEqual(len(result), 3)

    def test_filter_short_paragraphs(self):
        text = "<p>Short</p><p>This is a longer paragraph that meets the minimum length requirement.</p>"
        result = extract_paragraphs(text)
        self.assertEqual(len(result), 1)


class TestCleanExcerpt(unittest.TestCase):
    def test_clean_html(self):
        excerpt = "<p><b>Hello</b> <i>world</i></p>"
        result = clean_excerpt(excerpt)
        self.assertIn("Hello", result)
        self.assertIn("world", result)

    def test_clean_with_ads(self):
        excerpt = "<p>内容。广告时间。</p>"
        result = clean_excerpt(excerpt)
        self.assertNotIn("广告时间", result)

    def test_clean_with_excessive_whitespace(self):
        excerpt = "Hello   world   with   spaces"
        result = clean_excerpt(excerpt)
        self.assertEqual(result, "Hello world with spaces")


class TestCleanArticle(unittest.TestCase):
    def test_clean_article(self):
        entry = RssEntry(
            schema_version="v1",
            entry_id="test_entry",
            source_id="test_source",
            source_label="Test Source",
            is_official=False,
            title="Test Article",
            link="https://example.com/article",
            published_at="20240115",
            excerpt="<p>这是一篇测试文章的摘要内容。广告时间。</p>",
            captured_at="2024-01-15T10:00:00+00:00",
            do_not_copy_text=True,
        )
        cleaned = clean_article(entry)
        self.assertEqual(cleaned.entry_id, "test_entry")
        self.assertEqual(cleaned.title, "Test Article")
        self.assertTrue(cleaned.ad_removed)
        self.assertTrue(cleaned.do_not_copy_text)

    def test_cleaned_excerpt_truncation(self):
        long_text = "x" * 600
        entry = RssEntry(
            schema_version="v1",
            entry_id="test_entry",
            source_id="test_source",
            source_label="Test Source",
            is_official=False,
            title="Test Article",
            link="https://example.com/article",
            published_at="20240115",
            excerpt=long_text,
            captured_at="2024-01-15T10:00:00+00:00",
            do_not_copy_text=True,
        )
        cleaned = clean_article(entry)
        self.assertEqual(len(cleaned.cleaned_excerpt), 500)

    def test_do_not_copy_text_preserved(self):
        entry = RssEntry(
            schema_version="v1",
            entry_id="test_entry",
            source_id="test_source",
            source_label="Test Source",
            is_official=False,
            title="Test Article",
            link="https://example.com/article",
            published_at="20240115",
            excerpt="Test excerpt",
            captured_at="2024-01-15T10:00:00+00:00",
            do_not_copy_text=True,
        )
        cleaned = clean_article(entry)
        self.assertTrue(cleaned.do_not_copy_text)


class TestCleanAllArticles(unittest.TestCase):
    def test_clean_all_articles(self):
        entries = (
            RssEntry(
                schema_version="v1",
                entry_id="entry1",
                source_id="source1",
                source_label="Source 1",
                is_official=False,
                title="Article 1",
                link="https://example.com/article1",
                published_at="20240115",
                excerpt="<p>Article 1 content</p>",
                captured_at="2024-01-15T10:00:00+00:00",
                do_not_copy_text=True,
            ),
            RssEntry(
                schema_version="v1",
                entry_id="entry2",
                source_id="source2",
                source_label="Source 2",
                is_official=True,
                title="Article 2",
                link="https://example.com/article2",
                published_at="20240115",
                excerpt="<p>Article 2 content</p>",
                captured_at="2024-01-15T10:00:00+00:00",
                do_not_copy_text=True,
            ),
        )
        report = clean_all_articles(entries)
        self.assertEqual(report.input_count, 2)
        self.assertEqual(report.output_count, 2)

    def test_clean_all_articles_empty(self):
        report = clean_all_articles(())
        self.assertEqual(report.input_count, 0)
        self.assertEqual(report.output_count, 0)


if __name__ == "__main__":
    unittest.main()