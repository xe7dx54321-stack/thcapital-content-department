#!/usr/bin/env python3
"""
market_official_update_lane.py
Official Update Lane for market-scout
抓取 OpenAI / Google / Anthropic / DeepMind / xAI / NVIDIA 官方一手更新
+ X 官方账号快信号
"""

import argparse, os, json, re, sys, subprocess
from datetime import datetime

ROOT      = "/Users/apple/Documents/同行资本市场内容系统"
DATE_ID   = datetime.now().strftime('%Y%m%d')
DATE_STR  = datetime.now().strftime('%Y-%m-%d')

# 每个 source：type=web 表示从官方博客抓，type=rss 表示直接用 RSS
# 确认可工作的 RSS + 页面列表
SOURCES = {
    "web__openai_news":    {"label": "OpenAI News",      "type": "rss",  "url": "https://openai.com/news/rss.xml"},
    "web__nvidia_blog":    {"label": "NVIDIA Blog",      "type": "rss",  "url": "https://blogs.nvidia.com/feed/"},
    "web__google_blog_ai": {"label": "Google AI Blog",   "type": "page", "url": "https://blog.google/technology/ai/"},
    "web__anthropic_news": {"label": "Anthropic News",   "type": "page", "url": "https://www.anthropic.com/news/"},
    "web__deepmind_blog":  {"label": "DeepMind Blog",    "type": "page", "url": "https://deepmind.google/blog/"},
    "web__xai_news":       {"label": "xAI News",         "type": "page", "url": "https://x.ai/blog"},
    "x__openai":           {"label": "@OpenAI (X)",       "type": "x",    "account": "OpenAI",     "nitter": "https://nitter.net/OpenAI/rss"},
    "x__openaidevs":       {"label": "@OpenAIDevs (X)",   "type": "x",    "account": "OpenAIDevs", "nitter": "https://nitter.net/OpenAIDevs/rss"},
    "x__anthropic_ai":     {"label": "@AnthropicAI (X)",  "type": "x",    "account": "AnthropicAI","nitter": "https://nitter.net/AnthropicAI/rss"},
}

OUTPUT_DIR     = os.path.join(ROOT, "02_topic_radar", "source_packets", f"{DATE_ID}__official_lane")
OUTPUT_TOP20   = os.path.join(ROOT, "03_topic_candidates", f"{DATE_ID}__official-top20.md")
OUTPUT_MANIFEST= os.path.join(ROOT, "10_logs", f"{DATE_ID}__official-source-manifest.md")
ARCHIVE_DIR    = os.path.join(ROOT, "02_topic_radar", "raw", f"official_{DATE_ID}")

def mkdirp(p):
    os.makedirs(p, exist_ok=True)

def curl(url, timeout=20):
    try:
        r = subprocess.run(
            ["curl", "-s", "-L", "--max-time", str(timeout), "-A",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/122 Safari/537.36",
             url],
            capture_output=True, text=True, timeout=timeout+5
        )
        return r.stdout or ""
    except Exception:
        return ""

def score_entry(title, body, src_id):
    s, reasons = 0, []
    t = (title + " " + body).lower()
    # 模型/产品信号
    for kw in ["gpt", "gemini", "claude", "grok", "llm", "model", "nvidia", "gpu", "chip", "deepmind", "openai", "anthropic", "x.ai", "reinforcement", "agent", "codex", "voice", "api", "platform"]:
        if kw in t:
            s += 7
    # 发布/产品信号
    for kw in ["launch", "release", "announce", "new", "introduces", "unveils", "debut", "shipping", "deploy", "updates"]:
        if kw in t:
            s += 5
    # 安全/政策/责任信号
    for kw in ["safety", "policy", "responsible", "trust", "security", "alignment", "compliance", "cyber"]:
        if kw in t:
            s += 4
    # 平台层动作
    for kw in ["api", "sdk", "cloud", "enterprise", "pricing", "partnership", "collaboration"]:
        if kw in t:
            s += 3
    # X 快信号加分
    if src_id.startswith("x__"):
        s += 4
    # 突发/独家信号
    if any(k in t for k in ["breaking", "exclusive", "just announced", "live now", "today"]):
        s += 6; reasons.append("突发信号")
    # 截断
    if s > 60:
        s = 60
    return s, reasons

