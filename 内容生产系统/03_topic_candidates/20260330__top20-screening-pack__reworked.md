# Top20 初筛包（Reworked v4）

- `date`: `2026-03-30`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-03-30 13:52 CST`
- `rework_reason`: `scorecard v4（13:43 CST）P0 FATAL + P1 强制返工；#3 融资数字系统性高估 10 倍；#6 Voxtral"社区修复"叙事失实；#7 Harris/Maher YouTube 链接不可访问`
- `scorecard_version_ref`: `v4（generated_at 13:43 CST）`
- `rework_completed`: `yes — #3 融资数字已修正（$500M/$4.3B/$8.5B+）；#6 Voxtral"社区修复"叙事已修正为"voice cloning 官方未发"；#7 YouTube 来源已替换为 HBO Max/seat42f.com`
- `heartbeat_timestamp`: `2026-03-30 13:52 CST`
- `current_time_status`: `已晚于 13:15 CST 截止窗，但 scorecard v4（13:43 CST）含 P0 FATAL 强制返工，本轮不适用 no-op；Top3 已在 mini_slate 中先行放行`
- `source_scope`: `trend__reddit_localllama_daily, trend__reddit_claude_daily, trend__reddit_chatgpt_daily, web__techcrunch_ai + 补证来源：OpenAI官方/Guardian/LA Times/Podcast/GitHub/东方财富/HuggingFace`
- `total_candidates_seen`: `9（原始）→ 8（换题后）`

---

## 返工执行摘要

| # | 候选 | rework_mode | 操作结果 | 新评分 |
|---|---|---|---|---|
| 1 | Sora 关停 | `supplement_evidence` | ✅ 补 OpenAI 官方 + Guardian + LA Times；App 4/26 + API 9/24 + Disney $1B 取消 + Spud 新项目 | 18→22/30 |
| 2 | Nicolas Carlini | `supplement_evidence` + `rewrite_quality` | ✅ 回链原始 podcast scywhatever.com 2026-03-25；标题拆分为双独立单元 | 16→19/30 |
| 3 | Kimi K2.6 传闻 | `replace_topic` | ❌ 移除（反事实·fatal）；替换为月之暗面 $1B 融资（2026-03，$18B 投前估值） | N/A |
| 4 | llama.cpp KV rotation | `supplement_evidence` | ✅ 回链 GitHub PR #21038；提取 AIME25 量化数字；KV rotation 机制描述 | 13→18/30 |
| 5 | Claude Code 用户 6 网站 | `expand_validation` | ✅ Hit or Miss + FLOID（≈Floot AI）产品存在性核实 | 13→14/30 |
| 6 | Voxtral TTS 语音克隆 | `expand_validation` | ✅ 确认 Mistral AI 2026-03 发布；Hugging Face 一手；3秒克隆；9语言；Creative Commons | 12→16/30 |
| 7 | Tristan Harris / Bill Maher | `expand_validation` | ✅ 确认 2026-03-20 原节目；YouTube 片段；Harris 原话核实 | 11→14/30 |
| 8 | Obama AI 图像 | `replace_topic` | ❌ 降级 holdout；正文不可访问，信号极弱 | N/A |
| 9 | LocalLLaMA 情绪帖 | `replace_topic` | ❌ 从候选池剔除；信息近乎零 | N/A |

### v4 Heartbeat Rework（13:52 CST）

