#!/usr/bin/env python3
"""
market_topic_capture_round.py – Full Builder/Research Diffusion Lane
Covers: HN/GitHub/arXiv/HF Papers + YouTube×6 + Reddit×3 + Builder Blogs + 
        X (Twitter) profiles + 中文AI媒体 + 破圈验证
"""
import argparse, os, json, re, sys, subprocess
from datetime import datetime

ROOT = "/Users/apple/Documents/同行资本市场内容系统"
DATE_STR = datetime.now().strftime('%Y-%m-%d')
DATE_ID   = datetime.now().strftime('%Y%m%d')

SOURCES = {
    # ── Hacker News / GitHub / Research ─────────────────────────
    "trend__hn_frontpage":           {"label": "Hacker News Front Page",       "base_url": "https://hnrss.org/frontpage"},
    "trend__github_trending":         {"label": "GitHub Trending",               "base_url": "https://github.com/trending"},
    "trend__huggingface_daily_papers":{"label": "HuggingFace Daily Papers",     "base_url": "https://huggingface.co/papers.rss"},
    "trend__arxiv_cs_ai_recent":      {"label": "arXiv cs.AI Recent",            "base_url": "https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sort_order=descending&max_results=20"},
    # ── Existing: YC / TC / FinSMEs / TrendHunt ─────────────────
    "trend__yc_launches_ai":          {"label": "YC Launches (AI)",             "base_url": "https://www.ycombinator.com/companies?tags=AI"},
    "web__techcrunch_ai":             {"label": "TechCrunch AI",                "base_url": "https://techcrunch.com/feed/"},
    "web__finsmes_ai_gnews":          {"label": "FinSMEs AI (GNews)",           "base_url": "https://news.google.com/search?q=finsmes+AI+startup+funding&hl=en-US&gl=US&ceid=US:en"},
    "trend__trend_hunt_ai_agents":    {"label": "Trend Hunt AI Agents",         "base_url": "https://www.producthunt.com/posts"},
    # ── Reddit ─────────────────────────────────────────────────
    "trend__reddit_localllama_daily": {"label": "Reddit / r/LocalLLaMA",        "base_url": "https://old.reddit.com/r/LocalLLaMA/hot.rss"},
    "trend__reddit_claude_daily":      {"label": "Reddit / r/ClaudeAI",          "base_url": "https://old.reddit.com/r/ClaudeAI/hot.rss"},
    "trend__reddit_chatgpt_daily":     {"label": "Reddit / r/ChatGPT",          "base_url": "https://old.reddit.com/r/ChatGPT/hot.rss"},
    # ── YouTube ────────────────────────────────────────────────
    "youtube__openai":               {"label": "YouTube / OpenAI",             "yt_channel_id": "UCXZCJLdBC09xxGZ6gcdrc6A"},
    "youtube__ycombinator":            {"label": "YouTube / Y Combinator",      "yt_channel_id": "UCxIJaCMEptJjxmmQgGFsnCg"},
    "youtube__googledeepmind":         {"label": "YouTube / Google DeepMind",   "yt_channel_id": "UCP7jMXSY2xbc3KCAE0MHQ-A"},
    "youtube__aidotengineer":          {"label": "YouTube / AI Engineer",       "yt_channel_id": "UCLKPca3kwwd-B59HNr-_lvA"},
    "youtube__latent_space_pod":        {"label": "YouTube / Latent Space",      "yt_channel_id": "UCxBcwypKK-W3GHd_RZ9FZrQ"},
    "youtube__langchain":              {"label": "YouTube / LangChain",         "yt_channel_id": "UCC-lyoTfSrcJzA1ab3APAgw"},
    # ── Builder / Expert Blogs ──────────────────────────────────
    "web__simon_willison":            {"label": "Simon Willison",               "base_url": "https://simonwillison.net/atom.xml"},
    "web__latent_space":              {"label": "Latent Space Blog",            "base_url": "https://www.latent.space/p/feed"},
    "web__one_useful_thing":          {"label": "One Useful Thing",             "base_url": "https://oneusefulthing.substack.com/feed"},
    "web__interconnects":             {"label": "Interconnects.ai",            "base_url": "https://interconnects.ai/feed"},
    "web__understanding_ai":          {"label": "Understanding AI",             "base_url": "https://understandingai.org/rss"},
    "web__deeplearningai_batch":       {"label": "DeepLearning.ai Batch",      "base_url": "https://www.deeplearning.ai/feed/"},
    "web__infoq_ai_ml":               {"label": "InfoQ AI/ML",                 "base_url": "https://feed.infoq.com/ai_ml"},
    "web__semianalysis":              {"label": "SemiAnalysis",               "base_url": "https://semianalysis.com/feed/"},
    "web__huggingface_blog":          {"label": "HuggingFace Blog",            "base_url": "https://blog.huggingface.co/feed.xml"},
    "web__openclaw_docs":             {"label": "OpenClaw Docs",               "base_url": "https://ln.dev/docs"},
    # ── X (Twitter) – no public RSS, listed for completeness ───
    "x__karpathy":                    {"label": "X / @karpathy",              "base_url": "https://twitter.com/karpathy"},
    "x__swyx":                        {"label": "X / @swyx",                  "base_url": "https://twitter.com/swyx"},
    "x__hwchase17":                   {"label": "X / @hwchase17",             "base_url": "https://twitter.com/hwchase17"},
    # ── 中文 AI 媒体 ─────────────────────────────────────────────
    "web__jiqizhixin_site":           {"label": "机器之心",                     "base_url": "https://jiqizhixin.com"},
    "web__qbitai_site":               {"label": "QbitAI",                      "base_url": "https://www.qbitai.com"},
    "web__zhidx":                     {"label": "至顶网",                      "base_url": "https://www.zhidx.com/rss"},
    "web__36kr_ai":                   {"label": "36氪 AI",                     "base_url": "https://36kr.com/feed"},
    "web__ifanr_ai":                  {"label": "爱范儿 AI",                   "base_url": "https://www.ifanr.com/feed"},
    "web__sspai_ai":                  {"label": "少数派 AI",                   "base_url": "https://sspai.com/feed"},
    # ── Bilibili ────────────────────────────────────────────────
    "trend__bilibili_popular_all":     {"label": "B站 / 全站排行榜",            "base_url": "https://api.bilibili.com/x/web-interface/popular"},
    # ── 破圈验证 ────────────────────────────────────────────────
    "trend__baidu_realtime":          {"label": "百度实时热搜",                 "base_url": "https://top.baidu.com/board?tab=realtime"},
    "trend__zhihu_hotlist":           {"label": "知乎热榜",                     "base_url": "https://www.zhihu.com/api/v3/tab/follow-hot-topics"},
    "trend__feigua_bilibili":         {"label": "飞瓜B站科技榜",               "base_url": "https://www.feigua.com.cn/bilibili/rank.html"},
    "trend__newrank_ai_media_rank":   {"label": "新榜AI媒体榜",                "base_url": "https://www.newrank.cn/new/#/ai"},
}

