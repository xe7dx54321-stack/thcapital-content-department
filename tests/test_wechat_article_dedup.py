import unittest

from content_system.wechat_article_dedup import (
    DedupResult,
    DedupReport,
    normalize_text,
    jaccard_similarity,
    text_hash,
    url_hash,
    is_url_duplicate,
    is_title_duplicate,
    is_content_duplicate,
    deduplicate_articles,
    get_unique_results,
)
from content_system.wechat_article_cleaner import CleanedArticle


class TestNormalizeText(unittest.TestCase):
    def test_normalize_lowercase(self):
        text = "Hello World"
        result = normalize_text(text)
        self.assertEqual(result, "hello world")

    def test_normalize_remove_punctuation(self):
        text = "Hello, World! How are you?"
        result = normalize_text(text)
        self.assertEqual(result, "hello world how are you")

    def test_normalize_remove_excessive_whitespace(self):
        text = "Hello   world   with   spaces"
        result = normalize_text(text)
        self.assertEqual(result, "hello world with spaces")


class TestJaccardSimilarity(unittest.TestCase):
    def test_identical_text(self):
        similarity = jaccard_similarity("Hello world", "Hello world")
        self.assertEqual(similarity, 1.0)

    def test_completely_different(self):
        similarity = jaccard_similarity("Hello world", "Goodbye moon")
        self.assertEqual(similarity, 0.0)

    def test_partially_similar(self):
        similarity = jaccard_similarity("Hello world today", "Hello world tomorrow")
        self.assertGreaterEqual(similarity, 0.5)
        self.assertLess(similarity, 1.0)


class TestTextHash(unittest.TestCase):
    def test_text_hash_consistency(self):
        hash1 = text_hash("Hello world")
        hash2 = text_hash("Hello world")
        self.assertEqual(hash1, hash2)

    def test_text_hash_different(self):
        hash1 = text_hash("Hello world")
        hash2 = text_hash("Goodbye world")
        self.assertNotEqual(hash1, hash2)

    def test_text_hash_length(self):
        result = text_hash("Hello world")
        self.assertEqual(len(result), 16)


class TestUrlHash(unittest.TestCase):
    def test_url_hash_consistency(self):
        hash1 = url_hash("https://example.com/article")
        hash2 = url_hash("https://example.com/article")
        self.assertEqual(hash1, hash2)

    def test_url_hash_ignore_query_params(self):
        hash1 = url_hash("https://example.com/article?param=1")
        hash2 = url_hash("https://example.com/article?param=2")
        self.assertEqual(hash1, hash2)

    def test_url_hash_case_insensitive(self):
        hash1 = url_hash("https://Example.com/Article")
        hash2 = url_hash("https://example.com/article")
        self.assertEqual(hash1, hash2)


class TestIsUrlDuplicate(unittest.TestCase):
    def test_url_duplicate(self):
        seen_urls = {"hash1"}
        url = "https://example.com/article"
        h = url_hash(url)
        seen_urls.add(h)
        is_dup, dup_hash = is_url_duplicate(url, seen_urls)
        self.assertTrue(is_dup)
        self.assertEqual(dup_hash, h)

    def test_url_not_duplicate(self):
        seen_urls = set()
        url = "https://example.com/article"
        is_dup, dup_hash = is_url_duplicate(url, seen_urls)
        self.assertFalse(is_dup)
        self.assertIsNone(dup_hash)


class TestIsTitleDuplicate(unittest.TestCase):
    def test_title_duplicate(self):
        seen_titles = {"hash1": "Hello world article"}
        is_dup, dup_hash = is_title_duplicate("Hello world article", seen_titles)
        self.assertTrue(is_dup)

    def test_title_similar(self):
        seen_titles = {"hash1": "Hello world article about AI technology"}
        is_dup, dup_hash = is_title_duplicate("Hello world article about AI technology", seen_titles)
        self.assertTrue(is_dup)

    def test_title_not_duplicate(self):
        seen_titles = {"hash1": "Hello world article"}
        is_dup, dup_hash = is_title_duplicate("Completely different article", seen_titles)
        self.assertFalse(is_dup)


class TestIsContentDuplicate(unittest.TestCase):
    def test_content_duplicate(self):
        seen_contents = {"hash1": "This is a test content"}
        is_dup, dup_hash = is_content_duplicate("This is a test content", seen_contents)
        self.assertTrue(is_dup)

    def test_content_similar(self):
        seen_contents = {"hash1": "This is a test content about AI technology"}
        is_dup, dup_hash = is_content_duplicate("This is a test content about AI technology", seen_contents)
        self.assertTrue(is_dup)

    def test_content_not_duplicate(self):
        seen_contents = {"hash1": "This is a test content"}
        is_dup, dup_hash = is_content_duplicate("Completely different content", seen_contents)
        self.assertFalse(is_dup)


