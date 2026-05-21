#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from statistics import median
from zoneinfo import ZoneInfo


CN_TZ = ZoneInfo("Asia/Shanghai")
ROOT = Path("/Users/apple/Documents/同行资本内容部门/内容生产系统")
DEEP_ARTICLE_ROOT = ROOT / "02_topic_radar" / "deep_articles"
BRAND_ROOT = ROOT / "08_brand_assets"
LOG_ROOT = ROOT / "10_logs"
KV_RE = re.compile(r"^- `([^`]+)`: ?`?(.*?)`?$")
IMAGE_RE = re.compile(r"^!\[.*?\]\((https?://[^)]+)\)")
SKIP_TITLE_TOKENS = ("招聘", "榜单", "早知道", "极客早知道")
PREFERRED_SOURCES = {
    "Founder Park",
    "量子位",
    "机器之心",
    "智东西",
    "极客公园",
    "爱范儿",
    "APPSO",
    "赛博禅心",
    "数字生命卡兹克",
    "饼干哥哥AGI",
    "袋鼠帝AI客栈",
}


@dataclass
class DeepArticle:
    path: Path
    title: str
    source_name: str
    canonical_url: str
    published_at: str
    status: str
    image_count: int
    normalized_char_count: int
    raw_body_path: Path | None
    opening_paragraphs: list[str]
    first_image_after_text_paragraphs: int | None
    image_break_count: int
    published_dt: datetime | None
    artifact_dt: datetime | None
    export_day: date | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a head-media learning memo for TH Capital content factory")
    parser.add_argument("--date", default=datetime.now(CN_TZ).date().isoformat())
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--window-start", default="17:00")
    parser.add_argument("--window-end", default="14:30")
    parser.add_argument("--write-log", action="store_true")
    return parser.parse_args()


def clean(value: str, fallback: str = "n/a") -> str:
    value = re.sub(r"\s+", " ", value).strip().strip("`")
    return value if value else fallback


def now_cst() -> str:
    return datetime.now(CN_TZ).strftime("%Y-%m-%d %H:%M:%S CST")


def parse_cst(raw: str) -> datetime | None:
    raw = clean(raw, "")
    if not raw or raw == "n/a":
        return None
    for fmt in (
        "%Y-%m-%d %H:%M:%S CST",
        "%Y-%m-%d %H:%M CST",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
    ):
        try:
            return datetime.strptime(raw, fmt).replace(tzinfo=CN_TZ)
        except ValueError:
            continue
    return None


def parse_hm(raw: str) -> time:
    hour, minute = [int(part) for part in raw.split(":", 1)]
    return time(hour=hour, minute=minute)


def business_window(date_text: str, start_hm: str, end_hm: str) -> tuple[datetime, datetime]:
    target_day = date.fromisoformat(date_text)
    start_day = target_day - timedelta(days=1)
    return (
        datetime.combine(start_day, parse_hm(start_hm), tzinfo=CN_TZ),
        datetime.combine(target_day, parse_hm(end_hm), tzinfo=CN_TZ),
    )


def parse_artifact_dt(path: Path) -> datetime | None:
    match = re.match(r"(?P<day>\d{8})_(?P<hms>\d{6})__", path.name)
    if not match:
        return None
    try:
        parsed = datetime.strptime(
            f"{match.group('day')} {match.group('hms')}",
            "%Y%m%d %H%M%S",
        )
    except ValueError:
        return None
    return parsed.replace(tzinfo=CN_TZ)


def parse_export_day(raw_path: Path | None) -> date | None:
    if raw_path is None:
        return None
    match = re.search(r"/(\d{4}-\d{2}-\d{2})/", str(raw_path))
    if not match:
        return None
    try:
        return date.fromisoformat(match.group(1))
    except ValueError:
        return None


def article_in_business_window(article: DeepArticle, start_dt: datetime, end_dt: datetime) -> bool:
    timestamps = [article.published_dt, article.artifact_dt]
    if any(ts is not None and start_dt <= ts <= end_dt for ts in timestamps):
        return True
    if article.export_day is not None and start_dt.date() <= article.export_day <= end_dt.date():
        return True
    return False


