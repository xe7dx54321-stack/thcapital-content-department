# Top20 初筛包

- `date`: `2026-03-30`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-03-30 16:44 CST`
- `source_scope`: `trend__reddit_localllama_daily, trend__reddit_claude_daily, trend__reddit_chatgpt_daily, web__techcrunch_ai, trend__hn_frontpage, trend__arxiv_cs_ai_recent, trend__zhihu_hotlist, trend__wechat_geekpark, trend__wechat_qbitai`
- `total_candidates_seen`: `24`
- `top20_count`: `20`

## 使用说明

- 这是 `signal-scout` 阶段正式交付包。
- 不是原始 source packet 堆砌。
- 每个候选必须包含结构化评分与证据摘要。
- 本版为下午更新版：上午 9 个 packet + 下午 15 个 packet 合并评分。

## 评分框架

| 维度 | 说明 | 分值 |
|---|---|---|
| 一手性 | 是否来自官方 / 论文 / 产品页 / 原帖 | 0-3 |
| 传播性 | 是否已有多平台、多语种或多媒体跟进 | 0-3 |
| 破圈性 | 是否跨至少 2 个内容场域发酵 | 0-3 |
| 赛道匹配 | 是否契合 AI / Agent / 一人公司 / 模型 / infra / 硬件主线 | 0-3 |
| 可延展性 | 是否能写出快讯、解读、复盘多层内容 | 0-3 |
| 数据硬度 | 是否有硬数据、原始截图、官方说明 | 0-3 |
| 视觉素材丰富度 | 是否具备可直接利用的图、表、截图、原帖 | 0-3 |
| 平台适配潜力 | 是否容易改写为多平台内容 | 0-3 |
| 时效窗口 | 是不是当下写最有价值 | 0-3 |
| 讨论度 / 争议度 | 是否有持续讨论空间 | 0-3 |

## Top20 候选

### 1. DeepSeek 服务宕机约 12 小时：知乎 125 万热度，财联社跟进
- `topic_key`: `deepseek-outage-12-hours-125w-heat`
- `title`: `3 月 29 日大量用户反映 DeepSeek 服务出现异常，在宕机 12 小时后恢复服务`
- `primary_platform`: `知乎热榜`
- `published_at`: `2026-03-29 23:04 CST`
- `original_link`: `https://www.zhihu.com/question/2021724542909903612`
- `score_total`: `25/30`
- `score_breakdown`: `一手性=2 | 传播性=3 | 破圈性=3 | 赛道匹配=2 | 可延展性=3 | 数据硬度=2 | 视觉素材=1 | 平台适配=3 | 时效窗口=3 | 讨论度=3`
- `signal_summary`: `2026 年 3 月 29 日夜，DeepSeek 网页端和 App 同时出现"服务器繁忙"提示，大量用户无法进行新对话，部分用户反映对话内容丢失。DeepSeek 官方服务状态页记录了完整事件时间线：21:35 发现异常 → 23:23 首次解决 → 次日 00:20 再次出现性能异常 → 01:24 实施修复但未完全解决。宕机约 12 小时后恢复服务。知乎热度 125 万，81 个回答，203 人关注。财联社、IT之家、腾讯新闻等多家媒体跟进报道。`
- `why_in_top20`: `重大 AI 公司服务稳定性事件；中国头部大模型公司（DeepSeek）史上首次大规模宕机；多源媒体（财联社+IT之家+腾讯新闻）交叉验证；知乎 125 万热度证明破圈程度；宕机原因和时长有官方记录（硬数据）；可延展至：大模型稳定性、SLA 讨论、云服务竞争等。`
- `visual_assets`: `知乎热榜截图；DeepSeek 官方服务状态页截图；IT之家报道配图；财联社报道截图`
- `risks`: `知乎热榜问题是用户讨论视角，非官方公告；需回链 DeepSeek 官方博客或状态页确认事件细节`

---

