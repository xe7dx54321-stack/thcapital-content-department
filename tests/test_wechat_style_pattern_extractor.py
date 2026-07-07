import unittest

from content_system.wechat_style_pattern_extractor import (
    StylePattern,
    StyleAnalysis,
    StylePatternReport,
    has_long_citation,
    extract_patterns,
    analyze_style,
    analyze_all_styles,
    STYLE_PATTERNS,
)
from content_system.wechat_article_cleaner import CleanedArticle


class TestHasLongCitation(unittest.TestCase):
    def test_short_citation(self):
        text = '他说："这是一个简短的引用。"'
        has_long, warning = has_long_citation(text)
        self.assertFalse(has_long)
        self.assertIsNone(warning)

    def test_long_citation(self):
        long_text = "x" * 150
        text = f'他说："{long_text}"'
        has_long, warning = has_long_citation(text)
        self.assertTrue(has_long)
        self.assertIsNotNone(warning)

    def test_no_citation(self):
        text = "这是一段没有引用的普通文字。"
        has_long, warning = has_long_citation(text)
        self.assertFalse(has_long)
        self.assertIsNone(warning)

    def test_long_citation_chinese_quotes(self):
        long_text = "x" * 150
        text = f"他说：「{long_text}」"
        has_long, warning = has_long_citation(text)
        self.assertTrue(has_long)

    def test_long_citation_limit_100(self):
        text = '引用内容："' + "x" * 100 + '"'
        has_long, warning = has_long_citation(text)
        self.assertFalse(has_long)
        text = '引用内容："' + "x" * 101 + '"'
        has_long, warning = has_long_citation(text)
        self.assertTrue(has_long)


class TestExtractPatterns(unittest.TestCase):
    def test_extract_bullet_list(self):
        text = "- 第一项\n- 第二项\n- 第三项"
        patterns = extract_patterns(text)
        self.assertTrue(any(p.pattern_type == "bullet_list" for p in patterns))

    def test_extract_numbered_list(self):
        text = "1. 第一步\n2. 第二步\n3. 第三步"
        patterns = extract_patterns(text)
        self.assertTrue(any(p.pattern_type == "numbered_list" for p in patterns))

    def test_extract_bold_text(self):
        text = "重点内容【加粗显示】普通内容"
        patterns = extract_patterns(text)
        self.assertTrue(any(p.pattern_type == "bold_text" for p in patterns))

    def test_extract_statistic(self):
        text = "增长率达到50%，同比增长20%。"
        patterns = extract_patterns(text)
        self.assertTrue(any(p.pattern_type == "statistic_usage" for p in patterns))

    def test_extract_comparative(self):
        text = "相比之下，新方法更优。一方面性能更好，另一方面成本更低。"
        patterns = extract_patterns(text)
        self.assertTrue(any(p.pattern_type == "comparative_structure" for p in patterns))

    def test_multiple_patterns(self):
        text = "1. 第一步：完成基础设置\n2. 第二步：进行对比分析\n重点：【性能提升50%】增长率达到50%"
        patterns = extract_patterns(text)
        pattern_types = [p.pattern_type for p in patterns]
        self.assertIn("numbered_list", pattern_types)
        self.assertIn("bold_text", pattern_types)


class TestAnalyzeStyle(unittest.TestCase):
    def test_analyze_style_basic(self):
        article = CleanedArticle(
            schema_version="v1",
            entry_id="test_entry",
            source_id="test_source",
            title="Test Article",
            link="https://example.com/article",
            cleaned_excerpt="- 要点一\n- 要点二\n重点内容【加粗】",
            paragraphs=("- 要点一", "- 要点二", "重点内容【加粗】"),
            ad_removed=False,
            do_not_copy_text=True,
        )
        analysis = analyze_style(article)
        self.assertEqual(analysis.entry_id, "test_entry")
        self.assertEqual(analysis.title, "Test Article")
        self.assertFalse(analysis.has_long_citation)
        self.assertGreater(len(analysis.patterns), 0)

    def test_long_citation_detection(self):
        long_text = "x" * 150
        article = CleanedArticle(
            schema_version="v1",
            entry_id="test_entry",
            source_id="test_source",
            title="Test Article",
            link="https://example.com/article",
            cleaned_excerpt=f'引用："{long_text}"',
            paragraphs=(f'引用："{long_text}"',),
            ad_removed=False,
            do_not_copy_text=True,
        )
        analysis = analyze_style(article)
        self.assertTrue(analysis.has_long_citation)
        self.assertIsNotNone(analysis.citation_warning)


class TestAnalyzeAllStyles(unittest.TestCase):
    def test_analyze_all_styles(self):
        articles = (
            CleanedArticle(
                schema_version="v1",
                entry_id="entry1",
                source_id="source1",
                title="Article 1",
                link="https://example.com/article1",
                cleaned_excerpt="- 要点一\n- 要点二",
                paragraphs=("- 要点一", "- 要点二"),
                ad_removed=False,
                do_not_copy_text=True,
            ),
            CleanedArticle(
                schema_version="v1",
                entry_id="entry2",
                source_id="source2",
                title="Article 2",
                link="https://example.com/article2",
                cleaned_excerpt="1. 第一步\n2. 第二步",
                paragraphs=("1. 第一步", "2. 第二步"),
                ad_removed=False,
                do_not_copy_text=True,
            ),
        )
        report = analyze_all_styles(articles)
        self.assertEqual(report.input_count, 2)
        self.assertEqual(len(report.analyses), 2)

    def test_empty_input(self):
        report = analyze_all_styles(())
        self.assertEqual(report.input_count, 0)
        self.assertEqual(len(report.analyses), 0)


if __name__ == "__main__":
    unittest.main()
