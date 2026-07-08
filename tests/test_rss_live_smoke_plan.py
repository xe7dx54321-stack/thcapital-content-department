"""Phase36 tests: RSS Live Smoke Plan"""

import unittest
import sys
sys.path.insert(0, '/workspace/src')

from content_system.rss_live_smoke_plan import (
    build_rss_live_smoke_plan,
    SmokeTestPlanResult
)


class TestRssLiveSmokePlan(unittest.TestCase):

    def test_plan_generated(self):
        result = build_rss_live_smoke_plan()
        self.assertEqual(result.schema_version, "v1")
        self.assertEqual(result.status, "plan_generated")

    def test_max_sources_limited(self):
        result = build_rss_live_smoke_plan()
        self.assertEqual(result.max_sources, 2)
        self.assertEqual(result.max_articles_per_source, 20)

    def test_no_secret_in_output(self):
        result = build_rss_live_smoke_plan()
        # Should not contain real RSS URL
        for step in result.steps:
            if "env" in step.command.lower():
                self.assertTrue("https://" not in step.command)

    def test_env_allowlist_no_real_url(self):
        result = build_rss_live_smoke_plan()
        for env in result.env_allowlist:
            # Should only be env variable names, not URLs
            self.assertTrue("https://" not in env)
            self.assertTrue(env.endswith("_RSS_URL"))

    def test_requires_real_execution_false_in_cloud(self):
        result = build_rss_live_smoke_plan()
        self.assertFalse(result.requires_real_execution)
        self.assertFalse(result.enabled)

    def test_safety_rules_defined(self):
        result = build_rss_live_smoke_plan()
        self.assertIn("no_secret_in_output", result.safety_rules)
        self.assertIn("no_fulltext_in_git", result.safety_rules)
        self.assertIn("no_auto_publish", result.safety_rules)

    def test_validation_fields_defined(self):
        result = build_rss_live_smoke_plan()
        self.assertTrue("boundary_gate_status" in result.validation_fields)
        self.assertTrue("workbench_panel_visible" in result.validation_fields)

    def test_to_dict_serialization(self):
        result = build_rss_live_smoke_plan()
        data = result.to_dict()
        self.assertIn("max_sources", data)
        self.assertIn("steps", data)


if __name__ == "__main__":
    unittest.main()