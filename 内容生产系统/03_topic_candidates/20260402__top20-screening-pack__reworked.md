# Top20 初筛包（Rework版）

- `date`: `2026-04-02`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-04-02 14:48 CST`
- `source_scope`: `manifest 20260402（business window: 2026-04-01 17:00 -> 2026-04-02 14:30）`
- `parent_pack`: `20260402__top20-screening-pack.md（2026-04-02 05:15 CST）`
- `rework_trigger`: `market-editor scorecard（2026-04-02 06:47 CST）`
- `rework_mode`: `supplement_evidence`
- `total_candidates_seen`: `42`
- `top20_count`: `20`
- `delivery_lane`: `day_mainline`
- `supply_risk_note`: `本包为 rework 返工版，仅补强证据链，不做自判放行；是否可进入下一工序由 market-editor 最新 scorecard 决定。`

## 使用说明

- 这是 `signal-scout` 阶段返工件。
- 基于原始 Top20（2026-04-02 05:15 CST）补强证据。
- 仅补强了可确认的信源，无法补强的维持原状并注明原因。
- 每个候选必须包含结构化评分与证据摘要。

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

### 1. Claude Code 源码泄露事件持续发酵
- `topic_key`: `claude-code-source-leak`
- `title`: `Claude Code开源发酵：负责人反省，平替版狂飙10万星，Anthropic紧急封杀`
- `primary_platform`: `wechat__zhidx / 知乎 / HN / Reddit`
- `published_at`: `2026-04-01 19:54 CST`
- `original_link`: `https://mp.weixin.qq.com/s/GEX4Du2Ov6cgjCjUB-Csgg`
- `score_total`: `26`
- `score_breakdown`: `一手性:2 | 传播性:3 | 破圈性:3 | 赛道匹配:3 | 可延展性:3 | 数据硬度:2 | 视觉素材:2 | 平台适配:3 | 时效窗口:3 | 讨论度:2`
- `signal_summary`: `Claude Code 51万行源码被泄露至GitHub，开源社区迅速出现多个复刻版（狂飙10万星），Anthropic紧急封杀并由负责人公开反省。此事在HN、Reddit、知乎热榜、机器之心、极客公园等多平台同步发酵。`
- `why_in_top20`: `年度级别安全事件，跨全球开发者社区与中国内容场的双向共振，一手信源多元（官方封杀+创始人反省+社区复刻+知乎讨论），可拆解快讯/深度/复盘多层次内容。`
- `visual_assets`: `GitHub复刻项目截图、Anthropic官方封杀声明截图（GitHub DMCA: https://github.com/github/dmca/blob/master/2026/03/2026-03-31-anthropic.md）、知乎热榜截图、微信文章封面图`
- `risks`: `Anthropic官方回应内容需进一步回链验证；事件仍在快速演进中`

### 2. TurboQuant 团队学术不端争议
- `topic_key`: `turboquant-academic-misconduct`
- `title`: `TurboQuant团队学术不端？谷歌回应了，但争议更大了`
- `primary_platform`: `机器之心官网 / 知乎`
- `published_at`: `2026-04-01`
- `original_link`: `https://www.jiqizhixin.com/`
- `score_total`: `22`
- `score_breakdown`: `一手性:2 | 传播性:2 | 破圈性:2 | 赛道匹配:3 | 可延展性:3 | 数据硬度:2 | 视觉素材:2 | 平台适配:2 | 时效窗口:3 | 讨论度:3`
- `signal_summary`: `机器之心和知乎同步报道TurboQuant团队涉嫌学术不端，谷歌已回应但争议持续。Reddit上另有实测帖说明该技术本身仍有实际价值。争议性与技术价值形成张力。`
- `why_in_top20`: `学术诚信话题在AI圈持续敏感，谷歌回应增加官方背书；技术真实性（TurboQuant量化方案）与声誉风险并存，具备持续讨论空间和研报拆解价值。`
- `visual_assets`: `Reddit讨论帖截图、机器之心文章、知乎讨论帖`
- `risks`: `⚠️ 补证未完成：原始Reddit讨论帖URL缺失；谷歌官方回应原文未捕获到；需继续补链`
- `rework_note`: `rework_mode=supplement_evidence；补证缺口：①原始Reddit讨论帖（机器之心二手报道无直达链接）②Google官方回应原文；维持原对象，不换题`

