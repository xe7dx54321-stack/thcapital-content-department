"""Phase36 tests: Rollback Safety Runbook"""

import unittest
import sys
sys.path.insert(0, '/workspace/src')

from content_system.rollback_safety_runbook import (
    build_rollback_safety_runbook,
    RollbackRunbookResult
)


class TestRollbackSafetyRunbook(unittest.TestCase):

    def test_runbook_generated(self):
        result = build_rollback_safety_runbook()
        self.assertEqual(result.schema_version, "v1")
        self.assertEqual(result.status, "runbook_generated")

    def test_contains_pause_resume(self):
        result = build_rollback_safety_runbook()
        self.assertTrue(result.contains_pause_resume)
        # Check that pause and resume sections exist
        pause_section = [s for s in result.sections if s.section_id == "pause_runtime"]
        resume_section = [s for s in result.sections if s.section_id == "resume_runtime"]
        self.assertTrue(len(pause_section) == 1)
        self.assertTrue(len(resume_section) == 1)

    def test_contains_disable_rss(self):
        result = build_rollback_safety_runbook()
        self.assertTrue(result.contains_disable_rss)
        disable_section = [s for s in result.sections if s.section_id == "disable_rss"]
        self.assertTrue(len(disable_section) == 1)

    def test_section_count_sufficient(self):
        result = build_rollback_safety_runbook()
        self.assertTrue(result.section_count >= 8)

    def test_stop_observation_section_exists(self):
        result = build_rollback_safety_runbook()
        stop_section = [s for s in result.sections if s.section_id == "stop_observation"]
        self.assertTrue(len(stop_section) == 1)
        # Should mention what conditions require stopping
        self.assertTrue("泄漏" in stop_section[0].notes or "secret" in stop_section[0].notes.lower())

    def test_git_commands_included(self):
        result = build_rollback_safety_runbook()
        rollback_section = [s for s in result.sections if s.section_id == "rollback_commit"]
        self.assertTrue(len(rollback_section) == 1)
        self.assertTrue(any("git" in cmd for cmd in rollback_section[0].commands))

    def test_to_dict_serialization(self):
        result = build_rollback_safety_runbook()
        data = result.to_dict()
        self.assertIn("sections", data)
        self.assertIn("contains_pause_resume", data)


if __name__ == "__main__":
    unittest.main()