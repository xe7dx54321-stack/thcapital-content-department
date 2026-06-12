from __future__ import annotations

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from content_system.acquisition_lane_registry import REQUIRED_LANES, validate_acquisition_lanes


class AcquisitionLaneRegistryTest(unittest.TestCase):
    def test_required_lanes_present(self) -> None:
        payload = validate_acquisition_lanes(ROOT)
        self.assertEqual(payload["status"], "PASS")
        self.assertGreaterEqual(payload["lane_count"], len(REQUIRED_LANES))
        self.assertGreater(payload["weak_signal_lane_count"], 0)


if __name__ == "__main__":
    unittest.main()
