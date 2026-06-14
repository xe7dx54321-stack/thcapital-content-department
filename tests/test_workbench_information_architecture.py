import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from content_system.wechat_workbench_frontend import render_workbench_html
from content_system.workbench_view_model import build_workbench_view_model_from_data
from content_system.paths import get_project_paths
from workbench_vm_fixture import sample_workbench_data


class WorkbenchInformationArchitectureTest(unittest.TestCase):
    def test_frontend_has_five_chinese_nav_views(self):
        data = sample_workbench_data()
        data["workbench_view_model"] = build_workbench_view_model_from_data(data, {})
        html = render_workbench_html(data, get_project_paths(ROOT))
        for label in ["今日总览", "今日稿件", "质量检查", "历史回放", "系统运维"]:
            self.assertIn(label, html)
        self.assertIn('id="view-overview"', html)
        self.assertIn('class="view active"', html)


if __name__ == "__main__":
    unittest.main()
