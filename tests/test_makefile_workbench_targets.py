"""Makefile target checks for the Workbench entrypoints."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class MakefileWorkbenchTargetsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.makefile = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")

    def test_wechat_workbench_frontend_target_exists(self) -> None:
        self.assertRegex(self.makefile, r"(?m)^wechat-workbench-frontend:")
        self.assertIn("scripts/build_wechat_workbench_frontend.py", self.makefile)

    def test_wechat_workbench_dependency_is_defined(self) -> None:
        dependency_line = re.search(r"(?m)^wechat-workbench:\s*(.+)$", self.makefile)
        self.assertIsNotNone(dependency_line)
        self.assertIn("wechat-workbench-frontend", dependency_line.group(1))

    def test_env_files_are_ignored(self) -> None:
        gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertRegex(gitignore, r"(?m)^\.env$")
        self.assertRegex(gitignore, r"(?m)^\.env\.rss$")


if __name__ == "__main__":
    unittest.main()
