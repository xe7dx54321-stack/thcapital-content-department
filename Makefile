.PHONY: doctor path-audit sources-validate source-health source-runtime-health manifest-validate manifest-write-from-packets official-lane-with-manifest official-lane-health-check official-lane-daily daily-official-lane daily-source-summary official-lane-quality-gate daily-official-quality-gate official-daily-dashboard daily-official-dashboard official-daily-full-run daily-official-full-run runtime-baseline source-coverage evidence-packets topic-clusters value-scores high-value-candidates phase1-daily content-briefs content-outlines content-drafts content-quality-review platform-packages content-workbench phase2-daily review-queue proponent-reviews critic-reviews judge-gate revision-instructions human-exception-queue agent-review-dashboard phase3-daily publishing-candidates human-feedback-template human-feedback-validate review-outcome-memory rule-update-suggestions learning-loop-dashboard phase4-daily head-media-patterns title-patterns opening-patterns structure-patterns content-recipe-suggestions pattern-adapters phase5-daily learning-daily llm-config-validate agent-prompts-validate llm-agent-smoke llm-proponent-reviews llm-critic-reviews llm-judge-gate llm-rewrite-suggestions agent-run-summary agent-evaluation-template agent-evaluation-validate phase6-daily minimax-proponent-live-pilot claude-critic-live-pilot claude-judge-live-pilot claude-rewrite-live-pilot llm-ab-comparison daily-scheduler failure-notification retry-fallback-runner weekly-content-retro phase7-daily runtime-store-init runtime-store-sync runtime-store-summary artifact-repository-sync publishing-dry-run human-review-console cost-budget-guard phase8-daily wechat-workbench-data wechat-article-preview wechat-workbench serve-wechat-workbench workbench-context chief-editor-agent workbench-action-router workbench-feedback-memory phase9-daily action-approval-board execute-rewrite-actions execute-evidence-actions execute-topic-actions versioned-article-preview serve-workbench-interactions phase10-daily version-comparison-score version-review-board article-version-memory action-effectiveness prompt-rule-regression phase11-daily promote-accepted-versions final-article-candidates final-publish-checklist final-candidate-memory multiday-version-analytics phase12-daily serve-workbench-ui final-review-actions publish-session-board post-publish-metrics-board content-performance-memory performance-learning-feedback phase13-daily topic-methodology-validate article-methodology-validate content-recipes-validate methodology-topic-score methodology-article-review chief-editor-methodology-context methodology-performance-alignment phase14-daily methodology-briefs methodology-outlines methodology-drafts execute-methodology-rewrite-actions visual-methodology-validate article-visual-plans image-asset-requests methodology-regression-tests human-methodology-calibration phase15-daily live-methodology-brief-pilot live-methodology-draft-pilot live-methodology-rewrite-pilot live-visual-prompt-pilot live-output-comparison live-calibration-board image-generation-approval-queue phase16-daily promote-approved-live-outputs promote-live-rewrite-versions manual-image-generation-tasks image-asset-library image-asset-library-board article-with-images-preview final-visual-review phase17-daily visual-approved-final-candidates wechat-copy-pack-with-images visual-publishing-checklist post-publish-visual-performance-board visual-strategy-learning-feedback phase18-daily publishing-session-calendar content-queue-priority weekly-publishing-rhythm published-article-archive published-article-archive-board post-publish-metrics-review content-ops-closeout phase19-daily one-week-trial-protocol content-ops-failure-handling publishing-checklist-regression operator-runbook phase0-19-system-closeout phase20-daily trial-day-1 trial-day-2 trial-day-3 trial-day-4 trial-day-5 weekly-trial-retrospective trial-fix-pack phase21-trial trial-day-run recurring-issue-board weekly-publishing-calendar content-fix-pack post-publish-feedback phase22-daily high-priority-issue-resolution-plan execute-quick-fix-candidates repair-content-queue-readiness calibrate-publishing-calendar-readiness trial-day-status-stabilizer issue-resolution-verification stable-trial-readiness-gate phase23-daily stable-trial-day-1 stable-trial-day-2 stable-trial-day-3 content-quality-calibration ops-to-methodology-feedback stable-ops-readiness-review phase24-daily stable-daily-ops-baseline operator-acceptance-checklist stable-daily-ops content-factory-v1-closeout phase25-daily source-coverage-gap-audit high-value-source-expansion-plan hot-signal-capture fallback-backfill-queue daily-hot-material-pool hot-material-quality-gate phase26-daily status

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
	$(PYTHON) scripts/build_wechat_workbench_data.py
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