def article_is_future(article: DeepArticle, target_day: date) -> bool:
    known_days = [
        article.published_dt.date() if article.published_dt is not None else None,
        article.artifact_dt.date() if article.artifact_dt is not None else None,
        article.export_day,
    ]
    return any(day is not None and day > target_day for day in known_days)


def article_recency(article: DeepArticle) -> datetime:
    timestamps = [ts for ts in [article.published_dt, article.artifact_dt] if ts is not None]
    if timestamps:
        return max(timestamps)
    if article.export_day is not None:
        return datetime.combine(article.export_day, time.min, tzinfo=CN_TZ)
    return datetime(1970, 1, 1, tzinfo=CN_TZ)


def article_sort_key(
    article: DeepArticle,
    *,
    target_day: date,
    start_dt: datetime,
    end_dt: datetime,
) -> tuple[int, int, float, int, str]:
    if article_in_business_window(article, start_dt, end_dt):
        bucket = 0
    elif article.published_dt is not None and article.published_dt.date() == target_day:
        bucket = 1
    elif article.artifact_dt is not None and article.artifact_dt.date() == target_day:
        bucket = 2
    elif article.export_day == target_day:
        bucket = 3
    else:
        bucket = 4
    preferred_rank = 0 if article.source_name in PREFERRED_SOURCES else 1
    recency = article_recency(article).timestamp()
    return (bucket, preferred_rank, -recency, -article.normalized_char_count, article.path.name)


def parse_kv_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = KV_RE.match(raw_line.strip())
        if not match:
            continue
        key, value = match.groups()
        fields[clean(key)] = clean(value)
    return fields


def read_raw_body(raw_body_path: Path | None) -> str:
    if not raw_body_path or not raw_body_path.exists():
        return ""
    return raw_body_path.read_text(encoding="utf-8")


def extract_content_paragraphs(raw_text: str) -> tuple[list[str], int | None, int]:
    if not raw_text:
        return [], None, 0
    paragraphs: list[str] = []
    current: list[str] = []
    first_image_after_text_paragraphs: int | None = None
    image_break_count = 0
    text_paragraph_count = 0

    def flush_current() -> None:
        nonlocal text_paragraph_count
        if not current:
            return
        paragraph = clean(" ".join(current), "")
        current.clear()
        if not paragraph:
            return
        if paragraph.startswith("# "):
            return
        if paragraph.startswith("- Source:") or paragraph.startswith("- URL:") or paragraph.startswith("- Fetched:"):
            return
        paragraphs.append(paragraph)
        text_paragraph_count += 1

    for raw_line in raw_text.splitlines():
        line = raw_line.strip()
        if not line:
            flush_current()
            continue
        if IMAGE_RE.match(line):
            flush_current()
            image_break_count += 1
            if first_image_after_text_paragraphs is None:
                first_image_after_text_paragraphs = text_paragraph_count
            continue
        current.append(line)
    flush_current()
    return paragraphs, first_image_after_text_paragraphs, image_break_count


def load_article(path: Path) -> DeepArticle | None:
    fields = parse_kv_fields(path)
    title = clean(fields.get("title", "n/a"))
    source_name = clean(fields.get("source_name", "n/a"))
    status = clean(fields.get("status", "n/a"))
    if status != "full_text":
        return None
    if any(token in title for token in SKIP_TITLE_TOKENS):
        return None
    try:
        image_count = int(clean(fields.get("image_count", "0"), "0"))
    except ValueError:
        image_count = 0
    try:
        normalized_char_count = int(clean(fields.get("normalized_char_count", "0"), "0"))
    except ValueError:
        normalized_char_count = 0
    raw_body_value = fields.get("raw_export_copy_path") or fields.get("x_reader_export_path") or "n/a"
    raw_body_path = Path(raw_body_value) if raw_body_value != "n/a" else None
    raw_text = read_raw_body(raw_body_path)
    paragraphs, first_image_after_text_paragraphs, image_break_count = extract_content_paragraphs(raw_text)
    if normalized_char_count < 1200 or len(paragraphs) < 10:
        return None
    published_dt = parse_cst(fields.get("published_at", ""))
    artifact_dt = parse_artifact_dt(path)
    export_day = parse_export_day(raw_body_path)
    return DeepArticle(
        path=path,
        title=title,
        source_name=source_name,
        canonical_url=clean(fields.get("canonical_url", "n/a")),
        published_at=clean(fields.get("published_at", "n/a")),
        status=status,
        image_count=image_count,
        normalized_char_count=normalized_char_count,
        raw_body_path=raw_body_path,
        opening_paragraphs=paragraphs[:6],
        first_image_after_text_paragraphs=first_image_after_text_paragraphs,
        image_break_count=image_break_count,
        published_dt=published_dt,
        artifact_dt=artifact_dt,
        export_day=export_day,
    )


