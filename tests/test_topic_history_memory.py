import unittest
from pathlib import Path
from datetime import datetime, timedelta

from content_system.topic_history_memory import (
    TopicHistoryReport,
    HistoricalTopic,
    build_topic_history_memory,
    report_to_dict,
    write_report,
    load_report,
    normalize_title,
)


class TestTopicHistoryMemory(unittest.TestCase):
    def test_build_topic_history_memory_without_data(self):
        repo_root = Path("/tmp/test_history_no_data")
        repo_root.mkdir(parents=True, exist_ok=True)
        report = build_topic_history_memory(repo_root, run_date="20260707")
        self.assertIsInstance(report, TopicHistoryReport)
        self.assertEqual(report.schema_version, "v1")
        self.assertEqual(report.run_date, "20260707")
        self.assertEqual(report.history_window_days, 7)
        self.assertEqual(len(report.historical_topics), 0)
        self.assertGreater(len(report.warnings), 0)

    def test_build_topic_history_memory_with_sample_data(self):
        repo_root = Path("/tmp/test_history_with_data")
        repo_root.mkdir(parents=True, exist_ok=True)
        report = build_topic_history_memory(repo_root, run_date="20260707", history_window_days=3)
        self.assertIsInstance(report, TopicHistoryReport)
        self.assertEqual(report.history_window_days, 3)

    def test_normalize_title(self):
        title = "  OpenAI 发布 GPT-5 技术细节分析  "
        normalized = normalize_title(title)
        self.assertEqual(normalized, "openai 发布 gpt 5 技术细节分析")

    def test_report_to_dict(self):
        repo_root = Path("/tmp/test_history_dict")
        repo_root.mkdir(parents=True, exist_ok=True)
        report = build_topic_history_memory(repo_root, run_date="20260707")
        data = report_to_dict(report)
        self.assertIsInstance(data, dict)
        self.assertIn("schema_version", data)
        self.assertIn("generated_at", data)
        self.assertIn("run_date", data)
        self.assertIn("historical_topics", data)

    def test_write_and_load_report(self):
        repo_root = Path("/tmp/test_history_io")
        repo_root.mkdir(parents=True, exist_ok=True)
        report = build_topic_history_memory(repo_root, run_date="20260707")
        output_path = str(repo_root / "test_history")
        write_report(report, output_path)

        loaded = load_report(output_path + ".json")
        self.assertIsInstance(loaded, TopicHistoryReport)
        self.assertEqual(loaded.schema_version, report.schema_version)
        self.assertEqual(loaded.run_date, report.run_date)

    def test_historical_topic_dataclass(self):
        topic = HistoricalTopic(
            topic_id="topic_001",
            title="Test Topic",
            run_date="20260707",
            topic_type="main",
            source_id="test_source",
            lane="tech",
            event_type="model_release",
            angle_type="technical",
            companies=("OpenAI",),
            products=("GPT-5",),
            score=0.85,
            normalized_title="test topic",
        )
        self.assertEqual(topic.topic_id, "topic_001")
        self.assertEqual(topic.topic_type, "main")
        self.assertEqual(topic.score, 0.85)


if __name__ == "__main__":
    unittest.main()