action-approval-board:
	$(PYTHON) scripts/build_action_approval_board.py

execute-rewrite-actions:
	$(PYTHON) scripts/execute_rewrite_actions.py

execute-evidence-actions:
	$(PYTHON) scripts/execute_evidence_expansion_actions.py

execute-topic-actions:
	$(PYTHON) scripts/execute_topic_replacement_actions.py

versioned-article-preview:
	$(PYTHON) scripts/build_versioned_article_preview.py

serve-workbench-interactions:
	$(PYTHON) scripts/serve_workbench_interactions.py

phase10-daily:
	$(PYTHON) scripts/run_phase10_daily_action_pipeline.py

version-comparison-score:
	$(PYTHON) scripts/score_article_versions.py

version-review-board:
	$(PYTHON) scripts/build_version_review_board.py

article-version-memory:
	$(PYTHON) scripts/update_article_version_memory.py

action-effectiveness:
	$(PYTHON) scripts/build_action_effectiveness_analytics.py

prompt-rule-regression:
	$(PYTHON) scripts/build_prompt_rule_regression_dashboard.py

phase11-daily:
	$(PYTHON) scripts/run_phase11_daily_quality_loop_pipeline.py

promote-accepted-versions:
	$(PYTHON) scripts/promote_accepted_versions.py

final-article-candidates:
	$(PYTHON) scripts/build_final_article_candidates.py

final-publish-checklist:
	$(PYTHON) scripts/build_final_publish_checklist.py

final-candidate-memory:
	$(PYTHON) scripts/update_final_candidate_memory.py

multiday-version-analytics:
	$(PYTHON) scripts/build_multiday_version_analytics.py

phase12-daily:
	$(PYTHON) scripts/run_phase12_daily_finalization_pipeline.py

serve-workbench-ui:
	$(PYTHON) scripts/serve_workbench_ui.py

final-review-actions:
	$(PYTHON) scripts/update_final_review_status.py --list

publish-session-board:
	$(PYTHON) scripts/build_publish_session_board.py

post-publish-metrics-board:
	$(PYTHON) scripts/build_post_publish_metrics_board.py

content-performance-memory:
	$(PYTHON) scripts/update_content_performance_memory.py

performance-learning-feedback:
	$(PYTHON) scripts/build_performance_learning_feedback.py

phase13-daily:
	$(PYTHON) scripts/run_phase13_daily_performance_pipeline.py

topic-methodology-validate:
	$(PYTHON) scripts/validate_topic_selection_methodology.py

article-methodology-validate:
	$(PYTHON) scripts/validate_article_quality_methodology.py

content-recipes-validate:
	$(PYTHON) scripts/validate_content_strategy_recipes.py

methodology-topic-score:
	$(PYTHON) scripts/score_topics_with_methodology.py

methodology-article-review:
	$(PYTHON) scripts/review_articles_with_methodology.py

chief-editor-methodology-context:
	$(PYTHON) scripts/build_chief_editor_methodology_context.py

methodology-performance-alignment:
	$(PYTHON) scripts/build_methodology_performance_alignment.py

phase14-daily:
	$(PYTHON) scripts/run_phase14_daily_methodology_pipeline.py

methodology-briefs:
	$(PYTHON) scripts/build_methodology_briefs.py

methodology-outlines:
	$(PYTHON) scripts/build_methodology_outlines.py

methodology-drafts:
	$(PYTHON) scripts/build_methodology_drafts.py

execute-methodology-rewrite-actions:
	$(PYTHON) scripts/execute_methodology_rewrite_actions.py

visual-methodology-validate:
	$(PYTHON) scripts/validate_article_visual_methodology.py

article-visual-plans:
	$(PYTHON) scripts/build_visual_plans.py

image-asset-requests:
	$(PYTHON) scripts/build_image_asset_requests.py

methodology-regression-tests:
	$(PYTHON) scripts/run_methodology_regression_tests.py

human-methodology-calibration:
	$(PYTHON) scripts/build_human_methodology_calibration_board.py