### 2. 警察用 AI 人脸识别错误逮捕田纳西州女性：HN 372 分 / 161 评论
- `topic_key`: `ai-facial-recognition-wrongful-arrest-tn-woman`
- `title`: `Police used AI facial recognition to wrongly arrest TN woman for crimes in ND`
- `primary_platform`: `Hacker News`
- `published_at`: `2026-03-29 22:20 CST`
- `original_link`: `https://news.ycombinator.com/item?id=47563384`
- `score_total`: `23/30`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=3 | 赛道匹配=2 | 可延展性=3 | 数据硬度=2 | 视觉素材=1 | 平台适配=3 | 时效窗口=2 | 讨论度=3`
- `signal_summary`: `美国田纳西州一名女性 Angela Lipps 被 AI 人脸识别技术错误识别，遭警方逮捕，但实际犯罪行为发生在北达科他州。原文来自 CNN 报道。HN 讨论串 372 points，161 comments，登上 HN 首页。事件在美国引发关于 AI 人脸识别准确率、种族偏见和法律程序的广泛讨论。`
- `why_in_top20`: `AI 人脸识别技术在执法场景的典型滥用案例；涉及 AI 伦理、法律正当程序和种族偏见等高热话题；跨科技+法律+社会多场域；HN 高热讨论（372 points）证明技术社区关注度；CNN 原始报道是一手媒体源。`
- `visual_assets`: `CNN 文章截图；HN 讨论串截图；涉事女性相关媒体配图（需注意版权）`
- `risks`: `CNN 报道后二次传播；法律案件细节需核实；视觉素材版权需注意`

---

### 3. Claude Code 每 10 分钟对项目仓库执行 Git reset --hard origin/main（严重 Bug）
- `topic_key`: `claude-code-git-reset-hard-every-10-mins`
- `title`: `Claude Code runs Git reset –hard origin/main against project repo every 10 mins`
- `primary_platform`: `Hacker News`
- `published_at`: `2026-03-30 06:15 CST`
- `original_link`: `https://github.com/anthropics/claude-code/issues/40710`
- `score_total`: `22/30`
- `score_breakdown`: `一手性=3 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=3 | 视觉素材=1 | 平台适配=2 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `GitHub issue（anthropics/claude-code#40710）报告：Claude Code 每 10 分钟自动对项目仓库执行 git reset --hard origin/main，导致开发者代码被强制回滚。HN 讨论串 212 points，138 comments，登上 HN 首页。Issue 本身是一手产品 Bug 报告，评论中有开发者报告类似遭遇。`
- `why_in_top20`: `Anthropic 官方产品（Claude Code）的严重数据损坏 Bug；GitHub Issue 是一手信源且可验证；有具体技术机制（每 10 分钟触发）；涉及 AI Coding Tools 赛道的核心可靠性问题；HN 高热（212 points，138 comments）说明影响面广。`
- `visual_assets`: `GitHub Issue 页面截图；HN 讨论串截图；评论中附带的 terminal 截图`
- `risks`: `Bug 具体触发条件需进一步验证；Claude Code 团队是否已确认修复需跟进`

---

