"""Run lightweight methodology regression tests."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_json": paths.logs_root / f"{run_date}__methodology-regression-tests.json",
        "dated_md": paths.logs_root / f"{run_date}__methodology-regression-tests.md",
        "latest_json": paths.logs_root / "latest_methodology_regression_tests.json",
        "latest_md": paths.logs_root / "latest_methodology_regression_tests.md",
    }


def load_tests(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "config" / "methodology_regression_tests.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    case_type = str(case.get("case_type") or "")
    text = f"{case.get('title') or ''} {case.get('text') or ''}"
    passed = True
    reasons: list[str] = []
    if case_type.startswith("good_topic"):
        passed = bool(re.search(r"Agent|AI|入口|产业|开发者|企业", text)) and bool(re.search(r"变化|重估|影响|重新", text))
        reasons.append("good topic should contain relevant AI/Agent signal and change language.")
    elif case_type.startswith("bad_topic"):
        passed = bool(re.search(r"PR|营销|没有|持续赋能|值得关注|未来可期", text))
        reasons.append("bad topic should trigger weak-signal language.")
    elif "strong_title" in case_type:
        passed = bool(re.search(r"不是|而是|为什么|真正|争夺|重估", text))
        reasons.append("strong title should contain judgment tension.")
    elif "weak_title" in case_type:
        passed = bool(re.search(r"未来可期|值得关注|持续赋能", text))
        reasons.append("weak title should contain generic language.")
    elif "strong_opening" in case_type:
        passed = bool(re.search(r"市场以为|真正|不是|但", text))
        reasons.append("strong opening should establish expectation gap.")
    elif "weak_opening" in case_type:
        passed = bool(re.search(r"近年来|快速发展|不断涌现", text))
        reasons.append("weak opening should be generic background.")
    elif "visual_good" in case_type:
        passed = bool(re.search(r"封面|价值链|框架", text))
        reasons.append("good visual plan should use information-bearing visuals.")
    elif "visual_bad" in case_type:
        passed = bool(re.search(r"科幻|机器人|没有信息|蓝色", text))
        reasons.append("bad visual plan should detect decorative visual pattern.")
    elif "weak_logic" in case_type:
        passed = text.count("。") >= 3 and not re.search(r"先看|再看|最后", text)
        reasons.append("weak logic should be list-like and non-progressive.")
    elif "strong_logic" in case_type:
        passed = bool(re.search(r"先看|再看|最后", text))
        reasons.append("strong logic should show progression.")
    elif "without_judgment" in case_type or "without_evidence" in case_type:
        passed = True
        reasons.append("case included as calibration anchor.")
    return {
        "case_id": case.get("case_id"),
        "case_type": case_type,
        "expected": case.get("expected"),
        "result": "PASS" if passed else "FAIL",
        "reasons": reasons,
    }


def run_methodology_regression_tests(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    test_payload = load_tests(repo_root)
    run_date = today_token()
    cases = [case for case in test_payload.get("cases", []) if isinstance(case, dict)]
    results = [evaluate_case(case) for case in cases]
    summary = {
        "case_count": len(results),
        "pass_count": sum(1 for item in results if item.get("result") == "PASS"),
        "fail_count": sum(1 for item in results if item.get("result") == "FAIL"),
    }
    payload = {"schema_version": SCHEMA_VERSION, "generated_at": utc_now(), "run_date": run_date, "results": results, "summary": summary, "warnings": [] if results else ["No regression tests configured."]}
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return payload, outputs


def render_markdown(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{item.get('case_id')}` | `{item.get('case_type')}` | `{item.get('result')}` | {'; '.join(item.get('reasons') or [])} |"
        for item in list_payload(payload, "results")
    ) or "| - | - | - | No cases |"
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return f"""# Methodology Regression Tests

## Summary

- case_count: `{summary.get('case_count', 0)}`
- pass_count: `{summary.get('pass_count', 0)}`
- fail_count: `{summary.get('fail_count', 0)}`

| Case | Type | Result | Reason |
|---|---|---|---|
{rows}
"""
