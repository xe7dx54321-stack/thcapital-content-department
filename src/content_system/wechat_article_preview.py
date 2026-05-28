"""Render a WeChat-like article preview as static HTML."""

from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json, repo_relative, today_token, utc_now


SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class ArticlePreviewResult:
    run_date: str
    selected_article_id: str
    title: str
    outputs: dict[str, str]


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_html": paths.frontstage_root / f"{run_date}__wechat-article-preview.html",
        "latest_html": paths.frontstage_root / "latest_wechat_article_preview.html",
    }


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noreferrer">\1</a>', escaped)
    return escaped


def markdown_to_html(markdown: str) -> str:
    blocks: list[str] = []
    list_items: list[str] = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            blocks.append("<ul>" + "".join(list_items) + "</ul>")
            list_items = []

    for raw in markdown.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            flush_list()
            continue
        if stripped.startswith("### "):
            flush_list()
            blocks.append(f"<h3>{inline_markdown(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            flush_list()
            blocks.append(f"<h2>{inline_markdown(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            flush_list()
            blocks.append(f"<h1>{inline_markdown(stripped[2:])}</h1>")
        elif stripped.startswith("> "):
            flush_list()
            blocks.append(f"<blockquote>{inline_markdown(stripped[2:])}</blockquote>")
        elif stripped.startswith("- "):
            item = inline_markdown(stripped[2:])
            klass = " evidence-line" if "http" in stripped or "证据" in stripped else ""
            list_items.append(f'<li class="{klass.strip()}">{item}</li>')
        elif re.match(r"^\d+\.\s+", stripped):
            numbered_text = re.sub(r"^\d+\.\s+", "", stripped)
            list_items.append(f"<li>{inline_markdown(numbered_text)}</li>")
        else:
            flush_list()
            klass = "risk-note" if any(token in stripped for token in ("风险", "人工", "核验", "证据不足")) else ""
            blocks.append(f'<p class="{klass}">{inline_markdown(stripped)}</p>')
    flush_list()
    return "\n".join(blocks)


def selected_article(data: dict[str, Any]) -> dict[str, Any]:
    selected_id = str(data.get("selected_article_id") or "")
    articles = data.get("articles") if isinstance(data.get("articles"), list) else []
    for article in articles:
        if isinstance(article, dict) and article.get("article_id") == selected_id:
            return article
    return articles[0] if articles and isinstance(articles[0], dict) else {}


def render_article_preview_html(data: dict[str, Any]) -> str:
    article = selected_article(data)
    title = str(article.get("wechat_title") or article.get("title") or "未选择文章")
    body_html = markdown_to_html(str(article.get("wechat_body_markdown") or ""))
    sources = article.get("source_ids") if isinstance(article.get("source_ids"), list) else []
    evidence = article.get("evidence_ids") if isinstance(article.get("evidence_ids"), list) else []
    source_rows = "\n".join(f"<li>{html.escape(str(item))}</li>" for item in sources) or "<li>暂无 source</li>"
    evidence_rows = "\n".join(f"<li>{html.escape(str(item))}</li>" for item in evidence) or "<li>暂无 evidence</li>"
    generated_at = html.escape(str(data.get("generated_at") or utc_now()))
    run_date = html.escape(str(data.get("run_date") or today_token()))
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} - WeChat Preview</title>
  <style>
    :root {{ color-scheme: light; --ink: #202124; --muted: #6b7280; --line: #e7e2d8; --accent: #1f7a5c; --wechat: #576b95; }}
    body {{ margin: 0; background: #f6f3ee; color: var(--ink); font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", system-ui, sans-serif; letter-spacing: 0; }}
    .page {{ max-width: 760px; margin: 24px auto 40px; background: #fff; min-height: calc(100vh - 64px); padding: 42px 42px 60px; box-sizing: border-box; border: 1px solid var(--line); border-radius: 8px; box-shadow: 0 20px 60px rgba(79,70,58,.12); }}
    .meta {{ color: #8a8f98; font-size: 14px; line-height: 1.8; margin: 12px 0 30px; }}
    .brand {{ color: var(--wechat); }}
    h1 {{ font-size: 28px; line-height: 1.38; font-weight: 760; margin: 0; letter-spacing: 0; }}
    article h1 {{ display: none; }}
    article h2 {{ font-size: 20px; line-height: 1.55; margin: 38px 0 15px; color: #22272e; }}
    article h2::before {{ content: ""; display: inline-block; width: 4px; height: 18px; margin: 0 10px -3px 0; border-radius: 999px; background: var(--accent); }}
    article h3 {{ font-size: 17px; margin: 28px 0 10px; color: #3f4b59; }}
    article p, article li {{ font-size: 16.5px; line-height: 1.95; color: #2f3742; }}
    article p {{ margin: 15px 0; }}
    article ul {{ padding-left: 22px; margin: 12px 0 18px; }}
    article li {{ margin: 7px 0; }}
    article code {{ background: #f2f4f7; padding: 2px 5px; border-radius: 5px; font-size: 13px; color: #4b5563; }}
    article a {{ color: var(--wechat); text-decoration: none; border-bottom: 1px solid rgba(87,107,149,.24); }}
    article blockquote, .evidence-line {{ background: #f4f8f6; border-left: 3px solid rgba(31,122,92,.42); margin: 14px 0; padding: 12px 14px; border-radius: 6px; color: #374151; }}
    .risk-note {{ background: #fff9ee; border: 1px solid #ead7b8; padding: 14px 15px; border-radius: 7px; }}
    .evidence-box {{ margin-top: 34px; border-top: 1px solid var(--line); padding-top: 22px; color: #374151; }}
    .evidence-box h2 {{ border: 0; padding: 0; font-size: 18px; color: #1f2933; }}
    .evidence-box h2::before {{ display: none; }}
    .evidence-box h3 {{ color: #6b7280; font-size: 14px; }}
    .toolbar {{ position: sticky; bottom: 14px; display: flex; justify-content: flex-end; pointer-events: none; }}
    button {{ pointer-events: auto; border: 0; background: var(--accent); color: white; padding: 10px 14px; border-radius: 7px; font-size: 14px; cursor: pointer; }}
    @media (max-width: 820px) {{
      .page {{ margin: 0; min-height: 100vh; border: 0; border-radius: 0; padding: 34px 22px 56px; }}
      h1 {{ font-size: 24px; }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <h1>{html.escape(title)}</h1>
    <div class="meta"><span class="brand">同行资本</span><br>{run_date} · 预览生成于 {generated_at}</div>
    <article id="article-body">{body_html}</article>
    <section class="evidence-box">
      <h2>发布前证据简表</h2>
      <h3>Sources</h3>
      <ul>{source_rows}</ul>
      <h3>Evidence</h3>
      <ul>{evidence_rows}</ul>
    </section>
    <div class="toolbar"><button type="button" onclick="navigator.clipboard.writeText(document.getElementById('article-body').innerText)">复制正文</button></div>
  </main>
</body>
</html>
"""


def render_wechat_article_preview(paths: ProjectPaths, repo_root: Path) -> ArticlePreviewResult:
    data_path = paths.frontstage_root / "latest_wechat_workbench_data.json"
    data = read_json(data_path)
    if not data:
        data = {"run_date": today_token(), "articles": [], "selected_article_id": "", "generated_at": utc_now()}
    run_date = str(data.get("run_date") or today_token()).replace("-", "")[:8]
    article = selected_article(data)
    html_text = render_article_preview_html(data)
    outputs = output_paths(paths, run_date)
    for path in outputs.values():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html_text, encoding="utf-8")
    return ArticlePreviewResult(
        run_date=run_date,
        selected_article_id=str(data.get("selected_article_id") or ""),
        title=str(article.get("wechat_title") or article.get("title") or ""),
        outputs={key: repo_relative(path, repo_root) for key, path in outputs.items()},
    )
