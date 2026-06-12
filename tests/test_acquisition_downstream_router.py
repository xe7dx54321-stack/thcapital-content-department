from __future__ import annotations

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from content_system.acquisition_downstream_router import load_downstream_routes, validate_downstream_routes


class AcquisitionDownstreamRouterTest(unittest.TestCase):
    def test_weak_signal_not_direct_brief(self) -> None:
        payload = validate_downstream_routes(ROOT)
        self.assertEqual(payload["status"], "PASS")
        routes = load_downstream_routes(ROOT)
        for lane in ("reddit_llm_discussion", "youtube_signal", "x_signal", "trend_heat_validation"):
            self.assertNotIn("brief_candidate", str(routes[lane]))

    def test_manual_source_not_direct_topic_output(self) -> None:
        routes = load_downstream_routes(ROOT)
        self.assertNotIn("topic_scoring", str(routes["wechat_metadata"].get("outputs", [])))


if __name__ == "__main__":
    unittest.main()