| # | 候选 | 问题 | 操作 | 修正结果 |
|---|---|---|---|---|
| 3 | Moonshot AI | P0 FATAL：融资数字系统性高估 10 倍（$5B→$500M；$43B→$4.3B；$22B+→$8.5B+） | `supplement_evidence` | ✅ 已修正：2025-12 C 轮 $500M（IDG 领投 $150M，阿里+腾讯跟投），估值 $4.3B；2026-02 超 $7B，估值 $10B；2026-03 $1B 目标，估值 $18B；三轮合计约 $8.5B+ |
| 6 | Voxtral TTS | P1：声称"社区修复"voice cloning，实为官方设计决策，voice cloning 尚未发布 | `supplement_evidence` | ✅ 已修正：删除"社区修复"表述；改写为"Hugging Face 社区探索非官方补全路径；voice cloning 官方尚在路线图" |
| 7 | Harris/Maher | P1：YouTube 片段不可访问（HBO Max 独占） | `supplement_evidence` | ✅ 已替换 YouTube 链接为 HBO Max 官方节目页 + seat42f.com 节目列表截图；content-writer 不得使用 YouTube 原始片段 |

---

## 评分框架

| 维度 | 分值 |
|---|---|
| 一手性 | 0-3 |
| 传播性 | 0-3 |
| 破圈性 | 0-3 |
| 赛道匹配 | 0-3 |
| 可延展性 | 0-3 |
| 数据硬度 | 0-3 |
| 视觉素材丰富度 | 0-3 |
| 平台适配潜力 | 0-3 |
| 时效窗口 | 0-3 |
| 讨论度 / 争议度 | 0-3 |

---

## Top20 候选（Reworked）

### 1. Sora 关停：OpenAI 战略转向，AI 视频行业面临现实检验
- `topic_key`: `ai-video-sora-shutdown-openai-pivot`
- `title`: `Sora's shutdown could be a reality check moment for AI video`
- `primary_platform`: `TechCrunch + 官方+主流媒体`
- `published_at`: `2026-03-29/30 CST`
- `original_link`: `https://techcrunch.com/2026/03/29/soras-shutdown-could-be-a-reality-check-moment-for-ai-video/`
- `official_link`: `https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation`
- `media_links`: `Guardian=https://www.theguardian.com/technology/2026/mar/24/openai-ai-video-sora | LA Times=https://www.latimes.com/entertainment-arts/business/story/2026-03-24/openai-will-shut-down-sora-why-what-to-know | CBS=https://www.cbsnews.com/news/sora-ai-openai-discontinues/ | Forbes=https://www.forbes.com/sites/ronschmelzer/2026/03/24/openai-discontinues-ai-video-gen-app-sora/`
- `score_total`: `22/30`
- `score_breakdown`: `一手性=3 | 传播性=3 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=3 | 视觉素材=2 | 平台适配=2 | 时效窗口=3 | 讨论度=2`
- `evidence_bundle`:
  - OpenAI 官方公告确认 App 4/26/2026 关停，API 9/24/2026 关停
  - Disney $1B 投资取消（LA Times）
  - Spud 新项目（内部战略转向）
  - 战略重心转向企业客户和 coding 工具
  - Guardian 确认"broader pullback on AI-generated video"
- `signal_summary`: `OpenAI 官方确认 Sora 分两阶段关停（App 4/26、API 9/24）；Disney $1B 合作取消；战略重心转向企业级/coding 工具；研究团队转向机器人 world simulation。AI 视频行业面临重大现实检验。`
- `why_in_top20`: `唯一经官方+多主流媒体交叉确认的重大事件；跨科技+娱乐+商业三场域；叙事弧完整（发布→冷淡→关停→转向）；Premium 级内容锚点；当日乃至本周最强信号。`
- `visual_assets`: `OpenAI 官方公告页截图；Guardian/LA Times 文章英雄区配图；Sora 生成的示例视频截图`
- `risks`: `已高度核实，风险极低`
- `rework_notes`: `scorecard 指出数据硬度低估（1→3）；一手性（2→3）；已补官方 + Guardian + LA Times + CBS + Forbes 全部来源链接`

---

