# 同行资本市场内容系统｜Web / RSS Source Registry

## 1. 用途

记录站点、博客、newsletter、RSS feed、官网更新页等需要长期监控的 source。

适合收录：

- 官方博客
- 产品 changelog
- company blog
- longform 媒体站点
- RSS feed

---

## 2. 表结构

| source_key | source_name | source_type | handle_or_url | region | language | signal_quality | citation_reliability | capture_method | status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| web__openai_news | OpenAI News | company | https://openai.com/news | global | en | high | high | rss / official-feed | active | 已切到 OpenAI 官方 RSS，优先保证稳定和一手性；正文继续回链单篇 OpenAI 原文页 |
| web__anthropic_news | Anthropic News | company | https://www.anthropic.com/news | global | en | high | high | web / jina-reader | active | 官方研究、产品、MCP 与安全口径 |
| web__deepmind_blog | Google DeepMind Blog | company | https://deepmind.google/discover/blog/ | global | en | high | high | web / jina-reader | active | 前沿模型、研究、机器人与产品化信号 |
| web__google_blog_ai | Google AI Blog | company | https://blog.google/technology/ai/ | global | en | high | high | rss / official-feed | active | 已切到 Google AI 官方 RSS，适合稳定承接 Gemini / 产品集成 / 平台动作 |
| web__xai_news | xAI News | company | https://x.ai/news | global | en | high | high | web / jina-reader | active | 已验证可稳定抓到新闻列表与单篇入口，适合盯模型、产品、组织动作 |
| web__figure_news | Figure News | company | https://www.figure.ai/news/helix-02 | global | en | high | high | web / browser-reader / manual | candidate | 具身智能官方一手口径，高价值但需更稳抓取链 |
| web__tesla_ai_robotics | Tesla AI & Robotics | company | https://www.tesla.com/en_QA/AI | global | en | medium | high | web / manual | candidate | Optimus / 机器人长期必盯的官方原始入口 |
| web__deepmind_robotics | Google DeepMind Robotics | company | https://deepmind.google/blog/gemini-robotics-brings-ai-into-the-physical-world/ | global | en | medium | high | web / manual | candidate | 具身方向的一手研究 / 产品页，适合后续扩成站点级入口 |
| web__nvidia_blog | NVIDIA Blog | company | https://blogs.nvidia.com/ | global | en | high | high | web / jina-reader | active | 已修正为可用首页入口并验证抓取，适合补 AI 硬件 / 推理卡 / 数据中心官方变化 |
| web__simon_willison | Simon Willison | kol | https://simonwillison.net/ | global | en | high | medium | web / jina-reader | active | LLM / agent / coding workflow 高质量个人观察 |
| web__latent_space | Latent Space | media | https://www.latent.space/ | global | en | high | medium | web / rss / jina-reader | active | AI engineer、agent、infra、workflow 强相关 |
| web__one_useful_thing | One Useful Thing | kol | https://www.oneusefulthing.org/ | global | en | high | medium | web / jina-reader | active | AI 使用范式、教育和用户行为视角强 |
| web__interconnects | Interconnects | media | https://www.interconnects.ai/ | global | en | high | medium | web / jina-reader | active | 模型与产业交界的深度解释力强 |
| web__understanding_ai | Understanding AI | media | https://www.understandingai.org/ | global | en | medium | medium | web / jina-reader | active | 适合补技术解释和通俗拆解 |
| web__deeplearningai_batch | DeepLearning.AI The Batch | media | https://www.deeplearning.ai/the-batch/ | global | en | high | medium | web / jina-reader | active | AI 大事件归纳入口，适合二次延伸 |
| web__techcrunch_ai | TechCrunch AI | media | https://techcrunch.com/category/artificial-intelligence/ | global | en | high | medium | web / jina-reader | active | 新公司、新融资、新产品发现效率高 |
| web__infoq_ai_ml | InfoQ AI/ML | media | https://www.infoq.com/ai-ml-data-eng/ | global | en | medium | medium | web / jina-reader | active | 工程、架构、应用落地题材较多 |
| web__semianalysis | SemiAnalysis | media | https://www.semianalysis.com/ | global | en | high | medium | web / jina-reader | active | 模型 / infra / 硬件大背景解释力强 |
| web__huggingface_blog | Hugging Face Blog | company | https://huggingface.co/blog | global | en | high | high | web / jina-reader | active | 开源模型、工具、生态变化入口 |
| web__sensortower_blog | Sensor Tower Blog | media | https://sensortower.com/blog | global | en | medium | medium | web / browser-reader | candidate | AI App 增长与排名变化的辅助验证层 |
| web__diandian_appintel | 点点数据 | aggregator | https://www.diandian.com/ | cn | zh | medium | low-medium | web / manual | candidate | AI 应用榜单与类别移动的重要补源 |
| web__itjuzi | IT 桔子 / 中国人工智能融资报告 | aggregator | https://cdn.itjuzi.com/pdf/1a5ee188cfde75809136ad47f4077d3a.pdf | cn | zh | high | high | web / jina-reader / official-pdf-fallback | active | 已切到 IT 桔子公开 AI 融资报告 PDF 的稳定抓取链路；直连库页仍会被 `412` 挡住，当前先用公开报告补国内融资规模、阶段、区域与子赛道结构 |
| web__jiqizhixin_site | 机器之心官网 | media | https://www.jiqizhixin.com/ | cn | zh | high | medium | web / jina-reader | active | 已验证可稳定抓到首页热点与文章入口，和公众号形成双重覆盖 |
| web__qbitai_site | 量子位官网 | media | https://www.qbitai.com/ | cn | zh | high | medium | web / jina-reader | active | 已验证可稳定抓到首页热点与文章入口，适合补中文模型 / 产品传播层 |
| web__zhidx | 智东西 | media | https://zhidx.com/ | cn | zh | high | medium | web / jina-reader | active | 已验证可抓首页热点，适合补具身、硬件、产业化与大公司落地叙事 |
| web__36kr_ai | 36氪 AI | media | https://www.36kr.com/information/AI | cn | zh | medium | medium | web / jina-reader | active | 已验证 AI 频道抓取，适合补创业 / 商业化 / 融资叙事入口 |
| web__ifanr_ai | 爱范儿 AIGC | media | https://www.ifanr.com/category/aigc | cn | zh | medium | medium | web / jina-reader | active | 已验证 AIGC 分类页可抓，适合补大众产品、AI 硬件和消费侧传播角度 |
| web__openclaw_docs | OpenClaw / ClawHub Docs | tool_builder | https://docs.openclaw.ai/tools/clawhub | global | en | high | high | web / jina-reader | active | skill / tool / agent 能力更新，高贴合主战场 |
| web__sspai_ai | 少数派 AI Tag | media | https://sspai.com/tag/AI | cn | zh | medium | medium | web / jina-reader | active | 中文语境下的应用型、体验型 AI 内容入口 |
| web__finsmes_ai_gnews | FinSMEs AI Funding / Google News Fallback | media | https://news.google.com/rss/search?q=site:finsmes.com%20artificial%20intelligence%20funding&hl=en-US&gl=US&ceid=US:en | global | en | medium | low | rss / gnews-site-filter | active | FinSMEs 官方页直连受阻时的可运行 fallback；仅作融资入口，正式引用仍需回链官网或公告 |
| web__finsmes_ai | FinSMEs AI | media | https://www.finsmes.com/category/ai | global | en | medium | low | web / browser-reader / alt-provider | candidate | 融资线索强，但当前 direct 与 Jina 都受限，暂不进主盘 |
| web__theinformation_briefings | The Information Briefings | media | https://www.theinformation.com/briefings | global | en | high | medium | web / manual | candidate | 高价值快讯，但付费墙和引用限制需要人工判断 |

---

## 3. V2 备注

- 本表同时承担两种角色：
  - `L1` 原始信源池
  - `L2 / L3` 的网站面补充池
- 对官方站点，优先级高于媒体转载。
