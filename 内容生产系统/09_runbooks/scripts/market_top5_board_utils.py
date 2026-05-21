from __future__ import annotations

import re
from pathlib import Path


TOP5_SECTION_HEADER = "## Top 5 Recommended"
HOLDOUT_SECTION_HEADER = "## Holdout 3"


def clean(value: str) -> str:
    return value.strip().strip("`").strip()


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_markdown_table(lines: list[str], section_header: str) -> list[list[str]]:
    rows: list[list[str]] = []
    in_section = False
    table_started = False
    for line in lines:
        if line.startswith(section_header):
            in_section = True
            continue
        if not in_section:
            continue
        if line.startswith("## ") and not line.startswith(section_header):
            break
        if not line.strip():
            continue
        if line.lstrip().startswith("|"):
            table_started = True
            rows.append(split_row(line))
            continue
        if table_started:
            break
    if len(rows) < 2:
        return []
    cleaned_rows: list[list[str]] = []
    for row in rows[1:]:
        joined = "".join(cell.replace("-", "").replace(" ", "") for cell in row)
        if not joined:
            continue
        cleaned_rows.append(row)
    return cleaned_rows


def _candidate_keys_from_rows(rows: list[list[str]], index: int) -> list[str]:
    keys: list[str] = []
    for row in rows:
        if len(row) <= index:
            continue
        key = clean(row[index])
        if not key or key.lower() in {"candidate_key", "n/a"}:
            continue
        keys.append(key)
    return keys


def top5_candidate_keys(board_path: Path) -> list[str]:
    if not board_path.exists():
        return []
    lines = board_path.read_text(encoding="utf-8").splitlines()
    top5_rows = parse_markdown_table(lines, TOP5_SECTION_HEADER)
    holdout_rows = parse_markdown_table(lines, HOLDOUT_SECTION_HEADER)
    keys = _candidate_keys_from_rows(top5_rows, 1)
    keys.extend(_candidate_keys_from_rows(holdout_rows, 1))

    deduped: list[str] = []
    seen: set[str] = set()
    for key in keys:
        if key in seen:
            continue
        seen.add(key)
        deduped.append(key)
    return deduped


def top5_board_is_ready(board_path: Path) -> bool:
    return bool(top5_candidate_keys(board_path))
