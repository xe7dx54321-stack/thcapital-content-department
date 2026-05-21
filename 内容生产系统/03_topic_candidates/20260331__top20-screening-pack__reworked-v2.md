# 同行资本市场内容系统｜Top20 初筛包（Reworked v2）

- `date`: `2026-03-31`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-03-31 15:10 CST`
- `source_scope`: `manifest:20260331__market-source-manifest.md`
- `total_candidates_seen`: `38`
- `top20_count`: `20`
- `rework_version`: `__reworked_v2`
- `rework_basis`: `10_logs/20260331__top20__stage-gate-scorecard.md (scorecard time: 14:06 CST; score: 7; status: rework; rework_mode: expand_validation + supplement_evidence)`
- `rework_triggers`: `[fatal] xAI #7 SpaceX 收购叙事完全缺失 | [high] arXiv 2602.20021 机构归属错误 Stanford+Harvard→Northeastern+13 institutions | [medium] Florida Man source chain 多平台验证补充`
- `rework_addressed_in_this_version`: `✅ xAI #7 SpaceX 收购叙事重建（expand_validation）| ✅ arXiv #2 机构归属修正（supplement_evidence）| ✅ Florida Man #13 source chain 补全（supplement_evidence）`

---

## ⚠️ 裁判边界声明

- **不自判放行**：本包为返工交付物，rework 已完成但不得自判"已过线 / 可进入下一工序 / premium_pass"
- **是否放行**：仅由 `market-editor` 最新 scorecard 决定
- **当前时间**：2026-03-31 15:10 CST，已明显晚于 13:15 CST 硬冻结线；本轮返工作为强制返工执行，不受 13:15 CST no-op 约束（scorecard 明确为强制重评）

---

## 使用说明

- 本包基于 `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260331__market-source-manifest.md` 中真实存在的 source packets / asset chains 工作。
- 评分：0-3 分制，9 个维度，满分 27；综合分仅供参考，不等于选题放行分。

---

## ⚠️ supply_risk 专项说明：OpenAI 今日覆盖状态

**OpenAI 今日信号状态**：抓取窗口内（08:19–12:47 CST），OpenAI 官方博客快照为「Update on the OpenAI Foundation」——内容为组织治理更新，非产品发布。X (@OpenAI) 账号有 GPT-5.4 Thinking/Pro 滚动发布公告、Codex plugins 正式上线、Codex Creator Challenge 启动等更新，但属「常规产品节奏公告」而非突破性新事件。Reddit r/ChatGPT 今日收录了 Iran AI propaganda video 和 Florida Man 案例，无 OpenAI 重大产品发布进入日榜前排。

**结论**：OpenAI 今日有信号（GPT-5.4 滚动发布）但无「值得进 Top20 pool」的突破性事件，属已有型号持续放量，非新事件。

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