def select_articles(
    count: int,
    *,
    date_text: str | None = None,
    window_start: str = "17:00",
    window_end: str = "14:30",
) -> list[DeepArticle]:
    target_date_text = date_text or datetime.now(CN_TZ).date().isoformat()
    target_day = date.fromisoformat(target_date_text)
    start_dt, end_dt = business_window(target_date_text, window_start, window_end)
    candidates: list[DeepArticle] = []
    for path in sorted(DEEP_ARTICLE_ROOT.glob("*__deep-article.md"), reverse=True):
        article = load_article(path)
        if not article:
            continue
        if article_is_future(article, target_day):
            continue
        candidates.append(article)
    ranked = sorted(
        candidates,
        key=lambda article: article_sort_key(
            article,
            target_day=target_day,
            start_dt=start_dt,
            end_dt=end_dt,
        ),
    )
    return ranked[:count]


def format_excerpt(paragraphs: list[str], limit: int = 2, max_chars: int = 220) -> str:
    chosen = paragraphs[:limit]
    text = " / ".join(chosen)
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip("，。；： ") + "…"


def median_first_image(articles: list[DeepArticle]) -> str:
    values = [item.first_image_after_text_paragraphs for item in articles if item.first_image_after_text_paragraphs is not None]
    if not values:
        return "样本里暂未提取到稳定的首图位置"
    return f"首张图通常出现在前 {median(values)} 个文字段落之后"


def style_learning_section() -> str:
    return """### 6. 文风不是学别人怎么说话，而是学“什么题，讲给谁听”

- **事件科普 / 热点解释**：优先用大白话讲清对象、变化和 why now，术语只保留必要的那几个，并且要顺手翻译。读者进入这类文章时往往是“听说了，但没完全跟上”。
- **产品推荐 / 工具体验**：更适合“场景 → 动作 → 收益”的写法。第一人称体验可以用，但重点不是抒情，而是降低读者试用门槛，让他知道自己能立刻拿走什么。
- **产业判断 / 商业分析**：要比快讯更硬，但不能写成研报。财务口径、竞争格局、商业化变量可以上，但每个专业点都要回答“这跟潜在客户、投资人或普通从业者有什么关系”。
- **教程 / builder 向拆解**：过程感要强，适合写“我怎么判断 / 怎么验证 / 哪一步最容易误判 / 适用边界是什么”。这类题材不怕稍微专业，怕的是只给结论不给路径。
- **争议观点 / 趋势判断**：第一屏要亮立场，但后面必须马上补证据和边界。真正好的观点稿，不是把话说狠，而是把“为什么你会误判”讲透。

一句话总结：不是固定一种“同行资本文风”打天下，而是**在品牌底色稳定的前提下，按题材、读者心智和平台任务重新计算表达方式**。
"""


