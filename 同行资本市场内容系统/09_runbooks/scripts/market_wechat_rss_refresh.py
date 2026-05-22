#!/usr/bin/env python3
"""
market_wechat_rss_refresh.py
微信公众账号 RSS / 搜索刷新轮。
Batch A = 强链主账号（早轮）;  Batch B = 弱/无效账号补轮（傍晚）。
只做内容工厂自己的 feed 刷新，不写 topic_candidate / draft。
"""
import argparse, os, re, sys, json
from datetime import datetime
from pathlib import Path

_REPO_ROOT = None
for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "content_system" / "paths.py").exists():
        _REPO_ROOT = _parent
        sys.path.insert(0, str(_parent / "src"))
        break
if _REPO_ROOT is None:
    raise RuntimeError("Cannot locate repository root")
from content_system.paths import get_project_paths

ROOT        = str(get_project_paths(_REPO_ROOT).market_content_root)
SRC_DIR     = os.path.join(ROOT, "02_topic_radar", "source_packets")
LOG_DIR     = os.path.join(ROOT, "10_logs")
DATE_ID     = datetime.now().strftime("%Y%m%d")
TODAY_STR   = datetime.now().strftime("%Y-%m-%d")
NOW_HR      = datetime.now().strftime("%Y-%m-%d %H:%M")

# ── Batch 定义 ────────────────────────────────────────────────────────────────
BATCH_A = {
    "wechat__liangziwei":          "量子位",
    "wechat__xinzhiyuan":          "新智元",
    "wechat__jiqizhixin":          "机器之心",
    "wechat__zhidx":               "智东西",
    "wechat__36kr":                "36氪",
    "wechat__ifanr":               "爱范儿",
    "wechat__geekpark":            "极客公园",
    "wechat__founder_park":        "Founder Park",
    "wechat__appsso":              "AppSo",
    "wechat__guiguang_ai_tools":   "硅星人",
}
BATCH_B = {
    "wechat__guixingren_pro":      "硅谷好人Pro",
    "wechat__saibo_chanxin":       "赛博信新",
    "wechat__digital_life_khazix": "Digital Life Khazix",
    "wechat__bingan_gege_agi":    "冰岩AI",
    "wechat__kangaroo_ai_inn":    "Kangaroo AI Inn",
}
BATCH_C_RAW = {
    "wechat__guixingren_pro":      "硅谷好人Pro",
    "wechat__saibo_chanxin":       "赛博信新",
    "wechat__digital_life_khazix": "Digital Life Khazix",
    "wechat__bingan_gege_agi":    "冰岩AI",
    "wechat__kangaroo_ai_inn":    "Kangaroo AI Inn",
    "wechat__liangziwei":          "量子位",
    "wechat__xinzhiyuan":          "新智元",
}

BATCH_MAP = {
    "a": (BATCH_A,    "Batch A 强链主账号"),
    "b": (BATCH_B,    "Batch B 弱/无效账号补轮（傍晚）"),
    "c": (BATCH_C_RAW,"Batch C 全量账号"),
    "all": (dict(list(BATCH_A.items()) + list(BATCH_B.items())),
            "All 有效账号 (A+B)"),
}

# ── Helper ───────────────────────────────────────────────────────────────────
def jina_read(url, timeout=30):
    """用 jina.ai reader 把 URL 转成 markdown 文本"""
    import subprocess
    cmd = [
        "curl", "-s", "--max-time", str(timeout),
        "-H", "Accept: text/markdown",
        f"https://r.jina.ai/{url}",
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout + 10)
        if r.returncode == 0 and r.stdout:
            return r.stdout.decode("utf-8", errors="replace")
    except Exception:
        pass
    return ""

def web_search(query, count=5):
    """通过 jina search 端做轻量搜索（返回 markdown 摘要）"""
    import subprocess
    url = f"https://s.jina.ai/{query}"
    cmd = [
        "curl", "-s", "--max-time", "20",
        "-H", "Accept: text/markdown",
        url,
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=30)
        if r.returncode == 0 and r.stdout:
            return r.stdout.decode("utf-8", errors="replace")[:3000]
    except Exception:
        pass
    return ""

def strip_frontmatter(text):
    if not isinstance(text, str):
        return text
    return re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL).strip()