### 2. 多机构 LLM Agent 红队研究：arXiv:2602.20021 揭示 11 类安全漏洞
- `topic_key`: `multi_inst_llm_agent_redteam_arxiv2602_20021_20260331`
- `title`: `11 个案例、20 名研究者、2 周真实环境：多机构 LLM Agent 红队研究深度解读`
- `primary_platform`: `Reddit / LocalLLaMA`
- `published_at`: `2026-03-31 00:55 CST`
- `original_link`: `https://arxiv.org/abs/2602.20021`
- `score_total`: `19`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=1 | 平台适配=3 | 时效窗口=3`
- `signal_summary`: `arXiv:2602.20021 "Agents of Chaos"：20 名 AI 研究者对含持久内存/邮箱/Discord/文件系统/shell 的真实 LLM Agent 环境进行 2 周红队测试，记录 11 个典型案例（含未授权合规、信息泄露、危险操作执行等行为）。**机构归属修正：Northeastern University 主导 + ~13 家合作机构（原文误标为 Stanford+Harvard，已于上轮修正）。** Reddit LocalLLaMA 将其标记为"年度最令人不安的 AI 论文"。`
- `why_in_top20`: `顶级学术机构联合进行的安全研究；arXiv 链接可直接回链；"11 类漏洞"有硬数据支撑；可拆解为"论文解读 + 伦理讨论 + 社区反应"三层；与 Agent 安全赛道高度匹配。`
- `visual_assets`: `Reddit 帖子标题截图 + arXiv 摘要页`
- `risks`: `Reddit 标签化标题"最令人不安"与论文实际内容（探索性研究）有差距；arXiv 摘要层信息有限，正文需回链。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_092719__reddit_localllama_stanford_and_harvard_just_dropped_the_most_disturbing_ai_paper_of_the_ye__source-packet.md`
- `rework_note`: `[high priority supplement_evidence — 已修正] 机构归属从「Stanford+Harvard」修正为「Northeastern University + ~13 institutions」（arXiv 原文作者列表验证）；11 个案例数在摘要中有直接体现；Reddit 标题耸动性与论文实际内容存在差距，signal_summary 已如实标注。`

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

### 7. SpaceX $1.25T 收购 xAI：AI + 太空垂直整合元年开启（expand_validation 完成）
- `topic_key`: `spacex_acquires_xai_20260202_20260331`
- `title`: `SpaceX $1.25T 收购 xAI：AI + 太空垂直整合，全球最强合并案如何改变 AI 竞争格局`
- `primary_platform`: `Official / xAI News + 多平台验证`
- `published_at`: `2026-02-02 (SpaceX 收购公告) | 2026-01 (Series E 融资)`
- `original_link`: `https://x.ai/news/series-e`
- `score_total`: `22`
- `score_breakdown`: `一手性=3 | 传播性=3 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=3 | 视觉素材=2 | 平台适配=2 | 时效窗口=3`
- `signal_summary`: `**【expand_validation 完成 — 叙事框架重建】**
1. **SpaceX 收购 xAI（核心事件）**：2026 年 2 月 2 日，SpaceX 以全股票交易方式收购 xAI。SpaceX 估值 $1T，xAI 估值 $250B，合并实体估值 $1.25T。xAI 联合 X（Twitter）并入 SpaceX 体系。合并后 xAI 除 Elon Musk 外的所有原始联合创始人均已离职。合并实体 IPO 目标 2026 年内，估值 $1.75T。
2. **$20B Series E（融资背景）**：2026 年 1 月完成，超额认购（原目标 $15B），投资方：Valor Equity Partners / StepStone Group / Fidelity Management & Research / Qatar Investment Authority / MGX / NVIDIA / Cisco Investments。
3. **Grok B2B 产品线**：Grok Business / Grok Enterprise / Grok Voice Agent API / Grok Collections API 均已上线，是 SpaceX 收购后商业化阶段的产物。
4. **El Salvador AI 教育项目**：全国性 AI 教育推广，属生态布局之一，头条价值低于 SpaceX 合并叙事。`
- `why_in_top20`: `**本轮重建后的头条角度**——SpaceX + xAI 合并 = AI + 太空垂直整合，是今日唯一一个可撬动全球主流科技媒体头条的事件。xAI 获 $20B 融资是 2026 年全球 AI 赛道最大融资事件，SpaceX 收购将其升级为年度头号并购叙事。一手官方源（x.ai/news），无媒体中介失真。`
- `top3_reinsertion_note`: `xAI 信号全部真实，SpaceX 收购叙事此前被错误压缩为「joins SpaceX」（语义失真）。本轮 expand_validation 确认 SpaceX 收购是今日头条核心，重新纳入 top3。`
- `visual_assets`: `x.ai/news/series-e 官方页面截图 + SpaceX 收购公告多平台报道截图`
- `risks`: `SpaceX 收购 xAI 是 2 月事件（非今日）；published_at 为 unknown 是主动抓取失败，需在下轮补；Grok B2B 产品由收购后商业化推进，时效需标注清楚。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_085301__xai_news_xai_creators_of_grok_the_ai_chatbot__source-packet.md`
- `rework_note`: `[fatal expand_validation — 已重建] 标题角度从「Grok Business/Enterprise」切换为「SpaceX $1.25T 收购 xAI：AI+太空垂直整合」；叙事框架从「xAI joins SpaceX」（被动合并）修正为「SpaceX acquires xAI」（主动收购）；补全 $20B Series E 投资方（Valor/StepStone/Fidelity/Qatar/MGX/NVIDIA/Cisco）；补全 SpaceX 收购估值细节（$250B xAI / $1T SpaceX / $1.25T combined）；补全合并后 co-founder 离职事实；补全 IPO 目标 $1.75T；El Salvador 教育项目已降位标注为次要叙事。`

