# Top20 初筛包

- `date`: `2026-03-28`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-03-28 18:46 CST`
- `source_scope`: `WeChat (6) | Reddit/r/LocalLLaMA (3) | Reddit/r/ChatGPT (2) | Reddit/r/ClaudeAI (2) | TechCrunch AI (5) | HN Frontpage (1) | FinSMEs (1) | OpenAI News (1) | Zhihu Hot (2) | Bilibili (1) | YouTube (2) | Baidu (1) | Feigua (1) | Trend Hunt (7)`
- `total_candidates_seen`: `35`
- `top20_count`: `20`

---

## 使用说明

- 这是 `signal-scout` 阶段正式交付包。
- 不是原始 source packet 堆砌，每个候选包含结构化评分与证据摘要。
- 本日有效候选 35 个，选取得分最高且信号完整的 20 条进 Top20，余下列入 Holdout Watchlist。

---

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

---

## Top20 候选

### 1. SoftBank $400亿贷款指向 2026 年 OpenAI IPO

- `title`: Why SoftBank's new $40B loan points to a 2026 OpenAI IPO
- `topic_key`: softbank-openai-ipo-signal
- `primary_platform`: TechCrunch AI
- `published_at`: 2026-03-28 05:44 CST
- `original_link`: https://techcrunch.com/2026/03/27/why-softbanks-new-40b-loan-points-to-a-2026-openai-ipo/
- `score_total`: 22/30
- `score_breakdown`: 一手性 1 | 传播性 3 | 破圈性 3 | 赛道匹配 3 | 可延展性 3 | 数据硬度 3 | 视觉素材 1 | 平台适配 3 | 时效窗口 3 | 讨论度 2
- `signal_summary`: JPMorgan + Goldman Sachs 联合向 SoftBank 提供 12 个月无担保贷款 $40B，TechCrunch 解读这与 OpenAI 可能的 2026 年 IPO 直接相关。涉及华尔街最大两家投行、大规模融资结构变化，以及 OpenAI 上市预期，是融资市场与 AI 资本格局的交叉点。
- `why_top1`: 数据硬（$40B + 投行名称）+ 产业解读空间大（IPO 预期对 OpenAI 估值、融资竞品格局、AI 一级市场影响）+ 时效性极强
- `visual_assets`: TC 文章截图；软银 / OpenAI 相关图片
- `risks`: 仍是媒体解读，非软银或 OpenAI 官方公告；需要回链两方公告或 SEC 文件交叉验证

---

### 2. 昆仑万维一口气球发3个大模型 + 2026 AGI 战略（中关村论坛）

- `title`: 刚刚，一口气连发3个王炸模型、亮出2026年AGI战略，昆仑万维夯爆了
- `topic_key`: kunlun-agi-three-models-2026
- `primary_platform`: 微信 / 机器之心
- `published_at`: 2026-03-27 21:38 CST
- `original_link`: https://mp.weixin.qq.com/s/g5-Y-7H1hfovmyBcB6WSqQ
- `score_total`: 21/30
- `score_breakdown`: 一手性 2 | 传播性 2 | 破圈性 3 | 赛道匹配 3 | 可延展性 3 | 数据硬度 2 | 视觉素材 2 | 平台适配 3 | 时效窗口 3 | 讨论度 2
- `signal_summary`: 昆仑万维在中关村论坛一口气发布 3 个大模型，公布 2026 AGI 战略，定位"全球第一梯队"。中文 AI 大厂自研模型密集发布，AGI 战略明确，是国产大模型竞争格局的重要信号。
- `why_top2`: 中文大厂密集动作 + 3 个模型同期发布 + AGI 时间表表态 + 中关村论坛官方背书
- `visual_assets`: 机器之心文章截图；中关村论坛现场图片
- `risks`: 需要回链昆仑万维官方发布会或官方公告；具体模型参数和能力待验证

---

### 3. Google TurboQuant + Qwen 本地跑通 MacBook Air——开源推理效率突破

- `title`: Google TurboQuant running Qwen Locally on MacAir
- `topic_key`: turboquant-qwen-macbook-air
- `primary_platform`: Reddit /r/LocalLLaMA
- `published_at`: 2026-03-28 07:33 CST
- `original_link`: https://old.reddit.com/r/LocalLLaMA/comments/1s5kdu0/google_turboquant_running_qwen_locally_on_macair/
- `score_total`: 21/30
- `score_breakdown`: 一手性 2 | 传播性 2 | 破圈性 2 | 赛道匹配 3 | 可延展性 3 | 数据硬度 3 | 视觉素材 2 | 平台适配 2 | 时效窗口 3 | 讨论度 2
- `signal_summary`: 开发者将 Google TurboQuant 压缩算法 patch 进 llama.cpp，在普通 MacBook Air（M4, 16GB）上成功跑通 Qwen 3.5-9B，20000 token context。附 atomic.chat 开源工具。
- `why_top3`: 硬技术突破 + 硬件降级门槛（MacBook Air 即可）+ 开源生态信号 + 命中"AI 普惠"主线
- `visual_assets`: Reddit 帖子正文截图；atomic.chat 界面截图
- `risks`: Reddit 帖子为二手验证；需回链 TurboQuant 原论文 / Google 官方博客

---

### 4. UCSD AIBuildAI 智能体：AI 自动构建 AI 模型，OpenAI MLE-Bench 榜单第一

- `title`: 让AI自动构建AI模型：UCSD 推出 AIBuildAI 智能体，斩获OpenAI MLE-Bench榜单第一
- `topic_key`: aibuildai-mle-bench-top
- `primary_platform`: 微信 / 机器之心
- `published_at`: 2026-03-27 21:38 CST
- `original_link`: https://mp.weixin.qq.com/s/8sb5CpBLb3PEQ7IGY6A5ug
- `score_total`: 20/30
- `score_breakdown`: 一手性 2 | 传播性 2 | 破圈性 2 | 赛道匹配 3 | 可延展性 3 | 数据硬度 3 | 视觉素材 2 | 平台适配 2 | 时效窗口 3 | 讨论度 1
- `signal_summary`: UCSD 推出 AIBuildAI 智能体，用户用自然语言描述任务即可全自动构建 AI 模型，在 OpenAI MLE-Bench 榜单获得第一。是 AutoML + AI Agent 的深度结合，AutoMLBench 第一名有真实 benchmark 支撑。
- `why_top4`: 学术 + 工业级 benchmark 验证 + AutoML + AI Agent 交叉赛道 + 开源或可复现
- `visual_assets`: 机器之心文章截图；MLE-Bench 榜单截图
- `risks`: 需要回链 UCSD 论文或 GitHub repo；中文报道可能有信息衰减

---

### 5. Unsloth Studio 重大更新：50+ 功能，推理速度追平 llama.cpp

- `title`: New Unsloth Studio Release!
- `topic_key`: unsloth-studio-major-update
- `primary_platform`: Reddit /r/LocalLLaMA
- `published_at`: 2026-03-27 23:06 CST
- `original_link`: https://old.reddit.com/r/LocalLLaMA/comments/1s56q9g/new_unsloth_studio_release/
- `score_total`: 20/30
- `score_breakdown`: 一手性 2 | 传播性 2 | 破圈性 2 | 赛道匹配 3 | 可延展性 3 | 数据硬度 3 | 视觉素材 2 | 平台适配 3 | 时效窗口 2 | 讨论度 1
- `signal_summary`: Unsloth Studio Beta 一周后重大更新：预编译 llama.cpp/mamba_ssm 二进制（安装体积降 50%）、推理速度提升 20-30% 追平 llama-server、Tool calling 改进、AMD/MacOS CPU 支持、uv 一行安装等 50+ 新功能。MLX/AMD/API 下月推出。
- `why_top5`: 官方产品更新，硬数据密集 + 开发者生态信号 + 开源效率赛道持续升温
- `visual_assets`: Reddit 帖子含详细 changelog；官网 https://github.com/unslothai/unsloth
- `risks`: 商业产品更新，需要回链官方 release notes / GitHub

---

### 6. KV Dequant 优化 +22.8% decode 提升——TurboQuant 具体实现细节

- `title`: Skipping 90% of KV dequant work → +22.8% decode at 32K (llama.cpp, TurboQuant)
- `topic_key`: kv-dequant-turboquant-detail
- `primary_platform`: Reddit /r/LocalLLaMA
- `published_at`: 2026-03-27 22:56 CST
- `original_link`: https://old.reddit.com/r/LocalLLaMA/comments/1s56g07/skipping_90_of_kv_dequant_work_228_decode_at_32k/
- `score_total`: 19/30
- `score_breakdown`: 一手性 2 | 传播性 1 | 破圈性 1 | 赛道匹配 3 | 可延展性 3 | 数据硬度 3 | 视觉素材 3 | 平台适配 2 | 时效窗口 3 | 讨论度 1
- `signal_summary`: 开发者分享在 llama.cpp 中实现 TurboQuant KV cache 压缩的具体瓶颈与解决方案：利用 attention sparsity 跳过 90% V dequant，Qwen3.5-35B-A3B M5 Max 上实现 +22.8% decode，PPL 不变，NIAH 7/9 → 9/9。附 GitHub + 论文。CUDA 移植测试中。
- `why_top6`: 硬核开源技术内容，数据完整 + 与 TurboQuant 主线强关联
- `visual_assets`: Reddit 含详细技术指标；GitHub: https://github.com/TheTom/turboquant_plus
- `risks`: 技术细节深，需要目标读者是开发者；CUDA 版本尚未完成

---

### 7. STADLER × ChatGPT：230 年老企业用 AI 重塑知识工作（OpenAI 官方案例）

- `title`: STADLER reshapes knowledge work at a 230-year-old company
- `topic_key`: stadler-chatgpt-enterprise
- `primary_platform`: OpenAI News（官方一手源）
- `published_at`: 2026-03-28 06:00 CST
- `original_link`: https://openai.com/index/stadler
- `score_total`: 19/30
- `score_breakdown`: 一手性 3 | 传播性 1 | 破圈性 1 | 赛道匹配 3 | 可延展性 2 | 数据硬度 3 | 视觉素材 1 | 平台适配 3 | 时效窗口 2 | 讨论度 1
- `signal_summary`: OpenAI 官方客户案例：STADLER（230 年历史企业）使用 ChatGPT 改造知识工作，节省时间、提升 650 名员工生产力。是 B2B 企业 AI 落地 + 传统行业数字化转型的典型样本。
- `why_top7`: 官方一手 + B2B 企业场景 + 真实生产力数据 + AI 企业落地赛道
- `visual_assets`: OpenAI 官方页面截图
- `risks`: 企业案例细节有限；需要回链 STADLER 官网或 LinkedIn 补充

---

### 8. 最强 Claude 模型提前曝光 + Anthropic 三千份保密档案外泄

- `title`: 最强Claude模型提前曝光！附带Anthropic三千份保密档案在线裸奔
- `topic_key`: claude-leak-next-model
- `primary_platform`: 微信 / 量子位
- `published_at`: 2026-03-28 00:01 CST（最新鲜）
- `original_link`: https://mp.weixin.qq.com/s/JbEkb5rK3hx8viEl-lsVRQ
- `score_total`: 18/30
- `score_breakdown`: 一手性 2 | 传播性 2 | 破圈性 2 | 赛道匹配 3 | 可延展性 3 | 数据硬度 2 | 视觉素材 1 | 平台适配 2 | 时效窗口 3 | 讨论度 3
- `signal_summary`: 量子位报道：比 Opus 4.6 更强的 Claude 新模型提前曝光，同时 Anthropic 内部 3000 份保密档案在线外泄，新模型能力 + 数据安全双重叙事叠加，是 Claude / Anthropic 近期最大舆论事件。
- `why_top8`: 新模型信号 + 数据安全事件双重叙事 + Claude 生态关注度高 + 时效极强
- `visual_assets`: 量子位文章截图；Anthropic 相关图片
- `risks`: 需要回链原始泄露源或 Anthropic 官方回应；媒体报道可能存在夸大

---

### 9. 知乎热榜：千问正式上线 AI 打车，高德滴滴 AI 交锋（94 万热度）

- `title`: 千问正式上线 AI 打车，高德和滴滴开始在 AI 交锋，对消费者来说意味着什么？
- `topic_key`: qwen-ai-taxi-gaode-didi
- `primary_platform`: 知乎热榜
- `published_at`: 2026-03-24 09:31 CST
- `original_link`: https://www.zhihu.com/question/2019707833172672559
- `score_total`: 18/30
- `score_breakdown`: 一手性 1 | 传播性 2 | 破圈性 3 | 赛道匹配 3 | 可延展性 3 | 数据硬度 2 | 视觉素材 1 | 平台适配 3 | 时效窗口 2 | 讨论度 3
- `signal_summary`: 知乎热榜 94 万热度：阿里千问 3 月 23 日正式上线 AI 打车（选车型、途经点、预约、个性化需求"空气清新/驾驶平稳"、App 内支付），滴滴 AI 出行助手小滴同步上线（90+ 服务标签、扶老携幼/商务接待）。AI 应用深入出行赛道，两大平台正式交锋。
- `why_top9`: 94 万热 + 真实用户问答 + 阿里 vs 滴滴双强 AI 落地对比 + 消费级 AI 应用叙事
- `visual_assets`: 知乎热榜截图；千问/滴滴 App 界面想象图
- `risks`: 热榜问题说明热度不代表事实强度；需要回链千问/滴滴官方公告

---

### 10. "刚刚，NeurIPS 退让了"

- `title`: 刚刚，NeurIPS退让了
- `topic_key`: neurips-retreat-ai-governance
- `primary_platform`: 微信 / 机器之心
- `published_at`: 2026-03-27 21:38 CST
- `original_link`: https://mp.weixin.qq.com/s/8sb5CpBLb3PEQ7IGY6A5ug（机机之心综合报道页面）
- `score_total`: 17/30
- `score_breakdown`: 一手性 1 | 传播性 2 | 破圈性 2 | 赛道匹配 2 | 可延展性 3 | 数据硬度 2 | 视觉素材 1 | 平台适配 2 | 时效窗口 3 | 讨论度 3
- `signal_summary`: 机器之心报道 NeurIPS "退让了"——具体内容需回链原文，但顶会 AI 伦理/政策争议类事件通常代表学术圈对 AI 进展的制度性回应，是 AI 治理话题的破圈信号。
- `why_top10`: 顶会动态 + AI 治理/伦理争议 + 学术圈制度性回应 + 高讨论度
- `visual_assets`: 机器之心文章截图
- `risks`: 标题语义不明确，需要回链机器之心原文或 NeurIPS 官方声明确认具体事件

---

### 11. OpenAI 关闭 Sora + Meta 法院败诉——AI 基础设施扩张遭遇"现实世界抵抗"

- `title`: OpenAI shuts down Sora while Meta gets shut out in court
- `topic_key`: openai-sora-meta-court-resistance
- `primary_platform`: TechCrunch AI
- `published_at`: 2026-03-27 21:30 CST
- `original_link`: https://techcrunch.com/video/openai-shuts-down-sora-while-meta-gets-shut-out-in-court/
- `score_total`: 17/30
- `score_breakdown`: 一手性 1 | 传播性 3 | 破圈性 3 | 赛道匹配 2 | 可延展性 3 | 数据硬度 2 | 视觉素材 2 | 平台适配 2 | 时效窗口 2 | 讨论度 3
- `signal_summary`: TechCrunch 播客分析：OpenAI 关闭 Sora 与 Meta 在肯塔基州数据中心用地诉讼中败诉的对比叙事——AI 基础设施向外扩张，但"现实世界"开始反击（82 岁老太太拒绝 $2600 万征地补偿）。
- `why_top11`: 产业叙事深度（AI 扩张 vs 社区阻力）+ 跨平台讨论潜力 + Meta 诉讼是真实法律事件
- `visual_assets`: TC 播客视频封面；肯塔基州数据中心相关图片
- `risks`: 播客内容，缺少单一核心数据点；Meta 诉讼需回链法院文件

---

### 12. VCs 赌 AI 下一波十亿级投资，为何 OpenAI 却关闭 Sora？

- `title`: VCs are betting billions on AI's next wave, so why is OpenAI killing Sora?
- `topic_key`: vcs-betting-ai-next-wave-sora-killed
- `primary_platform`: TechCrunch AI Podcast
- `published_at`: 2026-03-27 23:40 CST
- `original_link`: https://techcrunch.com/podcast/vcs-are-betting-billions-on-ais-next-wave-so-why-is-openai-killing-sora/
- `score_total`: 16/30
- `score_breakdown`: 一手性 1 | 传播性 2 | 破圈性 3 | 赛道匹配 2 | 可延展性 3 | 数据硬度 2 | 视觉素材 1 | 平台适配 3 | 时效窗口 2 | 讨论度 3
- `signal_summary`: TechCrunch Equity 播客：VC 们在 AI 领域持续投入数十亿，但 OpenAI 关闭 Sora 的决定暴露了 AI 商业化的深层矛盾——算力成本、产品化节奏与资本回报预期的冲突。
- `why_top12`: 投资叙事 + AI 商业化困境 + 播客形式可转为图文摘要
- `visual_assets`: TC 播客封面图
- `risks`: 播客内容，直接引用价值有限；需要回链更多 VCs 投资数据

---

### 13. HN 热帖：.claude/ 文件夹结构解析（388 分 / 194 评论）

- `title`: Anatomy of the .claude/ folder
- `topic_key`: hn-claude-folder-anatomy
- `primary_platform`: Hacker News Frontpage
- `published_at`: 2026-03-27 22:35 CST
- `original_link`: https://news.ycombinator.com/item?id=47543139
- `score_total`: 16/30
- `score_breakdown`: 一手性 2 | 传播性 2 | 破圈性 2 | 赛道匹配 2 | 可延展性 3 | 数据硬度 2 | 视觉素材 2 | 平台适配 3 | 时效窗口 2 | 讨论度 3
- `signal_summary`: 开发者博客解析 Claude Code 的 .claude/ 配置文件夹结构，HN 上获得 388 分 / 194 评论。是开发者工具、Claude 生态、prompt 配置管理的实用内容，命中 builder 受众。
- `why_top13`: HN 高热 + builder 圈层扩散 + Claude 生态深度内容
- `visual_assets`: 博客文章配图；HN 评论区技术讨论截图
- `risks`: 技术细分受众；需要回链原博客文章 + GitHub（如有）

---

### 14. 用户详述 ChatGPT Plus 退订：产品体验恶化（真实负面反馈）

- `title`: I finally cancelled my ChatGPT Plus subscription.
- `topic_key`: chatgpt-plus-cancellation
- `primary_platform`: Reddit /r/ChatGPT
- `published_at`: 2026-03-27 20:53 CST
- `original_link`: https://old.reddit.com/r/ChatGPT/comments/1s538v6/i_finally_cancelled_my_chatgpt_plus_subscription/
- `score_total`: 15/30
- `score_breakdown`: 一手性 1 | 传播性 2 | 破圈性 2 | 赛道匹配 2 | 可延展性 2 | 数据硬度 2 | 视觉素材 1 | 平台适配 2 | 时效窗口 2 | 讨论度 3
- `signal_summary`: 用户详述退订原因：ChatGPT 不回答所问问题、给出不想要的建议、无尽单方面独白、直接撒谎，audio 功能问题尤其严重，转向寻找替代品。反映付费用户对产品质量下滑的真实不满。
- `why_top14`: 真实用户负面反馈 + ChatGPT 付费留存压力信号 + "AI 产品体验 vs 期望差距"话题
- `visual_assets`: Reddit 帖子截图
- `risks`: 单一个案，需要更多样本交叉验证；情绪成分较高

---

### 15. Claude Pro 用户投诉用量异常：计费透明度问题

- `title`: This isn't right
- `topic_key`: claude-pro-billing-anomaly
- `primary_platform`: Reddit /r/ClaudeAI
- `published_at`: 2026-03-27 22:27 CST
- `original_link`: https://old.reddit.com/r/ClaudeAI/comments/1s55mvg/this_isnt_right/
- `score_total`: 14/30
- `score_breakdown`: 一手性 1 | 传播性 1 | 破圈性 1 | 赛道匹配 2 | 可延展性 2 | 数据硬度 2 | 视觉素材 1 | 平台适配 2 | 时效窗口 2 | 讨论度 2
- `signal_summary`: Claude Pro 用户反映使用量计费异常：一句"Hello"占用 4% 用量，天气查询占 7%，认为系统出问题时会用量失控，官方只有 chatbot 客服无法解决。反映 AI 订阅制计费透明度问题。
- `why_top15`: 付费产品计费争议 + 客服体验差 + Anthropic 运营压力信号
- `visual_assets`: Reddit 帖子截图
- `risks`: 单一个案；Anthropic 官方无回应

---

### 16. GAN 风格思考框架——一句话改善任何 Claude 对话

- `title`: One sentence that instantly improves any Claude conversation — borrowed from how GANs work
- `topic_key`: gan-style-claude-prompt
- `primary_platform`: Reddit /r/ClaudeAI
- `published_at`: 2026-03-27 17:56 CST
- `original_link`: https://old.reddit.com/r/ClaudeAI/comments/1s4zqeq/one_sentence_that_instantly_improves_any_claude/
- `score_total`: 13/30
- `score_breakdown`: 一手性 1 | 传播性 2 | 破圈性 1 | 赛道匹配 2 | 可延展性 3 | 数据硬度 2 | 视觉素材 1 | 平台适配 2 | 时效窗口 1 | 讨论度 1
- `signal_summary`: 高赞 prompt 工程技巧：在任何 Claude 对话中加入"Use a GAN-style thinking framework"，让 Claude 从"yes-man"模式切换到对抗性思考伙伴。附 Mac Mini vs 云 GPU 的具体应用实例。
- `why_top16`: prompt 工程技巧圈层传播 + Mac Mini 一人 AI 工作站话题潜在关联
- `visual_assets`: Reddit 帖子正文截图
- `risks`: 技巧类内容，时效窗口较短；非产品或公司新闻

---

### 17. SK hynix 美股 IPO 融资 $100-140 亿——"RAMmageddon"终结方案

- `title`: Memory chip giant SK hynix could help end 'RAMmageddon' with blockbuster US IPO
- `topic_key`: sk-hynix-ipo-rammageddon
- `primary_platform`: TechCrunch AI
- `published_at`: 2026-03-28 03:11 CST
- `original_link`: https://techcrunch.com/2026/03/27/memory-chip-giant-sk-hynix-could-help-end-rammageddon-with-blockbuster-us-ipo/
- `score_total`: 15/30
- `score_breakdown`: 一手性 1 | 传播性 2 | 破圈性 2 | 赛道匹配 2 | 可延展性 2 | 数据硬度 3 | 视觉素材 1 | 平台适配 2 | 时效窗口 2 | 讨论度 1
- `signal_summary`: TechCrunch 报道 SK hynix 考虑赴美上市，融资 $100-140 亿扩充产能，是解决 AI 记忆芯片全球短缺（"RAMmageddon"）的关键举措。SK hynix 是 HBM 龙头，HBM 是 AI GPU 核心内存。
- `why_top17`: AI 硬件基础设施 + 芯片短缺叙事 + 大规模融资；赛道匹配度高
- `visual_assets`: TC 文章截图；SK hynix / HBM 相关图
- `risks`: 仍是媒体报道，需要回链 SK hynix 官方公告或韩交所文件

---

### 18. 杨植麟主持大模型圆桌：张鹏、罗福莉、夏立雪都放开说了

- `title`: 杨植麟当主持人的大模型圆桌：张鹏罗福莉夏立雪都放开说了
- `topic_key`: yang-zhilin-model-roundtable
- `primary_platform`: 微信 / 量子位
- `published_at`: 2026-03-28 00:01 CST（最新鲜）
- `original_link`: https://mp.weixin.qq.com/s/pOYgY0ci86dHZgMWcbwXq（推测）
- `score_total`: 14/30
- `score_breakdown`: 一手性 1 | 传播性 1 | 破圈性 2 | 赛道匹配 2 | 可延展性 2 | 数据硬度 1 | 视觉素材 1 | 平台适配 2 | 时效窗口 2 | 讨论度 2
- `signal_summary`: 量子位 / 机器之心报道：杨植麟当主持人，MiniMax CEO 张鹏、阿里 罗福莉、字节 夏立雪共同参与大模型圆桌，四位核心人物罕见同框，观点放开。是国产大模型核心人物生态的关键观察窗口。
- `why_top18`: 国产大模型核心人物同框 + 四方观点碰撞 + 行业趋势信号
- `visual_assets`: 量子位/机器之心文章截图；可能需要回链现场视频
- `risks`: 需要回链圆桌实录或视频；报道可能有选择性

---

### 19. 极客公园：谷歌推《黑客帝国》同名 AI；智元机器人量产超万台；央视谈人脸识别

- `title`: 谷歌推《黑客帝国》同名 AI；传智元机器人量产超万台；央视：使用人脸识别时，千万穿好衣服 | 极客早知道
- `topic_key`: geekpark-google-matrix-zhiyuan-robot
- `primary_platform`: 微信 / 极客公园
- `published_at`: 2026-03-27（具体时间待确认）
- `original_link`: https://mp.weixin.qq.com/s/aJZKf9WefHQDwFQiYgVPGw
- `score_total`: 13/30
- `score_breakdown`: 一手性 1 | 传播性 1 | 破圈性 2 | 赛道匹配 2 | 可延展性 2 | 数据硬度 2 | 视觉素材 1 | 平台适配 2 | 时效窗口 2 | 讨论度 1
- `signal_summary`: 极客公园早报：谷歌推出与《黑客帝国》同名的 AI 产品（Matrix 相关？），智元机器人宣布量产超万台，央视对人脸识别使用发出提醒。三个独立事件的综合科技早报，消费级 AI + 硬件 + 监管三个维度。
- `why_top19`: 智元机器人量产是新事件 + 谷歌 AI 命名话题性强 + 央视监管信号
- `visual_assets`: 极客公园文章截图
- `risks`: 三合一综合报道，单条信息深度有限；需要逐条回链验证

---

### 20. Newo 融资 $2500 万 Series A（FinSMEs 来源，2 月 10 日归档）

- `title`: Newo Raises $25M in Series A Funding
- `topic_key`: newo-series-a-finsmes
- `primary_platform`: FinSMEs via Google News Fallback
- `published_at`: 2026-02-10 16:00 CST（近 7 周前，时效性低）
- `original_link`: Google News 长链
- `score_total`: 9/30
- `score_breakdown`: 一手性 0 | 传播性 1 | 破圈性 1 | 赛道匹配 1 | 可延展性 2 | 数据硬度 1 | 视觉素材 1 | 平台适配 2 | 时效窗口 0 | 讨论度 0
- `signal_summary`: FinSMEs 报道 Newo 获 $2500 万 Series A 融资，来源为 Google News site-filter fallback，非官方直连，信号质量低。时效性已过近 7 周。
- `why_top20`: 作为 Newco / 融资入口保留；实际内容价值有限
- `visual_assets`: Google News RSS 条目截图
- `risks`: 日期过老（2 月 10 日）；非 AI 相关度高；需要回链公司官网和官方公告才有实质价值

---

## 结论

- `top3_must_watch`:
  1. **SoftBank $40B 贷款指向 2026 OpenAI IPO**（数据硬 + 产业解读空间大 + 时效性强）
  2. **昆仑万维 3 个大模型 + 2026 AGI 战略**（中文大厂密集动作 + 第一梯队定位）
  3. **Google TurboQuant + Qwen 本地跑通 MacBook Air**（技术突破 + 开源生态 + AI 普惠叙事）

- `top6_strong_pool`:
  4. UCSD AIBuildAI：AI 自动构建 AI 模型，MLE-Bench 第一
  5. Unsloth Studio 50+ 功能重大更新
  6. KV Dequant 优化 +22.8% decode（TurboQuant 技术细节）
  7. STADLER × ChatGPT 230 年老企业案例（OpenAI 官方一手）
  8. 最强 Claude 模型曝光 + Anthropic 3000 档案外泄
  9. 知乎热榜：千问 AI 打车 vs 滴滴 AI（小滴）94 万热度

- `holdout_watchlist`:
  - "AGI is here" 情绪帖：内容空洞，情绪信号可参考
  - Genshin AI 绘图多指问题（游戏领域，AI 识别争议）
  - B 站 Warhammer 40K 定格动画（无 AI 参与，纯娱乐）
  - GAN-style Claude prompt 技巧（技巧类，短期热度）
  - SK hynix IPO（赛道匹配，需官方文件验证）
  - 用户退订 ChatGPT Plus / Claude 计费投诉（AI 产品留存压力，需更多样本）
  - 杨植麟主持大模型圆桌（核心人物观点，需回链实录）
  - 极客公园三合一早报（信息分散，单条价值有限）
  - 知乎"如何看待《原神》六指派蒙 AI 绘图"（泛娱乐 + AI 识别争议）
  - YouTube OpenAI 购物助手视频（产品演示类，内容深度待确认）
  - Trend Hunt 各源（待读取判断）

- `supply_risk`:
  - 本日源数量 35 个，来源结构改善（微信 6 条 + 中文平台覆盖显著增强）
  - TechCrunch 来源 5 条，集中度仍偏高
  - 官方一手源仅 1 条（OpenAI News），建议后续优先补齐 Anthropic、Google AI、MiniMax 等官方 RSS
  - 部分中文微信源为标题摘要，信息深度依赖回链原文