def build_memo(date_text: str, articles: list[DeepArticle]) -> str:
    sample_rows = "\n".join(
        f"| {index} | {item.source_name} | {item.title} | {item.published_at} | {item.normalized_char_count} | {item.image_count} | {item.first_image_after_text_paragraphs if item.first_image_after_text_paragraphs is not None else 'n/a'} | [原文]({item.canonical_url}) |"
        for index, item in enumerate(articles, start=1)
    )
    opening_notes = "\n".join(
        f"- `{item.source_name}｜{item.title}`：{format_excerpt(item.opening_paragraphs)}"
        for item in articles
    )
    image_examples = "\n".join(
        f"- `{item.source_name}`：全文 `image_count={item.image_count}`，首图位置 `{item.first_image_after_text_paragraphs if item.first_image_after_text_paragraphs is not None else 'n/a'}`，说明图片被拿来承担“对象识别 / 证据锚点 / 节奏换气”，而不是纯装饰。"
        for item in articles[:4]
    )
    return f"""# 头部媒体学习 memo v1

- `generated_at`: `{now_cst()}`
- `date`: `{date_text}`
- `sample_count`: `{len(articles)}`
- `purpose`: `先把学习过程测试跑通，再把学习结果反哺到当前选题成稿逻辑。`

## 本轮样本池

| # | 来源 | 标题 | 发布时间 | 正文字数 | 图片数 | 首图前文字段落数 | 原文 |
| --- | --- | --- | --- | --- | --- | --- | --- |
{sample_rows}

## 先说结论

- 头部号并不是把“背景介绍”死板放在第一段，而是先用一个能抓人的判断或反差，把读者拉住，再在前 10%-15% 内把背景补齐。
- 头部号几乎都会很早给证据，不让文章一直漂在抽象判断上；证据可以是截图、原话、数字卡、结构图。
- 图片不是陪衬，而是正文的一部分：要么证明事实，要么翻译复杂信息，要么作为阅读节奏的停顿点。
- 真正能提高点击率和阅读时长的，不是堆术语，而是把 `headline → stakes → 证据 → 判断 → 下一步` 这条链路压实。

## 我们从样本里学到了什么

### 1. 开头先抓“为什么我现在要继续读”

{opening_notes}

- 共同点 1：第一屏先抛一个已经带判断的句子，不先做百科式背景。
- 共同点 2：开头 2-4 段内就把“发生了什么”和“你为什么该关心”说清楚。
- 共同点 3：判断句先行，但不会马上飞到大框架，通常会很快落到一个真实对象、一个真实动作或一句原话。

### 2. 背景不一定放第一段，但一定不能拖太晚

- 最优位置不是“文章最前面”，而是“钩子之后、抽象判断之前”。
- 如果读者对原始事件陌生，背景最好在前 10%-15% 交代完，否则读者会进入“你在说啥”的状态。
- 背景段的任务不是补百科，而是补最小上下文：对象是谁、这次发生了什么、为什么这个节点和以前不一样。

### 3. 证据要早，不然判断站不住

- {median_first_image(articles)}。
- 头部号喜欢在前半段就放第一张关键图：原文截图、人物原话、产品界面、对比图表。
- 这一步的作用不是“让页面好看”，而是给读者一个“我不是在听你空口分析”的心理锚点。

### 4. 图片要承担三种明确职责

{image_examples}

- **证据图**：原始推文、公告页、问询函首页、产品页标题区。它负责“证明这件事真的发生了”。
- **解释图**：结构图、变量卡、对比卡。它负责“把复杂逻辑翻译成人脑一眼能懂的形状”。
- **节奏图**：长文中段用来换气，避免连续高密度文字把用户赶走。

### 5. 头部号真正高明的地方，不是热闹，而是“翻译”

- Founder Park 这类长文，会把抽象概念翻译成可执行的动作、可量化的收益、可复用的方法。
- 量子位、机器之心这类快热点，会先给事件冲击，再迅速翻译成“行业正在怎么变”。
- 对我们来说，最该学的不是语气，而是这层翻译能力：把模型、机器人、Agent、硬件这些题，翻译成普通人和潜在客户能带走的收益与判断。

{style_learning_section()}

## TH Capital 内容结构 v2

### 微信公众号

1. `钩子`：先给一个反直觉判断或“别只把这事当快讯”的提醒。
2. `背景桥接`：在前 2-4 段内把原始事件、对象、节点补齐。
3. `第一证据锚点`：截图 / 原话 / 关键数字卡尽量前置。
4. `正文拆解`：每个小节只回答一个问题，不重复 headline。
5. `我们的判断`：把热闹翻译成结构变化、商业含义、风险边界。
6. `下一步观察`：告诉读者后面要继续盯什么。

### 小红书

1. `封面先给利益点`：不是“发生了什么”，而是“这件事跟你有什么关系”。
2. `首屏先给结论`：前两屏内必须完成对象、变化、why now。
3. `正文按卡片节奏写`：一屏一件事，短句、硬信息、强转译。
4. `至少一张可收藏图卡`：数字卡 / 变化卡 / 风险卡。
5. `结尾做轻互动`：用“你最关心哪一点”而不是硬转化。

### 今日头条 / 百家号

1. `先把好处讲出来`：普通人会省掉什么动作、节省什么时间、少踩什么坑。
2. `背景简短`：别堆概念，直接说这次变化和你每天怎么用有关。
3. `结构走 3 点拆解`：非常适合“3 个变化 / 3 个信号 / 3 个误区”。
4. `证据 + 风险同场`：既让人觉得真实，也避免写成夸张快讯。

### B站专栏

1. `把热闹拆给你看`：用“大家都在看 A，但真正该看 B”做切口。
2. `正文要有过程感`：从事件、数字、结构、边界一路拆开。
3. `多用图卡和信息块`：B站用户更接受“拆解感”和“带走感”。

## 这轮先采用什么，不采用什么

### Adopt

- 开头先给判断，不做流水账背景。
- 前 10%-15% 内补背景，不让冷启动用户掉线。
- 第一证据锚点前置。
- 图片明确服务“证明 / 解释 / 换气”三种任务。
- 每个平台保留同一套核心判断，但重新计算原生表达。

### Avoid

- 先讲一大段抽象框架，再慢慢告诉读者发生了什么。
- 标题讲的是 A，正文一直在复述 B。
- 每一段都像“值得关注的是 / 某种程度上 / 在这个节点”这种空话。
- 图片只放在开头堆漂亮，不参与正文表达。
- 把长文直接裁成其他平台版本。

## 本轮对当前选题的直接改法

- `apple-siri-chatgpt-entry`：从“技术升级”改成“普通人每天会少做哪几步”，强化 consumer 入口和场景代入。
- `unitree-ipo-economics`：从“机器人很酷”改成“公开数字第一次说明商业模型开始成立”，同时把错把 `6 亿` 当营收的口径纠正回真实财务表达。

## 后续动作

- 这份 memo 作为学习层的第一版固定资产，后续可以每天增量刷新。
- 下一步进入成稿测试：把这套结构直接应用到当前锁题对象，检验落地效果。
"""