def parse_rss(xml, src_id, label):
    entries = []
    for item in re.findall(r'<item>(.*?)</item>', xml, re.S)[:30]:
        t = re.search(r'<title>(.*?)</title>', item, re.S)
        l = re.search(r'<link>(.*?)</link>', item)
        d = re.search(r'<description>(.*?)</description>', item, re.S)
        if not t: continue
        title = t.group(1).strip().replace('<![CDATA[','').replace(']]>','').strip()
        link  = l.group(1).strip() if l else ""
        desc  = d.group(1)[:400] if d else ""
        s, reasons = score_entry(title, desc, src_id)
        entries.append({
            "entity_name":   title[:80],
            "source_url":    link,
            "title_text":    title,
            "body_snippet":  desc[:200],
            "score":         s,
            "signal_reasons": reasons,
            "type":          "official_rss",
            "_source":       src_id,
            "label":         label,
        })
    # Sort by score desc, dedupe by URL
    entries.sort(key=lambda x: x["score"], reverse=True)
    seen, out = {}, []
    for e in entries:
        if e["source_url"] not in seen:
            seen[e["source_url"]] = True
            out.append(e)
    return out[:20]

def parse_page(url, src_id, label):
    """从官方博客页面直接提取文章链接标题"""
    html = curl(url, timeout=20)
    if not html: return []
    entries, seen = [], {}

    # Domain-specific extraction
    if "google.com" in url or "blog.google" in url:
        for m in re.findall(r'<a[^>]+href="(https://blog\.google[^#"\s]+)"[^>]*>(.*?)</a>', html, re.S):
            u, blk = m
            t = re.sub(r'<[^>]+>', '', blk).strip()
            if t and len(t) > 15 and u not in seen:
                s, reasons = score_entry(t, "", src_id)
                seen[u] = {"entity_name": t[:80], "source_url": u, "title_text": t,
                           "body_snippet": "", "score": s, "signal_reasons": reasons,
                           "type": "official_page", "_source": src_id, "label": label}

    elif "anthropic.com" in url:
        for m in re.findall(r'<a[^>]+href="(https://www\.anthropic\.com/[^#"\s]+)"[^>]*>(.*?)</a>', html, re.S):
            u, blk = m
            t = re.sub(r'<[^>]+>', '', blk).strip()
            if t and len(t) > 15 and u not in seen:
                s, reasons = score_entry(t, "", src_id)
                seen[u] = {"entity_name": t[:80], "source_url": u, "title_text": t,
                           "body_snippet": "", "score": s, "signal_reasons": reasons,
                           "type": "official_page", "_source": src_id, "label": label}

    elif "deepmind.google" in url:
        for m in re.findall(r'<a[^>]+href="(https://deepmind\.google/[^#"\s]+)"[^>]*>(.*?)</a>', html, re.S):
            u, blk = m
            t = re.sub(r'<[^>]+>', '', blk).strip()
            if t and len(t) > 15 and u not in seen:
                s, reasons = score_entry(t, "", src_id)
                seen[u] = {"entity_name": t[:80], "source_url": u, "title_text": t,
                           "body_snippet": "", "score": s, "signal_reasons": reasons,
                           "type": "official_page", "_source": src_id, "label": label}

    elif "x.ai" in url:
        for m in re.findall(r'<a[^>]+href="(https://x\.ai/[^#"\s]+)"[^>]*>(.*?)</a>', html, re.S):
            u, blk = m
            t = re.sub(r'<[^>]+>', '', blk).strip()
            if t and len(t) > 15 and u not in seen:
                s, reasons = score_entry(t, "", src_id)
                seen[u] = {"entity_name": t[:80], "source_url": u, "title_text": t,
                           "body_snippet": "", "score": s, "signal_reasons": reasons,
                           "type": "official_page", "_source": src_id, "label": label}

    # Also look for RSS/atom links in the page
    for m in re.findall(r'<link[^>]+href="([^"]+)"[^>]*type="application/(?:rss|atom)[^"]*"', html):
        rss_url = m.strip()
        if rss_url and rss_url.startswith("http"):
            xml = curl(rss_url, timeout=15)
            if xml and "<item>" in xml:
                # Parse as RSS
                for item in re.findall(r'<item>(.*?)</item>', xml, re.S)[:20]:
                    t2 = re.search(r'<title>(.*?)</title>', item, re.S)
                    l2 = re.search(r'<link>(.*?)</link>', item)
                    d2 = re.search(r'<description>(.*?)</description>', item, re.S)
                    if not t2: continue
                    title = t2.group(1).strip().replace('<![CDATA[','').replace(']]>','').strip()
                    link  = l2.group(1).strip() if l2 else ""
                    desc  = d2.group(1)[:200] if d2 else ""
                    s, reasons = score_entry(title, desc, src_id)
                    if link and link not in seen:
                        seen[link] = {"entity_name": title[:80], "source_url": link,
                                      "title_text": title, "body_snippet": desc,
                                      "score": s, "signal_reasons": reasons,
                                      "type": "official_rss", "_source": src_id, "label": label}

    return list(seen.values())[:20]

