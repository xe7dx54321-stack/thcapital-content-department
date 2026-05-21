# 同行资本市场内容系统｜2026-03-25 Seed Candidate Pool

## 1. 这份池子是干什么的

这不是“所有可能 source 的大全”，而是：

> **按当前业务目标，重选出来的第一版业务化 seed pool。**

其中：

- A 类直接进入正式 watchlist
- B 类保留为高优先级战略源
- C 类作为人工补录 / 待核验短名单

---

## 2. A 类：直接进正式盘

| lane | source_key | source_name | platform | handle_or_url | why_selected | registry_target |
| --- | --- | --- | --- | --- | --- | --- |
| breakout_growth | `trend__hn_frontpage` | Hacker News Frontpage | web | https://news.ycombinator.com/ | builder / startup / agent 话题最稳定的早期热榜之一 | trend |
| breakout_growth | `trend__hn_topstories_api` | Hacker News Top Stories API | web | https://hacker-news.firebaseio.com/v0/topstories.json | 适合结构化抓当日高热入口，再反查正文 | trend |
| breakout_growth | `trend__github_trending` | GitHub Trending | web | https://github.com/trending | 开源 agent / workflow / tools 新热点发现效率高 | trend |
| financing_newco | `trend__yc_launches_ai` | YC Launches | web | https://www.ycombinator.com/launches.json | 已验证可直连结构化 JSON，适合发现新产品、新业务和潜在融资线索 | trend |
| product_discovery | `trend__trend_hunt_ai` | Trend Hunt / Product Hunt Mirror | web | https://trend-hunt.com/api/search?q=ai&locale=en&limit=10&category=AI | 可稳定拿到 Product Hunt 相关产品发现线索，适合作为官方 PH 被拦时的 operational mirror | trend |
| product_discovery | `trend__trend_hunt_ai_agents` | Trend Hunt / Product Hunt Mirror / AI Agents | web | https://trend-hunt.com/api/search?q=ai+agents&locale=en&limit=10 | 专门补 agent 产品发现，能显著提高主战场命中率 | trend |
| product_discovery | `trend__trend_hunt_automation` | Trend Hunt / Product Hunt Mirror / Automation | web | https://trend-hunt.com/api/search?q=automation&locale=en&limit=10&category=Productivity | 补 workflow / automation 相邻战场高热对象，后续可回切到 agent 叙事 | trend |
| official_updates | `web__anthropic_news` | Anthropic News | web | https://www.anthropic.com/news | 官方一手更新，agent / MCP / Claude 相关价值高 | web-rss |
| official_updates | `web__openai_news` | OpenAI News | web | https://openai.com/news | 已验证可经 Jina 稳定拿到列表与单篇链接，适合承接官方大事件 | web-rss |
| official_updates | `web__deepmind_blog` | Google DeepMind Blog | web | https://deepmind.google/discover/blog/ | 模型、机器人、研究与产品化变化的重要一手源 | web-rss |
| official_updates | `web__google_blog_ai` | Google AI Blog | web | https://blog.google/technology/ai/ | Google 系 AI 生态更新，适合观察平台层变化 | web-rss |
| official_updates | `x__openai` | OpenAI | x | @OpenAI | 已验证可抓到近期帖文摘录，适合作为官方事件补充入口 | x |
| official_updates | `x__openaidevs` | OpenAI Devs | x | @OpenAIDevs | API / SDK / devtool 更新密度高，适合补充官方站未第一时间展开的线索 | x |
| official_updates | `x__anthropic_ai` | Anthropic | x | @AnthropicAI | 适合补官方社交快讯与产品/安全动态 | x |
| expert_view | `web__simon_willison` | Simon Willison | web | https://simonwillison.net/ | agent / coding / tools 方向高密度观点源 | web-rss |
| expert_view | `web__latent_space` | Latent Space | web | https://www.latent.space/ | builder / infra / agent workflow 拆解很强 | web-rss |
| expert_view | `web__one_useful_thing` | One Useful Thing | web | https://www.oneusefulthing.org/ | 适合拿用户教育、行为变化、AI 使用范式的题 | web-rss |
| expert_view | `web__interconnects` | Interconnects | web | https://www.interconnects.ai/ | 偏模型与产业交界，适合做深度解释和观点延伸 | web-rss |
| expert_view | `x__karpathy` | Andrej Karpathy | x | @karpathy | 已验证可抓观点片段；适合拆方法论与延伸产品线索 | x |
| expert_view | `x__swyx` | swyx | x | @swyx | agent infra / builder 社区桥梁型强源，适合抓高密度观点 | x |
| expert_view | `x__hwchase17` | Harrison Chase | x | @hwchase17 | agent builder 与框架动态价值高 | x |
| official_updates | `web__deeplearningai_batch` | DeepLearning.AI The Batch | web | https://www.deeplearning.ai/the-batch/ | AI 大事件梳理效率高，适合做二次延伸入口 | web-rss |
| financing_newco | `web__techcrunch_ai` | TechCrunch AI | web | https://techcrunch.com/category/artificial-intelligence/ | 新公司、新融资、新产品发现效率高 | web-rss |
| financing_newco | `web__finsmes_ai_gnews` | FinSMEs AI Funding / Google News Fallback | web | https://news.google.com/rss/search?q=site:finsmes.com%20artificial%20intelligence%20funding&hl=en-US&gl=US&ceid=US:en | FinSMEs 官方页 blocked 时的可运行融资 fallback，适合补 AI 融资对象池 | web-rss |
| adjacent_research | `web__semianalysis` | SemiAnalysis | web | https://www.semianalysis.com/ | agent 相关模型 / infra / 硬件的大背景解释力强 | web-rss |
| open_source_skill | `web__huggingface_blog` | Hugging Face Blog | web | https://huggingface.co/blog | 开源模型、工具、生态变化高频入口 | web-rss |
| open_source_skill | `web__openclaw_docs` | OpenClaw / ClawHub Docs | web | https://docs.openclaw.ai/tools/clawhub | skill / tool / agent 能力相关，和 TH 主战场高度契合 | web-rss |
| cn_signal | `web__sspai_ai` | 少数派 AI Tag | web | https://sspai.com/tag/AI | 中文语境里较容易产出可改写的应用型选题 | web-rss |
| video_demo | `youtube__openai` | OpenAI YouTube | youtube | https://www.youtube.com/feeds/videos.xml?channel_id=UCXZCJLdBC09xxGZ6gcdrc6A | 官方发布会、demo、访谈一手视频源 | youtube |
| video_demo | `youtube__ycombinator` | Y Combinator YouTube | youtube | https://www.youtube.com/feeds/videos.xml?user=YCombinator | 创始人访谈、创业产品、build-in-public 线索密度高 | youtube |
| video_demo | `youtube__googledeepmind` | Google DeepMind YouTube | youtube | https://www.youtube.com/@GoogleDeepMind | 模型、研究、机器人和 demo 适合拆选题 | youtube |
| video_demo | `youtube__aidotengineer` | AI Engineer | youtube | https://www.youtube.com/@aiDotEngineer | agent 实操、workflow、stack 教学密度高 | youtube |
| video_demo | `youtube__latent_space_pod` | Latent Space Pod | youtube | https://www.youtube.com/@LatentSpacePod | 和长文版形成互补，适合抓访谈和观点演化 | youtube |
| video_demo | `youtube__langchain` | LangChain | youtube | https://www.youtube.com/@LangChain | agent builder 教学、案例、框架更新较密集 | youtube |
| reddit_discussion | `trend__reddit_localllama_daily` | Reddit / LocalLLaMA Daily Top | web | https://www.reddit.com/r/LocalLLaMA/top.json?t=day&limit=10 | 已验证可抓 top 与 thread，上游真问题密度高 | trend |
| reddit_discussion | `trend__reddit_claude_daily` | Reddit / ClaudeAI Daily Top | web | https://www.reddit.com/r/ClaudeAI/top.json?t=day&limit=10 | 可观察 Claude / agent 使用反馈与吐槽 | trend |
| reddit_discussion | `trend__reddit_chatgpt_daily` | Reddit / ChatGPT Daily Top | web | https://www.reddit.com/r/ChatGPT/top.json?t=day&limit=10 | 覆盖大盘使用反馈，但需后续噪音控制 | trend |