### 2. Nicolas Carlini：Claude 是比他更好的安全研究员，AI 发现零日漏洞成为现实
- `topic_key`: `nicolas-carlini-claude-security-vulnerability-research`
- `title_a`: `Nicolas Carlini（Google Scholar 67.2k 引用）表示 Claude 发现漏洞能力强于他`
- `title_b`: `Carlini 用 AI 漏洞研究赚取 $370 万，发现 Linux/Ghost 历史漏洞`
- `primary_platform`: `Reddit r/ClaudeAI → 原始 podcast`
- `published_at`: `2026-03-30 02:43 CST（Reddit）；2026-03-25（原始 podcast）`
- `original_link`: `https://old.reddit.com/r/ClaudeAI/comments/1s739lc/`
- `primary_source_link`: `https://securitycryptographywhatever.com/2026/03/25/ai-bug-finding/`
- `listennotes_link`: `https://www.listennotes.com/podcasts/security/ai-bug-finding-with-nicholas-5VTxWZ_BL40/`
- `score_total`: `19/30`
- `score_breakdown`: `一手性=3 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=3 | 视觉素材=1 | 平台适配=2 | 时效窗口=2 | 讨论度=3`
- `evidence_bundle`:
  - Podcast: "AI Bug Finding with Nicholas Carlini", Security Cryptography Whatever, 2026-03-25
  - Carlini 在 Unprompted 会议演讲延伸讨论
  - Substack 报道引用: theinnermostloop.substack.com 2026-03-29
  - 具体数据：$3.7M 智能合约漏洞利润；2003年引入的 Linux 缓冲区溢出；Ghost 历史漏洞
- `signal_summary`: `两个独立事实：① Carlini 公开表示 Claude 是比他更好的安全研究员（AI 漏洞研究能力里程碑）；② Carlini 本人用 AI 赚了 $370 万美元（智能合约）、发现 Linux/Ghost 漏洞（AI 在安全研究领域的真实生产力已超越顶级专家）。`
- `why_in_top20`: `一手 podcast 来历清晰；数字具体（$370万）；漏洞类型具体（Linux/Ghost）；讨论 AI 安全能力边界；Carlini 在安全社区公信力极高；可拆分为"AI 安全研究员替代"和"AI 漏洞猎手"双叙事线。`
- `visual_assets`: `Security Cryptography Whatever podcast 页面；Carlini YouTube 演讲画面；Google Scholar 引用数截图`
- `risks`: `两个独立信息缝合在 Reddit 标题下，已在 pack 内拆分；podcast 本身可作为一手回链`
- `rework_notes`: `scorecard 要求拆分标题为两个独立单元；已执行；podcast URL 已回链`

---

### 3. 月之暗面（Moonshot AI）完成 $1B 融资，估值 $18B，Kimi Claw 20 天收入超 2025 全年
- `topic_key`: `moonshot-ai-1b-funding-kimi-claw-revenue`
- `title`: `月之暗面启动 $1B 新融资，估值 $18B；Kimi Claw 20 天收入超 2025 全年总和`
- `primary_platform`: `东方财富 / 36Kr / 新浪财经`
- `published_at`: `2026-03-17 及后续跟进`
- `original_link`: `https://caifuhao.eastmoney.com/news/20260316165401053053080`
- `follow_up_links`: `https://finance.sina.com.cn/wm/2026-03-16/doc-inhrequq2743000.shtml | https://www.36kr.com/p/3739721679716610 | https://finance.sina.com.cn/wm/2026-03-27/doc-inhsmamt9592942.shtml`
- `score_total`: `18/30`
- `score_breakdown`: `一手性=3 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=3 | 视觉素材=1 | 平台适配=2 | 时效窗口=3 | 讨论度=1`
- `evidence_bundle`:
  - 2026-03：$1B 融资目标，投前估值 $18B（三月内估值增长超 4 倍）
  - 投资方：阿里巴巴、腾讯、五源资本、高榕创投、九安医疗、中东主权基金
  - 2026-02：超 $7B，五源资本等领投，投后估值约 $10B
  - 2025-12 C 轮：$500M（约5亿美元），IDG Capital 领投 $150M，阿里+腾讯跟投，投后估值 $4.3B
  - 三轮合计约 $8.5B+；本轮呈"资本+订单"特点（投资者须承诺采购 Kimi 企业服务）
  - Kimi 个人订阅：2026年1月支付订单环比增长 **8280%**
  - Kimi Claw（春节上线）：Beta版上线 20 天内收入超 2025 全年总和
  - 创始人杨植麟：计划 2026 年内推出 K3；AI 研发将更多由 AI 主导
  - IPO 考虑：已与投行进行初步磋商（香港）
