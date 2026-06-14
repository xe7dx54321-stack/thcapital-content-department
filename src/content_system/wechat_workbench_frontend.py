"""Build the static WeChat workbench frontend with a clean IA."""

from __future__ import annotations

import html
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import read_json, repo_relative, today_token
from content_system.wechat_article_preview import markdown_to_html
from content_system.workbench_view_model import build_workbench_view_model


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


def esc(value: Any) -> str:
    return html.escape(str(value or ""))


def safe_json_for_script(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")


def status_tone(status: Any) -> str:
    text = str(status or "").upper()
    if text in {"READY_TO_REVIEW", "NORMAL", "READY", "PASS", "GO_LIVE_APPROVED", "SUCCESS"}:
        return "good"
    if text in {"NEEDS_ATTENTION", "WARNING", "NEEDS_REVISION", "ACTIONABLE", "GO_LIVE_WITH_WARNINGS", "REVISED"}:
        return "warn"
    if text in {"SYSTEM_ISSUE", "ERROR", "FAIL", "BLOCKED"}:
        return "bad"
    return "muted"


def list_items(items: list[Any], empty: str = "暂无") -> str:
    rows = [f"<li>{esc(item)}</li>" for item in items if str(item or "").strip()]
    if not rows:
        return f"<p class=\"muted\">{esc(empty)}</p>"
    return "<ul class=\"clean-list\">" + "".join(rows) + "</ul>"


def metric(label: str, value: Any, tone: str = "muted") -> str:
    return f"""
    <div class="metric {tone}">
      <span>{esc(label)}</span>
      <strong>{esc(value)}</strong>
    </div>
    """


def render_styles() -> str:
    return """
:root {
  color-scheme: light;
  --bg: #f7f7f5;
  --surface: #ffffff;
  --surface-soft: #f3f4f2;
  --text: #1f2933;
  --muted: #68727f;
  --border: #e4e7e2;
  --good: #177245;
  --good-bg: #e8f5ee;
  --warn: #95610a;
  --warn-bg: #fff5dc;
  --bad: #a63a2c;
  --bad-bg: #fff0ed;
  --ink: #17202a;
  --shadow: 0 20px 50px rgba(20, 28, 35, .08);
}
* { box-sizing: border-box; }
html { min-height: 100%; scroll-behavior: smooth; }
body {
  margin: 0;
  min-height: 100%;
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
  letter-spacing: 0;
}
button, textarea { font: inherit; letter-spacing: 0; }
button { cursor: pointer; }
.shell { max-width: 1180px; margin: 0 auto; padding: 22px 22px 80px; }
.topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  background: rgba(247, 247, 245, .92);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border);
}
.topbar-inner {
  max-width: 1180px;
  margin: 0 auto;
  padding: 16px 22px 12px;
}
.brand-row { display: flex; align-items: end; justify-content: space-between; gap: 18px; }
.eyebrow { color: var(--muted); font-size: 12px; font-weight: 700; }
h1, h2, h3, p { margin-top: 0; }
h1 { margin-bottom: 3px; font-size: 22px; line-height: 1.3; }
.page-note { margin: 0; color: var(--muted); font-size: 13px; }
.nav {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 14px;
}
.nav button {
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--muted);
  min-height: 34px;
  padding: 6px 13px;
  border-radius: 999px;
}
.nav button.active { background: var(--ink); color: #fff; border-color: var(--ink); }
.view { display: none; padding-top: 22px; }
.view.active { display: block; }
.section-head { display: flex; justify-content: space-between; align-items: start; gap: 18px; margin-bottom: 16px; }
.section-head h2 { margin-bottom: 5px; font-size: 22px; }
.muted { color: var(--muted); }
.grid { display: grid; gap: 14px; }
.grid.two { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }
.grid.three { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 18px;
  box-shadow: 0 8px 24px rgba(20, 28, 35, .04);
}
.hero-card { padding: 24px; box-shadow: var(--shadow); }
.label { color: var(--muted); font-size: 12px; font-weight: 750; text-transform: uppercase; }
.value { font-size: 16px; line-height: 1.7; }
.status-bar { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 10px; margin-bottom: 14px; }
.status-chip {
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 12px;
  background: var(--surface);
}
.status-chip span { display: block; color: var(--muted); font-size: 12px; margin-bottom: 3px; }
.status-chip strong { font-size: 15px; }
.good { color: var(--good); }
.warn { color: var(--warn); }
.bad { color: var(--bad); }
.status-chip.good, .metric.good, .pill.good { background: var(--good-bg); border-color: rgba(23,114,69,.18); color: var(--good); }
.status-chip.warn, .metric.warn, .pill.warn { background: var(--warn-bg); border-color: rgba(149,97,10,.2); color: var(--warn); }
.status-chip.bad, .metric.bad, .pill.bad { background: var(--bad-bg); border-color: rgba(166,58,44,.2); color: var(--bad); }
.actions { display: flex; flex-wrap: wrap; gap: 9px; margin-top: 16px; }
.btn {
  min-height: 36px;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 7px 12px;
  background: var(--surface);
  color: var(--text);
}
.btn.primary { background: var(--ink); color: #fff; border-color: var(--ink); }
.btn.warn { background: var(--warn-bg); border-color: rgba(149,97,10,.25); }
.btn.bad { background: var(--bad-bg); border-color: rgba(166,58,44,.25); }
.alert-list { display: grid; gap: 8px; }
.alert {
  border-radius: 8px;
  border: 1px solid var(--border);
  padding: 10px 12px;
  background: var(--surface-soft);
}
.alert.ok { background: var(--good-bg); color: var(--good); }
.alert.warning { background: var(--warn-bg); color: var(--warn); }
.alert.info { background: #eef4ff; color: #335b8e; }
.article-shell {
  max-width: 760px;
  margin: 0 auto;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 34px 42px 44px;
  box-shadow: var(--shadow);
}
.article-title { font-size: 28px; line-height: 1.32; margin-bottom: 8px; }
.article-meta { color: var(--muted); font-size: 13px; margin-bottom: 26px; }
.article-body { font-size: 16px; line-height: 1.88; }
.article-body h1 { display: none; }
.article-body h2 { font-size: 21px; margin: 34px 0 12px; }
.article-body h3 { font-size: 18px; margin: 28px 0 10px; }
.article-body p { margin: 14px 0; }
.article-body li { margin: 7px 0; }
.decision-list { display: grid; gap: 10px; }
.decision-row { display: grid; grid-template-columns: 160px minmax(0, 1fr); gap: 12px; }
.clean-list { margin: 8px 0 0; padding-left: 20px; line-height: 1.7; }
details {
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px 14px;
  background: var(--surface);
}
details + details { margin-top: 10px; }
summary { cursor: pointer; font-weight: 720; }
.check-row {
  display: grid;
  grid-template-columns: 220px 86px minmax(0, 1fr);
  gap: 12px;
  align-items: start;
  border-top: 1px solid var(--border);
  padding: 12px 0;
}
.check-row:first-child { border-top: 0; }
.pill {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  border: 1px solid var(--border);
  border-radius: 999px;
  min-height: 24px;
  padding: 3px 8px;
  font-size: 12px;
  font-weight: 750;
}
.metric {
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px;
  background: var(--surface-soft);
}
.metric span { display: block; color: var(--muted); font-size: 12px; margin-bottom: 5px; }
.metric strong { font-size: 21px; }
.day-card { border-top: 1px solid var(--border); padding: 12px 0; }
.day-card:first-child { border-top: 0; }
.day-title { display: flex; justify-content: space-between; gap: 12px; align-items: start; }
.ops-table { display: grid; gap: 10px; }
.ops-row { display: grid; grid-template-columns: 190px minmax(0, 1fr); gap: 12px; border-top: 1px solid var(--border); padding-top: 10px; }
.debug-actions .btn { margin: 0 7px 7px 0; }
.toast {
  position: fixed;
  left: 50%;
  bottom: 22px;
  transform: translateX(-50%);
  background: var(--ink);
  color: #fff;
  border-radius: 999px;
  padding: 10px 14px;
  opacity: 0;
  pointer-events: none;
  transition: opacity .16s ease;
}
.toast.show { opacity: 1; }
@media (max-width: 860px) {
  .shell, .topbar-inner { padding-left: 14px; padding-right: 14px; }
  .status-bar, .grid.two, .grid.three { grid-template-columns: 1fr; }
  .article-shell { padding: 24px 18px 34px; }
  .decision-row, .check-row, .ops-row { grid-template-columns: 1fr; }
}
"""


def render_today_overview(vm: dict[str, Any]) -> str:
    overview = vm["today_overview"]
    alerts = "".join(f"<div class=\"alert {esc(item.get('level'))}\">{esc(item.get('message'))}</div>" for item in overview.get("alerts", []))
    return f"""
    <section class="view active" id="view-overview" data-view="overview">
      <div class="section-head">
        <div><h2>今日总览</h2><p class="page-note">只看今天结论：系统是否正常、有没有候选稿、是否值得打开。</p></div>
      </div>
      <div class="status-bar">
        <div class="status-chip {status_tone(overview.get('overall_status'))}"><span>今日状态</span><strong>{esc(overview.get('overall_status_zh'))}</strong></div>
        <div class="status-chip {status_tone(overview.get('system_status'))}"><span>系统运行</span><strong>{esc(overview.get('system_status_zh'))}</strong></div>
        <div class="status-chip {status_tone(overview.get('candidate_status'))}"><span>候选稿</span><strong>{esc(overview.get('candidate_status_zh'))}</strong></div>
        <div class="status-chip {status_tone(overview.get('quality_status'))}"><span>质量结果</span><strong>{esc(overview.get('quality_status_zh'))}</strong></div>
        <div class="status-chip"><span>下一次自动运行</span><strong>{esc(overview.get('next_scheduled_run') or '待调度')}</strong></div>
      </div>
      <div class="grid two">
        <article class="card hero-card">
          <p class="label">今日最终结论</p>
          <div class="decision-list">
            <div class="decision-row"><strong>今日主选题</strong><span>{esc(overview.get('main_topic'))}</span></div>
            <div class="decision-row"><strong>推荐标题</strong><span>{esc(overview.get('recommended_title'))}</span></div>
            <div class="decision-row"><strong>一句话判断</strong><span>{esc(overview.get('one_sentence_judgement'))}</span></div>
            <div class="decision-row"><strong>为什么值得看</strong><span>{esc(overview.get('why_worth_reading'))}</span></div>
            <div class="decision-row"><strong>最大风险</strong><span>{esc(overview.get('main_risk'))}</span></div>
            <div class="decision-row"><strong>建议动作</strong><span>{esc(overview.get('recommended_action'))}</span></div>
          </div>
          <div class="actions">
            <button class="btn primary" type="button" data-jump="article">查看今日稿件</button>
            <button class="btn" type="button" data-jump="quality">查看质量检查</button>
            <button class="btn" type="button" data-refresh>刷新状态</button>
            <button class="btn warn" type="button" data-api="/api/runtime/run-daily" data-confirm="确认手动补跑今日内容生产？">手动补跑今日内容生产</button>
          </div>
        </article>
        <aside class="card">
          <p class="label">今日简要告警</p>
          <div class="alert-list">{alerts}</div>
        </aside>
      </div>
    </section>
    """


def render_today_article(vm: dict[str, Any]) -> str:
    article = vm["today_article"]
    review = article.get("agent_review_summary", {})
    body_html = markdown_to_html(str(article.get("article_markdown") or ""))
    return f"""
    <section class="view" id="view-article" data-view="article">
      <div class="section-head">
        <div><h2>今日稿件</h2><p class="page-note">这里只放今天候选稿和审稿意见，不放系统日志。</p></div>
      </div>
      <div class="grid two">
        <div class="card">
          <p class="label">稿件头部</p>
          <h3>{esc(article.get('title') or '暂无标题')}</h3>
          <p class="muted">{esc(article.get('subtitle'))}</p>
          <div class="decision-list">
            <div class="decision-row"><strong>主选题</strong><span>{esc(article.get('topic'))}</span></div>
            <div class="decision-row"><strong>生成时间</strong><span>{esc(article.get('generated_at'))}</span></div>
            <div class="decision-row"><strong>状态</strong><span>{esc(article.get('status_zh') or article.get('status'))}</span></div>
            <div class="decision-row"><strong>质量评级</strong><span>{esc(article.get('quality_rating'))}</span></div>
          </div>
        </div>
        <div class="card">
          <p class="label">人工判断</p>
          <div class="decision-list">
            <div class="decision-row"><strong>是否值得读</strong><span>{'是' if article.get('quality_rating') in {'PASS', 'ACTIONABLE'} else '待确认'}</span></div>
            <div class="decision-row"><strong>是否可进入人工修改</strong><span>{'是' if article.get('status') else '否'}</span></div>
            <div class="decision-row"><strong>主要优点</strong><span>{esc('；'.join(review.get('strengths') or []) or '结构完整，保留了人工复核边界。')}</span></div>
            <div class="decision-row"><strong>主要问题</strong><span>{esc(review.get('core_issue'))}</span></div>
            <div class="decision-row"><strong>建议修改方向</strong><span>{esc(review.get('recommendation'))}</span></div>
          </div>
        </div>
      </div>
      <div class="article-shell" style="margin-top:16px">
        <h1 class="article-title">{esc(article.get('title'))}</h1>
        <div class="article-meta">本地候选稿 · 人工审阅后才可进入发布准备</div>
        <article class="article-body">{body_html}</article>
      </div>
      <div class="card" style="margin-top:16px">
        <p class="label">Agent 审稿摘要</p>
        <p><strong>Agent 判断：</strong>{esc(review.get('decision'))} · <strong>核心问题：</strong>{esc(review.get('core_issue'))} · <strong>建议：</strong>{esc(review.get('recommendation'))}</p>
        <details>
          <summary>展开详细 proponent / critic / judge / rewrite</summary>
          <pre>{esc(json.dumps(review.get('details') or {}, ensure_ascii=False, indent=2))}</pre>
        </details>
        <div class="actions">
          <button class="btn" type="button" data-copy="article-body">复制正文</button>
          <button class="btn" type="button" data-copy-value="{esc(article.get('title'))}">复制标题</button>
          <button class="btn" type="button" data-placeholder>标记为值得人工修改</button>
          <button class="btn" type="button" data-placeholder>标记为放弃</button>
          <button class="btn" type="button" data-placeholder>请求重写标题</button>
          <button class="btn" type="button" data-placeholder>请求换角度</button>
        </div>
      </div>
    </section>
    """


def render_quality(vm: dict[str, Any]) -> str:
    quality = vm["quality_check"]
    evidence = quality.get("evidence_summary", {})
    checklist = "".join(
        f"<div class=\"check-row\"><strong>{esc(item.get('label'))}</strong><span class=\"pill {status_tone(item.get('status'))}\">{esc(item.get('status_zh') or item.get('status'))}</span><span>{esc(item.get('reason'))}</span></div>"
        for item in quality.get("checklist", [])
    )
    return f"""
    <section class="view" id="view-quality" data-view="quality">
      <div class="section-head"><div><h2>质量检查</h2><p class="page-note">这里只看内容质量、证据质量和人工审核清单。</p></div></div>
      <div class="grid three">
        {metric('质量评级', quality.get('rating_zh') or quality.get('rating'), status_tone(quality.get('rating')))}
        {metric('阻断问题', quality.get('blocking_issue_count'), 'bad' if quality.get('blocking_issue_count') else 'good')}
        {metric('非阻断警告', quality.get('warning_count'), 'warn' if quality.get('warning_count') else 'good')}
      </div>
      <div class="card" style="margin-top:14px">
        <p class="label">核心 checklist</p>
        {checklist or '<p class="muted">暂无质量检查。</p>'}
      </div>
      <div class="grid two" style="margin-top:14px">
        <div class="card">
          <p class="label">证据检查</p>
          <div class="decision-list">
            <div class="decision-row"><strong>核心证据数量</strong><span>{esc(evidence.get('core_evidence_count'))}</span></div>
            <div class="decision-row"><strong>一手来源数量</strong><span>{esc(evidence.get('primary_source_count'))}</span></div>
            <div class="decision-row"><strong>二手来源数量</strong><span>{esc(evidence.get('secondary_source_count'))}</span></div>
            <div class="decision-row"><strong>弱信号数量</strong><span>{esc(evidence.get('weak_signal_count'))}</span></div>
          </div>
          <p class="muted">{esc(evidence.get('note'))}</p>
          <p class="label">需要人工确认的证据</p>
          {list_items(evidence.get('needs_human_confirmation') or [], '暂无需要人工确认的证据')}
        </div>
        <div class="card">
          <p class="label">人工审阅清单</p>
          {list_items(quality.get('human_review_checklist') or [])}
        </div>
      </div>
    </section>
    """


def render_replay(vm: dict[str, Any]) -> str:
    replay = vm["replay_dashboard"]
    summary = replay.get("summary", {})
    day_rows = ""
    for day in replay.get("days", []):
        flags = []
        if day.get("duplicate_topic"):
            flags.append("重复选题风险")
        if day.get("source_metadata_title"):
            flags.append("source metadata 标题")
        if day.get("low_evidence_selected"):
            flags.append("证据偏弱")
        day_rows += f"""
        <details class="day-card">
          <summary>{esc(day.get('business_date'))} · {esc(day.get('topic_title'))} · {esc(day.get('quality_status'))}</summary>
          <p><strong>是否值得看：</strong>{'是' if day.get('worth_reading') else '待确认'} · <strong>主要问题：</strong>{esc('，'.join(flags) or '暂无明显问题')}</p>
          <p class="muted">Brief / Outline / Draft / Review / Human checklist 已保存在 replay namespace；此处只展示结论，不污染今日稿件。</p>
        </details>
        """
    proposal_rows = ""
    for item in replay.get("calibration_proposals", []):
        proposal_rows += f"""
        <div class="card">
          <p class="label">{esc(item.get('proposal_type') or '校准建议')} · {esc(item.get('severity'))}</p>
          <p>{esc(item.get('reason') or item.get('expected_effect'))}</p>
          <p class="muted">目标配置：{esc(item.get('target_config'))} · 自动应用：否，需要人工确认。</p>
        </div>
        """
    return f"""
    <section class="view" id="view-replay" data-view="replay">
      <div class="section-head"><div><h2>历史回放</h2><p class="page-note">Phase33 7 天压缩回放，只做校准分析，不代表今天正式产出。</p></div></div>
      <div class="grid three">
        {metric('回放天数', summary.get('replay_ready_days'), 'good')}
        {metric('选出主选题天数', summary.get('selected_days'), 'good')}
        {metric('生成候选稿数', summary.get('final_candidate_count'), 'good')}
        {metric('质量 PASS 天数', summary.get('pass_days'), 'good')}
        {metric('重复选题风险', summary.get('duplicate_topic_ratio'), 'warn')}
        {metric('校准建议数量', summary.get('proposal_count'), 'warn' if summary.get('proposal_count') else 'good')}
      </div>
      <div class="card" style="margin-top:14px">
        <p class="label">每日卡片</p>
        {day_rows or '<p class="muted">暂无 7 天回放。</p>'}
      </div>
      <div class="grid two" style="margin-top:14px">
        {proposal_rows or '<div class="card"><p class="muted">暂无校准建议。这些建议不会自动应用。</p></div>'}
      </div>
    </section>
    """


def render_system_ops(vm: dict[str, Any]) -> str:
    ops = vm["system_ops"]
    runtime = ops.get("runtime", {})
    launch = ops.get("launchagent", {})
    jobs = ops.get("jobs", {})
    acquisition = ops.get("acquisition", {})
    openclaw = ops.get("openclaw", {})
    debug_buttons = "".join(
        f"<button class=\"btn {'bad' if item.get('dangerous') else ''}\" type=\"button\" data-api=\"{esc(item.get('endpoint'))}\" data-confirm=\"{'确认执行：' + esc(item.get('label')) if item.get('dangerous') else ''}\">{esc(item.get('label'))}</button>"
        for item in ops.get("debug_actions", [])
    )
    lane_rows = [f"{item.get('time')} · {item.get('lane')} · {item.get('next_action')}" for item in acquisition.get("next_lanes", [])]
    return f"""
    <section class="view" id="view-system" data-view="system">
      <div class="section-head"><div><h2>系统运维</h2><p class="page-note">Runtime、LaunchAgent、OpenClaw、日志和调试动作集中放在这里。</p></div></div>
      <div class="grid two">
        <div class="card">
          <p class="label">系统健康</p>
          <div class="ops-table">
            <div class="ops-row"><strong>Runtime 状态</strong><span>{esc(runtime.get('status'))}</span></div>
            <div class="ops-row"><strong>Runtime PID</strong><span>{esc(runtime.get('pid'))}</span></div>
            <div class="ops-row"><strong>Heartbeat age</strong><span>{esc(runtime.get('heartbeat_age_seconds'))} 秒</span></div>
            <div class="ops-row"><strong>Next scheduled run</strong><span>{esc(runtime.get('next_scheduled_run'))}</span></div>
            <div class="ops-row"><strong>Go-Live Gate</strong><span>{esc(runtime.get('go_live_gate'))} · blocking {esc(runtime.get('blocking_failures'))}</span></div>
          </div>
        </div>
        <div class="card">
          <p class="label">LaunchAgent</p>
          <div class="ops-table">
            <div class="ops-row"><strong>installed / loaded / enabled</strong><span>{esc(launch.get('installed'))} / {esc(launch.get('loaded'))} / {esc(launch.get('enabled'))}</span></div>
            <div class="ops-row"><strong>plist</strong><span>{esc(launch.get('plist_path'))}</span></div>
          </div>
        </div>
      </div>
      <div class="grid two" style="margin-top:14px">
        <div class="card">
          <p class="label">今日任务状态</p>
          <div class="ops-table">
            <div class="ops-row"><strong>成功 / 失败 / 等待</strong><span>{esc((jobs.get('ledger') or {}).get('success', 0))} / {esc((jobs.get('ledger') or {}).get('failed', 0))} / {esc((jobs.get('ledger') or {}).get('pending', 0))}</span></div>
            <div class="ops-row"><strong>重试队列</strong><span>{esc((jobs.get('retry') or {}).get('retry_count', 0))}</span></div>
            <div class="ops-row"><strong>missed-run catch-up</strong><span>{esc((jobs.get('missed_run') or {}).get('catchup_count', 0))}</span></div>
          </div>
        </div>
        <div class="card">
          <p class="label">数据采集状态</p>
          <div class="ops-table">
            <div class="ops-row"><strong>网络 readiness</strong><span>{esc((acquisition.get('network') or {}).get('status', 'UNKNOWN'))}</span></div>
            <div class="ops-row"><strong>connector runs</strong><span>{esc((acquisition.get('runtime_plan') or {}).get('connector_runs', 0))}</span></div>
            <div class="ops-row"><strong>下一轮采集</strong><span>{esc('；'.join(lane_rows[:3]) or '暂无')}</span></div>
          </div>
        </div>
      </div>
      <div class="grid two" style="margin-top:14px">
        <div class="card">
          <p class="label">OpenClaw 共存状态</p>
          <div class="ops-table">
            <div class="ops-row"><strong>conflict_count</strong><span>{esc(openclaw.get('conflict_count'))}</span></div>
            <div class="ops-row"><strong>manual_review_count</strong><span>{esc(openclaw.get('manual_review_count'))}</span></div>
            <div class="ops-row"><strong>safe_to_disable</strong><span>{esc(openclaw.get('safe_to_disable'))}</span></div>
            <div class="ops-row"><strong>gateway / cron</strong><span>未修改 / 未修改</span></div>
          </div>
        </div>
        <div class="card debug-actions">
          <p class="label">调试工具</p>
          <details>
            <summary>展开 Runtime 调试按钮</summary>
            <div style="margin-top:12px">{debug_buttons}</div>
          </details>
        </div>
      </div>
    </section>
    """


def render_scripts(view_model: dict[str, Any]) -> str:
    return f"""
const viewModel = JSON.parse(document.getElementById("view-model-data").textContent || "{{}}");
function showToast(message) {{
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 1800);
}}
function activate(view) {{
  document.querySelectorAll(".nav button").forEach((button) => button.classList.toggle("active", button.dataset.view === view));
  document.querySelectorAll(".view").forEach((section) => section.classList.toggle("active", section.dataset.view === view));
}}
document.querySelectorAll("[data-view]").forEach((button) => {{
  if (button.tagName === "BUTTON") button.addEventListener("click", () => activate(button.dataset.view));
}});
document.querySelectorAll("[data-jump]").forEach((button) => button.addEventListener("click", () => activate(button.dataset.jump)));
document.querySelectorAll("[data-refresh]").forEach((button) => button.addEventListener("click", () => window.location.reload()));
document.querySelectorAll("[data-copy]").forEach((button) => button.addEventListener("click", async () => {{
  const article = viewModel.today_article || {{}};
  await navigator.clipboard.writeText(article.article_markdown || "");
  showToast("正文已复制");
}}));
document.querySelectorAll("[data-copy-value]").forEach((button) => button.addEventListener("click", async () => {{
  await navigator.clipboard.writeText(button.dataset.copyValue || "");
  showToast("标题已复制");
}}));
document.querySelectorAll("[data-placeholder]").forEach((button) => button.addEventListener("click", () => showToast("已记录为安全占位：不会自动执行。")));
document.querySelectorAll("[data-api]").forEach((button) => button.addEventListener("click", async () => {{
  const confirmText = button.dataset.confirm || "";
  if (confirmText && !window.confirm(confirmText)) return;
  const endpoint = button.dataset.api;
  if (endpoint === "/api/workbench-data") {{
    window.location.reload();
    return;
  }}
  try {{
    const response = await fetch(endpoint, {{ method: "POST", headers: {{ "Content-Type": "application/json" }}, body: "{{}}" }});
    showToast(response.ok ? "命令已发送到本地 Runtime Control" : "命令失败，请查看系统运维");
  }} catch (error) {{
    showToast("本地控制服务不可用");
  }}
}}));
activate("overview");
console.log("Phase33B Workbench IA loaded");
"""


def render_workbench_html(data: dict[str, Any], paths: ProjectPaths) -> str:
    view_model = build_workbench_view_model(paths, data)
    run_date = str(view_model.get("run_date") or data.get("run_date") or today_token())
    vm_json = safe_json_for_script(view_model)
    nav = """
      <button class="active" type="button" data-view="overview">今日总览</button>
      <button type="button" data-view="article">今日稿件</button>
      <button type="button" data-view="quality">质量检查</button>
      <button type="button" data-view="replay">历史回放</button>
      <button type="button" data-view="system">系统运维</button>
    """
    html_text = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>同行资本内容工厂 · Workbench</title>
  <style>{render_styles()}</style>
</head>
<body>
  <header class="topbar">
    <div class="topbar-inner">
      <div class="brand-row">
        <div>
          <div class="eyebrow">TH Capital Content Factory</div>
          <h1>同行资本内容工厂</h1>
          <p class="page-note">运营控制台 · {esc(run_date)} · 本地预览不会自动发布</p>
        </div>
      </div>
      <nav class="nav" aria-label="Workbench 主导航">{nav}</nav>
    </div>
  </header>
  <main class="shell">
    {render_today_overview(view_model)}
    {render_today_article(view_model)}
    {render_quality(view_model)}
    {render_replay(view_model)}
    {render_system_ops(view_model)}
  </main>
  <div class="toast" id="toast" role="status" aria-live="polite"></div>
  <script>window.__workbenchConsoleErrors = []; window.addEventListener("error", (event) => window.__workbenchConsoleErrors.push(event.message || "error")); window.addEventListener("unhandledrejection", (event) => window.__workbenchConsoleErrors.push(String(event.reason || "unhandledrejection"))); </script>
  <script type="application/json" id="view-model-data">{vm_json}</script>
  <script>{render_scripts(view_model)}</script>
</body>
</html>
"""
    return html_text


def build_wechat_workbench_frontend(paths: ProjectPaths, repo_root: Path) -> WechatWorkbenchFrontendResult:
    data = read_json(paths.frontstage_root / "latest_wechat_workbench_data.json")
    if not data:
        data = {"run_date": today_token(), "topics": [], "articles": [], "selected_article_id": "", "system_status": {}}
    data["workbench_view_model"] = build_workbench_view_model(paths, data)
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