OUTPUT_SRC_PACKETS = os.path.join(ROOT, "02_topic_radar", "source_packets", f"{DATE_ID}__source_packets")
OUTPUT_ASSET_CHAINS = os.path.join(ROOT, "02_topic_radar", "asset_chains")
OUTPUT_TOP20  = os.path.join(ROOT, "03_topic_candidates", f"{DATE_ID}__top20-screening-pack.md")
OUTPUT_MANIFEST = os.path.join(ROOT, "10_logs", f"{DATE_ID}__market-source-manifest.md")

def mkdirp(path):
    os.makedirs(path, exist_ok=True)

def curl(url, timeout=15):
    try:
        r = subprocess.run(
            ["curl", "-s", "-L", "--max-time", str(timeout), "-A",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", url],
            capture_output=True, text=True, timeout=timeout+5
        )
        return r.stdout or ""
    except Exception:
        return ""

def score(title, body, src):
    s, reasons = 0, []
    kw = ["AI","agent","LLM","model","automation","generative","startup","funding","seed","Series","launch","product","robot","autonomous","agentic","reasoning","reasoner"," Reasoning"]
    hits = sum(1 for k in kw if k.lower() in (title+body).lower())
    s += min(hits*5, 30)
    if any(k in body.lower() for k in ["raised","funding","seed","Series","round","investment"]):
        s += 20; reasons.append("融资信号")
    if src == "trend__yc_launches_ai":
        s += 10; reasons.append("YC来源")
    if any(k in title.lower() for k in ["launch","announced","releases","founded","new ","released","unveils"]):
        s += 10; reasons.append("新产品信号")
    return s, reasons

def make_entry(name, url, src, etype="article", body=""):
    s, reasons = score(name, body, src)
    return {"entity_name": name, "source_url": url, "score": s,
            "signal_reasons": reasons, "type": etype, "_source": src}

# ── Fetcher: Hacker News Front Page ───────────────────────────
def fetch_hn_frontpage():
    xml = curl("https://hnrss.org/frontpage", timeout=15)
    entries = []
    if not xml or "<item>" not in xml:
        return entries
    for item in re.findall(r'<item>(.*?)</item>', xml, re.S)[:30]:
        t = re.search(r'<title>(.*?)</title>', item)
        l = re.search(r'<link>(.*?)</link>', item)
        if not t: continue
        title = t.group(1).strip().replace('<![CDATA[','').replace(']]>','')
        link  = l.group(1).strip() if l else ""
        entry = make_entry(title, link, "trend__hn_frontpage", "discussion", "")
        pm = re.search(r'<p>Points:\s*(\d+)', item)
        cm = re.search(r'<p># Comments:\s*(\d+)', item)
        entry["hn_points"]   = int(pm.group(1)) if pm else 0
        entry["hn_comments"] = int(cm.group(1)) if cm else 0
        entries.append(entry)
    return entries

# ── Fetcher: GitHub Trending ──────────────────────────────────
def fetch_github_trending():
    html = curl("https://github.com/trending", timeout=20)
    entries = []
    if not html: return entries
    articles = re.findall(r'<article class="Box-row">(.*?)</article>', html, re.S)
    for art in articles[:25]:
        name_m = re.search(r'href="/([^"]+)"[^>]*>([^<]+)</a>', art)
        desc_m = re.search(r'<p class="col-9[^"]*">(.*?)</p>', art, re.S)
        lang_m = re.search(r'<span itemprop="programmingLanguage">([^<]+)</span>', art)
        if not name_m: continue
        repo_path = name_m.group(1).strip()
        repo_name = name_m.group(2).strip()
        desc = re.sub(r'<[^>]+>','', desc_m.group(1).strip()) if desc_m else ""
        lang = lang_m.group(1).strip() if lang_m else ""
        url  = f"https://github.com/{repo_path}"
        entry = make_entry(f"{repo_name} ({lang})", url, "trend__github_trending", "open_source", desc)
        entry["github_lang"] = lang
        entries.append(entry)
    return entries

# ── Fetcher: HuggingFace Papers RSS ───────────────────────────
def fetch_huggingface_papers():
    xml = curl("https://huggingface.co/papers.rss", timeout=15)
    if not xml or "<item>" not in xml:
        xml = curl("https://huggingface.co/papers.atom", timeout=15)
    entries = []
    if not xml or "<entry>" not in xml: return entries
    tag = "<entry>" if "<entry>" in xml else "<item>"
    for item in re.findall(re.escape(tag).replace('\\>','[^>]*>').replace('\\<','[^<]*<'), xml, re.S)[:20]:
        t = re.search(r'<title>(.*?)</title>', item)
        l = re.search(r'<link[^>]*href="([^"]+)"', item)
        if not t: continue
        title = t.group(1).strip().replace('<![CDATA[','').replace(']]>','')
        link  = l.group(1).strip() if l else ""
        if not link:
            l2 = re.search(r'<link>(.*?)</link>', item)
            link = l2.group(1).strip() if l2 else ""
        entries.append(make_entry(title, link, "trend__huggingface_daily_papers", "research_paper", ""))
    return entries

# ── Fetcher: arXiv cs.AI ──────────────────────────────────────
def fetch_arxiv_cs_ai():
    url = ("https://export.arxiv.org/api/query?search_query=cat:cs.AI"
           "&sortBy=submittedDate&sort_order=descending&max_results=20")
    raw = curl(url, timeout=20)
    entries = []
    if not raw or "<entry>" not in raw: return entries
    for entry_xml in re.findall(r'<entry>(.*?)</entry>', raw, re.S)[:20]:
        t = re.search(r'<title>(.*?)</title>', entry_xml)
        l = re.search(r'<id>(.*?)</id>', entry_xml)
        a = re.search(r'<author>.*?<name>(.*?)</name>', entry_xml, re.S)
        if not t: continue
        title = t.group(1).strip().replace('\n',' ')
        link  = l.group(1).strip() if l else ""
        author = a.group(1).strip() if a else ""
        e = make_entry(title[:120], link, "trend__arxiv_cs_ai_recent", "research_paper", f"Author: {author}")
        e["arxiv_author"] = author
        entries.append(e)
    return entries

# ── Fetcher: YC ──────────────────────────────────────────────
def fetch_yc():
    html = curl("https://www.ycombinator.com/companies?tags=AI", timeout=15)
    entries = []
    if not html or "File Not Found" in html[:200]:
        xml = curl("https://www.ycombinator.com/blog/feed", timeout=15)
        if xml and "<item>" in xml:
            for item in re.findall(r'<item>(.*?)</item>', xml, re.S)[:30]:
                t = re.search(r'<title>(.*?)</title>', item)
                l = re.search(r'<link>(.*?)</link>', item)
                if t:
                    title = t.group(1).strip().replace('<![CDATA[','').replace(']]>','')
                    link  = l.group(1).strip() if l else ""
                    if any(k in title.lower() for k in ["ai","startup","launch","founded","funding"]):
                        s, reasons = score(title, "", "trend__yc_launches_ai")
                        if s > 0: entries.append(make_entry(title, link, "trend__yc_launches_ai", "startup", ""))
        return entries
    names = re.findall(r'class="[^"]*name[^"]*"[^>]*>([^<]+)', html)
    links = re.findall(r'href="(/companies/[^"]+)"', html)
    seen = set()
    for path, name in zip(links, names):
        if path in seen: continue
        seen.add(path)
        name = name.strip()
        if name and any(k in name.lower() for k in ["ai","agent","llm","model","automation","robot"]):
            url = f"https://www.ycombinator.com{path}"
            s, reasons = score(name, "", "trend__yc_launches_ai")
            if s > 0: entries.append(make_entry(name, url, "trend__yc_launches_ai", "startup", ""))
    return entries

# ── Fetcher: TechCrunch ───────────────────────────────────────
def fetch_tc():
    xml = curl("https://techcrunch.com/feed/", timeout=20)
    entries = []
    if not xml or "<item>" not in xml: return entries
    for item in re.findall(r'<item>(.*?)</item>', xml, re.S)[:25]:
        t = re.search(r'<title>(.*?)</title>', item)
        l = re.search(r'<link>(.*?)</link>', item)
        d = re.search(r'<description>(.*?)</description>', item, re.S)
        if not t: continue
        title = t.group(1).strip().replace('<![CDATA[','').replace(']]>','')
        link  = l.group(1).strip() if l else ""
        body  = re.sub(r'<[^>]+>','', d.group(1)) if d else ""
        s, reasons = score(title, body, "web__techcrunch_ai")
        if s > 0: entries.append(make_entry(title, link, "web__techcrunch_ai", "article", body[:300]))
    return entries

# ── Fetcher: FinSMEs via Google News ─────────────────────────
def fetch_finsmes_gnews():
    xml = curl("https://news.google.com/search?q=finsmes+AI+startup+funding&hl=en-US&gl=US&ceid=US:en", timeout=20)
    entries = []
    if not xml or "<item>" not in xml: return entries
    for item in re.findall(r'<item>(.*?)</item>', xml, re.S)[:20]:
        t = re.search(r'<title>(.*?)</title>', item)
        l = re.search(r'<link>(.*?)</link>', item)
        if not t: continue
        title = t.group(1).strip().replace('<![CDATA[','').replace(']]>','')
        link  = l.group(1).strip() if l else ""
        s, reasons = score(title, "", "web__finsmes_ai_gnews")
        if s > 0: entries.append(make_entry(title, link, "web__finsmes_ai_gnews", "article", ""))
    return entries

# ── Fetcher: Product Hunt ─────────────────────────────────────
def fetch_trend_hunt():
    html = curl("https://www.producthunt.com/posts", timeout=20)
    entries = []
    if not html: return entries
    titles = re.findall(r'class="[^"]*title[^"]*"[^>]*>([^<]+)', html)
    links  = re.findall(r'href="(/posts/[^?"]+)"', html)
    seen = set()
    for link, title in zip(links[:20], titles[:20]):
        if link in seen or not title.strip(): continue
        seen.add(link)
        url = f"https://www.producthunt.com{link}"
        s, reasons = score(title, "", "trend__trend_hunt_ai_agents")
        if s > 0: entries.append(make_entry(title.strip()[:80], url, "trend__trend_hunt_ai_agents", "product", ""))
    return entries

# ── Fetcher: YouTube Channel ───────────────────────────────────
def fetch_youtube_channel(src_id, label):
    cfg = SOURCES.get(src_id, {})
    channel_id = cfg.get("yt_channel_id","")
    if not channel_id: return []
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    xml = curl(url, timeout=15)
    entries = []
    if not xml or "<entry>" not in xml: return entries
    for entry in re.findall(r'<entry>(.*?)</entry>', xml, re.S)[:15]:
        t = re.search(r'<title>(.*?)</title>', entry)
        l = re.search(r'<link[^>]*rel="alternate"[^>]*href="([^"]+)"', entry)
        if not t: continue
        title = t.group(1).strip().replace('<![CDATA[','').replace(']]>','')
        link  = l.group(1).strip() if l else ""
        e = make_entry(title[:100], link, src_id, "video", "")
        entries.append(e)
    return entries

# ── Fetcher: Bilibili ──────────────────────────────────────────
def fetch_bilibili_popular():
    raw = curl("https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1", timeout=15)
    entries = []
    if not raw: return entries
    try:
        data = json.loads(raw)
        for item in data.get("data", {}).get("list", [])[:20]:
            title = item.get("title","")
            link  = f"https://www.bilibili.com/video/{item.get('bvid','')}"
            desc  = f"播放:{item.get('stat',{}).get('view',0)} 点赞:{item.get('stat',{}).get('like',0)}"
            e = make_entry(title[:80], link, "trend__bilibili_popular_all", "video", desc)
            e["bilibili_stat"] = item.get("stat",{})
            entries.append(e)
    except Exception:
        pass
    return entries

# ── Fetcher: 百度实时热搜 ──────────────────────────────────────
def fetch_baidu_realtime():
    html = curl("https://top.baidu.com/board?tab=realtime", timeout=15)
    entries = []
    if not html: return entries
    # Extract from embedded JSON: each entry has "query", "url", "hotScore"
    raw_json = re.search(r'(\[.*?"query"[^;]+)\s*,\s*"isRec?', html, re.S)
    items = []
    if raw_json:
        try:
            items = json.loads("[" + raw_json.group(1) + "]")
        except Exception:
            pass
    if not items:
        # fallback: parse individual "query"/"url"/"hotScore" triples
        queries = re.findall(r'"query"\s*:\s*"([^"]+)"', html)
        raw_urls = re.findall(r'"rawUrl"\s*:\s*"([^"]+)"', html)
        scores  = re.findall(r'"hotScore"\s*:\s*"([^"]+)"', html)
        hot_tags = re.findall(r'"hotTag"\s*:\s*"([^"]+)"', html)
        for i, (q, u, sc, tag) in enumerate(zip(queries[:30], raw_urls[:30], scores[:30], hot_tags[:30])):
            if not q.strip(): continue
            s, reasons = score(q, "", "trend__baidu_realtime")
            if s == 0: s = int(sc)//2000000 + 1 if sc.isdigit() else 1
            entry = make_entry(q.strip(), u if u else f"https://www.baidu.com/s?wd={q}", "trend__baidu_realtime", "hot_search", "")
            entry["rank"] = i+1; entry["platform"] = "baidu"; entry["hot_score"] = sc; entry["hot_tag"] = tag
            entries.append(entry)
        return entries
    for i, item in enumerate(items[:30]):
        title = item.get("query","") or item.get("word","")
        url   = item.get("rawUrl","") or item.get("url","")
        sc    = item.get("hotScore","")
        tag   = item.get("hotTag","")
        if not title.strip(): continue
        s, reasons = score(title, "", "trend__baidu_realtime")
        if s == 0: s = int(sc)//2000000 + 1 if sc.isdigit() else 1
        entry = make_entry(title.strip(), url, "trend__baidu_realtime", "hot_search", "")
        entry["rank"] = i+1; entry["platform"] = "baidu"; entry["hot_score"] = sc; entry["hot_tag"] = tag
        entries.append(entry)
    return entries

# ── Fetcher: 知乎热榜 ─────────────────────────────────────────
def fetch_zhihu_hotlist():
    raw = curl("https://api.zhihu.com/topstory/hot-list", timeout=15)
    entries = []
    if not raw: return entries
    try:
        data = json.loads(raw)
        for item in data.get("data", [])[:20]:
            target = item.get("target", {})
            title = target.get("title", "")
            link  = target.get("url", "")
            answer_count = target.get("answer_count", 0)
            if title:
                s, reasons = score(title, "", "trend__zhihu_hotlist")
                if s == 0: s = min(answer_count // 100, 20) + 2
                entry = make_entry(title[:120], link, "trend__zhihu_hotlist", "question", "")
                entry["answer_count"] = answer_count
                entries.append(entry)
    except Exception:
        pass
    return entries

# ── Fetcher: 飞瓜B站 ──────────────────────────────────────────
def fetch_feigua_bilibili():
    html = curl("https://www.feigua.com.cn/bilibili/rank.html", timeout=15)
    entries = []
    if not html: return entries
    titles = re.findall(r'class="[^"]*title[^"]*"[^>]*>([^<]+)', html)
    links  = re.findall(r'href="([^"]+bilibili[^"]+)"', html)
    seen = set()
    for link, title in zip(links[:20], titles[:20]):
        if link in seen or not title.strip(): continue
        seen.add(link)
        entries.append(make_entry(title.strip()[:80], link, "trend__feigua_bilibili", "video", ""))
    return entries

# ── Fetcher: 新榜AI媒体 ────────────────────────────────────────
def fetch_newrank_ai_media_rank():
    html = curl("https://www.newrank.cn/new/#/ai", timeout=15)
    entries = []
    if not html: return entries
    titles = re.findall(r'class="[^"]*title[^"]*"[^>]*>([^<]+)', html)
    links  = re.findall(r'href="([^"]+)"', html)
    seen = set()
    for link, title in zip(links[:20], titles[:20]):
        if link in seen or not title.strip(): continue
        seen.add(link)
        entries.append(make_entry(title.strip()[:80], link, "trend__newrank_ai_media_rank", "media_rank", ""))
    return entries

# ── Fetcher: Reddit Subreddit (via old.reddit.com RSS) ───────
def fetch_reddit_subreddit(subreddit, src_id):
    url = f"https://old.reddit.com/r/{subreddit}/hot.rss"
    raw = curl(url, timeout=20)
    entries = []
    if not raw or "<entry>" not in raw: return entries
    for entry in re.findall(r'<entry>(.*?)</entry>', raw, re.S)[:30]:
        t   = re.search(r'<title>(.*?)</title>', entry)
        l   = re.search(r'<link[^>]*href="([^"]+)"', entry)
        id_ = re.search(r'<id>(.*?)</id>', entry)
        c   = re.search(r'<author>.*?<name>(.*?)</name>', entry, re.S)
        if not t: continue
        title = t.group(1).strip().replace('<![CDATA[','').replace(']]>','')
        link  = l.group(1).strip() if l else ""
        author = c.group(1).strip() if c else ""
        desc  = f"Reddit r/{subreddit}"
        entry = make_entry(title, link, src_id, "discussion", desc)
        entries.append(entry)
    return entries

def fetch_reddit_localllama():
    return fetch_reddit_subreddit("LocalLLaMA", "trend__reddit_localllama_daily")
def fetch_reddit_claude():
    return fetch_reddit_subreddit("ClaudeAI", "trend__reddit_claude_daily")
def fetch_reddit_chatgpt():
    return fetch_reddit_subreddit("ChatGPT", "trend__reddit_chatgpt_daily")

# ── Generic RSS/Atom feed fetcher ─────────────────────────────
def _fetch_rss_feed(src_id, url, etype="article"):
    raw = curl(url, timeout=15)
    entries = []
    if not raw: return entries
    tag = "<entry>" if "<entry>" in raw else "<item>"
    tag_pat = re.escape(tag)
    for item in re.findall(tag_pat.replace('\\>','[^>]*>').replace('\\<','[^<]*<'), raw, re.S)[:20]:
        t = re.search(r'<title>(.*?)</title>', item)
        l = re.search(r'<link[^>]*href="([^"]+)"', item)
        if not t: continue
        title = t.group(1).strip().replace('<![CDATA[','').replace(']]>','').replace('&amp;','&')
        link  = l.group(1).strip() if l else ""
        if not link:
            l2 = re.search(r'<link>(.*?)</link>', item)
            link = l2.group(1).strip() if l2 else ""
        entries.append(make_entry(title[:120], link, src_id, etype, ""))
    return entries

# ── Builder / Expert Blog fetchers ───────────────────────────
def fetch_simon_willison():
    return _fetch_rss_feed("web__simon_willison", "https://simonwillison.net/atom.xml", "blog_post")
def fetch_latent_space():
    return _fetch_rss_feed("web__latent_space", "https://www.latent.space/p/feed", "podcast_post")
def fetch_one_useful_thing():
    return _fetch_rss_feed("web__one_useful_thing", "https://oneusefulthing.substack.com/feed", "newsletter")
def fetch_interconnects():
    return _fetch_rss_feed("web__interconnects", "https://interconnects.ai/feed", "newsletter")
def fetch_understanding_ai():
    return _fetch_rss_feed("web__understanding_ai", "https://understandingai.org/rss", "blog_post")
def fetch_deeplearningai_batch():
    return _fetch_rss_feed("web__deeplearningai_batch", "https://www.deeplearning.ai/feed/", "newsletter")
def fetch_infoq_ai_ml():
    return _fetch_rss_feed("web__infoq_ai_ml", "https://feed.infoq.com/ai_ml", "article")
def fetch_semianalysis():
    return _fetch_rss_feed("web__semianalysis", "https://semianalysis.com/feed/", "article")
def fetch_huggingface_blog():
    return _fetch_rss_feed("web__huggingface_blog", "https://blog.huggingface.co/feed.xml", "blog_post")
def fetch_openclaw_docs():
    return _fetch_rss_feed("web__openclaw_docs", "https://ln.dev/docs", "docs_update")

# ── X / Twitter profiles (no public RSS – stub returns []) ──
def fetch_x_profile(username, src_id):
    return []

# ── 中文 AI 媒体 fetchers ─────────────────────────────────────
def fetch_jiqizhixin():
    html = curl("https://jiqizhixin.com", timeout=15)
    entries = []
    if not html: return entries
    titles = re.findall(r'class="[^"]*title[^"]*"[^>]*>([^<]+)', html)
    links  = re.findall(r'href="(/articles/[^?"]+)"', html)
    seen = set()
    for link, title in zip(links[:20], titles[:20]):
        if link in seen or not title.strip(): continue
        seen.add(link)
        url = f"https://jiqizhixin.com{link}" if link.startswith('/') else link
        entries.append(make_entry(title.strip()[:80], url, "web__jiqizhixin_site", "article", ""))
    return entries

def fetch_qbitai():
    html = curl("https://www.qbitai.com", timeout=15)
    entries = []
    if not html: return entries
    titles = re.findall(r'class="[^"]*news__title[^"]*"[^>]*>([^<]+)', html)
    links  = re.findall(r'href="(/news/[^?"]+)"', html)
    seen = set()
    for link, title in zip(links[:20], titles[:20]):
        if link in seen or not title.strip(): continue
        seen.add(link)
        url = f"https://www.qbitai.com{link}" if link.startswith('/') else link
        entries.append(make_entry(title.strip()[:80], url, "web__qbitai_site", "article", ""))
    return entries

def fetch_zhidx():
    return _fetch_rss_feed("web__zhidx", "https://www.zhidx.com/rss", "article")
def fetch_36kr_ai():
    return _fetch_rss_feed("web__36kr_ai", "https://36kr.com/feed", "article")
def fetch_ifanr_ai():
    return _fetch_rss_feed("web__ifanr_ai", "https://www.ifanr.com/feed", "article")
def fetch_sspai_ai():
    return _fetch_rss_feed("web__sspai_ai", "https://sspai.com/feed", "article")

# ── FETCHERS dict ────────────────────────────────────────────
FETCHERS = {
    "trend__hn_frontpage":              fetch_hn_frontpage,
    "trend__github_trending":            fetch_github_trending,
    "trend__huggingface_daily_papers":  fetch_huggingface_papers,
    "trend__arxiv_cs_ai_recent":         fetch_arxiv_cs_ai,
    "trend__yc_launches_ai":            fetch_yc,
    "web__techcrunch_ai":               fetch_tc,
    "web__finsmes_ai_gnews":            fetch_finsmes_gnews,
    "trend__trend_hunt_ai_agents":      fetch_trend_hunt,
    "trend__reddit_localllama_daily":   fetch_reddit_localllama,
    "trend__reddit_claude_daily":        fetch_reddit_claude,
    "trend__reddit_chatgpt_daily":       fetch_reddit_chatgpt,
    "youtube__openai":                  lambda: fetch_youtube_channel("youtube__openai", "OpenAI"),
    "youtube__ycombinator":              lambda: fetch_youtube_channel("youtube__ycombinator", "Y Combinator"),
    "youtube__googledeepmind":          lambda: fetch_youtube_channel("youtube__googledeepmind", "Google DeepMind"),
    "youtube__aidotengineer":           lambda: fetch_youtube_channel("youtube__aidotengineer", "AI Engineer"),
    "youtube__latent_space_pod":        lambda: fetch_youtube_channel("youtube__latent_space_pod", "Latent Space"),
    "youtube__langchain":               lambda: fetch_youtube_channel("youtube__langchain", "LangChain"),
    "web__simon_willison":               fetch_simon_willison,
    "web__latent_space":                 fetch_latent_space,
    "web__one_useful_thing":             fetch_one_useful_thing,
    "web__interconnects":                fetch_interconnects,
    "web__understanding_ai":             fetch_understanding_ai,
    "web__deeplearningai_batch":        fetch_deeplearningai_batch,
    "web__infoq_ai_ml":                 fetch_infoq_ai_ml,
    "web__semianalysis":                fetch_semianalysis,
    "web__huggingface_blog":             fetch_huggingface_blog,
    "web__jiqizhixin_site":             fetch_jiqizhixin,
    "web__qbitai_site":                  fetch_qbitai,
    "web__zhidx":                        fetch_zhidx,
    "web__36kr_ai":                      fetch_36kr_ai,
    "web__ifanr_ai":                     fetch_ifanr_ai,
    "web__sspai_ai":                     fetch_sspai_ai,
    "trend__bilibili_popular_all":       fetch_bilibili_popular,
    "trend__baidu_realtime":             fetch_baidu_realtime,
    "trend__zhihu_hotlist":              fetch_zhihu_hotlist,
    "trend__feigua_bilibili":           fetch_feigua_bilibili,
    "trend__newrank_ai_media_rank":      fetch_newrank_ai_media_rank,
    "x__karpathy":                       lambda: fetch_x_profile("karpathy", "x__karpathy"),
    "x__swyx":                           lambda: fetch_x_profile("swyx", "x__swyx"),
    "x__hwchase17":                      lambda: fetch_x_profile("hwchase17", "x__hwchase17"),
    "trend__hn_frontpage":              fetch_hn_frontpage,
    "trend__github_trending":            fetch_github_trending,
    "trend__huggingface_daily_papers":  fetch_huggingface_papers,
    "trend__arxiv_cs_ai_recent":         fetch_arxiv_cs_ai,
    "trend__yc_launches_ai":            fetch_yc,
    "web__techcrunch_ai":               fetch_tc,
    "web__finsmes_ai_gnews":            fetch_finsmes_gnews,
    "trend__trend_hunt_ai_agents":      fetch_trend_hunt,
    "trend__reddit_localllama_daily":   fetch_reddit_localllama,
    "trend__reddit_claude_daily":        fetch_reddit_claude,
    "trend__reddit_chatgpt_daily":       fetch_reddit_chatgpt,
    "youtube__openai":                  lambda: fetch_youtube_channel("youtube__openai", "OpenAI"),
    "youtube__ycombinator":              lambda: fetch_youtube_channel("youtube__ycombinator", "Y Combinator"),
    "youtube__googledeepmind":          lambda: fetch_youtube_channel("youtube__googledeepmind", "Google DeepMind"),
    "youtube__aidotengineer":           lambda: fetch_youtube_channel("youtube__aidotengineer", "AI Engineer"),
    "youtube__latent_space_pod":         lambda: fetch_youtube_channel("youtube__latent_space_pod", "Latent Space"),
    "youtube__langchain":               lambda: fetch_youtube_channel("youtube__langchain", "LangChain"),
}

# ── Main ────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", default=DATE_STR)
    p.add_argument("--write", action="store_true")
    p.add_argument("--source-id", dest="source_ids", action="append", default=[])
    args = p.parse_args()
    run_ids = args.source_ids or list(SOURCES.keys())
    mkdirp(OUTPUT_SRC_PACKETS)
    mkdirp(OUTPUT_ASSET_CHAINS)
    all_entries = []
    log_lines = [f"# Market Source Manifest {args.date}"]
    for sid in run_ids:
        if sid not in FETCHERS:
            print(f"[SKIP] {sid} – unknown source")
            continue
        label = SOURCES.get(sid, {}).get("label", sid)
        print(f"[FETCH] {sid} ({label})…", end=" ", flush=True)
        try:
            entries = FETCHERS[sid]()
            n = len(entries)
            print(f"{n} entries")
            log_lines.append(f"- **{sid}** [{label}]: {n} entries")
            for e in entries:
                e["_fetched_at"] = datetime.now().isoformat()
            all_entries.extend(entries)
        except Exception as ex:
            print(f"ERROR {ex}")
            log_lines.append(f"- **{sid}** [{label}]: ERROR {ex}")
    by_src = {}
    for e in all_entries:
        by_src.setdefault(e["_source"], []).append(e)
    src_packet_path = os.path.join(OUTPUT_SRC_PACKETS, f"{DATE_ID}__src-{sid}.json")
    for sid, entries in by_src.items():
        sp = os.path.join(OUTPUT_SRC_PACKETS, f"{DATE_ID}__src-{sid}.json")
        with open(sp, "w", encoding="utf-8") as f:
            json.dump({sid: entries}, f, ensure_ascii=False, indent=2)
    combined_path = os.path.join(OUTPUT_SRC_PACKETS, f"{DATE_ID}__all-source-packets.json")
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=2)
    if args.write:
        top_entries = sorted(all_entries, key=lambda x: x.get("score", 0), reverse=True)[:20]
        lines = [f"# Top20 初筛包 — {args.date}", "", "## 评分标准说明", "", "| 字段 | 说明 |", "|---|---|", "| score | 关键词命中+信号类型加分 |", "| signal_reasons | 进入理由 |", "", "## Top20 列表", ""]
        for i, e in enumerate(top_entries, 1):
            reasons = ", ".join(e.get("signal_reasons", []))
            lines.append(f"### {i}. {e['entity_name']}")
            lines.append(f"- **URL**: {e['source_url']}")
            lines.append(f"- **类型**: {e['type']}")
            lines.append(f"- **评分**: {e.get('score',0)} | {reasons}")
            lines.append(f"- **来源**: {e['_source']}")
            lines.append("")
        top20_path = OUTPUT_TOP20
        with open(top20_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        manifest_path = OUTPUT_MANIFEST
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write("\n".join(log_lines))
        print(f"\n✅ Top20 → {top20_path}")
        print(f"✅ Manifest → {manifest_path}")
        print(f"✅ Combined source packets → {combined_path}")
    else:
        print(f"\n[PREVIEW] {len(all_entries)} total entries (no --write)")

if __name__ == "__main__":
    main()