def parse_x_nitter(nitter_url, src_id, label):
    xml = curl(nitter_url, timeout=20)
    if not xml or "<item>" not in xml:
        return []
    entries = []
    for item in re.findall(r'<item>(.*?)</item>', xml, re.S)[:20]:
        t = re.search(r'<title>(.*?)</title>', item, re.S)
        l = re.search(r'<link>(.*?)</link>', item)
        d = re.search(r'<description>(.*?)</description>', item, re.S)
        if not t: continue
        raw = t.group(1).strip().replace('<![CDATA[','').replace(']]>','').strip()
        # Strip "@OpenAI: " prefix that Nitter adds
        title = re.sub(r'^[^@]+@\w+\s*:\s*', '', raw).strip()
        link  = l.group(1).strip() if l else ""
        desc  = d.group(1)[:300] if d else ""
        s, reasons = score_entry(title, desc, src_id)
        entries.append({
            "entity_name":   title[:80],
            "source_url":    link,
            "title_text":    title,
            "body_snippet":  desc[:200],
            "score":         s,
            "signal_reasons": reasons,
            "type":          "x_signal",
            "_source":       src_id,
            "label":         label,
        })
    return entries[:20]

def fetch_entries(src_id, info):
    stype = info["type"]
    if stype == "rss":
        xml = curl(info["url"], timeout=20)
        if xml and ("<item>" in xml or "<entry>" in xml):
            return parse_rss(xml, src_id, info["label"])
        # Fall back to page parse
        return parse_page(info["url"], src_id, info["label"])
    elif stype == "x":
        nitter = info.get("nitter", "")
        if nitter:
            entries = parse_x_nitter(nitter, src_id, info["label"])
            if entries:
                return entries
        # Fallback to page
        return parse_page(f"https://nitter.net/{info['account']}", src_id, info["label"])
    else:
        return parse_page(info["url"], src_id, info["label"])

def build_top20(entries, date_str):
    entries.sort(key=lambda x: x.get("score", 0), reverse=True)
    top = entries[:20]
    lines = [
        f"# 官方原始信源 Top20 | {date_str}",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} | Official Update Lane",
        "> 覆盖：OpenAI / Google AI Blog / Anthropic / DeepMind / xAI / NVIDIA 官方博客 + X 官方账号快信号",
        "",
        "| # | 标题 | 来源 | 类型 | 评分 | 信号理由 | 链接 |",
        "|---|------|------|------|------|---------|------|",
    ]
    for i, e in enumerate(top, 1):
        title   = (e.get("title_text") or e.get("entity_name",""))[:55]
        src     = e.get("label", e.get("_source","?"))
        etype   = e.get("type","announcement")
        score   = e.get("score", 0)
        reasons = ", ".join(e.get("signal_reasons",[])[:3]) or "—"
        url     = (e.get("source_url") or "#")[:70]
        lines.append(f"| {i} | {title} | {src} | {etype} | {score} | {reasons} | [链接]({url}) |")

    lines += ["", "## 信号摘要"]
    src_counts = {}
    for e in top:
        k = e.get("_source","?")
        src_counts[k] = src_counts.get(k, 0) + 1
    src_labels = " | ".join(f"{SOURCES.get(k,{}).get('label',k)}:{v}" for k,v in src_counts.items())
    lines += [
        f"- 共 {len(top)} 条，覆盖：{src_labels}",
        "- 评分说明：模型/产品关键词×7 + 发布信号×5 + 安全政策×4 + 平台层动作×3 + X快信号×4 + 突发信号×6",
        "- 仅收录一手官方原始内容，不做二手转述"
    ]
    return "\n".join(lines)