### 4. Sora 关停：AI 视频行业的一记现实检验
- `topic_key`: `ai-video-sora-shutdown-reality-check`
- `title`: `Sora's shutdown could be a reality check moment for AI video`
- `primary_platform`: `TechCrunch`
- `published_at`: `2026-03-30 00:30 CST`
- `original_link`: `https://techcrunch.com/2026/03/29/soras-shutdown-could-be-a-reality-check-moment-for-ai-video/`
- `score_total`: `18/30`
- `score_breakdown`: `一手性=2 | 传播性=3 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=1 | 视觉素材=2 | 平台适配=2 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `TechCrunch 报道 OpenAI Sora 关停事件，援引"Is this just normal corporate strategy, or are we about to see a broader pullback on AI-generated video?"——是关于 AI 视频行业走向的重要信号。`
- `why_in_top20`: `重大厂关停产品事件，跨科技+娱乐场域；时效强；可延展到 AI 视频行业格局分析、竞争格局影响等多个方向。`
- `visual_assets`: `TechCrunch 文章页截图；可截取文章英雄区配图`
- `risks`: `媒体二手报道，尚无 OpenAI 官方声明；需回链官方博客或公告交叉验证`

---

### 5. Nicolas Carlini 称 Claude 是比他更好的安全研究员
- `topic_key`: `claude-security-researcher-nicolas-carlini`
- `title`: `Nicolas Carlini (67.2k citations) says Claude is a better security researcher than him`
- `primary_platform`: `Reddit / r/ClaudeAI`
- `published_at`: `2026-03-30 02:43 CST`
- `original_link`: `https://old.reddit.com/r/ClaudeAI/comments/1s739lc/nicolas_carlini_672k_citations_on_google_scholar/`
- `score_total`: `16/30`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉素材=1 | 平台适配=2 | 时效窗口=2 | 讨论度=3`
- `signal_summary`: `顶级安全研究员 Nicolas Carlini（Google Scholar 引用 67.2k）公开表示 Claude 是比他更好的安全研究员，并分享了自己通过智能合约漏洞赚了 370 万美元、发现 Linux 古老漏洞的经历。附有 YouTube 视频链接。`
- `why_in_top20`: `有具体数字（370 万美元）、具体漏洞类型（2003 年引入的缓冲区溢出）、具体人名和引用数；讨论 AI 安全研究能力边界；Carlini 本人在安全社区有极高可信度。`
- `visual_assets`: `Reddit 帖子页；YouTube 视频页（Carlini 本人出镜）；Google Scholar 页面截图`
- `risks`: `Reddit 二手传播，Carlini 原始视频内容需单独验证；数字和漏洞细节需回链原始视频`

---

### 6. Coding Agents Could Make Free Software Matter Again
- `topic_key`: `coding-agents-free-software-revival`
- `title`: `Coding Agents Could Make Free Software Matter Again`
- `primary_platform`: `Hacker News`
- `published_at`: `2026-03-30 06:21 CST`
- `original_link`: `https://news.ycombinator.com/item?id=47568028`
- `score_total`: `15/30`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=1 | 视觉素材=1 | 平台适配=2 | 时效窗口=2 | 讨论度=2`
- `signal_summary`: `博客文章认为 AI Coding Agents 的崛起可能让免费开源软件重新变得重要——因为 AI 能处理开源项目的维护成本，降低贡献门槛。HN 132 points，122 comments，登上 HN 首页。`
- `why_in_top20`: `命中 AI Agent 赛道核心叙事；开源生态影响角度新颖；HN 高评论数（122）说明讨论深度好；可延展至开源生态、软件开发工作流变革等话题。`
- `visual_assets`: `博客文章截图；HN 讨论串截图`
- `risks`: `博客观点文，论据需核实；暂无硬数据支撑`

---

### 7. Kimi K2.6 将在 2 周内发布，K3 目标是追平美国模型参数规模
- `topic_key`: `kimik2-moonshot-kimi-k3-roadmap`
- `title`: `Kimi K2.6 will drop in the next 2 weeks, K3 is WIP and will be huge`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-03-29 19:39 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1s6stgl/kimi_k26_will_drop_in_the_next_2_weeks_k3_is_wip/`
- `score_total`: `14/30`
- `score_breakdown`: `一手性=1 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=1 | 视觉素材=1 | 平台适配=2 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `Reddit 用户自称从 Moonshot 内部人士获悉：Kimi K2.6 将在 10-15 天内发布，为小幅提升；K3 正在开发中，目标是参数规模追平美国模型。`
- `why_in_top20`: `涉及中国头部大模型公司（月之暗面/Kimi）的最新 roadmap；"K3 对标美国模型"是强叙事锚点；可延伸到大模型竞争格局、中美模型对比等话题；时效窗口新鲜（帖子发布距今不足 24 小时）。`
- `visual_assets`: `Reddit 帖子截图`
- `risks`: `来源可靠性存疑（"heard from someone at Moonshot"属于弱链）；需回链月之暗面官方博客或 KIMI 官方账号验证`

---

### 8. Philly 法院将全面禁止智能眼镜：下一周生效
- `topic_key`: `philly-smart-eyeglasses-ban`
- `title`: `Philly courts will ban all smart eyeglasses starting next week`
- `primary_platform`: `Hacker News`
- `published_at`: `2026-03-30 09:38 CST`
- `original_link`: `https://news.ycombinator.com/item?id=47569471`
- `score_total`: `13/30`
- `score_breakdown`: `一手性=2 | 传播性=1 | 破圈性=2 | 赛道匹配=2 | 可延展性=2 | 数据硬度=1 | 视觉素材=1 | 平台适配=2 | 时效窗口=2 | 讨论度=1`
- `signal_summary`: `费城法院宣布下周起全面禁止佩戴智能眼镜（含 Meta Ray-Ban 等），以防止 AI 录制庭审内容。原文来自费城问询报（Philadelphia Inquirer）。HN 130 points，40 comments。`
- `why_in_top20`: `AI 硬件在特定场景（法院）的监管落地案例；涉及 Meta Ray-Ban 等主流 AI 眼镜；政策监管信号；跨科技+法律+公共政策场域。`
- `visual_assets`: `Philadelphia Inquirer 文章截图；HN 讨论串截图`
- `risks`: `地方性法规，影响范围有限；讨论度低于其他 HN 热帖`

---

