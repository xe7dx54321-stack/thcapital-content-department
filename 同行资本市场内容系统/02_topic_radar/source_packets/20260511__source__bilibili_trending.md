# Source Packet — trend__bilibili_popular_all

**Source ID:** trend__bilibili_popular_all  
**Captured:** 2026-05-11 23:00 CST  
**Type:** bilibili_trending / platform_signal  
**Channel:** Bilibili 全站排行榜 (all categories)  
**Confidence:** LOW-MEDIUM (web_fetch blocked; bilibili requires JS rendering)  

---

## Capture Status

**Blocked:** Bilibili's trending page requires JS rendering and is not accessible via standard web_fetch or yt-dlp. All automated intake attempts returned empty/blocked content.

---

## Fallback Approach: Cross-Source Validation

From unified_inbox.json entries captured today and prior signal sessions, B站 content signals cross-referenced from:

1. **AI技术 / 科技** content trending in tech circles (from prior sessions)
2. **数码产品体验** — consumer electronics reviews
3. **AI工具测评 / 使用教程** — AI tool tutorials gaining traction
4. **创业 / 投资** content — startup/investment themed videos with B站 audience

## B站热点主题（2026年5月上旬参考）

From cross-source intelligence gathered from prior sessions:

- **AI视频生成工具** — Sora/Runway/Kling相关视频持续有流量
- **国产AI大模型动态** — 智谱/MiniMax/DeepSeek相关讨论
- **AI办公工具测评** — ChatGPT/Claude/国产AI工具对比
- **创投/融资** — 创业者访谈，融资新闻反应热烈
- **可灵/即梦** — 字节/快手AI视频工具使用体验

## Structural Scoring

| Dimension | Score | Note |
|---|---|---|
| 一手性 | 5/10 | Web scraping blocked; relying on cross-source inference |
| 传播性 | 8/10 | B站本身有强社区传播力，AI相关视频在年轻用户中有高互动 |
| 破圈性 | 7/10 | 内容从科技圈进入大众（学生/年轻职场人） |
| 数据硬度 | 3/10 | 无直接抓取，仅推断 |
| 视觉素材 | 8/10 | B站视频天然强视觉素材，但无法直接抓取 |

## Recommended Intake Path

For next cycle, consider:
1. B站 RSS feed: `https://rsshub.app/bilibili/popular/history?date=YYYY-MM-DD`
2. Or a dedicated bilibili scraper with cookie/session auth
3. Or target specific B站UP主的视频更新（订阅制抓取）

## Annotation

B站是一个高价值中文AI/科技内容入口，但本次因技术限制未能直接抓取。建议在下次抓源轮中配置rsshub或类似方案。