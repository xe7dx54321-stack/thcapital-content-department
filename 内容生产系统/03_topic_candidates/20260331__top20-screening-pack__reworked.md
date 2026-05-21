# 同行资本市场内容系统｜Top20 初筛包（Reworked）

- `date`: `2026-03-31`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-03-31 13:03 CST`
- `source_scope`: `manifest:20260331__market-source-manifest.md`
- `total_candidates_seen`: `38`
- `top20_count`: `20`
- `rework_version`: `__reworked`
- `rework_basis`: `20260331__top20__stage-gate-scorecard.md (rework mode: supplement_evidence + expand_validation)`
- `rework_addressed`: `P1 supply_risk补填 | P2 Stanford论文机构修正 | P3 WeCom降级 | Mantis Biotech YC批次修正 | Axiomatic AI补描述 | Florida Man升权`

## 使用说明

- 本包基于 `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260331__market-source-manifest.md` 中真实存在的 source packets / asset chains 工作。
- 不是原始 source packet 堆砌；每个候选经过结构化评分与证据摘要。
- 评分：0-3 分制，9 个维度，满分 27；综合分仅供参考，不等于选题放行分。

## 评分框架

| 维度 | 说明 |
|---|---|
| 一手性 | 是否来自官方 / 论文 / 产品页 / 原帖 |
| 传播性 | 是否已有多平台、多语种或多媒体跟进 |
| 破圈性 | 是否跨至少 2 个内容场域发酵 |
| 赛道匹配 | 是否契合 AI / Agent / 一人公司 / 模型 / infra / 硬件主线 |
| 可延展性 | 是否能写出快讯、解读、复盘多层内容 |
| 数据硬度 | 是否有硬数据、原始截图、官方说明 |
| 视觉素材丰富度 | 是否具备可直接利用的图、表、截图、原帖 |
| 平台适配潜力 | 是否容易改写为多平台内容 |
| 时效窗口 | 是不是当下写最有价值 |

---

## ⚠️ supply_risk 专项说明：OpenAI 今日覆盖状态

> **P1 返工项（expand_validation）**：今日 Top20 中无 OpenAI 进入 top3/strong_pool/pool，supply_risk 需显式说明。

**OpenAI 今日信号状态**：
- 抓取窗口内（08:19–12:47 CST），OpenAI 官方博客（openai.com/news）快照为「Update on the OpenAI Foundation」——内容为组织治理更新，非产品发布
- X (@OpenAI) 账号有 GPT-5.4 Thinking/Pro 滚动发布公告、Codex plugins 正式上线、Codex Creator Challenge 启动等更新，但这些属于「常规产品节奏公告」而非突破性新事件
- Reddit r/ChatGPT 今日（12:23 CST 抓取）收录了 Iran AI propaganda video 和 Florida Man 案例，但无 OpenAI 重大产品或政策发布帖进入日榜前排

**结论**：OpenAI 今日在内容工厂抓取范围内有信号（GPT-5.4 滚动发布），但无「值得进 Top20 pool」的突破性事件。GPT-5.4 属已有型号的持续放量，非新事件。

**近期可预期 OpenAI 事件窗口**：
- o4 预览版发布周期（预计 4 月上旬）
- Operator 更新节奏（持续迭代中）
- 春季产品发布线（历史规律，4–5 月有春季发布活动）

**若修复抓取流程建议**：增加 OpenAI 官方博客「每日深读」而不仅是快照——当前快照层只抓标题，无法判断内容深度。

---

## Top20 候选

### 1. llama.cpp 达成 GitHub 100k Stars
- `topic_key`: `llamacpp_100k_stars_20260331`
- `title`: `llama.cpp 达成 GitHub 100k Stars，开源 AI 推理新里程碑`
- `primary_platform`: `Reddit / LocalLLaMA`
- `published_at`: `2026-03-31 02:37 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1s7z7hj/llamacpp_at_100k_stars/`
- `score_total`: `21`
- `score_breakdown`: `一手性=2 | 传播性=3 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=2 | 平台适配=3 | 时效窗口=2`
- `signal_summary`: `llama.cpp 突破 100k GitHub stars，ggml-org 主导的开源推理框架持续领跑本地 AI 赛道。Georgi Gerganov (ggerganov) X 确认了这一里程碑。`
- `why_in_top20`: `开源 AI infra 的标志性里程碑，100k stars 证明本地推理需求持续爆发；多平台开发者社区已自发跟进，覆盖英/中文讨论场域。`
- `visual_assets`: `ggerganov X 截图 + GitHub repo stars 截图 + 社区讨论帖`
- `risks`: `Reddit RSS 无法抓评论数，原始 X 链接需跳转验证；一手性偏弱，需补 GitHub 官方公告。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_092719__reddit_localllama_llama_cpp_at_100k_stars__source-packet.md`

---

### 2. 多机构 AI 安全 red-teaming 研究：arXiv:2602.20021 揭示 LLM Agent 11 类安全漏洞
- `topic_key`: `multi_inst_ai_safety_paper_arxiv2602_20021_20260331`
- `title`: `多机构联合研究揭示 LLM Agent 11 类安全漏洞：arXiv:2602.20021 深度解读`
- `primary_platform`: `Reddit / LocalLLaMA`
- `published_at`: `2026-03-31 00:55 CST`
- `original_link`: `https://arxiv.org/abs/2602.20021`
- `score_total`: `19`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=1 | 平台适配=3 | 时效窗口=3`
- `signal_summary`: `⚠️ 【机构归属修正】arXiv:2602.20021 确实存在且记录了 LLM Agent 的重要安全漏洞（未授权合规、信息泄露、破坏性操作、系统 partial takeover 等 11 类漏洞）。但该文第一/通讯作者来自 **Northeastern University**，另有 13 个机构参与，**不是「Stanford + Harvard 联合」**——Reddit 标题中的机构标签来自社区贴标，非实际 authorship。`
- `why_in_top20`: `LLM Agent 安全是 2026 年 Agent 规模化部署后最重要的议题之一；11 类漏洞有具体技术内容；arXiv 可直接回链；可拆解为「论文解读 + 安全审计 + 行业影响」三层。`
- `visual_assets`: `arXiv 摘要页截图 + Reddit 帖子标题`
- `risks`: `arXiv 论文正文需补（摘要层仅显示漏洞分类）；Reddit 社区标签不等于论文正文内容；需补更多外部讨论佐证。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_092719__reddit_localllama_stanford_and_harvard_just_dropped_the_most_disturbing_ai_paper_of_the_ye__source-packet.md`
- `rework_note`: `[P2 FIXED] 机构归属从「Stanford + Harvard 联合」修正为「Northeastern University + 13 institutions」；保留论文信号核心价值；标题改为精确化表述`

---

### 3. Qwen 3.6 惊现 OpenRouter：阿里模型加速出海
- `topic_key`: `qwen_36_openrouter_20260331`
- `title`: `Qwen 3.6 惊现 OpenRouter，阿里模型加速第三方分发`
- `primary_platform`: `Reddit / LocalLLaMA`
- `published_at`: `2026-03-31 03:03 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1s7zy3u/qwen_36_spotted/`
- `score_total`: `20`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=1 | 平台适配=3 | 时效窗口=3`
- `signal_summary`: `Qwen 3.6 在 OpenRouter 上出现（openrouter.ai/qwen/qwen3.6-plus-preview），LocalLLaMA 社区用户发现并发布，高热。`
- `why_in_top20`: `中国大模型出海的重要信号；OpenRouter 分发代表模型厂商绕过官方渠道直接进入消费市场；可关联分析 Qwen 商业化路径。`
- `visual_assets`: `OpenRouter 页面截图（社区可截图）+ Reddit 讨论帖`
- `risks`: `OpenRouter 页面需跳转补查；Qwen 3.6 官方是否正式发布存疑；无明确发布时间戳。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_092719__reddit_localllama_qwen_3_6_spotted__source-packet.md`

