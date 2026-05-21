#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import market_top20_continuity_board_builder as continuity_builder
from market_approved_topic_builder import load_candidates


ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
BOARD_20260413 = ROOT / "03_topic_candidates" / "20260413__daily-top8-to-top5.md"
PACK_20260413 = ROOT / "03_topic_candidates" / "20260413__top20-screening-pack.md"
REWORKED_PACK_20260413 = ROOT / "03_topic_candidates" / "20260413__top20-screening-pack__reworked.md"
SCORECARD_20260413 = ROOT / "10_logs" / "20260413__top20__stage-gate-scorecard.md"
BOARD_20260412 = ROOT / "03_topic_candidates" / "20260412__daily-top8-to-top5.md"
PACK_20260414 = ROOT / "03_topic_candidates" / "20260414__top20-screening-pack.md"
REWORKED_PACK_20260414 = ROOT / "03_topic_candidates" / "20260414__top20-screening-pack__reworked.md"
SCORECARD_20260414 = ROOT / "10_logs" / "20260414__top20__stage-gate-scorecard.md"


class DayMainlineParserRegressionTest(unittest.TestCase):
    def test_continuity_builder_reads_current_mini_slate_schema(self) -> None:
        pack_items = continuity_builder.merge_pack_items(
            continuity_builder.parse_pack(PACK_20260413),
            continuity_builder.parse_pack(REWORKED_PACK_20260413),
        )
        scorecard_text = SCORECARD_20260413.read_text(encoding="utf-8")
        parsed = continuity_builder.parse_mini_slate(scorecard_text, pack_items)

        self.assertGreaterEqual(len(parsed), 10)
        self.assertEqual(parsed[0].topic_key, "ai-pricing-wave-2026")

    def test_load_candidates_reads_current_top5_board_schema(self) -> None:
        candidates = load_candidates(BOARD_20260413)

        self.assertEqual(len(candidates), 8)
        self.assertEqual(candidates[1].candidate_key, "ai-pricing-wave-2026")
        self.assertIn("AI 涨价潮", candidates[1].title)
        self.assertEqual(candidates[6].selection_bucket, "holdout")

    def test_load_candidates_reads_legacy_top5_board_schema(self) -> None:
        candidates = load_candidates(BOARD_20260412)

        self.assertEqual(len(candidates), 8)
        self.assertEqual(candidates[1].candidate_key, "cirrus_labs_join_openai_20260412")
        self.assertEqual(candidates[6].selection_bucket, "holdout")

    def test_continuity_builder_reads_table_backed_scorecard_schema(self) -> None:
        pack_items = continuity_builder.merge_pack_items(
            continuity_builder.parse_pack(PACK_20260414),
            continuity_builder.parse_pack(REWORKED_PACK_20260414),
        )
        scorecard_text = SCORECARD_20260414.read_text(encoding="utf-8")
        scorecard_fields = continuity_builder.parse_fields(SCORECARD_20260414)
        parsed = continuity_builder.parse_mini_slate(scorecard_text, pack_items)

        self.assertEqual(continuity_builder.normalize_continuity_decision(scorecard_fields.get("continuity_decision", "")), "continuity_only")
        self.assertEqual(continuity_builder.normalize_continuity_output(scorecard_fields.get("continuity_output", "")), "top20_mini_slate")
        self.assertEqual(continuity_builder.extract_total_score(scorecard_text, scorecard_fields), 72.0)
        self.assertGreaterEqual(len(parsed), 8)
        self.assertEqual(parsed[0].topic_key, "apple_siri_wwdc_2026_overhaul")
        self.assertEqual(parsed[1].topic_key, "feishu_cli_open_source_agent_operations")


if __name__ == "__main__":
    unittest.main()
