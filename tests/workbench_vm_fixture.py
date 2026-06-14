from __future__ import annotations


def sample_workbench_data(title: str = "AI Agent 工作流进入企业生产") -> dict:
    return {
        "run_date": "20260614",
        "generated_at": "2026-06-14T09:00:00+08:00",
        "autonomous_content_production_panel": {
            "selected_topic": {"title": title, "evidence_ids": ["ev_1"]},
            "selected_brief": {
                "one_sentence_thesis": "Agent 正从演示工具进入企业工作流。",
                "narrative_angle": "从工具演示到生产流程。",
                "evidence_inventory": [
                    {
                        "evidence_id": "ev_1",
                        "title": "Official release",
                        "source_name": "Official",
                        "evidence_role": "hard_evidence",
                        "metadata_only": False,
                        "can_use_as_hard_evidence": True,
                    },
                    {
                        "evidence_id": "ev_2",
                        "title": "Community discussion",
                        "source_name": "Reddit",
                        "evidence_role": "weak_signal",
                        "metadata_only": True,
                        "can_use_as_hard_evidence": False,
                    },
                ],
            },
            "selected_final_candidate": {
                "candidate_id": "autofinal_1",
                "title": title,
                "article_markdown": "# AI Agent 工作流进入企业生产\n\n## 为什么现在写\n证据显示企业工作流开始变化。",
                "status": "READY_FOR_HUMAN_REVIEW",
                "evidence_ids": ["ev_1", "ev_2"],
                "manual_review_required": True,
                "do_not_publish": True,
            },
            "selected_review": {
                "proponent": {"strongest_points": ["why now 清楚"]},
                "critic": {"main_concerns": ["第二部分案例仍需一手来源"]},
                "judge": {"decision": "REVISE", "quality_score": 0.82},
                "rewrite": {"generated": True, "rewrite_version_id": "rw_1"},
                "status": "REVISED",
            },
            "quality_regression_status": "PASS",
            "quality_regression_summary": {"check_count": 3, "pass": 3, "warn": 0, "fail": 0, "blocking_failures": 0},
            "quality_checks": [
                {"check_id": "has_why_now", "status": "PASS", "message": "why now exists"},
                {"check_id": "has_reader_question", "status": "PASS", "message": "reader question exists"},
                {"check_id": "no_target_price", "status": "PASS", "message": "no target price"},
            ],
        },
        "runtime_control_center_panel": {
            "runtime_status": "IDLE",
            "launchagent_installed": True,
            "launchagent_loaded": True,
            "launchagent_enabled": True,
            "runtime_pid": 12345,
            "runtime_instance_id": "runtime_1",
            "last_heartbeat": "2026-06-14T09:00:00+08:00",
            "heartbeat_age_seconds": 60,
            "next_scheduled_run": "18:00 晚间采集",
            "ledger_summary": {"success": 2, "failed": 0, "pending": 1},
            "retry_summary": {"retry_count": 0},
            "missed_run_summary": {"catchup_count": 0},
            "network_readiness": {"status": "FULL"},
        },
        "acquisition_playbook_panel": {
            "runtime_plan_summary": {"connector_runs": 3},
            "lane_cards": [{"time": "18:00", "lane": "official_ai_lab", "next_action": "RUN_NOW"}],
        },
        "openclaw_migration_panel": {
            "coexistence_summary": {"conflict_count": 1, "manual_review": 1, "safe_to_disable": 0},
            "phase29_status": "ACTIONABLE",
        },
        "openclaw_activation_panel": {"phase30_status": "ACTIONABLE"},
        "replay_trial_panel": {
            "availability_summary": {"replay_ready_days": 7},
            "topic_selection_summary": {"selected_days": 7},
            "article_review_summary": {"final_candidate_count": 7},
            "quality_summary": {"pass_days": 6},
            "diagnosis_summary": {"duplicate_topic_ratio": 0.2, "source_metadata_title_ratio": 0},
            "calibration_summary": {"proposal_count": 1},
            "day_cards": [
                {"business_date": "2026-06-13", "topic_title": "Agent production", "quality_status": "PASS", "worth_reading": True}
            ],
            "proposals": [
                {"proposal_type": "metadata_title_penalty", "severity": "MEDIUM", "target_config": "topic_scoring_playbook.yaml", "reason": "metadata title risk"}
            ],
        },
    }
