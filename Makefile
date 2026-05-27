.PHONY: doctor path-audit sources-validate source-health source-runtime-health manifest-validate manifest-write-from-packets official-lane-with-manifest official-lane-health-check official-lane-daily daily-official-lane daily-source-summary official-lane-quality-gate daily-official-quality-gate official-daily-dashboard daily-official-dashboard official-daily-full-run daily-official-full-run runtime-baseline source-coverage evidence-packets topic-clusters value-scores high-value-candidates phase1-daily content-briefs content-outlines content-drafts content-quality-review platform-packages content-workbench phase2-daily review-queue proponent-reviews critic-reviews judge-gate revision-instructions human-exception-queue agent-review-dashboard phase3-daily publishing-candidates human-feedback-template human-feedback-validate review-outcome-memory rule-update-suggestions learning-loop-dashboard phase4-daily head-media-patterns title-patterns opening-patterns structure-patterns content-recipe-suggestions pattern-adapters phase5-daily learning-daily llm-config-validate agent-prompts-validate llm-agent-smoke llm-proponent-reviews llm-critic-reviews llm-judge-gate llm-rewrite-suggestions agent-run-summary agent-evaluation-template agent-evaluation-validate phase6-daily minimax-proponent-live-pilot claude-critic-live-pilot claude-judge-live-pilot claude-rewrite-live-pilot llm-ab-comparison daily-scheduler failure-notification retry-fallback-runner weekly-content-retro phase7-daily runtime-store-init runtime-store-sync runtime-store-summary artifact-repository-sync publishing-dry-run human-review-console cost-budget-guard phase8-daily wechat-workbench-data wechat-article-preview wechat-workbench serve-wechat-workbench workbench-context chief-editor-agent workbench-action-router workbench-feedback-memory phase9-daily status

PYTHON ?= python3

doctor:
	$(PYTHON) scripts/doctor.py

path-audit:
	$(PYTHON) scripts/audit_hardcoded_paths.py

sources-validate:
	$(PYTHON) scripts/validate_sources.py

source-health:
	$(PYTHON) scripts/build_source_health.py

source-runtime-health:
	$(PYTHON) scripts/build_source_runtime_health.py

manifest-validate:
	$(PYTHON) scripts/validate_runtime_manifest.py

manifest-write-from-packets:
	$(PYTHON) scripts/write_runtime_manifest_from_packets.py

official-lane-with-manifest:
	$(PYTHON) scripts/run_official_lane_with_manifest.py

official-lane-health-check:
	$(PYTHON) scripts/run_official_lane_health_check.py

# Recommended daily entry for the official update lane.
official-lane-daily: official-lane-health-check

# Alias for users who search for daily commands first.
daily-official-lane: official-lane-health-check

daily-source-summary:
	$(PYTHON) scripts/build_daily_source_run_summary.py

official-lane-quality-gate:
	$(PYTHON) scripts/check_official_lane_quality_gate.py

daily-official-quality-gate: official-lane-quality-gate

official-daily-dashboard:
	$(PYTHON) scripts/build_official_daily_dashboard.py

daily-official-dashboard: official-daily-dashboard

official-daily-full-run:
	$(PYTHON) scripts/run_official_daily_full_run.py

daily-official-full-run:
	$(PYTHON) scripts/run_official_daily_full_run.py

runtime-baseline:
	$(PYTHON) scripts/update_official_runtime_baseline.py

source-coverage:
	$(PYTHON) scripts/build_source_coverage_alignment.py

evidence-packets:
	$(PYTHON) scripts/build_evidence_packets.py

topic-clusters:
	$(PYTHON) scripts/build_topic_clusters.py

value-scores:
	$(PYTHON) scripts/score_topic_clusters.py

high-value-candidates:
	$(PYTHON) scripts/build_high_value_candidate_pool.py

phase1-daily:
	$(PYTHON) scripts/run_phase1_daily_pipeline.py

content-briefs:
	$(PYTHON) scripts/build_content_briefs.py

content-outlines:
	$(PYTHON) scripts/build_content_outlines.py

content-drafts:
	$(PYTHON) scripts/build_content_drafts.py

content-quality-review:
	$(PYTHON) scripts/review_content_quality.py

platform-packages:
	$(PYTHON) scripts/build_platform_packages.py

content-workbench:
	$(PYTHON) scripts/build_content_workbench.py

phase2-daily:
	$(PYTHON) scripts/run_phase2_daily_pipeline.py

review-queue:
	$(PYTHON) scripts/build_agent_review_queue.py

proponent-reviews:
	$(PYTHON) scripts/build_proponent_reviews.py

critic-reviews:
	$(PYTHON) scripts/build_critic_reviews.py

judge-gate:
	$(PYTHON) scripts/build_judge_gate.py

revision-instructions:
	$(PYTHON) scripts/build_revision_instructions.py

human-exception-queue:
	$(PYTHON) scripts/build_human_exception_queue.py

agent-review-dashboard:
	$(PYTHON) scripts/build_agent_review_dashboard.py