def build_manifest(packets, date_str):
    lines = [
        f"# 官方原始信源清单 | {date_str}",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ""
    ]
    total = 0
    for pkt in packets:
        src   = pkt["source_id"]
        info  = SOURCES.get(src, {})
        label = info.get("label", src)
        count = pkt.get("entry_count", 0)
        total += count
        status = "✓" if count > 0 else "✗"
        lines.append(f"- {status} **{label}** (`{src}`): {count} 条")
    lines += ["", f"合计：{total} 条入口记录", f"覆盖公司：OpenAI / Google / Anthropic / DeepMind / xAI / NVIDIA"]
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--date', default=DATE_STR)
    ap.add_argument('--write', action='store_true', default=True)
    ap.add_argument('--source-id', action='append', default=[])
    args = ap.parse_args()

    active = args.source_id if args.source_id else list(SOURCES.keys())
    print(f"[{datetime.now().isoformat()}] market_official_update_lane starting")
    print(f"  Active sources ({len(active)}): {active}")

    mkdirp(OUTPUT_DIR)
    mkdirp(ARCHIVE_DIR)

    packets = []
    all_entries = []

    for src_id in active:
        if src_id not in SOURCES:
            print(f"  [!] Unknown source: {src_id}")
            continue
        info  = SOURCES[src_id]
        print(f"  Fetching {src_id} ({info['label']})...", end=" ", flush=True)
        try:
            entries = fetch_entries(src_id, info)
            print(f"→ {len(entries)} entries")
        except Exception as ex:
            print(f"[!] Error: {ex}")
            entries = []
        pkt = {
            "source_id":    src_id,
            "label":        info["label"],
            "type":         info["type"],
            "captured_at":  datetime.now().isoformat(),
            "entry_count":  len(entries),
            "entries":      entries,
        }
        packets.append(pkt)
        all_entries.extend(entries)

        # Archive raw
        safe = src_id.replace("__", "_")
        with open(os.path.join(ARCHIVE_DIR, f"{DATE_ID}__{safe}.json"), 'w', encoding='utf-8') as f:
            json.dump(pkt, f, ensure_ascii=False, indent=2)

    if args.write:
        mkdirp(os.path.dirname(OUTPUT_TOP20))
        with open(OUTPUT_TOP20, 'w', encoding='utf-8') as f:
            f.write(build_top20(all_entries, args.date))
        print(f"  Wrote Top20 → {OUTPUT_TOP20}")

        mkdirp(os.path.dirname(OUTPUT_MANIFEST))
        with open(OUTPUT_MANIFEST, 'w', encoding='utf-8') as f:
            f.write(build_manifest(packets, args.date))
        print(f"  Wrote manifest → {OUTPUT_MANIFEST}")

        pkt_out = os.path.join(OUTPUT_DIR, f"{DATE_ID}__packets.json")
        with open(pkt_out, 'w', encoding='utf-8') as f:
            json.dump(packets, f, ensure_ascii=False, indent=2)
        print(f"  Wrote packets JSON → {pkt_out}")

    print(f"[{datetime.now().isoformat()}] market_official_update_lane done ({len(all_entries)} total entries)")
    return 0

if __name__ == '__main__':
    sys.exit(main())