def build_empty_memo(date_text: str) -> str:
    return f"""# 头部媒体学习 memo v1

- `generated_at`: `{now_cst()}`
- `date`: `{date_text}`
- `sample_count`: `0`
- `purpose`: `先把学习过程测试跑通，再把学习结果反哺到当前选题成稿逻辑。`

## 当前状态

- 今天还没拿到满足 `full_text + 长文 + 可学习结构` 的头部样本，所以这轮 memo 先落空板，不报错。
- 自动化应该继续跑，等待下一轮 deep capture 补齐学习素材。

## 下一步

- 继续刷新 `deep_articles`，优先吸收图文结构完整、信息密度高、具备真实截图 / 证据锚点的样本。
- 一旦样本充足，再自动回填正式学习 memo。
"""


def main() -> None:
    args = parse_args()
    articles = select_articles(
        args.count,
        date_text=args.date,
        window_start=args.window_start,
        window_end=args.window_end,
    )
    memo = build_memo(args.date, articles) if articles else build_empty_memo(args.date)
    token = args.date.replace("-", "")
    brand_path = BRAND_ROOT / f"{token}__head-media-learning-memo-v1.md"
    brand_path.write_text(memo, encoding="utf-8")

    if args.write_log:
        log_lines = [
            "# Head Media Learning Test",
            "",
            f"- `generated_at`: `{now_cst()}`",
            f"- `memo_path`: `{brand_path}`",
            f"- `sample_count`: `{len(articles)}`",
            "",
            "## Samples",
            "",
        ]
        for item in articles:
            log_lines.extend(
                [
                    f"- `{item.source_name}`｜`{item.title}`｜`images={item.image_count}`｜`chars={item.normalized_char_count}`｜`url={item.canonical_url}`",
                ]
            )
        (LOG_ROOT / f"{token}__head-media-learning-test.md").write_text("\n".join(log_lines).rstrip() + "\n", encoding="utf-8")

    print(brand_path)


if __name__ == "__main__":
    main()
