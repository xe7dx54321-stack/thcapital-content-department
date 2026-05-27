"""SQLite schema for the local runtime store."""

from __future__ import annotations


SCHEMA_VERSION = "v1"

CREATE_TABLES_SQL = (
    """
    CREATE TABLE IF NOT EXISTS pipeline_runs (
        id INTEGER PRIMARY KEY,
        run_id TEXT UNIQUE,
        run_date TEXT,
        pipeline_name TEXT,
        status TEXT,
        started_at TEXT,
        finished_at TEXT,
        summary_json TEXT,
        source_file TEXT,
        created_at TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS agent_runs (
        id INTEGER PRIMARY KEY,
        request_id TEXT UNIQUE,
        run_date TEXT,
        agent_name TEXT,
        provider_id TEXT,
        model TEXT,
        mode TEXT,
        status TEXT,
        latency_ms INTEGER,
        estimated_input_tokens INTEGER,
        estimated_output_tokens INTEGER,
        estimated_cost_usd REAL,
        fallback_used INTEGER,
        error TEXT,
        source_file TEXT,
        created_at TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS source_health_snapshots (
        id INTEGER PRIMARY KEY,
        run_date TEXT,
        source_id TEXT,
        status TEXT,
        items_found INTEGER,
        missing_expected INTEGER,
        error_hint TEXT,
        source_file TEXT,
        created_at TEXT,
        UNIQUE(run_date, source_id, source_file)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS content_artifacts (
        id INTEGER PRIMARY KEY,
        artifact_id TEXT UNIQUE,
        run_date TEXT,
        artifact_type TEXT,
        title TEXT,
        status TEXT,
        score REAL,
        path TEXT,
        source_file TEXT,
        created_at TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS publishing_candidates (
        id INTEGER PRIMARY KEY,
        publishing_candidate_id TEXT UNIQUE,
        run_date TEXT,
        title TEXT,
        platforms TEXT,
        publish_status TEXT,
        publish_priority TEXT,
        human_confirmation_required INTEGER,
        source_file TEXT,
        created_at TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS human_feedback_records (
        id INTEGER PRIMARY KEY,
        feedback_id TEXT UNIQUE,
        run_date TEXT,
        publishing_candidate_id TEXT,
        human_action TEXT,
        human_score REAL,
        feedback_tags TEXT,
        human_notes TEXT,
        source_file TEXT,
        created_at TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS weekly_retros (
        id INTEGER PRIMARY KEY,
        run_date TEXT UNIQUE,
        status TEXT,
        summary_json TEXT,
        source_file TEXT,
        created_at TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS system_events (
        id INTEGER PRIMARY KEY,
        event_id TEXT UNIQUE,
        run_date TEXT,
        event_type TEXT,
        severity TEXT,
        message TEXT,
        source_file TEXT,
        created_at TEXT
    )
    """,
)

CREATE_INDEXES_SQL = (
    "CREATE INDEX IF NOT EXISTS idx_pipeline_runs_date ON pipeline_runs(run_date)",
    "CREATE INDEX IF NOT EXISTS idx_agent_runs_date_agent ON agent_runs(run_date, agent_name)",
    "CREATE INDEX IF NOT EXISTS idx_source_health_date_source ON source_health_snapshots(run_date, source_id)",
    "CREATE INDEX IF NOT EXISTS idx_content_artifacts_type_date ON content_artifacts(artifact_type, run_date)",
    "CREATE INDEX IF NOT EXISTS idx_content_artifacts_title ON content_artifacts(title)",
    "CREATE INDEX IF NOT EXISTS idx_publishing_status ON publishing_candidates(publish_status, run_date)",
    "CREATE INDEX IF NOT EXISTS idx_feedback_candidate ON human_feedback_records(publishing_candidate_id)",
    "CREATE INDEX IF NOT EXISTS idx_system_events_date ON system_events(run_date, severity)",
)

DROP_TABLES_SQL = tuple(
    f"DROP TABLE IF EXISTS {name}"
    for name in (
        "pipeline_runs",
        "agent_runs",
        "source_health_snapshots",
        "content_artifacts",
        "publishing_candidates",
        "human_feedback_records",
        "weekly_retros",
        "system_events",
    )
)
