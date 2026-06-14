import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from content_system.workbench_view_model import build_workbench_view_model_from_data
from workbench_vm_fixture import sample_workbench_data


class WorkbenchArticleWorkspaceTest(unittest.TestCase):
    def test_article_workspace_is_content_only(self):
        article = build_workbench_view_model_from_data(sample_workbench_data(), {})["today_article"]
        payload = json.dumps(article, ensure_ascii=False)
        self.assertIn("article_markdown", article)
        self.assertIn("agent_review_summary", article)
        self.assertNotIn("Runtime PID", payload)
        self.assertNotIn("LaunchAgent", payload)
        self.assertNotIn("OpenClaw", payload)
        self.assertNotIn("path-audit", payload)

    def test_article_actions_are_content_actions(self):
        actions = build_workbench_view_model_from_data(sample_workbench_data(), {})["today_article"]["actions"]
        labels = {item["label"] for item in actions}
        self.assertIn("复制正文", labels)
        self.assertIn("请求重写标题", labels)
        self.assertNotIn("暂停 Runtime", labels)


if __name__ == "__main__":
    unittest.main()