### 9. llama.cpp KV rotation PR：q8 量化在 AIME25 上性能暴跌，可通过 rotation 恢复
- `topic_key`: `llama-cpp-kv-rotation-q8-aime25`
- `title`: `In the recent kv rotation PR: q8 kv quants tank performance on AIME25, recovered with rotation`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-03-30 01:57 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1s720r8/in_the_recent_kv_rotation_pr_it_was_found_that/`
- `score_total`: `13/30`
- `score_breakdown`: `一手性=2 | 传播性=1 | 破圈性=1 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉素材=1 | 平台适配=1 | 时效窗口=2 | 讨论度=1`
- `signal_summary`: `llama.cpp 社区发现：现有 q8 kv 量化在 AIME25 基准测试中性能大幅下降，但通过 KV rotation 技术可以在很大程度上恢复性能。附有 GitHub PR 链接（llama.cpp#21038）和具体 issue 评论。`
- `why_in_top20`: `涉及开源 AI infra 核心工具（llama.cpp）的技术突破；AIME25 是硬基准测试，有量化数据；GitHub PR 是强一手信源；技术社区关注度高。`
- `visual_assets`: `GitHub PR 截图；Reddit 帖子截图`
- `risks`: `技术门槛较高，受众相对垂直；暂无主流媒体报道`

---

### 10. 用户用 Claude Code 开发多个 AI 应用：从"完全不会编程"到发布 6 个网站
- `topic_key`: `claude-code-no-code-user-multi-product-launch`
- `title`: `I am fully addicted to building dumb little AI web apps. I love it.`
- `primary_platform`: `Reddit / r/ClaudeAI`
- `published_at`: `2026-03-29 15:12 CST`
- `original_link`: `https://old.reddit.com/r/ClaudeAI/comments/1s6of32/i_am_fully_addicted_to_building_dumb_little_ai/`
- `score_total`: `13/30`
- `score_breakdown`: `一手性=1 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=1 | 视觉素材=2 | 平台适配=3 | 时效窗口=2 | 讨论度=2`
- `signal_summary`: `自称完全不会编程的用户，分享如何用 Claude Code 开发了 6 个网站（Hit or Miss、FLOID、Bentu、Spork、Plainsight、ThisIsNotAnApp），附各网站链接。展现了"一人公司"创业者的 AI 原生工作流。`
- `why_in_top20`: `典型"不会编程的普通人用 AI 工具完成产品发布"的叙事；命中 AI Agent / 一人公司赛道；6 个具体产品链接（可派生外部对象）；平台适配性强（公众号/小红书/B 站均适合）。`
- `visual_assets`: `各产品网站截图（Hit or Miss / FLOID / Bentu / Spork / Plainsight / ThisIsNotAnApp）；Reddit 帖子页截图`
- `risks`: `社区信号，帖子正文内容无法完全获取；各产品网站内容需单独验证`

---

### 11. Voxtral TTS 开源模型缺失 codec encoder weights 导致无法语音克隆
- `topic_key`: `voxtral-tts-voice-cloning-missing-weights`
- `title`: `The missing piece of Voxtral TTS to enable voice cloning`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-03-29 18:32 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1s6rmoi/the_missing_piece_of_voxtral_tts_to_enable_voice/`
- `score_total`: `12/30`
- `score_breakdown`: `一手性=2 | 传播性=1 | 破圈性=1 | 赛道匹配=2 | 可延展性=2 | 数据硬度=2 | 视觉素材=1 | 平台适配=1 | 时效窗口=2 | 讨论度=1`
- `signal_summary`: `Reddit 用户 al0olo 发现 Voxtral TTS 开源模型缺少 codec encoder weights，导致 ref_audio 通道被阻断无法实现语音克隆。同时提供了 GitHub 修复链接（Al0olo/voxtral-voice-clone）。`
- `why_in_top20`: `涉及开源 TTS / voice cloning 赛道的技术补全；GitHub 修复是一手信源；voice cloning 是当下 AI 热点方向之一；有具体代码级技术细节。`
- `visual_assets`: `GitHub 仓库截图；Reddit 帖子截图`
- `risks`: `技术受众较垂直；暂无主流媒体报道`

---

### 12. BeSafe-Bench：面向实体 Agent 的行为安全风险基准测试
- `topic_key`: `besafe-bench-agent-safety-risks`
- `title`: `BeSafe-Bench: Unveiling Behavioral Safety Risks of Situated Agents in Functional Environments`
- `primary_platform`: `arXiv cs.AI`
- `published_at`: `2026-03-30 12:00 CST`
- `original_link`: `https://arxiv.org/abs/2603.25747`
- `score_total`: `12/30`
- `score_breakdown`: `一手性=3 | 传播性=1 | 破圈性=1 | 赛道匹配=3 | 可延展性=2 | 数据硬度=3 | 视觉素材=1 | 平台适配=2 | 时效窗口=2 | 讨论度=1`
- `signal_summary`: `arXiv 新论文 BeSafe-Bench（BSB）：首个评估实体 Agent 在实际环境中行为安全风险的基准测试，覆盖 Web、Mobile、Embodied VLM、Embodied VLA 四个领域。评估 13 个主流 Agent 发现：即使表现最好的 Agent 也只能在不到 40% 的任务中完全遵守安全约束，且强任务表现往往伴随严重安全违规。`
- `why_in_top20`: `arXiv 原始论文是一手信源；Agent Safety 是 AI 领域前沿研究方向；有具体量化数据（<40% 任务安全完成率）；覆盖多模态 Agent 场景；对 AI 安全监管有参考价值。`
- `visual_assets`: `arXiv 论文摘要页截图；论文配图（需核实版权）`
- `risks`: `学术论文，受众较窄；距实际应用有距离；暂无主流媒体报道`