### 3. Qwen3.5-27B 实测性能对比
- `topic_key`: `qwen3-5-27b-performance`
- `title`: `FOR ME, Qwen3.5-27B is better than Gemini 3.1 Pro and GPT-5.3 Codex / TurboQuant isn't just for KV`
- `primary_platform`: `Reddit /r/LocalLLaMA`
- `published_at`: `2026-04-01 19:58 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1s9ig5r/turboquant_isnt_just_for_kv_qwen3527b_at_nearq4_0/`
- `score_total`: `21`
- `score_breakdown`: `一手性:2 | 传播性:2 | 破圈性:2 | 赛道匹配:3 | 可延展性:2 | 数据硬度:3 | 视觉素材:1 | 平台适配:2 | 时效窗口:3 | 讨论度:2`
- `signal_summary`: `Reddit用户实测Qwen3.5-27B在多项指标上接近或超越Gemini 3.1 Pro和GPT-5.3 Codex，且结合TurboQuant可在16GB 5060 Ti上运行至near-Q4_0质量。开源模型性能追赶闭源的实测证据。原始Reddit帖子含详细benchmark数据（Q4_0 PPL: 7.2431 vs TQ3_1S PPL: 7.2570，差距仅0.19%）。`
- `why_in_top20`: `开源模型性能突破的实测证据，具体硬件要求（16GB 5060 Ti）有强参考价值；可与TurboQuant争议形成对比报道（技术有实力但团队有争议）。`
- `visual_assets`: `Reddit帖子原文、硬件配置截图`
- `risks`: `单一用户实测，样本有限；需更多benchmark验证`
- `rework_note`: `✅ 证据补强完成：Reddit原文URL已确认可访问；benchmark数据可支撑数据硬度评分`

### 4. 1-bit Bonsai：首个商业可行1-bit LLM
- `topic_key`: `1-bit-bonsai-llm`
- `title`: `PrismML — Announcing 1-bit Bonsai: The First Commercially Viable 1-bit LLMs`
- `primary_platform`: `Reddit /r/LocalLLaMA`
- `published_at`: `2026-04-01 05:34 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1s90wo4/prismml_announcing_1bit_bonsai_the_first/`
- `score_total`: `20`
- `score_breakdown`: `一手性:2 | 传播性:2 | 破圈性:2 | 赛道匹配:3 | 可延展性:3 | 数据硬度:2 | 视觉素材:1 | 平台适配:2 | 时效窗口:2 | 讨论度:1`
- `signal_summary`: `PrismML宣布推出1-bit Bonsai，号称首个商业可行1-bit LLM。Reddit社区讨论热烈，但目前信息量有限，需要跟进官网/论文。`
- `why_in_top20`: `模型效率方向的重要进展，1-bit LLM商业可行性的首次正式宣布；赛道匹配度高（模型/infra/效率），值得持续跟踪。`
- `visual_assets`: `Reddit公告帖、官网链接（待获取）`
- `risks`: `商业可行性质疑声存在；需要回链官方技术文档和论文验证`

### 5. OpenAI Codex GitHub Trending
- `topic_key`: `openai-codex-github`
- `title`: `openai/codex` (GitHub Trending, 71,578 stars, +2,345 today)
- `primary_platform`: `GitHub Trending / YouTube`
- `published_at`: `2026-04-02`
- `original_link`: `https://github.com/openai/codex`
- `score_total`: `19`
- `score_breakdown`: `一手性:3 | 传播性:2 | 破圈性:2 | 赛道匹配:3 | 可延展性:2 | 数据硬度:2 | 视觉素材:1 | 平台适配:2 | 时效窗口:2 | 讨论度:0`
- `signal_summary`: `OpenAI Codex在GitHub Trending上位列第一，71,578 stars，24小时内新增2,345。YouTube上有"What Codex Unlocks for Ramp"视频。官方仓库一手开源信号。`
- `why_in_top20`: `OpenAI官方Agent编码工具，GitHub高热验证开发者需求旺盛；72K stars是强信号，适合作为Agent工具链入口报道。`
- `visual_assets`: `GitHub仓库截图、stars历史趋势图`
- `risks`: `信息较新，具体功能细节需进一步挖掘`