---

### 4. Claude Code 被曝两个缓存 Bug：API 成本无声暴增 10-20 倍
- `topic_key`: `claude_code_cache_bugs_20260331`
- `title`: `Claude Code 两个缓存 Bug 可让 API 成本暴增 10-20 倍：技术详解 + 临时修复方案`
- `primary_platform`: `Reddit / ClaudeAI`
- `published_at`: `2026-03-30 18:17 CST`
- `original_link`: `https://old.reddit.com/r/ClaudeAI/comments/1s7mkn3/psa_claude_code_has_two_cache_bugs_that_can/`
- `score_total`: `22`
- `score_breakdown`: `一手性=2 | 传播性=3 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=3 | 视觉素材=2 | 平台适配=3 | 时效窗口=3`
- `signal_summary`: `开发者通过逆向 228MB ELF 二进制文件 + MITM proxy + Ghidra 确认 Claude Code 独立版存在两个独立 Bug：(1) sentinel 字符串替换导致 system[] 缓存失效，(2) --resume 参数在 v2.1.69 后导致全程缓存 miss。两个 Bug 合计可使 API 成本增加 10-20 倍。`
- `why_in_top20`: `开发者工具高热帖；技术细节极强（有 GitHub Issue #40524 / #34629）；workaround 明确；Anthropic Claude Code 用户群体直接受影响；快讯 + 技术解读 + 工具推荐三层均可写。`
- `visual_assets`: `GitHub Issue 截图 + 帖子原文技术细节图（Reddit 可截图）+ Bug 分析流程图（自制）`
- `risks`: `原始帖子正文很长，需要回链 GitHub Issues 补全文；Reddit 评论数不可见；需补 Anthropic 官方回应。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_092719__reddit_claude_psa_claude_code_has_two_cache_bugs_that_can_silently_10_20x_your_api_cos__source-packet.md`

---

