#!/usr/bin/env python3
"""扫描仓库中的硬编码路径，并输出可审计报告。

P0-002 的目标不是立刻修改所有历史脚本，而是先把路径问题地图画出来：
- 找出 /Users/...、/Volumes/...、Windows 盘符路径、file:// 等硬编码路径。
- 按文件位置和扩展名给出风险等级。
- 生成 Markdown + JSON 报告，供后续逐步配置化改造。

运行：
    python3 scripts/audit_hardcoded_paths.py --write
    make path-audit
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
DEFAULT_LOGS_DIR = REPO_ROOT / "同行资本市场内容系统" / "10_logs"

SCAN_EXTENSIONS = {
    ".py",
    ".sh",
    ".command",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".sql",
    ".env",
    ".example",
}

EXCLUDED_DIR_NAMES = {
    ".git",
    ".github",
    ".idea",
    ".vscode",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    ".venv",
    "venv",
    "runtime",
}

ARCHIVE_DIR_NAMES = {
    "_archive",
    "archive",
    "archives",
    "备份",
    "归档",
}

PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    (
        "mac_user_path",
        re.compile(r"/Users/[A-Za-z0-9_.\-\u4e00-\u9fff]+(?:/[A-Za-z0-9_.\-\u4e00-\u9fff ()]+)+"),
        "macOS 用户目录绝对路径，换机器或换用户名后容易失效。",
    ),
    (
        "mac_volume_path",
        re.compile(r"/Volumes/[A-Za-z0-9_.\-\u4e00-\u9fff ]+(?:/[A-Za-z0-9_.\-\u4e00-\u9fff ()]+)+"),
        "macOS 外接盘/卷绝对路径，依赖本机挂载状态。",
    ),
    (
        "windows_drive_path",
        re.compile(r"\b[A-Za-z]:[\\/][^\s\"'`<>|]+"),
        "Windows 盘符绝对路径，跨系统不可移植。",
    ),
    (
        "file_url_path",
        re.compile(r"file://[^\s\"'`<>]+"),
        "本地 file:// URL，通常不能跨机器访问。",
    ),
]


@dataclass(frozen=True)
class Finding:
    file: str
    line: int
    kind: str
    severity: str
    match: str
    context: str
    recommendation: str


def is_archive_path(path: Path) -> bool:
    return any(part in ARCHIVE_DIR_NAMES for part in path.parts)


def should_skip_dir(path: Path, include_archive: bool) -> bool:
    if path.name in EXCLUDED_DIR_NAMES:
        return True
    if not include_archive and path.name in ARCHIVE_DIR_NAMES:
        return True
    return False


def should_scan_file(path: Path) -> bool:
    if path.name.startswith(".") and path.suffix not in {".env", ".example"}:
        return False
    if path.suffix in SCAN_EXTENSIONS:
        return True
    if path.name in {"Makefile", "Dockerfile", "env.example", ".env.example"}:
        return True
    return False


def iter_files(root: Path, include_archive: bool) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if any(should_skip_dir(parent, include_archive) for parent in path.parents if parent != root):
            continue
        if should_scan_file(path):
            yield path


def classify_severity(path: Path, kind: str, include_archive: bool) -> str:
    suffix = path.suffix.lower()
    parts = set(path.parts)

    if is_archive_path(path) and include_archive:
        return "LOW"

    if suffix in {".py", ".sh", ".command"} or path.name in {"Makefile", "Dockerfile"}:
        return "HIGH"

    if "09_runbooks" in parts or "内容工厂控制台" in parts:
        return "HIGH"

    if suffix in {".json", ".yaml", ".yml", ".toml", ".env", ".example"}:
        return "MEDIUM"

    if suffix in {".md", ".txt", ".html"}:
        return "MEDIUM"

    return "LOW"


def recommendation_for(kind: str) -> str:
    if kind in {"mac_user_path", "mac_volume_path", "windows_drive_path"}:
        return "改为环境变量、配置文件或基于仓库根目录的相对路径。"
    if kind == "file_url_path":
        return "改为可配置路径或仓库内相对链接；不要依赖本机 file:// URL。"
    return "改为可移植配置。"


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return None
    except OSError:
        return None


def scan_file(root: Path, path: Path, include_archive: bool) -> list[Finding]:
    text = read_text(path)
    if text is None:
        return []

    findings: list[Finding] = []
    rel = path.relative_to(root).as_posix()

    for line_number, line in enumerate(text.splitlines(), start=1):
        for kind, pattern, _description in PATTERNS:
            for match in pattern.finditer(line):
                matched_text = match.group(0).rstrip(".,);]")
                findings.append(
                    Finding(
                        file=rel,
                        line=line_number,
                        kind=kind,
                        severity=classify_severity(path, kind, include_archive),
                        match=matched_text,
                        context=line.strip()[:240],
                        recommendation=recommendation_for(kind),
                    )
                )

    return findings


def scan_repo(root: Path, include_archive: bool) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_files(root, include_archive=include_archive):
        findings.extend(scan_file(root, path, include_archive=include_archive))
    return sorted(findings, key=lambda item: (item.severity, item.file, item.line, item.kind))


def summarize(findings: list[Finding]) -> dict[str, int]:
    summary = {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "TOTAL": len(findings)}
    for item in findings:
        summary[item.severity] = summary.get(item.severity, 0) + 1
    return summary


def render_markdown(root: Path, findings: list[Finding], include_archive: bool) -> str:
    generated_at = datetime.now(timezone.utc).isoformat()
    summary = summarize(findings)

    lines = [
        "# P0-002 路径硬编码审计报告",
        "",
        f"- 生成时间：`{generated_at}`",
        f"- 扫描根目录：`{root}`",
        f"- 是否包含归档目录：`{include_archive}`",
        f"- 总发现数：`{summary['TOTAL']}`",
        f"- HIGH：`{summary.get('HIGH', 0)}`",
        f"- MEDIUM：`{summary.get('MEDIUM', 0)}`",
        f"- LOW：`{summary.get('LOW', 0)}`",
        "",
        "## 结论",
        "",
    ]

    if not findings:
        lines.extend([
            "未发现明显本机绝对路径硬编码。",
            "",
        ])
    else:
        high_count = summary.get("HIGH", 0)
        if high_count:
            lines.extend([
                f"发现 `{high_count}` 个 HIGH 级硬编码路径。建议优先处理脚本、Makefile、控制台入口中的路径。",
                "",
            ])
        else:
            lines.extend([
                "未发现 HIGH 级硬编码路径。MEDIUM/LOW 项可按后续重构计划逐步处理。",
                "",
            ])

    lines.extend([
        "## 处理优先级建议",
        "",
        "1. 先处理 `.py`、`.sh`、`Makefile` 中的 HIGH 项。",
        "2. 再处理 JSON/YAML/TOML 配置中的 MEDIUM 项。",
        "3. 文档、归档、历史说明中的路径只要不参与运行，可以暂时保留或降级处理。",
        "4. 所有运行路径最终应收敛到环境变量、配置文件或仓库根目录相对路径。",
        "",
    ])

    if findings:
        lines.extend([
            "## 明细",
            "",
            "| Severity | File | Line | Kind | Match | Recommendation |",
            "|---|---:|---:|---|---|---|",
        ])
        for item in findings:
            match_text = item.match.replace("|", "\\|")
            recommendation = item.recommendation.replace("|", "\\|")
            lines.append(
                f"| {item.severity} | `{item.file}` | {item.line} | `{item.kind}` | `{match_text}` | {recommendation} |"
            )

        lines.extend([
            "",
            "## 上下文摘录",
            "",
        ])
        for index, item in enumerate(findings, start=1):
            context = item.context.replace("`", "\\`")
            lines.extend([
                f"### {index}. {item.file}:{item.line}",
                "",
                f"- Severity：`{item.severity}`",
                f"- Kind：`{item.kind}`",
                f"- Match：`{item.match}`",
                f"- Context：`{context}`",
                f"- Recommendation：{item.recommendation}",
                "",
            ])

    return "\n".join(lines).rstrip() + "\n"


def write_reports(root: Path, findings: list[Finding], include_archive: bool, logs_dir: Path) -> tuple[Path, Path]:
    logs_dir.mkdir(parents=True, exist_ok=True)
    date_key = datetime.now().strftime("%Y%m%d")

    json_path = logs_dir / f"{date_key}__path-hardcode-audit.json"
    md_path = logs_dir / f"{date_key}__path-hardcode-audit.md"

    payload = {
        "schema_version": "p0-002.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "include_archive": include_archive,
        "summary": summarize(findings),
        "findings": [asdict(item) for item in findings],
    }

    json_text = json.dumps(payload, ensure_ascii=False, indent=2)
    md_text = render_markdown(root, findings, include_archive=include_archive)

    json_path.write_text(json_text + "\n", encoding="utf-8")
    md_path.write_text(md_text, encoding="utf-8")

    (logs_dir / "latest_path_hardcode_audit.json").write_text(json_text + "\n", encoding="utf-8")
    (logs_dir / "latest_path_hardcode_audit.md").write_text(md_text, encoding="utf-8")

    return md_path, json_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="扫描仓库中的硬编码绝对路径。")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="仓库根目录，默认自动识别。")
    parser.add_argument("--write", action="store_true", help="写入 Markdown/JSON 审计报告。")
    parser.add_argument("--include-archive", action="store_true", help="包含 _archive/归档/备份 等目录。")
    parser.add_argument("--fail-on-high", action="store_true", help="发现 HIGH 项时返回非 0 状态码。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()

    if not root.exists():
        print(f"❌ root not found: {root}", file=sys.stderr)
        return 2

    findings = scan_repo(root, include_archive=args.include_archive)
    summary = summarize(findings)

    print("\nP0-002 路径硬编码审计")
    print("=" * 60)
    print(f"扫描根目录：{root}")
    print(f"总发现数：{summary['TOTAL']}")
    print(f"HIGH：{summary.get('HIGH', 0)}")
    print(f"MEDIUM：{summary.get('MEDIUM', 0)}")
    print(f"LOW：{summary.get('LOW', 0)}")

    if findings:
        print("\nTop findings:")
        for item in findings[:20]:
            print(f"- [{item.severity}] {item.file}:{item.line} {item.match}")

    if args.write:
        md_path, json_path = write_reports(root, findings, include_archive=args.include_archive, logs_dir=DEFAULT_LOGS_DIR)
        print(f"\nMarkdown 报告：{md_path}")
        print(f"JSON 报告：{json_path}")

    if args.fail_on_high and summary.get("HIGH", 0) > 0:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
