#!/usr/bin/env python3
"""
market_wechat_deep_capture_round.py
使用 web_fetch（jina-reader）抓取今日微信source packet中高优先级URL全文，
输出到 deep_articles，保留原始导出+清洗正文，
最后触发 market_learning_memo_builder 供晚上选题复盘使用。
"""
import subprocess, os, re, json, sys
from datetime import datetime

ROOT       = "/Users/apple/Documents/同行资本市场内容系统"
DEEP_DIR   = os.path.join(ROOT, "02_topic_radar", "deep_articles")
LOG_DIR    = os.path.join(ROOT, "10_logs")
TODAY      = datetime.now().strftime("%Y-%m-%d")
DATE_SHORT = datetime.now().strftime("%Y%m%d")

# 从今日source packet整理的高优先级URL
PRIORITY_URLS = [
    ("HIGH",   "量子位",    "NCB评估指标（浙大×爱丁堡）",         "https://hub.baai.ac.cn/view/54568"),
    ("HIGH",   "量子位",    "Google AI Co-Mathematician",         "https://hub.baai.ac.cn/view/54560"),
    ("HIGH",   "新智元",    "中国移动Token运营体系",              "https://hub.baai.ac.cn/view/54565"),
    ("HIGH",   "36氪",      "大模型清场前夜-Kimi+阶跃+DeepSeek",  "https://36kr.com/p/3802258052096004"),
    ("HIGH",   "36氪",      "字节豆包付费订阅测试",               "https://36kr.com/p/3802970281041408"),
    ("HIGH",   "36氪",      "Anthropic推进500亿美元新融资",        "https://36kr.com/p/3797476502494217"),
    ("HIGH",   "机器之心",  "DeepSeek正在进行73亿美元融资",        "https://finance.sina.com.cn/stock/t/2026-05-09/doc-inhximsz3242168.shtml"),
    ("HIGH",   "智东西",    "阶跃星辰完成约170亿人民币融资",       "https://zhidx.com/p/556043.html"),
    ("MEDIUM", "极客公园",  "无屏手环被AI重新激活",               "https://www.geekpark.net/news/363933"),
    ("MEDIUM", "爱范儿",    "苹果带摄像头AirPods H90",             "https://tech.ifeng.com/c/8sxWMvClWC1"),
    ("MEDIUM", "新智元",    "Anthropic Claude新功能Orbit泄露",     "https://finance.sina.com.cn/wm/2026-05-10/doc-inhxkaqp6334720.shtml"),
    ("MEDIUM", "量子位",    "xAI解散但Grok仍在训练",              "https://hub.baai.ac.cn/view/54540"),
    ("MEDIUM", "量子位",    "百度文心大模型5.1发布",              "https://www.qbitai.com/2026/05/415019.html"),
    ("MEDIUM", "量子位",    "两项AI政策同时发布",                 "https://www.qbitai.com/2026/05/414496.html"),
]

# 去重（保留第一个出现的）
seen = set()
deduped = []
for row in PRIORITY_URLS:
    if row[3] not in seen:
        seen.add(row[3])
        deduped.append(row)
PRIORITY_URLS = deduped

os.makedirs(os.path.join(DEEP_DIR, TODAY), exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

log_lines = []
ts = datetime.now().strftime("%Y-%m-%d %H:%M")
log_lines.append(f"[{ts}] market_wechat_deep_capture_round START | urls={len(PRIORITY_URLS)}")

results = []

def strip_frontmatter(text):
    if not isinstance(text, str):
        return text
    body = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)
    return body.strip()