---

## 3. B 类：高价值，但先不当默认主盘

| lane | source_key | source_name | platform | handle_or_url | why_not_A_now | next_step |
| --- | --- | --- | --- | --- | --- | --- |
| product_discovery | `trend__producthunt_ai` | Product Hunt AI Topic | web | https://www.producthunt.com/topics/artificial-intelligence | 官方 topic 页有价值，但当前 direct 抓取仍被拦 | 日常先走 trend-hunt mirror，后续再接 official API / 浏览器链 |
| financing_newco | `web__finsmes_ai` | FinSMEs AI | web | https://www.finsmes.com/category/ai | 融资线索价值高，但当前直接访问受限 | 留作战略源，后续测试浏览器链 |
| financing_newco | `web__theinformation_briefings` | The Information Briefings | web | https://www.theinformation.com/briefings | 价值高，但存在付费墙 / 引用限制 | 人工筛读，作为加分源 |
| build_in_public | `x__levelsio` | Pieter Levels | x | @levelsio | 一人公司、快速验证、爆款业务视角强 | 作为邻接高热观察源保留 |
| breakout_growth | `trend__bilibili_popular_all` | Bilibili Popular All | bilibili | https://www.bilibili.com/v/popular/all | 热榜价值有，但 AI 过滤还不够精确 | 后续加关键词/作者过滤后再升格 |