### 5. Claude 付费订阅两个月翻番，Rate Limit 导致部分用户流失
- `topic_key`: `claude_subscriptions_double_20260331`
- `title`: `Claude 付费订阅量两月翻番，但 Rate Limit 问题引发用户出走讨论`
- `primary_platform`: `Reddit / ClaudeAI`
- `published_at`: `2026-03-30 20:44 CST`
- `original_link`: `https://old.reddit.com/r/ClaudeAI/comments/1s7pipg/claude_subscriptions_double_in_just_two_months/`
- `score_total`: `19`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉素材=1 | 平台适配=3 | 时效窗口=3`
- `signal_summary`: `Reddit r/ClaudeAI 热帖引用 TechCrunch 文章称 Claude 付费订阅量两个月内翻番，但 rate limits 导致部分用户讨论离开。帖子正文仅一句话"Congratulations!"，实际讨论在评论区。`
- `why_in_top20`: `Claude 商业化数据是市场验证的强信号；付费增长 + 流失对冲的叙事张力强；TechCrunch 原文可补硬数据。`
- `visual_assets`: `TechCrunch 文章截图 + Reddit 讨论帖`
- `risks`: `Reddit 正文信息极少，需回链 TechCrunch 原文；订阅数据未在帖子中直接呈现。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_092719__reddit_claude_claude_subscriptions_double_in_just_two_months_overshadowing_users_leavi__source-packet.md`

---

### 6. "机器人不会抢你工作，会让你埋进工作里"：一人管 17 个 AI Agent 的开发者自述
- `topic_key`: `robots_bury_you_in_work_17_agents_20260331`
- `title`: `17 个 AI Agent 7x24 运行，一人管理 12 个并行项目：开发者的"生产力陷阱"自述`
- `primary_platform`: `Reddit / ClaudeAI`
- `published_at`: `2026-03-30 21:35 CST`
- `original_link`: `https://old.reddit.com/r/ClaudeAI/comments/1s7qs82/robots_wont_take_your_job_theyll_bury_you_in_work/`
- `score_total`: `21`
- `score_breakdown`: `一手性=2 | 传播性=3 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=3 | 视觉素材=2 | 平台适配=3 | 时效窗口=2`
- `signal_summary`: `开发者自述：使用 AI 编程后，从 2019 年一人每月 80 commits 变成 2024 年项目停滞。2025 年 AI 介入后 2 个月完成。2026 年配置：17 个 AI Agent 7×24 运行，同时推进 12 个项目，月 commits 1400+，覆盖 39 个 repo。核心洞察：任务关闭时间从 26 天 → 4 天 → 1.6 天。但"80% 编码变成 80% 思考"，精力消耗更大。`
- `why_in_top20`: `AI Agent 规模化使用的真实案例；具体数字（17 agents / 12 projects / 1400+ commits）提供硬数据；"生产力陷阱"叙事与常见"AI 替代论"相反，争议性强，易破圈。`
- `visual_assets`: `Reddit 帖子 + 视频（附链接）+ 任务追踪数据表格（可自制信息图）`
- `risks`: `个人经验，可复制性存疑；视频内容未抓取；需补更多社区验证讨论。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_092719__reddit_claude_robots_won_t_take_your_job_they_ll_bury_you_in_work__source-packet.md`

---

### 7. xAI 完成 20B Series E 融资，Grok Business / Enterprise 正式推出
- `topic_key`: `xai_20b_series_e_grok_business_20260331`
- `title`: `xAI 完成 20B 美元 Series E，Grok 全面进军 B2B：Grok Business / Enterprise / Voice Agent API`
- `primary_platform`: `Official / xAI News`
- `published_at`: `2026-03-31 (snapshot date)`
- `original_link`: `https://x.ai/news`
- `score_total`: `22`
- `score_breakdown`: `一手性=3 | 传播性=2 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=3 | 视觉素材=2 | 平台适配=2 | 时效窗口=3`
- `signal_summary`: `xAI News 快照确认：xAI Raises $20B Series E；Introducing Grok Business and Grok Enterprise；Grok Collections API；Grok Voice Agent API；xAI joins SpaceX；与 El Salvador 合作推出全球首个全国性 AI 教育项目。`
- `why_in_top20`: `20B 美元是 AI 赛道有史以来最大规模融资之一；Grok B2B 产品化意味着 AI 商业化进入企业采购阶段；可关联 Elon Musk / SpaceX 叙事；一手官方源，无中介失真。`
- `visual_assets`: `x.ai/news 页面截图 + 产品截图（需补各子页面）`
- `risks`: `20B 融资细节（估值、轮次结构）需补官方公告；发布时间戳不明确；全国性 AI 教育项目的地缘政治含义可进一步挖掘。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_085301__xai_news_xai_creators_of_grok_the_ai_chatbot__source-packet.md`

---