phase15-daily:
	$(PYTHON) scripts/run_phase15_daily_generation_pipeline.py

live-methodology-brief-pilot:
	$(PYTHON) scripts/run_live_methodology_brief_pilot.py --limit 1

live-methodology-draft-pilot:
	$(PYTHON) scripts/run_live_methodology_draft_pilot.py --limit 1

live-methodology-rewrite-pilot:
	$(PYTHON) scripts/run_live_methodology_rewrite_pilot.py --limit 1

live-visual-prompt-pilot:
	$(PYTHON) scripts/run_live_visual_prompt_pilot.py --limit 3

live-output-comparison:
	$(PYTHON) scripts/compare_live_outputs.py

live-calibration-board:
	$(PYTHON) scripts/build_live_calibration_board.py

image-generation-approval-queue:
	$(PYTHON) scripts/build_image_generation_approval_queue.py

phase16-daily:
	$(PYTHON) scripts/run_phase16_daily_live_pilot_pipeline.py

promote-approved-live-outputs:
	$(PYTHON) scripts/promote_approved_live_outputs.py

promote-live-rewrite-versions:
	$(PYTHON) scripts/promote_live_rewrite_versions.py

manual-image-generation-tasks:
	$(PYTHON) scripts/build_manual_image_generation_tasks.py

image-asset-library:
	$(PYTHON) scripts/update_image_asset_library.py

image-asset-library-board:
	$(PYTHON) scripts/build_image_asset_library_board.py

article-with-images-preview:
	$(PYTHON) scripts/build_article_with_images_preview.py

final-visual-review:
	$(PYTHON) scripts/build_final_visual_review.py

phase17-daily:
	$(PYTHON) scripts/run_phase17_daily_visual_production_pipeline.py

visual-approved-final-candidates:
	$(PYTHON) scripts/build_visual_approved_final_candidates.py

wechat-copy-pack-with-images:
	$(PYTHON) scripts/build_wechat_copy_pack_with_images.py

visual-publishing-checklist:
	$(PYTHON) scripts/build_visual_publishing_checklist.py

post-publish-visual-performance-board:
	$(PYTHON) scripts/build_post_publish_visual_performance_board.py

visual-strategy-learning-feedback:
	$(PYTHON) scripts/build_visual_strategy_learning_feedback.py

phase18-daily:
	$(PYTHON) scripts/run_phase18_daily_publishing_pack_pipeline.py

publishing-session-calendar:
	$(PYTHON) scripts/build_publishing_session_calendar.py

content-queue-priority:
	$(PYTHON) scripts/build_content_queue_priority_board.py

weekly-publishing-rhythm:
	$(PYTHON) scripts/build_weekly_publishing_rhythm.py

published-article-archive:
	$(PYTHON) scripts/update_published_article_archive.py

published-article-archive-board:
	$(PYTHON) scripts/build_published_article_archive_board.py

post-publish-metrics-review:
	$(PYTHON) scripts/build_post_publish_metrics_review_board.py

content-ops-closeout:
	$(PYTHON) scripts/build_content_ops_closeout.py

phase19-daily:
	$(PYTHON) scripts/run_phase19_daily_ops_pipeline.py

one-week-trial-protocol:
	$(PYTHON) scripts/build_one_week_trial_protocol.py

content-ops-failure-handling:
	$(PYTHON) scripts/build_content_ops_failure_handling.py

publishing-checklist-regression:
	$(PYTHON) scripts/run_publishing_checklist_regression.py

operator-runbook:
	$(PYTHON) scripts/build_operator_runbook.py

phase0-19-system-closeout:
	$(PYTHON) scripts/build_phase0_19_system_closeout.py

phase20-daily:
	$(PYTHON) scripts/run_phase20_daily_hardening_pipeline.py

trial-day-1:
	$(PYTHON) scripts/run_trial_day.py --day 1

trial-day-2:
	$(PYTHON) scripts/run_trial_day.py --day 2

trial-day-3:
	$(PYTHON) scripts/run_trial_day.py --day 3

trial-day-4:
	$(PYTHON) scripts/run_trial_day.py --day 4

trial-day-5:
	$(PYTHON) scripts/run_trial_day.py --day 5

weekly-trial-retrospective:
	$(PYTHON) scripts/build_weekly_trial_retrospective.py

trial-fix-pack:
	$(PYTHON) scripts/build_trial_fix_pack.py

