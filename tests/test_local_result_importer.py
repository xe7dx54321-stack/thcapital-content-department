"""Phase37A tests: Local Result Importer"""
import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.local_result_importer import import_local_results


class TestLocalResultImporter(unittest.TestCase):

    def test_no_local_results_no_failure(self):
        """无本地结果时不失败"""
        result = import_local_results(Path("/tmp/nonexistent_dir"))
        self.assertEqual(result.status, "NO_LOCAL_RESULTS_FOUND")
        self.assertEqual(result.local_result_count, 0)
        self.assertTrue(result.missing_file_count > 0)

    def test_empty_dir_no_failure(self):
        """空目录不失败"""
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            result = import_local_results(Path(tmpdir))
            self.assertEqual(result.status, "NO_LOCAL_RESULTS_FOUND")
            self.assertEqual(result.local_result_count, 0)

    def test_missing_files_tracked(self):
        result = import_local_results(Path("/tmp/nonexistent"))
        self.assertTrue(len(result.missing_files) > 0)

    def test_recommended_next_action_defined(self):
        result = import_local_results(Path("/tmp/nonexistent"))
        self.assertTrue(len(result.recommended_next_action) > 0)

    def test_to_dict(self):
        result = import_local_results(Path("/tmp/nonexistent"))
        data = result.to_dict()
        self.assertIn("status", data)
        self.assertIn("local_result_count", data)
        self.assertIn("missing_files", data)


if __name__ == "__main__":
    unittest.main()