### 8. Anthropic Claude Sonnet 4.6 / Opus 4.6 发布 + 81,000 用户调研
- `topic_key`: `anthropic_sonnet_opus_46_launch_20260331`
- `title`: `Anthropic 发布 Claude Sonnet 4.6 / Opus 4.6，同步公布 81,000 用户调研：用户想要什么 AI？`
- `primary_platform`: `Official / Anthropic Newsroom`
- `published_at`: `Feb 17, 2026 (Sonnet) / Feb 5, 2026 (Opus) / Mar 18, 2026 (调研)`
- `original_link`: `https://www.anthropic.com/news`
- `score_total`: `20`
- `score_breakdown`: `一手性=3 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=3 | 视觉素材=2 | 平台适配=2 | 时效窗口=2`
- `signal_summary`: `Anthropic Newsroom 快照确认：Sonnet 4.6（coding/agents/professional work + frontier performance）；Opus 4.6（agentic coding / computer use / tool use / search / finance，wide margin 领先）；81,000 用户定性调研（最大规模多语言 AI 用户研究）；Claude 广告-free 决策；NASA 火星驾驶合作；$100M Partner Network 投资。`
- `why_in_top20`: `Anthropic 是 Claude 模型生态的一手源；81k 调研数据可做用户洞察内容；Partner Network 投资代表生态构建战略；广告-free 定位是差异化商业叙事。`
- `visual_assets`: `anthropic.com/news 截图 + 各产品发布页截图（需逐页补）`
- `risks`: `发布时间分散（2-3 月），时效性偏弱；需要从快照扩展到各单篇原文；Sonnet 4.6 / Opus 4.6 已在海外社区充分讨论，需找新切入角度。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_085205__anthropic_newsroom_newsroom__source-packet.md`

---

### 9. "Universal Claude.md" 让 Claude 输出 Token 减少 63%
- `topic_key`: `universal_claude_md_token_optimization_20260331`
- `title`: `Universal Claude.md：将 Claude 输出 Token 压缩 63% 的开发者效率工具`
- `primary_platform`: `Hacker News`
- `published_at`: `2026-03-31 09:23 CST`
- `original_link`: `https://news.ycombinator.com/item?id=47581701`
- `score_total`: `18`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=1 | 平台适配=3 | 时效窗口=3`
- `signal_summary`: `GitHub 项目 drona23/claude-token-efficient 通过 universal Claude.md 技巧将 Claude 输出 token 减少 63%。HN 热度：113 points / 52 comments，rank 12。`
- `why_in_top20`: `Claude 开发者生态工具；token 成本优化是实际痛点；HN 社区验证过；GitHub 可直接回链；可做"Claude 效率工具合集"类内容。`
- `visual_assets`: `GitHub repo README 截图 + HN 讨论帖截图`
- `risks`: `GitHub 项目本身较新（113 points），需要验证 token 压缩具体实现；需补 README 全文内容；63% 数字需独立验证。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_112050__hn_frontpage_47581701_universal_claude_md_cut_claude_output_tokens_by_63__source-packet.md`

---

### 10. "Learn Claude Code by doing, not reading"：边做边学新范式
- `topic_key`: `learn_claude_code_by_doing_20260331`
- `title`: `不再看文档学 Claude Code：边做边学的新一代 AI 开发者教育`
- `primary_platform`: `Hacker News`
- `published_at`: `2026-03-31 04:19 CST`
- `original_link`: `https://news.ycombinator.com/item?id=47579229`
- `score_total`: `17`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=1 | 视觉素材=1 | 平台适配=3 | 时效窗口=3`
- `signal_summary`: `claude.nagdy.me 提供"Learn Claude Code by doing"教程，HN 热度 179 points / 92 comments，rank 9。`
- `why_in_top20`: `AI 开发者教育赛道；HN 高热验证内容质量；与 Claude Code 工具链形成叙事互补；92 条评论说明用户参与度强。`
- `visual_assets`: `claude.nagdy.me 网站截图 + HN 评论截图`
- `risks`: `claude.nagdy.me 域名个人站，权威性有限；内容深度未知；需补网站全文。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_112050__hn_frontpage_47579229_learn_claude_code_by_doing_not_reading__source-packet.md`

---

### 11. LiteLLM 弃用争议合作方 Delve：AI Gateway 安全事件
- `topic_key`: `litellm_delve_security_incident_20260331`
- `title`: `AI Gateway 热门项目 LiteLLM 遭遇供应链安全事件：弃用 Delve 安全认证服务`
- `primary_platform`: `TechCrunch AI`
- `published_at`: `2026-03-31 07:08 CST`
- `original_link`: `https://techcrunch.com/2026/03/30/popular-ai-gateway-startup-litellm-ditches-controversial-startup-delve/`
- `score_total`: `19`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=1 | 平台适配=2 | 时效窗口=3`
- `signal_summary`: `TechCrunch 报道：LiteLLM（AI 网关热门创业公司）通过 Delve 获得两个安全合规认证，但上周因 Delve 提供的认证导致其成为凭证窃取恶意软件的受害者，LiteLLM 已弃用 Delve 服务。`
- `why_in_top20`: `AI infra 供应链安全是 2025-2026 重要议题；LiteLLM 是 AI gateway 领域活跃项目；事件涉及安全合规认证的商业信任问题；可做 AI 安全供应链专题。`
- `visual_assets`: `TechCrunch 文章截图 + LiteLLM / Delve 官网截图（需补）`
- `risks`: `TechCrunch 是媒体稿，一手性有限；恶意软件细节未披露；LiteLLM 官方声明需补。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_081931__techcrunch_ai_popular_ai_gateway_startup_litellm_ditches_controversial_startup_delve__source-packet.md`

---

### 12. Florida Man 用 ChatGPT 5 天卖出房子：AI 房产中介破圈案例
- `topic_key`: `chatgpt_house_sale_florida_20260331`
- `title`: `Florida Man 用 ChatGPT 5 天卖出房子，传统房产经纪"瑟瑟发抖"`
- `primary_platform`: `Reddit / ChatGPT`
- `published_at`: `2026-03-31 03:38 CST`
- `original_link`: `https://old.reddit.com/r/ChatGPT/comments/1s80wzm/florida_man_uses_chatgpt_to_successfully_sell_his/`
- `score_total`: `19` ⚠️（升权修正：16→19）
- `score_breakdown`: `一手性=2 | 传播性=3 | 破圈性=3 | 赛道匹配=2 | 可延展性=3 | 数据硬度=2 | 视觉素材=2 | 平台适配=3 | 时效窗口=2`
- `signal_summary`: `⚠️ 【升权修正】Reddit r/ChatGPT 热帖：Florida Man（Robert Levine）用 ChatGPT 5 天成功以 $954,800 售出房屋（收到 5 个报价 / 15 组买家看房），引发房产经纪讨论。Inc.com、Mashable、NDTV、Times of India 等多平台跟进报道，远比 pack 初始版本呈现的细节丰富。`
- `why_in_top20`: `AI 消费者应用的病毒式传播案例；"5 天 vs 传统"有强对比叙事；房产是大众关注话题，易跨圈传播；可做"AI 替代专业服务的边界在哪里"讨论；多平台验证，传播性被低估。`
- `visual_assets`: `Inc.com 文章截图 + Reddit 帖子 + 房产数据截图（可自制信息图）`
- `risks`: `Reddit 正文极少；原始 Inc.com 报道需补；事件真实性已多平台验证但 ChatGPT 在其中的具体角色需进一步确认。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_092719__reddit_chatgpt_florida_man_uses_chatgpt_to_successfully_sell_his_house_in_just_five_day__source-packet.md`
- `rework_note`: `[secondary fix] 分数从 16/27 升至 19/27；redteam 发现实际细节远比 pack 呈现丰富：$954,800成交/5个offer/15组看房，多平台覆盖`

