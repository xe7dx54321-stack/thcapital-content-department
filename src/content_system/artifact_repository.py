"""Repository API over the local SQLite runtime store."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.runtime_store import connect, default_db_path, init_runtime_store


def _db(paths: ProjectPaths, db_path: Path | None = None) -> Path:
    final_path = db_path or default_db_path(paths)
    init_runtime_store(paths, final_path)
    return final_path


def _rows(query: str, params: tuple[Any, ...], paths: ProjectPaths, db_path: Path | None = None) -> list[dict[str, Any]]:
    with connect(_db(paths, db_path)) as connection:
        return [dict(row) for row in connection.execute(query, params).fetchall()]


def list_recent_artifacts(paths: ProjectPaths, artifact_type: str | None = None, limit: int = 20, db_path: Path | None = None) -> list[dict[str, Any]]:
    if artifact_type:
        return _rows(
            """
            SELECT artifact_id, run_date, artifact_type, title, status, score, path, source_file, created_at
            FROM content_artifacts
            WHERE artifact_type = ?
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (artifact_type, limit),
            paths,
            db_path,
        )
    return _rows(
        """
        SELECT artifact_id, run_date, artifact_type, title, status, score, path, source_file, created_at
        FROM content_artifacts
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (limit,),
        paths,
        db_path,
    )


def get_artifact_by_id(paths: ProjectPaths, artifact_id: str, db_path: Path | None = None) -> dict[str, Any]:
    rows = _rows(
        """
        SELECT artifact_id, run_date, artifact_type, title, status, score, path, source_file, created_at
        FROM content_artifacts
        WHERE artifact_id = ?
        LIMIT 1
        """,
        (artifact_id,),
        paths,
        db_path,
    )
    return rows[0] if rows else {}


def list_recent_agent_runs(paths: ProjectPaths, agent_name: str | None = None, limit: int = 20, db_path: Path | None = None) -> list[dict[str, Any]]:
    if agent_name:
        return _rows(
            """
            SELECT request_id, run_date, agent_name, provider_id, model, mode, status, latency_ms,
                   estimated_input_tokens, estimated_output_tokens, estimated_cost_usd, fallback_used, error, source_file, created_at
            FROM agent_runs
            WHERE agent_name = ?
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (agent_name, limit),
            paths,
            db_path,
        )
    return _rows(
        """
        SELECT request_id, run_date, agent_name, provider_id, model, mode, status, latency_ms,
               estimated_input_tokens, estimated_output_tokens, estimated_cost_usd, fallback_used, error, source_file, created_at
        FROM agent_runs
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (limit,),
        paths,
        db_path,
    )


def list_publishing_candidates(paths: ProjectPaths, status: str | None = None, limit: int = 20, db_path: Path | None = None) -> list[dict[str, Any]]:
    if status:
        return _rows(
            """
            SELECT publishing_candidate_id, run_date, title, platforms, publish_status, publish_priority,
                   human_confirmation_required, source_file, created_at
            FROM publishing_candidates
            WHERE publish_status = ?
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (status, limit),
            paths,
            db_path,
        )
    return _rows(
        """
        SELECT publishing_candidate_id, run_date, title, platforms, publish_status, publish_priority,
               human_confirmation_required, source_file, created_at
        FROM publishing_candidates
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (limit,),
        paths,
        db_path,
    )


def list_human_feedback(paths: ProjectPaths, limit: int = 20, db_path: Path | None = None) -> list[dict[str, Any]]:
    return _rows(
        """
        SELECT feedback_id, run_date, publishing_candidate_id, human_action, human_score, feedback_tags,
               human_notes, source_file, created_at
        FROM human_feedback_records
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (limit,),
        paths,
        db_path,
    )


def search_artifacts_by_title(paths: ProjectPaths, keyword: str, limit: int = 20, db_path: Path | None = None) -> list[dict[str, Any]]:
    like = f"%{keyword}%"
    return _rows(
        """
        SELECT artifact_id, run_date, artifact_type, title, status, score, path, source_file, created_at
        FROM content_artifacts
        WHERE title LIKE ?
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (like, limit),
        paths,
        db_path,
    )


def repository_summary(paths: ProjectPaths, db_path: Path | None = None) -> dict[str, Any]:
    return {
        "recent_artifacts": list_recent_artifacts(paths, limit=10, db_path=db_path),
        "recent_agent_runs": list_recent_agent_runs(paths, limit=10, db_path=db_path),
        "publishing_candidates": list_publishing_candidates(paths, limit=10, db_path=db_path),
        "human_feedback": list_human_feedback(paths, limit=10, db_path=db_path),
    }
