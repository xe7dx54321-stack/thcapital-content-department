#!/usr/bin/env python3
"""Audit hardcoded local paths in the repository.

P0-002 builds a map of portability risks. It intentionally does not rewrite
existing business scripts; it only reports findings for later configuration work.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]

PATTERNS = {
    "mac_user_path": re.compile(r"/Users/[A-Za-z0-9._-]+/[^\s\"'`<>)]*"),
    "mac_volume_path": re.compile(r"/Volumes/[^\s\"'`<>)]*"),
    "windows_drive_path": re.compile(r"\b[A-Za-z]:[\\/][^\s\"'`<>)]*"),
    "file_url": re.compile(r"file://[^\s\"'`<>)]*"),
    "home_documents_path": re.compile(r"~/[^\s\"'`<>)]*"),
}

EXCLUDED_DIR_NAMES = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".DS_Store",
    "runtime",
    "tmp",
    ".cache",
}

SKIPPED_FILE_NAMES = {
    ".DS_Store",
    "latest_doctor_report.json",
    "latest_path_hardcode_audit.md",
    "latest_path_hardcode_audit.json",
}

BINARY_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
    ".tgz",
    ".sqlite",
    ".sqlite3",
    ".db",
    ".pyc",
    ".docx",
    ".xlsx",
    ".pptx",
    ".mp4",
    ".mov",
}

CODE_SUFFIXES = {".py", ".sh", ".command"}
CONFIG_SUFFIXES = {".yaml", ".yml", ".json", ".toml", ".env", ".example"}
TEXT_SUFFIXES = {".md", ".txt", ".html", ".css", ".js", ".jsx", ".ts", ".tsx", ".sql", ".csv"}
RUNNING_PARTS = {"scripts", "src", "内容工厂控制台", "config"}
HISTORICAL_PARTS = {"_archive", "archive", "archives", "备份", "归档", "00_planning", "planning", "docs"}
RUNBOOK_PARTS = {"09_runbooks", "runbooks", "templates"}


@dataclass(frozen=True)
class Finding:
    file: str
    line: int
    column: int
    pattern: str
    risk: str
    match: str
    line_text: str


@dataclass(frozen=True)
class ScanResult:
    findings: list[Finding]
    files_scanned: int
    files_with_findings: int
    files_skipped_decode: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit hardcoded local paths.")
    parser.add_argument("--fail-on-high", action="store_true", help="Exit 1 when HIGH findings exist.")
    parser.add_argument("--max-md-items", type=int, default=100, help="Maximum findings per risk section in Markdown.")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="Repository root. Defaults to this script's repo.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Report output directory.")
    return parser.parse_args()


def is_under_excluded_dir(path: Path, root: Path) -> bool:
    try:
        relative_parts = path.relative_to(root).parts
    except ValueError:
        relative_parts = path.parts
    return any(part in EXCLUDED_DIR_NAMES for part in relative_parts)


def should_skip_file(path: Path, root: Path) -> bool:
    if path.name in SKIPPED_FILE_NAMES:
        return True
    if path.name.endswith("__path-hardcode-audit.md") or path.name.endswith("__path-hardcode-audit.json"):
        return True
    if is_under_excluded_dir(path, root):
        return True
    if path.suffix.lower() in BINARY_SUFFIXES:
        return True
    if path.name in {"Makefile", "Dockerfile"}:
        return False
    if path.suffix.lower() in CODE_SUFFIXES | CONFIG_SUFFIXES | TEXT_SUFFIXES:
        return False
    return True


def iter_scan_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if should_skip_file(path, root):
            continue
        yield path


def read_text(path: Path) -> tuple[str | None, bool]:
    try:
        return path.read_text(encoding="utf-8"), False
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8", errors="ignore"), True
        except OSError:
            return None, True
    except OSError:
        return None, True


def is_obvious_comment(line_text: str, suffix: str) -> bool:
    stripped = line_text.lstrip()
    if not stripped:
        return False
    if stripped.startswith("#"):
        return True
    if suffix in {".py", ".sh", ".command", ".yaml", ".yml", ".toml", ".env"}:
        return stripped.startswith("#")
    if suffix in {".js", ".jsx", ".ts", ".tsx", ".css"}:
        return stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*")
    return False


def classify_risk(relative_path: str, line_text: str) -> str:
    path = Path(relative_path)
    parts = set(path.parts)
    suffix = path.suffix.lower()

    if parts & HISTORICAL_PARTS:
        return "LOW"

    is_comment = is_obvious_comment(line_text, suffix)
    is_code_or_entry = suffix in CODE_SUFFIXES or path.name in {"Makefile", "Dockerfile"}
    is_runtime_config = suffix in CONFIG_SUFFIXES and bool(parts & (RUNNING_PARTS | RUNBOOK_PARTS))
    is_runbook_or_template = bool(parts & RUNBOOK_PARTS)
    is_running_location = bool(parts & RUNNING_PARTS) or "09_runbooks/scripts" in relative_path

    if (is_code_or_entry or is_runtime_config or is_running_location) and not is_comment:
        return "HIGH"
    if "config" in parts and is_comment:
        return "MEDIUM"
    if is_comment and (is_code_or_entry or is_runtime_config):
        return "MEDIUM"
    if is_runbook_or_template:
        return "MEDIUM"
    if suffix in CONFIG_SUFFIXES:
        return "MEDIUM"
    if suffix in {".md", ".txt", ".html"}:
        return "LOW"
    return "LOW"


def clean_match(value: str) -> str:
    return value.rstrip(".,;:]}")


def should_ignore_match(relative_path: str, line_text: str, matched_text: str) -> bool:
    if relative_path == "scripts/audit_hardcoded_paths.py" and "re.compile(" in line_text:
        return True
    return "[^" in matched_text or "\\s" in matched_text or "[A-Za-z" in matched_text


def scan_file(root: Path, path: Path) -> list[Finding]:
    text, _decode_warning = read_text(path)
    if text is None:
        return []

    relative_path = path.relative_to(root).as_posix()
    findings: list[Finding] = []

    for line_number, line_text in enumerate(text.splitlines(), start=1):
        for pattern_name, pattern in PATTERNS.items():
            for match in pattern.finditer(line_text):
                matched_text = clean_match(match.group(0))
                if should_ignore_match(relative_path, line_text, matched_text):
                    continue
                findings.append(
                    Finding(
                        file=relative_path,
                        line=line_number,
                        column=match.start() + 1,
                        pattern=pattern_name,
                        risk=classify_risk(relative_path, line_text),
                        match=matched_text,
                        line_text=line_text.strip()[:500],
                    )
                )

    return findings


def scan_repo(root: Path) -> ScanResult:
    findings: list[Finding] = []
    files_scanned = 0
    files_with_findings = 0
    files_skipped_decode = 0

    for path in iter_scan_files(root):
        text, decode_warning = read_text(path)
        if text is None:
            files_skipped_decode += 1
            continue
        if decode_warning:
            files_skipped_decode += 1

        files_scanned += 1
        relative_path = path.relative_to(root).as_posix()
        file_findings: list[Finding] = []

        for line_number, line_text in enumerate(text.splitlines(), start=1):
            for pattern_name, pattern in PATTERNS.items():
                for match in pattern.finditer(line_text):
                    matched_text = clean_match(match.group(0))
                    if should_ignore_match(relative_path, line_text, matched_text):
                        continue
                    file_findings.append(
                        Finding(
                            file=relative_path,
                            line=line_number,
                            column=match.start() + 1,
                            pattern=pattern_name,
                            risk=classify_risk(relative_path, line_text),
                            match=matched_text,
                            line_text=line_text.strip()[:500],
                        )
                    )

        if file_findings:
            files_with_findings += 1
            findings.extend(file_findings)

    risk_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    findings.sort(key=lambda item: (risk_order.get(item.risk, 9), item.file, item.line, item.column, item.pattern))
    return ScanResult(
        findings=findings,
        files_scanned=files_scanned,
        files_with_findings=files_with_findings,
        files_skipped_decode=files_skipped_decode,
    )


def build_summary(result: ScanResult) -> dict[str, int]:
    high = sum(1 for item in result.findings if item.risk == "HIGH")
    medium = sum(1 for item in result.findings if item.risk == "MEDIUM")
    low = sum(1 for item in result.findings if item.risk == "LOW")
    return {
        "total_findings": len(result.findings),
        "high": high,
        "medium": medium,
        "low": low,
        "files_scanned": result.files_scanned,
        "files_with_findings": result.files_with_findings,
    }


def build_payload(root: Path, result: ScanResult) -> dict[str, object]:
    return {
        "schema_version": "v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": ".",
        "summary": build_summary(result),
        "findings": [asdict(item) for item in result.findings],
    }


def escape_table_cell(value: object, max_length: int = 160) -> str:
    text = str(value).replace("\n", " ").replace("\r", " ")
    text = text.replace("|", "\\|")
    if len(text) > max_length:
        return text[: max_length - 1] + "..."
    return text


def recommendation_for(finding: Finding) -> str:
    if finding.risk == "HIGH":
        return "优先改为环境变量、配置项或基于仓库根目录的相对路径。"
    if finding.risk == "MEDIUM":
        return "确认是否参与运行；如参与运行，纳入 P0-003 配置化。"
    return "保留历史记录即可；如会被脚本读取，再逐步清理。"


def conclusion(summary: dict[str, int]) -> str:
    if summary["total_findings"] == 0:
        return "未发现目标类型的硬编码路径。"
    if summary["high"] > 0:
        return f"发现 {summary['high']} 个 HIGH 风险项，P0-003 应优先处理运行脚本、控制台入口和配置文件。"
    if summary["medium"] > 0:
        return "未发现 HIGH 风险项，但存在 MEDIUM 项，建议核对其是否参与运行。"
    return "仅发现 LOW 风险项，主要集中在历史文档或说明材料中。"


def render_section(title: str, findings: list[Finding], max_items: int) -> list[str]:
    lines = [f"## {title}", ""]
    if not findings:
        lines.extend(["无。", ""])
        return lines

    lines.extend(
        [
            "| 文件 | 行号 | 类型 | 命中内容 | 建议 |",
            "|---|---:|---|---|---|",
        ]
    )
    for item in findings[:max_items]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_table_cell(item.file, 120)}`",
                    str(item.line),
                    f"`{escape_table_cell(item.pattern, 40)}`",
                    f"`{escape_table_cell(item.match, 140)}`",
                    escape_table_cell(recommendation_for(item), 120),
                ]
            )
            + " |"
        )
    if len(findings) > max_items:
        lines.append("")
        lines.append(f"仅展示前 {max_items} 条；完整 findings 请查看 JSON 报告。")
    lines.append("")
    return lines


def render_markdown(payload: dict[str, object], max_items: int) -> str:
    summary = payload["summary"]
    assert isinstance(summary, dict)
    findings = [Finding(**item) for item in payload["findings"]]  # type: ignore[arg-type]

    by_risk = {
        "HIGH": [item for item in findings if item.risk == "HIGH"],
        "MEDIUM": [item for item in findings if item.risk == "MEDIUM"],
        "LOW": [item for item in findings if item.risk == "LOW"],
    }

    lines = [
        "# 路径硬编码审计报告",
        "",
        f"生成时间：`{payload['generated_at']}`",
        f"扫描文件数：`{summary['files_scanned']}`",
        f"命中总数：`{summary['total_findings']}`",
        f"HIGH：`{summary['high']}`",
        f"MEDIUM：`{summary['medium']}`",
        f"LOW：`{summary['low']}`",
        "",
        "## 结论摘要",
        "",
        conclusion(summary),  # type: ignore[arg-type]
        "",
    ]

    lines.extend(render_section("HIGH 风险项", by_risk["HIGH"], max_items))
    lines.extend(render_section("MEDIUM 风险项", by_risk["MEDIUM"], max_items))
    lines.extend(render_section("LOW 风险项", by_risk["LOW"], max_items))
    lines.extend(
        [
            "## 下一步建议",
            "",
            "1. P0-003 优先处理 HIGH 风险项中的运行脚本、控制台入口和配置文件。",
            "2. 不一次性替换历史文档中的路径，避免制造无意义的大 diff。",
            "3. 建议引入统一路径配置策略，优先使用仓库根目录相对路径和环境变量。",
            "4. 每次路径配置化后重新运行 `make path-audit`，观察 HIGH 数量是否下降。",
            "",
        ]
    )
    return "\n".join(lines)


def resolve_output_dir(root: Path, output_dir: Path) -> Path:
    if output_dir.is_absolute():
        return output_dir
    return root / output_dir


def write_reports(root: Path, output_dir: Path, payload: dict[str, object], markdown: str) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    date_key = datetime.now().strftime("%Y%m%d")

    dated_md = output_dir / f"{date_key}__path-hardcode-audit.md"
    dated_json = output_dir / f"{date_key}__path-hardcode-audit.json"
    latest_md = output_dir / "latest_path_hardcode_audit.md"
    latest_json = output_dir / "latest_path_hardcode_audit.json"

    json_text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    markdown_text = markdown.rstrip() + "\n"

    dated_json.write_text(json_text, encoding="utf-8")
    dated_md.write_text(markdown_text, encoding="utf-8")
    latest_json.write_text(json_text, encoding="utf-8")
    latest_md.write_text(markdown_text, encoding="utf-8")

    return dated_md.relative_to(root), dated_json.relative_to(root)


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    requested_output = args.output_dir or (root / "同行资本市场内容系统" / "10_logs")
    output_dir = resolve_output_dir(root, requested_output)

    if not root.exists():
        print(f"root not found: {root}", file=sys.stderr)
        return 2

    result = scan_repo(root)
    payload = build_payload(root, result)
    markdown = render_markdown(payload, max_items=args.max_md_items)
    md_path, json_path = write_reports(root, output_dir, payload, markdown)
    summary = payload["summary"]
    assert isinstance(summary, dict)

    print("路径硬编码审计完成")
    print(f"扫描文件数: {summary['files_scanned']}")
    print(f"命中总数: {summary['total_findings']}")
    print(f"HIGH: {summary['high']}")
    print(f"MEDIUM: {summary['medium']}")
    print(f"LOW: {summary['low']}")
    print(f"Markdown: {md_path.as_posix()}")
    print(f"JSON: {json_path.as_posix()}")

    if args.fail_on_high and int(summary["high"]) > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