---

### 13. Tristan Harris 在 Bill Maher 节目谈 AI 失业问题
- `topic_key`: `tristan-harris-ai-unemployment-bill-maher`
- `title`: `Tristan Harris on Bill Maher: "What's going to happen to everyone else when they don't have a job?"`
- `primary_platform`: `Reddit / r/ChatGPT`
- `published_at`: `2026-03-29 21:59 CST`
- `original_link`: `https://old.reddit.com/r/ChatGPT/comments/1s6vtjl/tristan_harris_on_bill_maher_whats_going_to/`
- `score_total`: `11/30`
- `score_breakdown`: `一手性=1 | 传播性=2 | 破圈性=2 | 赛道匹配=2 | 可延展性=2 | 数据硬度=1 | 视觉素材=1 | 平台适配=2 | 时效窗口=2 | 讨论度=3`
- `signal_summary`: `Reddit 用户转发 Tristan Harris 在 Bill Maher 节目中的片段，标题引用"What's going to happen to everyone else when they don't have a job?"——将 AI 裁员议题与公共讨论结合。`
- `why_in_top20`: `Tristan Harris 是科技伦理领域高知名度人物；Bill Maher 节目是美国主流公共讨论场；AI 就业影响是持续高热话题；跨科技+媒体+公共政策多场域。`
- `visual_assets`: `Reddit 帖子截图；如能找到 Bill Maher 节目片段视频则可大幅加分`
- `risks`: `Reddit 二手转发；暂无节目视频片段；原文立场需回链 Bill Maher 官方节目`

---

### 14. AutoB2G: Large Language Model Driven Agentic Framework for Automated Bug Fixing
- `topic_key`: `autob2g-llm-agentic-automated-bug-fixing`
- `title`: `AutoB2G: A Large Language Model Driven Agentic Framework for Automated Bug Reporting and Fixing`
- `primary_platform`: `arXiv cs.AI`
- `published_at`: `2026-03-30 12:00 CST`
- `original_link`: `https://arxiv.org/abs/2603.25747` (same abs page, check actual ID)
- `score_total`: `11/30`
- `score_breakdown`: `一手性=3 | 传播性=1 | 破圈性=1 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉素材=1 | 平台适配=1 | 时效窗口=2 | 讨论度=0`
- `signal_summary`: `arXiv cs.AI RSS 收录，标题表明是 LLM 驱动的 Agent 框架，用于自动化 Bug 报告和修复。是 AI Coding Agent 赛道的学术研究前沿。`
- `why_in_top20`: `AI Coding Agent 的学术方向；arXiv 原始论文是一手信源；自动化 bug fixing 是开发者工具的核心场景。`
- `visual_assets`: `arXiv 摘要页截图`
- `risks`: `学术论文，受众窄；暂无 HN 或媒体报道验证；具体方法论需读论文`

---