phase21-trial:
	$(PYTHON) scripts/run_phase21_trial_pipeline.py

trial-day-run:
	$(PYTHON) scripts/run_daily_content_ops.py --mode dry_run

recurring-issue-board:
	$(PYTHON) scripts/build_recurring_issue_board.py

weekly-publishing-calendar:
	$(PYTHON) scripts/build_weekly_publishing_calendar.py

content-fix-pack:
	$(PYTHON) scripts/build_content_ops_fix_pack.py

post-publish-feedback:
	$(PYTHON) scripts/build_post_publish_feedback.py

phase22-daily:
	$(PYTHON) scripts/run_phase22_daily_ops_pipeline.py

high-priority-issue-resolution-plan:
	$(PYTHON) scripts/build_high_priority_issue_resolution_plan.py

execute-quick-fix-candidates:
	$(PYTHON) scripts/execute_quick_fix_candidates.py

repair-content-queue-readiness:
	$(PYTHON) scripts/repair_content_queue_readiness.py

calibrate-publishing-calendar-readiness:
	$(PYTHON) scripts/calibrate_publishing_calendar_readiness.py

trial-day-status-stabilizer:
	$(PYTHON) scripts/stabilize_trial_day_status.py

issue-resolution-verification:
	$(PYTHON) scripts/build_issue_resolution_verification_board.py

stable-trial-readiness-gate:
	$(PYTHON) scripts/build_stable_trial_readiness_gate.py

phase23-daily:
	$(PYTHON) scripts/run_phase23_daily_stability_pipeline.py

stable-trial-day-1:
	$(PYTHON) scripts/run_stable_trial_day.py --day 1

stable-trial-day-2:
	$(PYTHON) scripts/run_stable_trial_day.py --day 2

stable-trial-day-3:
	$(PYTHON) scripts/run_stable_trial_day.py --day 3

content-quality-calibration:
	$(PYTHON) scripts/build_content_quality_calibration.py

ops-to-methodology-feedback:
	$(PYTHON) scripts/build_ops_to_methodology_feedback.py

stable-ops-readiness-review:
	$(PYTHON) scripts/build_stable_ops_readiness_review.py

phase24-daily:
	$(PYTHON) scripts/run_phase24_daily_stable_trial_pipeline.py

stable-daily-ops-baseline:
	$(PYTHON) scripts/build_stable_daily_ops_baseline.py

operator-acceptance-checklist:
	$(PYTHON) scripts/build_operator_acceptance_checklist.py

stable-daily-ops:
	$(PYTHON) scripts/run_stable_daily_ops.py

content-factory-v1-closeout:
	$(PYTHON) scripts/build_content_factory_v1_closeout.py

phase25-daily:
	$(PYTHON) scripts/run_phase25_daily_baseline_pipeline.py

source-coverage-gap-audit:
	$(PYTHON) scripts/build_source_coverage_gap_audit.py

high-value-source-expansion-plan:
	$(PYTHON) scripts/build_high_value_source_expansion_plan.py

hot-signal-capture:
	$(PYTHON) scripts/build_hot_signal_capture.py

fallback-backfill-queue:
	$(PYTHON) scripts/build_fallback_backfill_queue.py

daily-hot-material-pool:
	$(PYTHON) scripts/build_daily_hot_material_pool.py

hot-material-quality-gate:
	$(PYTHON) scripts/run_hot_material_quality_gate.py

phase26-daily:
	$(PYTHON) scripts/run_phase26_daily_acquisition_pipeline.py

p0-source-connector-selection:
	$(PYTHON) scripts/build_p0_source_connector_selection.py

rss-official-blog-connectors:
	$(PYTHON) scripts/run_rss_official_blog_connectors.py

lightweight-research-connectors:
	$(PYTHON) scripts/run_lightweight_research_connectors.py

manual-url-backfill-ingestion:
	$(PYTHON) scripts/run_manual_url_backfill_ingestion.py

normalize-connector-outputs:
	$(PYTHON) scripts/normalize_connector_outputs.py

connector-source-health-gate:
	$(PYTHON) scripts/run_connector_source_health_gate.py

phase27-daily:
	$(PYTHON) scripts/run_phase27_daily_connector_pipeline.py

status:
	bash 内容工厂控制台/status.sh
