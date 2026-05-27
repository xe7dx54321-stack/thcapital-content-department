"""Build the static WeChat workbench frontend."""

from __future__ import annotations

import html
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token
from content_system.wechat_article_preview import markdown_to_html


@dataclass(frozen=True)
class WechatWorkbenchFrontendResult:
    run_date: str
    selected_article_id: str
    html_path: str
    latest_html_path: str


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_html": paths.frontstage_root / f"{run_date}__wechat-workbench.html",
        "latest_html": paths.frontstage_root / "latest_wechat_workbench.html",
    }


def selected_article(data: dict[str, Any]) -> dict[str, Any]:
    selected_id = str(data.get("selected_article_id") or "")
    for article in data.get("articles", []) if isinstance(data.get("articles"), list) else []:
        if isinstance(article, dict) and article.get("article_id") == selected_id:
            return article
    articles = data.get("articles")
    return articles[0] if isinstance(articles, list) and articles and isinstance(articles[0], dict) else {}


def render_topic_list(data: dict[str, Any]) -> str:
    rows: list[str] = []
    for topic in data.get("topics", []) if isinstance(data.get("topics"), list) else []:
        rows.append(
            f"""<button class="topic" type="button">
  <span class="topic-title">{html.escape(str(topic.get('title') or '未命名选题'))}</span>
  <span class="topic-meta">{html.escape(str(topic.get('score_band') or '-'))} · {html.escape(str(topic.get('score') or 0))} · {html.escape(str(topic.get('status') or 'recommended'))}</span>
  <span class="topic-reason">{html.escape(str(topic.get('why_it_matters') or ''))}</span>
</button>"""
        )
    return "\n".join(rows) or '<div class="empty">今日暂无推荐选题</div>'


def render_action_panel(paths: ProjectPaths) -> str:
    response = read_json(paths.market_content_root / "09_workbench_actions" / "latest_chief_editor_response.json")
    pending = read_json(paths.market_content_root / "09_workbench_actions" / "latest_pending_actions.json")
    response_text = response.get("human_readable_reply") or "暂无主编 Agent 响应。可以在下方输入需求，并复制命令到终端执行。"
    actions = list_payload(pending, "actions")
    action_lines = "".join(f"<li>{html.escape(str(item.get('action_type')))} · {html.escape(str(item.get('status')))}</li>" for item in actions[:5])
    return f"""<div class="agent-result">
  <strong>最近一次 AI 理解</strong>
  <p>{html.escape(str(response_text))}</p>
  <strong>Pending action queue</strong>
  <ul>{action_lines or '<li>暂无 pending action</li>'}</ul>
</div>"""


