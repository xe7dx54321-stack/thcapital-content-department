# 同行资本市场内容系统｜Trend Entrance Registry

## 1. 用途

记录不是单一账号，而是趋势入口、榜单页、聚合页、社区热门页等 source。

它们不一定直接产生成文观点，但常常最适合：

- 发现突发热点
- 观察增长速度
- 判断话题是否开始扩散

---

## 2. 表结构

| source_key | source_name | source_type | handle_or_url | region | language | signal_quality | citation_reliability | capture_method | status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trend__hn_frontpage | Hacker News Frontpage | trend_entrance | https://news.ycombinator.com/ | global | en | high | medium | rss / hn-official-feed | active | 已切到 HN 官方 RSS，并增加 AI / agent / builder 关键词闸门，适合观察技术扩散 |
| trend__hn_topstories_api | Hacker News Top Stories API | trend_entrance | https://hacker-news.firebaseio.com/v0/topstories.json | global | en | high | medium | api / web | active | 适合结构化抓取当日高热入口，再反查正文 |
| trend__github_trending | GitHub Trending | trend_entrance | https://github.com/trending | global | en | high | medium | web / jina-reader | active | 适合发现 agent / workflow / tools 开源热点 |
| trend__yc_launches_ai | YC Launches | trend_entrance | https://www.ycombinator.com/launches.json | global | en | high | medium | json / yc-launches-direct | active | 已验证可直连 `launches.json`，适合发现新项目、新业务、融资前后线索 |
| trend__trend_hunt_ai | Trend Hunt / Product Hunt Mirror | trend_entrance | https://trend-hunt.com/api/search?q=ai&locale=en&limit=10&category=AI | global | en | medium | low | api / third-party-mirror | active | 已验证可稳定返回 Product Hunt 相关产品列表；作为发现入口使用，事实引用需回链官网 / PH 页面 |
| trend__trend_hunt_ai_agents | Trend Hunt / Product Hunt Mirror / AI Agents | trend_entrance | https://trend-hunt.com/api/search?q=ai+agents&locale=en&limit=10 | global | en | high | low | api / third-party-mirror | active | 适合专门盯 agent 产品发现；比泛 AI query 更贴主战场 |
| trend__trend_hunt_automation | Trend Hunt / Product Hunt Mirror / Automation | trend_entrance | https://trend-hunt.com/api/search?q=automation&locale=en&limit=10&category=Productivity | global | en | medium | low | api / third-party-mirror | active | 适合补 workflow / automation 邻接热点，便于发现可切回 agent 叙事的对象 |
| trend__producthunt_ai | Product Hunt AI Topic | trend_entrance | https://www.producthunt.com/topics/artificial-intelligence | global | en | medium | low | web / browser-reader / official-api | candidate | 官方 topic 页仍受验证页影响；日常运行先走 Trend Hunt mirror，后续再接 PH token |
| trend__reddit_localllama_daily | Reddit / LocalLLaMA Daily Top | community | https://www.reddit.com/r/LocalLLaMA/top.json?t=day&limit=10 | global | en | high | low | reddit-readonly / public-json | active | 已验证可抓 top / search / thread，真问题、真反馈、高赞讨论价值高 |
| trend__reddit_claude_daily | Reddit / ClaudeAI Daily Top | community | https://www.reddit.com/r/ClaudeAI/top.json?t=day&limit=10 | global | en | medium | low | reddit-readonly / public-json | active | 已验证可通过无鉴权 JSON 入口抓取讨论与评论上下文 |
| trend__reddit_chatgpt_daily | Reddit / ChatGPT Daily Top | community | https://www.reddit.com/r/ChatGPT/top.json?t=day&limit=10 | global | en | medium | low | reddit-readonly / public-json | active | 已验证可抓，但仍需后续噪音控制 |
| trend__huggingface_daily_papers | Hugging Face Daily Papers | trend_entrance | https://huggingface.co/papers | global | en | high | medium | web / jina-reader | active | 本轮已验证可稳定抓取 papers 列表；保留 `451` 软失败兜底，但已进入默认主链 |
| trend__arxiv_cs_ai_recent | arXiv cs.AI recent | trend_entrance | https://arxiv.org/list/cs.AI/recent | global | en | medium | high | rss / arxiv-official-feed | active | 已接入官方 RSS，适合补论文与方法创新早期信号 |
| trend__diandian_app_rank | 点点数据 AI / App 排名 | trend_entrance | https://www.diandian.com/ | cn | zh | medium | low-medium | web / manual | candidate | AI app 榜单与增长变化入口，可判断产品化热度 |
| trend__baidu_realtime | 百度热搜 | heat_validation | https://top.baidu.com/board?tab=realtime | cn | zh | medium | low | web / jina-reader + ai-gate | active | 已接入内容工厂主链路，用来判断 AI / agent / robotics 话题是否开始破圈 |
| trend__zhihu_hotlist | 知乎热榜 | heat_validation | https://api.zhihu.com/topstory/hot-list?limit=20 | cn | zh | medium | low-medium | public json / zhihu hot-list | active | 已验证可直连公开 JSON；适合补中文问答场域的 AI 讨论热度和用户疑问 |
| trend__newrank_wechat | 新榜（泛入口） | heat_validation | https://www.newrank.cn/ | cn | zh | medium | low | web / manual | candidate | 泛新榜入口保留；当前正式日跑已切到更贴 AI 主题的 `trend__newrank_ai_media_rank` |
| trend__newrank_ai_media_rank | 新榜 AI 新媒体影响力排行榜 | heat_validation | https://www.newrank.cn/public/info/rank_detail.html?name=ai | cn | zh | medium | low-medium | public json / searchByName + local OCR | active | 已验证可直连公开接口；当前通过本地 OCR 补出头部账号和关键字段，更适合做 AI 垂类账号势能、微信生态和竞品观察的月度验证层 |
| trend__feigua_bilibili | 飞瓜 B站科技热视频榜 | heat_validation | https://bz.feigua.cn/ranking/DailyHotVideoV2/20260325/1/30.html | cn | zh | medium | low-medium | html / feigua tech hot video + bilibili backlink | active | 已验证可直连科技分榜 HTML；当前会自动回链 B站原视频，适合补 B 站视频场域的 AI / robotics / hardware 热度验证 |
| trend__bilibili_popular_all | Bilibili Popular All / AI-Relevant | heat_validation | https://api.bilibili.com/x/web-interface/popular?ps=30&pn=1 | cn | zh | medium | low | api / bilibili-popular + ai-relevant-gate | active | 已接入内容工厂视频链；保留 AI 相关且可重构的娱乐向 / 产品向话题，不收纯泛娱乐噪音 |

---

## 3. V2 备注

- 这张表现在同时承接：
  - `L2 技术 / 产品扩散`
  - `L4 平台热度验证`
- `L4` 的职责不是最早发现，而是验证：
  - 是否破圈
  - 是否值得今天正式写
  - 是否已经出现跨平台共振