---

## 4. C 类：人工补录 / 待核验短名单

| lane | source_key | source_name | platform | handle_or_url | why_track | current_mode |
| --- | --- | --- | --- | --- | --- | --- |
| wechat_cn_ai | `wechat__liangziwei` | 量子位 | wechat | wechat://量子位 | AI 大盘与热点快讯覆盖全 | 候选，待接入微信链 |
| wechat_cn_ai | `wechat__xinzhiyuan` | 新智元 | wechat | wechat://新智元 | 模型、产品、行业事件密度高 | 候选，待接入微信链 |
| wechat_cn_ai | `wechat__jiqizhixin` | 机器之心 | wechat | wechat://机器之心 | AI 研究和产业报道较全 | 候选，待接入微信链 |
| wechat_cn_ai | `wechat__geekpark` | 极客公园 | wechat | wechat://极客公园 | 产品与创业叙事适合公域转写 | 候选，待接入微信链 |
| wechat_cn_ai | `wechat__founder_park` | Founder Park | wechat | wechat://Founder Park | 创业者和 AI 产品观察强 | 候选，待接入微信链 |
| wechat_cn_ai | `wechat__appsso` | APPSO | wechat | wechat://APPSO | 大众产品热点和可传播角度较多 | 候选，待接入微信链 |
| wechat_cn_ai | `wechat__guiguang_ai_tools` | 归藏的AI工具箱 | wechat | wechat://归藏的AI工具箱 | 工具测评 / 教学 / 玩法线索有价值 | 候选，待接入微信链 |
| wechat_cn_ai | `wechat__guixingren_pro` | 硅星人Pro | wechat | wechat://硅星人Pro | 海外 AI 创业和产品语境补充强 | 候选，待接入微信链 |

---

## 5. 动态派生规则

以下不是固定 source，但必须进入 skill 规则：

1. **融资事件派生链**
   - 项目名 → 官网 → 创始人 X → YouTube demo → GitHub / 文档 → 社区讨论

2. **大神观点派生链**
   - 原观点 → 评论区高信号回复 → 被提及产品 / skill / workflow → 对立观点

3. **开源热点派生链**
   - Trending repo → README / docs → maintainer 账号 → demo 视频 → 使用案例

4. **热视频派生链**
   - 视频 → 原始事件 / 原文 / 产品 → 多平台是否同步发酵 → 是否可换角度重写

---

## 6. 这轮候选池的实际含义

这轮不是把所有平台一次性做深，而是先做到两件事：

1. **用 A 类把系统每天能吃的确定性输入补足**
2. **用 B / C 类把真正重要但还不顺手的地方先纳入治理范围**

也就是说，后面不是重新从零找 source，而是在这份池子上持续升降级。
