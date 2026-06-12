from __future__ import annotations

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from content_system.openclaw_acquisition_semantics_audit import audit_job, infer_lane


class OpenClawAcquisitionSemanticsTest(unittest.TestCase):
    def test_old_cron_lane_inference(self) -> None:
        self.assertEqual(infer_lane("Reddit LocalLLaMA radar", ["trend__reddit_localllama_daily"]), "reddit_llm_discussion")
        self.assertEqual(infer_lane("YC launches and TechCrunch AI funding", ["web__yc_launches_ai"]), "funding_startup")

    def test_full_text_job_not_migrated(self) -> None:
        job = {"id": "wechat_fulltext", "agentId": "signal-harvester", "enabled": True, "message": "微信 全文 深抓"}
        audited = audit_job(job)
        self.assertEqual(audited["migration_value"], "NONE")


if __name__ == "__main__":
    unittest.main()