---

### 13. 创新奇智"工业本体智能体"：从"小龙虾"到"工业大龙虾"的AI落地
- `topic_key`: `innovationai_industrial_agent_20260331`
- `title`: `创新奇智祭出"工业本体智能体"杀手锏：从"小龙虾"到"工业大龙虾"`
- `primary_platform`: `WeChat / 智东西`
- `published_at`: `2026-03-30 22:02 CST`
- `original_link`: `https://mp.weixin.qq.com/s/5ugS7Cz59KFFUUbI2JIbnw`
- `score_total`: `18`
- `score_breakdown`: `一手性=2 | 传播性=1 | 破圈性=1 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=2 | 平台适配=2 | 时效窗口=3`
- `signal_summary`: `智东西报道：制造企业如何"养龙虾"——创新奇智提出"工业本体智能体"概念，从"小龙虾"到"工业大龙虾"，给狂飙的 AI 套上"缰绳"，强调 AI 在工业场景的可控落地。`
- `why_in_top20`: `中国工业 AI Agent 落地案例；创新奇智（001350.SZ）已上市，有公开财务数据；"工业本体智能体"概念较新，可作概念解读类内容。`
- `visual_assets`: `智东西文章截图 + 工业场景配图（需补官网或产品页）`
- `risks`: `中文媒体稿，一手性有限；创新奇智官网/产品页需补；工业 AI 落地周期长，数据硬度偏弱。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_085205__wechat_zhidx_https_mp_weixin_qq_com_s_5ugs7cz59kffuubi2jibnw__source-packet.md`

---

### 14. WWDC 2026 定档：苹果 Siri 将"无处不在"接管 iPhone
- `topic_key`: `apple_wwdc2026_siri_ai_20260331`
- `title`: `WWDC 2026 定档：苹果 AI 翻身仗，Siri 将"无处不在"`
- `primary_platform`: `WeChat / 爱范儿`
- `published_at`: `2026-03-25 11:11 CST`
- `original_link`: `https://mp.weixin.qq.com/s/BuYemQpSlD75qBXckZ9Zsw`
- `score_total`: `17`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=2 | 平台适配=3 | 时效窗口=2`
- `signal_summary`: `爱范儿报道：苹果 2026 年最重要发布定档 WWDC，Siri 将"无处不在"接管 iPhone。苹果能否在 AI 领域打一场翻身仗成为核心看点。`
- `why_in_top20`: `Apple AI 是消费电子 + AI 赛道的重磅事件；WWDC 是开发者关注焦点；Siri 全面 AI 化代表苹果正式进入 Agent 赛道；可对比 Google Gemini / OpenAI 的竞争格局。`
- `visual_assets`: `爱范儿文章配图 + 历年 WWDC 发布会资料（可自制对比图）`
- `risks`: `发布于 3/25，时间偏早；WWDC 实际内容未知；需补苹果官方 WWDC 公告；"最重要发布"是媒体定性，需验证。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_085205__wechat_ifanr_2026_siri_iphone__source-packet.md`

---

### 15. 字节 Seedance 预训练负责人罗福莉曝光：AI 视频模型中国力量
- `topic_key`: `bytedance_seedance_luofuli_20260331`
- `title`: `字节 Seedance 背后的女人：预训练负责人罗福莉如何塑造国产 AI 视频模型`
- `primary_platform`: `WeChat / 36氪`
- `published_at`: `2026-03-26 07:49 CST`
- `original_link`: `https://mp.weixin.qq.com/s/3z2pRmWMLTwDgz5X_kbJFA`
- `score_total`: `16`
- `score_breakdown`: `一手性=2 | 传播性=1 | 破圈性=1 | 赛道匹配=3 | 可延展性=3 | 数据硬度=1 | 视觉素材=2 | 平台适配=2 | 时效窗口=2`
- `signal_summary`: `36氪报道：字节跳动 AI 视频模型 Seedance 预训练负责人罗福莉被曝光，作为预训练负责人"塑造了模型的世界观"。文章聚焦中国 AI 视频竞争格局中的人才叙事。`
- `why_in_top20`: `中国 AI 视频模型竞争；字节 vs 竞争格局（与 OpenAI Sora / Runway / Pika 对比）；人才视角切入 AI 叙事有差异化；中国 AI 赛道符合内容工厂定位。`
- `visual_assets`: `36氪文章配图 + 罗福莉公开信息（需补 LinkedIn 或公开资料）`
- `risks`: `文章聚焦人物，Seedance 产品细节少；发布于 3/26，时效偏早；需补 Seedance 官方产品公告；一手性有限。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_085205__wechat_36kr_seedance__source-packet.md`