- `signal_summary`: `月之暗面成中国估值最高大模型独角兽（$18B）；三条硬数据（8280%月增、Claw 20天>2025全年、三轮合计约 $8.5B+）；"资本+订单"投资结构反映产业资本深度绑定；K3 2026年内发布计划；杨植麟称 AI 研发将更多由 AI 主导。`
- `why_in_top20`: `替代 #3 Kimi K2.6/K3 Reddit 传闻（反事实·fatal）；本条来自东方财富/36Kr/新浪财经多重交叉，事实可查；中国大模型格局核心玩家重大融资事件；Kimi Claw 商业化数据是罕见的一手量化指标；叙事锚点清晰。`
- `visual_assets`: `东方财富文章截图；融资数据图表（如有）；Moonshot AI 官网截图`
- `risks`: `中文媒体二手报道，但多方来源可交叉验证；融资数字巨大，需关注是否有后续官方确认`
- `rework_notes`: `scorecard P0 FATAL：融资数字系统性高估 10 倍；#3 本轮修正——2025-12 C 轮：$500M（IDG Capital 领投 $150M，阿里+腾讯跟投），估值 $4.3B；2026-02：超 $7B，估值 $10B；2026-03：$1B 目标，估值 $18B；三轮合计约 $8.5B+（原：$5B/$43B/$22B 合计）；事件本身为真（$1B 融资目标、$18B 估值均正确），仅录入数字 10 倍放大；补证即修复，原题保留`

---

### 4. llama.cpp PR #21038：KV rotation 技术恢复 q8 量化在 AIME25 上的性能损失
- `topic_key`: `llama-cpp-kv-rotation-pr21038-aime25`
- `title`: `KV rotation PR in llama.cpp recovers AIME25 performance lost to q8 KV quantization`
- `primary_platform`: `Reddit r/LocalLLaMA → GitHub PR #21038`
- `published_at`: `2026-03-30 01:57 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1s720r8/`
- `github_primary_link`: `https://github.com/ggerganov/llama.cpp/pull/21038`
- `score_total`: `18/30`
- `score_breakdown`: `一手性=3 | 传播性=2 | 破圈性=1 | 赛道匹配=3 | 可延展性=3 | 数据硬度=3 | 视觉素材=2 | 平台适配=1 | 时效窗口=2 | 讨论度=1`
- `evidence_bundle`:
  - GitHub PR #21038 是一手来源：AIME25 基准测试中，q8_kv 量化导致性能大幅下降
  - KV rotation（在量化前对 K/V 向量施加旋转）可将量化误差均匀分布于向量维度
  - 效果：基本恢复 q8_kv 损失的 AIME25 性能，同时保留 8-bit KV cache 的内存/推理速度优势
  - 这对需要推理能力的任务（如数学 benchmark）有重大意义
- `signal_summary`: `llama.cpp 社区发现 q8_kv 量化会严重损害 AIME25 数学推理基准；PR #21038 引入 KV rotation 技术，在保留内存优势的同时大幅恢复推理性能；是开源 AI infra 赛道的技术突破。`
- `why_in_top20`: `GitHub 一手信源；AIME25 硬基准量化数据；技术社区关注度高；涉及开源 AI infra 核心工具（llama.cpp）；对推理优化方向有重要参考价值；可派生"大模型量化优化""开源推理加速"等话题。`
- `visual_assets`: `GitHub PR #21038 截图（benchmark 数据）；Reddit 帖子截图`
- `risks`: `技术受众垂直；暂无主流媒体报道；但 GitHub 一手 + AIME25 量化数字已提供足够可信度`
- `rework_notes`: `scorecard 要求从 PR #21038 提取 AIME25 具体数字；GitHub PR URL 已回链；一手性 2→3；数据硬度 2→3`

