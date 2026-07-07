import os
import unittest

from content_system.wechat_rss_source_registry import (
    WechatRssSource,
    WechatRssRegistry,
    resolve_env_variables,
    contains_forbidden_pattern,
    validate_source,
    validate_registry,
    source_from_mapping,
    registry_from_config,
)


class TestResolveEnvVariables(unittest.TestCase):
    def test_resolve_env_variable(self):
        os.environ["TEST_RSS_URL"] = "https://example.com/rss"
        result = resolve_env_variables("${TEST_RSS_URL}")
        self.assertEqual(result, "https://example.com/rss")

    def test_resolve_missing_env_variable(self):
        result = resolve_env_variables("${NONEXISTENT_VAR}")
        self.assertEqual(result, "${NONEXISTENT_VAR}")

    def test_resolve_multiple_env_variables(self):
        os.environ["PROTOCOL"] = "https"
        os.environ["DOMAIN"] = "example.com"
        result = resolve_env_variables("${PROTOCOL}://${DOMAIN}/rss")
        self.assertEqual(result, "https://example.com/rss")

    def test_no_env_variable(self):
        result = resolve_env_variables("https://example.com/rss")
        self.assertEqual(result, "https://example.com/rss")


class TestContainsForbiddenPattern(unittest.TestCase):
    def test_secret_in_url(self):
        url = "https://example.com/rss?secret=abc123"
        self.assertTrue(contains_forbidden_pattern(url))

    def test_token_in_url(self):
        url = "https://example.com/rss?token=xyz789"
        self.assertTrue(contains_forbidden_pattern(url))

    def test_api_key_in_url(self):
        url = "https://example.com/rss?api_key=secret_key"
        self.assertTrue(contains_forbidden_pattern(url))

    def test_password_in_url(self):
        url = "https://user:password@example.com/rss"
        self.assertTrue(contains_forbidden_pattern(url))

    def test_normal_url(self):
        url = "https://example.com/rss"
        self.assertFalse(contains_forbidden_pattern(url))

    def test_url_with_query_params(self):
        url = "https://example.com/rss?category=tech&limit=10"
        self.assertFalse(contains_forbidden_pattern(url))


class TestValidateSource(unittest.TestCase):
    def test_valid_source(self):
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
        issues = validate_source(source)
        errors = [i for i in issues if i.severity == "ERROR"]
        self.assertEqual(len(errors), 0)

    def test_invalid_source_id(self):
        source = WechatRssSource(
            schema_version="v1",
            source_id="Test-Source",
            label="Test Source",
            tier="A",
            language="zh",
            enabled=True,
            is_official=False,
            rss_url="https://example.com/rss",
            owner="test",
            notes="",
        )
        issues = validate_source(source)
        errors = [i for i in issues if i.severity == "ERROR"]
        self.assertTrue(any(i.field == "source_id" for i in errors))

    def test_invalid_tier(self):
        source = WechatRssSource(
            schema_version="v1",
            source_id="test_source",
            label="Test Source",
            tier="Z",
            language="zh",
            enabled=True,
            is_official=False,
            rss_url="https://example.com/rss",
            owner="test",
            notes="",
        )
        issues = validate_source(source)
        errors = [i for i in issues if i.severity == "ERROR"]
        self.assertTrue(any(i.field == "tier" for i in errors))

    def test_secret_url_detection(self):
        source = WechatRssSource(
            schema_version="v1",
            source_id="test_source",
            label="Test Source",
            tier="A",
            language="zh",
            enabled=True,
            is_official=False,
            rss_url="https://example.com/rss?secret=abc123",
            owner="test",
            notes="",
        )
        issues = validate_source(source)
        errors = [i for i in issues if i.severity == "ERROR"]
        self.assertTrue(any("sensitive" in i.message for i in errors))

    def test_official_configurable(self):
        source = WechatRssSource(
            schema_version="v1",
            source_id="test_source",
            label="Test Source",
            tier="A",
            language="zh",
            enabled=True,
            is_official=True,
            rss_url="https://example.com/rss",
            owner="test",
            notes="",
        )
        issues = validate_source(source)
        errors = [i for i in issues if i.severity == "ERROR"]
        self.assertEqual(len(errors), 0)


class TestValidateRegistry(unittest.TestCase):
    def test_valid_registry(self):
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
        registry = WechatRssRegistry(schema_version="v1", sources=(source,))
        issues = validate_registry(registry)
        errors = [i for i in issues if i.severity == "ERROR"]
        self.assertEqual(len(errors), 0)

    def test_empty_registry(self):
        registry = WechatRssRegistry(schema_version="v1", sources=())
        issues = validate_registry(registry)
        errors = [i for i in issues if i.severity == "ERROR"]
        self.assertTrue(any(i.field == "sources" for i in errors))

    def test_duplicate_source_id(self):
        source1 = WechatRssSource(
            schema_version="v1",
            source_id="test_source",
            label="Test Source 1",
            tier="A",
            language="zh",
            enabled=True,
            is_official=False,
            rss_url="https://example.com/rss1",
            owner="test",
            notes="",
        )
        source2 = WechatRssSource(
            schema_version="v1",
            source_id="test_source",
            label="Test Source 2",
            tier="A",
            language="zh",
            enabled=True,
            is_official=False,
            rss_url="https://example.com/rss2",
            owner="test",
            notes="",
        )
        registry = WechatRssRegistry(schema_version="v1", sources=(source1, source2))
        issues = validate_registry(registry)
        errors = [i for i in issues if i.severity == "ERROR"]
        self.assertTrue(any("unique" in i.message for i in errors))


class TestSourceFromMapping(unittest.TestCase):
    def test_source_from_mapping(self):
        mapping = {
            "source_id": "test_source",
            "label": "Test Source",
            "tier": "B",
            "language": "en",
            "enabled": True,
            "is_official": False,
            "rss_url": "${TEST_URL}",
            "owner": "test",
            "notes": "Test notes",
        }
        source = source_from_mapping(mapping)
        self.assertEqual(source.source_id, "test_source")
        self.assertEqual(source.tier, "B")
        self.assertTrue(source.enabled)
        self.assertFalse(source.is_official)
        self.assertEqual(source.rss_url, "${TEST_URL}")

    def test_default_values(self):
        mapping = {"source_id": "test", "owner": "test"}
        source = source_from_mapping(mapping)
        self.assertEqual(source.tier, "C")
        self.assertEqual(source.language, "zh")
        self.assertTrue(source.enabled)
        self.assertFalse(source.is_official)


class TestRegistryFromConfig(unittest.TestCase):
    def test_registry_from_config(self):
        config = {
            "sources": [
                {"source_id": "test1", "label": "Test 1", "tier": "A", "owner": "test", "rss_url": "https://example.com/rss1"},
                {"source_id": "test2", "label": "Test 2", "tier": "B", "owner": "test", "rss_url": "https://example.com/rss2"},
            ]
        }
        registry = registry_from_config(config)
        self.assertEqual(len(registry.sources), 2)
        self.assertEqual(registry.sources[0].source_id, "test1")
        self.assertEqual(registry.sources[1].source_id, "test2")

    def test_empty_config(self):
        config = {}
        registry = registry_from_config(config)
        self.assertEqual(len(registry.sources), 0)


if __name__ == "__main__":
    unittest.main()