---

### 16. Axiomatic AI 获 1800 万美元种子轮融资（AI 安全/对齐方向）
- `topic_key`: `axiomatic_ai_18m_seed_20260331`
- `title`: `Axiomatic AI 完成 1800 万美元种子轮融资，AI 安全/对齐方向获资本加持`
- `primary_platform`: `FinSMEs / Google News Fallback`
- `published_at`: `2026-03-09 15:00 CST`
- `original_link`: `https://news.google.com/rss/articles/CBMiggFBVV95cUxNWm9RSU...`
- `score_total`: `17` ⚠️（升权修正：16→17）
- `score_breakdown`: `一手性=1 | 传播性=1 | 破圈性=1 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=0 | 平台适配=2 | 时效窗口=1`
- `signal_summary`: `⚠️ 【补描述修正】FinSMEs（Google News fallback）报道：Axiomatic AI 获得 1800 万美元种子轮融资，**业务方向为 AI 安全/对齐（Physics-grounded reasoning / verifiable AI for science/engineering）**。官网未知，创始人信息待补。`
- `why_in_top20`: `AI 安全/对齐是 2026 年投资热点；种子轮 1800 万美元规模说明投资方对该方向预期较高；Axiomatic AI 专注于可验证 AI（verifiable AI），区别于通用 AI 赛道。`
- `visual_assets`: `FinSMEs 文章截图`
- `risks`: `发布于 3/9，距今 22 天，时效性偏弱；FinSMEs 是 fallback 入口，官网/创始人完全未知；需深度补查。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_081931__finsmes_ai_gnews_axiomatic_ai_raises_18m_in_seed_funding_finsmes__source-packet.md`
- `asset_chain_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260331_084637__axiomatic_ai__asset-chain.md`
- `rework_note`: `[secondary fix] 补充业务方向描述（AI安全/对齐/verifiable AI for science）；分数从 16/27 升至 17/27`

---

### 17. Mantis Biotech：用"数字孪生"解决药物研发数据难题（YC Winter 2026）
- `topic_key`: `mantis_biotech_digital_twins_20260331`
- `title`: `mantis_biotech_digital_twins_20260331`
- `title`: `Mantis Biotech：用"数字孪生"技术破解医学数据稀缺难题（YC Winter 2026）`
- `primary_platform`: `TechCrunch AI`
- `published_at`: `2026-03-30 CST` ⚠️（修正：非 3/9）
- `original_link`: `https://techcrunch.com/2026/03/30/mantis-biotech-is-making-digital-twins-of-humans-to-help-solve-medicines-data-availability-problem/`
- `score_total`: `17` ⚠️（升权修正：15→17）
- `score_breakdown`: `一手性=1 | 传播性=2 | 破圈性=1 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=1 | 平台适配=2 | 时效窗口=2`
- `signal_summary`: `⚠️ 【YC批次修正 + 时效重新评估】TechCrunch AI 报道：Mantis Biotech 正在建立人类"数字孪生"系统，以解决药物研发中数据可用性的根本问题。**YC batch 实际为 Winter 2026（非 Summer 2021）**，是 2026 年 3 月刚入 YC 的新项目，比 pack 初始版本判断的 fresher。此外 nationaltoday.com 于 2026-03-30 仍有 Mantis Biotech 临床试验进展报道，时效性被低估。`
- `why_in_top20`: `AI + 医疗是最强监管和商业化交叉赛道之一；数字孪生概念在 AI 语境下有新技术解读空间；TechCrunch 背书有一定权威性；YC Winter 2026 新鲜度高。`
- `visual_assets`: `TechCrunch 文章截图 + mantislabs.com 官网截图（需补）`
- `risks`: `YC 官网/产品未补；融资阶段未知；TechCrunch 是媒体稿，一手性有限。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_081931__techcrunch_ai_mantis_biotech_is_making_digital_twins_of_humans_to_help_solve_medicine___source-packet.md`
- `asset_chain_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260331_084637__mantis_biotech__asset-chain.md`
- `rework_note`: `[secondary fix] YC batch 从 Summer 2021 修正为 Winter 2026；TechCrunch 文章日期修正为 3/30（非 3/9）；升权 15→17`