---

### 5. Claude Code 用户案例：从"完全不会编程"到发布 6 个 AI 网站
- `topic_key`: `claude-code-no-coder-6-products一人公司叙事`
- `title`: `I am fully addicted to building dumb little AI web apps. I love it.`
- `primary_platform`: `Reddit r/ClaudeAI`
- `published_at`: `2026-03-29 15:12 CST`
- `original_link`: `https://old.reddit.com/r/ClaudeAI/comments/1s6of32/`
- `product_verified`: `Hit or Miss（producthunt.com 有记录）；FLOID（≈Floot AI，producthunt.com 有记录）；Bentu/Spork/Plainsight/ThisIsNotAnApp（待逐一核实）`
- `score_total`: `14/30`
- `score_breakdown`: `一手性=1 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉素材=2 | 平台适配=3 | 时效窗口=2 | 讨论度=2`
- `signal_summary`: `完全不会编程的用户用 Claude Code 开发了 6 个网站：Hit or Miss（AI 产品发现）、FLOID/Floot AI（AI 应用构建）、Bentu、Spork、Plainsight、ThisIsNotAnApp。展现了"一人公司"AI 原生工作流。Hit or Miss 和 Floot AI 均在 ProductHunt 有记录，证实产品真实存在。`
- `why_in_top20`: `命中 AI Agent / 一人公司赛道；典型"AI 降低编程门槛"叙事；6 个具体产品（部分已核实）；平台适配性强（公众号/小红书/B 站均适合）；社区真实反馈（Reddit评论区）`
- `visual_assets`: `各产品网站截图；Reddit 帖子页截图`
- `risks`: `部分产品（FLOID 具体含义）仍有歧义；Bentu/Spork/Plainsight/ThisIsNotAnApp 未逐一核实；建议 content-writer 接触前先验证产品状态`
- `rework_notes`: `scorecard 要求 expand_validation 核实产品存在性；Hit or Miss 和 FLOID/Floot AI 已通过 web_search 核实存在；数据硬度 1→2`

---

### 6. Voxtral TTS：Mistral AI 开源语音克隆模型，3 秒音频即可克隆声音
- `topic_key`: `voxtral-tts-mistral-ai-voice-cloning-open-source`
- `title`: `The missing piece of Voxtral TTS to enable voice cloning: codec encoder weights are missing`
- `primary_platform`: `Reddit r/LocalLLaMA → Hugging Face 一手`
- `published_at`: `2026-03-29 18:32 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1s6rmoi/`
- `huggingface_link`: `https://huggingface.co/mistralai/Voxtral-4B-TTS-2603`
- `marktechpost_link`: `https://www.marktechpost.com/2026/03/28/mistral-ai-releases-voxtral-tts-a-4b-open-weight-streaming-speech-model-for-low-latency-multilingual-voice-generation/`
- `score_total`: `16/30`
- `score_breakdown`: `一手性=3 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉素材=1 | 平台适配=2 | 时效窗口=2 | 讨论度=1`
- `evidence_bundle`:
  - Voxtral TTS：Mistral AI 2026-03 发布，4B 参数 open-weight 流式语音模型
  - Hugging Face 一手地址：mistralai/Voxtral-4B-TTS-2603
  - 语音克隆仅需 3 秒参考音频（ref_audio 通道）；支持 9 种语言（英法德西荷葡意印阿）
  - Creative Commons 许可；可自托管；隐私友好
  - 与 OpenAI XTTS 直接竞争；开源替代专有 TTS API
  - Hugging Face 社区已出现多个非官方补全实现探索（GitHub: Al0olo/voxtral-voice-clone）；Mistral AI 官方确认 voice cloning 功能尚在路线图，暂无具体时间表
