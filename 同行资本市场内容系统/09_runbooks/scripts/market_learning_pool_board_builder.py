#!/usr/bin/env python3
"""
market_learning_pool_board_builder.py
对齐 memo 与 ready draft packs，生成学习看板（Board）：
  - /11_frontstage/YYYYMMDD__head-media-learning-board.html
  - /11_frontstage/YYYYMMDD__head-media-learning-board.md
  - /11_frontstage/YYYYMMDD__head-media-learning-board.snapshot.json
若样本不足，落轻量空板不报错。不要混入研究线资产，不要发群消息。
"""
import argparse, os, json, re, sys
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
LOG_DIR = os.path.join(ROOT, "10_logs")

def load_memo(date_str):
    """读取 memo 文件内容"""
    path = os.path.join(FRONSTAGE, f"{date_str.replace('-', '')}__head-media-learning-memo.md")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def scan_ready_drafts():
    """扫描 04_drafts/ready 下的 draft packs，返回 [{title, path, snippet}]"""
    drafts_dir = os.path.join(ROOT, "04_drafts", "ready")
    packs = []
    if os.path.isdir(drafts_dir):
        for f in os.listdir(drafts_dir):
            if f.endswith('.md'):
                p = os.path.join(drafts_dir, f)
                try:
                    with open(p, 'r', encoding='utf-8') as fh:
                        raw = fh.read()
                    body = re.sub(r'^---\n.*?---\n', '', raw, flags=re.DOTALL).strip()
                    packs.append({'title': f, 'path': p, 'snippet': body[:200]})
                except Exception:
                    pass
    return packs

def build_board(date_str, count=8, write_files=True, write_log=False):
    memo = load_memo(date_str)
    drafts = scan_ready_drafts()
    log_lines = [f"[{datetime.now().isoformat()}] market_learning_pool_board_builder running for {date_str}"]

    # 简单合并逻辑：memo 样本 + draft 对齐
    sections = []

    # --- Section 1: 头部样本来源 ---
    if memo:
        sections.append(("## 📥 今日头部样本", memo))
        log_lines.append("INFO: loaded memo")
    else:
        sections.append(("## 📥 今日头部样本", "⚠️ 无 memo 数据"))

    # --- Section 2: Ready Draft Packs 对齐 ---
    if drafts:
        draft_lines = ["### 当前 Ready Draft Packs"]
        for d in drafts[:5]:
            draft_lines.append(f"- **{d['title']}**：{d['snippet'][:80]}...")
        sections.append(("\n".join(draft_lines), ""))
        log_lines.append(f"INFO: aligned {len(drafts[:5])} draft packs")
    else:
        sections.append(("### 当前 Ready Draft Packs", "⚠️ 无 ready drafts"))

    # --- Build Markdown ---
    date_label = f"{date_str} ({datetime.now().strftime('%A')})"
    md_lines = [f"# 头部号学习池 · 对标看板 | {date_label}"]
    md_lines.append("")
    md_lines.append(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} | 学习窗：T-1 17:00 → T 14:30")
    md_lines.append("")

    for heading, body in sections:
        md_lines.append(heading)
        md_lines.append("")
        if body:
            md_lines.append(body)
        md_lines.append("")

    md_content = '\n'.join(md_lines)

    # --- Build HTML ---
    html_content = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>头部号学习池 | {date_label}</title>
<style>
body{{font-family:-apple-system,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;color:#222;line-height:1.6}}
h1{{color:#1a1a2e;border-bottom:2px solid #e94560;padding-bottom:.5rem}}
h2{{color:#16213e;margin-top:1.5rem}}
.meta{{background:#f8f9fa;padding:.5rem .75rem;border-radius:6px;font-size:.85rem;color:#555}}
pre{{background:#f4f4f4;padding:1rem;border-radius:6px;overflow-x:auto;white-space:pre-wrap}}
.footer{{margin-top:2rem;padding-top:1rem;border-top:1px solid #ddd;font-size:.8rem;color:#888}}
</style>
</head>
<body>
<h1>📊 头部号学习池 · 对标看板 | {date_label}</h1>
<div class="meta">学习窗：T-1 17:00 → T 14:30 &nbsp;|&nbsp; 生成：{datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
"""
    # 把 md 转成简易 html
    for line in md_lines[2:]:  # skip title/meta
        if line.startswith('# '):
            html_content += f"<h2>{line[2:]}</h2>\n"
        elif line.startswith('## '):
            html_content += f"<h3>{line[3:]}</h3>\n"
        elif line.startswith('### '):
            html_content += f"<h4>{line[4:]}</h4>\n"
        elif line.startswith('- '):
            html_content += f"<li>{line[2:]}</li>\n"
        elif line.startswith('>'):
            html_content += f"<blockquote>{line[2:]}</blockquote>\n"
        elif line.strip():
            html_content += f"<p>{line}</p>\n"
    html_content += '<div class="footer">由 content-analyst 自动生成 · 请勿混入研究线资产</div>\n</body>\n</html>'

    # --- Build Snapshot JSON ---
    snapshot = {
        "date": date_str,
        "generated_at": datetime.now().isoformat(),
        "learning_window": "T-1 17:00 → T 14:30",
        "memo_loaded": memo is not None,
        "draft_packs_aligned": len(drafts[:5]),
        "board_md_preview": md_content[:500],
        "status": "success" if (memo or drafts) else "lightweight_empty"
    }

    out_base = f"{date_str.replace('-', '')}__head-media-learning-board"
    results = []

    if write_files:
        os.makedirs(FRONSTAGE, exist_ok=True)

        md_path = os.path.join(FRONSTAGE, f"{out_base}.md")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        results.append(md_path)
        log_lines.append(f"OK: wrote {md_path}")

        html_path = os.path.join(FRONSTAGE, f"{out_base}.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        results.append(html_path)
        log_lines.append(f"OK: wrote {html_path}")

        json_path = os.path.join(FRONSTAGE, f"{out_base}.snapshot.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, ensure_ascii=False, indent=2)
        results.append(json_path)
        log_lines.append(f"OK: wrote {json_path}")

    if write_log:
        log_path = os.path.join(LOG_DIR, f"{date_str}__head-media-learning-board.log")
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(log_lines) + '\n')
        results.append(log_path)

    print('\n'.join(log_lines[-5:]))
    return results

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--date', default=datetime.now().strftime('%Y-%m-%d'))
    ap.add_argument('--count', type=int, default=8)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--write-log', action='store_true')
    args = ap.parse_args()
    build_board(args.date, args.count, write_files=args.write, write_log=args.write_log)