class TestDeduplicateArticles(unittest.TestCase):
    def test_url_deduplication(self):
        article1 = CleanedArticle(
            schema_version="v1",
            entry_id="entry1",
            source_id="source1",
            title="Test Article",
            link="https://example.com/article",
            cleaned_excerpt="Content 1",
            paragraphs=("Content 1",),
            ad_removed=False,
            do_not_copy_text=True,
        )
        article2 = CleanedArticle(
            schema_version="v1",
            entry_id="entry2",
            source_id="source2",
            title="Test Article",
            link="https://example.com/article",
            cleaned_excerpt="Content 2",
            paragraphs=("Content 2",),
            ad_removed=False,
            do_not_copy_text=True,
        )
        report = deduplicate_articles((article1, article2))
        self.assertEqual(report.unique_count, 1)
        self.assertEqual(report.duplicate_count, 1)
        self.assertTrue(report.results[1].is_duplicate)
        self.assertEqual(report.results[1].duplicate_reason, "url_match")

    def test_title_deduplication(self):
        article1 = CleanedArticle(
            schema_version="v1",
            entry_id="entry1",
            source_id="source1",
            title="Test Article about AI Technology",
            link="https://example.com/article1",
            cleaned_excerpt="Content 1",
            paragraphs=("Content 1",),
            ad_removed=False,
            do_not_copy_text=True,
        )
        article2 = CleanedArticle(
            schema_version="v1",
            entry_id="entry2",
            source_id="source2",
            title="Test Article about AI Technology",
            link="https://example.com/article2",
            cleaned_excerpt="Content 2",
            paragraphs=("Content 2",),
            ad_removed=False,
            do_not_copy_text=True,
        )
        report = deduplicate_articles((article1, article2))
        self.assertEqual(report.unique_count, 1)
        self.assertTrue(report.results[1].is_duplicate)
        self.assertEqual(report.results[1].duplicate_reason, "title_similarity")

    def test_content_deduplication(self):
        article1 = CleanedArticle(
            schema_version="v1",
            entry_id="entry1",
            source_id="source1",
            title="Article 1",
            link="https://example.com/article1",
            cleaned_excerpt="This is the same content across different sources",
            paragraphs=("This is the same content across different sources",),
            ad_removed=False,
            do_not_copy_text=True,
        )
        article2 = CleanedArticle(
            schema_version="v1",
            entry_id="entry2",
            source_id="source2",
            title="Article 2",
            link="https://example.com/article2",
            cleaned_excerpt="This is the same content across different sources",
            paragraphs=("This is the same content across different sources",),
            ad_removed=False,
            do_not_copy_text=True,
        )
        report = deduplicate_articles((article1, article2))
        self.assertEqual(report.unique_count, 1)
        self.assertTrue(report.results[1].is_duplicate)
        self.assertEqual(report.results[1].duplicate_reason, "content_similarity")

    def test_no_duplicates(self):
        article1 = CleanedArticle(
            schema_version="v1",
            entry_id="entry1",
            source_id="source1",
            title="Article 1",
            link="https://example.com/article1",
            cleaned_excerpt="Content 1",
            paragraphs=("Content 1",),
            ad_removed=False,
            do_not_copy_text=True,
        )
        article2 = CleanedArticle(
            schema_version="v1",
            entry_id="entry2",
            source_id="source2",
            title="Article 2",
            link="https://example.com/article2",
            cleaned_excerpt="Content 2",
            paragraphs=("Content 2",),
            ad_removed=False,
            do_not_copy_text=True,
        )
        report = deduplicate_articles((article1, article2))
        self.assertEqual(report.unique_count, 2)
        self.assertEqual(report.duplicate_count, 0)


class TestGetUniqueResults(unittest.TestCase):
    def test_get_unique_results(self):
        results = (
            DedupResult(
                schema_version="v1",
                entry_id="entry1",
                source_id="source1",
                title="Article 1",
                link="https://example.com/article1",
                is_duplicate=False,
                duplicate_of=None,
                duplicate_reason=None,
                do_not_copy_text=True,
            ),
            DedupResult(
                schema_version="v1",
                entry_id="entry2",
                source_id="source2",
                title="Article 2",
                link="https://example.com/article2",
                is_duplicate=True,
                duplicate_of="hash",
                duplicate_reason="url_match",
                do_not_copy_text=True,
            ),
        )
        report = DedupReport(
            schema_version="v1",
            generated_at="2024-01-15T10:00:00+00:00",
            run_date="20240115",
            input_count=2,
            unique_count=1,
            duplicate_count=1,
            results=results,
            warnings=(),
        )
        unique = get_unique_results(report)
        self.assertEqual(len(unique), 1)
        self.assertEqual(unique[0].entry_id, "entry1")


if __name__ == "__main__":
    unittest.main()