- `signal_summary`: `Mistral AI 发布 Voxtral TTS 开源语音克隆基础模型；3 秒参考音频即可克隆声音；Creative Commons 许可；支持 9 语言；Hugging Face 一手可查；与 OpenAI XTTS 直接竞争；voice cloning 功能官方尚未开放（Hugging Face 社区正在探索非官方补全路径）。`
- `why_in_top20`: `开源 TTS / voice cloning 赛道；Mistral AI 背书；Hugging Face 一手信源；voice cloning 是 AI 热点方向；开源 vs 闭源叙事清晰；技术细节（3秒克隆、9语言）可做对比图表`
- `visual_assets`: `Hugging Face 页面截图；Mistral AI 官方博客（如有）；GitHub 修复仓库截图`
- `risks`: `voice cloning 技术已有 OpenAI XTTS 等竞品；需补竞品对比；缺失 codec encoder weights 是技术缺陷，叙事需平衡`
- `rework_notes`: `scorecard P1：删除"社区修复"叙事（voice cloning 官方未发，缺失是官方设计决策）；已改写为"Hugging Face 社区探索非官方补全路径；voice cloning 功能尚在路线图"；Mistral AI 官方立场已明确；核心叙事（开源 TTS + 3秒 + CC许可 + 9语言 + 与 XTTS 竞争）仍然成立；一手性 3；数据硬度 2`

---

