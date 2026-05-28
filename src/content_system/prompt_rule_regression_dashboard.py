"""Build prompt and rule regression dashboard from version outcomes."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, safe_float, today_token, utc_now, write_json_and_markdown


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class PromptRuleRegressionResult:
    run_date: str
    suggestion_count: int
    output_path: str
    board_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "frontstage_dated_md": paths.frontstage_root / f"{run_date}__prompt-rule-regression-dashboard.md",
        "frontstage_latest_md": paths.frontstage_root / "latest_prompt_rule_regression_dashboard.md",
        "dated_json": paths.logs_root / f"{run_date}__prompt-rule-regression-dashboard.json",
        "latest_json": paths.logs_root / "latest_prompt_rule_regression_dashboard.json",
    }


def suggestion_id(run_date: str, target: str, text: str) -> str:
    digest = hashlib.sha1(f"{run_date}|{target}|{text}".encode("utf-8")).hexdigest()[:10]
    return f"preg_{run_date}_{digest}"


def make_suggestion(run_date: str, target_area: str, suggestion: str, reason: str, confidence: float) -> dict[str, Any]:
    return {
        "suggestion_id": suggestion_id(run_date, target_area, suggestion),
        "target_area": target_area,
        "suggestion": suggestion,
        "reason": reason,
        "confidence": confidence,
        "auto_apply": False,
    }


def build_prompt_rule_regression_dashboard(paths: ProjectPaths, repo_root: Path) -> tuple[PromptRuleRegressionResult, dict[str, Any]]:
    analytics = read_json(paths.logs_root / "latest_action_effectiveness_analytics.json")
    memory = read_json(paths.market_content_root / "09_workbench_actions" / "versions" / "article_version_memory.json")
    rule_suggestions = read_json(paths.market_content_root / "07_publishing" / "latest_rule_update_suggestions.json")
    recipes = read_json(paths.market_content_root / "08_learning_patterns" / "latest_content_recipe_suggestions.json")
    adapters = read_json(paths.market_content_root / "08_learning_patterns" / "latest_pattern_adapters.json")
    prompts = read_json(paths.repo_root / "config" / "agent_prompts.json") if hasattr(paths, "repo_root") else {}
    scoring_rules = read_json(repo_root / "config" / "value_scoring_rules.json")
    run_date = str(analytics.get("run_date") or today_token()).replace("-", "")[:8]
    summary = analytics.get("summary") if isinstance(analytics.get("summary"), dict) else {}
    avg_delta = safe_float(summary.get("average_score_delta"))
    rejected = int(summary.get("rejected_count") or 0)
    accepted = int(summary.get("accepted_count") or 0)
    suggestions: list[dict[str, Any]] = []

    if avg_delta > 3 and rejected == 0:
        suggestions.append(
            make_suggestion(
                run_date,
                "chief_editor_prompt",
                "Keep the current Chief Editor routing style; recent version outcomes are positive.",
                f"Average score delta is {avg_delta} with no rejected versions.",
                0.68,
            )
        )
    elif rejected > accepted:
        suggestions.append(
            make_suggestion(
                run_date,
                "rewrite_agent_prompt",
                "Tighten rewrite prompt constraints before expanding automation.",
                f"Rejected versions ({rejected}) exceed accepted versions ({accepted}).",
                0.72,
            )
        )
    else:
        suggestions.append(
            make_suggestion(
                run_date,
                "scoring_rule",
                "Do not auto-change scoring or prompt rules yet; continue collecting version review decisions.",
                "Current evidence is too small for confident rule changes.",
                0.6,
            )
        )

    for item in list_payload(analytics, "problem_patterns")[:3]:
        suggestions.append(
            make_suggestion(
                run_date,
                "rewrite_agent_prompt",
                f"Review action pattern `{item.get('pattern')}` before reuse.",
                str(item.get("reason") or "Problem pattern detected in action effectiveness analytics."),
                0.66,
            )
        )
    if list_payload(rule_suggestions, "suggestions"):
        suggestions.append(
            make_suggestion(
                run_date,
                "scoring_rule",
                "Cross-check existing rule update suggestions against accepted/rejected article versions.",
                "Rule suggestions exist, but Phase 11 policy requires human review before applying them.",
                0.63,
            )
        )
    if list_payload(recipes, "suggestions") or list_payload(adapters, "adapters"):
        suggestions.append(
            make_suggestion(
                run_date,
                "content_recipe",
                "Use accepted version patterns to validate content recipes and pattern adapters.",
                "Content recipe and pattern adapter artifacts are available for comparison.",
                0.58,
            )
        )

    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "summary": {
            "version_count": (memory.get("summary") or {}).get("version_count", 0) if isinstance(memory.get("summary"), dict) else 0,
            "accepted_count": accepted,
            "rejected_count": rejected,
            "average_score_delta": avg_delta,
            "prompt_count": len(list_payload(prompts, "prompts")),
            "scoring_rule_loaded": bool(scoring_rules),
            "overall_direction": "improving" if avg_delta > 0 else "flat_or_unknown" if avg_delta == 0 else "regressing",
        },
        "suggestions": suggestions,
        "policy": {
            "auto_apply": False,
            "notes": "Dashboard only suggests prompt/rule changes. It never edits config, prompts, or scoring rules.",
        },
    }
    outputs = output_paths(paths, run_date)
    write_json_and_markdown(payload, render_markdown(payload), outputs)
    return (
        PromptRuleRegressionResult(
            run_date,
            len(suggestions),
            repo_relative(outputs["latest_json"], repo_root),
            repo_relative(outputs["frontstage_latest_md"], repo_root),
        ),
        payload,
    )


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    rows = "\n".join(
        f"| `{item.get('target_area')}` | {item.get('suggestion')} | {item.get('reason')} | `{item.get('confidence')}` | `{item.get('auto_apply')}` |"
        for item in list_payload(payload, "suggestions")
    ) or "| - | No suggestions | - | 0 | false |"
    return f"""# Prompt / Rule Regression Dashboard

## Summary

- Run date: `{payload.get('run_date')}`
- Overall direction: `{summary.get('overall_direction')}`
- Versions: `{summary.get('version_count', 0)}`
- Accepted: `{summary.get('accepted_count', 0)}`
- Rejected: `{summary.get('rejected_count', 0)}`
- Average score delta: `{summary.get('average_score_delta', 0)}`
- Policy: prompt/rule changes are suggestions only and `auto_apply=false`.

## Suggestions

| Target Area | Suggestion | Reason | Confidence | Auto Apply |
|---|---|---|---:|---|
{rows}
"""