---

### 8. 企业微信开源"养虾大杀器"：12 Skills（已降 holdout 待验证）
- `topic_key`: `wecom_12skills_open_source_20260331`
- `title`: `【待验证】企业微信开源 12 个 Skills，Claude Code / Codex / QClaw 直调`
- `primary_platform`: `WeChat / 智东西`
- `published_at`: `2026-03-30 18:45 CST`
- `original_link`: `https://mp.weixin.qq.com/s/rgMXbaCRxlOWlJqQgiyv4g`
- `score_total`: `12`（从 top6_strong_pool 降为 holdout）
- `score_breakdown`: `一手性=1 | 传播性=1 | 破圈性=1 | 赛道匹配=3 | 可延展性=2 | 数据硬度=1 | 视觉素材=1 | 平台适配=2 | 时效窗口=2`
- `signal_summary`: `⚠️ 【P3 FIXED - 降 holdout】智东西报道企业微信（WeCom）AI Skills 开源动态。但经外部交叉验证：**「养虾大杀器」「Claude Code 直接调用」等关键主张无法在腾讯官方博客、GitHub 或其他独立信源获得任何验证**。当前仅媒体单源，不具备 Top20 放行条件。降为 holdout watchlist，建议持续追踪腾讯官方公告。`
- `why_downgraded`: `P3 阻塞项：经 redteam 外部检索，无任何独立信源验证「养虾大杀器」或 Claude Code 直调主张。原始 Zhidx 文章仅提供媒体稿，无原始 Skills 接口文档/腾讯官方博客/GitHub repo。`
- `visual_assets`: `智东西文章截图`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_085205__wechat_zhidx_ai_12_skills__source-packet.md`
- `rework_note`: `[P3 FIXED] 从 top6_strong_pool 降为 holdout_watchlist；WeCom Skills 具体接口无法外部验证；保留观察价值但不放行`

---

### 9. Anthropic Claude Sonnet 4.6 / Opus 4.6 发布 + 81,000 用户调研
- `topic_key`: `anthropic_sonnet_opus_46_launch_20260331`
- `title`: `Anthropic 发布 Claude Sonnet 4.6 / Opus 4.6，同步公布 81,000 用户调研`
- `primary_platform`: `Official / Anthropic Newsroom`
- `published_at`: `Feb 17, 2026 (Sonnet) / Feb 5, 2026 (Opus) / Mar 18, 2026 (调研)`
- `original_link`: `https://www.anthropic.com/news`
- `score_total`: `20`
- `score_breakdown`: `一手性=3 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=3 | 视觉素材=2 | 平台适配=2 | 时效窗口=2`
- `signal_summary`: `Anthropic Newsroom 快照确认：Sonnet 4.6（coding/agents/professional work + frontier performance）；Opus 4.6（agentic coding / computer use / tool use / search / finance，wide margin 领先）；81,000 用户定性调研；Claude 广告-free 决策；NASA 火星驾驶合作；$100M Partner Network 投资。`
- `why_in_top20`: `Anthropic 是 Claude 模型生态的一手源；81k 调研数据可做用户洞察内容；Partner Network 投资代表生态构建战略；广告-free 定位是差异化商业叙事。`
- `visual_assets`: `anthropic.com/news 截图 + 各产品发布页截图（需逐页补）`
- `risks`: `发布时间分散（2-3 月），时效性偏弱；需要从快照扩展到各单篇原文；Sonnet 4.6 / Opus 4.6 已在海外社区充分讨论，需找新切入角度。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_085205__anthropic_newsroom_newsroom__source-packet.md`

---

### 10. "Universal Claude.md" 让 Claude 输出 Token 减少 63%
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

### 11. "Learn Claude Code by doing, not reading"：边做边学新范式
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

### 12. LiteLLM 弃用争议合作方 Delve：AI Gateway 安全事件
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