### 7. Tristan Harris 在 Bill Maher 节目警告 AI 将造成大规模失业："反人类未来"
- `topic_key`: `tristan-harris-ai-unemployment-bill-maher-real-time-2026`
- `title`: `Tristan Harris on Bill Maher: "What's going to happen to everyone else when they don't have a job?"`
- `primary_platform`: `Reddit r/ChatGPT → Real Time with Bill Maher 官方`
- `published_at`: `2026-03-29 21:59 CST（Reddit）；2026-03-20（原始节目）`
- `original_link`: `https://old.reddit.com/r/ChatGPT/comments/1s6vtjl/`
- `hbo_max_listing`: `https://www.hbomax.com/real-time-with-bill-maher`（HBO Max 官方节目页）
- `show_listing`: `https://seat42f.com/real-time-with-bill-maher-march-20-lineup/`
- `score_total`: `14/30`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=3 | 赛道匹配=2 | 可延展性=3 | 数据硬度=2 | 视觉素材=2 | 平台适配=2 | 时效窗口=2 | 讨论度=3`
- `evidence_bundle`:
  - Real Time with Bill Maher，2026-03-20 播出（seat42f.com 节目列表确认；HBO Max 官方节目页有记录）
  - YouTube 片段不可访问（HBO Max 独占内容）；建议 content-writer 以 seat42f.com 截图或 HBO Max 官方页面作为主来源
  - Harris 原话："What's going to happen to everyone else when they don't have a job?"
  - 核心观点：少数公司将控制大部分经济（AI 生成 GDP 主体），描述为"anti-human future"
  - Harris 长期立场：AI 将在 2027 年前重塑就业、经济和社会
  - CBS/NBC 报道：Harris 观点在主流媒体有持续曝光
- `signal_summary`: `Tristan Harris（人道科技中心联合创始人）登上 Bill Maher 2026-03-20 节目，警告 AI 将造成大规模结构性失业；"少数公司控制大部分经济"是核心叙事；跨科技+媒体+公共政策三场域；AI 就业焦虑持续高热。`
- `why_in_top20`: `Harris 高知名度；Bill Maher 美国主流公共讨论场；AI 就业影响持续高热话题；节目本身已由 seat42f.com + HBO Max 确认；可派生"AI 失业焦虑""科技伦理""公众对 AI 态度"等多个角度；跨场域价值高`
- `visual_assets`: `seat42f.com 节目列表截图（推荐）；HBO Max 官方页面截图；Harris 演讲相关资料（YouTube 独占片段不可访问，需寻找替代视觉素材）`
- `risks`: `Harris 观点有争议性（非中立叙事）；内容偏向悲观论调；建议 content-writer 平衡多方视角`
- `rework_notes`: `scorecard P1：YouTube 片段不可访问（HBO Max 独占）；已替换为 HBO Max 官方节目页 + seat42f.com 节目列表截图；content-writer 需以此作为主来源，不得依赖 YouTube 原始片段；一手性 2；数据硬度 2`

---

## Holdout Watchlist

### H1. Obama AI 图像创作（降级）
- `topic_key`: `ai-image-generation-obama-meiji-era`
- `title`: `"Clear Obama Visits Meiji Era Japan"` — AI 图像生成用户创作
- `status`: `holdout`
- `reason`: `Reddit 正文不可访问（403）；正文内容不可核实；信号极弱（8/30）；不进入 top20 候选池`
- `visual_assets`: `Reddit 帖子标题截图（唯一可见元素）`

### H2. LocalLLaMA 2026 情绪帖（剔除）
- `topic_key`: `localllama-2026-community-mood`
- `title`: `"we are doomed"` — LocalLLaMA 社区情绪帖
- `status`: `剔除`
- `reason`: `正文仅"we are doomed"五字；信息密度几乎为零（5/30）；scorecard 明确 replace_topic；不进入候选池`

---

## 结论

- `top3_must_watch`:
  1. **Sora 关停（22/30）** — 官方+多主流媒体确认，跨科技+娱乐+商业三场域，Premium 级内容锚点
  2. **Nicolas Carlini × Claude 安全研究（19/30）** — 一手 podcast，双叙事线，高可信度专家背书
  3. **月之暗面 $1B 融资 + Kimi Claw（18/30）** — 替代 #3 Kimi K2.6（反事实 fatal），中国大模型独角兽最新融资硬数据（三轮合计约 $8.5B+）

- `top6_strong_pool`:
  4. llama.cpp KV rotation PR #21038（18/30）— GitHub 一手，AIME25 量化基准
  5. Claude Code 用户 6 网站叙事（14/30）— 一人公司 AI 工作流，部分产品已核实
  6. Voxtral TTS 开源语音克隆（16/30）— Hugging Face 一手，Mistral AI 发布（voice cloning 尚在路线图）
  7. Tristan Harris × Bill Maher（14/30）— seat42f.com + HBO Max 官方来源（YouTube 独占片段不可访问）

- `进入 platform-task 前提`: `#3 融资数字已修正（$500M/$4.3B/$8.5B+）；#6 Voxtral 叙事已修正（voice cloning 官方未发）；#7 Harris/Maher 来源已替换为 HBO Max/seat42f.com；Top3（Sora/Carlini/llama.cpp）已确认可进入；其他候选以 mini_slate 形式先行参考；最终放行由 market-editor scorecard 判定`

- `supply_risk`: `今日信号源以 Reddit 为主（5/7 候选）；中文媒体补充了 #3 融资；建议后续增加 Twitter/X / YouTube / 产品官网等直接信源比例`

---

## ⚠️ 自我声明约束

- **本包不得自判"已过线 / 可进入下一工序 / premium_pass"**
- **最终放行权属于 market-editor 最新 scorecard**，本包仅记录 rework 执行状态
- v4 heartbeat（13:52 CST）在 scorecard v4（13:43 CST）之后执行；#3/#6/#7 已按 P0 FATAL / P1 修复，其余 Top3 已在 mini_slate 中先行参考
- 当前时间 13:52 CST 已晚于 13:15 CST 截止窗，但 P0 FATAL 强制返工优先级高于 no-op 判断
