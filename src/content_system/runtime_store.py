"""SQLite runtime store indexing for generated content-system artifacts."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from content_system.paths import ProjectPaths
from content_system.runtime_store_schema import CREATE_INDEXES_SQL, CREATE_TABLES_SQL, DROP_TABLES_SQL, SCHEMA_VERSION


DB_FILENAME = "content_system_runtime.db"


@dataclass(frozen=True)
class RuntimeStoreSyncReport:
    schema_version: str
    generated_at: str
    run_date: str
    db_path: str
    status: str
    summary: dict[str, int]
    warnings: tuple[str, ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_token() -> str:
    return datetime.now().strftime("%Y%m%d")


def runtime_store_dir(paths: ProjectPaths) -> Path:
    return paths.market_content_root / "12_runtime_store"


def default_db_path(paths: ProjectPaths) -> Path:
    return runtime_store_dir(paths) / DB_FILENAME


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def list_payload(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    raw = payload.get(key)
    return [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def make_event_id(run_date: str, event_type: str, source_file: str, message: str) -> str:
    digest = hashlib.sha1("|".join((run_date, event_type, source_file, message)).encode("utf-8")).hexdigest()[:16]
    return f"evt_{run_date}_{digest}"


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_runtime_store(paths: ProjectPaths, db_path: Path | None = None, reset: bool = False) -> Path:
    final_path = db_path or default_db_path(paths)
    with connect(final_path) as connection:
        if reset:
            for statement in DROP_TABLES_SQL:
                connection.execute(statement)
        for statement in CREATE_TABLES_SQL:
            connection.execute(statement)
        for statement in CREATE_INDEXES_SQL:
            connection.execute(statement)
        connection.commit()
    return final_path


def upsert_system_event(connection: sqlite3.Connection, run_date: str, event_type: str, severity: str, message: str, source_file: str) -> None:
    event_id = make_event_id(run_date, event_type, source_file, message)
    connection.execute(
        """
        INSERT INTO system_events(event_id, run_date, event_type, severity, message, source_file, created_at)
        VALUES(?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(event_id) DO UPDATE SET
            severity=excluded.severity,
            message=excluded.message,
            created_at=excluded.created_at
        """,
        (event_id, run_date, event_type, severity, message, source_file, utc_now()),
    )


def upsert_pipeline(connection: sqlite3.Connection, payload: dict[str, Any], source_file: str, pipeline_name: str) -> int:
    if not payload:
        return 0
    run_date = str(payload.get("run_date") or today_token()).replace("-", "")[:8]
    run_id = f"{pipeline_name}:{run_date}:{source_file}"
    steps = list_payload(payload, "steps")
    started_at = str(steps[0].get("started_at") if steps else payload.get("generated_at") or "")
    finished_at = str(steps[-1].get("finished_at") if steps else payload.get("generated_at") or "")
    connection.execute(
        """
        INSERT INTO pipeline_runs(run_id, run_date, pipeline_name, status, started_at, finished_at, summary_json, source_file, created_at)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(run_id) DO UPDATE SET
            status=excluded.status,
            started_at=excluded.started_at,
            finished_at=excluded.finished_at,
            summary_json=excluded.summary_json,
            created_at=excluded.created_at
        """,
        (
            run_id,
            run_date,
            pipeline_name,
            str(payload.get("status") or "UNKNOWN"),
            started_at,
            finished_at,
            json_text(payload.get("summary") or {}),
            source_file,
            utc_now(),
        ),
    )
    return 1


def upsert_agent_runs(connection: sqlite3.Connection, records: Iterable[dict[str, Any]], source_file: str) -> int:
    count = 0
    for record in records:
        request_id = str(record.get("request_id") or "")
        if not request_id:
            continue
        connection.execute(
            """
            INSERT INTO agent_runs(request_id, run_date, agent_name, provider_id, model, mode, status, latency_ms,
                estimated_input_tokens, estimated_output_tokens, estimated_cost_usd, fallback_used, error, source_file, created_at)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(request_id) DO UPDATE SET
                status=excluded.status,
                latency_ms=excluded.latency_ms,
                estimated_input_tokens=excluded.estimated_input_tokens,
                estimated_output_tokens=excluded.estimated_output_tokens,
                estimated_cost_usd=excluded.estimated_cost_usd,
                fallback_used=excluded.fallback_used,
                error=excluded.error,
                created_at=excluded.created_at
            """,
            (
                request_id,
                str(record.get("run_date") or ""),
                str(record.get("agent_name") or ""),
                str(record.get("provider_id") or ""),
                str(record.get("model") or ""),
                str(record.get("mode") or ""),
                str(record.get("status") or ""),
                safe_int(record.get("latency_ms")),
                safe_int(record.get("estimated_input_tokens")),
                safe_int(record.get("estimated_output_tokens")),
                safe_float(record.get("estimated_cost_usd")),
                1 if record.get("fallback_used") else 0,
                str(record.get("error") or record.get("fallback_reason") or ""),
                source_file,
                utc_now(),
            ),
        )
        count += 1
    return count


def upsert_source_health(connection: sqlite3.Connection, payload: dict[str, Any], source_file: str) -> int:
    run_date = str(payload.get("run_date") or today_token()).replace("-", "")[:8]
    count = 0
    for record in list_payload(payload, "records"):
        source_id = str(record.get("source_id") or "")
        if not source_id:
            continue
        connection.execute(
            """
            INSERT INTO source_health_snapshots(run_date, source_id, status, items_found, missing_expected, error_hint, source_file, created_at)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(run_date, source_id, source_file) DO UPDATE SET
                status=excluded.status,
                items_found=excluded.items_found,
                missing_expected=excluded.missing_expected,
                error_hint=excluded.error_hint,
                created_at=excluded.created_at
            """,
            (
                run_date,
                source_id,
                str(record.get("runtime_status") or record.get("status") or ""),
                safe_int(record.get("items_found")),
                1 if str(record.get("runtime_status")) == "MISSING_EXPECTED" else 0,
                str(record.get("runtime_reason") or record.get("error_hint_count") or ""),
                source_file,
                utc_now(),
            ),
        )
        count += 1
    return count


def title_for(item: dict[str, Any]) -> str:
    for key in ("title", "theme", "recommended_title", "package_id", "review_item_id", "cluster_id"):
        value = item.get(key)
        if value:
            return str(value)
    wechat = item.get("wechat") if isinstance(item.get("wechat"), dict) else {}
    if wechat.get("title"):
        return str(wechat["title"])
    return ""


def artifact_id_for(item: dict[str, Any], artifact_type: str, fallback_source: str) -> str:
    for key in (
        "evidence_id",
        "cluster_id",
        "candidate_id",
        "brief_id",
        "outline_id",
        "draft_id",
        "package_id",
        "review_item_id",
        "judge_decision_id",
        "llm_judge_decision_id",
        "publishing_candidate_id",
        "adapter_id",
    ):
        value = item.get(key)
        if value:
            return f"{artifact_type}:{value}"
    digest = hashlib.sha1(json_text(item).encode("utf-8")).hexdigest()[:14]
    return f"{artifact_type}:{fallback_source}:{digest}"


def status_for(item: dict[str, Any]) -> str:
    for key in ("status", "score_band", "quality_status", "publish_status", "decision", "coverage_status", "recommended_action"):
        value = item.get(key)
        if value:
            return str(value)
    return ""


def score_for(item: dict[str, Any]) -> float:
    for key in ("score", "total_score", "decision_score", "quality_score"):
        if key in item:
            return safe_float(item.get(key))
    return 0.0


def upsert_content_artifacts(connection: sqlite3.Connection, items: Iterable[dict[str, Any]], artifact_type: str, run_date: str, source_file: str, path_value: str) -> int:
    count = 0
    for item in items:
        artifact_id = artifact_id_for(item, artifact_type, source_file)
        connection.execute(
            """
            INSERT INTO content_artifacts(artifact_id, run_date, artifact_type, title, status, score, path, source_file, created_at)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(artifact_id) DO UPDATE SET
                run_date=excluded.run_date,
                title=excluded.title,
                status=excluded.status,
                score=excluded.score,
                path=excluded.path,
                source_file=excluded.source_file,
                created_at=excluded.created_at
            """,
            (artifact_id, run_date, artifact_type, title_for(item), status_for(item), score_for(item), path_value, source_file, utc_now()),
        )
        count += 1
    return count


def upsert_publishing_candidates(connection: sqlite3.Connection, items: Iterable[dict[str, Any]], source_file: str) -> int:
    count = 0
    for item in items:
        candidate_id = str(item.get("publishing_candidate_id") or "")
        if not candidate_id:
            continue
        connection.execute(
            """
            INSERT INTO publishing_candidates(publishing_candidate_id, run_date, title, platforms, publish_status,
                publish_priority, human_confirmation_required, source_file, created_at)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(publishing_candidate_id) DO UPDATE SET
                title=excluded.title,
                platforms=excluded.platforms,
                publish_status=excluded.publish_status,
                publish_priority=excluded.publish_priority,
                human_confirmation_required=excluded.human_confirmation_required,
                created_at=excluded.created_at
            """,
            (
                candidate_id,
                str(item.get("run_date") or ""),
                str(item.get("title") or ""),
                json_text(item.get("platforms") or []),
                str(item.get("publish_status") or ""),
                str(item.get("publish_priority") or ""),
                1 if item.get("human_confirmation_required") else 0,
                source_file,
                utc_now(),
            ),
        )
        count += 1
    return count


def upsert_feedback(connection: sqlite3.Connection, items: Iterable[dict[str, Any]], source_file: str) -> int:
    count = 0
    for item in items:
        feedback_id = str(item.get("feedback_id") or "")
        if not feedback_id:
            continue
        connection.execute(
            """
            INSERT INTO human_feedback_records(feedback_id, run_date, publishing_candidate_id, human_action,
                human_score, feedback_tags, human_notes, source_file, created_at)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(feedback_id) DO UPDATE SET
                human_action=excluded.human_action,
                human_score=excluded.human_score,
                feedback_tags=excluded.feedback_tags,
                human_notes=excluded.human_notes,
                created_at=excluded.created_at
            """,
            (
                feedback_id,
                str(item.get("run_date") or ""),
                str(item.get("publishing_candidate_id") or ""),
                str(item.get("human_action") or ""),
                safe_float(item.get("human_score")) if item.get("human_score") is not None else None,
                json_text(item.get("feedback_tags") or []),
                str(item.get("human_notes") or ""),
                source_file,
                utc_now(),
            ),
        )
        count += 1
    return count


def upsert_weekly_retro(connection: sqlite3.Connection, payload: dict[str, Any], source_file: str) -> int:
    if not payload:
        return 0
    run_date = str(payload.get("run_date") or today_token()).replace("-", "")[:8]
    connection.execute(
        """
        INSERT INTO weekly_retros(run_date, status, summary_json, source_file, created_at)
        VALUES(?, ?, ?, ?, ?)
        ON CONFLICT(run_date) DO UPDATE SET
            status=excluded.status,
            summary_json=excluded.summary_json,
            source_file=excluded.source_file,
            created_at=excluded.created_at
        """,
        (run_date, str(payload.get("status") or ""), json_text(payload.get("summary") or {}), source_file, utc_now()),
    )
    return 1


def pipeline_specs(paths: ProjectPaths) -> tuple[tuple[str, Path], ...]:
    return (
        ("phase7_daily", paths.logs_root / "latest_phase7_daily_pipeline.json"),
        ("phase6_daily", paths.logs_root / "latest_phase6_daily_agent_pipeline.json"),
        ("learning_daily", paths.logs_root / "latest_learning_daily_pipeline.json"),
        ("phase5_daily", paths.logs_root / "latest_phase5_daily_learning_pipeline.json"),
        ("phase4_daily", paths.logs_root / "latest_phase4_daily_pipeline.json"),
        ("phase3_daily", paths.logs_root / "latest_phase3_daily_pipeline.json"),
        ("phase2_daily", paths.logs_root / "latest_phase2_daily_pipeline.json"),
        ("phase1_daily", paths.logs_root / "latest_phase1_daily_pipeline.json"),
    )


def content_specs(paths: ProjectPaths) -> tuple[tuple[str, Path, str], ...]:
    market = paths.market_content_root
    return (
        ("evidence_packet", market / "03_topic_candidates" / "latest_evidence_packets.json", "evidence_packets"),
        ("topic_cluster", market / "03_topic_candidates" / "latest_topic_clusters.json", "clusters"),
        ("high_value_candidate", market / "03_topic_candidates" / "latest_high_value_candidates.json", "candidates"),
        ("content_brief", market / "05_draft_packs" / "latest_content_briefs.json", "briefs"),
        ("content_outline", market / "05_draft_packs" / "latest_content_outlines.json", "outlines"),
        ("content_draft", market / "05_draft_packs" / "latest_content_drafts.json", "drafts"),
        ("quality_review", market / "05_draft_packs" / "latest_content_quality_review.json", "reviews"),
        ("platform_package", market / "05_draft_packs" / "latest_platform_packages.json", "packages"),
        ("review_queue_item", market / "06_review_queue" / "latest_agent_review_queue.json", "items"),
        ("judge_decision", market / "06_review_queue" / "latest_judge_gate.json", "decisions"),
        ("llm_judge_decision", market / "06_review_queue" / "latest_llm_judge_gate.json", "decisions"),
        ("publishing_candidate", market / "07_publishing" / "latest_publishing_candidate_queue.json", "candidates"),
        ("pattern_adapter", market / "08_learning_patterns" / "latest_pattern_adapters.json", "adapters"),
    )


def sync_runtime_store(paths: ProjectPaths, repo_root: Path, db_path: Path | None = None) -> RuntimeStoreSyncReport:
    final_db = init_runtime_store(paths, db_path)
    summary = {
        "pipeline_runs": 0,
        "agent_runs": 0,
        "source_health_snapshots": 0,
        "content_artifacts": 0,
        "publishing_candidates": 0,
        "human_feedback_records": 0,
        "weekly_retros": 0,
        "system_events": 0,
    }
    warnings: list[str] = []
    with connect(final_db) as connection:
        for pipeline_name, path in pipeline_specs(paths):
            rel = repo_relative(path, repo_root)
            payload = read_json(path)
            if payload:
                summary["pipeline_runs"] += upsert_pipeline(connection, payload, rel, pipeline_name)
            elif path.exists():
                upsert_system_event(connection, today_token(), "json_read_error", "WARN", f"Could not parse {rel}", rel)
                summary["system_events"] += 1

        agent_log_path = paths.logs_root / "agent_run_log.json"
        agent_log = read_json(agent_log_path)
        summary["agent_runs"] += upsert_agent_runs(connection, list_payload(agent_log, "records"), repo_relative(agent_log_path, repo_root))

        source_path = paths.logs_root / "latest_source_runtime_health.json"
        source_payload = read_json(source_path)
        if source_payload:
            summary["source_health_snapshots"] += upsert_source_health(connection, source_payload, repo_relative(source_path, repo_root))

        for artifact_type, path, list_key in content_specs(paths):
            payload = read_json(path)
            items = list_payload(payload, list_key)
            run_date = str(payload.get("run_date") or today_token()).replace("-", "")[:8]
            rel = repo_relative(path, repo_root)
            summary["content_artifacts"] += upsert_content_artifacts(connection, items, artifact_type, run_date, rel, rel)
            if artifact_type == "publishing_candidate":
                summary["publishing_candidates"] += upsert_publishing_candidates(connection, items, rel)

        feedback_path = paths.market_content_root / "07_publishing" / "latest_human_feedback_template.json"
        feedback = read_json(feedback_path)
        summary["human_feedback_records"] += upsert_feedback(connection, list_payload(feedback, "feedback_items"), repo_relative(feedback_path, repo_root))

        memory_path = paths.market_content_root / "07_publishing" / "review_outcome_memory.json"
        memory = read_json(memory_path)
        memory_items = list_payload(memory, "records")
        memory_feedback = []
        for item in memory_items:
            if item.get("publishing_candidate_id"):
                memory_feedback.append(
                    {
                        "feedback_id": f"memory:{item.get('publishing_candidate_id')}",
                        "run_date": item.get("run_date"),
                        "publishing_candidate_id": item.get("publishing_candidate_id"),
                        "human_action": item.get("human_action"),
                        "human_score": item.get("human_score"),
                        "feedback_tags": item.get("feedback_tags"),
                        "human_notes": item.get("human_notes"),
                    }
                )
        summary["human_feedback_records"] += upsert_feedback(connection, memory_feedback, repo_relative(memory_path, repo_root))

        retro_path = paths.logs_root / "latest_weekly_content_retro.json"
        summary["weekly_retros"] += upsert_weekly_retro(connection, read_json(retro_path), repo_relative(retro_path, repo_root))
        connection.commit()

    status = "DEGRADED" if warnings else "SUCCESS"
    return RuntimeStoreSyncReport(SCHEMA_VERSION, utc_now(), today_token(), str(final_db), status, summary, tuple(warnings))


def count_table(connection: sqlite3.Connection, table: str) -> int:
    return int(connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])


def runtime_store_summary(paths: ProjectPaths, db_path: Path | None = None) -> dict[str, Any]:
    final_db = db_path or default_db_path(paths)
    init_runtime_store(paths, final_db)
    with connect(final_db) as connection:
        latest_pipeline = connection.execute(
            "SELECT pipeline_name, status, run_date FROM pipeline_runs ORDER BY created_at DESC, id DESC LIMIT 1"
        ).fetchone()
        failed_agents = connection.execute("SELECT COUNT(*) FROM agent_runs WHERE status='FAILED'").fetchone()[0]
        estimated_cost = connection.execute("SELECT COALESCE(SUM(estimated_cost_usd), 0) FROM agent_runs").fetchone()[0]
        events = [
            dict(row)
            for row in connection.execute(
                "SELECT run_date, event_type, severity, message, source_file FROM system_events ORDER BY id DESC LIMIT 20"
            ).fetchall()
        ]
        return {
            "db_path": str(final_db),
            "pipeline_runs": count_table(connection, "pipeline_runs"),
            "agent_runs": count_table(connection, "agent_runs"),
            "source_health_snapshots": count_table(connection, "source_health_snapshots"),
            "content_artifacts": count_table(connection, "content_artifacts"),
            "publishing_candidates": count_table(connection, "publishing_candidates"),
            "human_feedback_records": count_table(connection, "human_feedback_records"),
            "weekly_retros": count_table(connection, "weekly_retros"),
            "system_events": count_table(connection, "system_events"),
            "latest_pipeline": dict(latest_pipeline) if latest_pipeline else {},
            "agent_failed_count": int(failed_agents),
            "estimated_cost_usd": round(float(estimated_cost or 0.0), 6),
            "recent_system_events": events,
        }


def summary_output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__runtime-store-summary.json",
        "dated_md": paths.logs_root / f"{run_date}__runtime-store-summary.md",
        "latest_json": paths.logs_root / "latest_runtime_store_summary.json",
        "latest_md": paths.logs_root / "latest_runtime_store_summary.md",
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__runtime-store-summary-board.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_runtime_store_summary_board.md",
    }


def render_runtime_store_summary_markdown(summary: dict[str, Any], run_date: str) -> str:
    events = summary.get("recent_system_events") or []
    event_lines = "\n".join(f"- `{item.get('severity')}` {item.get('event_type')}: {item.get('message')}" for item in events) or "- None"
    latest = summary.get("latest_pipeline") or {}
    return f"""# Runtime Store Summary

## Summary

- Run date: `{run_date}`
- Database: `{summary.get('db_path')}`
- Pipeline runs: `{summary.get('pipeline_runs')}`
- Agent runs: `{summary.get('agent_runs')}`
- Source health snapshots: `{summary.get('source_health_snapshots')}`
- Content artifacts: `{summary.get('content_artifacts')}`
- Publishing candidates: `{summary.get('publishing_candidates')}`
- Human feedback records: `{summary.get('human_feedback_records')}`
- Weekly retros: `{summary.get('weekly_retros')}`
- System events: `{summary.get('system_events')}`

## Latest Pipeline

- Pipeline: `{latest.get('pipeline_name', '-')}`
- Status: `{latest.get('status', '-')}`
- Run date: `{latest.get('run_date', '-')}`

## Agent Health

- Failed agent runs: `{summary.get('agent_failed_count')}`
- Estimated cost USD: `{summary.get('estimated_cost_usd')}`

## Recent System Events

{event_lines}
"""


def write_runtime_store_summary(paths: ProjectPaths, summary: dict[str, Any], run_date: str | None = None) -> dict[str, Path]:
    final_run_date = run_date or today_token()
    outputs = summary_output_paths(paths, final_run_date)
    for path in outputs.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": final_run_date, "summary": summary}
    markdown = render_runtime_store_summary_markdown(summary, final_run_date)
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    for path in (outputs["dated_json"], outputs["latest_json"]):
        path.write_text(text + "\n", encoding="utf-8")
    for path in (outputs["dated_md"], outputs["latest_md"], outputs["frontstage_dated_md"], outputs["frontstage_latest_md"]):
        path.write_text(markdown, encoding="utf-8")
    return outputs


def report_to_dict(report: RuntimeStoreSyncReport) -> dict[str, Any]:
    return asdict(report)