def clean_body(text):
    if not isinstance(text, str):
        return ""
    text = strip_frontmatter(text)
    text = re.sub(r'\[?(?:广告|Advertisement|闭上|关闭)\]?', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def truncate(text, max_chars=400):
    if not isinstance(text, str):
        return ""
    text = text.strip()
    return text[:max_chars] + ("..." if len(text) > max_chars else "")

# ── Per-account capture ──────────────────────────────────────────────────────
def capture_account(account_id, account_name, window="T日"):
    """
    对单个公众号账号做 RSS 刷新，返回 (summary_lines, status, found_urls)
    """
    label = f"{account_name} {window}"
    print(f"  [{account_id}] {account_name} …")

    # 用 jina search 搜 "公众号名 + AI/融资/产品" 当天文章
    query = f"{account_name} 2026 site:mp.weixin.qq.com"
    search_result = web_search(query, count=5)
    found_urls = re.findall(r'https?://[^\s<>"\']+', search_result)
    # 只保留 mp.weixin.qq.com 链接
    found_urls = [u for u in found_urls if "mp.weixin.qq.com" in u][:4]

    if not found_urls:
        # 回退：搜通用搜索
        query2 = f"{account_name} 微信公众号 2026年5月"
        search_result2 = web_search(query2, count=5)
        found_urls = re.findall(r'https?://[^\s<>"\']+', search_result2)
        found_urls = [u for u in found_urls if "mp.weixin.qq.com" in u or "weixin.qq.com" in u][:4]

    # 抓取找到的 URL
    articles = []
    for url in found_urls[:3]:
        body = jina_read(url, timeout=20)
        body_clean = clean_body(body)
        if body_clean:
            articles.append({
                "url": url,
                "title_hint": truncate(body_clean.split('\n')[0] if '\n' in body_clean else body_clean, 80),
                "body_preview": truncate(body_clean, 300),
                "body_len": len(body_clean),
            })

    status = "found" if articles else "no_articles"
    print(f"    → {status} | {len(articles)} articles | {'; '.join(a['title_hint'][:40] for a in articles[:2])}")

    return build_summary(account_id, account_name, articles, window), status, articles

def build_summary(account_id, account_name, articles, window):
    lines = []
    lines.append(f"# SOURCE PACKET | {account_id} | {account_name}")
    lines.append(f"**抓取时间:** {NOW_HR} CST")
    lines.append(f"**source-id:** {account_id}")
    lines.append(f"**抓取方式:** WeChat RSS 搜索刷新 (Jina Reader + Search)")
    lines.append(f"**数据窗口:** {window}")
    lines.append(f"**当日批次:** {window}")
    lines.append("")
    lines.append("---")
    lines.append("")

    if not articles:
        lines.append("## 核心内容摘要")
        lines.append("> ❌ 本轮未找到当日新文章，可能账号无更新或被搜索引擎限流。")
        lines.append("")
        return "\n".join(lines)

    lines.append(f"## 核心内容摘要 ({len(articles)} 条)")
    lines.append("")

    for i, art in enumerate(articles, 1):
        title = art.get("title_hint", "无标题")[:80]
        body  = art.get("body_preview", "")[:300]
        url   = art.get("url", "")
        lines.append(f"### {i}. {title}")
        lines.append(f"- **来源:** {account_name} (微信公众平台)")
        if body:
            lines.append(f"- **摘要:** {body}")
        lines.append(f"- **链接:** {url}")
        lines.append("")

    lines.append("---")
    lines.append(f"*market-scout runtime | WeChat RSS 刷新 | 不构成投资结论*")
    return "\n".join(lines)

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="WeChat RSS 刷新轮")
    ap.add_argument("--batch", default="a", choices=["a","b","c","all"],
                    help="A=强链主账号; B=弱/无效账号补轮; C=全量; all=全部")
    ap.add_argument("--write-log", action="store_true", default=False,
                    help="写 source packet 到 source_packets 目录")
    ap.add_argument("--date", default=TODAY_STR)
    args = ap.parse_args()

    batch_accounts, batch_label = BATCH_MAP.get(args.batch, BATCH_A)

    print(f"[{datetime.now().isoformat()}] market_wechat_rss_refresh START")
    print(f"  Batch: {args.batch} — {batch_label}")
    print(f"  Accounts: {list(batch_accounts.values())}")

    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    log_lines = []
    log_lines.append(f"[{NOW_HR}] market_wechat_rss_refresh START | batch={args.batch} | {batch_label}")
    log_lines.append(f"  Accounts: {', '.join(batch_accounts.values())}")

    results = {}
    for account_id, account_name in batch_accounts.items():
        summary_md, status, articles = capture_account(account_id, account_name)
        results[account_id] = {
            "account_name": account_name,
            "status": status,
            "article_count": len(articles),
        }

        if args.write_log:
            out_name = f"{DATE_ID}__source__wechat__{account_id.replace('wechat__','')}.md"
            out_path = os.path.join(SRC_DIR, out_name)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(summary_md)
            print(f"    → wrote {out_path}")

        log_lines.append(f"{'OK' if status=='found' else 'WARN'} [{account_id}] {account_name} | {status} | {len(articles)} articles")

    # 日志写入
    log_name = f"{DATE_ID}__wechat-rss-refresh__batch-{args.batch}.log"
    log_path = os.path.join(LOG_DIR, log_name)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")
    print(f"\n✓ 日志 → {log_path}")

    found_count   = sum(1 for v in results.values() if v["status"] == "found")
    no_art_count  = sum(1 for v in results.values() if v["status"] == "no_articles")
    total_articles = sum(v["article_count"] for v in results.values())

    print(f"\n✓ market_wechat_rss_refresh 完成")
    print(f"  Batch {args.batch} | {found_count}/{len(results)} 账号找到文章 | {total_articles} 篇总文章")
    if args.write_log:
        print(f"  Source packets → {SRC_DIR}/")
    return 0

if __name__ == "__main__":
    sys.exit(main())
