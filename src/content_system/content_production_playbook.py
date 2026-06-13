"""Content production playbook build and validation entry points."""

from __future__ import annotations

from pathlib import Path

from content_system.paths import ProjectPaths
from content_system.phase32_content_production import build_content_playbook_report, validate_content_playbooks


def build_content_production_playbooks(paths: ProjectPaths, repo_root: Path):
    return build_content_playbook_report(paths, repo_root)


def validate_content_production_playbooks(paths: ProjectPaths, repo_root: Path):
    return validate_content_playbooks(paths, repo_root)