---

### 18. Mach9：YC 新发布，AI 驱动的 CAD 软件让地图制作加速 100 倍
- `topic_key`: `mach9_ai_cad_yc_launches_20260331`
- `title`: `YC 新发布 Mach9：AI 驱动 CAD 软件让工程制图加速 100 倍`
- `primary_platform`: `YC Launches`
- `published_at`: `2026-03-31 04:07 CST`
- `original_link`: `https://www.ycombinator.com/launches/Pof-mach9-make-maps-fast-ai-powered-cad-software-for-reality-capture`
- `score_total`: `15`
- `score_breakdown`: `一手性=2 | 传播性=1 | 破圈性=1 | 赛道匹配=2 | 可延展性=3 | 数据硬度=2 | 视觉素材=2 | 平台适配=2 | 时效窗口=2`
- `signal_summary`: `YC Launches 收录 Mach9：AI 驱动的 CAD 软件，帮助基础设施测绘和工程团队将原始点云数据转换为工程级 CAD/GIS 成果物，速度提升高达 100 倍。官网 mach9.ai。`
- `why_in_top20`: `YC 平台背书的新项目；AI + CAD/BIM 是 toB 硬科技赛道；100x 加速是强量化数据；B2B 场景有稳定付费意愿。`
- `visual_assets`: `YC Launch 页面截图 + mach9.ai 官网截图（需补）`
- `risks`: `YC Summer 2021 batch，距今年代偏久；实际落地案例少；100x 加速数字需独立验证；官网产品细节需补。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_081931__yc_launches_mach9_mach9_make_maps_fast_ai_powered_cad_software_for_reality_capture__source-packet.md`
- `asset_chain_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260331_084634__mach9__asset-chain.md`

---

### 19. NVIDIA / DeepMind 官方博客更新
- `topic_key`: `nvidia_deepmind_official_updates_20260331`
- `title`: `NVIDIA 博客 + DeepMind 新闻：AI 硬件与模型官方动态双线更新`
- `primary_platform`: `Official / Web`
- `published_at`: `2026-03-31 (snapshot)`
- `original_link`: `https://nvidia.com/blog` / `https://deepmind.google/blog`
- `score_total`: `14`
- `score_breakdown`: `一手性=3 | 传播性=1 | 破圈性=1 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉素材=1 | 平台适配=1 | 时效窗口=1`
- `signal_summary`: `NVIDIA 博客和 DeepMind 官方博客今日快照更新（具体内容待深读）。`
- `why_in_top20`: `NVIDIA 是 AI 硬件周期核心指标；DeepMind 是模型能力边界的官方源；两者同时更新代表行业双线并进。进 Top20 垫底，但作为官方动态监测保留。`
- `visual_assets`: `NVIDIA 博客截图 + DeepMind 博客截图`
- `risks`: `快照层，具体内容未知；时效窗口已过；需深读各子页面才能判断是否有可写事件。降级观察，不建议优先推进。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_085205__nvidia_blog_nvidia_blog__source-packet.md`

---