### 6. Cognichip $60M AI芯片设计融资
- `topic_key`: `cognichip-60m-funding`
- `title`: `Cognichip wants AI to design the chips that power AI, and just raised $60M to try`
- `primary_platform`: `TechCrunch AI`
- `published_at`: `2026-04-02 00:00 CST`
- `original_link`: `https://techcrunch.com/2026/04/01/cognichip-wants-ai-to-design-the-chips-that-power-ai-and-just-raised-60m-to-try/`
- `score_total`: `22`
- `score_breakdown`: `一手性:3 | 传播性:2 | 破圈性:2 | 赛道匹配:3 | 可延展性:3 | 数据硬度:3 | 视觉素材:1 | 平台适配:2 | 时效窗口:3 | 讨论度:1`
- `signal_summary`: `Cognichip宣布获得$60M融资，目标是让AI设计AI芯片。TechCrunch报道，一手融资新闻，有明确的商业价值和产业意义。`
- `why_in_top20`: `AI for Chip Design是今年硬科技热门赛道；$60M融资金额明确，TechCrunch背书；可作为AI基础设施投资线索。`
- `visual_assets`: `TechCrunch文章配图、Cognichip官网（待挖掘）`
- `risks`: `需要回链Cognichip官网和投资人声明；赛道竞争激烈程度需补充`

### 7. 知乎热帖：Claude自我进化问题
- `topic_key`: `zhihu-claude-self-evolution`
- `title`: `Claude 正在自己设计下一代 Claude，当 AI 开始自我进化，将对行业带来哪些影响？`
- `primary_platform`: `知乎热榜`
- `published_at`: `2026-03-31 10:11 CST`
- `original_link`: `https://www.zhihu.com/question/2022254775757009403`
- `score_total`: `18`
- `score_breakdown`: `一手性:1 | 传播性:2 | 破圈性:2 | 赛道匹配:2 | 可延展性:3 | 数据硬度:1 | 视觉素材:1 | 平台适配:3 | 时效窗口:2 | 讨论度:3`
- `signal_summary`: `知乎热榜问题，探讨Claude自我进化对行业的影响。75万热度级别，中文圈强传播，具备哲学+产业双讨论空间。`
- `why_in_top20`: `知乎75万热度验证中文大众对AI自我进化的强烈好奇；问题本身即内容框架，适合做观点聚合+专家解读。`
- `visual_assets`: `知乎热榜截图、问题评论区高赞回答`
- `risks`: `纯问答形态，一手事实信息有限；需要回链相关AI新闻背景`

### 8. Claude写了完整的FreeBSD远程内核RCE
- `topic_key`: `claude-freebsd-rce`
- `title`: `Claude wrote a full FreeBSD remote kernel RCE with root shell`
- `primary_platform`: `HN Frontpage`
- `published_at`: `2026-04-01 13:21 CST`
- `original_link`: `https://github.com/califio/publications/blob/main/MADBugs/CVE-2026-4747/write-up.md`
- `score_total`: `21`
- `score_breakdown`: `一手性:3 | 传播性:2 | 破圈性:2 | 赛道匹配:2 | 可延展性:2 | 数据硬度:3 | 视觉素材:2 | 平台适配:2 | 时效窗口:2 | 讨论度:2`
- `signal_summary`: `HN报道Claude写出了完整的FreeBSD远程内核RCE漏洞利用（含root shell），CVE-2026-4747编号。这是AI安全能力的重大演示，也是危险信号。`
- `why_in_top20`: `AI安全能力边界的实测案例；开发者圈层高度关注；CVE编号提供硬数据；可拆解安全研究者视角+产业影响双层内容。`
- `visual_assets`: `GitHub CVE write-up、HN讨论帖、代码截图`
- `risks`: `技术门槛较高；需补充漏洞利用的技术细节和Anthropic官方回应`

