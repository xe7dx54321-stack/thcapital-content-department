#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from market_publish_queue_builder import DEFAULT_QUEUE_ROOT, rebuild_board


CN_TZ = ZoneInfo("Asia/Shanghai")
DATE_PREFIX_RE = re.compile(r"^(\d{8})")
ARCHIVE_FILE_RE = re.compile(r"^\d{8}(?:_\d{6})?.*__(?:publish-queue-item|publish-queue-board)\.md$")


@dataclass
class ArchiveMove:
    source: Path
    target: Path
    date_token: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Archive old publish queue files while keeping current-day queue clean")
    parser.add_argument("--keep-date", required=True, help="Keep this business date in root, YYYY-MM-DD")
    parser.add_argument("--queue-root", default=str(DEFAULT_QUEUE_ROOT))
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def keep_token(date_text: str) -> str:
    return datetime.strptime(date_text, "%Y-%m-%d").strftime("%Y%m%d")


def now_cst() -> str:
    return datetime.now(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def candidate_moves(queue_root: Path, keep_day_token: str) -> list[ArchiveMove]:
    moves: list[ArchiveMove] = []
    archive_root = queue_root / "archive"
    for path in sorted(queue_root.glob("*")):
        if not path.is_file():
            continue
        if not ARCHIVE_FILE_RE.match(path.name):
            continue
        match = DATE_PREFIX_RE.match(path.name)
        if not match:
            continue
        token = match.group(1)
        if token >= keep_day_token:
            continue
        target = archive_root / token / path.name
        moves.append(ArchiveMove(source=path, target=target, date_token=token))
    return moves


def archive_log_text(queue_root: Path, keep_day_token: str, moves: list[ArchiveMove]) -> str:
    archive_root = queue_root / "archive"
    grouped: dict[str, list[ArchiveMove]] = defaultdict(list)
    for move in moves:
        grouped[move.date_token].append(move)

    lines = [
        "# Publish Queue Archive Log",
        "",
        f"- `generated_at`: `{now_cst()}`",
        f"- `keep_token`: `{keep_day_token}`",
        f"- `queue_root`: `{queue_root}`",
        f"- `archive_root`: `{archive_root}`",
        f"- `moved_file_count`: `{len(moves)}`",
        "",
        "## Moved Groups",
        "",
    ]
    if not moves:
        lines.append("- `none`")
    else:
        for token in sorted(grouped):
            lines.append(f"### `{token}`")
            lines.append("")
            for move in grouped[token]:
                lines.append(f"- `{move.source.name}` -> `{move.target}`")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    queue_root = Path(args.queue_root)
    queue_root.mkdir(parents=True, exist_ok=True)
    keep_day_token = keep_token(args.keep_date)
    moves = candidate_moves(queue_root, keep_day_token)
    archive_root = queue_root / "archive"
    log_path = archive_root / f"{keep_day_token}__publish-queue-archive-log.md"
    board_path = queue_root / f"{keep_day_token}__publish-queue-board.md"
    log_text = archive_log_text(queue_root, keep_day_token, moves)

    if args.write:
        archive_root.mkdir(parents=True, exist_ok=True)
        for move in moves:
            move.target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(move.source), str(move.target))
        rebuild_board(queue_root, board_path)
        log_path.write_text(log_text, encoding="utf-8")
        print(board_path)
        print(log_path)
        for move in moves:
            print(move.target)
        return

    print(log_text)


if __name__ == "__main__":
    main()
