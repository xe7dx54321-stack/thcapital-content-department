"""Repository path helper checks for local Mac execution."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402


class RepoPathsTest(unittest.TestCase):
    def test_paths_resolve_under_repo_root(self) -> None:
        paths = get_project_paths(REPO_ROOT)
        self.assertEqual(paths.repo_root, REPO_ROOT)
        self.assertEqual(paths.market_content_root, REPO_ROOT / "同行资本市场内容系统")
        self.assertEqual(paths.logs_root, REPO_ROOT / "同行资本市场内容系统" / "10_logs")

    def test_paths_work_from_non_repo_cwd_when_root_provided(self) -> None:
        old_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                os.chdir(temp_dir)
                paths = get_project_paths(REPO_ROOT)
            finally:
                os.chdir(old_cwd)
        self.assertEqual(paths.logs_root, REPO_ROOT / "同行资本市场内容系统" / "10_logs")


if __name__ == "__main__":
    unittest.main()