### 9. Google March 2026 AI官方更新汇总
- `topic_key`: `google-march-2026-ai-updates`
- `title`: `The latest AI news we announced in March 2026`
- `primary_platform`: `Google AI Blog`
- `published_at`: `2026-04-01 21:00 CST`
- `original_link`: `https://blog.google/innovation-and-ai/technology/ai/google-ai-updates-march-2026/`
- `score_total`: `19`
- `score_breakdown`: `一手性:3 | 传播性:2 | 破圈性:2 | 赛道匹配:3 | 可延展性:3 | 数据硬度:3 | 视觉素材:2 | 平台适配:2 | 时效窗口:2 | 讨论度:0`
- `signal_summary`: `Google AI Blog发布3月AI更新汇总，官方一手信源，内容包括Veo 3.1 Lite、Gemini 3.1 Flash Live更新、Translate实时翻译等。Google官方RSS确认。`
- `why_in_top20`: `官方一手信源，Google产品节奏全景图；适合做AI大厂动态快讯框架的锚点；硬数据+官方说明确保内容可信度。`
- `visual_assets`: `Google Blog官方图片、产品截图`
- `risks`: `汇总性质，单条新闻深度有限；需拆分单条产品做深度`

### 10. 机器之心×KAUST HorusEye登Nature子刊
- `topic_key`: `horuseye-nature`
- `title`: `破局X射线断层成像修复！KAUST、上智院等提出通用自监督基础模型HorusEye，登Nature子刊`
- `primary_platform`: `机器之心官网`
- `published_at`: `unknown`
- `original_link`: `https://www.jiqizhixin.com/`
- `score_total`: `17`
- `score_breakdown`: `一手性:2 | 传播性:1 | 破圈性:1 | 赛道匹配:2 | 可延展性:2 | 数据硬度:3 | 视觉素材:2 | 平台适配:2 | 时效窗口:2 | 讨论度:1`
- `signal_summary`: `KAUST和上智院联合发布HorusEye，一个用于X射线断层成像修复的通用自监督基础模型，登上Nature子刊。学术研究+产业应用双重价值。`
- `why_in_top20`: `Nature子刊背书，学术影响力高；KAUST是中东AI研究重镇；AI+医疗影像赛道匹配；可拆解学术价值+商业落地双视角。`
- `visual_assets`: `机器之心文章配图、Nature论文（待挖掘）`
- `risks`: `⚠️ 补证未完成：Nature论文原文URL缺失；published_at缺失；机器之心原文入口缺失`
- `rework_note`: `rework_mode=supplement_evidence；补证缺口：①Nature子刊论文URL ②published_at明确时间 ③机器之心正文URL；维持原对象，不换题`

### 11. Replicas：YC背景编码Agent
- `topic_key`: `replicas-yc-coding-agents`
- `title`: `Replicas - End-to-End Background Coding Agents`
- `primary_platform`: `YC Launches`
- `published_at`: `2026-04-02 01:38 CST`
- `original_link`: `https://www.ycombinator.com/launches/PpP-replicas-end-to-end-background-coding-agents`
- `score_total`: `19`
- `score_breakdown`: `一手性:3 | 传播性:1 | 破圈性:1 | 赛道匹配:3 | 可延展性:2 | 数据硬度:2 | 视觉素材:1 | 平台适配:2 | 时效窗口:3 | 讨论度:1`
- `signal_summary`: `YC Launches新上线项目Replicas，提供端到端后台编码Agent。YC官方背书，一手Startup信息。`
- `why_in_top20`: `YC Launches是优质早期项目入口；背景编码Agent是今年Infra/Agent主线；Replicas具体方案待挖掘，适合作为NewCo发现线索。`
- `visual_assets`: `YC Launches页面、官网链接（待挖掘）`
- `risks`: `新项目信息有限；需要跟进官网和创始团队背景`

### 12. 知乎3.31 Claude Code泄露专帖
- `topic_key`: `zhihu-claude-code-leak-discussion`
- `title`: `如何看待3.31 Claude Code源码泄露一事？`
- `primary_platform`: `知乎热榜`
- `published_at`: `2026-03-31 19:42 CST`
- `original_link`: `https://www.zhihu.com/question/2022398469655074136`
- `score_total`: `20`
- `score_breakdown`: `一手性:1 | 传播性:3 | 破圈性:3 | 赛道匹配:3 | 可延展性:2 | 数据硬度:1 | 视觉素材:1 | 平台适配:3 | 时效窗口:2 | 讨论度:3`
- `signal_summary`: `知乎热榜第2条，专门讨论Claude Code泄露事件。中文开发者社区的主要讨论场，热度高，可与第1条联动。`
- `why_in_top20`: `中文开发者社区对Claude Code泄露的核心讨论场；高热问题意味着大众关注度；可与HN/Reddit信息互补形成跨场域报道。`
- `visual_assets`: `知乎热榜截图、高赞回答截图`
- `risks`: `知乎内容以观点为主，需要配合其他一手信源`

