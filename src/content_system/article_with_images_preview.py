"""Render a WeChat-style article preview with image assets or placeholders."""

from __future__ import annotations

import html
from pathlib import Path
from typing import Any

from content_system.live_methodology_agent_utils import SCHEMA_VERSION
from content_system.paths import ProjectPaths
from content_system.phase7_report_utils import list_payload, read_json, repo_relative, today_token, utc_now, write_json_and_markdown
from content_system.wechat_article_preview import markdown_to_html


def output_paths(paths: ProjectPaths, run_date: str) -> dict[str, Path]:
    return {
        "dated_html": paths.frontstage_root / f"{run_date}__article-with-images-preview.html",
        "latest_html": paths.frontstage_root / "latest_article_with_images_preview.html",
        "dated_json": paths.logs_root / f"{run_date}__article-with-images-preview.json",
        "latest_json": paths.logs_root / "latest_article_with_images_preview.json",
    }


def select_article(paths: ProjectPaths) -> dict[str, Any]:
    publishing_root = paths.market_content_root / "07_publishing"
    draft_root = paths.market_content_root / "05_draft_packs"
    final_payload = read_json(publishing_root / "latest_final_article_candidates.json")
    drafts_payload = read_json(draft_root / "latest_methodology_content_drafts.json")
    final_candidates = list_payload(final_payload, "candidates")
    if final_candidates:
        item = final_candidates[0]
        return {
            "article_id": item.get("source_article_id") or item.get("final_candidate_id") or "",
            "title": item.get("wechat_title") or item.get("title") or "",
            "body_markdown": item.get("wechat_body_markdown") or item.get("body_markdown") or "",
            "source": "final_candidate",
        }
    drafts = list_payload(drafts_payload, "drafts")
    if drafts:
        item = drafts[0]
        return {
            "article_id": item.get("draft_id") or "",
            "title": item.get("selected_title") or "",
            "body_markdown": item.get("body_markdown") or "",
            "source": "methodology_draft",
        }
    return {"article_id": "", "title": "暂无文章", "body_markdown": "", "source": "none"}


def related_visuals(paths: ProjectPaths, article_id: str) -> list[dict[str, Any]]:
    draft_root = paths.market_content_root / "05_draft_packs"
    plan_payload = read_json(draft_root / "latest_article_visual_plans.json")
    request_payload = read_json(draft_root / "latest_image_asset_requests.json")
    library_payload = read_json(paths.market_content_root / "08_assets" / "image_asset_library.json")
    plans = list_payload(plan_payload, "visual_plans")
    plan = next((item for item in plans if item.get("article_id") == article_id), plans[0] if plans else {})
    visuals = plan.get("visuals") if isinstance(plan.get("visuals"), list) else []
    requests_by_visual = {str(item.get("visual_id")): item for item in list_payload(request_payload, "requests") if item.get("visual_id")}
    assets = list_payload(library_payload, "assets")
    result: list[dict[str, Any]] = []
    for visual in visuals:
        if not isinstance(visual, dict):
            continue
        request = requests_by_visual.get(str(visual.get("visual_id") or ""), {})
        asset = next(
            (
                item
                for item in assets
                if item.get("article_id") == plan.get("article_id")
                and (item.get("visual_type") == visual.get("visual_type") or item.get("visual_id") == visual.get("visual_id"))
            ),
            {},
        )
        result.append({"visual": visual, "request": request, "asset": asset})
    return result


def build_article_with_images_preview(paths: ProjectPaths, repo_root: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    run_date = today_token()
    article = select_article(paths)
    visuals = related_visuals(paths, str(article.get("article_id") or ""))
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_date": run_date,
        "article": article,
        "visual_slots": visuals,
        "summary": {
            "visual_slot_count": len(visuals),
            "available_asset_count": sum(1 for item in visuals if (item.get("asset") or {}).get("asset_status") == "AVAILABLE"),
            "placeholder_count": sum(1 for item in visuals if not item.get("asset") or (item.get("asset") or {}).get("asset_status") in {"", "PLACEHOLDER"}),
        },
        "policy": {"no_auto_image_generation": True, "no_auto_publish": True, "preview_only": True},
    }
    outputs = output_paths(paths, run_date)
    html_text = render_html(payload, paths)
    outputs["dated_html"].parent.mkdir(parents=True, exist_ok=True)
    outputs["dated_html"].write_text(html_text, encoding="utf-8")
    outputs["latest_html"].write_text(html_text, encoding="utf-8")
    json_outputs = {key: value for key, value in outputs.items() if key.endswith("_json")}
    write_json_and_markdown(payload, "", json_outputs)
    payload["outputs"] = {key: repo_relative(path, repo_root) for key, path in outputs.items()}
    return payload, outputs


