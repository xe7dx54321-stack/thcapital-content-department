import unittest

from content_system.wechat_article_intelligence import (
    ArticleIntelligence,
    IntelligenceReport,
    extract_entities,
    extract_angles,
    extract_claims,
    extract_patterns,
    extract_intelligence,
    extract_all_intelligence,
)
from content_system.wechat_article_cleaner import CleanedArticle


class TestExtractEntities(unittest.TestCase):
    def test_extract_companies(self):
        text = "OpenAI发布了新的GPT模型，Anthropic也推出了Claude。"
        entities = extract_entities(text)
        companies = [e for e in entities if e.entity_type == "company"]
        self.assertTrue(any(e.name == "OpenAI" for e in companies))
        self.assertTrue(any(e.name == "Anthropic" for e in companies))

    def test_extract_models(self):
        text = "GPT-4和Claude 3都是强大的大模型。"
        entities = extract_entities(text)
        models = [e for e in entities if e.entity_type == "model"]
        self.assertTrue(any(e.name == "GPT" for e in models))
        self.assertTrue(any(e.name == "Claude" for e in models))

    def test_extract_people(self):
        text = "Sam Altman和Jensen Huang讨论AI的未来。"
        entities = extract_entities(text)
        people = [e for e in entities if e.entity_type == "person"]
        self.assertTrue(any(e.name == "Sam Altman" for e in people))
        self.assertTrue(any(e.name == "Jensen Huang" for e in people))

    def test_no_entities(self):
        text = "这是一篇没有任何已知实体的文章。"
        entities = extract_entities(text)
        self.assertEqual(len(entities), 0)


class TestExtractAngles(unittest.TestCase):
    def test_extract_technical_angle(self):
        text = "本文深入分析GPT-4的技术架构和训练原理。"
        angles = extract_angles(text)
        self.assertTrue(any(a.angle_name == "技术深度" for a in angles))

    def test_extract_business_angle(self):
        text = "AI市场增长迅速，估值不断上升。"
        angles = extract_angles(text)
        self.assertTrue(any(a.angle_name == "商业分析" for a in angles))

    def test_extract_multiple_angles(self):
        text = "技术架构先进，市场前景广阔，与竞品相比优势明显。"
        angles = extract_angles(text)
        angle_names = [a.angle_name for a in angles]
        self.assertIn("技术深度", angle_names)
        self.assertIn("商业分析", angle_names)
        self.assertIn("产品对比", angle_names)

    def test_at_least_11_angles_available(self):
        from content_system.wechat_article_intelligence import ANGLE_KEYWORDS
        self.assertGreaterEqual(len(ANGLE_KEYWORDS), 11)


class TestExtractClaims(unittest.TestCase):
    def test_extract_claims(self):
        text = "OpenAI宣称GPT-4性能提升了50%。据报道，市场反应积极。"
        claims = extract_claims(text)
        self.assertGreaterEqual(len(claims), 1)

    def test_claim_confidence(self):
        text = "公司表示新产品将改变行业格局。"
        claims = extract_claims(text)
        if claims:
            self.assertEqual(claims[0].confidence, 0.7)

    def test_no_claims(self):
        text = "这是一段普通的描述性文字，没有任何宣称。"
        claims = extract_claims(text)
        self.assertEqual(len(claims), 0)


class TestExtractPatterns(unittest.TestCase):
    def test_extract_quantitative_pattern(self):
        text = "增长率达到50%，市场份额占30%。"
        patterns = extract_patterns(text)
        self.assertTrue(any(p.pattern_type == "quantitative" for p in patterns))

    def test_extract_example_pattern(self):
        text = "例如，在医疗领域的应用就非常广泛。"
        patterns = extract_patterns(text)
        self.assertTrue(any(p.pattern_type == "example_based" for p in patterns))

    def test_extract_comparative_pattern(self):
        text = "相比传统方法，新方法具有明显优势。"
        patterns = extract_patterns(text)
        self.assertTrue(any(p.pattern_type == "comparative" for p in patterns))


class TestExtractIntelligence(unittest.TestCase):
    def test_extract_intelligence(self):
        article = CleanedArticle(
            schema_version="v1",
            entry_id="test_entry",
            source_id="test_source",
            title="Test Article about OpenAI GPT",
            link="https://example.com/article",
            cleaned_excerpt="OpenAI发布了GPT-4，技术架构先进，市场反应积极。",
            paragraphs=("OpenAI发布了GPT-4，技术架构先进，市场反应积极。",),
            ad_removed=False,
            do_not_copy_text=True,
        )
        intelligence = extract_intelligence(article)
        self.assertEqual(intelligence.entry_id, "test_entry")
        self.assertEqual(intelligence.title, "Test Article about OpenAI GPT")
        self.assertTrue(intelligence.do_not_copy_text)
        self.assertGreater(len(intelligence.entities), 0)
        self.assertGreater(len(intelligence.angles), 0)

    def test_do_not_copy_text_preserved(self):
        article = CleanedArticle(
            schema_version="v1",
            entry_id="test_entry",
            source_id="test_source",
            title="Test Article",
            link="https://example.com/article",
            cleaned_excerpt="Test content",
            paragraphs=("Test content",),
            ad_removed=False,
            do_not_copy_text=True,
        )
        intelligence = extract_intelligence(article)
        self.assertTrue(intelligence.do_not_copy_text)


class TestExtractAllIntelligence(unittest.TestCase):
    def test_extract_all_intelligence(self):
        articles = (
            CleanedArticle(
                schema_version="v1",
                entry_id="entry1",
                source_id="source1",
                title="Article 1",
                link="https://example.com/article1",
                cleaned_excerpt="OpenAI news",
                paragraphs=("OpenAI news",),
                ad_removed=False,
                do_not_copy_text=True,
            ),
            CleanedArticle(
                schema_version="v1",
                entry_id="entry2",
                source_id="source2",
                title="Article 2",
                link="https://example.com/article2",
                cleaned_excerpt="Anthropic updates",
                paragraphs=("Anthropic updates",),
                ad_removed=False,
                do_not_copy_text=True,
            ),
        )
        report = extract_all_intelligence(articles)
        self.assertEqual(report.input_count, 2)
        self.assertEqual(report.output_count, 2)

    def test_empty_input(self):
        report = extract_all_intelligence(())
        self.assertEqual(report.input_count, 0)
        self.assertEqual(report.output_count, 0)


if __name__ == "__main__":
    unittest.main()