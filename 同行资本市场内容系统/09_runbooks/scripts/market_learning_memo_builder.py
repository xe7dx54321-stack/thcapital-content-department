#!/usr/bin/env python3
"""
market_learning_memo_builder.py
扫描 02_topic_radar/deep_articles 中的头部号 full_text 样本，
生成学习备忘（Memo），写入 11_frontstage/YYYYMMDD__head-media-learning-memo.md
可选 --write-log 写 log。
"""
import argparse, os, glob, re, sys
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

ROOT = str(get_project_paths(_REPO_ROOT).market_content_root)
FRONSTAGE = os.path.join(ROOT, "11_frontstage")
DEEP_ARTICLES = os.path.join(ROOT, "02_topic_radar", "deep_articles")
LOG_DIR = os.path.join(ROOT, "10_logs")

def extract_frontmatter(content):
    """提取 markdown frontmatter 中的字段"""
    fm = {}
    m = re.match(r'^---\n(.*?)---\n', content, re.DOTALL)
    if not m:
        return fm
    for line in m.group(1).splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm

def scan_deep_articles(count):
    """扫描 deep_articles 目录，返回 (source_name, content, meta) 列表"""
    articles = []
    if not os.path.isdir(DEEP_ARTICLES):
        return articles
    # 递归扫描所有 .md 文件
    for path in glob.glob(os.path.join(DEEP_ARTICLES, "**/*.md"), recursive=True):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw = f.read()
            fm = extract_frontmatter(raw)
            # 去掉 frontmatter
            body = re.sub(r'^---\n.*?---\n', '', raw, flags=re.DOTALL).strip()
            source = fm.get('source', fm.get('media', fm.get('author', os.path.basename(path))))
            articles.append({
                'source': source,
                'title': fm.get('title', '无标题'),
                'date': fm.get('date', fm.get('published', '未知')),
                'word_count': len(body),
                'body_preview': body[:300] if body else '',
                'path': path
            })
        except Exception:
            pass
    # 按 word_count 降序，取前 count 条（模拟头部号样本逻辑）
    articles.sort(key=lambda x: x['word_count'], reverse=True)
    return articles[:count]

def build_memo(date_str, count, write_log=False):
    arts = scan_deep_articles(count)
    log_lines = [f"[{datetime.now().isoformat()}] market_learning_memo_builder running for {date_str}, count={count}"]

    lines = []
    lines.append(f"# 头部号学习备忘 | {date_str}")
    lines.append("")
    lines.append(f"> 学习窗：T-1 17:00 → T 14:30  |  抓取时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")

    if not arts:
        lines.append("⚠️ deep_articles 目录无样本，落轻量空板。")
        log_lines.append("INFO: no deep_articles samples found, wrote lightweight empty memo")
    else:
        lines.append(f"## 扫描结果（{len(arts)} 条头部样本）")
        lines.append("")
        for i, a in enumerate(arts, 1):
            lines.append(f"### {i}. {a['source']} — {a['title']}")
            lines.append(f"- 日期：{a['date']}  |  字数：{a['word_count']}")
            if a['body_preview']:
                lines.append(f"- 引言：{a['body_preview'][:150]}...")
            lines.append("")

        # 简单归纳：提取共性关键词
        all_bodies = ' '.join(a['body_preview'] for a in arts if a['body_preview'])
        log_lines.append(f"INFO: sampled {len(arts)} articles")

    memo_md = '\n'.join(lines)
    out_name = f"{date_str.replace('-', '')}__head-media-learning-memo.md"
    out_path = os.path.join(FRONSTAGE, out_name)
    os.makedirs(FRONSTAGE, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(memo_md)

    log_lines.append(f"OK: memo written to {out_path}")
    if write_log:
        log_path = os.path.join(LOG_DIR, f"{date_str}__head-media-learning-memo.log")
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(log_lines) + '\n')
    print('\n'.join(log_lines[-3:]))
    return out_path

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--date', default=datetime.now().strftime('%Y-%m-%d'))
    ap.add_argument('--count', type=int, default=8)
    ap.add_argument('--write-log', action='store_true')
    args = ap.parse_args()
    build_memo(args.date, args.count, args.write_log)