def clean_body(text):
    if not isinstance(text, str):
        return ""
    text = strip_frontmatter(text)
    text = re.sub(r'\[?(?:广告|Advertisement|闭上|关闭)\]?', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def fetch_web(url, timeout=60):
    """用 subprocess curl 调用 jina reader / web fetch"""
    cmd = [
        'curl', '-s', '--max-time', str(timeout),
        '-H', 'Accept: text/markdown',
        f'https://r.jina.ai/{url}',
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout + 5)
        if r.returncode == 0 and r.stdout:
            return r.stdout.decode('utf-8', errors='replace')
    except Exception:
        pass
    return ""

for i, (priority, source, title_hint, url) in enumerate(PRIORITY_URLS):
    safe_name = re.sub(r'[^\w]', '_', source)[:20]
    safe_hint = re.sub(r'[^\w]', '_', title_hint)[:30]
    out_name  = f"{DATE_SHORT}__{safe_name}__{safe_hint}.md"
    out_path  = os.path.join(DEEP_DIR, TODAY, out_name)
    raw_path  = out_path.replace('.md', '__raw.md')

    print(f"[{i+1}/{len(PRIORITY_URLS)}] [{priority}] {source} | {title_hint[:40]}")

    raw_text = fetch_web(url)
    status = "success" if raw_text else "failed"

    # 保存原始导出
    with open(raw_path, 'w', encoding='utf-8') as f:
        f.write(f"<!-- WEB_FETCH RAW EXPORT -->\n<!-- source: {source} -->\n<!-- url: {url} -->\n<!-- priority: {priority} -->\n<!-- fetched: {datetime.now().isoformat()} -->\n\n{raw_text}")

    body = clean_body(raw_text)
    body_preview = body[:200] if body else ""

    frontmatter = f"""---
source: "{source}"
title: "{title_hint}"
url: "{url}"
priority: "{priority}"
captured: "{datetime.now().isoformat()}"
fetch_status: "{status}"
---

"""
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter + body)

    badge = "🟢" if status == "success" else "🔴"
    print(f"    {badge} {status} | {len(body)} chars | → {os.path.basename(out_path)}")
    log_lines.append(f"{'OK' if status=='success' else 'FAIL'} [{priority}] {source} | {title_hint[:40]} | {status} | {len(body)}chars")

    results.append({
        "priority": priority,
        "source": source,
        "title": title_hint,
        "url": url,
        "status": status,
        "path": out_path,
        "preview": body_preview[:120]
    })

# 生成捕获报告
from collections import Counter
priority_counts = Counter(r['priority'] for r in results)
success_count   = sum(1 for r in results if r['status'] == 'success')

report_lines = []
report_lines.append(f"# 微信全文深抓补轮报告 | {TODAY} {ts}")
report_lines.append("")
report_lines.append(f"> cron触发：19:49 CST  |  抓取窗口：T日全量信号  |  目标：下午新增条目补全文")
report_lines.append("")
report_lines.append(f"## 抓取统计")
report_lines.append(f"- 总计：{len(results)} 条  |  成功：{success_count}  |  失败：{len(results)-success_count}")
report_lines.append(f"- HIGH：{priority_counts.get('HIGH',0)} 条  |  MEDIUM：{priority_counts.get('MEDIUM',0)} 条")
report_lines.append("")
report_lines.append(f"## 成功条目（{success_count} 条）")
report_lines.append("")
for r in results:
    badge = "🟢" if r['status'] == 'success' else "🔴"
    report_lines.append(f"{badge} **[{r['priority']}]** {r['source']} — {r['title']}")
    if r['preview']:
        report_lines.append(f"   > {r['preview'][:100]}...")
    report_lines.append("")
report_lines.append(f"## 失败条目")
report_lines.append("")
for r in results:
    if r['status'] != 'success':
        report_lines.append(f"🔴 **[{r['priority']}]** {r['source']} — {r['title']}")
        report_lines.append(f"   > {r['url']}")
        report_lines.append("")
report_lines.append("")
report_lines.append(f"*market-scout runtime | 微信全文深抓补轮 | 不构成投资结论*")

report_md = '\n'.join(report_lines)
report_path = os.path.join(LOG_DIR, f"{DATE_SHORT}__wechat-deep-capture-report.md")
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report_md)

log_path = os.path.join(LOG_DIR, f"{DATE_SHORT}__wechat-deep-capture.log")
with open(log_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(log_lines) + '\n')

print(f"\n✓ 报告 → {os.path.basename(report_path)}")
print(f"✓ 日志 → {os.path.basename(log_path)}")

# 触发 learning memo builder
print("\n=== 触发 learning memo builder ===")
try:
    r = subprocess.run(
        ['python3',
         os.path.join(ROOT, "09_runbooks", "scripts", "market_learning_memo_builder.py"),
         '--date', TODAY, '--count', '10', '--write-log'],
        capture_output=True, text=True, timeout=60
    )
    if r.stdout: print(r.stdout)
    if r.returncode != 0 and r.stderr:
        print(r.stderr[:300])
except Exception as e:
    print(f"memo builder error: {e}")

print(f"\n✓ 深抓补轮完成 | {success_count}/{len(results)} 成功")