from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from content_system.runtime_acquisition_router import build_route_plan_from_readiness
from content_system.runtime_network_readiness import check_runtime_network_readiness


class RuntimeNetworkRoutingTests(unittest.TestCase):
    def test_network_modes(self) -> None:
        old = os.environ.get("THCAP_RUNTIME_NETWORK_MODE")
        try:
            for mode in ("FULL", "DOMESTIC_ONLY", "OFFLINE"):
                os.environ["THCAP_RUNTIME_NETWORK_MODE"] = mode
                readiness = check_runtime_network_readiness()
                self.assertEqual(readiness["status"], mode)
                route = build_route_plan_from_readiness(readiness)
                self.assertGreaterEqual(route["summary"]["route_count"], 1)
            os.environ["THCAP_RUNTIME_NETWORK_MODE"] = "OFFLINE"
            route = build_route_plan_from_readiness(check_runtime_network_readiness())
            actions = {item["action"] for item in route["routes"]}
            self.assertIn("QUEUE_RETRY", actions)
            self.assertIn("RUN_NOW", actions)
        finally:
            if old is None:
                os.environ.pop("THCAP_RUNTIME_NETWORK_MODE", None)
            else:
                os.environ["THCAP_RUNTIME_NETWORK_MODE"] = old


if __name__ == "__main__":
    unittest.main()
