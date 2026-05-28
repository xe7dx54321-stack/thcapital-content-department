"""Render versioned article previews for workbench action outputs."""

from __future__ import annotations

import html
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now
from content_system.wechat_article_preview import markdown_to_html


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class VersionedArticlePreviewResult:
    run_date: str
    version_count: int
    html_path: str
    json_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_html": paths.frontstage_root / f"{run_date}__versioned-article-preview.html",
        "latest_html": paths.frontstage_root / "latest_versioned_article_preview.html",
        "dated_json": paths.logs_root / f"{run_date}__versioned-article-preview.json",
        "latest_json": paths.logs_root / "latest_versioned_article_preview.json",
    }


def selected_article(data: dict[str, Any], article_id: str = "") -> dict[str, Any]:
    articles = list_payload(data, "articles")
    for article in articles:
        if article_id and article.get("article_id") == article_id:
            return article
    selected_id = data.get("selected_article_id")
    for article in articles:
        if article.get("article_id") == selected_id:
            return article
    return articles[0] if articles else {}


def render_html(payload: dict[str, Any], workbench_data: dict[str, Any]) -> str:
    versions = list_payload(payload, "versions")
    first_version = versions[0] if versions else {}
    original = selected_article(workbench_data, str(first_version.get("source_article_id") or ""))
    original_title = original.get("wechat_title") or original.get("title") or "原稿"
    new_title = first_version.get("new_title") or original_title
    original_body = markdown_to_html(str(original.get("wechat_body_markdown") or ""))
    new_body = markdown_to_html(str(first_version.get("new_body_markdown") or original.get("wechat_body_markdown") or ""))
    version_cards = "\n".join(
        f"""<section class="version-card">
  <h3>{html.escape(str(item.get('version_id') or 'version'))}</h3>
  <p><strong>Source action:</strong> {html.escape(str(item.get('source_action_id') or ''))}</p>
  <p><strong>Status:</strong> {html.escape(str(item.get('status') or ''))}</p>
  <p><strong>Change:</strong> {html.escape(str(item.get('change_summary') or ''))}</p>
  <p><strong>do_not_overwrite_original:</strong> true</p>
</section>"""
        for item in versions
    ) or '<section class="version-card"><h3>No generated version yet</h3><p>No approved executable action has produced a version.</p></section>'
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Versioned Article Preview</title>
  <style>
    body {{ margin: 0; background: #f6f3ee; color: #1f2933; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", system-ui, sans-serif; }}
    header {{ padding: 24px 28px; border-bottom: 1px solid #e7e2d8; background: rgba(255,255,255,.7); }}
    h1 {{ margin: 0; font-size: 24px; }}
    .meta {{ color: #6b7280; margin-top: 8px; }}
    .layout {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; padding: 20px; }}
    .paper, .version-card {{ background: #fff; border: 1px solid #e7e2d8; border-radius: 8px; box-shadow: 0 18px 48px rgba(79,70,58,.1); }}
    .paper {{ padding: 34px 38px; min-width: 0; }}
    .paper h2 {{ font-size: 14px; color: #1f7a5c; margin: 0 0 18px; }}
    .paper h1 {{ font-size: 26px; line-height: 1.4; }}
    article h1 {{ display: none; }}
    article h2 {{ margin-top: 32px; font-size: 19px; }}
    article p, article li {{ font-size: 16px; line-height: 1.9; }}
    .versions {{ padding: 0 20px 28px; display: grid; gap: 12px; }}
    .version-card {{ padding: 16px; }}
    .version-card h3 {{ margin: 0 0 10px; }}
    @media (max-width: 900px) {{ .layout {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <header>
    <h1>版本化文章预览</h1>
    <div class="meta">Run date {html.escape(str(payload.get('run_date') or ''))} · 原稿不会被覆盖</div>
  </header>
  <main class="layout">
    <section class="paper">
      <h2>原版本</h2>
      <h1>{html.escape(str(original_title))}</h1>
      <article>{original_body}</article>
    </section>
    <section class="paper">
      <h2>新版本</h2>
      <h1>{html.escape(str(new_title))}</h1>
      <article>{new_body}</article>
    </section>
  </main>
  <section class="versions">{version_cards}</section>
</body>
</html>
"""


def build_versioned_article_preview(paths: ProjectPaths, repo_root: Path) -> tuple[VersionedArticlePreviewResult, dict[str, Any]]:
    workbench_data = read_json(paths.frontstage_root / "latest_wechat_workbench_data.json")
    rewrite_payload = read_json(paths.market_content_root / "09_workbench_actions" / "versions" / "latest_rewrite_versions.json")
    evidence_payload = read_json(paths.market_content_root / "09_workbench_actions" / "versions" / "latest_evidence_expansion.json")
    topic_payload = read_json(paths.market_content_root / "09_workbench_actions" / "versions" / "latest_topic_replacements.json")
    run_date = str(workbench_data.get("run_date") or rewrite_payload.get("run_date") or today_token()).replace("-", "")[:8]
    versions = list_payload(rewrite_payload, "versions")
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "version_count": len(versions),
        "versions": versions,
        "evidence_expansion_count": len(list_payload(evidence_payload, "expansions")),
        "topic_replacement_count": len(list_payload(topic_payload, "replacements")),
        "do_not_overwrite_original": True,
    }
    outputs = output_paths(paths, run_date)
    html_text = render_html(payload, workbench_data)
    for key, path in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == ".html":
            path.write_text(html_text, encoding="utf-8")
        else:
            import json

            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return (
        VersionedArticlePreviewResult(
            run_date,
            len(versions),
            repo_relative(outputs["latest_html"], repo_root),
            repo_relative(outputs["latest_json"], repo_root),
        ),
        payload,
    )