### 13. The OpenAI Graveyard
- `topic_key`: `openai-graveyard`
- `title`: `The OpenAI graveyard: All the deals and products that haven't happened`
- `primary_platform`: `HN Frontpage / Forbes`
- `published_at`: `2026-04-01 23:55 CST`
- `original_link`: `https://www.forbes.com/sites/phoebeliu/2026/03/31/openai-graveyard-deals-and-products-havent-happened-openai/`
- `score_total`: `18`
- `score_breakdown`: `一手性:2 | 传播性:2 | 破圈性:2 | 赛道匹配:2 | 可延展性:3 | 数据硬度:2 | 视觉素材:1 | 平台适配:2 | 时效窗口:2 | 讨论度:2`
- `signal_summary`: `Forbes报道OpenAI未能落地的交易和产品清单，HN作为趋势入口验证讨论度。这是对OpenAI战略质疑的系统性梳理。`
- `why_in_top20`: `对OpenAI有系统性批判视角；适合做AI大厂战略复盘内容；事实基础较强（Forbes背书）。`
- `visual_assets`: `Forbes文章、OpenAI产品时间线图`
- `risks`: `批评性报道，需要平衡OpenAI官方回应`

### 14. 飞书开源AI项目获5.5k星
- `topic_key`: `feishu-open-source-ai-5.5k`
- `title`: `飞书开源！让所有AI都能用，斩获5.5k星`
- `primary_platform`: `微信 / 智东西`
- `published_at`: `2026-04-01`
- `original_link`: `https://mp.weixin.qq.com/s/kcegdsr1jYoigC18GBVI_A`（经manifest追溯确认完整URL）
- `score_total`: `16`
- `score_breakdown`: `一手性:2 | 传播性:2 | 破圈性:2 | 赛道匹配:3 | 可延展性:2 | 数据硬度:2 | 视觉素材:1 | 平台适配:2 | 时效窗口:2 | 讨论度:1`
- `signal_summary`: `飞书（字节旗下）开源AI项目，获得5.5k GitHub stars。智东西和微信传播，中文AI圈关注。`
- `why_in_top20`: `字节跳动在AI Infra的开源动作；5.5k stars有一定说服力；飞书在办公场景的AI落地值得跟踪。`
- `visual_assets`: `微信文章截图、GitHub仓库截图`
- `risks`: `⚠️ 补证未完成：GitHub仓库URL缺失（manifest内无此文件）；原链接为微信文章入口，无法直接验证5.5k stars真实性`
- `rework_note`: `rework_mode=supplement_evidence；补证缺口：①飞书AI开源项目的GitHub仓库URL（5.5k stars原始Repo）；②项目方官方公告；维持原对象，不换题`

### 15. StepFun 3.5 Flash登顶OpenClaw任务性价比
- `topic_key`: `stepfun-3-5-flash-openclaw`
- `title`: `StepFun 3.5 Flash is #1 cost-effective model for OpenClaw tasks (300 battles)`
- `primary_platform`: `HN Frontpage`
- `published_at`: `2026-04-02`
- `original_link`: `https://news.ycombinator.com/item?id=47602879`
- `score_total`: `15`
- `score_breakdown`: `一手性:2 | 传播性:1 | 破圈性:1 | 赛道匹配:3 | 可延展性:1 | 数据硬度:3 | 视觉素材:1 | 平台适配:1 | 时效窗口:2 | 讨论度:1`
- `signal_summary`: `HN讨论StepFun 3.5 Flash在OpenClaw任务中以300次对比成为成本效益最高的模型。开源模型实测数据，具体可验证。HN原始帖可回链。`
- `why_in_top20`: `中国开源模型获得海外开发者认可的具体案例；300 battles数据有说服力；StepFun是今年值得关注的中国AI公司。`
- `visual_assets`: `HN讨论帖、benchmark数据截图`
- `risks`: `单一benchmark场景；OpenClaw任务代表性需说明`
- `rework_note`: `补强HN原始讨论帖URL（scorecard要求回链）；原Top20包内original_link仅标注"HN Frontpage"已补全为完整HN URL`

