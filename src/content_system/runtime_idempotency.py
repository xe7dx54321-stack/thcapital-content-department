"""Idempotency key helpers for runtime jobs."""

from __future__ import annotations

import hashlib
import re
from typing import Any


def _slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.:-]+", "-", value.strip()).strip("-")


def idempotency_key(job_id: str, business_date: str, schedule_slot: str = "", scope: str = "daily") -> str:
    job = _slug(job_id)
    day = _slug(business_date)
    slot = _slug(schedule_slot)
    if scope == "daily_slot":
        return f"{job}:{day}:{slot or 'unslotted'}"
    if scope == "weekly":
        return f"{job}:week:{day[:7]}:{slot or 'weekly'}"
    if scope == "artifact_version":
        return f"{job}:artifact:{day}:{slot or 'latest'}"
    return f"{job}:{day}"


def artifact_idempotency_key(job_id: str, artifact_refs: list[Any]) -> str:
    normalized = "|".join(sorted(str(item) for item in artifact_refs))
    digest = hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:12] if normalized else "none"
    return f"{_slug(job_id)}:artifact:{digest}"


def duplicate_run_prevented(existing_run: dict[str, Any]) -> bool:
    return existing_run.get("status") in {"SUCCESS", "ACTIONABLE", "DEGRADED", "RUNNING"}
