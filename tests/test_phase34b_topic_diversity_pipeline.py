import unittest
from pathlib import Path
import shutil

from content_system.phase34b_topic_diversity_pipeline import (
    PipelineOutput,
    PipelineConfig,
    run_pipeline,
    pipeline_to_dict,
    write_pipeline_output,
    load_topic_diversity_policy,
    load_differentiated_angle_policy,
    load_candidates,
)


class TestPhase34bTopicDiversityPipeline(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("/tmp/test_pipeline")
        self.test_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_run_pipeline_basic(self):
        config = PipelineConfig(dry_run=True, run_date="20260707", output_dir="test_output")
        output = run_pipeline(self.test_dir, config)
        self.assertIsInstance(output, PipelineOutput)
        self.assertEqual(output.schema_version, "v1")
        self.assertEqual(output.run_date, "20260707")
        self.assertTrue(output.dry_run)

    def test_pipeline_all_reports_generated(self):
        config = PipelineConfig(dry_run=True, run_date="20260707", output_dir="test_output")
        output = run_pipeline(self.test_dir, config)

        self.assertIsInstance(output.history_report, dict)
        self.assertIsInstance(output.similarity_report, dict)
        self.assertIsInstance(output.source_lane_report, dict)
        self.assertIsInstance(output.competitive_penalty_report, dict)
        self.assertIsInstance(output.angle_boost_report, dict)
        self.assertIsInstance(output.title_guard_report, dict)
        self.assertIsInstance(output.diversity_report, dict)
        self.assertIsInstance(output.reranking_report, dict)
        self.assertIsInstance(output.brief_integration_report, dict)

    def test_pipeline_outputs_written(self):
        config = PipelineConfig(dry_run=True, run_date="20260707", output_dir="test_output")
        output = run_pipeline(self.test_dir, config)

        self.assertIn("history", output.outputs)
        self.assertIn("similarity", output.outputs)
        self.assertIn("source_lane", output.outputs)
        self.assertIn("competitive_penalty", output.outputs)
        self.assertIn("angle_boost", output.outputs)
        self.assertIn("title_guard", output.outputs)
        self.assertIn("diversity", output.outputs)
        self.assertIn("reranking", output.outputs)
        self.assertIn("brief_integration", output.outputs)

    def test_pipeline_with_sample_candidates(self):
        config = PipelineConfig(dry_run=True, run_date="20260707", output_dir="test_output")
        output = run_pipeline(self.test_dir, config)

        diversity = output.diversity_report
        self.assertGreater(diversity.get("candidate_count", 0), 0)

    def test_cloud_mode_no_rss_required(self):
        config = PipelineConfig(dry_run=True, run_date="20260707", output_dir="test_output")
        output = run_pipeline(self.test_dir, config)

        self.assertIn("No candidates found; using sample data for dry-run", output.warnings)
        self.assertIsInstance(output, PipelineOutput)

    def test_load_topic_diversity_policy(self):
        policy = load_topic_diversity_policy(self.test_dir)
        self.assertIsInstance(policy, dict)

    def test_load_differentiated_angle_policy(self):
        policy = load_differentiated_angle_policy(self.test_dir)
        self.assertIsInstance(policy, dict)

    def test_load_candidates_no_files(self):
        candidates = load_candidates(self.test_dir, "20260707")
        self.assertEqual(candidates, [])

    def test_pipeline_to_dict(self):
        config = PipelineConfig(dry_run=True, run_date="20260707", output_dir="test_output")
        output = run_pipeline(self.test_dir, config)
        data = pipeline_to_dict(output)
        self.assertIsInstance(data, dict)

    def test_write_pipeline_output(self):
        config = PipelineConfig(dry_run=True, run_date="20260707", output_dir="test_output")
        output = run_pipeline(self.test_dir, config)
        output_path = str(self.test_dir / "pipeline_output")
        write_pipeline_output(output, output_path)
        output_file = Path(output_path + ".json")
        self.assertTrue(output_file.exists())


if __name__ == "__main__":
    unittest.main()
