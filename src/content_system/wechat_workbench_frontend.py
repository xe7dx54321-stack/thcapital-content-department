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
    shell.innerHTML = `<section class="review-mode">
      <div class="review-grid">
        <div class="review-card"><p class="review-label">质量分</p><p class="review-value">${escapeHtml(article.quality_score || 0)}</p></div>
        <div class="review-card"><p class="review-label">状态</p><p class="review-value"><span class="badge ${statusClass(article.status)}">${escapeHtml(statusLabel(article.status))}</span></p></div>
        <div class="review-card"><p class="review-label">Judge 决策</p><p class="review-value">${escapeHtml(shortText(article.judge_decision))}</p></div>
        <div class="review-card"><p class="review-label">发布候选</p><p class="review-value">${escapeHtml(shortText(article.publishing_candidate_id, "尚未进入发布候选"))}</p></div>
        <div class="review-card wide"><p class="review-label">Critic 摘要</p><p class="review-value">${escapeHtml(shortText(article.critic_summary))}</p></div>
        <div class="review-card wide"><p class="review-label">Revision 建议</p><p class="review-value">${escapeHtml(shortText(article.revision_summary))}</p></div>
        <div class="review-card wide"><p class="review-label">Evidence</p>${renderMiniList(article.evidence_ids, "暂无 evidence")}</div>
        <div class="review-card wide"><p class="review-label">Source</p>${renderMiniList(article.source_ids, "暂无 source")}</div>
      </div>
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

function renderInsightPanel() {
  const article = getSelectedArticle();
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

function renderAll() {
  renderTopbar();
  renderTopicRail();
  renderReader();
  renderInsightPanel();
  renderChiefBar();
}

document.querySelectorAll(".mode-tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    readerMode = tab.dataset.mode || "read";
    renderReader();
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