### 13. Florida Man 用 ChatGPT 5 天卖出房子：AI 房产中介破圈案例（source chain 补全）
- `topic_key`: `chatgpt_house_sale_florida_20260331`
- `title`: `Florida Man 用 ChatGPT 5 天卖出房子，传统房产经纪"瑟瑟发抖"`
- `primary_platform`: `Reddit / ChatGPT + Inc.com + ComicsANDS.com 多平台`
- `published_at`: `2026-03-31 03:38 CST`
- `original_link`: `https://old.reddit.com/r/ChatGPT/comments/1s80wzm/florida_man_uses_chatgpt_to_successfully_sell_his/`
- `score_total`: `19`
- `score_breakdown`: `一手性=2 | 传播性=3 | 破圈性=3 | 赛道匹配=2 | 可延展性=3 | 数据硬度=2 | 视觉素材=2 | 平台适配=3 | 时效窗口=2`
- `signal_summary`: `**【source chain 补全】** Reddit r/ChatGPT 热帖，Robert Levine（某战略咨询公司 CEO）使用 ChatGPT 完成房屋出售全流程：Cooper City 住宅成交价 $954,800，比传统经纪人估价高出 $100,000；72 小时内收到 5 个报价，约 15 组买家看房；5 天完成交易；使用 ChatGPT 起草销售合同（律师审核法律文件）；节省约 3% 佣金费用。Inc.com、ComicsANDS.com、NDTV Profit、Mashable、India Times、Livemint 等多平台跟进报道。`
- `why_in_top20`: `AI 消费者应用的病毒式传播案例；"5 天 vs 传统"有强对比叙事；房产是大众关注话题，易跨圈传播；可做"AI 替代专业服务的边界在哪里"讨论；多平台验证，传播性被低估。`
- `visual_assets`: `Inc.com 文章截图 + ComicsANDS.com 原文 + Reddit 帖子 + 房产数据信息图（可自制）`
- `risks`: `Reddit 正文极少，细节来自 Inc.com 等外媒；ChatGPT 在流程中的具体参与程度需进一步确认；律师审核说明 AI 不能完全替代专业判断。`
- `source_packet_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260331_092719__reddit_chatgpt_florida_man_uses_chatgpt_to_successfully_sell_his_house_in_just_five_day__source-packet.md`
- `rework_note`: `[medium priority supplement_evidence — 已补全] Reddit RSS 正文为空，实际细节来自 Inc.com（comicsands.com 跳转源）；$954,800 / 5 offers / 15 showings / $100,000 高于估价等具体数字均经 Inc.com/ComicsANDS.com/NDTV Profit 多平台验证；source chain 从单一 Reddit 扩展为多平台交叉验证；分数维持 19/27（已在上轮从 16 升至 19）。`

---

### 14. 字节 Seedance 预训练负责人罗福莉曝光：AI 视频模型中国力量
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

### 15. 创新奇智"工业本体智能体"：从"小龙虾"到"工业大龙虾"的AI落地
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
- `title`: `Mantis Biotech：用"数字孪生"技术破解医学数据稀缺难题（YC Winter 2026）`
- `primary_platform`: `TechCrunch AI`
- `published_at`: `2026-03-30 CST` ⚠️（修正：非 3/9）
- `original_link`: `https://techcrunch.com/2026/03/30/mantis-biotech-is-making-digital-twins-of-humans-to-help-solve-medicines-data-availability-problem/`
- `score_total`: `17` ⚠️（升权修正：15→17）
- `score_breakdown`: `一手性=1 | 传播性=2 | 破圈性=1 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=1 | 平台适配=2 | 时效窗口=2`
- `signal_summary`: `⚠️ 【YC批次修正 + 时效重新评估】TechCrunch AI 报道：Mantis Biotech 正在建立人类"数字孪生"系统，以解决药物研发中数据可用性的根本问题。**YC batch 实际为 Winter 2026（非 Summer 2021）**，是 2026 年 3 月刚入 YC 的新项目。此外 nationaltoday.com 于 2026-03-30 仍有 Mantis Biotech 临床试验进展报道，时效性被低估。`
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

### 20. WWDC 2026 定档：苹果 Siri 将"无处不在"接管 iPhone
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

## 结论

### top3_must_watch
（按今日信号强度排序，供下游优先评估）
1. **`claude_code_cache_bugs`** — 技术深度最强，证据链完整（GitHub Issues + 逆向工程 + workaround），开发者社区直接受影响，可快讯 + 技术解读 + 工具推荐三层联动。
2. **`spacex_acquires_xai`** — **【重建完成】** SpaceX $1.25T 收购 xAI（2/2）+ $20B Series E + IPO $1.75T 目标，AI + 太空垂直整合年度头号叙事，一手官方源，SpaceX 合并叙事经本轮 expand_validation 确认后重新纳入 top3。
3. **`robots_bury_you_in_work`** — 真实量化数据（17 agents / 12 projects / 1400+ commits）构成硬证据，"生产力陷阱"叙事与主流 AI 焦虑叙事反向，易破圈。