def render_visual_card(slot: dict[str, Any], paths: ProjectPaths) -> str:
    visual = slot.get("visual") if isinstance(slot.get("visual"), dict) else {}
    request = slot.get("request") if isinstance(slot.get("request"), dict) else {}
    asset = slot.get("asset") if isinstance(slot.get("asset"), dict) else {}
    status = asset.get("asset_status") or "PLACEHOLDER"
    asset_path = str(asset.get("asset_path") or "")
    show_image = status == "AVAILABLE" and asset_path
    src = html.escape(asset_path)
    body = f'<img src="{src}" alt="{html.escape(str(visual.get("visual_type") or "article visual"))}">' if show_image else f"""
      <div class="visual-placeholder-label">Image placeholder</div>
      <div class="visual-placeholder-type">{html.escape(str(visual.get('visual_type') or request.get('visual_type') or 'visual'))}</div>
      <p>{html.escape(str(visual.get('information_job') or request.get('design_brief') or '等待人工生成或上传图片资产。'))}</p>
    """
    return f"""<section class="visual-card">
      {body}
      <dl>
        <dt>Placement</dt><dd>{html.escape(str(visual.get('placement') or '-'))}</dd>
        <dt>Supports claim</dt><dd>{html.escape(str(visual.get('supports_claim') or '-'))}</dd>
        <dt>Asset status</dt><dd>{html.escape(status)}</dd>
        <dt>Prompt / brief</dt><dd>{html.escape(str(request.get('image_prompt') or request.get('design_brief') or '')[:280])}</dd>
      </dl>
    </section>"""


def render_html(payload: dict[str, Any], paths: ProjectPaths) -> str:
    article = payload.get("article") if isinstance(payload.get("article"), dict) else {}
    title = str(article.get("title") or "暂无文章")
    visual_cards = "\n".join(render_visual_card(slot, paths) for slot in payload.get("visual_slots", [])) or '<section class="visual-card"><p>暂无图片规划。运行 make phase15-daily / make phase17-daily 后会显示图片占位。</p></section>'
    body_html = markdown_to_html(str(article.get("body_markdown") or ""))
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} · 图文预览</title>
  <style>
    body {{ margin:0; background:#f6f3ee; color:#1f2933; font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",system-ui,sans-serif; }}
    main {{ max-width: 820px; margin: 0 auto; padding: 34px 18px 70px; }}
    article {{ background:#fff; border:1px solid #e7e2d8; border-radius:8px; padding:38px 42px; box-shadow:0 20px 60px rgba(79,70,58,.12); }}
    h1 {{ font-size:28px; line-height:1.38; margin:0 0 12px; }}
    .meta {{ color:#8a8f98; font-size:14px; margin-bottom:28px; }}
    .article-body p,.article-body li {{ font-size:16.5px; line-height:1.95; }}
    .article-body h2 {{ margin-top:34px; font-size:20px; }}
    .visual-card {{ margin:24px 0; padding:18px; border:1px dashed #d8d0c2; border-radius:8px; background:#faf8f4; }}
    .visual-card img {{ display:block; max-width:100%; border-radius:6px; margin:0 auto 12px; }}
    .visual-placeholder-label {{ color:#1f7a5c; font-size:12px; font-weight:700; }}
    .visual-placeholder-type {{ margin:6px 0; font-size:18px; font-weight:760; }}
    dl {{ display:grid; grid-template-columns: 120px 1fr; gap:6px 12px; margin:12px 0 0; color:#4b5563; font-size:13px; }}
    dt {{ color:#6b7280; }}
  </style>
</head>
<body>
<main>
  <article>
    <h1>{html.escape(title)}</h1>
    <div class="meta">同行资本 · 本地图文预览 · 不自动发布</div>
    {visual_cards}
    <div class="article-body">{body_html}</div>
  </article>
</main>
</body>
</html>
"""