phase3-daily:
	$(PYTHON) scripts/run_phase3_daily_pipeline.py

publishing-candidates:
	$(PYTHON) scripts/build_publishing_candidate_queue.py

human-feedback-template:
	$(PYTHON) scripts/build_human_feedback_template.py

human-feedback-validate:
	$(PYTHON) scripts/validate_human_feedback.py

review-outcome-memory:
	$(PYTHON) scripts/update_review_outcome_memory.py

rule-update-suggestions:
	$(PYTHON) scripts/build_rule_update_suggestions.py

learning-loop-dashboard:
	$(PYTHON) scripts/build_learning_loop_dashboard.py

phase4-daily:
	$(PYTHON) scripts/run_phase4_daily_pipeline.py

head-media-patterns:
	$(PYTHON) scripts/build_head_media_pattern_library.py

title-patterns:
	$(PYTHON) scripts/extract_title_patterns.py

opening-patterns:
	$(PYTHON) scripts/extract_opening_patterns.py

structure-patterns:
	$(PYTHON) scripts/extract_structure_patterns.py

content-recipe-suggestions:
	$(PYTHON) scripts/build_content_recipe_suggestions.py

pattern-adapters:
	$(PYTHON) scripts/build_pattern_adapters.py

phase5-daily:
	$(PYTHON) scripts/run_phase5_daily_learning_pipeline.py

learning-daily:
	$(PYTHON) scripts/run_learning_daily_pipeline.py

llm-config-validate:
	$(PYTHON) scripts/validate_llm_provider_config.py

agent-prompts-validate:
	$(PYTHON) scripts/validate_agent_prompts.py

llm-agent-smoke:
	$(PYTHON) scripts/run_llm_agent_client_smoke.py

llm-proponent-reviews:
	$(PYTHON) scripts/run_llm_proponent_reviews.py

llm-critic-reviews:
	$(PYTHON) scripts/run_llm_critic_reviews.py

llm-judge-gate:
	$(PYTHON) scripts/run_llm_judge_gate.py

llm-rewrite-suggestions:
	$(PYTHON) scripts/run_llm_rewrite_suggestions.py

agent-run-summary:
	$(PYTHON) scripts/build_agent_run_summary.py

agent-evaluation-template:
	$(PYTHON) scripts/build_agent_evaluation_template.py

agent-evaluation-validate:
	$(PYTHON) scripts/validate_agent_evaluation.py

phase6-daily:
	$(PYTHON) scripts/run_phase6_daily_agent_pipeline.py

minimax-proponent-live-pilot:
	$(PYTHON) scripts/run_minimax_proponent_live_pilot.py

claude-critic-live-pilot:
	$(PYTHON) scripts/run_claude_critic_live_pilot.py

claude-judge-live-pilot:
	$(PYTHON) scripts/run_claude_judge_live_pilot.py

claude-rewrite-live-pilot:
	$(PYTHON) scripts/run_claude_rewrite_live_pilot.py

llm-ab-comparison:
	$(PYTHON) scripts/build_llm_ab_comparison.py

daily-scheduler:
	$(PYTHON) scripts/run_daily_scheduler.py

failure-notification:
	$(PYTHON) scripts/build_failure_notification_report.py

retry-fallback-runner:
	$(PYTHON) scripts/run_retry_fallback_runner.py

weekly-content-retro:
	$(PYTHON) scripts/build_weekly_content_retro.py

phase7-daily:
	$(PYTHON) scripts/run_phase7_daily_pipeline.py

runtime-store-init:
	$(PYTHON) scripts/init_runtime_store.py

runtime-store-sync:
	$(PYTHON) scripts/sync_runtime_store.py

runtime-store-summary:
	$(PYTHON) scripts/build_runtime_store_summary.py

artifact-repository-sync:
	$(PYTHON) scripts/sync_artifact_repository.py

publishing-dry-run:
	$(PYTHON) scripts/run_publishing_dry_run.py

human-review-console:
	$(PYTHON) scripts/run_human_review_console.py --summary

cost-budget-guard:
	$(PYTHON) scripts/check_cost_budget_guard.py

phase8-daily:
	$(PYTHON) scripts/run_phase8_daily_production_pipeline.py

wechat-workbench-data:
	$(PYTHON) scripts/build_wechat_workbench_data.py

wechat-article-preview:
	$(PYTHON) scripts/render_wechat_article_preview.py

wechat-workbench:
	$(PYTHON) scripts/build_wechat_workbench_frontend.py

serve-wechat-workbench:
	$(PYTHON) scripts/serve_wechat_workbench.py

workbench-context:
	$(PYTHON) scripts/build_workbench_context.py

chief-editor-agent:
	$(PYTHON) scripts/run_chief_editor_agent.py

workbench-action-router:
	$(PYTHON) scripts/route_workbench_actions.py

workbench-feedback-memory:
	$(PYTHON) scripts/update_workbench_feedback_memory.py

phase9-daily:
	$(PYTHON) scripts/run_phase9_daily_workbench_pipeline.py

status:
	bash 内容工厂控制台/status.sh