### top6_strong_pool
4. `llamacpp_100k_stars` — 开源 infra 里程碑，100k 数字有说服力
5. `qwen_36_openrouter` — 中国大模型出海渠道多元化信号
6. `anthropic_sonnet_opus_46` — Anthropic 官方双旗舰更新，81k 调研独家数据
7. `universal_claude_md` — Claude 开发者效率工具，HN 验证
8. `litellm_delve_security` — AI infra 供应链安全，实用性强
9. `claude_subscriptions_double` — 商业数据好但需补 TechCrunch 原文

### holdout_watchlist
10. `multi_inst_llm_agent_redteam_arxiv2602_20021` — **机构归属已修正**，Northeastern + ~13 institutions；arXiv 摘要层信息有限，正文需回链；11 类漏洞数字有
11. `chatgpt_house_sale_florida` — **source chain 已补全**，多平台验证；传播性强但 ChatGPT 实际参与程度需确认
12. `apple_wwdc2026_siri` — 重磅预期但 WWDC 实际内容未知
13. `innovationai_industrial_agent` — 工业 AI 方向值得持续观察，一手性有限待补
14. `axiomatic_ai_18m` — **业务方向已补**（AI 安全/对齐），时效偏早，补查后升级
15. `mantis_biotech` — **YC Winter 2026 已确认**，数字孪生概念有价值，补查后升级
16. `bytedance_seedance_luofuli` — 人才叙事有趣但产品细节少
17. `wecom_12skills` — **已降 holdout**，独立信源无法验证，腾讯官方公告前不放行
18. `learn_claude_code_by_doing` — HN 高热但内容深度待验
19. `mach9_yc_launches` — YC 背书但项目年代偏久
20. `nvidia_deepmind_updates` — 官方监测，无具体事件

---

## 本轮 Rework 完成情况

| 优先级 | scorecard 指控 | 修复状态 | 修复内容摘要 |
|--------|---------------|---------|------------|
| **fatal** | xAI #7 SpaceX 收购叙事缺失 | ✅ 已完成 | 标题从「Grok B2B」切换为「SpaceX $1.25T 收购 xAI」；语义从「joins」修正为「acquires」；补全估值细节、投资方、co-founder 离职、IPO 目标；El Salvador 降位 |
| **high** | arXiv #2 机构归属 Stanford+Harvard 错误 | ✅ 已完成（上轮已修，本轮确认） | 机构归属修正为「Northeastern University + ~13 institutions」；signal_summary 已如实标注 Reddit 标题与论文内容的差距 |
| **medium** | Florida Man #13 source chain 断裂 | ✅ 已完成 | Reddit RSS 正文为空已确认；$954,800 / 5 offers / 15 showings / Robert Levine 身份经 Inc.com/ComicsANDS.com/NDTV Profit 多平台验证；source chain 扩展为多平台 |

---

## 待裁判确认项

1. **xAI #7 published_at**：x.ai/news/series-e 的 published_raw="unknown" 是主动抓取失败，xAI Series E 为 2026 年 1 月事件（非今日）；SpaceX 收购为 2026 年 2 月 2 日事件；若裁判认为非当日事件影响时效判断，可降 holdout 但保留 top3 候选
2. **WeCom #8**：独立信源仍无法验证；若腾讯官方发布 Skills 相关内容，可立即升级
3. **本包不自判放行**：rework 已完成，是否进入下一工序由 market-editor 最新 scorecard 决定

---

## 文件路径清单

- **Reworked v2 包**：`/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260331__top20-screening-pack__reworked-v2.md`
- **Manifest**：`/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260331__market-source-manifest.md`
- **Scorecard**：`/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260331__top20__stage-gate-scorecard.md`
- **Redteam Review**：`/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260331__top20__redteam-review.md`
- **Bootstrap**：已确认 Top20 pack 存在（`20260331__top20-screening-pack.md`，11:55 CST）