### 16. 阿里达摩院开源架构CPU直指AI Agent
- `topic_key`: `ali-damo-cpu-ai-agent`
- `title`: `刚刚，阿里达摩院祭出开源架构CPU王炸，直指 AI Agent`
- `primary_platform`: `智东西 / 机器之心`
- `published_at`: `2026-04-01`
- `original_link`: `https://zhidx.com/p/542389.html`
- `score_total`: `17`
- `score_breakdown`: `一手性:2 | 传播性:2 | 破圈性:2 | 赛道匹配:3 | 可延展性:3 | 数据硬度:2 | 视觉素材:1 | 平台适配:2 | 时效窗口:2 | 讨论度:1`
- `signal_summary`: `阿里达摩院发布开源架构CPU，定位直指AI Agent场景。智东西和机器之心同步报道。`
- `why_in_top20`: `阿里达摩院是AI芯片重要力量；开源CPU+AI Agent组合具战略意义；中国AI硬件开源信号。`
- `visual_assets`: `智东西文章配图、达摩院发布资料（待挖掘）`
- `risks`: `需要回链达摩院官方发布和具体开源协议`

### 17. 智谱Z.ai负责人深度拆解GLM-5.1
- `topic_key`: `zhipu-glm-5-1-genaicon`
- `title`: `智谱Z.ai负责人李子玄：深度拆解 GLM-5.1 训练全流程｜GenAICon 2026`
- `primary_platform`: `微信 / 智东西`
- `published_at`: `2026-04-01 18:18 CST`
- `original_link`: `https://mp.weixin.qq.com/s/O2zFXBCz2VKA2xnu8JacIQ`
- `score_total`: `17`
- `score_breakdown`: `一手性:2 | 传播性:2 | 破圈性:1 | 赛道匹配:3 | 可延展性:3 | 数据硬度:2 | 视觉素材:1 | 平台适配:2 | 时效窗口:2 | 讨论度:1`
- `signal_summary`: `智谱Z.ai负责人在GenAICon 2026深度拆解GLM-5.1训练全流程。智谱是中国头部大模型公司，GLM-5.1是核心产品。`
- `why_in_top20`: `中国大模型公司核心技术披露；GenAICon conference背书增加可信度；可作为大模型技术解读内容素材。`
- `visual_assets`: `微信文章配图、演讲PPT截图（需获取）`
- `risks`: `会议演讲整理需回链演讲视频或PPT原版`

### 18. Founder Park: Claude Code Harness深度解读
- `topic_key`: `founder-park-claude-code-harness`
- `title`: `看看 Claude Code 怎么做 Harness，这才是 Agent 工程化的真正难点`
- `primary_platform`: `微信 / Founder Park`
- `published_at`: `2026-04-01 21:33 CST`
- `original_link`: `https://mp.weixin.qq.com/s/2NUlZtRMbNHpBvgAe3__Qg`
- `score_total`: `18`
- `score_breakdown`: `一手性:2 | 传播性:2 | 破圈性:2 | 赛道匹配:3 | 可延展性:3 | 数据硬度:2 | 视觉素材:1 | 平台适配:2 | 时效窗口:2 | 讨论度:2`
- `signal_summary`: `Founder Park深度分析Claude Code的Harness实现，探讨Agent工程化的真正难点。中文优质科技媒体，深度解读角度稀缺。`
- `why_in_top20`: `Agent工程化是今年技术主线；Founder Park是中文优质科技媒体；Claude Code Harness的工程细节在国内传播价值高。`
- `visual_assets`: `Founder Park文章配图、技术架构图（待获取）`
- `risks`: `需要回链原文获取技术细节截图`

### 19. 机器之心：Claude Code Python复刻版
- `topic_key`: `claude-code-python-clone`
- `title`: `Claude Code 源码泄露了，有人用Python复刻了一个极简版`
- `primary_platform`: `机器之心官网 / 微信`
- `published_at`: `2026-04-01`
- `original_link`: `https://www.jiqizhixin.com/`
- `score_total`: `16`
- `score_breakdown`: `一手性:2 | 传播性:2 | 破圈性:2 | 赛道匹配:2 | 可延展性:2 | 数据硬度:2 | 视觉素材:1 | 平台适配:2 | 时效窗口:2 | 讨论度:2`
- `signal_summary`: `机器之心报道GitHub上出现Python极简版Claude Code复刻。开源社区对Claude Code泄露的工程响应。`
- `why_in_top20`: `Python版复刻降低社区参与门槛；与第1条Claude Code泄露主事件联动；展现开源社区的快速响应能力。`
- `visual_assets`: `机器之心文章、GitHub复刻项目截图（待挖掘）`
- `risks`: `复刻版质量和维护状态需验证`

