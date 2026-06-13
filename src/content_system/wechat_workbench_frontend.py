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
    articles = data.get("articles") if isinstance(data.get("articles"), list) else []
    for article in articles:
        if isinstance(article, dict) and article.get("article_id") == selected_id:
            return article
    return articles[0] if articles and isinstance(articles[0], dict) else {}


def latest_action_payloads(paths: ProjectPaths) -> tuple[dict[str, Any], dict[str, Any]]:
    action_root = paths.market_content_root / "09_workbench_actions"
    response = read_json(action_root / "latest_chief_editor_response.json")
    pending = read_json(action_root / "latest_pending_actions.json")
    return response, pending


def safe_json_for_script(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")


def render_styles() -> str:
    return """
:root {
  color-scheme: light;
  --bg: #f6f3ee;
  --surface: #ffffff;
  --surface-soft: #faf8f4;
  --surface-muted: #f1eee8;
  --text-main: #1f2933;
  --text-soft: #3f4b59;
  --text-muted: #6b7280;
  --border: #e7e2d8;
  --border-strong: #d8d0c2;
  --accent: #1f7a5c;
  --accent-ink: #165640;
  --accent-soft: #e7f3ee;
  --gold: #a97824;
  --gold-soft: #f6eddd;
  --danger: #9a3412;
  --danger-soft: #fff4e8;
  --wechat: #576b95;
  --shadow: 0 20px 60px rgba(79, 70, 58, 0.12);
}
* { box-sizing: border-box; }
html { min-height: 100%; }
body {
  min-height: 100%;
  margin: 0;
  background:
    linear-gradient(180deg, rgba(255,255,255,.56), rgba(255,255,255,0) 320px),
    var(--bg);
  color: var(--text-main);
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", system-ui, sans-serif;
  letter-spacing: 0;
}
button, textarea { font: inherit; letter-spacing: 0; }
button { cursor: pointer; }
.app-shell {
  min-height: 100vh;
  padding-bottom: 236px;
}
.topbar {
  position: sticky;
  top: 0;
  z-index: 20;
  min-height: 68px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 14px 24px;
  border-bottom: 1px solid rgba(231, 226, 216, .86);
  background: rgba(250, 248, 244, .92);
  backdrop-filter: blur(18px);
}
.brand-block { display: flex; flex-direction: column; gap: 4px; min-width: 260px; }
.eyebrow {
  color: var(--accent);
  font-size: 12px;
  font-weight: 700;
}
.topbar h1 {
  margin: 0;
  font-size: 19px;
  line-height: 1.35;
  font-weight: 750;
}
.status-strip {
  display: flex;
  justify-content: flex-end;
  flex-wrap: wrap;
  gap: 8px;
}
.status-pill {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 5px 10px;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: rgba(255,255,255,.72);
  color: var(--text-muted);
  font-size: 12px;
  white-space: nowrap;
}
.status-pill strong { color: var(--text-main); font-weight: 650; margin-left: 4px; }
.workspace {
  display: grid;
  grid-template-columns: 320px minmax(500px, 1fr) 316px;
  gap: 18px;
  padding: 18px;
  align-items: start;
}
.topic-rail,
.insight-panel {
  position: sticky;
  top: 86px;
  max-height: calc(100vh - 330px);
  overflow: auto;
}
.rail-head,
.panel-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin: 0 0 12px;
}
.rail-head h2,
.panel-head h2 {
  margin: 0;
  font-size: 15px;
  font-weight: 760;
}
.muted { color: var(--text-muted); }
.count-note { color: var(--text-muted); font-size: 12px; }
.topic-card {
  width: 100%;
  display: block;
  text-align: left;
  margin: 0 0 10px;
  padding: 13px 13px 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: rgba(255,255,255,.74);
  box-shadow: 0 5px 18px rgba(79, 70, 58, 0.04);
  transition: background .16s ease, border-color .16s ease, transform .16s ease, box-shadow .16s ease;
}
.topic-card:hover {
  transform: translateY(-1px);
  border-color: var(--border-strong);
  background: var(--surface);
  box-shadow: 0 14px 26px rgba(79, 70, 58, 0.08);
}
.topic-card.is-selected {
  border-color: rgba(31, 122, 92, .42);
  background: linear-gradient(180deg, #ffffff, var(--accent-soft));
  box-shadow: 0 16px 34px rgba(31, 122, 92, 0.12);
}
.topic-title {
  display: block;
  color: var(--text-main);
  font-size: 14px;
  font-weight: 720;
  line-height: 1.48;
}
.topic-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
  margin: 9px 0 7px;
}
.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 22px;
  padding: 3px 7px;
  border-radius: 999px;
  background: var(--surface-muted);
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 680;
  white-space: nowrap;
}
.badge.ready { background: var(--accent-soft); color: var(--accent-ink); }
.badge.needs_revision { background: var(--gold-soft); color: var(--gold); }
.badge.hold { background: var(--danger-soft); color: var(--danger); }
.topic-reason {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  color: var(--text-muted);
  font-size: 12px;
  line-height: 1.55;
}
.reader-wrap {
  min-width: 0;
}
.reader-toolbar {
  max-width: 760px;
  margin: 0 auto 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}
.mode-tabs {
  display: inline-flex;
  padding: 3px;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: rgba(255,255,255,.74);
}
.mode-tab {
  border: 0;
  border-radius: 999px;
  background: transparent;
  color: var(--text-muted);
  min-height: 30px;
  padding: 5px 13px;
  font-size: 13px;
}
.mode-tab.is-active {
  background: var(--text-main);
  color: #fff;
}
.selected-note {
  color: var(--text-muted);
  font-size: 12px;
  text-align: right;
  line-height: 1.5;
}
.article-shell {
  max-width: 760px;
  margin: 0 auto;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--surface);
  box-shadow: var(--shadow);
  overflow: hidden;
}
.article-paper {
  padding: 40px 42px 50px;
}
.wechat-title {
  margin: 0;
  color: #202124;
  font-size: 28px;
  line-height: 1.38;
  font-weight: 760;
}
.wechat-meta {
  margin: 13px 0 30px;
  color: #8a8f98;
  font-size: 14px;
  line-height: 1.8;
}
.wechat-brand { color: var(--wechat); }
.article-body h1 { display: none; }
.article-body h2 {
  margin: 38px 0 15px;
  color: #22272e;
  font-size: 20px;
  line-height: 1.55;
  font-weight: 760;
}
.article-body h2::before {
  content: "";
  display: inline-block;
  width: 4px;
  height: 18px;
  margin: 0 10px -3px 0;
  border-radius: 999px;
  background: var(--accent);
}
.article-body h3 {
  margin: 28px 0 10px;
  font-size: 17px;
  line-height: 1.65;
  color: var(--text-soft);
}
.article-body p,
.article-body li {
  color: #2f3742;
  font-size: 16.5px;
  line-height: 1.95;
}
.article-body p { margin: 15px 0; }
.article-body ul { margin: 12px 0 20px; padding-left: 22px; }
.article-body li { margin: 7px 0; }
.article-body a {
  color: var(--wechat);
  text-decoration: none;
  border-bottom: 1px solid rgba(87, 107, 149, .24);
}
.article-body code {
  color: #4b5563;
  background: #f2f4f7;
  border-radius: 5px;
  padding: 2px 5px;
  font-size: 13px;
}
.article-body blockquote,
.article-body .evidence-line {
  margin: 14px 0;
  padding: 12px 14px;
  border-left: 3px solid rgba(31, 122, 92, .42);
  border-radius: 6px;
  background: #f4f8f6;
  color: #374151;
}
.article-body .risk-note {
  margin: 18px 0;
  padding: 14px 15px;
  border: 1px solid #ead7b8;
  border-radius: 7px;
  background: #fff9ee;
}
.article-footer {
  margin-top: 34px;
  padding-top: 22px;
  border-top: 1px solid var(--border);
  color: var(--text-muted);
  font-size: 13px;
  line-height: 1.7;
}
.review-mode {
  padding: 30px;
  background: linear-gradient(180deg, #fff, #fbfaf7);
}
.review-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}
.review-section {
  border: 1px solid var(--border);
  border-radius: 8px;
  background: rgba(255,255,255,.64);
  margin-bottom: 14px;
  overflow: hidden;
}
.review-section summary {
  cursor: pointer;
  padding: 14px 16px;
  color: var(--text-main);
  font-weight: 700;
}
.review-section .review-grid {
  padding: 0 14px 14px;
}
.review-section-note {
  display: block;
  margin-top: 3px;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 400;
}
.review-card,
.insight-card {
  border: 1px solid var(--border);
  border-radius: 8px;
  background: rgba(255,255,255,.78);
  padding: 13px;
}
.review-card.wide { grid-column: 1 / -1; }
.review-label,
.insight-label {
  margin: 0 0 7px;
  color: var(--text-muted);
  font-size: 12px;
}
.review-value,
.insight-value {
  margin: 0;
  color: var(--text-main);
  font-size: 14px;
  line-height: 1.65;
}
.mini-list {
  margin: 0;
  padding-left: 18px;
  color: var(--text-soft);
  font-size: 13px;
  line-height: 1.65;
  word-break: break-word;
}
.version-panel {
  border-color: rgba(31, 122, 92, .28);
  background: linear-gradient(180deg, #fff, #f5fbf8);
}
.final-panel {
  border-color: rgba(169, 120, 36, .32);
  background: linear-gradient(180deg, #fff, #fff8ed);
}
.performance-panel {
  border-color: rgba(87, 107, 149, .3);
  background: linear-gradient(180deg, #fff, #f4f6fb);
}
.methodology-panel {
  border-color: rgba(31, 122, 92, .26);
  background: linear-gradient(180deg, #fff, #f6fbf8);
}
.generation-panel {
  border-color: rgba(169, 120, 36, .28);
  background: linear-gradient(180deg, #fff, #fffaf1);
}
.live-panel {
  border-color: rgba(78, 100, 160, .25);
  background: linear-gradient(180deg, #fff, #f7f8ff);
}
.image-asset-panel {
  border-color: rgba(31, 122, 92, .28);
  background: linear-gradient(180deg, #fff, #f5fbf8);
}
.publishing-pack-panel {
  border-color: rgba(169, 120, 36, .34);
  background: linear-gradient(180deg, #fff, #fff7e9);
}
.content-ops-panel {
  border-color: rgba(87, 107, 149, .32);
  background: linear-gradient(180deg, #fff, #f5f7fb);
}
.delta-number {
  display: inline-flex;
  align-items: center;
  min-height: 30px;
  padding: 3px 9px;
  border-radius: 999px;
  background: var(--accent-soft);
  color: var(--accent-ink);
  font-weight: 780;
}
.version-actions {
  display: grid;
  gap: 7px;
  margin-top: 10px;
}
.copy-review-command {
  min-height: 30px;
  padding: 6px 9px;
  border: 1px solid var(--border);
  border-radius: 7px;
  background: #fff;
  color: var(--text-soft);
  font-size: 12px;
  text-align: left;
}
.copy-review-command:hover {
  border-color: rgba(31, 122, 92, .35);
  color: var(--accent-ink);
  background: var(--accent-soft);
}
.copy-final-content {
  min-height: 30px;
  padding: 6px 9px;
  border: 1px solid #ead7b8;
  border-radius: 7px;
  background: #fff;
  color: var(--gold);
  font-size: 12px;
  text-align: left;
}
.copy-final-content:hover {
  background: var(--gold-soft);
}
.copy-performance-command {
  min-height: 30px;
  padding: 6px 9px;
  border: 1px solid rgba(87, 107, 149, .24);
  border-radius: 7px;
  background: #fff;
  color: var(--wechat);
  font-size: 12px;
  text-align: left;
}
.copy-performance-command:hover {
  background: #eef2fa;
}
.copy-image-request {
  min-height: 30px;
  padding: 6px 9px;
  border: 1px solid #ead7b8;
  border-radius: 7px;
  background: #fff;
  color: var(--gold);
  font-size: 12px;
  text-align: left;
}
.copy-image-request:hover { background: var(--gold-soft); }
.copy-image-asset {
  min-height: 30px;
  padding: 6px 9px;
  border: 1px solid rgba(31, 122, 92, .24);
  border-radius: 7px;
  background: #fff;
  color: var(--accent-ink);
  font-size: 12px;
  text-align: left;
}
.copy-image-asset:hover { background: var(--accent-soft); }
.copy-publishing-pack {
  min-height: 30px;
  padding: 6px 9px;
  border: 1px solid #ead7b8;
  border-radius: 7px;
  background: #fff;
  color: var(--gold);
  font-size: 12px;
  text-align: left;
}
.copy-publishing-pack:hover { background: var(--gold-soft); }
.methodology-score-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
  margin: 10px 0;
}
.methodology-score-item {
  min-height: 46px;
  padding: 8px;
  border: 1px solid rgba(31, 122, 92, .16);
  border-radius: 7px;
  background: rgba(255,255,255,.72);
}
.methodology-score-item span {
  display: block;
  color: var(--text-muted);
  font-size: 11px;
}
.methodology-score-item strong {
  display: block;
  margin-top: 3px;
  color: var(--accent-ink);
  font-size: 15px;
}
.insight-panel {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.insight-card {
  background: rgba(255,255,255,.68);
  box-shadow: 0 5px 18px rgba(79, 70, 58, 0.035);
}
.readiness {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}
.score-number {
  color: var(--accent-ink);
  font-size: 24px;
  font-weight: 780;
}
.empty-state {
  padding: 44px 32px;
  color: var(--text-muted);
  text-align: center;
}
.chief-bar {
  position: fixed;
  left: 16px;
  right: 16px;
  bottom: 14px;
  z-index: 30;
  display: grid;
  grid-template-columns: minmax(420px, 1fr) 400px;
  gap: 16px;
  padding: 15px;
  border: 1px solid rgba(216, 208, 194, .92);
  border-radius: 10px;
  background: rgba(255,255,255,.94);
  box-shadow: 0 -14px 50px rgba(79, 70, 58, 0.16);
  backdrop-filter: blur(18px);
}
.chief-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
}
.chief-title h2 {
  margin: 0;
  font-size: 15px;
  font-weight: 760;
}
.target-chip {
  color: var(--text-muted);
  font-size: 12px;
  max-width: 48%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin: 0 0 9px;
}
.quick-action {
  min-height: 28px;
  padding: 5px 9px;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: var(--surface-soft);
  color: var(--text-soft);
  font-size: 12px;
}
.quick-action:hover {
  border-color: rgba(31, 122, 92, .35);
  color: var(--accent-ink);
  background: var(--accent-soft);
}
#chief-message {
  width: 100%;
  min-height: 82px;
  resize: vertical;
  padding: 12px 13px;
  border: 1px solid var(--border-strong);
  border-radius: 8px;
  outline: none;
  background: #fff;
  color: var(--text-main);
  font-size: 14px;
  line-height: 1.6;
}
#chief-message:focus {
  border-color: rgba(31, 122, 92, .55);
  box-shadow: 0 0 0 3px rgba(31, 122, 92, .11);
}
.command-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 9px;
}
.primary-btn,
.secondary-btn {
  min-height: 34px;
  padding: 7px 12px;
  border-radius: 7px;
  font-size: 13px;
}
.primary-btn {
  border: 1px solid var(--accent);
  background: var(--accent);
  color: #fff;
}
.secondary-btn {
  border: 1px solid var(--border);
  background: #fff;
  color: var(--text-soft);
}
.command-preview {
  flex: 1;
  color: var(--text-muted);
  font-size: 12px;
  line-height: 1.45;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.agent-memory {
  min-width: 0;
  border-left: 1px solid var(--border);
  padding-left: 16px;
  overflow: auto;
  max-height: 190px;
}
.agent-memory h3 {
  margin: 0 0 8px;
  font-size: 13px;
  color: var(--text-main);
}
.agent-memory p,
.agent-memory li {
  color: var(--text-muted);
  font-size: 12.5px;
  line-height: 1.55;
}
.agent-memory p { margin: 0 0 10px; }
.agent-memory ul { margin: 6px 0 0; padding-left: 18px; }
.code-line {
  display: block;
  margin-top: 7px;
  padding: 8px;
  border-radius: 7px;
  background: var(--surface-soft);
  color: var(--text-soft);
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 11px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
@media (max-width: 1180px) {
  .workspace { grid-template-columns: 300px minmax(0, 1fr); }
  .insight-panel {
    position: static;
    max-height: none;
    grid-column: 1 / -1;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
@media (max-width: 860px) {
  .app-shell { padding-bottom: 0; }
  .topbar { position: static; align-items: flex-start; flex-direction: column; }
  .status-strip { justify-content: flex-start; }
  .workspace { grid-template-columns: 1fr; padding: 12px; }
  .topic-rail, .insight-panel { position: static; max-height: none; }
  .insight-panel { display: flex; }
  .reader-toolbar { flex-direction: column; align-items: stretch; }
  .selected-note { text-align: left; }
  .article-paper { padding: 30px 22px 40px; }
  .wechat-title { font-size: 24px; }
  .review-grid { grid-template-columns: 1fr; }
  .chief-bar {
    position: static;
    grid-template-columns: 1fr;
    margin: 0 12px 14px;
  }
  .agent-memory { border-left: 0; border-top: 1px solid var(--border); padding-left: 0; padding-top: 12px; }
}
"""


def render_scripts() -> str:
    return r"""
const workbenchData = JSON.parse(document.getElementById("workbench-data").textContent || "{}");
const chiefResponse = JSON.parse(document.getElementById("chief-response-data").textContent || "{}");
const pendingPayload = JSON.parse(document.getElementById("pending-actions-data").textContent || "{}");
const articles = Array.isArray(workbenchData.articles) ? workbenchData.articles : [];
const topics = Array.isArray(workbenchData.topics) ? workbenchData.topics : [];
let selectedArticleId = workbenchData.selected_article_id || (articles[0] && articles[0].article_id) || "";
let readerMode = "read";
let currentCommand = "";

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function inlineMarkdown(text) {
  let escaped = escapeHtml(text);
  escaped = escaped.replace(/`([^`]+)`/g, "<code>$1</code>");
  escaped = escaped.replace(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>');
  return escaped;
}

function markdownToHtml(markdown) {
  const blocks = [];
  let listItems = [];
  const flushList = () => {
    if (listItems.length) {
      blocks.push("<ul>" + listItems.join("") + "</ul>");
      listItems = [];
    }
  };
  String(markdown || "").split(/\r?\n/).forEach((raw) => {
    const stripped = raw.trim();
    if (!stripped) {
      flushList();
      return;
    }
    if (stripped.startsWith("### ")) {
      flushList();
      blocks.push(`<h3>${inlineMarkdown(stripped.slice(4))}</h3>`);
    } else if (stripped.startsWith("## ")) {
      flushList();
      blocks.push(`<h2>${inlineMarkdown(stripped.slice(3))}</h2>`);
    } else if (stripped.startsWith("# ")) {
      flushList();
      blocks.push(`<h1>${inlineMarkdown(stripped.slice(2))}</h1>`);
    } else if (stripped.startsWith("> ")) {
      flushList();
      blocks.push(`<blockquote>${inlineMarkdown(stripped.slice(2))}</blockquote>`);
    } else if (stripped.startsWith("- ")) {
      const klass = /http|证据|source|evidence/i.test(stripped) ? " class=\"evidence-line\"" : "";
      listItems.push(`<li${klass}>${inlineMarkdown(stripped.slice(2))}</li>`);
    } else if (/^\d+\.\s+/.test(stripped)) {
      listItems.push(`<li>${inlineMarkdown(stripped.replace(/^\d+\.\s+/, ""))}</li>`);
    } else {
      flushList();
      const klass = /(风险|人工|核验|证据不足|发布前)/.test(stripped) ? " class=\"risk-note\"" : "";
      blocks.push(`<p${klass}>${inlineMarkdown(stripped)}</p>`);
    }
  });
  flushList();
  return blocks.join("\n");
}

function getSelectedArticle() {
  return articles.find((item) => item.article_id === selectedArticleId) || articles[0] || {};
}

function statusLabel(status) {
  const labels = {
    ready: "Ready",
    needs_revision: "Needs Revision",
    hold: "Hold",
    recommended: "Recommended"
  };
  return labels[status] || status || "Recommended";
}

function statusClass(status) {
  if (status === "ready") return "ready";
  if (status === "needs_revision") return "needs_revision";
  if (status === "hold") return "hold";
  return "";
}

function shortText(value, fallback = "暂无") {
  const text = String(value || "").trim();
  return text || fallback;
}

function renderTopbar() {
  const summary = workbenchData.summary || {};
  const status = workbenchData.system_status || {};
  document.getElementById("run-date").textContent = workbenchData.run_date || "-";
  document.getElementById("ready-count").textContent = summary.ready_count ?? 0;
  document.getElementById("cost-status").textContent = status.cost_guard || "UNKNOWN";
  document.getElementById("live-mode").textContent = status.live_mode || "dry_run";
}

function renderTopicRail() {
  const rail = document.getElementById("topic-list");
  const count = document.getElementById("topic-count");
  count.textContent = `${articles.length || topics.length || 0} 条`;
  if (!articles.length && !topics.length) {
    rail.innerHTML = '<div class="empty-state">今日暂无可预览选题。请先运行 make phase9-daily。</div>';
    return;
  }
  const rows = articles.length ? articles : topics.map((topic, index) => ({
    article_id: topic.topic_id || `topic_${index + 1}`,
    title: topic.title,
    wechat_title: topic.title,
    status: topic.status,
    score_band: topic.score_band,
    topic_score: topic.score,
    why_it_matters: topic.why_it_matters,
    evidence_count: topic.evidence_count,
    source_count: topic.source_count
  }));
  rail.innerHTML = rows.map((item) => {
    const selected = item.article_id === selectedArticleId ? " is-selected" : "";
    const reason = item.why_it_matters || item.proponent_summary || item.next_step || "等待主编判断。";
    return `<button class="topic-card${selected}" type="button" data-article-id="${escapeHtml(item.article_id)}">
      <span class="topic-title">${escapeHtml(item.wechat_title || item.title || "未命名选题")}</span>
      <span class="topic-meta">
        <span class="badge ${statusClass(item.status)}">${escapeHtml(statusLabel(item.status))}</span>
        <span class="badge">${escapeHtml(item.score_band || "-")} · ${escapeHtml(item.topic_score || item.quality_score || 0)}</span>
        <span class="badge">${escapeHtml(item.evidence_count ?? (item.evidence_ids || []).length ?? 0)} evidence</span>
      </span>
      <span class="topic-reason">${escapeHtml(reason)}</span>
    </button>`;
  }).join("");
  rail.querySelectorAll(".topic-card").forEach((button) => {
    button.addEventListener("click", () => {
      selectedArticleId = button.dataset.articleId || selectedArticleId;
      renderAll();
    });
  });
}

function renderReader() {
  const article = getSelectedArticle();
  const title = article.wechat_title || article.title || "未选择文章";
  const selectedNote = document.getElementById("selected-note");
  selectedNote.textContent = `${article.article_id || "-"} · ${title}`;
  document.querySelectorAll(".mode-tab").forEach((tab) => {
    tab.classList.toggle("is-active", tab.dataset.mode === readerMode);
  });
  const shell = document.getElementById("article-shell");
  if (!article.article_id) {
    shell.innerHTML = '<div class="empty-state">暂无文章预览。请先运行内容生产 pipeline。</div>';
    return;
  }
  if (readerMode === "review") {
    const opsSection = renderReviewSection("今日运营", "先看今天能不能发、卡在哪里、下一步人工动作是什么。", `
        ${renderStableWorkbenchBaseline("review-card wide")}
        ${renderHotMaterialPanel("review-card wide")}
        ${renderConnectorHealthPanel("review-card wide")}
        ${renderEvidenceTopicPromotionPanel("review-card wide")}
        ${renderOpenClawMigrationPanel("review-card wide")}
        ${renderOpenClawActivationPanel("review-card wide")}
        ${renderRuntimeControlCenterPanel("review-card wide")}
        ${renderAcquisitionPlaybookPanel("review-card wide")}
        ${renderAutonomousContentProductionPanel("review-card wide")}
        ${renderReplayTrialPanel("review-card wide")}
        ${renderContentOpsPanel("review-card wide")}
        ${renderContentHardeningPanel("review-card wide", "ops")}
      `, true);
    const articleSection = renderReviewSection("文章审稿", "文章质量、方法论、版本、rewrite 与最终候选稿。", `
        <div class="review-card"><p class="review-label">质量分</p><p class="review-value">${escapeHtml(article.quality_score || 0)}</p></div>
        <div class="review-card"><p class="review-label">状态</p><p class="review-value"><span class="badge ${statusClass(article.status)}">${escapeHtml(statusLabel(article.status))}</span></p></div>
        <div class="review-card"><p class="review-label">Judge 决策</p><p class="review-value">${escapeHtml(shortText(article.judge_decision))}</p></div>
        <div class="review-card"><p class="review-label">发布候选</p><p class="review-value">${escapeHtml(shortText(article.publishing_candidate_id, "尚未进入发布候选"))}</p></div>
        <div class="review-card wide"><p class="review-label">Critic 摘要</p><p class="review-value">${escapeHtml(shortText(article.critic_summary))}</p></div>
        <div class="review-card wide"><p class="review-label">Revision 建议</p><p class="review-value">${escapeHtml(shortText(article.revision_summary))}</p></div>
        ${renderMethodologyPanel("review-card wide")}
        ${renderVersionReviewCard("review-card wide")}
        ${renderFinalReviewCard("review-card wide")}
        <div class="review-card wide"><p class="review-label">Evidence</p>${renderMiniList(article.evidence_ids, "暂无 evidence")}</div>
        <div class="review-card wide"><p class="review-label">Source</p>${renderMiniList(article.source_ids, "暂无 source")}</div>
      `, true);
    const visualSection = renderReviewSection("图文发布准备", "copy pack、图片槽位、图片资产和视觉 checklist。", `
        ${renderGenerationVisualPanel("review-card wide")}
        ${renderImageAssetPanel("review-card wide")}
        ${renderPublishingPackPanel("review-card wide")}
      `, false);
    const performanceSection = renderReviewSection("发布后复盘", "人工发布 session、metrics、视觉表现和学习反馈。", `
        ${renderPerformancePanel("review-card wide")}
      `, false);
    const systemSection = renderReviewSection("系统运维", "失败处理、trial retrospective、fix pack、operator runbook 和 Phase0-19 closeout。", `
        ${renderStableWorkbenchBaseline("review-card wide")}
        ${renderHotMaterialPanel("review-card wide")}
        ${renderConnectorHealthPanel("review-card wide")}
        ${renderEvidenceTopicPromotionPanel("review-card wide")}
        ${renderOpenClawMigrationPanel("review-card wide")}
        ${renderOpenClawActivationPanel("review-card wide")}
        ${renderRuntimeControlCenterPanel("review-card wide")}
        ${renderAcquisitionPlaybookPanel("review-card wide")}
        ${renderAutonomousContentProductionPanel("review-card wide")}
        ${renderReplayTrialPanel("review-card wide")}
        ${renderStableTrialPanel("review-card wide")}
        ${renderStableOpsPanel("review-card wide")}
        ${renderPhase22Panel("review-card wide")}
        ${renderTrialPanel("review-card wide")}
        ${renderContentHardeningPanel("review-card wide", "system")}
        ${renderLivePilotPanel("review-card wide")}
      `, false);
    shell.innerHTML = `<section class="review-mode">
      <h1 class="wechat-title">${escapeHtml(title)}</h1>
      ${opsSection}
      ${articleSection}
      ${visualSection}
      ${performanceSection}
      ${systemSection}
    </section>`;
    return;
  }
  shell.innerHTML = `<section class="article-paper">
    <h1 class="wechat-title">${escapeHtml(title)}</h1>
    <div class="wechat-meta"><span class="wechat-brand">同行资本</span><br>${escapeHtml(workbenchData.run_date || "")} · 本地公众号预览</div>
    <article class="article-body" id="article-body">${markdownToHtml(article.wechat_body_markdown || "")}</article>
    <div class="article-footer">
      本页为本地预览，不会进入公众号草稿箱，也不会自动发布。发布前仍需人工确认事实、证据和标题承诺。
    </div>
  </section>`;
}

function renderMiniList(items, emptyText) {
  const list = Array.isArray(items) ? items : [];
  if (!list.length) return `<p class="review-value">${escapeHtml(emptyText)}</p>`;
  return `<ul class="mini-list">${list.slice(0, 8).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
}

function getVersionReview() {
  return workbenchData.version_review || {};
}

function getLatestComparison() {
  const review = getVersionReview();
  return review.latest_comparison || {};
}

function getLatestDecision() {
  const review = getVersionReview();
  return review.latest_decision || {};
}

function getFinalReview() {
  return workbenchData.final_review || {};
}

function getFinalCandidate() {
  const review = getFinalReview();
  return review.selected_candidate || {};
}

function getFinalChecklist() {
  const review = getFinalReview();
  return review.selected_checklist || {};
}

function getPerformancePanel() {
  return workbenchData.performance_panel || {};
}

function getMethodologyPanel() {
  return workbenchData.methodology_panel || {};
}

function getGenerationVisualPanel() {
  return workbenchData.generation_visual_panel || {};
}

function getLivePilotPanel() {
  return workbenchData.live_pilot_panel || {};
}

function getImageAssetPanel() {
  return workbenchData.image_asset_panel || {};
}

function getPublishingPackPanel() {
  return workbenchData.publishing_pack_panel || {};
}

function getContentOpsPanel() {
  return workbenchData.content_ops_panel || {};
}

function getContentHardeningPanel() {
  return workbenchData.content_hardening_panel || {};
}

function getTrialPanel() {
  return workbenchData.trial_panel || {};
}

function getPhase22Panel() {
  return workbenchData.phase22_panel || {};
}

function getPhase23Panel() {
  return workbenchData.phase23_panel || {};
}

function getPhase24Panel() {
  return workbenchData.phase24_panel || {};
}

function getPhase25Panel() {
  return workbenchData.phase25_panel || {};
}

function getHotMaterialPanel() {
  return workbenchData.hot_material_panel || {};
}

function getConnectorHealthPanel() {
  return workbenchData.connector_health_panel || {};
}

function getEvidenceTopicPromotionPanel() {
  return workbenchData.evidence_topic_promotion_panel || {};
}

function getOpenClawMigrationPanel() {
  return workbenchData.openclaw_migration_panel || {};
}

function getOpenClawActivationPanel() {
  return workbenchData.openclaw_activation_panel || {};
}

function getRuntimeControlCenterPanel() {
  return workbenchData.runtime_control_center_panel || {};
}

function getAcquisitionPlaybookPanel() {
  return workbenchData.acquisition_playbook_panel || {};
}

function getAutonomousContentProductionPanel() {
  return workbenchData.autonomous_content_production_panel || {};
}

function getReplayTrialPanel() {
  return workbenchData.replay_trial_panel || {};
}

function renderReviewSection(title, note, body, open = true) {
  return `<details class="review-section" ${open ? "open" : ""}>
    <summary>${escapeHtml(title)}<span class="review-section-note">${escapeHtml(note || "")}</span></summary>
    <div class="review-grid">${body}</div>
  </details>`;
}

function getSelectedMethodologyTopic() {
  const panel = getMethodologyPanel();
  const article = getSelectedArticle();
  const topicId = article.topic_id || "";
  const topics = Array.isArray(panel.topic_scores) ? panel.topic_scores : [];
  return topics.find((item) => item.topic_id === topicId) || panel.selected_topic_score || {};
}

function getSelectedMethodologyArticle() {
  const panel = getMethodologyPanel();
  const article = getSelectedArticle();
  const reviews = Array.isArray(panel.article_reviews) ? panel.article_reviews : [];
  return reviews.find((item) => item.article_id === article.article_id) || panel.selected_article_review || {};
}

function getSelectedSession() {
  const panel = getPerformancePanel();
  return panel.selected_session || {};
}

function getSelectedMetrics() {
  const panel = getPerformancePanel();
  return panel.selected_metrics || {};
}

function versionReviewCommand(kind) {
  const comparison = getLatestComparison();
  const versionId = comparison.version_id || "";
  if (!versionId) return "python3 scripts/review_article_version.py --list";
  if (kind === "accept") return `python3 scripts/review_article_version.py --accept ${versionId} --score 8 --note ${shellQuote("人工确认新版更好")}`;
  if (kind === "reject") return `python3 scripts/review_article_version.py --reject ${versionId} --note ${shellQuote("人工确认新版不适合")}`;
  if (kind === "revise") return `python3 scripts/review_article_version.py --revise-more ${versionId} --note ${shellQuote("继续修改后再看")}`;
  return "python3 scripts/review_article_version.py --list";
}

function renderVersionReviewCard(cardClass = "review-card wide") {
  const comparison = getLatestComparison();
  const decision = getLatestDecision();
  const scores = comparison.scores || {};
  const versionId = comparison.version_id || "";
  if (!versionId) {
    return `<div class="${cardClass} version-panel">
      <p class="review-label">版本 Review</p>
      <p class="review-value">暂无新版本评分。批准并执行 action 后，运行 <code>make phase11-daily</code> 会在这里显示新旧版本质量对比。</p>
    </div>`;
  }
  const improvements = Array.isArray(comparison.improvements) ? comparison.improvements : [];
  const regressions = Array.isArray(comparison.regressions) ? comparison.regressions : [];
  return `<div class="${cardClass} version-panel">
    <p class="review-label">版本 Review</p>
    <p class="review-value"><strong>${escapeHtml(versionId)}</strong> · 推荐：<span class="badge ready">${escapeHtml(comparison.recommendation || "HUMAN_REVIEW")}</span> · 人工决策：<span class="badge">${escapeHtml(decision.decision || "UNREVIEWED")}</span></p>
    <p class="review-value">Score delta <span class="delta-number">${escapeHtml(scores.delta ?? 0)}</span> · 原稿 ${escapeHtml(scores.original_overall ?? 0)} → 新版 ${escapeHtml(scores.new_overall ?? 0)}</p>
    <p class="review-label">Improvements</p>${renderMiniList(improvements, "暂无明显提升")}
    <p class="review-label">Regressions</p>${renderMiniList(regressions, "暂无明显退化")}
    <div class="version-actions">
      <button class="copy-review-command" type="button" data-command="${escapeHtml(versionReviewCommand("accept"))}">复制 Accept 命令</button>
      <button class="copy-review-command" type="button" data-command="${escapeHtml(versionReviewCommand("reject"))}">复制 Reject 命令</button>
      <button class="copy-review-command" type="button" data-command="${escapeHtml(versionReviewCommand("revise"))}">复制 Revise-more 命令</button>
    </div>
  </div>`;
}

function renderFinalReviewCard(cardClass = "review-card wide") {
  const candidate = getFinalCandidate();
  const checklist = getFinalChecklist();
  const checks = Array.isArray(checklist.checks) ? checklist.checks : [];
  if (!candidate.final_candidate_id) {
    return `<div class="${cardClass} final-panel">
      <p class="review-label">最终候选稿</p>
      <p class="review-value">暂无 final article candidate。人工 ACCEPT 版本后运行 <code>make phase12-daily</code>，这里会显示最终人工发布前候选稿。</p>
    </div>`;
  }
  const risks = Array.isArray(candidate.remaining_risks) ? candidate.remaining_risks : [];
  const warningChecks = checks.filter((item) => item.status !== "PASS").slice(0, 6).map((item) => `${item.label}: ${item.status}${item.note ? " - " + item.note : ""}`);
  return `<div class="${cardClass} final-panel">
    <p class="review-label">最终候选稿</p>
    <p class="review-value"><strong>${escapeHtml(candidate.final_candidate_id)}</strong> · ${escapeHtml(candidate.quality_status || "NEEDS_FINAL_CHECK")} · Checklist ${escapeHtml(checklist.status || "UNREVIEWED")}</p>
    <p class="review-value">Version ${escapeHtml(candidate.version_id || "-")} · Human score ${escapeHtml(candidate.human_score ?? "-")} · Delta ${escapeHtml(candidate.version_score_delta ?? 0)}</p>
    <p class="review-label">Remaining risks</p>${renderMiniList(risks, "暂无剩余风险")}
    <p class="review-label">Checklist warnings</p>${renderMiniList(warningChecks, "Checklist 暂无 WARN/FAIL")}
    <div class="version-actions">
      <button class="copy-final-content" type="button" data-copy-kind="title">复制最终标题</button>
      <button class="copy-final-content" type="button" data-copy-kind="body">复制最终正文</button>
      <button class="copy-final-content" type="button" data-copy-kind="steps">复制人工发布步骤</button>
    </div>
  </div>`;
}

function performanceCommand(kind) {
  const candidate = getFinalCandidate();
  const session = getSelectedSession();
  if (kind === "create") {
    const finalId = candidate.final_candidate_id || "<final_candidate_id>";
    return `python3 scripts/create_manual_publish_session.py --create ${finalId} --note ${shellQuote("准备手动发布")}`;
  }
  if (kind === "published") {
    const sessionId = session.publish_session_id || "<publish_session_id>";
    return `python3 scripts/create_manual_publish_session.py --mark-published ${sessionId} --url ${shellQuote("https://example.com/manual-placeholder")} --note ${shellQuote("已手动发布")}`;
  }
  if (kind === "metrics") {
    const sessionId = session.publish_session_id || "<publish_session_id>";
    return `python3 scripts/record_post_publish_metrics.py --session ${sessionId} --views 1000 --likes 20 --wows 5 --shares 3 --comments 2 --note ${shellQuote("人工录入表现数据")}`;
  }
  return "python3 scripts/create_manual_publish_session.py --list";
}

function renderPerformancePanel(cardClass = "review-card wide") {
  const panel = getPerformancePanel();
  const session = getSelectedSession();
  const metrics = getSelectedMetrics();
  const memory = panel.selected_performance_record || {};
  const recommendations = Array.isArray(panel.recommendations) ? panel.recommendations : [];
  const sessionSummary = panel.session_summary || {};
  const metricsSummary = panel.metrics_summary || {};
  return `<div class="${cardClass} performance-panel">
    <p class="review-label">发布表现闭环</p>
    <p class="review-value">Sessions ${escapeHtml(sessionSummary.session_count ?? 0)} · Metrics ${escapeHtml(metricsSummary.metrics_count ?? 0)} · Rating ${escapeHtml(metrics.performance_rating || memory.performance_rating || "UNKNOWN")}</p>
    <p class="review-value">当前 session：${escapeHtml(session.publish_session_id || "暂无")} · ${escapeHtml(session.publish_status || "未创建")} · ${escapeHtml(session.published_url || "")}</p>
    <p class="review-value">Views ${escapeHtml(metrics.views ?? "-")} · Likes ${escapeHtml(metrics.likes ?? "-")} · Wows ${escapeHtml(metrics.wows ?? "-")} · Shares ${escapeHtml(metrics.shares ?? "-")} · Comments ${escapeHtml(metrics.comments ?? "-")}</p>
    <p class="review-label">Learning feedback</p>${renderMiniList(recommendations.map((item) => `${item.target_area}: ${item.recommendation}`), "暂无表现反馈建议")}
    <div class="version-actions">
      <button class="copy-performance-command" type="button" data-command="${escapeHtml(performanceCommand("create"))}">复制创建发布 session 命令</button>
      <button class="copy-performance-command" type="button" data-command="${escapeHtml(performanceCommand("published"))}">复制标记已发布命令</button>
      <button class="copy-performance-command" type="button" data-command="${escapeHtml(performanceCommand("metrics"))}">复制录入表现数据命令</button>
    </div>
  </div>`;
}

function renderMethodologyScoreGrid(topic, articleReview) {
  const topicScores = topic.methodology_scores || {};
  const articleScores = articleReview.scores || {};
  const items = [
    ["选题总分", topic.methodology_total_score ?? "-"],
    ["文章总分", articleReview.methodology_total_score ?? "-"],
    ["预期差", topicScores.expectation_gap ?? "-"],
    ["证据强度", topicScores.evidence_strength ?? "-"],
    ["核心判断", articleScores.core_judgment ?? "-"],
    ["判断密度", articleScores.judgment_density ?? "-"]
  ];
  return `<div class="methodology-score-grid">${items.map(([label, value]) => `<div class="methodology-score-item"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>`).join("")}</div>`;
}

function renderMethodologyPanel(cardClass = "review-card wide") {
  const panel = getMethodologyPanel();
  const topic = getSelectedMethodologyTopic();
  const articleReview = getSelectedMethodologyArticle();
  const recommendations = Array.isArray(panel.recommendations) ? panel.recommendations : [];
  const topicMissing = Array.isArray(topic.missing_requirements) ? topic.missing_requirements : [];
  const weaknesses = Array.isArray(articleReview.weaknesses) ? articleReview.weaknesses : [];
  const priorities = Array.isArray(articleReview.rewrite_priorities) ? articleReview.rewrite_priorities : [];
  const flags = Array.isArray(articleReview.generic_language_flags) ? articleReview.generic_language_flags : [];
  if (!topic.topic_id && !articleReview.article_id) {
    return `<div class="${cardClass} methodology-panel">
      <p class="review-label">内容方法论</p>
      <p class="review-value">暂无方法论评分。运行 <code>make phase14-daily</code> 后，这里会展示选题方法论、文章方法论和打法 recipe。</p>
    </div>`;
  }
  return `<div class="${cardClass} methodology-panel">
    <p class="review-label">内容方法论</p>
    <p class="review-value"><strong>${escapeHtml(topic.recommended_recipe_id || articleReview.recipe_id || "strategy_recipe")}</strong> · 选题 ${escapeHtml(topic.recommendation || "WATCH")} · 文章 ${escapeHtml(articleReview.recommendation || "REVISE")}</p>
    ${renderMethodologyScoreGrid(topic, articleReview)}
    <p class="review-label">核心判断</p><p class="review-value">${escapeHtml(shortText(topic.core_judgment || articleReview.review_summary, "尚未形成清晰核心判断"))}</p>
    <p class="review-label">为什么现在写</p><p class="review-value">${escapeHtml(shortText(topic.why_now, "需要补充当前窗口期判断"))}</p>
    <p class="review-label">读者收益</p><p class="review-value">${escapeHtml(shortText(topic.reader_value_summary, "需要明确读者读完获得什么"))}</p>
    <p class="review-label">主要弱点</p>${renderMiniList(weaknesses.concat(topicMissing).slice(0, 8), "暂无主要弱点")}
    <p class="review-label">重写优先级</p>${renderMiniList(priorities, "暂无重写优先级")}
    <p class="review-label">空泛表达提示</p>${renderMiniList(flags, "未发现高频空泛表达")}
    <p class="review-label">表现对齐建议</p>${renderMiniList(recommendations.map((item) => `${item.target_area || "methodology"}: ${item.recommendation || ""}`), "暂无方法论-表现对齐建议")}
  </div>`;
}

function renderGenerationVisualPanel(cardClass = "review-card wide") {
  const panel = getGenerationVisualPanel();
  const brief = panel.selected_brief || {};
  const outline = panel.selected_outline || {};
  const draft = panel.selected_draft || {};
  const visualPlan = panel.selected_visual_plan || {};
  const requests = Array.isArray(panel.selected_image_requests) ? panel.selected_image_requests : [];
  const visuals = Array.isArray(visualPlan.visuals) ? visualPlan.visuals : [];
  if (!brief.brief_id && !visualPlan.visual_plan_id) {
    return `<div class="${cardClass} generation-panel">
      <p class="review-label">生成与图片策略</p>
      <p class="review-value">暂无 methodology generation / visual plan。运行 <code>make phase15-daily</code> 后会显示方法论 brief、outline、draft 和图片需求。</p>
    </div>`;
  }
  const visualRows = visuals.slice(0, 5).map((item) => `${item.placement}: ${item.visual_type} / ${item.source_strategy} / ${item.information_job}`);
  const requestRows = requests.slice(0, 5).map((item) => `${item.visual_type}: ${item.asset_status} / ${item.recommended_tool}`);
  return `<div class="${cardClass} generation-panel">
    <p class="review-label">生成与图片策略</p>
    <p class="review-value">Brief <strong>${escapeHtml(brief.status || "n/a")}</strong> · Outline ${escapeHtml(outline.status || "n/a")} · Draft ${escapeHtml(draft.status || "n/a")}</p>
    <p class="review-value">Visual plan ${escapeHtml(visualPlan.visual_plan_id || "暂无")} · recommended visuals ${escapeHtml(visualPlan.recommended_visual_count ?? 0)} · do_not_auto_generate_images=true</p>
    <p class="review-label">Methodology brief</p>
    <p class="review-value">${escapeHtml(shortText(brief.core_judgment || brief.core_question, "暂无方法论 brief"))}</p>
    <p class="review-label">Visual placements</p>${renderMiniList(visualRows, "暂无 visual plan")}
    <p class="review-label">Image asset requests</p>${renderMiniList(requestRows, "暂无 image request")}
    <div class="version-actions">
      <button class="copy-image-request" type="button" data-copy-image="prompt">复制首个 image prompt</button>
      <button class="copy-image-request" type="button" data-copy-image="brief">复制首个 design brief</button>
    </div>
  </div>`;
}

function liveStatusText(summary) {
  if (!summary || !Object.keys(summary).length) return "暂无";
  const ready = summary.ready_check_status || "NOT_REQUIRED";
  const reason = summary.ready_check_reason ? ` / ${summary.ready_check_reason}` : "";
  return `${summary.live_attempted ? "attempted" : "not attempted"} · ${summary.live_succeeded ? "succeeded" : "not succeeded"} · ${ready}${reason}`;
}

function renderLivePilotPanel(cardClass = "review-card wide") {
  const panel = getLivePilotPanel();
  const comparison = panel.comparison_summary || {};
  const approval = panel.image_approval_summary || {};
  const phase16 = panel.phase16_summary || {};
  const comparisons = Array.isArray(panel.comparisons) ? panel.comparisons : [];
  const approvals = Array.isArray(panel.approval_requests) ? panel.approval_requests : [];
  const hasLivePayload = Object.keys(panel.brief_summary || {}).length || Object.keys(panel.draft_summary || {}).length || Object.keys(panel.visual_prompt_summary || {}).length;
  if (!hasLivePayload) {
    return `<div class="${cardClass} live-panel">
      <p class="review-label">Live Pilot</p>
      <p class="review-value">暂无 live pilot sidecar。运行 <code>make phase16-daily</code> 后，这里会展示 dry-run / readiness 状态、live-vs-rule 对比和图片生成审批队列。</p>
    </div>`;
  }
  return `<div class="${cardClass} live-panel">
    <p class="review-label">Live Pilot Sidecars</p>
    <p class="review-value">Brief ${escapeHtml(liveStatusText(panel.brief_summary))}</p>
    <p class="review-value">Draft ${escapeHtml(liveStatusText(panel.draft_summary))}</p>
    <p class="review-value">Rewrite ${escapeHtml(liveStatusText(panel.rewrite_summary))}</p>
    <p class="review-value">Visual prompt ${escapeHtml(liveStatusText(panel.visual_prompt_summary))}</p>
    <p class="review-label">Live vs Rule</p>
    <p class="review-value">Comparisons ${escapeHtml(comparison.comparison_count ?? 0)} · use_live ${escapeHtml(comparison.use_live ?? 0)} · merge ${escapeHtml(comparison.merge ?? 0)} · human_review ${escapeHtml(comparison.human_review ?? 0)}</p>
    ${renderMiniList(comparisons.map((item) => `${item.comparison_type}: ${item.recommendation} / delta ${item.scores ? item.scores.delta : 0}`), "暂无 live comparison")}
    <p class="review-label">Image generation approval</p>
    <p class="review-value">Requests ${escapeHtml(approval.request_count ?? 0)} · pending ${escapeHtml(approval.pending ?? 0)} · approved ${escapeHtml(approval.approved ?? 0)} · do_not_auto_generate_images=true</p>
    ${renderMiniList(approvals.map((item) => `${item.visual_type}: ${item.approval_status} / generation_allowed ${item.generation_allowed}`), "暂无图片生成审批请求")}
    <p class="review-label">Pipeline policy</p>
    <p class="review-value">live attempted ${escapeHtml(phase16.live_attempted_count ?? 0)} · live succeeded ${escapeHtml(phase16.live_succeeded_count ?? 0)} · sidecar_only=true · do_not_auto_publish=true</p>
  </div>`;
}

function imageAssetCommand(kind) {
  const panel = getImageAssetPanel();
  const tasks = Array.isArray(panel.manual_image_tasks) ? panel.manual_image_tasks : [];
  const assets = Array.isArray(panel.image_assets) ? panel.image_assets : [];
  const task = tasks[0] || {};
  const asset = assets[0] || {};
  if (kind === "mark_available") {
    const assetId = asset.asset_id || "<imgasset_id>";
    const path = task.expected_asset_path || asset.asset_path || "同行资本市场内容系统/08_assets/images/example.png";
    return `python3 scripts/update_image_asset_library.py --mark-available ${assetId} --path ${shellQuote(path)} --note ${shellQuote("人工生成后放入本地")}`;
  }
  if (kind === "approve_visual") {
    const assetId = asset.asset_id || "<imgasset_id>";
    return `python3 scripts/review_visual_asset.py --approve ${assetId} --note ${shellQuote("图能解释文章核心框架")}`;
  }
  return "python3 scripts/update_image_asset_library.py";
}

function renderImageAssetPanel(cardClass = "review-card wide") {
  const panel = getImageAssetPanel();
  const contentPromotion = panel.live_content_promotion_summary || {};
  const rewritePromotion = panel.live_rewrite_promotion_summary || {};
  const taskSummary = panel.manual_image_task_summary || {};
  const librarySummary = panel.image_asset_library_summary || {};
  const previewSummary = panel.article_with_images_summary || {};
  const reviewSummary = panel.final_visual_review_summary || {};
  const tasks = Array.isArray(panel.manual_image_tasks) ? panel.manual_image_tasks : [];
  const assets = Array.isArray(panel.image_assets) ? panel.image_assets : [];
  const reviews = Array.isArray(panel.visual_reviews) ? panel.visual_reviews : [];
  const hasPanel = Object.keys(taskSummary).length || Object.keys(librarySummary).length || Object.keys(reviewSummary).length;
  if (!hasPanel) {
    return `<div class="${cardClass} image-asset-panel">
      <p class="review-label">图片资产链路</p>
      <p class="review-value">暂无 Phase17 图片资产数据。运行 <code>make phase17-daily</code> 后会显示 live promotion、manual image tasks、asset library 和 final visual review。</p>
    </div>`;
  }
  const taskRows = tasks.slice(0, 5).map((item) => `${item.visual_type}: ${item.generation_status} / ${item.expected_asset_path}`);
  const assetRows = assets.slice(0, 5).map((item) => `${item.visual_type}: ${item.asset_status} / wechat_ready ${item.wechat_ready} / ${item.asset_path}`);
  const reviewRows = reviews.slice(0, 5).map((item) => `${item.visual_type}: ${item.review_status} / wechat_ready ${item.wechat_ready}`);
  return `<div class="${cardClass} image-asset-panel">
    <p class="review-label">Approved Live Promotion & Image Assets</p>
    <p class="review-value">Live candidates ${escapeHtml(contentPromotion.candidate_count ?? 0)} · Live rewrites ${escapeHtml(rewritePromotion.promoted ?? 0)} · sidecar only</p>
    <p class="review-value">Image tasks ${escapeHtml(taskSummary.task_count ?? 0)} · assets ${escapeHtml(librarySummary.asset_count ?? 0)} · available ${escapeHtml(librarySummary.available ?? 0)} · wechat_ready ${escapeHtml(reviewSummary.wechat_ready ?? 0)}</p>
    <p class="review-value">Article-with-images preview: ${escapeHtml(previewSummary.visual_slot_count ?? 0)} slots · <code>${escapeHtml(panel.article_with_images_preview_path || "latest_article_with_images_preview.html")}</code></p>
    <p class="review-label">Manual image tasks</p>${renderMiniList(taskRows, "暂无已批准图片生成任务")}
    <p class="review-label">Image asset library</p>${renderMiniList(assetRows, "暂无图片资产 metadata")}
    <p class="review-label">Final visual review</p>${renderMiniList(reviewRows, "暂无最终视觉审查")}
    <div class="version-actions">
      <button class="copy-image-asset" type="button" data-copy-asset="prompt">复制首个 image prompt</button>
      <button class="copy-image-asset" type="button" data-copy-asset="brief">复制首个 design brief</button>
      <button class="copy-image-asset" type="button" data-copy-asset="path">复制 expected asset path</button>
      <button class="copy-image-asset" type="button" data-command="${escapeHtml(imageAssetCommand("mark_available"))}">复制标记 available 命令</button>
      <button class="copy-image-asset" type="button" data-command="${escapeHtml(imageAssetCommand("approve_visual"))}">复制视觉 approve 命令</button>
    </div>
  </div>`;
}

function publishingPackText(kind) {
  const panel = getPublishingPackPanel();
  const pack = panel.selected_copy_pack || {};
  const slots = Array.isArray(pack.image_slots) ? pack.image_slots : [];
  if (kind === "title") return pack.title_to_copy || "";
  if (kind === "body") return pack.body_with_image_markers || pack.body_markdown_to_copy || "";
  if (kind === "slots") {
    return slots.map((slot) => `${slot.slot_marker || ""} ${slot.copy_instruction || ""}\nasset: ${slot.asset_path || ""}\ncaption: ${slot.caption_suggestion || ""}`).join("\n\n");
  }
  if (kind === "steps") {
    const steps = Array.isArray(pack.manual_copy_steps) ? pack.manual_copy_steps : [];
    const visualSteps = Array.isArray(pack.visual_copy_steps) ? pack.visual_copy_steps : [];
    return [...steps, ...visualSteps].join("\n");
  }
  return "";
}

function renderPublishingPackPanel(cardClass = "review-card wide") {
  const panel = getPublishingPackPanel();
  const candidateSummary = panel.visual_candidate_summary || {};
  const packSummary = panel.copy_pack_summary || {};
  const checklistSummary = panel.visual_checklist_summary || {};
  const performanceSummary = panel.visual_performance_summary || {};
  const feedbackSummary = panel.visual_strategy_feedback_summary || {};
  const candidate = panel.selected_visual_candidate || {};
  const pack = panel.selected_copy_pack || {};
  const checklist = panel.selected_visual_checklist || {};
  const slots = Array.isArray(pack.image_slots) ? pack.image_slots : [];
  const checks = Array.isArray(checklist.checks) ? checklist.checks : [];
  const recommendations = Array.isArray(panel.visual_strategy_recommendations) ? panel.visual_strategy_recommendations : [];
  const hasPanel = Object.keys(candidateSummary).length || Object.keys(packSummary).length || Object.keys(checklistSummary).length;
  if (!hasPanel) {
    return `<div class="${cardClass} publishing-pack-panel">
      <p class="review-label">图文发布包</p>
      <p class="review-value">暂无 Phase18 图文发布包。运行 <code>make phase18-daily</code> 后会显示 visual-approved candidate、copy pack、visual checklist 和视觉反馈。</p>
    </div>`;
  }
  const slotRows = slots.slice(0, 6).map((slot) => `${slot.slot_marker}: ${slot.visual_type} / ${slot.asset_status} / ${slot.placement}`);
  const checklistRows = checks.filter((item) => item.status !== "PASS").slice(0, 6).map((item) => `${item.label}: ${item.status}${item.note ? " - " + item.note : ""}`);
  const recommendationRows = recommendations.map((item) => `${item.target_area || "visual"}: ${item.recommendation || ""}`);
  return `<div class="${cardClass} publishing-pack-panel">
    <p class="review-label">图文发布包</p>
    <p class="review-value">Visual candidates ${escapeHtml(candidateSummary.candidate_count ?? 0)} · Packs ${escapeHtml(packSummary.pack_count ?? 0)} · Checklists ${escapeHtml(checklistSummary.checklist_count ?? 0)} · do_not_publish=true</p>
    <p class="review-value">当前包：<strong>${escapeHtml(pack.copy_pack_id || "暂无")}</strong> · ${escapeHtml(pack.pack_status || "NEEDS_REVIEW")} · Checklist ${escapeHtml(checklist.status || "UNREVIEWED")}</p>
    <p class="review-value">Visual status ${escapeHtml(candidate.visual_status || "UNKNOWN")} · visual ready ${escapeHtml(candidateSummary.visual_ready ?? 0)} · performance records ${escapeHtml(performanceSummary.record_count ?? 0)} · feedback ${escapeHtml(feedbackSummary.recommendation_count ?? 0)}</p>
    <p class="review-label">Image slots</p>${renderMiniList(slotRows, "暂无图片槽位")}
    <p class="review-label">Checklist warnings</p>${renderMiniList(checklistRows, "视觉 checklist 暂无 WARN/FAIL")}
    <p class="review-label">Visual strategy feedback</p>${renderMiniList(recommendationRows, "暂无视觉策略反馈")}
    <div class="version-actions">
      <button class="copy-publishing-pack" type="button" data-copy-pack="title">复制标题</button>
      <button class="copy-publishing-pack" type="button" data-copy-pack="body">复制正文含图片槽位</button>
      <button class="copy-publishing-pack" type="button" data-copy-pack="slots">复制图片槽位说明</button>
      <button class="copy-publishing-pack" type="button" data-copy-pack="steps">复制人工发布步骤</button>
    </div>
  </div>`;
}

function renderContentOpsPanel(cardClass = "review-card wide") {
  const panel = getContentOpsPanel();
  const calendarSummary = panel.calendar_summary || {};
  const queueSummary = panel.queue_summary || {};
  const rhythmSummary = panel.rhythm_summary || {};
  const archiveSummary = panel.archive_summary || {};
  const metricsSummary = panel.metrics_review_summary || {};
  const closeoutSummary = panel.closeout_summary || {};
  const todayItems = Array.isArray(panel.today_recommendations) ? panel.today_recommendations : [];
  const thisWeek = Array.isArray(panel.this_week_recommendations) ? panel.this_week_recommendations : [];
  const blockers = Array.isArray(panel.blockers) ? panel.blockers : [];
  const rhythm = Array.isArray(panel.weekly_rhythm) ? panel.weekly_rhythm : [];
  const actions = Array.isArray(panel.operator_actions) ? panel.operator_actions : [];
  const insights = Array.isArray(panel.metrics_insights) ? panel.metrics_insights : [];
  const hasPanel = Object.keys(calendarSummary).length || Object.keys(queueSummary).length || Object.keys(closeoutSummary).length;
  if (!hasPanel) {
    return `<div class="${cardClass} content-ops-panel">
      <p class="review-label">内容运营</p>
      <p class="review-value">暂无 Phase19 内容运营数据。运行 <code>make phase19-daily</code> 后会显示发布日历、队列优先级、周节奏、已发布归档和运营 closeout。</p>
    </div>`;
  }
  const todayRows = todayItems.map((item) => `${item.priority}: ${item.title || item.queue_item_id} / ${item.readiness_status}`);
  const weekRows = thisWeek.slice(0, 6).map((item) => `${item.priority}: ${item.title || item.queue_item_id} / ${item.recommended_next_action}`);
  const blockerRows = blockers.slice(0, 6).map((item) => `${item.title || item.queue_item_id}: ${item.readiness_status} / ${(item.blockers || []).join("; ")}`);
  const rhythmRows = rhythm.slice(0, 7).map((item) => `${item.weekday}: ${item.recommended_content_type} / ${item.status}`);
  return `<div class="${cardClass} content-ops-panel">
    <p class="review-label">内容运营</p>
    <p class="review-value">Calendar ${escapeHtml(calendarSummary.planned_slots ?? 0)} slots · Queue ${escapeHtml(queueSummary.item_count ?? 0)} · Today ${escapeHtml(queueSummary.today ?? 0)} · This week ${escapeHtml(queueSummary.this_week ?? 0)}</p>
    <p class="review-value">Rhythm ready days ${escapeHtml(rhythmSummary.ready_days ?? 0)} · Published ${escapeHtml(archiveSummary.published_count ?? 0)} · Metrics articles ${escapeHtml(metricsSummary.with_metrics_count ?? 0)} · Closeout blocked ${escapeHtml(closeoutSummary.blocked_count ?? 0)}</p>
    <p class="review-label">今日建议发布</p>${renderMiniList(todayRows, "暂无 TODAY 内容")}
    <p class="review-label">本周优先</p>${renderMiniList(weekRows, "暂无 THIS_WEEK 内容")}
    <p class="review-label">待处理 blocker</p>${renderMiniList(blockerRows, "暂无 blocker")}
    <p class="review-label">本周节奏</p>${renderMiniList(rhythmRows, "暂无 weekly rhythm")}
    <p class="review-label">发布后复盘</p>${renderMiniList(insights, "暂无指标复盘 insight")}
    <p class="review-label">运营动作</p>${renderMiniList(actions, "暂无 operator action")}
  </div>`;
}

function renderContentHardeningPanel(cardClass = "review-card wide", mode = "system") {
  const panel = getContentHardeningPanel();
  const trial = panel.trial_summary || {};
  const failure = panel.failure_summary || {};
  const regression = panel.regression_summary || {};
  const readiness = panel.system_closeout_readiness || {};
  const phase20 = panel.phase20_summary || {};
  const issues = Array.isArray(panel.failure_issues) ? panel.failure_issues : [];
  const checks = Array.isArray(panel.regression_checks) ? panel.regression_checks : [];
  const checklist = Array.isArray(panel.daily_checklist) ? panel.daily_checklist : [];
  const gaps = Array.isArray(panel.known_gaps) ? panel.known_gaps : [];
  const sections = Array.isArray(panel.runbook_sections) ? panel.runbook_sections : [];
  const hasPanel = Object.keys(trial).length || Object.keys(failure).length || Object.keys(regression).length || Object.keys(readiness).length;
  if (!hasPanel) {
    return `<div class="${cardClass} hardening-panel">
      <p class="review-label">Phase20 试运行加固</p>
      <p class="review-value">暂无 Phase20 hardening 数据。运行 <code>make phase20-daily</code> 后会显示 trial protocol、failure handling、checklist regression、runbook 和 system closeout。</p>
    </div>`;
  }
  const issueRows = issues.slice(0, 6).map((item) => `${item.severity}: ${item.area} / ${item.description}`);
  const checkRows = checks.slice(0, 6).map((item) => `${item.status}: ${item.check_id} / ${item.message}`);
  const runbookRows = sections.slice(0, 6).map((item) => item.title || "");
  const title = mode === "ops" ? "今日建议动作与试运行状态" : "系统运维与回归检查";
  return `<div class="${cardClass} hardening-panel">
    <p class="review-label">${escapeHtml(title)}</p>
    <p class="review-value">Trial ${escapeHtml(trial.days ?? 0)} days · checklist ${escapeHtml(trial.daily_checklist_count ?? 0)} · Phase20 ${escapeHtml(phase20.trial_readiness_status || readiness.status || "UNKNOWN")}</p>
    <p class="review-value">Failure issues ${escapeHtml(failure.issue_count ?? 0)} · blockers ${escapeHtml(failure.blocker_count ?? 0)} · can_continue ${escapeHtml(failure.can_continue ?? true)} · regression ${escapeHtml(regression.regression_status || "UNKNOWN")}</p>
    <p class="review-label">Daily checklist</p>${renderMiniList(checklist.slice(0, 6), "暂无 trial checklist")}
    <p class="review-label">Failure handling</p>${renderMiniList(issueRows, "暂无 failure issue")}
    <p class="review-label">Regression checks</p>${renderMiniList(checkRows, "暂无 checklist regression")}
    <p class="review-label">Runbook sections</p>${renderMiniList(runbookRows, "暂无 operator runbook")}
    <p class="review-label">Known gaps</p>${renderMiniList(gaps.slice(0, 6), "暂无 closeout gap")}
  </div>`;
}

function renderTrialPanel(cardClass = "review-card wide") {
  const panel = getTrialPanel();
  const days = Array.isArray(panel.day_summaries) ? panel.day_summaries : [];
  const retrospective = panel.retrospective_summary || {};
  const fixSummary = panel.fix_pack_summary || {};
  const phase21 = panel.phase21_summary || {};
  const recurring = Array.isArray(panel.recurring_issues) ? panel.recurring_issues : [];
  const friction = Array.isArray(panel.operator_friction) ? panel.operator_friction : [];
  const recommendations = Array.isArray(panel.recommendations) ? panel.recommendations : [];
  const fixes = Array.isArray(panel.fixes) ? panel.fixes : [];
  const safety = panel.safety_boundary_check || {};
  const hasPanel = days.length || Object.keys(retrospective).length || Object.keys(fixSummary).length;
  if (!hasPanel) {
    return `<div class="${cardClass} trial-panel">
      <p class="review-label">试运行</p>
      <p class="review-value">暂无 Phase21 trial 数据。运行 <code>make phase21-trial</code> 后会显示 Day 1-5、weekly retrospective 和 trial fix pack。</p>
    </div>`;
  }
  const dayRows = days.map((item) => `Day ${item.trial_day}: ${item.day_status} / issues ${item.issue_count} / actions ${item.action_count} / continue ${item.can_continue_trial}`);
  const recurringRows = recurring.map((item) => `${item.area}: ${item.description} / count ${item.count}`);
  const fixRows = fixes.slice(0, 6).map((item) => `${item.severity}: ${item.fix_type} / ${item.area} / ${item.description}`);
  return `<div class="${cardClass} trial-panel">
    <p class="review-label">Phase21 试运行</p>
    <p class="review-value">Days ${escapeHtml(retrospective.days_recorded ?? days.length)} · pass ${escapeHtml(retrospective.pass_days ?? 0)} · warn ${escapeHtml(retrospective.warn_days ?? 0)} · blocked ${escapeHtml(retrospective.blocked_days ?? 0)} · phase21 ${escapeHtml(phase21.status || "UNKNOWN")}</p>
    <p class="review-value">Fixes ${escapeHtml(fixSummary.fix_count ?? 0)} · quick ${escapeHtml(fixSummary.quick_fix ?? 0)} · next phase ${escapeHtml(fixSummary.next_phase ?? 0)} · high ${escapeHtml(fixSummary.high_severity ?? 0)} · scaffold_only=true</p>
    <p class="review-label">Trial Day 1-5</p>${renderMiniList(dayRows, "暂无 trial day record")}
    <p class="review-label">Recurring issues</p>${renderMiniList(recurringRows, "暂无 recurring issue")}
    <p class="review-label">Operator friction</p>${renderMiniList(friction, "暂无 operator friction")}
    <p class="review-label">Trial fix pack</p>${renderMiniList(fixRows, "暂无 trial fix")}
    <p class="review-label">Safety boundary</p><p class="review-value">auto_publish=${escapeHtml(safety.auto_publish ?? false)} · wechat_api=${escapeHtml(safety.wechat_api ?? false)} · auto_image_generation=${escapeHtml(safety.auto_image_generation ?? false)} · violations ${escapeHtml((safety.violations || []).length || 0)}</p>
    <p class="review-label">Next phase</p>${renderMiniList([panel.next_phase_recommendation || "Phase 22：Trial Fix Implementation & Stable Ops v1"].concat(recommendations.slice(0, 3)), "暂无 next phase recommendation")}
  </div>`;
}

function renderPhase22Panel(cardClass = "review-card wide") {
  const panel = getPhase22Panel();
  const runner = panel.daily_runner_summary || {};
  const issues = panel.recurring_issue_summary || {};
  const calendar = panel.weekly_calendar_summary || {};
  const fixSummary = panel.fix_pack_summary || {};
  const feedback = panel.post_publish_feedback_summary || {};
  const actions = Array.isArray(panel.daily_actions) ? panel.daily_actions : [];
  const recurring = Array.isArray(panel.recurring_issues) ? panel.recurring_issues : [];
  const calendarItems = Array.isArray(panel.weekly_calendar) ? panel.weekly_calendar : [];
  const fixes = Array.isArray(panel.fixes) ? panel.fixes : [];
  const recommendations = Array.isArray(panel.post_publish_recommendations) ? panel.post_publish_recommendations : [];
  const policy = panel.policy || {};
  const hasPanel = Object.keys(runner).length || Object.keys(issues).length || Object.keys(calendar).length || Object.keys(fixSummary).length;
  if (!hasPanel) {
    return `<div class="${cardClass} phase22-panel">
      <p class="review-label">Phase22 内容运营闭环</p>
      <p class="review-value">暂无 Phase22 数据。运行 <code>make phase22-daily</code> 后会显示每日 action list、recurring issues、weekly calendar、fix pack 和 post-publish feedback。</p>
    </div>`;
  }
  const actionRows = actions.slice(0, 6).map((item) => `${item.urgency}: ${item.area} / ${item.instruction}`);
  const issueRows = recurring.slice(0, 6).map((item) => `${item.recommended_order}. ${item.urgency} ${item.area}: ${item.description}`);
  const calendarRows = calendarItems.slice(0, 7).map((item) => `${item.date}: ${item.status} / ${item.title}`);
  const fixRows = fixes.slice(0, 6).map((item) => `${item.recommended_order}. ${item.urgency || item.priority} ${item.area}: ${item.action || item.recommended_change}`);
  const recommendationRows = recommendations.slice(0, 5).map((item) => `${item.priority || "LOW"} ${item.target_area}: ${item.recommendation}`);
  return `<div class="${cardClass} phase22-panel">
    <p class="review-label">Phase22 内容运营闭环</p>
    <p class="review-value">Runner ${escapeHtml(panel.daily_runner_status || "UNKNOWN")} · actions ${escapeHtml(runner.action_count ?? 0)} · ready ${escapeHtml(runner.ready_actions ?? 0)} · recurring issues ${escapeHtml(issues.issue_count ?? 0)}</p>
    <p class="review-value">Calendar ${escapeHtml(calendar.calendar_days ?? 0)} days · ready ${escapeHtml(calendar.ready_days ?? 0)} · blocked ${escapeHtml(calendar.blocked_days ?? 0)} · feedback ${escapeHtml(feedback.recommendation_count ?? 0)}</p>
    <p class="review-label">今日 action list</p>${renderMiniList(actionRows, "暂无 daily action")}
    <p class="review-label">Recurring Issues Panel</p>${renderMiniList(issueRows, "暂无 recurring issue")}
    <p class="review-label">7 天发布计划</p>${renderMiniList(calendarRows, "暂无 weekly calendar")}
    <p class="review-label">Content Fix Pack</p>${renderMiniList(fixRows, "暂无 fix pack")}
    <p class="review-label">Post-publish feedback</p>${renderMiniList(recommendationRows, "暂无 performance feedback")}
    <p class="review-label">Allowed / Forbidden</p>
    <p class="review-value">Allowed: dry-run, manual-confirm, copy command hints, record human metrics. Boundary: no_auto_publish=${escapeHtml(policy.no_auto_publish ?? true)} · no_wechat_api=${escapeHtml(policy.no_wechat_api ?? true)} · no_auto_image_generation=${escapeHtml(policy.no_auto_image_generation ?? true)} · no_mainline_overwrite=${escapeHtml(policy.no_mainline_overwrite ?? true)}</p>
  </div>`;
}

function renderStableOpsPanel(cardClass = "review-card wide") {
  const panel = getPhase23Panel();
  const issueSummary = panel.issue_resolution_summary || {};
  const quickSummary = panel.quick_fix_summary || {};
  const queueSummary = panel.queue_repair_summary || {};
  const calendarSummary = panel.calendar_calibration_summary || {};
  const stabilizerSummary = panel.stabilizer_summary || {};
  const verificationSummary = panel.verification_summary || {};
  const gateSummary = panel.gate_summary || {};
  const issues = Array.isArray(panel.issues) ? panel.issues : [];
  const fixes = Array.isArray(panel.fix_results) ? panel.fix_results : [];
  const queueItems = Array.isArray(panel.queue_items) ? panel.queue_items : [];
  const calendarDays = Array.isArray(panel.calendar_days) ? panel.calendar_days : [];
  const verifications = Array.isArray(panel.verifications) ? panel.verifications : [];
  const criteria = Array.isArray(panel.gate_criteria) ? panel.gate_criteria : [];
  const nextActions = Array.isArray(panel.next_actions) ? panel.next_actions : [];
  const manualItems = Array.isArray(panel.manual_items) ? panel.manual_items : [];
  const unresolvedItems = Array.isArray(panel.unresolved_items) ? panel.unresolved_items : [];
  const policy = panel.policy || {};
  const hasPanel = Object.keys(issueSummary).length || Object.keys(gateSummary).length || panel.gate_status;
  if (!hasPanel || panel.gate_status === "UNKNOWN") {
    return `<div class="${cardClass} stable-ops-panel">
      <p class="review-label">Phase23 Stable Ops</p>
      <p class="review-value">暂无 Phase23 数据。运行 <code>make phase23-daily</code> 后会显示 high-priority issue resolution、quick fixes、queue/calendar repair、verification 和 stable readiness gate。</p>
    </div>`;
  }
  const issueRows = issues.slice(0, 6).map((item) => `${item.severity}: ${item.resolution_type} / ${item.area} / ${item.title}`);
  const fixRows = fixes.slice(0, 6).map((item) => `${item.status}: ${item.fix_type} / ${item.change_summary}`);
  const queueRows = queueItems.slice(0, 6).map((item) => `${item.repaired_readiness_status}: ${item.title} / next: ${item.next_operator_action}`);
  const calendarRows = calendarDays.slice(0, 7).map((item) => `${item.date}: ${item.calibrated_status} / ${item.required_operator_action || item.readiness_reason}`);
  const verificationRows = verifications.slice(0, 6).map((item) => `${item.verification_status}: ${item.source_issue_id} / remaining ${(item.remaining_work || []).join("; ")}`);
  const criterionRows = criteria.slice(0, 8).map((item) => `${item.status}: ${item.criterion_id} / ${item.message}`);
  const manualRows = manualItems.slice(0, 4).map((item) => `${item.status || item.verification_status}: ${item.source_issue_id || item.resolution_id || item.fix_result_id}`);
  const unresolvedRows = unresolvedItems.slice(0, 4).map((item) => `${item.verification_status}: ${item.source_issue_id || item.resolution_id}`);
  return `<div class="${cardClass} stable-ops-panel">
    <p class="review-label">Phase23 Stable Ops Panel</p>
    <p class="review-value">Gate ${escapeHtml(panel.gate_status || "UNKNOWN")} · criteria pass ${escapeHtml(gateSummary.pass ?? 0)} / warn ${escapeHtml(gateSummary.warn ?? 0)} / fail ${escapeHtml(gateSummary.fail ?? 0)} · blocking ${escapeHtml(gateSummary.blocking_failures ?? 0)}</p>
    <p class="review-value">High issues ${escapeHtml(issueSummary.high_priority ?? 0)} · quick fixes ${escapeHtml(quickSummary.applied_sidecar ?? 0)} applied · queue improved ${escapeHtml(queueSummary.improved ?? 0)} · calendar actionable ${escapeHtml(calendarSummary.actionable_days ?? 0)}</p>
    <p class="review-label">Trial Day Status Stabilizer</p>
    <p class="review-value">Trial ${escapeHtml(panel.stabilizer_status_before || "UNKNOWN")} → ${escapeHtml(panel.stabilizer_status_after || "UNKNOWN")} · blockers ${escapeHtml(stabilizerSummary.blocker_count ?? 0)} · actionable warnings ${escapeHtml(stabilizerSummary.actionable_warning_count ?? 0)} · continue ${escapeHtml(stabilizerSummary.can_continue ?? true)}</p>
    <p class="review-label">High-priority Issue Resolution</p>${renderMiniList(issueRows, "暂无 high-priority issue")}
    <p class="review-label">Quick Fix Execution</p>${renderMiniList(fixRows, "暂无 quick fix result")}
    <p class="review-label">Queue Readiness Repair</p>${renderMiniList(queueRows, "暂无 queue repair")}
    <p class="review-label">Calendar Readiness Calibration</p>${renderMiniList(calendarRows, "暂无 calendar calibration")}
    <p class="review-label">Issue Resolution Verification</p>${renderMiniList(verificationRows, "暂无 verification")}
    <p class="review-label">Stable Trial Readiness Gate</p>${renderMiniList(criterionRows, "暂无 gate criteria")}
    <p class="review-label">Needs manual / unresolved</p>${renderMiniList(manualRows.concat(unresolvedRows).slice(0, 8), "暂无 manual 或 unresolved item")}
    <p class="review-label">Next operator actions</p>${renderMiniList(nextActions, "暂无 next action")}
    <p class="review-label">Boundary</p>
    <p class="review-value">sidecar_only=${escapeHtml(policy.sidecar_only ?? true)} · no_auto_publish=${escapeHtml(policy.no_auto_publish ?? true)} · no_wechat_api=${escapeHtml(policy.no_wechat_api ?? true)} · no_auto_image_generation=${escapeHtml(policy.no_auto_image_generation ?? true)} · no_config_prompt_rule_changes=${escapeHtml(policy.no_config_prompt_rule_changes ?? true)}</p>
  </div>`;
}

function renderStableWorkbenchBaseline(cardClass = "review-card wide") {
  const panel = getPhase25Panel();
  const baselineSummary = panel.baseline_summary || {};
  const acceptanceSummary = panel.operator_acceptance_summary || {};
  const dailySummary = panel.stable_daily_ops_summary || {};
  const quality = panel.content_quality_status || {};
  const policy = panel.policy || {};
  const flow = Array.isArray(panel.recommended_operator_flow) ? panel.recommended_operator_flow : [];
  const warnings = Array.isArray(panel.acceptable_warnings) ? panel.acceptable_warnings : [];
  const blockers = Array.isArray(panel.true_blockers) ? panel.true_blockers : [];
  const manual = Array.isArray(panel.manual_required_items) ? panel.manual_required_items : [];
  const warnChecks = Array.isArray(panel.acceptance_warn_checks) ? panel.acceptance_warn_checks : [];
  const failChecks = Array.isArray(panel.acceptance_fail_checks) ? panel.acceptance_fail_checks : [];
  const limitations = Array.isArray(panel.known_limitations) ? panel.known_limitations : [];
  const nextPhase = Array.isArray(panel.next_phase_recommendations) ? panel.next_phase_recommendations : [];
  const hasPanel = panel.baseline_status && panel.baseline_status !== "UNKNOWN";
  if (!hasPanel) {
    return `<div class="${cardClass} stable-workbench-baseline">
      <p class="review-label">Stable Workbench Baseline</p>
      <p class="review-value">暂无 Phase25 baseline。运行 <code>make stable-daily-ops</code> 后会显示 stable daily ops、operator acceptance 和 Content Factory v1 closeout。</p>
    </div>`;
  }
  const flowRows = flow.slice(0, 5).map((item) => `${item.step}. ${item.name}: ${item.command} / ${item.operator_decision}`);
  const manualRows = manual.slice(0, 6).map((item) => `${item.area}: ${item.count} / ${item.operator_action}`);
  const checkRows = warnChecks.concat(failChecks).slice(0, 8).map((item) => `${item.status}: ${item.check_id} / ${item.operator_note}`);
  return `<div class="${cardClass} stable-workbench-baseline">
    <p class="review-label">Stable Workbench Baseline</p>
    <p class="review-value">Command <code>${escapeHtml(panel.daily_command || "make stable-daily-ops")}</code> · Stable daily ops ${escapeHtml(panel.stable_daily_ops_status || "UNKNOWN")} · Phase25 ${escapeHtml(panel.phase25_status || "UNKNOWN")}</p>
    <p class="review-value">Baseline ${escapeHtml(panel.baseline_status || "UNKNOWN")} · Acceptance ${escapeHtml(panel.operator_acceptance_status || "UNKNOWN")} · v1 ${escapeHtml(panel.v1_status || "UNKNOWN")}</p>
    <p class="review-value">Blocking ${escapeHtml(baselineSummary.blocking_issue_count ?? 0)} · can run daily ${escapeHtml(baselineSummary.can_run_daily ?? false)} · workbench ready ${escapeHtml(dailySummary.workbench_ready ?? false)} · manual review ${escapeHtml(acceptanceSummary.manual_review_required ?? true)}</p>
    <p class="review-label">Content inventory status</p>
    <p class="review-value">ready_to_publish ${escapeHtml(quality.ready_to_publish ?? 0)} · ready_for_review ${escapeHtml(quality.ready_for_review ?? 0)} · quality issues ${escapeHtml(quality.quality_issues ?? 0)} · publish blockers ${escapeHtml(quality.publish_blocking_quality_issues ?? 0)}</p>
    <p class="review-value">${escapeHtml(quality.interpretation || "Daily ops readiness does not mean content is ready to publish.")}</p>
    <p class="review-label">Recommended operator flow</p>${renderMiniList(flowRows, "暂无 operator flow")}
    <p class="review-label">Manual required items</p>${renderMiniList(manualRows, "暂无 manual item")}
    <p class="review-label">Acceptance warnings / failures</p>${renderMiniList(checkRows, "暂无 WARN/FAIL acceptance check")}
    <p class="review-label">Acceptable warnings</p>${renderMiniList(warnings.slice(0, 5), "暂无 acceptable warning")}
    <p class="review-label">True blockers</p>${renderMiniList(blockers, "暂无 true blocker")}
    <p class="review-label">Content Factory v1 limitations</p>${renderMiniList(limitations.slice(0, 5), "暂无 known limitation")}
    <p class="review-label">Next phase</p>${renderMiniList(nextPhase.slice(0, 6), "暂无 next phase recommendation")}
    <p class="review-label">Boundary</p>
    <p class="review-value">manual_ops_only=${escapeHtml(policy.manual_ops_only ?? true)} · no_auto_publish=${escapeHtml(policy.no_auto_publish ?? true)} · no_wechat_api=${escapeHtml(policy.no_wechat_api ?? true)} · no_auto_image_generation=${escapeHtml(policy.no_auto_image_generation ?? true)} · no_config_prompt_rule_changes=${escapeHtml(policy.no_config_prompt_rule_changes ?? true)}</p>
  </div>`;
}

function renderHotMaterialPanel(cardClass = "review-card wide") {
  const panel = getHotMaterialPanel();
  const materialSummary = panel.material_summary || {};
  const gateSummary = panel.quality_gate_summary || {};
  const signalSummary = panel.hot_signal_summary || {};
  const backfillSummary = panel.backfill_summary || {};
  const gapSummary = panel.gap_summary || {};
  const policy = panel.policy || {};
  const weakReasons = Array.isArray(panel.weak_supply_reasons) ? panel.weak_supply_reasons : [];
  const emptyLanes = Array.isArray(panel.empty_lanes) ? panel.empty_lanes : [];
  const materials = Array.isArray(panel.materials) ? panel.materials : [];
  const gateItems = Array.isArray(panel.gate_items) ? panel.gate_items : [];
  const tasks = Array.isArray(panel.top_backfill_tasks) ? panel.top_backfill_tasks : [];
  const hasPanel = panel.gate_status && panel.gate_status !== "UNKNOWN";
  if (!hasPanel) {
    return `<div class="${cardClass} hot-material-panel">
      <p class="review-label">Hot Material Panel</p>
      <p class="review-value">暂无 Phase26 上游素材数据。运行 <code>make phase26-daily</code> 后会显示 Source Coverage Gap Audit、Hot Signal Capture、Fallback Backfill Queue、Daily Hot Material Pool 和 Hot Material Quality Gate。</p>
    </div>`;
  }
  const materialRows = materials.slice(0, 8).map((item) => `${item.recommended_use}: ${item.lane_id} / ${item.evidence_strength} / ${item.title}`);
  const gateRows = gateItems.slice(0, 8).map((item) => `${item.gate_decision}: ${item.lane_id} / score ${item.quality_score} / ${item.required_next_action}`);
  const taskRows = tasks.slice(0, 8).map((item) => `${item.priority}: ${item.lane_id} / ${item.suggested_method} / ${item.suggested_query}`);
  const laneRows = emptyLanes.slice(0, 8).map((item) => `${item.status}: ${item.lane_id} / ${item.recommended_backfill || ""}`);
  return `<div class="${cardClass} hot-material-panel">
    <p class="review-label">Hot Material Panel</p>
    <p class="review-value">gate_status ${escapeHtml(panel.gate_status || "UNKNOWN")} · Phase26 ${escapeHtml(panel.phase26_status || "UNKNOWN")} · materials ${escapeHtml(materialSummary.material_count ?? 0)} · promote ${escapeHtml(gateSummary.promote_to_topic_pipeline ?? 0)} · backfill ${escapeHtml(gateSummary.backfill_required ?? 0)}</p>
    <p class="review-value">write_now ${escapeHtml(materialSummary.write_now ?? 0)} · develop_topic ${escapeHtml(materialSummary.develop_topic ?? 0)} · watch ${escapeHtml(materialSummary.watch ?? 0)} · backfill_first ${escapeHtml(materialSummary.backfill_first ?? 0)} · hold ${escapeHtml(materialSummary.hold ?? 0)}</p>
    <p class="review-value">signals ${escapeHtml(signalSummary.hot_signal_count ?? 0)} · active lanes ${escapeHtml(signalSummary.active_lanes ?? 0)} · backfill tasks ${escapeHtml(backfillSummary.task_count ?? 0)} · source gaps ${escapeHtml(gapSummary.gap_count ?? 0)} / high ${escapeHtml(gapSummary.high_severity ?? 0)}</p>
    <p class="review-label">weak_supply_reasons</p>${renderMiniList(weakReasons, "暂无 weak supply reason")}
    <p class="review-label">Daily Hot Material Pool</p>${renderMiniList(materialRows, "暂无 daily hot material")}
    <p class="review-label">Hot Material Quality Gate</p>${renderMiniList(gateRows, "暂无 gate item")}
    <p class="review-label">Fallback Backfill Queue</p>${renderMiniList(taskRows, "暂无 backfill task")}
    <p class="review-label">Empty / weak lanes</p>${renderMiniList(laneRows, "暂无 empty lane")}
    <p class="review-label">Boundary</p>
    <p class="review-value">diagnosis_and_scheduling_only=${escapeHtml(policy.diagnosis_and_scheduling_only ?? true)} · no_auto_publish=${escapeHtml(policy.no_auto_publish ?? true)} · no_wechat_api=${escapeHtml(policy.no_wechat_api ?? true)} · no_auto_image_generation=${escapeHtml(policy.no_auto_image_generation ?? true)} · no_sources_yaml_mutation=${escapeHtml(policy.no_sources_yaml_mutation ?? true)}</p>
  </div>`;
}

function renderConnectorHealthPanel(cardClass = "review-card wide") {
  const panel = getConnectorHealthPanel();
  const selection = panel.selection_summary || {};
  const rss = panel.rss_summary || {};
  const research = panel.research_summary || {};
  const manual = panel.manual_summary || {};
  const normalized = panel.normalized_summary || {};
  const health = panel.health_summary || {};
  const contribution = panel.connector_contribution || {};
  const policy = panel.policy || {};
  const connectors = Array.isArray(panel.connector_health) ? panel.connector_health : [];
  const checks = Array.isArray(panel.health_checks) ? panel.health_checks : [];
  const sources = Array.isArray(panel.selected_sources) ? panel.selected_sources : [];
  const normalizedItems = Array.isArray(panel.normalized_items) ? panel.normalized_items : [];
  const hasPanel = panel.gate_status && panel.gate_status !== "UNKNOWN";
  if (!hasPanel) {
    return `<div class="${cardClass} connector-health-panel">
      <p class="review-label">Connector Health Panel</p>
      <p class="review-value">暂无 Phase27 connector 数据。运行 <code>make phase27-daily</code> 后会显示 P0 source selection、connector run、normalized upstream items 和 source health gate。</p>
    </div>`;
  }
  const connectorRows = connectors.slice(0, 8).map((item) => `${item.connector_type}: ${item.status} / items ${item.item_count ?? 0}${item.issue ? ` / ${item.issue}` : ""}`);
  const checkRows = checks.slice(0, 8).map((item) => `${item.status}: ${item.check_id} / ${item.message || ""}`);
  const sourceRows = sources.slice(0, 8).map((item) => `${item.implementation_status}: ${item.source_name} / ${item.connector_type}`);
  const itemRows = normalizedItems.slice(0, 8).map((item) => `${item.source_type}: ${item.lane_id} / ${item.title}`);
  return `<div class="${cardClass} connector-health-panel">
    <p class="review-label">Connector Health Panel</p>
    <p class="review-value">gate_status ${escapeHtml(panel.gate_status || "UNKNOWN")} · Phase27 ${escapeHtml(panel.phase27_status || "UNKNOWN")} · selected ${escapeHtml(selection.selected_count ?? 0)} · normalized ${escapeHtml(normalized.item_count ?? 0)} · candidates ${escapeHtml(normalized.candidate_for_hot_material_pool ?? 0)}</p>
    <p class="review-value">RSS items ${escapeHtml(rss.item_count ?? 0)} · research items ${escapeHtml(research.item_count ?? 0)} · manual ready ${escapeHtml(manual.ready_for_review ?? 0)} · connector material ${escapeHtml(contribution.connector_item_count ?? 0)} · connector promote candidates ${escapeHtml(contribution.connector_promote_candidates ?? 0)}</p>
    <p class="review-value">healthy ${escapeHtml(health.healthy_connectors ?? 0)} · weak ${escapeHtml(health.weak_connectors ?? 0)} · failed ${escapeHtml(health.failed_connectors ?? 0)} · metadata ${escapeHtml((panel.metadata_check || {}).status || "UNKNOWN")} · copyright ${escapeHtml((panel.copyright_check || {}).status || "UNKNOWN")}</p>
    <p class="review-label">P0 source selection</p>${renderMiniList(sourceRows, "暂无 P0 selected source")}
    <p class="review-label">Connector health</p>${renderMiniList(connectorRows, "暂无 connector health")}
    <p class="review-label">Health gate checks</p>${renderMiniList(checkRows, "暂无 health check")}
    <p class="review-label">Normalized upstream items</p>${renderMiniList(itemRows, "暂无 normalized upstream item")}
    <p class="review-label">Boundary</p>
    <p class="review-value">metadata_only=${escapeHtml(policy.metadata_only ?? true)} · copyright_safe=${escapeHtml(policy.copyright_safe ?? true)} · no_full_text=${escapeHtml(policy.no_full_text ?? true)} · no_login_or_paywall_bypass=${escapeHtml(policy.no_login_or_paywall_bypass ?? true)} · manual_url_not_auto_fetched=${escapeHtml(policy.manual_url_not_auto_fetched ?? true)}</p>
  </div>`;
}

function renderEvidenceTopicPromotionPanel(cardClass = "review-card wide") {
  const panel = getEvidenceTopicPromotionPanel();
  const reliability = panel.reliability_summary || {};
  const evidence = panel.evidence_summary || {};
  const promoted = panel.promoted_topic_summary || {};
  const freshness = panel.freshness_summary || {};
  const dedup = panel.dedup_summary || {};
  const bridge = panel.bridge_summary || {};
  const policy = panel.policy || {};
  const packets = Array.isArray(panel.evidence_packets) ? panel.evidence_packets : [];
  const candidates = Array.isArray(panel.topic_candidates) ? panel.topic_candidates : [];
  const bridgeItems = Array.isArray(panel.bridge_items) ? panel.bridge_items : [];
  const checks = Array.isArray(panel.regression_checks) ? panel.regression_checks : [];
  const hasPanel = Object.keys(evidence).length || Object.keys(promoted).length || Object.keys(bridge).length;
  if (!hasPanel) {
    return `<div class="${cardClass} evidence-topic-promotion-panel">
      <p class="review-label">Evidence / Topic Promotion</p>
      <p class="review-value">暂无 Phase28 enrichment 数据。运行 <code>make phase28-daily</code> 后会显示 connector evidence packets、promoted topic candidates、freshness/dedup regression 和 acquisition-to-content bridge。</p>
    </div>`;
  }
  const evidenceRows = packets.slice(0, 8).map((item) => `${item.evidence_strength}: ${item.source_type} / ${item.source_origin || "phase27_connector"} / weak=${item.weak_signal_lane ?? false} / ${item.title}`);
  const candidateRows = candidates.slice(0, 8).map((item) => `${item.promotion_status}: ${item.evidence_strength} / ${item.source_origin || "phase27_connector"} / weak=${item.weak_signal_lane ?? false} / ${item.title}`);
  const bridgeRows = bridgeItems.slice(0, 8).map((item) => `${item.bridge_status}: ${item.recommended_pipeline_step} / ${item.operator_action}`);
  const checkRows = checks.slice(0, 8).map((item) => `${item.status}: ${item.check_id} / ${item.message || ""}`);
  return `<div class="${cardClass} evidence-topic-promotion-panel">
    <p class="review-label">Evidence / Topic Promotion Panel</p>
    <p class="review-value">Phase28 ${escapeHtml(panel.phase28_status || "UNKNOWN")} · reliability issues ${escapeHtml(reliability.issue_count ?? 0)} · regression ${escapeHtml(panel.regression_status || "UNKNOWN")}</p>
    <p class="review-value">Evidence packets ${escapeHtml(evidence.packet_count ?? 0)} · eligible ${escapeHtml(evidence.eligible_for_topic_promotion ?? 0)} · high ${escapeHtml(evidence.high_strength ?? 0)} · medium ${escapeHtml(evidence.medium_strength ?? 0)} · low ${escapeHtml(evidence.low_strength ?? 0)}</p>
    <p class="review-value">Promoted topics ${escapeHtml(promoted.promoted ?? 0)} · needs evidence ${escapeHtml(promoted.needs_evidence ?? 0)} · watch ${escapeHtml(promoted.watch ?? 0)} · ready for brief ${escapeHtml(bridge.ready_for_brief ?? 0)} · bridge needs evidence ${escapeHtml(bridge.needs_evidence ?? 0)}</p>
    <p class="review-value">Freshness today ${escapeHtml(freshness.today ?? 0)} · this week ${escapeHtml(freshness.this_week ?? 0)} · stale ${escapeHtml(freshness.stale ?? 0)} · unknown ${escapeHtml(freshness.unknown ?? 0)} · duplicate ratio ${escapeHtml(dedup.duplicate_ratio ?? 0)}</p>
    <p class="review-label">Connector Evidence Packets</p>${renderMiniList(evidenceRows, "暂无 evidence packet")}
    <p class="review-label">Promoted Topic Candidates</p>${renderMiniList(candidateRows, "暂无 promoted topic candidate")}
    <p class="review-label">Acquisition-to-Content Bridge</p>${renderMiniList(bridgeRows, "暂无 bridge item")}
    <p class="review-label">Freshness / Dedup Checks</p>${renderMiniList(checkRows, "暂无 regression check")}
    <p class="review-label">Boundary</p>
    <p class="review-value">metadata_derived_evidence_only=${escapeHtml(policy.metadata_derived_evidence_only ?? true)} · no_full_text=${escapeHtml(policy.no_full_text ?? true)} · no_auto_publish=${escapeHtml(policy.no_auto_publish ?? true)} · no_openclaw_migration=${escapeHtml(policy.no_openclaw_migration ?? true)}</p>
  </div>`;
}

function renderOpenClawMigrationPanel(cardClass = "review-card wide") {
  const panel = getOpenClawMigrationPanel();
  const inventory = panel.inventory_summary || {};
  const risk = panel.risk_summary || {};
  const plan = panel.migration_plan_summary || {};
  const connectors = panel.metadata_connector_summary || {};
  const weak = panel.weak_signal_summary || {};
  const normalized = panel.normalized_summary || {};
  const hot = panel.hot_material_summary || {};
  const policy = panel.policy || {};
  const sources = Array.isArray(panel.sources) ? panel.sources : [];
  const candidates = Array.isArray(panel.migration_candidates) ? panel.migration_candidates : [];
  const weakItems = Array.isArray(panel.weak_signal_items) ? panel.weak_signal_items : [];
  const signals = Array.isArray(panel.normalized_signals) ? panel.normalized_signals : [];
  const hasPanel = Object.keys(inventory).length || Object.keys(plan).length || Object.keys(connectors).length;
  if (!hasPanel) {
    return `<div class="${cardClass} openclaw-migration-panel">
      <p class="review-label">OpenClaw Source Migration</p>
      <p class="review-value">暂无 Phase29 OpenClaw migration 数据。运行 <code>make phase29-daily</code> 后会显示 source inventory、risk classification、migration plan、weak signal gate 和 normalized signals。</p>
    </div>`;
  }
  const sourceRows = sources.slice(0, 8).map((item) => `${item.source_type}: ${item.source_name} / lane ${item.lane_hint} / enabled jobs ${item.enabled_job_count ?? 0}`);
  const candidateRows = candidates.slice(0, 8).map((item) => `${item.migration_priority}: ${item.connector_type} / ${item.evidence_role} / ${item.source_name}`);
  const weakRows = weakItems.slice(0, 8).map((item) => `${item.safety_decision}: hard=${item.can_use_as_hard_evidence} / ${item.source_name}`);
  const signalRows = signals.slice(0, 8).map((item) => `${item.evidence_role}: candidate=${item.candidate_for_hot_material_pool} / hard=${item.can_use_as_hard_evidence} / ${item.source_name || item.title}`);
  return `<div class="${cardClass} openclaw-migration-panel">
    <p class="review-label">OpenClaw Source Migration Panel</p>
    <p class="review-value">Phase29 ${escapeHtml(panel.phase29_status || "UNKNOWN")} · OpenClaw available ${escapeHtml(panel.openclaw_available ?? false)} · gateway detected ${escapeHtml(panel.gateway_detected ?? false)} · sources ${escapeHtml(inventory.source_count ?? 0)} · jobs ${escapeHtml(inventory.job_count ?? 0)}</p>
    <p class="review-value">P0 ${escapeHtml(plan.p0 ?? 0)} · P1 ${escapeHtml(plan.p1 ?? 0)} · candidates ${escapeHtml(plan.candidate_count ?? 0)} · metadata items ${escapeHtml(connectors.item_count ?? 0)} · weak items ${escapeHtml(connectors.weak_signal_items ?? 0)}</p>
    <p class="review-value">blocked ${escapeHtml(risk.blocked ?? 0)} · manual backfill ${escapeHtml(risk.manual_backfill ?? 0)} · weak signal ${escapeHtml(risk.weak_signal ?? 0)} · hard evidence allowed ${escapeHtml(weak.hard_evidence_allowed ?? 0)}</p>
    <p class="review-value">normalized signals ${escapeHtml(normalized.signal_count ?? 0)} · hot materials ${escapeHtml(hot.openclaw_hot_material_count ?? 0)} · weak material ${escapeHtml(hot.weak_signal_material_count ?? 0)} · needs confirmation ${escapeHtml(weak.require_confirmation ?? 0)}</p>
    <p class="review-label">Source inventory</p>${renderMiniList(sourceRows, "暂无 OpenClaw source inventory")}
    <p class="review-label">P0/P1 migration candidates</p>${renderMiniList(candidateRows, "暂无 migration candidate")}
    <p class="review-label">Weak signal safety gate</p>${renderMiniList(weakRows, "暂无 weak signal item")}
    <p class="review-label">Normalized OpenClaw signals</p>${renderMiniList(signalRows, "暂无 normalized OpenClaw signal")}
    <p class="review-label">Boundary</p>
    <p class="review-value">metadata_only=${escapeHtml(policy.metadata_only ?? true)} · weak_signals_not_hard_evidence=${escapeHtml(policy.weak_signals_not_hard_evidence ?? true)} · no_openclaw_gateway=${escapeHtml(policy.no_openclaw_gateway ?? true)} · no_openclaw_cron_migration=${escapeHtml(policy.no_openclaw_cron_migration ?? true)} · no_full_text=${escapeHtml(policy.no_full_text ?? true)}</p>
  </div>`;
}

function renderOpenClawActivationPanel(cardClass = "review-card wide") {
  const panel = getOpenClawActivationPanel();
  const backfill = panel.backfill_summary || {};
  const confirmation = panel.confirmation_summary || {};
  const activation = panel.activation_summary || {};
  const regression = panel.regression_summary || {};
  const registry = panel.registry_summary || {};
  const policy = panel.policy || {};
  const backfillItems = Array.isArray(panel.backfill_items) ? panel.backfill_items : [];
  const confirmationItems = Array.isArray(panel.confirmation_items) ? panel.confirmation_items : [];
  const topics = Array.isArray(panel.topic_candidates) ? panel.topic_candidates : [];
  const checks = Array.isArray(panel.regression_checks) ? panel.regression_checks : [];
  const proposals = Array.isArray(panel.registry_proposal_items) ? panel.registry_proposal_items : [];
  const hasPanel = Object.keys(backfill).length || Object.keys(confirmation).length || Object.keys(activation).length;
  if (!hasPanel) {
    return `<div class="${cardClass} openclaw-activation-panel">
      <p class="review-label">OpenClaw Evidence / Topic Activation</p>
      <p class="review-value">暂无 Phase30 OpenClaw activation 数据。运行 <code>make phase30-daily</code> 后会显示 evidence backfill、weak signal confirmation、topic activation、regression gate 和 source registry proposal。</p>
    </div>`;
  }
  const backfillRows = backfillItems.slice(0, 8).map((item) => `${item.backfill_status}: ${item.evidence_role} / hard=${item.can_use_as_hard_evidence} / ${item.title}`);
  const confirmationRows = confirmationItems.slice(0, 8).map((item) => `${item.confirmation_status}: promote=${item.can_promote_to_topic} / ${item.required_source_type} / ${item.title}`);
  const topicRows = topics.slice(0, 8).map((item) => `${item.activation_status}: brief=${item.can_enter_brief_pipeline} / ${item.evidence_strength} / ${item.title}`);
  const checkRows = checks.slice(0, 8).map((item) => `${item.status}: ${item.check_id} / ${item.message || ""}`);
  const proposalRows = proposals.slice(0, 8).map((item) => `${item.recommended_registry_action}: ${item.risk_level} / auto=${item.auto_apply} / ${item.source_name}`);
  return `<div class="${cardClass} openclaw-activation-panel">
    <p class="review-label">OpenClaw Evidence / Topic Panel</p>
    <p class="review-value">Phase30 ${escapeHtml(panel.phase30_status || "UNKNOWN")} · regression ${escapeHtml(panel.regression_gate_status || "UNKNOWN")} · blocking ${escapeHtml(regression.blocking_failures ?? 0)} · registry proposals ${escapeHtml(registry.proposal_count ?? 0)}</p>
    <p class="review-value">Backfill ${escapeHtml(backfill.backfill_count ?? 0)} · ready confirmation ${escapeHtml(backfill.ready_for_confirmation ?? 0)} · needs primary ${escapeHtml(confirmation.needs_primary_source ?? 0)} · needs second ${escapeHtml(confirmation.needs_second_source ?? 0)} · manual review ${escapeHtml(confirmation.manual_review ?? 0)}</p>
    <p class="review-value">Activated topics ${escapeHtml(activation.activated ?? 0)} · needs evidence ${escapeHtml(activation.needs_evidence ?? 0)} · watch ${escapeHtml(activation.watch ?? 0)} · can enter brief ${escapeHtml(activation.can_enter_brief_pipeline ?? 0)}</p>
    <p class="review-label">Evidence Backfill</p>${renderMiniList(backfillRows, "暂无 OpenClaw evidence backfill item")}
    <p class="review-label">Confirmation Workflow</p>${renderMiniList(confirmationRows, "暂无 confirmation item")}
    <p class="review-label">Activated Topic Candidates</p>${renderMiniList(topicRows, "暂无 activated topic candidate")}
    <p class="review-label">Regression Gate</p>${renderMiniList(checkRows, "暂无 regression check")}
    <p class="review-label">Source Registry Proposal</p>${renderMiniList(proposalRows, "暂无 registry proposal")}
    <p class="review-label">Boundary</p>
    <p class="review-value">weak_signals_not_hard_evidence=${escapeHtml(policy.weak_signals_not_hard_evidence ?? true)} · no_full_text=${escapeHtml(policy.no_full_text ?? true)} · no_openclaw_gateway=${escapeHtml(policy.no_openclaw_gateway ?? true)} · no_openclaw_cron_migration=${escapeHtml(policy.no_openclaw_cron_migration ?? true)} · no_sources_yaml_mutation=${escapeHtml(policy.no_sources_yaml_mutation ?? true)}</p>
  </div>`;
}

function runtimeCommand(kind) {
  if (kind === "run") return "curl -X POST http://127.0.0.1:8766/runtime/run-daily";
  if (kind === "validation") return "curl -X POST http://127.0.0.1:8766/runtime/run-validation";
  if (kind === "retry") return "curl -X POST http://127.0.0.1:8766/runtime/retry-failed";
  if (kind === "pause") return "curl -X POST http://127.0.0.1:8766/runtime/pause";
  if (kind === "resume") return "curl -X POST http://127.0.0.1:8766/runtime/resume";
  return "curl http://127.0.0.1:8766/runtime/status";
}

function renderRuntimeControlCenterPanel(cardClass = "review-card wide") {
  const panel = getRuntimeControlCenterPanel();
  const ledger = panel.ledger_summary || {};
  const retry = panel.retry_summary || {};
  const missed = panel.missed_run_summary || {};
  const network = panel.network_readiness || {};
  const route = panel.acquisition_route_summary || {};
  const graph = panel.daily_pipeline_graph_summary || {};
  const e2e = panel.daily_end_to_end_summary || {};
  const dryRun = panel.autonomous_dry_run_summary || {};
  const coexistence = panel.openclaw_coexistence_summary || {};
  const conflictPlan = panel.phase31b_conflict_plan_summary || {};
  const trigger = panel.last_automatic_trigger || {};
  const missedLive = panel.phase31b_missed_live_summary || {};
  const idempotencyLive = panel.phase31b_idempotency_summary || {};
  const observation = panel.phase31b_observation_summary || {};
  const acceptance = panel.phase31b_acceptance_summary || {};
  const costGuard = panel.cost_guard_state || {};
  const policy = panel.policy || {};
  const recentRuns = Array.isArray(panel.recent_job_runs) ? panel.recent_job_runs : [];
  const retryItems = Array.isArray(panel.retry_items) ? panel.retry_items : [];
  const catchup = Array.isArray(panel.catchup_plan) ? panel.catchup_plan : [];
  const routes = Array.isArray(panel.routes) ? panel.routes : [];
  const hasPanel = Object.keys(ledger).length || Object.keys(dryRun).length || panel.runtime_status;
  if (!hasPanel || panel.runtime_status === "UNKNOWN") {
    return `<div class="${cardClass} runtime-control-panel">
      <p class="review-label">Autonomous Runtime Control Center</p>
      <p class="review-value">暂无 Runtime 数据。运行 <code>make autonomous-runtime-dry-run</code> 或 <code>make scheduler-once</code> 后会显示心跳、任务账本、retry queue、missed-run 和网络路由。</p>
    </div>`;
  }
  const runRows = recentRuns.slice(0, 8).map((item) => `${item.status}: ${item.job_id} / ${item.schedule_slot || "-"} / attempts ${item.attempt_count ?? 0}`);
  const retryRows = retryItems.slice(0, 8).map((item) => `${item.error_class}: ${item.job_id} / next ${item.next_retry_at || "-"}`);
  const catchupRows = catchup.slice(0, 8).map((item) => `${item.action}: ${item.source_slots || []} / ${item.reason}`);
  const routeRows = routes.slice(0, 8).map((item) => `${item.lane}: ${item.action} / ${item.reason}`);
  return `<div class="${cardClass} runtime-control-panel">
    <p class="review-label">Autonomous Runtime Control Center</p>
    <p class="review-value">LaunchAgent installed ${escapeHtml(panel.launchagent_installed ?? false)} · loaded ${escapeHtml(panel.launchagent_loaded ?? false)} · enabled ${escapeHtml(panel.launchagent_enabled ?? false)} · gate ${escapeHtml(panel.phase31b_acceptance_gate_status || "UNKNOWN")}</p>
    <p class="review-value">Runtime ${escapeHtml(panel.runtime_status || "UNKNOWN")} · PID ${escapeHtml(panel.runtime_pid || 0)} · heartbeat age ${escapeHtml(panel.heartbeat_age_seconds || "-")}s · current job ${escapeHtml(panel.current_job_id || "-")} · next ${escapeHtml(panel.next_scheduled_run || "-")}</p>
    <p class="review-value">Today jobs success ${escapeHtml(ledger.success ?? 0)} · failed ${escapeHtml(ledger.failed ?? 0)} · pending ${escapeHtml(ledger.pending ?? 0)} · retry ${escapeHtml(retry.retry_count ?? 0)} · missed ${escapeHtml(missed.missed_count ?? 0)}</p>
    <p class="review-value">Network ${escapeHtml(network.status || "UNKNOWN")} · routes run now ${escapeHtml(route.run_now ?? 0)} · delayed ${escapeHtml(route.delay_retry ?? 0)} · pipeline nodes ${escapeHtml(graph.node_count ?? 0)} · E2E ${escapeHtml(panel.daily_end_to_end_status || "UNKNOWN")}</p>
    <p class="review-value">Trigger ${escapeHtml(panel.phase31b_live_trigger_status || "UNKNOWN")} · source ${escapeHtml(trigger.status || "-")} · missed live pass ${escapeHtml(missedLive.pass ?? 0)} · idempotency skipped ${escapeHtml(idempotencyLive.duplicate_skipped ?? 0)} · OpenClaw conflicts ${escapeHtml(coexistence.conflict_count ?? 0)} / manual ${escapeHtml(conflictPlan.manual_review ?? 0)}</p>
    <p class="review-value">Observation cost ${escapeHtml(costGuard.estimated_cost ?? observation.estimated_cost ?? 0)} · retries ${escapeHtml(observation.retry_count ?? 0)} · auto publish ${escapeHtml(observation.auto_publish_attempts ?? 0)} · image gen ${escapeHtml(observation.image_generation_attempts ?? 0)} · secret exposure ${escapeHtml(observation.secret_exposure_count ?? 0)} · gate blocking ${escapeHtml(acceptance.blocking_failures ?? 0)}</p>
    <p class="review-value">Dry-run ${escapeHtml(panel.autonomous_dry_run_status || "UNKNOWN")} · steps ${escapeHtml(dryRun.step_count ?? 0)} · warnings ${escapeHtml(dryRun.warnings ?? 0)} · failures ${escapeHtml(dryRun.failures ?? 0)} · Workbench updated ${escapeHtml(panel.latest_workbench_generation_time || "-")}</p>
    <div class="version-actions">
      <button class="copy-review-command" type="button" data-command="${escapeHtml(runtimeCommand("run"))}">立即运行今日主链路</button>
      <button class="copy-review-command" type="button" data-command="${escapeHtml(runtimeCommand("validation"))}">运行安全验证任务</button>
      <button class="copy-review-command" type="button" data-command="${escapeHtml(runtimeCommand("retry"))}">重试失败任务</button>
      <button class="copy-review-command" type="button" data-command="${escapeHtml(runtimeCommand("pause"))}">暂停调度</button>
      <button class="copy-review-command" type="button" data-command="${escapeHtml(runtimeCommand("resume"))}">恢复调度</button>
      <button class="copy-review-command" type="button" data-command="${escapeHtml(runtimeCommand("status"))}">刷新状态</button>
    </div>
    <p class="review-label">Recent Job Runs</p>${renderMiniList(runRows, "暂无 job run")}
    <p class="review-label">Retry Queue</p>${renderMiniList(retryRows, "暂无 retry item")}
    <p class="review-label">Missed-run / Catch-up</p>${renderMiniList(catchupRows, "暂无 catch-up plan")}
    <p class="review-label">Network Routes</p>${renderMiniList(routeRows, "暂无 route")}
    <p class="review-label">Boundary</p>
    <p class="review-value">local_control_only=${escapeHtml(policy.local_control_only ?? true)} · no_auto_publish_button=${escapeHtml(policy.no_auto_publish_button ?? true)} · respect_idempotency=${escapeHtml(policy.respect_idempotency ?? true)} · respect_cost_and_safety_gate=${escapeHtml(policy.respect_cost_and_safety_gate ?? true)}</p>
  </div>`;
}

function renderAcquisitionPlaybookPanel(cardClass = "review-card wide") {
  const panel = getAcquisitionPlaybookPanel();
  const semantics = panel.semantics_summary || {};
  const lanes = panel.lane_summary || {};
  const cadence = panel.cadence_summary || {};
  const sources = panel.source_summary || {};
  const queries = panel.query_summary || {};
  const fallback = panel.fallback_summary || {};
  const runtimePlan = panel.runtime_plan_summary || {};
  const coverage = panel.regression_coverage || {};
  const duplicates = panel.regression_duplicates || {};
  const dryRun = panel.dry_run_summary || {};
  const policy = panel.policy || {};
  const laneCards = Array.isArray(panel.lane_cards) ? panel.lane_cards : [];
  const groupedRuns = Array.isArray(panel.grouped_runs) ? panel.grouped_runs : [];
  const connectorRuns = Array.isArray(panel.connector_runs) ? panel.connector_runs : [];
  const checks = Array.isArray(panel.checks) ? panel.checks : [];
  const hasPanel = Object.keys(cadence).length || Object.keys(runtimePlan).length || Object.keys(semantics).length;
  if (!hasPanel) {
    return `<div class="${cardClass} acquisition-playbook-panel">
      <p class="review-label">Acquisition Playbook</p>
      <p class="review-value">暂无 Phase31C acquisition playbook 数据。运行 <code>make autonomous-acquisition-dry-run</code> 后会显示 lane、cadence、source playbook、fallback、downstream route 和 runtime plan。</p>
    </div>`;
  }
  const laneRows = laneCards.slice(0, 12).map((item) => `${item.time}: ${item.lane} / ${item.next_action} / sources ${item.source_count ?? 0} / lookback ${item.lookback_hours ?? 0}h / ${item.network_requirement || "mixed"} / ${Array.isArray(item.downstream_outputs) ? item.downstream_outputs.slice(0, 3).join(", ") : ""}`);
  const groupRows = groupedRuns.slice(0, 8).map((item) => `${item.group_key}: lanes ${(item.lanes || []).join(", ")} / connector runs ${item.connector_run_count ?? 0}`);
  const connectorRows = connectorRuns.slice(0, 8).map((item) => `${item.group_key}: ${item.fetch_method} / ${item.source_id} / lane ${item.lane}`);
  const checkRows = checks.slice(0, 8).map((item) => `${item.status}: ${item.check_id} / ${item.message || ""}`);
  return `<div class="${cardClass} acquisition-playbook-panel">
    <p class="review-label">Acquisition Playbook</p>
    <p class="review-value">Audit jobs ${escapeHtml(semantics.acquisition_job_count ?? 0)} · high value ${escapeHtml(semantics.high_value_playbook_jobs ?? 0)} · lanes ${escapeHtml(lanes.lane_count ?? 0)} · weak lanes ${escapeHtml(lanes.weak_signal_lane_count ?? 0)} · schedule slots ${escapeHtml(cadence.schedule_slot_count ?? 0)}</p>
    <p class="review-value">Sources ${escapeHtml(sources.source_count ?? 0)} · metadata ${escapeHtml(sources.metadata_sources ?? 0)} · manual only ${escapeHtml(sources.manual_only_sources ?? 0)} · query keywords ${escapeHtml(queries.keyword_count ?? 0)} · fallback strategies ${escapeHtml(fallback.strategy_count ?? 0)}</p>
    <p class="review-value">Runtime lane runs ${escapeHtml(runtimePlan.lane_runs ?? 0)} · grouped ${escapeHtml(runtimePlan.grouped_runs ?? 0)} · connector runs ${escapeHtml(runtimePlan.connector_runs ?? 0)} · dedup ${escapeHtml(runtimePlan.shared_source_dedup_count ?? 0)} · dry-run ${escapeHtml(panel.dry_run_status || "UNKNOWN")}</p>
    <p class="review-value">Regression ${escapeHtml(panel.regression_status || "UNKNOWN")} · coverage ${escapeHtml(coverage.coverage_ratio ?? 0)} · duplicate source slots ${escapeHtml(duplicates.duplicate_source_slots ?? 0)} · duplicate connector runs ${escapeHtml(duplicates.duplicate_connector_runs ?? 0)} · failures ${escapeHtml(dryRun.failures ?? 0)}</p>
    <p class="review-label">Today's Lane Runs</p>${renderMiniList(laneRows, "暂无 lane run")}
    <p class="review-label">Grouped Slots</p>${renderMiniList(groupRows, "暂无 grouped slot")}
    <p class="review-label">Connector Dedup</p>${renderMiniList(connectorRows, "暂无 connector run")}
    <p class="review-label">Regression Checks</p>${renderMiniList(checkRows, "暂无 regression check")}
    <p class="review-label">Boundary</p>
    <p class="review-value">configured_playbook=${escapeHtml(policy.configured_playbook ?? true)} · no_openclaw_cron_copy=${escapeHtml(policy.no_openclaw_cron_copy ?? true)} · no_openclaw_mutation=${escapeHtml(policy.no_openclaw_mutation ?? true)} · metadata_only=${escapeHtml(policy.metadata_only ?? true)} · weak_signal_not_hard_evidence=${escapeHtml(policy.weak_signal_not_hard_evidence ?? true)} · no_full_text=${escapeHtml(policy.no_full_text ?? true)} · no_auto_publish=${escapeHtml(policy.no_auto_publish ?? true)}</p>
  </div>`;
}

function renderAutonomousContentProductionPanel(cardClass = "review-card wide") {
  const panel = getAutonomousContentProductionPanel();
  const topicScores = panel.topic_score_summary || {};
  const selection = panel.selection_summary || {};
  const brief = panel.brief_summary || {};
  const outline = panel.outline_summary || {};
  const draft = panel.draft_summary || {};
  const review = panel.review_summary || {};
  const finalCandidate = panel.final_candidate_summary || {};
  const regression = panel.quality_regression_summary || {};
  const pipeline = panel.pipeline_summary || {};
  const policy = panel.policy || {};
  const topicRows = Array.isArray(panel.top_topics) ? panel.top_topics : [];
  const finalRows = Array.isArray(panel.final_candidates) ? panel.final_candidates : [];
  const checkRows = Array.isArray(panel.quality_checks) ? panel.quality_checks : [];
  const mainTopic = panel.main_topic || {};
  const hasPanel = Object.keys(topicScores).length || Object.keys(selection).length || Object.keys(pipeline).length;
  if (!hasPanel) {
    return `<div class="${cardClass} autonomous-content-production-panel">
      <p class="review-label">Autonomous Content Production</p>
      <p class="review-value">暂无 Phase32 自动内容生产数据。运行 <code>make autonomous-topic-to-article</code> 后会显示自动选题、brief、大纲、初稿、Agent review、final candidate 与质量回归。</p>
    </div>`;
  }
  const topicList = topicRows.slice(0, 6).map((item) => `${item.decision || "WATCH"} · ${item.title || item.topic_id || "-"} · score ${item.score_total ?? 0} · ${item.recommended_angle || ""}`);
  const candidateList = finalRows.slice(0, 4).map((item) => `${item.status || "HOLD"} · ${item.title || item.candidate_id || "-"} · manual_review=${item.manual_review_required ?? true} · do_not_publish=${item.do_not_publish ?? true}`);
  const qualityRows = checkRows.slice(0, 8).map((item) => `${item.status}: ${item.check_id} / ${item.message || ""}`);
  return `<div class="${cardClass} autonomous-content-production-panel">
    <p class="review-label">Autonomous Content Production</p>
    <p class="review-value">Pipeline ${escapeHtml(panel.pipeline_status || "UNKNOWN")} · topics ${escapeHtml(topicScores.topic_count ?? 0)} · main candidates ${escapeHtml(topicScores.main_candidates ?? 0)} · selected ${escapeHtml(selection.selected ?? false)} · final candidates ${escapeHtml(finalCandidate.candidate_count ?? 0)}</p>
    <p class="review-value">Briefs ${escapeHtml(brief.brief_count ?? 0)} · ready outline ${escapeHtml(brief.ready_for_outline ?? 0)} · outlines ${escapeHtml(outline.outline_count ?? 0)} · drafts ${escapeHtml(draft.draft_count ?? 0)} · reviews ${escapeHtml(review.review_count ?? 0)}</p>
    <p class="review-value">Quality ${escapeHtml(panel.quality_regression_status || "UNKNOWN")} · pass ${escapeHtml(regression.pass ?? 0)} · warn ${escapeHtml(regression.warn ?? 0)} · fail ${escapeHtml(regression.fail ?? 0)} · blocking ${escapeHtml(regression.blocking_failures ?? 0)} · steps_ok ${escapeHtml(pipeline.steps_ok ?? 0)}</p>
    <p class="review-label">Today's Main Topic</p>
    <p class="review-value">${mainTopic.title ? `${escapeHtml(mainTopic.title)} · ${escapeHtml(mainTopic.recommended_angle || mainTopic.reason || "")}` : escapeHtml(panel.main_topic_status || "NO_QUALIFIED_TOPIC")}</p>
    <p class="review-label">Top Topic Scores</p>${renderMiniList(topicList, "暂无 topic score")}
    <p class="review-label">Final Candidates</p>${renderMiniList(candidateList, "暂无 final candidate")}
    <p class="review-label">Quality Regression</p>${renderMiniList(qualityRows, "暂无 quality check")}
    <p class="review-label">Boundary</p>
    <p class="review-value">do_not_publish=${escapeHtml(policy.do_not_publish ?? true)} · manual_review_required=${escapeHtml(policy.manual_review_required ?? true)} · no_wechat_api=${escapeHtml(policy.no_wechat_api ?? true)} · no_full_text=${escapeHtml(policy.no_full_text ?? true)} · no_image_generation=${escapeHtml(policy.no_image_generation ?? true)} · weak_signal_not_hard_evidence=${escapeHtml(policy.weak_signal_not_hard_evidence ?? true)}</p>
  </div>`;
}

function renderReplayTrialPanel(cardClass = "review-card wide") {
  const panel = getReplayTrialPanel();
  const availability = panel.availability_summary || {};
  const selection = panel.topic_selection_summary || {};
  const generation = panel.content_generation_summary || {};
  const review = panel.article_review_summary || {};
  const quality = panel.quality_summary || {};
  const checklist = panel.checklist_summary || {};
  const diagnosis = panel.diagnosis_summary || {};
  const calibration = panel.calibration_summary || {};
  const observation = panel.observation_summary || {};
  const policy = panel.policy || {};
  const dayCards = Array.isArray(panel.day_cards) ? panel.day_cards : [];
  const issues = Array.isArray(panel.issues) ? panel.issues : [];
  const proposals = Array.isArray(panel.proposals) ? panel.proposals : [];
  const hasPanel = Object.keys(availability).length || Object.keys(selection).length || panel.pipeline_status;
  if (!hasPanel) {
    return `<div class="${cardClass} replay-trial-panel">
      <p class="review-label">7-Day Replay Trial Dashboard</p>
      <p class="review-value">暂无 Phase33 replay 数据。运行 <code>make phase33-daily</code> 后会显示过去 7 天 time-sliced replay、质量回归、人工 checklist 和校准建议。</p>
    </div>`;
  }
  const dayRows = dayCards.map((item) => `${item.business_date}: ${item.status} / ${item.topic_title} / quality ${item.quality_status} / metadata=${item.source_metadata_title} / duplicate=${item.duplicate_topic} / worth_reading=${item.worth_reading}`);
  const issueRows = issues.slice(0, 6).map((item) => `${item.severity || "MEDIUM"} ${item.issue_type || item.issue_id}: ${item.recommended_fix || ""}`);
  const proposalRows = proposals.slice(0, 6).map((item) => `${item.severity || "MEDIUM"} ${item.proposal_type || item.proposal_id} -> ${item.target_config || ""} / auto_apply=${item.auto_apply ?? false}`);
  return `<div class="${cardClass} replay-trial-panel">
    <p class="review-label">7-Day Replay Trial Dashboard</p>
    <p class="review-value">Pipeline ${escapeHtml(panel.pipeline_status || "UNKNOWN")} · replay ready ${escapeHtml(availability.replay_ready_days ?? 0)}/7 · selected days ${escapeHtml(selection.selected_days ?? 0)} · no topic ${escapeHtml(selection.no_qualified_topic_days ?? 0)} · final candidates ${escapeHtml(review.final_candidate_count ?? 0)}</p>
    <p class="review-value">Briefs ${escapeHtml(generation.brief_count ?? 0)} · drafts ${escapeHtml(generation.draft_count ?? 0)} · quality pass/actionable/fail ${escapeHtml(quality.pass_days ?? 0)}/${escapeHtml(quality.actionable_days ?? 0)}/${escapeHtml(quality.fail_days ?? 0)} · checklists ${escapeHtml(checklist.checklist_count ?? 0)}</p>
    <p class="review-value">metadata title ratio ${escapeHtml(diagnosis.source_metadata_title_ratio ?? 0)} · duplicate ratio ${escapeHtml(diagnosis.duplicate_topic_ratio ?? 0)} · proposals ${escapeHtml(calibration.proposal_count ?? 0)} · observation checks ${escapeHtml(observation.check_count ?? 0)}</p>
    <p class="review-label">Replay Days</p>${renderMiniList(dayRows, "暂无 replay day")}
    <p class="review-label">Quality Diagnosis</p>${renderMiniList(issueRows, "暂无 replay issue")}
    <p class="review-label">Calibration Proposals</p>${renderMiniList(proposalRows, "暂无 calibration proposal")}
    <p class="review-label">Boundary</p>
    <p class="review-value">replay_namespace_only=${escapeHtml(policy.replay_namespace_only ?? true)} · no_production_latest_pollution=${escapeHtml(policy.no_production_latest_pollution ?? true)} · no_auto_publish=${escapeHtml(policy.no_auto_publish ?? true)} · no_wechat_api=${escapeHtml(policy.no_wechat_api ?? true)} · no_full_text=${escapeHtml(policy.no_full_text ?? true)} · no_image_generation=${escapeHtml(policy.no_image_generation ?? true)} · calibration_auto_apply=${escapeHtml(policy.calibration_auto_apply ?? false)}</p>
  </div>`;
}

function renderStableTrialPanel(cardClass = "review-card wide") {
  const panel = getPhase24Panel();
  const days = Array.isArray(panel.day_summaries) ? panel.day_summaries : [];
  const qualitySummary = panel.content_quality_summary || {};
  const feedbackSummary = panel.methodology_feedback_summary || {};
  const readinessSummary = panel.readiness_summary || {};
  const qualityIssues = Array.isArray(panel.quality_issues) ? panel.quality_issues : [];
  const blockingQuality = Array.isArray(panel.blocking_quality_issues) ? panel.blocking_quality_issues : [];
  const feedback = Array.isArray(panel.methodology_feedback) ? panel.methodology_feedback : [];
  const criteria = Array.isArray(panel.readiness_criteria) ? panel.readiness_criteria : [];
  const risks = Array.isArray(panel.remaining_risks) ? panel.remaining_risks : [];
  const commitments = Array.isArray(panel.operator_commitments) ? panel.operator_commitments : [];
  const policy = panel.policy || {};
  const hasPanel = days.length || Object.keys(readinessSummary).length || panel.readiness_status;
  if (!hasPanel || panel.readiness_status === "UNKNOWN") {
    return `<div class="${cardClass} stable-trial-panel">
      <p class="review-label">Phase24 Stable Trial</p>
      <p class="review-value">暂无 Phase24 数据。运行 <code>make phase24-daily</code> 后会显示 Stable Trial Day 1-3、Content Quality Calibration、Ops-to-Methodology Feedback 和 Stable Ops Readiness Review。</p>
    </div>`;
  }
  const dayRows = days.map((item) => `Day ${item.stable_trial_day}: ${item.day_status} / continue ${item.can_continue} / review ${item.ready_for_review} / publish ${item.ready_to_publish} / warnings ${item.actionable_warnings}`);
  const qualityRows = qualityIssues.slice(0, 8).map((item) => `${item.severity} ${item.area}: ${item.description}`);
  const blockerRows = blockingQuality.slice(0, 6).map((item) => `${item.area}: ${item.description}`);
  const feedbackRows = feedback.slice(0, 6).map((item) => `${item.target_config} / ${item.feedback_type}: ${item.suggested_change}`);
  const criteriaRows = criteria.slice(0, 8).map((item) => `${item.status}: ${item.criterion_id} / ${item.message}`);
  return `<div class="${cardClass} stable-trial-panel">
    <p class="review-label">Phase24 Stable Trial Panel</p>
    <p class="review-value">Readiness ${escapeHtml(panel.readiness_status || "UNKNOWN")} · stable days ${escapeHtml(readinessSummary.stable_trial_days ?? days.length)} · ready ${escapeHtml(readinessSummary.ready_days ?? 0)} · actionable ${escapeHtml(readinessSummary.actionable_days ?? 0)} · blocked ${escapeHtml(readinessSummary.blocked_days ?? 0)}</p>
    <p class="review-value">Quality issues ${escapeHtml(qualitySummary.quality_issue_count ?? 0)} · publish blockers ${escapeHtml(qualitySummary.publish_blocking_quality_issues ?? 0)} · methodology feedback ${escapeHtml(feedbackSummary.feedback_count ?? 0)} · phase24 ${escapeHtml(panel.phase24_status || "UNKNOWN")}</p>
    <p class="review-label">Stable Trial Day 1-3</p>${renderMiniList(dayRows, "暂无 stable trial day")}
    <p class="review-label">Content Quality Calibration</p>${renderMiniList(qualityRows, "暂无 quality issue")}
    <p class="review-label">Content Quality Blockers</p>${renderMiniList(blockerRows, "暂无 publish-blocking quality issue")}
    <p class="review-label">Ops-to-Methodology Feedback</p>${renderMiniList(feedbackRows, "暂无 methodology feedback")}
    <p class="review-label">Stable Ops Readiness Review</p>${renderMiniList(criteriaRows, "暂无 readiness criteria")}
    <p class="review-label">Remaining Risks</p>${renderMiniList(risks, "暂无 remaining risk")}
    <p class="review-label">Next Operator Commitments</p>${renderMiniList(commitments, "暂无 operator commitment")}
    <p class="review-label">Boundary</p>
    <p class="review-value">auto_apply=${escapeHtml(policy.auto_apply ?? false)} · no_auto_publish=${escapeHtml(policy.no_auto_publish ?? true)} · no_wechat_api=${escapeHtml(policy.no_wechat_api ?? true)} · no_auto_image_generation=${escapeHtml(policy.no_auto_image_generation ?? true)} · no_config_prompt_rule_changes=${escapeHtml(policy.no_config_prompt_rule_changes ?? true)}</p>
  </div>`;
}

function renderInsightPanel() {
  const article = getSelectedArticle();
  const comparison = getLatestComparison();
  const decision = getLatestDecision();
  const finalCandidate = getFinalCandidate();
  const finalChecklist = getFinalChecklist();
  const session = getSelectedSession();
  const metrics = getSelectedMetrics();
  const topicMethodology = getSelectedMethodologyTopic();
  const articleMethodology = getSelectedMethodologyArticle();
  const generation = getGenerationVisualPanel();
  const livePilot = getLivePilotPanel();
  const imageAsset = getImageAssetPanel();
  const publishingPack = getPublishingPackPanel();
  const contentOps = getContentOpsPanel();
  const hardening = getContentHardeningPanel();
  const trial = getTrialPanel();
  const phase22 = getPhase22Panel();
  const phase23 = getPhase23Panel();
  const phase24 = getPhase24Panel();
  const phase25 = getPhase25Panel();
  const hotMaterial = getHotMaterialPanel();
  const connectorHealth = getConnectorHealthPanel();
  const evidenceTopic = getEvidenceTopicPromotionPanel();
  const openclawMigration = getOpenClawMigrationPanel();
  const openclawActivation = getOpenClawActivationPanel();
  const runtimeControl = getRuntimeControlCenterPanel();
  const acquisitionPlaybook = getAcquisitionPlaybookPanel();
  const autonomousContent = getAutonomousContentProductionPanel();
  const replayTrial = getReplayTrialPanel();
  const visualSummary = generation.visual_plan_summary || {};
  const requestSummary = generation.image_request_summary || {};
  const liveComparisonSummary = livePilot.comparison_summary || {};
  const imageApprovalSummary = livePilot.image_approval_summary || {};
  const imageTaskSummary = imageAsset.manual_image_task_summary || {};
  const imageLibrarySummary = imageAsset.image_asset_library_summary || {};
  const visualReviewSummary = imageAsset.final_visual_review_summary || {};
  const packSummary = publishingPack.copy_pack_summary || {};
  const packChecklistSummary = publishingPack.visual_checklist_summary || {};
  const opsQueueSummary = contentOps.queue_summary || {};
  const opsCalendarSummary = contentOps.calendar_summary || {};
  const opsCloseoutSummary = contentOps.closeout_summary || {};
  const hardeningFailureSummary = hardening.failure_summary || {};
  const hardeningRegressionSummary = hardening.regression_summary || {};
  const hardeningReadiness = hardening.system_closeout_readiness || {};
  const trialSummary = trial.retrospective_summary || {};
  const trialFixSummary = trial.fix_pack_summary || {};
  const trialDays = Array.isArray(trial.day_summaries) ? trial.day_summaries : [];
  const trialRecurring = Array.isArray(trial.recurring_issues) ? trial.recurring_issues : [];
  const trialFixes = Array.isArray(trial.fixes) ? trial.fixes : [];
  const trialSafety = trial.safety_boundary_check || {};
  const trialDayText = trialDays.slice(0, 5).map((item) => `D${item.trial_day}: ${item.day_status || "UNKNOWN"} / issues ${item.issue_count ?? 0}`).join(" · ") || "暂无 Trial Day 1-5";
  const trialRecurringText = trialRecurring.slice(0, 2).map((item) => `${item.area || "system"}: ${item.description || item.issue_id || ""}`).join(" · ") || "暂无 Recurring issues";
  const trialFixText = trialFixes.slice(0, 2).map((item) => `${item.fix_type || "fix"}: ${item.description || item.fix_id || ""}`).join(" · ") || "暂无 Trial Fix Pack";
  const phase22Runner = phase22.daily_runner_summary || {};
  const phase22Issues = phase22.recurring_issue_summary || {};
  const phase22Calendar = phase22.weekly_calendar_summary || {};
  const phase22Feedback = phase22.post_publish_feedback_summary || {};
  const phase23Gate = phase23.gate_summary || {};
  const phase23Quick = phase23.quick_fix_summary || {};
  const phase23Verification = phase23.verification_summary || {};
  const phase23Calendar = phase23.calendar_calibration_summary || {};
  const phase24Readiness = phase24.readiness_summary || {};
  const phase24Quality = phase24.content_quality_summary || {};
  const phase24Feedback = phase24.methodology_feedback_summary || {};
  const phase25Baseline = phase25.baseline_summary || {};
  const phase25Acceptance = phase25.operator_acceptance_summary || {};
  const phase25Quality = phase25.content_quality_status || {};
  const hotMaterialSummary = hotMaterial.material_summary || {};
  const hotGateSummary = hotMaterial.quality_gate_summary || {};
  const hotSignalSummary = hotMaterial.hot_signal_summary || {};
  const connectorSummary = connectorHealth.health_summary || {};
  const normalizedSummary = connectorHealth.normalized_summary || {};
  const connectorContribution = connectorHealth.connector_contribution || {};
  const evidenceSummary = evidenceTopic.evidence_summary || {};
  const promotedSummary = evidenceTopic.promoted_topic_summary || {};
  const bridgeSummary = evidenceTopic.bridge_summary || {};
  const freshnessSummary = evidenceTopic.freshness_summary || {};
  const dedupSummary = evidenceTopic.dedup_summary || {};
  const openclawInventory = openclawMigration.inventory_summary || {};
  const openclawPlan = openclawMigration.migration_plan_summary || {};
  const openclawWeak = openclawMigration.weak_signal_summary || {};
  const openclawHot = openclawMigration.hot_material_summary || {};
  const openclawBackfill = openclawActivation.backfill_summary || {};
  const openclawConfirmation = openclawActivation.confirmation_summary || {};
  const openclawTopicActivation = openclawActivation.activation_summary || {};
  const openclawRegression = openclawActivation.regression_summary || {};
  const runtimeLedger = runtimeControl.ledger_summary || {};
  const runtimeRetry = runtimeControl.retry_summary || {};
  const runtimeMissed = runtimeControl.missed_run_summary || {};
  const runtimeNetwork = runtimeControl.network_readiness || {};
  const acquisitionCadence = acquisitionPlaybook.cadence_summary || {};
  const acquisitionRuntime = acquisitionPlaybook.runtime_plan_summary || {};
  const acquisitionRegression = acquisitionPlaybook.regression_coverage || {};
  const acquisitionDuplicates = acquisitionPlaybook.regression_duplicates || {};
  const acquisitionDry = acquisitionPlaybook.dry_run_summary || {};
  const autoTopicScores = autonomousContent.topic_score_summary || {};
  const autoSelection = autonomousContent.selection_summary || {};
  const autoBrief = autonomousContent.brief_summary || {};
  const autoOutline = autonomousContent.outline_summary || {};
  const autoDraft = autonomousContent.draft_summary || {};
  const autoReview = autonomousContent.review_summary || {};
  const autoFinal = autonomousContent.final_candidate_summary || {};
  const autoRegression = autonomousContent.quality_regression_summary || {};
  const autoPipeline = autonomousContent.pipeline_summary || {};
  const replayAvailability = replayTrial.availability_summary || {};
  const replaySelection = replayTrial.topic_selection_summary || {};
  const replayReview = replayTrial.article_review_summary || {};
  const replayQuality = replayTrial.quality_summary || {};
  const replayDiagnosis = replayTrial.diagnosis_summary || {};
  const replayCalibration = replayTrial.calibration_summary || {};
  const scores = comparison.scores || {};
  const panel = document.getElementById("insight-panel");
  const readyText = article.status === "ready" ? "可进入人工确认" : (article.next_step || "等待主编判断");
  panel.innerHTML = `
    <div class="panel-head"><h2>系统判断</h2><span class="count-note">当前稿件</span></div>
    <section class="insight-card readiness">
      <div>
        <p class="insight-label">当前状态</p>
        <p class="insight-value"><span class="badge ${statusClass(article.status)}">${escapeHtml(statusLabel(article.status))}</span></p>
      </div>
      <div class="score-number">${escapeHtml(article.quality_score || 0)}</div>
    </section>
    <section class="insight-card">
      <p class="insight-label">下一步建议</p>
      <p class="insight-value">${escapeHtml(readyText)}</p>
    </section>
    <section class="insight-card">
      <p class="insight-label">Judge</p>
      <p class="insight-value">${escapeHtml(shortText(article.judge_decision))}</p>
    </section>
    <section class="insight-card">
      <p class="insight-label">Critic</p>
      <p class="insight-value">${escapeHtml(shortText(article.critic_summary))}</p>
    </section>
    <section class="insight-card">
      <p class="insight-label">Revision</p>
      <p class="insight-value">${escapeHtml(shortText(article.revision_summary))}</p>
    </section>
    <section class="insight-card">
      <p class="insight-label">证据与来源</p>
      <p class="insight-value">${escapeHtml(article.evidence_count ?? (article.evidence_ids || []).length ?? 0)} evidence · ${escapeHtml(article.source_count ?? (article.source_ids || []).length ?? 0)} source</p>
    </section>
    <section class="insight-card version-panel">
      <p class="insight-label">版本质量回归</p>
      <p class="insight-value">${comparison.version_id ? `Delta <span class="delta-number">${escapeHtml(scores.delta ?? 0)}</span> · ${escapeHtml(comparison.recommendation || "HUMAN_REVIEW")} · ${escapeHtml(decision.decision || "UNREVIEWED")}` : "暂无新版本评分"}</p>
    </section>
    <section class="insight-card final-panel">
      <p class="insight-label">最终候选稿</p>
      <p class="insight-value">${finalCandidate.final_candidate_id ? `${escapeHtml(finalCandidate.quality_status || "NEEDS_FINAL_CHECK")} · ${escapeHtml(finalChecklist.status || "UNREVIEWED")} · would_publish=false` : "暂无 final candidate"}</p>
    </section>
    <section class="insight-card performance-panel">
      <p class="insight-label">发布表现</p>
      <p class="insight-value">${session.publish_session_id ? `${escapeHtml(session.publish_status || "PLANNED")} · ${escapeHtml(metrics.performance_rating || "UNKNOWN")} · views ${escapeHtml(metrics.views ?? "-")}` : "暂无人工发布 session"}</p>
    </section>
    <section class="insight-card methodology-panel">
      <p class="insight-label">内容方法论</p>
      <p class="insight-value">${topicMethodology.topic_id || articleMethodology.article_id ? `Topic ${escapeHtml(topicMethodology.methodology_total_score ?? "-")} · Article ${escapeHtml(articleMethodology.methodology_total_score ?? "-")} · ${escapeHtml(topicMethodology.recommended_recipe_id || articleMethodology.recipe_id || "recipe")}` : "暂无方法论评分"}</p>
    </section>
    <section class="insight-card generation-panel">
      <p class="insight-label">生成与图片策略</p>
      <p class="insight-value">Briefs ${escapeHtml((generation.brief_summary || {}).brief_count ?? 0)} · Visual plans ${escapeHtml(visualSummary.plan_count ?? 0)} · Image requests ${escapeHtml(requestSummary.request_count ?? 0)}</p>
    </section>
    <section class="insight-card live-panel">
      <p class="insight-label">Live Pilot</p>
      <p class="insight-value">Comparisons ${escapeHtml(liveComparisonSummary.comparison_count ?? 0)} · Image approvals ${escapeHtml(imageApprovalSummary.request_count ?? 0)} · sidecar only</p>
    </section>
    <section class="insight-card image-asset-panel">
      <p class="insight-label">图片资产链路</p>
      <p class="insight-value">Tasks ${escapeHtml(imageTaskSummary.task_count ?? 0)} · Assets ${escapeHtml(imageLibrarySummary.asset_count ?? 0)} · WeChat ready ${escapeHtml(visualReviewSummary.wechat_ready ?? 0)}</p>
    </section>
    <section class="insight-card publishing-pack-panel">
      <p class="insight-label">图文发布包</p>
      <p class="insight-value">Packs ${escapeHtml(packSummary.pack_count ?? 0)} · ready ${escapeHtml(packSummary.ready_for_manual_copy ?? 0)} · checklist ready ${escapeHtml(packChecklistSummary.ready ?? 0)} · manual copy only</p>
    </section>
    <section class="insight-card content-ops-panel">
      <p class="insight-label">内容运营</p>
      <p class="insight-value">Slots ${escapeHtml(opsCalendarSummary.planned_slots ?? 0)} · Queue ${escapeHtml(opsQueueSummary.item_count ?? 0)} · Today ${escapeHtml(opsQueueSummary.today ?? 0)} · Blocked ${escapeHtml(opsCloseoutSummary.blocked_count ?? 0)}</p>
    </section>
    <section class="insight-card hardening-panel">
      <p class="insight-label">试运行加固</p>
      <p class="insight-value">Issues ${escapeHtml(hardeningFailureSummary.issue_count ?? 0)} · Regression ${escapeHtml(hardeningRegressionSummary.regression_status || "UNKNOWN")} · Readiness ${escapeHtml(hardeningReadiness.status || "UNKNOWN")}</p>
    </section>
    <section class="insight-card phase22-panel">
      <p class="insight-label">Phase22 运营闭环</p>
      <p class="insight-value">Status ${escapeHtml(phase22.phase22_status || "UNKNOWN")} · Actions ${escapeHtml(phase22Runner.action_count ?? 0)} · Recurring ${escapeHtml(phase22Issues.issue_count ?? 0)} · Calendar ${escapeHtml(phase22Calendar.calendar_days ?? 0)}d · Feedback ${escapeHtml(phase22Feedback.recommendation_count ?? 0)}</p>
      <p class="insight-value">sidecar only · no auto publish · no WeChat API · no image generation</p>
    </section>
    <section class="insight-card stable-ops-panel">
      <p class="insight-label">Phase23 Stable Ops</p>
      <p class="insight-value">Gate ${escapeHtml(phase23.gate_status || "UNKNOWN")} · pass ${escapeHtml(phase23Gate.pass ?? 0)} · warn ${escapeHtml(phase23Gate.warn ?? 0)} · fail ${escapeHtml(phase23Gate.fail ?? 0)} · blocking ${escapeHtml(phase23Gate.blocking_failures ?? 0)}</p>
      <p class="insight-value">Quick fixes ${escapeHtml(phase23Quick.applied_sidecar ?? 0)} · verified ${escapeHtml(phase23Verification.verified ?? 0)} · unresolved ${escapeHtml(phase23Verification.unresolved ?? 0)} · actionable days ${escapeHtml(phase23Calendar.actionable_days ?? 0)}</p>
    </section>
    <section class="insight-card stable-trial-panel">
      <p class="insight-label">Phase24 Stable Trial</p>
      <p class="insight-value">Readiness ${escapeHtml(phase24.readiness_status || "UNKNOWN")} · days ${escapeHtml(phase24Readiness.stable_trial_days ?? 0)} · actionable ${escapeHtml(phase24Readiness.actionable_days ?? 0)} · blocked ${escapeHtml(phase24Readiness.blocked_days ?? 0)}</p>
      <p class="insight-value">Quality issues ${escapeHtml(phase24Quality.quality_issue_count ?? 0)} · blockers ${escapeHtml(phase24Quality.publish_blocking_quality_issues ?? 0)} · methodology feedback ${escapeHtml(phase24Feedback.feedback_count ?? 0)}</p>
    </section>
    <section class="insight-card stable-workbench-baseline">
      <p class="insight-label">Stable Daily Ops</p>
      <p class="insight-value"><code>${escapeHtml(phase25.daily_command || "make stable-daily-ops")}</code> · Baseline ${escapeHtml(phase25.baseline_status || "UNKNOWN")} · Acceptance ${escapeHtml(phase25.operator_acceptance_status || "UNKNOWN")} · v1 ${escapeHtml(phase25.v1_status || "UNKNOWN")}</p>
      <p class="insight-value">Blocking ${escapeHtml(phase25Baseline.blocking_issue_count ?? 0)} · manual review ${escapeHtml(phase25Acceptance.manual_review_required ?? true)} · ready_to_publish ${escapeHtml(phase25Quality.ready_to_publish ?? 0)} · quality blockers ${escapeHtml(phase25Quality.publish_blocking_quality_issues ?? 0)}</p>
    </section>
    <section class="insight-card hot-material-panel">
      <p class="insight-label">上游素材供给</p>
      <p class="insight-value">Gate ${escapeHtml(hotMaterial.gate_status || "UNKNOWN")} · materials ${escapeHtml(hotMaterialSummary.material_count ?? 0)} · promote ${escapeHtml(hotGateSummary.promote_to_topic_pipeline ?? 0)} · backfill ${escapeHtml(hotGateSummary.backfill_required ?? 0)}</p>
      <p class="insight-value">write_now ${escapeHtml(hotMaterialSummary.write_now ?? 0)} · develop_topic ${escapeHtml(hotMaterialSummary.develop_topic ?? 0)} · signals ${escapeHtml(hotSignalSummary.hot_signal_count ?? 0)} · active lanes ${escapeHtml(hotSignalSummary.active_lanes ?? 0)}</p>
    </section>
    <section class="insight-card connector-health-panel">
      <p class="insight-label">Phase27 Connector Health</p>
      <p class="insight-value">Gate ${escapeHtml(connectorHealth.gate_status || "UNKNOWN")} · normalized ${escapeHtml(normalizedSummary.item_count ?? 0)} · healthy ${escapeHtml(connectorSummary.healthy_connectors ?? 0)} · weak ${escapeHtml(connectorSummary.weak_connectors ?? 0)} · failed ${escapeHtml(connectorSummary.failed_connectors ?? 0)}</p>
      <p class="insight-value">connector material ${escapeHtml(connectorContribution.connector_item_count ?? 0)} · promote candidates ${escapeHtml(connectorContribution.connector_promote_candidates ?? 0)} · metadata ${escapeHtml((connectorHealth.metadata_check || {}).status || "UNKNOWN")} · copyright ${escapeHtml((connectorHealth.copyright_check || {}).status || "UNKNOWN")}</p>
    </section>
    <section class="insight-card evidence-topic-promotion-panel">
      <p class="insight-label">Phase28 Evidence / Topic</p>
      <p class="insight-value">Evidence ${escapeHtml(evidenceSummary.packet_count ?? 0)} · eligible ${escapeHtml(evidenceSummary.eligible_for_topic_promotion ?? 0)} · promoted ${escapeHtml(promotedSummary.promoted ?? 0)} · needs evidence ${escapeHtml(promotedSummary.needs_evidence ?? 0)}</p>
      <p class="insight-value">ready_for_brief ${escapeHtml(bridgeSummary.ready_for_brief ?? 0)} · bridge_needs_evidence ${escapeHtml(bridgeSummary.needs_evidence ?? 0)} · regression ${escapeHtml(evidenceTopic.regression_status || "UNKNOWN")} · freshness unknown ${escapeHtml(freshnessSummary.unknown ?? 0)} · duplicate ${escapeHtml(dedupSummary.duplicate_ratio ?? 0)}</p>
    </section>
    <section class="insight-card openclaw-migration-panel">
      <p class="insight-label">Phase29 OpenClaw Migration</p>
      <p class="insight-value">Status ${escapeHtml(openclawMigration.phase29_status || "UNKNOWN")} · sources ${escapeHtml(openclawInventory.source_count ?? 0)} · P0 ${escapeHtml(openclawPlan.p0 ?? 0)} · P1 ${escapeHtml(openclawPlan.p1 ?? 0)} · metadata items ${escapeHtml((openclawMigration.metadata_connector_summary || {}).item_count ?? 0)}</p>
      <p class="insight-value">weak signals ${escapeHtml(openclawWeak.item_count ?? 0)} · hard evidence allowed ${escapeHtml(openclawWeak.hard_evidence_allowed ?? 0)} · OpenClaw hot materials ${escapeHtml(openclawHot.openclaw_hot_material_count ?? 0)} · no gateway / no cron / no full text</p>
    </section>
    <section class="insight-card openclaw-activation-panel">
      <p class="insight-label">Phase30 OpenClaw Activation</p>
      <p class="insight-value">Status ${escapeHtml(openclawActivation.phase30_status || "UNKNOWN")} · backfill ${escapeHtml(openclawBackfill.backfill_count ?? 0)} · ready confirmation ${escapeHtml(openclawBackfill.ready_for_confirmation ?? 0)} · needs primary ${escapeHtml(openclawConfirmation.needs_primary_source ?? 0)} · needs second ${escapeHtml(openclawConfirmation.needs_second_source ?? 0)}</p>
      <p class="insight-value">activated ${escapeHtml(openclawTopicActivation.activated ?? 0)} · can enter brief ${escapeHtml(openclawTopicActivation.can_enter_brief_pipeline ?? 0)} · gate ${escapeHtml(openclawActivation.regression_gate_status || "UNKNOWN")} · blocking ${escapeHtml(openclawRegression.blocking_failures ?? 0)} · weak signals not hard evidence</p>
    </section>
    <section class="insight-card runtime-control-panel">
      <p class="insight-label">Autonomous Runtime</p>
      <p class="insight-value">status ${escapeHtml(runtimeControl.runtime_status || "UNKNOWN")} · success ${escapeHtml(runtimeLedger.success ?? 0)} · failed ${escapeHtml(runtimeLedger.failed ?? 0)} · retry ${escapeHtml(runtimeRetry.retry_count ?? 0)} · missed ${escapeHtml(runtimeMissed.missed_count ?? 0)} · network ${escapeHtml(runtimeNetwork.status || "UNKNOWN")}</p>
    </section>
    <section class="insight-card acquisition-playbook-panel">
      <p class="insight-label">Acquisition Playbook</p>
      <p class="insight-value">slots ${escapeHtml(acquisitionCadence.schedule_slot_count ?? 0)} · lane runs ${escapeHtml(acquisitionRuntime.lane_runs ?? 0)} · connector runs ${escapeHtml(acquisitionRuntime.connector_runs ?? 0)} · dedup ${escapeHtml(acquisitionRuntime.shared_source_dedup_count ?? 0)}</p>
      <p class="insight-value">coverage ${escapeHtml(acquisitionRegression.coverage_ratio ?? 0)} · duplicate source slots ${escapeHtml(acquisitionDuplicates.duplicate_source_slots ?? 0)} · dry-run ${escapeHtml(acquisitionPlaybook.dry_run_status || "UNKNOWN")} · failures ${escapeHtml(acquisitionDry.failures ?? 0)}</p>
    </section>
    <section class="insight-card autonomous-content-production-panel">
      <p class="insight-label">Phase32 自动内容生产</p>
      <p class="insight-value">Pipeline ${escapeHtml(autonomousContent.pipeline_status || "UNKNOWN")} · topics ${escapeHtml(autoTopicScores.topic_count ?? 0)} · selected ${escapeHtml(autoSelection.selected ?? false)} · briefs ${escapeHtml(autoBrief.brief_count ?? 0)} · outlines ${escapeHtml(autoOutline.outline_count ?? 0)}</p>
      <p class="insight-value">Drafts ${escapeHtml(autoDraft.draft_count ?? 0)} · reviews ${escapeHtml(autoReview.review_count ?? 0)} · final ${escapeHtml(autoFinal.candidate_count ?? 0)} · quality ${escapeHtml(autonomousContent.quality_regression_status || "UNKNOWN")} · blocking ${escapeHtml(autoRegression.blocking_failures ?? 0)} · steps_ok ${escapeHtml(autoPipeline.steps_ok ?? 0)}</p>
    </section>
    <section class="insight-card replay-trial-panel">
      <p class="insight-label">Phase33 7天回放校准</p>
      <p class="insight-value">Pipeline ${escapeHtml(replayTrial.pipeline_status || "UNKNOWN")} · ready ${escapeHtml(replayAvailability.replay_ready_days ?? 0)}/7 · selected ${escapeHtml(replaySelection.selected_days ?? 0)} · no topic ${escapeHtml(replaySelection.no_qualified_topic_days ?? 0)} · final ${escapeHtml(replayReview.final_candidate_count ?? 0)}</p>
      <p class="insight-value">quality P/A/F ${escapeHtml(replayQuality.pass_days ?? 0)}/${escapeHtml(replayQuality.actionable_days ?? 0)}/${escapeHtml(replayQuality.fail_days ?? 0)} · metadata ratio ${escapeHtml(replayDiagnosis.source_metadata_title_ratio ?? 0)} · proposals ${escapeHtml(replayCalibration.proposal_count ?? 0)} · auto_apply=0</p>
    </section>
    <section class="insight-card trial-panel">
      <p class="insight-label">Phase21 试运行</p>
      <p class="insight-value">Days ${escapeHtml(trialSummary.days_recorded ?? 0)} · Warn ${escapeHtml(trialSummary.warn_days ?? 0)} · Fixes ${escapeHtml(trialFixSummary.fix_count ?? 0)} · scaffold only</p>
      <p class="insight-value"><strong>Trial Day 1-5</strong> · ${escapeHtml(shortText(trialDayText, "", 180))}</p>
      <p class="insight-value"><strong>Recurring issues</strong> · ${escapeHtml(shortText(trialRecurringText, "", 180))}</p>
      <p class="insight-value"><strong>Trial Fix Pack</strong> · ${escapeHtml(shortText(trialFixText, "", 180))}</p>
      <p class="insight-value"><strong>Safety Boundary</strong> · auto_publish=${escapeHtml(trialSafety.auto_publish ?? false)} · wechat_api=${escapeHtml(trialSafety.wechat_api ?? false)} · auto_image_generation=${escapeHtml(trialSafety.auto_image_generation ?? false)}</p>
    </section>`;
}

function renderChiefBar() {
  const article = getSelectedArticle();
  document.getElementById("chief-target").textContent = `目标：${article.wechat_title || article.title || "未选择文章"}`;
  const reply = chiefResponse.human_readable_reply || "暂无主编 Agent 响应。输入需求后复制命令，在终端运行即可生成 PLAN_ONLY action plan。";
  const actions = Array.isArray(pendingPayload.actions) ? pendingPayload.actions : [];
  const actionRows = actions.length
    ? actions.slice(0, 5).map((item) => `<li>${escapeHtml(item.action_type || "action")} · ${escapeHtml(item.status || "PENDING")} · ${escapeHtml(item.description || "")}</li>`).join("")
    : "<li>暂无 pending action</li>";
  document.getElementById("agent-memory").innerHTML = `<h3>最近一次 AI 理解</h3>
    <p><strong>${escapeHtml(chiefResponse.intent || "no_intent")}</strong> · ${escapeHtml(reply)}</p>
    <h3>Pending actions</h3>
    <ul>${actionRows}</ul>`;
  updateCommandPreview();
}

function shellQuote(value) {
  return "'" + String(value).replace(/'/g, "'\"'\"'") + "'";
}

function buildCommand() {
  const article = getSelectedArticle();
  const rawMessage = document.getElementById("chief-message").value.trim() || "请给当前稿件生成下一步主编建议";
  const decorated = `目标文章：${article.wechat_title || article.title || "未选择文章"} (${article.article_id || "-"})\n用户诉求：${rawMessage}`;
  return `python3 scripts/run_chief_editor_agent.py --message ${shellQuote(decorated)} && make workbench-action-router`;
}

function updateCommandPreview() {
  currentCommand = buildCommand();
  document.getElementById("command-preview").textContent = currentCommand;
}

function copyText(value) {
  if (navigator.clipboard && window.isSecureContext) {
    return navigator.clipboard.writeText(value);
  }
  const textarea = document.createElement("textarea");
  textarea.value = value;
  textarea.style.position = "fixed";
  textarea.style.opacity = "0";
  document.body.appendChild(textarea);
  textarea.focus();
  textarea.select();
  document.execCommand("copy");
  textarea.remove();
  return Promise.resolve();
}

function copyCommand() {
  updateCommandPreview();
  copyText(currentCommand).then(() => {
    document.getElementById("command-status").textContent = "命令已复制，终端运行后会生成结构化 action plan。";
  }).catch(() => {
    document.getElementById("command-status").textContent = "复制失败，请手动复制下方命令。";
  });
}

function bindReviewCommandButtons() {
  document.querySelectorAll(".copy-review-command").forEach((button) => {
    button.addEventListener("click", () => {
      const command = button.dataset.command || "python3 scripts/review_article_version.py --list";
      copyText(command).then(() => {
        button.textContent = "已复制";
      }).catch(() => {
        button.textContent = "复制失败";
      });
    });
  });
}

function bindFinalCopyButtons() {
  document.querySelectorAll(".copy-final-content").forEach((button) => {
    button.addEventListener("click", () => {
      const candidate = getFinalCandidate();
      const checklist = getFinalChecklist();
      const kind = button.dataset.copyKind || "title";
      const value = kind === "body"
        ? (candidate.wechat_body_markdown || candidate.body_markdown || "")
        : kind === "steps"
          ? (Array.isArray(checklist.manual_steps) ? checklist.manual_steps.join("\\n") : "打开工作台，人工检查 checklist，然后手动复制到公众号后台。")
          : (candidate.wechat_title || candidate.title || "");
      copyText(value).then(() => {
        button.textContent = "已复制";
      }).catch(() => {
        button.textContent = "复制失败";
      });
    });
  });
}

function bindPerformanceCommandButtons() {
  document.querySelectorAll(".copy-performance-command").forEach((button) => {
    button.addEventListener("click", () => {
      const command = button.dataset.command || "python3 scripts/create_manual_publish_session.py --list";
      copyText(command).then(() => {
        button.textContent = "已复制";
      }).catch(() => {
        button.textContent = "复制失败";
      });
    });
  });
}

function bindImageRequestButtons() {
  document.querySelectorAll(".copy-image-request").forEach((button) => {
    button.addEventListener("click", () => {
      const panel = getGenerationVisualPanel();
      const requests = Array.isArray(panel.selected_image_requests) ? panel.selected_image_requests : [];
      const first = requests[0] || {};
      const kind = button.dataset.copyImage || "prompt";
      const value = kind === "brief" ? (first.design_brief || "") : (first.image_prompt || first.design_brief || "");
      copyText(value || "暂无 image asset request。请先运行 make image-asset-requests。").then(() => {
        button.textContent = "已复制";
      }).catch(() => {
        button.textContent = "复制失败";
      });
    });
  });
}

function bindImageAssetButtons() {
  document.querySelectorAll(".copy-image-asset").forEach((button) => {
    button.addEventListener("click", () => {
      const panel = getImageAssetPanel();
      const tasks = Array.isArray(panel.manual_image_tasks) ? panel.manual_image_tasks : [];
      const task = tasks[0] || {};
      const kind = button.dataset.copyAsset || "";
      const command = button.dataset.command || "";
      const value = command || (kind === "brief"
        ? (task.design_brief || "")
        : kind === "path"
          ? (task.expected_asset_path || "")
          : (task.image_prompt || task.design_brief || ""));
      copyText(value || "暂无 Phase17 图片资产数据。请先运行 make phase17-daily。").then(() => {
        button.textContent = "已复制";
      }).catch(() => {
        button.textContent = "复制失败";
      });
    });
  });
}

function bindPublishingPackButtons() {
  document.querySelectorAll(".copy-publishing-pack").forEach((button) => {
    button.addEventListener("click", () => {
      const kind = button.dataset.copyPack || "title";
      const value = publishingPackText(kind);
      copyText(value || "暂无 Phase18 图文发布包。请先运行 make phase18-daily。").then(() => {
        button.textContent = "已复制";
      }).catch(() => {
        button.textContent = "复制失败";
      });
    });
  });
}

function renderAll() {
  renderTopbar();
  renderTopicRail();
  renderReader();
  renderInsightPanel();
  renderChiefBar();
  bindReviewCommandButtons();
  bindFinalCopyButtons();
  bindPerformanceCommandButtons();
  bindImageRequestButtons();
  bindImageAssetButtons();
  bindPublishingPackButtons();
}

document.querySelectorAll(".mode-tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    readerMode = tab.dataset.mode || "read";
    renderReader();
    bindReviewCommandButtons();
    bindFinalCopyButtons();
    bindPerformanceCommandButtons();
    bindImageRequestButtons();
    bindImageAssetButtons();
    bindPublishingPackButtons();
  });
});
document.querySelectorAll(".quick-action").forEach((button) => {
  button.addEventListener("click", () => {
    document.getElementById("chief-message").value = button.dataset.prompt || "";
    updateCommandPreview();
  });
});
document.getElementById("chief-message").addEventListener("input", updateCommandPreview);
document.getElementById("copy-command").addEventListener("click", copyCommand);
document.getElementById("preview-command").addEventListener("click", updateCommandPreview);
renderAll();
"""


def render_workbench_html(data: dict[str, Any], paths: ProjectPaths) -> str:
    article = selected_article(data)
    fallback_title = str(article.get("wechat_title") or article.get("title") or "未选择文章")
    fallback_body = markdown_to_html(str(article.get("wechat_body_markdown") or ""))
    status = data.get("system_status") if isinstance(data.get("system_status"), dict) else {}
    response, pending = latest_action_payloads(paths)
    data_json = safe_json_for_script(data)
    response_json = safe_json_for_script(response)
    pending_json = safe_json_for_script(pending)
    css = render_styles()
    scripts = render_scripts()
    actions = list_payload(pending, "actions")
    action_count = len(actions)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>同行资本 · 微信公众号内容工作台</title>
  <style>{css}</style>
</head>
<body>
  <div class="app-shell">
    <header class="topbar">
      <div class="brand-block">
        <span class="eyebrow">TH Capital Editorial Desk</span>
        <h1>同行资本 · 微信公众号内容工作台</h1>
      </div>
      <div class="status-strip" aria-label="系统状态">
        <span class="status-pill">日期 <strong id="run-date">{html.escape(str(data.get('run_date') or ''))}</strong></span>
        <span class="status-pill">Ready <strong id="ready-count">{html.escape(str((data.get('summary') or {}).get('ready_count', 0)))}</strong></span>
        <span class="status-pill">Cost <strong id="cost-status">{html.escape(str(status.get('cost_guard') or 'UNKNOWN'))}</strong></span>
        <span class="status-pill">Mode <strong id="live-mode">{html.escape(str(status.get('live_mode') or 'dry_run'))}</strong></span>
      </div>
    </header>

    <div class="workspace">
      <aside class="topic-rail" aria-label="今日推荐选题">
        <div class="rail-head">
          <h2>今日推荐选题</h2>
          <span class="count-note" id="topic-count">0 条</span>
        </div>
        <div id="topic-list">
          <button class="topic-card is-selected" type="button">
            <span class="topic-title">{html.escape(fallback_title)}</span>
            <span class="topic-meta"><span class="badge">Loading</span></span>
            <span class="topic-reason">正在载入工作台数据。</span>
          </button>
        </div>
      </aside>

      <main class="reader-wrap">
        <div class="reader-toolbar">
          <div class="mode-tabs" aria-label="阅读模式切换">
            <button class="mode-tab is-active" type="button" data-mode="read">阅读模式</button>
            <button class="mode-tab" type="button" data-mode="review">审稿模式</button>
          </div>
          <div class="selected-note" id="selected-note">{html.escape(str(article.get('article_id') or '-'))} · {html.escape(fallback_title)}</div>
        </div>
        <section class="article-shell" id="article-shell">
          <section class="article-paper">
            <h1 class="wechat-title">{html.escape(fallback_title)}</h1>
            <div class="wechat-meta"><span class="wechat-brand">同行资本</span><br>{html.escape(str(data.get('run_date') or ''))} · 本地公众号预览</div>
            <article class="article-body">{fallback_body}</article>
          </section>
        </section>
      </main>

      <aside class="insight-panel" id="insight-panel" aria-label="系统判断">
        <div class="panel-head"><h2>系统判断</h2><span class="count-note">载入中</span></div>
      </aside>
    </div>
  </div>

  <section class="chief-bar" aria-label="Chief Editor Agent">
    <div class="chief-input">
      <div class="chief-title">
        <h2>Chief Editor Agent</h2>
        <span class="target-chip" id="chief-target">目标：{html.escape(fallback_title)}</span>
      </div>
      <div class="quick-actions">
        <button class="quick-action" type="button" data-prompt="这篇文章太泛了，改成投资人视角">改成投资人视角</button>
        <button class="quick-action" type="button" data-prompt="证据太弱，请补充一手证据，优先 OpenAI 和 Anthropic">补充一手证据</button>
        <button class="quick-action" type="button" data-prompt="标题太平了，请重写三个更有判断力的标题">重写标题</button>
        <button class="quick-action" type="button" data-prompt="开头没有冲击力，请重写第一段">重写开头</button>
        <button class="quick-action" type="button" data-prompt="今天选题不好，换成 AI Agent 浏览器方向">换选题</button>
        <button class="quick-action" type="button" data-prompt="这篇可以进入发布候选，但仍需人工确认">批准</button>
        <button class="quick-action" type="button" data-prompt="这篇先搁置，等待更多证据">搁置</button>
        <button class="quick-action" type="button" data-prompt="请按内容方法论重写：增强核心判断、预期差、证据链和判断密度">按方法论重写</button>
        <button class="quick-action" type="button" data-prompt="核心判断不够清楚，请把文章收束成一句可复述的判断">增强核心判断</button>
        <button class="quick-action" type="button" data-prompt="请强化这个选题的预期差，说明市场原来以为什么、现在发生了什么变化">强化预期差</button>
        <button class="quick-action" type="button" data-prompt="请补充产业链影响，说明影响哪些公司、环节和商业模式">补产业链影响</button>
        <button class="quick-action" type="button" data-prompt="请提升开头张力，用问题、冲突或反常识判断开场">提升开头张力</button>
        <button class="quick-action" type="button" data-prompt="请提升判断密度，删掉空泛表达，把每段改成有因果、有证据、有判断">提升判断密度</button>
      </div>
      <textarea id="chief-message" placeholder="例如：这篇文章太泛了，改成投资人视角，并补充 OpenAI 和 Anthropic 最近的证据。"></textarea>
      <div class="command-row">
        <button class="primary-btn" id="copy-command" type="button">复制主编命令</button>
        <button class="secondary-btn" id="preview-command" type="button">刷新命令</button>
        <span class="command-preview" id="command-status">不会自动执行，只生成 PLAN_ONLY action plan。</span>
      </div>
      <code class="code-line" id="command-preview">python3 scripts/run_chief_editor_agent.py --message ...</code>
    </div>
    <div class="agent-memory" id="agent-memory">
      <h3>最近一次 AI 理解</h3>
      <p>载入中。当前 pending actions：{action_count}</p>
    </div>
  </section>

  <script type="application/json" id="workbench-data">{data_json}</script>
  <script type="application/json" id="chief-response-data">{response_json}</script>
  <script type="application/json" id="pending-actions-data">{pending_json}</script>
  <script>{scripts}</script>
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