def render_workbench_html(data: dict[str, Any], paths: ProjectPaths) -> str:
    article = selected_article(data)
    title = str(article.get("wechat_title") or article.get("title") or "未选择文章")
    body_html = markdown_to_html(str(article.get("wechat_body_markdown") or ""))
    status = data.get("system_status") if isinstance(data.get("system_status"), dict) else {}
    topics = render_topic_list(data)
    action_panel = render_action_panel(paths)
    data_json = html.escape(json.dumps(data, ensure_ascii=False))
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>同行资本 · 微信公众号内容工作台</title>
  <style>
    :root {{ --bg: #f5f7fb; --panel: #ffffff; --ink: #18212f; --muted: #657084; --line: #dfe5ee; --green: #07c160; --blue: #2f6fed; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    header {{ height: 64px; display: flex; align-items: center; justify-content: space-between; padding: 0 22px; border-bottom: 1px solid var(--line); background: rgba(255,255,255,.92); position: sticky; top: 0; z-index: 2; }}
    header h1 {{ font-size: 18px; margin: 0; letter-spacing: 0; }}
    .status {{ display: flex; gap: 12px; color: var(--muted); font-size: 13px; flex-wrap: wrap; justify-content: flex-end; }}
    .layout {{ display: grid; grid-template-columns: 300px minmax(0, 1fr); min-height: calc(100vh - 244px); }}
    aside {{ border-right: 1px solid var(--line); background: #fbfcfe; padding: 16px; overflow: auto; }}
    aside h2, .preview-head h2 {{ font-size: 14px; color: var(--muted); text-transform: uppercase; letter-spacing: 0; margin: 0 0 12px; }}
    .topic {{ width: 100%; display: block; text-align: left; border: 1px solid var(--line); background: white; margin-bottom: 10px; padding: 12px; border-radius: 6px; cursor: default; }}
    .topic-title {{ display: block; font-size: 14px; line-height: 1.45; font-weight: 700; }}
    .topic-meta {{ display: block; margin-top: 8px; color: var(--blue); font-size: 12px; }}
    .topic-reason {{ display: block; margin-top: 7px; color: var(--muted); font-size: 12px; line-height: 1.5; }}
    main {{ padding: 22px 22px 180px; overflow: auto; }}
    .article-shell {{ max-width: 760px; margin: 0 auto; background: var(--panel); padding: 34px 28px 44px; border: 1px solid var(--line); }}
    .wechat-title {{ font-size: 27px; line-height: 1.35; margin: 0; letter-spacing: 0; }}
    .wechat-meta {{ color: var(--muted); margin: 12px 0 28px; font-size: 14px; line-height: 1.8; }}
    .wechat-brand {{ color: #576b95; }}
    article h1 {{ display: none; }}
    article h2 {{ border-left: 4px solid var(--green); padding-left: 10px; margin-top: 30px; font-size: 20px; }}
    article p, article li {{ font-size: 17px; line-height: 1.9; }}
    article p {{ margin: 15px 0; }}
    article code {{ background: #eef2f7; padding: 2px 5px; border-radius: 4px; }}
    .risk-note {{ background: #fff7ed; border: 1px solid #fed7aa; padding: 10px 12px; border-radius: 6px; }}
    .evidence-line {{ background: #f8fafc; border-left: 3px solid #cbd5e1; margin: 8px 0; padding: 8px 10px; }}
    .review-box {{ margin-top: 26px; border-top: 1px solid var(--line); padding-top: 18px; color: var(--muted); line-height: 1.7; }}
    .agent-bar {{ position: fixed; left: 0; right: 0; bottom: 0; background: #101827; color: white; padding: 14px 18px; display: grid; grid-template-columns: 1fr 380px; gap: 16px; box-shadow: 0 -8px 24px rgba(16,24,39,.18); }}
    textarea {{ width: 100%; min-height: 78px; resize: vertical; border: 1px solid #334155; background: #0f172a; color: white; padding: 12px; border-radius: 6px; font-size: 14px; }}
    .agent-actions {{ display: flex; gap: 8px; margin-top: 8px; align-items: center; }}
    button.primary {{ border: 0; background: var(--green); color: white; padding: 9px 13px; border-radius: 6px; cursor: pointer; }}
    .hint {{ color: #cbd5e1; font-size: 12px; }}
    .agent-result {{ font-size: 12px; color: #dbeafe; overflow: auto; max-height: 126px; }}
    .agent-result p {{ margin: 6px 0 10px; line-height: 1.5; }}
    .agent-result ul {{ margin: 6px 0 0; padding-left: 18px; }}
    @media (max-width: 820px) {{
      .layout {{ grid-template-columns: 1fr; }}
      aside {{ border-right: 0; border-bottom: 1px solid var(--line); }}
      .agent-bar {{ grid-template-columns: 1fr; position: static; }}
      main {{ padding-bottom: 22px; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>同行资本 · 微信公众号内容工作台</h1>
    <div class="status">
      <span>日期 {html.escape(str(data.get('run_date') or ''))}</span>
      <span>Phase8 {html.escape(str(status.get('phase8_status') or 'UNKNOWN'))}</span>
      <span>Cost {html.escape(str(status.get('cost_guard') or 'UNKNOWN'))}</span>
      <span>建议命令 <code>make phase9-daily</code></span>
    </div>
  </header>
  <div class="layout">
    <aside>
      <h2>今日推荐选题</h2>
      {topics}
    </aside>
    <main>
      <section class="article-shell">
        <div class="preview-head"><h2>公众号文章预览</h2></div>
        <h1 class="wechat-title">{html.escape(title)}</h1>
        <div class="wechat-meta"><span class="wechat-brand">同行资本</span><br>{html.escape(str(data.get('run_date') or ''))} · 本地预览</div>
        <article>{body_html}</article>
        <div class="review-box">
          <strong>Agent 审核摘要</strong><br>
          Judge: {html.escape(str(article.get('judge_decision') or '-'))}<br>
          Critic: {html.escape(str(article.get('critic_summary') or '-'))}<br>
          Revision: {html.escape(str(article.get('revision_summary') or '-'))}
        </div>
      </section>
    </main>
  </div>
  <section class="agent-bar">
    <div>
      <textarea id="chief-message" placeholder="对总控主编说：这篇文章太泛了，改成投资人视角"></textarea>
      <div class="agent-actions">
        <button class="primary" type="button" onclick="copyCommand()">生成命令</button>
        <span class="hint" id="command-hint">不会自动执行，只生成 PLAN_ONLY action plan。</span>
      </div>
    </div>
    {action_panel}
  </section>
  <script type="application/json" id="workbench-data">{data_json}</script>
  <script>
    function copyCommand() {{
      const msg = document.getElementById('chief-message').value || '请给当前稿件生成下一步主编建议';
      const command = 'python3 scripts/run_chief_editor_agent.py --message ' + JSON.stringify(msg) + ' && make workbench-action-router';
      navigator.clipboard.writeText(command);
      document.getElementById('command-hint').textContent = '已复制命令：' + command;
    }}
  </script>
</body>
</html>
"""


def build_wechat_workbench_frontend(paths: ProjectPaths, repo_root: Path) -> WechatWorkbenchFrontendResult:
    data = read_json(paths.frontstage_root / "latest_wechat_workbench_data.json")
    if not data:
        data = {"run_date": today_token(), "topics": [], "articles": [], "selected_article_id": "", "system_status": {}}
    run_date = str(data.get("run_date") or today_token()).replace("-", "")[:8]
    outputs = output_paths(paths, run_date)
    html_text = render_workbench_html(data, paths)
    for path in outputs.values():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html_text, encoding="utf-8")
    return WechatWorkbenchFrontendResult(
        run_date,
        str(data.get("selected_article_id") or ""),
        repo_relative(outputs["dated_html"], repo_root),
        repo_relative(outputs["latest_html"], repo_root),
    )
