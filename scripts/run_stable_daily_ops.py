#!/usr/bin/env python3
"""Run the simplified stable daily ops command."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.stable_daily_ops_runner import build_stable_daily_ops


def main() -> int:
    paths = get_project_paths(ROOT)
    payload, _outputs = build_stable_daily_ops(ROOT, paths.logs_root, paths.frontstage_root)
    summary = payload.get("daily_summary", {})
    print("Stable Daily Ops")
    print("================")
    print(f"status: {payload.get('status')}")
    print(f"baseline_status: {summary.get('baseline_status')}")
    print(f"operator_acceptance_status: {summary.get('operator_acceptance_status')}")
    print(f"blocking_issue_count: {summary.get('blocking_issue_count')}")
    print(f"workbench_ready: {summary.get('workbench_ready')}")
    upstream = summary.get("upstream_supply") if isinstance(summary.get("upstream_supply"), dict) else {}
    print("Upstream supply:")
    print(f"  gate_status: {upstream.get('gate_status', 'UNKNOWN')}")
    print(f"  status_label: {upstream.get('status_label', 'UNKNOWN')}")
    print(f"  hot_material_count: {upstream.get('hot_material_count', 0)}")
    print(f"  connector_item_count: {upstream.get('connector_item_count', 0)}")
    print(f"  evidence_packet_count: {upstream.get('evidence_packet_count', 0)}")
    print(f"  promoted_topic_count: {upstream.get('promoted_topic_count', 0)}")
    print(f"  ready_for_brief: {upstream.get('ready_for_brief', 0)}")
    print(f"  needs_evidence: {upstream.get('needs_evidence', 0)}")
    print(f"  promote_to_topic_pipeline: {upstream.get('promote_to_topic_pipeline', 0)}")
    print(f"  backfill_required: {upstream.get('backfill_required', 0)}")
    print(f"  weak_supply_reasons: {upstream.get('weak_supply_reasons', [])}")
    acquisition = summary.get("acquisition_to_content") if isinstance(summary.get("acquisition_to_content"), dict) else {}
    print("Acquisition to content:")
    print(f"  connector_topic_candidates: {acquisition.get('connector_topic_candidates', 0)}")
    print(f"  ready_for_brief: {acquisition.get('ready_for_brief', 0)}")
    print(f"  needs_evidence: {acquisition.get('needs_evidence', 0)}")
    print(f"  watch: {acquisition.get('watch', 0)}")
    openclaw = summary.get("openclaw_migration") if isinstance(summary.get("openclaw_migration"), dict) else {}
    print("OpenClaw migration:")
    print(f"  inventory_source_count: {openclaw.get('inventory_source_count', 0)}")
    print(f"  migration_candidate_count: {openclaw.get('migration_candidate_count', 0)}")
    print(f"  metadata_item_count: {openclaw.get('metadata_item_count', 0)}")
    print(f"  weak_signal_item_count: {openclaw.get('weak_signal_item_count', 0)}")
    print(f"  openclaw_hot_material_count: {openclaw.get('openclaw_hot_material_count', 0)}")
    print(f"  blocked_source_count: {openclaw.get('blocked_source_count', 0)}")
    print(f"  hard_evidence_allowed: {openclaw.get('hard_evidence_allowed', 0)}")
    openclaw_activation = summary.get("openclaw_activation") if isinstance(summary.get("openclaw_activation"), dict) else {}
    print("OpenClaw activation:")
    print(f"  backfill_count: {openclaw_activation.get('backfill_count', 0)}")
    print(f"  ready_for_confirmation: {openclaw_activation.get('ready_for_confirmation', 0)}")
    print(f"  needs_primary_source: {openclaw_activation.get('needs_primary_source', 0)}")
    print(f"  needs_second_source: {openclaw_activation.get('needs_second_source', 0)}")
    print(f"  manual_review: {openclaw_activation.get('manual_review', 0)}")
    print(f"  activated_topic_count: {openclaw_activation.get('activated_topic_count', 0)}")
    print(f"  can_enter_brief_pipeline: {openclaw_activation.get('can_enter_brief_pipeline', 0)}")
    print(f"  regression_gate_status: {openclaw_activation.get('regression_gate_status', 'UNKNOWN')}")
    runtime = summary.get("autonomous_runtime") if isinstance(summary.get("autonomous_runtime"), dict) else {}
    print("Autonomous runtime:")
    print(f"  runtime_status: {runtime.get('runtime_status', 'UNKNOWN')}")
    print(f"  last_heartbeat: {runtime.get('last_heartbeat', '')}")
    print(f"  next_scheduled_run: {runtime.get('next_scheduled_run', '')}")
    print(f"  job_run_count: {runtime.get('job_run_count', 0)}")
    print(f"  success: {runtime.get('success', 0)}")
    print(f"  failed: {runtime.get('failed', 0)}")
    print(f"  retry_count: {runtime.get('retry_count', 0)}")
    print(f"  missed_count: {runtime.get('missed_count', 0)}")
    print(f"  dry_run_status: {runtime.get('dry_run_status', 'UNKNOWN')}")
    print("Safety:")
    for key, value in payload.get("safety", {}).items():
        print(f"  {key}: {value}")
    print("Steps:")
    for step in payload.get("steps", []):
        print(f"  {step.get('name')}: {step.get('status')} ({step.get('return_code')})")
    return 0 if payload.get("status") in {"SUCCESS", "ACTIONABLE", "DEGRADED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