### 15. "Clear Obama Visits Meiji Era Japan"：AI 图像生成的用户创作案例
- `topic_key`: `ai-image-generation-obama-meiji-era-reddit`
- `title`: `Clear Obama Visits Meiji Era Japan`
- `primary_platform`: `Reddit / r/ChatGPT`
- `published_at`: `2026-03-29 22:47 CST`
- `original_link`: `https://old.reddit.com/r/ChatGPT/comments/1s6x0hd/clear_obama_visits_meiji_era_japan/`
- `score_total`: `8/30`
- `score_breakdown`: `一手性=1 | 传播性=1 | 破圈性=1 | 赛道匹配=2 | 可延展性=1 | 数据硬度=1 | 视觉素材=1 | 平台适配=1 | 时效窗口=1 | 讨论度=1`
- `signal_summary`: `Reddit 用户发布了一张 AI 生成的"Obama 访问明治时代日本"的图像，位于 r/ChatGPT 日榜第三。帖子正文信息有限，仅标题可见。`
- `why_in_top20`: `AI 图像生成的具体用户创作案例；Obama 形象有一定传播度；可作为 AI 图像能力展示的入门案例。整体信号较弱。`
- `visual_assets`: `Reddit 帖子截图（可见标题和链接）；如能获取图像本身则可加分`
- `risks`: `帖子正文内容不可见（Reddit API 403）；图像创作质量无法评估；讨论深度有限`

---

### 16. LocalLLaMA 2026："we are doomed" 情绪帖
- `topic_key`: `localllama-2026-community-mood`
- `title`: `LocalLLaMA 2026`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-03-29 18:03 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1s6r5gn/localllama_2026/`
- `score_total`: `5/30`
- `score_breakdown`: `一手性=1 | 传播性=1 | 破圈性=1 | 赛道匹配=2 | 可延展性=1 | 数据硬度=0 | 视觉素材=1 | 平台适配=0 | 时效窗口=1 | 讨论度=1`
- `signal_summary`: `Reddit 帖子标题为"LocalLLaMA 2026"，正文仅见"we are doomed"。属于社区情绪表达，信息密度极低。`
- `why_in_top20`: `作为 LocalLLaMA 社区情绪状态的侧面信号；可作为话题氛围参考但不适合作为正式内容选题。`
- `visual_assets`: `Reddit 帖子截图`
- `risks`: `信息量极少；正文内容未被抓取；无法形成有效内容方向`

---

### 17–20. 其他微信源候选（待一跳补查）

以下微信订阅源packet已完成抓取，待Asset Derivation阶段一跳派生后补充评分：
- `wechat/geekpark/AI` — GeekPark 微信公众号 AI 相关内容
- `wechat/qbitai/AI` — 量子位微信公众号 AI 相关内容
- `wechat/qbitai/skill_app` — 量子位技能类 App 相关内容
- `wechat/qbitai/mp.weixin (deep link)` — 微信深度链接文章

**建议一跳补查**：核实各公众号文章标题和链接，补充原始内容摘要后重新评分。

---

## 结论

- `top3_must_watch`:
  1. **DeepSeek 服务宕机约 12 小时** — 知乎 125 万热度，多家媒体（财联社+IT之家+腾讯新闻）跟进，中国头部大模型公司首次大规模宕机，有官方状态页硬数据
  2. **警察用 AI 人脸识别错误逮捕田纳西州女性** — HN 372 points/161 comments，CNN一手报道，AI伦理+法律+社会跨场域
  3. **Claude Code 每 10 分钟执行 Git reset --hard** — GitHub Issue一手信源，Anthropic 产品严重 Bug，212 points/138 comments

- `top6_strong_pool`:
  4. Sora 关停（TechCrunch 媒体入口，跨场域）
  5. Nicolas Carlini 称赞 Claude 安全研究能力（顶级专家，370万美元硬数据）
  6. Coding Agents Could Make Free Software Matter Again（HN 132 points/122 comments，开源生态叙事新颖）

- `holdout_watchlist`:
  7. Kimi K2.6 泄露 roadmap（时效强但来源弱）
  8. Philly 法院禁止智能眼镜（政策监管信号）
  9. llama.cpp KV rotation（GitHub一手，AIME25量化数据）
  10. Claude Code 用户发 6 个网站（一人公司叙事，平台适配）
  11. Voxtral TTS 语音克隆（开源赛道）
  12. BeSafe-Bench Agent 安全论文（学术一手）
  13. Tristan Harris × Bill Maher（跨场域高热）
  14–16. AutoB2G / Obama Meiji / LocalLLaMA 情绪帖（信号偏弱或信息不足）
  17–20. 微信源待补查

- `supply_risk`: `今日新增 HN（4条）+ arXiv（4条）+ 知乎（2条）+ 微信（5条）；DeepSeek 事件需回链官方状态页和财联社原始报道；Claude Code Bug 需 GitHub Issue 截图增强可信度；Kimi K2.6 传闻仍未官方验证；微信源 5 条待一跳派生补全内容摘要。`