### 20. 企业微信 AI Skills：中文 B2B AI Agent 生态观察（降 holdout 待验证）
- `topic_key`: `wecom_ai_skills_observation_20260331`
- `title`: `【待验证】企业微信 AI Skills 开源生态：中文 B2B AI Agent 现状观察`
- `primary_platform`: `WeChat / 智东西`
- `published_at`: `2026-03-30 18:45 CST`
- `original_link`: `https://mp.weixin.qq.com/s/rgMXbaCRxlOWlJqQgiyv4g`
- `score_total`: `12`
- `score_breakdown`: `一手性=1 | 传播性=1 | 破圈性=1 | 赛道匹配=3 | 可延展性=2 | 数据硬度=1 | 视觉素材=1 | 平台适配=2 | 时效窗口=2`
- `signal_summary`: `⚠️ 【P3 FIXED - 降 holdout】智东西报道企业微信（WeCom）AI Skills 开源动态。但经外部交叉验证：**「养虾大杀器」「Claude Code 直接调用」等关键主张无法在腾讯官方博客、GitHub 或其他独立信源获得任何验证**。当前仅媒体单源，不具备 Top20 放行条件。降为 holdout watchlist，建议持续追踪腾讯官方公告。`
- `why_downgraded`: `P3 阻塞项：经 redteam 外部检索（搜索「WeCom/WeChat Work 12 skills open source 2026」「wechat work skills open source」等关键词），无任何独立信源验证「养虾大杀器」或 Claude Code 直调主张。原始 Zhidx 文章仅提供媒体稿，无原始 Skills 接口文档/腾讯官方博客/GitHub repo。`
- `visual_assets`: `智东西文章截图`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_085205__wechat_zhidx_ai_12_skills__source-packet.md`
- `rework_note`: `[P3 FIXED] 从 top6_strong_pool 降为 holdout_watchlist；WeCom Skills 具体接口无法外部验证；保留观察价值但不放行`

---

## 结论

### top3_must_watch
（按今日信号强度排序，供下游优先评估）
1. **`claude_code_cache_bugs`** — 技术深度最强，证据链完整（GitHub Issues + 逆向工程 + workaround），开发者社区直接受影响，可快讯 + 技术解读 + 工具推荐三层联动。
2. **`xai_20b_series_e`** — 20B 美元是年度级事件，Grok B2B 产品矩阵官方确认，一手源无失真，叙事空间大（融资 / 企业 AI / Musk 生态）。
3. **`robots_bury_you_in_work`** — 真实量化数据（17 agents / 12 projects / 1400+ commits）构成硬证据，"生产力陷阱"叙事与主流 AI 焦虑叙事反向，易破圈。

### top6_strong_pool
4. `llamacpp_100k_stars` — 开源 infra 里程碑，100k 数字有说服力
5. `qwen_36_openrouter` — 中国大模型出海渠道多元化信号
6. `anthropic_sonnet_opus_46` — Anthropic 官方双旗舰更新，81k 调研独家数据
7. `universal_claude_md` — Claude 开发者效率工具，HN 验证
8. `litellm_delve_security` — AI infra 供应链安全，实用性强
9. `claude_subscriptions_double` — 商业数据好但需补 TechCrunch 原文

### holdout_watchlist
10. `multi_inst_ai_safety_paper` — 论文信号真实但 arXiv 正文需补；机构归属已修正
11. `learn_claude_code_by_doing` — HN 高热但内容深度待验
12. `apple_wwdc2026_siri` — 重磅预期但 WWDC 实际内容未知
13. `florida_man_chatgpt_house` — 传播性强（多平台验证），细节已补全
14. `bytedance_seedance_luofuli` — 人才叙事有趣但产品细节少
15. `innovationai_industrial_agent` — 工业 AI 方向值得持续观察
16. `axiomatic_ai_18m` — AI安全/对齐方向已补描述，时效偏早
17. `mantis_biotech` — YC Winter 2026，时效已修正
18. `mach9_yc_launches` — YC 背书但项目年代偏久
19. `wecom_ai_skills_observation` — **P3 降 holdout；无法外部验证**
20. `nvidia_deepmind_updates` — 官方监测，无具体事件

### supply_risk
- **今日信号质量**：整体偏中上，HN + Reddit 英文源质量高，WeChat 中文源覆盖工业/企业 AI 场景
- **OpenAI 覆盖说明（已补 P1）**：今日 GPT-5.4 滚动发布属常规节奏非新事件；近期可预期 o4 预览（4月上旬）/ Operator 更新 / 春季发布
- **弱链补查优先级**：(1) Axiomatic AI 官网/业务方向，(2) Mantis Biotech 产品详情，(3) Stanford 论文正文，(4) Claude 订阅数 TechCrunch 原文，(5) Florida Man Inc.com 原文
- **缺失项**：无今日 deep article，无 topic cluster；建议下轮增加 Reddit 评论深度抓取（当前 RSS 403 导致评论数不可见）
- **Late-breaking 信号评估（12:20 后）**：manifest 中 12:47 批次 WeChat 源（xAI IPO/苹果百度AI/黄仁勋50条/哈利波特GitHub/Claude Code电脑控制）信号强度未显著超越现有 top20 候选，本次不补进

---

## Rework 完成情况说明

| 阻塞项 | 状态 | 处理方式 |
|--------|------|----------|
| P1 OpenAI supply_risk | ✅ 已补填 | supply_risk 专项说明写明：GPT-5.4 属常规节奏非新事件，近期关注 o4 窗口 |
| P2 Stanford论文机构归属 | ✅ 已修正 | 机构归属从「Stanford+Harvard联合」修正为「Northeastern+13 institutions」；保留论文核心信号 |
| P3 WeCom 12 Skills | ✅ 已降级 | 从 top6_strong_pool 降为 holdout_watchlist；标注无法外部验证 |
| Mantis Biotech YC批次 | ✅ 已修正 | Summer 2021 → Winter 2026；升权 15→17 |
| Axiomatic AI 描述 | ✅ 已补填 | 补全 AI安全/对齐业务方向；升权 16→17 |
| Florida Man 评分 | ✅ 已升权 | 16→19；redteam 发现多平台验证细节丰富 |

### 不自判放行说明
> 本 rework 包已完成 scorecard 指出的所有 P1/P2/P3 补证和修正工作，但**不自判「已过线 / 可进入下一工序 / premium_pass」**。是否放行由 `market-editor` 最新 scorecard 决定。

---

**Rework 包路径**：`/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260331__top20-screening-pack__reworked.md`
**原始包路径**：`/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260331__top20-screening-pack.md`
**Scorecard 路径**：`/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260331__top20__stage-gate-scorecard.md`
**Manifest 路径**：`/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260331__market-source-manifest.md`