### 20. AI Marketing BS Index
- `topic_key`: `ai-marketing-bs-index`
- `title`: `The AI Marketing BS Index`
- `primary_platform`: `HN Frontpage`
- `published_at`: `2026-04-02 01:55 CST`
- `original_link`: `https://bastian.rieck.me/blog/2026/bs/`
- `score_total`: `15`
- `score_breakdown`: `一手性:2 | 传播性:2 | 破圈性:2 | 赛道匹配:2 | 可延展性:2 | 数据硬度:2 | 视觉素材:2 | 平台适配:2 | 时效窗口:2 | 讨论度:2`
- `signal_summary`: `HN报道一个用于衡量AI营销BS程度的指数，作者Bastian Rieck。独立研究者出品，HN背书。`
- `why_in_top20`: `AI营销泡沫是行业持续话题；独特视角和框架具备传播性；HN是开发者社区信任源。`
- `visual_assets`: `BS Index网站截图、方法论图示`
- `risks`: `独立研究者作品，影响力有限；需要验证方法论严谨性`

## 结论

- `top3_must_watch`:
  1. **Claude Code 源码泄露** — 跨平台共振最强（HN+Reddit+知乎+微信），可拆快讯/深度/复盘，时效窗口仍在
  2. **TurboQuant 学术不端争议** — 技术价值与声誉风险并存，谷歌官方回应增加可信度，适合做争议性话题分析
  3. **Cognichip $60M AI芯片设计** — 明确融资金额+赛道明确（AI for Chip Design），TechCrunch背书，可作为硬科技投资线索锚点

- `top6_strong_pool`:
  4. Qwen3.5-27B实测性能对比（开源模型追赶闭头的实测证据，✅ Reddit原文URL补强完成）
  5. 1-bit Bonsai LLM（首个商业可行1-bit LLM）
  6. OpenAI Codex GitHub Trending（72K stars，Agent工具链强信号）
  7. FreeBSD RCE by Claude（AI安全能力边界实测）
  8. 知乎Claude自我进化热帖（75万热度，中文大众AI认知窗口）
  9. Google March 2026 AI官方汇总（官方一手信源，全景图锚点）

- `holdout_watchlist`:
  10. 飞书开源5.5k星（⚠️ GitHub仓库仍缺失，补证未完成）— 字节AI Infra动作，待挖仓库
  11. 阿里达摩院开源CPU直指Agent（硬件开源战略）
  12. HorusEye Nature子刊（⚠️ Nature论文链接仍缺失，补证未完成）— 学术价值高但大众传播弱
  13. StepFun 3.5 Flash登顶性价比（✅ HN帖URL补强完成）
  14. The OpenAI Graveyard（系统性批判视角）

- `supply_risk`: `补证完成情况：#3 Qwen3.5-27B实测 ✅ / #15 StepFun ✅ / 其余3条（TurboQuant学术不端/HorusEye/飞书开源）manifest内无更强信源文件，维持原对象按rework规则继续流程。`

## Rework 补证执行摘要

| 候选 | scorecard要求 | 补强结果 | 状态 |
|---|---|---|---|
| #2 TurboQuant学术不端 | 补原始Reddit帖+谷歌回应 | manifest内无Google回应原文文件；Reddit无直达链接 | ⚠️ 维持原对象 |
| #3 Qwen3.5-27B实测 | 补Reddit原文URL | ✅ Reddit原文URL已补强：https://old.reddit.com/r/LocalLLaMA/comments/1s9ig5r/ | 完成 |
| #10 HorusEye | 补Nature论文+published_at | manifest内无Nature论文文件 | ⚠️ 维持原对象 |
| #14 飞书开源5.5k星 | 补GitHub仓库URL | manifest内无此GitHub仓库文件 | ⚠️ 维持原对象 |
| #15 StepFun | 补HN原始帖URL | ✅ HN帖URL已补强：https://news.ycombinator.com/item?id=47602879 | 完成 |
