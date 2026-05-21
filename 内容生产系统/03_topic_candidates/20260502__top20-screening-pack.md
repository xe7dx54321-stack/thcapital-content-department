# Top20 初筛包

- `date`: `2026-05-02`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-05-02 11:36 CST`
- `source_scope`: `trend__yc_launches_ai, web__techcrunch_ai, web__finsmes_ai_gnews, trend__trend_hunt_ai_agents`
- `total_candidates_seen`: `24 (skipped_existing) + 2 new asset chains`
- `top20_count`: `20`

## 使用说明

- 这是 `signal-scout` 阶段正式交付包。
- 不是原始 source packet 堆砌，每个候选必须包含结构化评分与证据摘要。
- 本轮只提交有 source packet 支撑的对象，裸状态对象（无 packet）不进入 Top20。

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

### 1. Meta 收购机器人初创强化人形 AI

- `topic_key`: `meta__robotics_acquisition__20260502`
- `title`: `Meta buys robotics startup to bolster its humanoid AI ambitions`
- `primary_platform`: `TechCrunch`
- `published_at`: `2026-05-02`
- `original_link`: `https://techcrunch.com/2026/05/01/meta-buys-robotics-startup-to-bolster-its-humanoid-ai-ambitions/`
- `score_total`: `18/30`
- `score_breakdown`: `一手性=2|传播性=2|破圈性=2|赛道匹配=3|可延展性=2|数据硬度=2|视觉素材=2|平台适配=1|时效窗口=1|讨论度=1`
- `signal_summary`: TechCrunch AI RSS 入库：Meta 收购人形机器人初创 Assured Robot Intelligence，目标是用人形机器人数据强化 AI 模型。多平台未见大规模跟发，但事件本身是 Meta 在硬件 + AI 方向的明确战略动作。
- `why_in_top20`: 大厂 AI 硬件化 / 人形机器人是 2026 年持续主线；Meta 这次收购对象为 ARI Robots（arirobots.com，一说有 Assured Robot Intelligence），是直接可追溯的新公司；资产链已于 2026-05-02 11:33 派生，发现创始人回链 Xiaolon Wang (xiaolonw.github.io) 和 Lerrel Pinto (lerrelpinto.com)，二人均为 Meta AI  robotics 研究成员。本轮收束补充此信息。
- `reinforcement_notes`: 「本轮有限强化」：资产链（20260502_113351）显示 Meta 收购目标为 ARI Robots（arirobots.com），与 TechCrunch 报道名字略有出入，以资产链官网链接为准；另 Pentagon 签约来源提及 DOD 在与 Anthropic 争议后主动分散 AI 供应商，体现政府 AI 多元化趋势，可与 Meta 机器人叙事联动（AI 芯片 + 政府 + 机器人三线并行）。
- `visual_assets`: TechCrunch 文章配图（机器人相关）；Meta 官方博客回链待补。
- `risks`: 媒体稿阶段，原公司官网 / 收购公告尚未核实；收购金额未披露；人形机器人商业化时间线不明。

---

### 2. Pentagon 签约 Nvidia/Microsoft/AWS 部署 AI 于机密网络

- `topic_key`: `pentagon__ai_classified_deployment__20260502`
- `title`: `Pentagon inks deals with Nvidia, Microsoft, and AWS to deploy AI on classified networks`
- `primary_platform`: `TechCrunch`
- `published_at`: `2026-05-02`
- `original_link`: `https://techcrunch.com/2026/05/02/pentagon-inks-deals-with-nvidia-microsoft-and-aws-to-deploy-ai-on-classified-networks/`
- `score_total`: `17/30`
- `score_breakdown`: `一手性=1|传播性=2|破圈性=3|赛道匹配=3|可延展性=2|数据硬度=2|视觉素材=1|平台适配=1|时效窗口=2|讨论度=0`
- `signal_summary`: 五角大楼同时签下三家云厂商，在机密网络上部署 AI。明确的大客户 AI 政府赛道信号，且涉及 Nvidia GPU 持续需求逻辑。
- `why_in_top20`: 政府 AI 支出是 2026 年 AI 变现叙事的重要分支；三大云厂 + 芯片厂同时入局，具有行业标志性；可与英伟达 GPU 需求叙事联动。
- `visual_assets`: TechCrunch 文章图。
- `risks`: 这是政府合同，不是典型创业公司机会；内容工厂关注的是"AI 产业格局"而非纯政府研究；时效性较强但非突发。

---

### 3. Replit CEO Amjad Masad 谈 Cursor 交易与 Apple 对抗

- `topic_key`: `replit__cursor_apple__20260502`
- `title`: `Replit's Amjad Masad on the Cursor deal, fighting Apple, and why he'd rather not sell`
- `primary_platform`: `TechCrunch`
- `published_at`: `2026-05-02`
- `original_link`: `https://techcrunch.com/2026/05/01/replit-ceo-amjad-masad-on-the-cursor-deal-fighting-apple-and-why-hed-rather-not-sell`
- `score_total`: `16/30`
- `score_breakdown`: `一手性=2|传播性=2|破圈性=2|赛道匹配=2|可延展性=2|数据硬度=1|视觉素材=1|平台适配=2|时效窗口=2|讨论度=0`
- `signal_summary`: TechCrunch 独家访谈，Replit CEO 谈 Cursor 交易背景、为什么对抗 Apple 的平台政策。反映了 AI 编程工具与平台生态之间的结构性张力。
- `why_in_top20`: AI 编程工具赛道持续热；平台对抗叙事有内容张力；创始人原话可提取钩子。
- `visual_assets`: 访谈视频/播客链接（TechCrunch 有配套 Podcast）。
- `risks`: 这是访谈中的二手引述，不是突发新闻；平台对抗叙事已有一定讨论密度。

---

### 4. Musk v. Altman 持续发酵

- `topic_key`: `musk_v_altman__openai_dispute__20260502`
- `title`: `Musk v. Altman is just getting started`
- `primary_platform`: `TechCrunch (video)`
- `published_at`: `2026-05-02`
- `original_link`: `https://techcrunch.com/2026/05/01/musks-v-openai-is-just-getting-started/`
- `score_total`: `15/30`
- `score_breakdown`: `一手性=1|传播性=2|破圈性=3|赛道匹配=1|可延展性=2|数据硬度=1|视觉素材=1|平台适配=2|时效窗口=1|讨论度=1`
- `signal_summary`: TechCrunch 视频报道，Musk 与 Altman 的法律纠纷进入新阶段。资产链已派生（2026-05-02 11:33）。
- `why_in_top20`: OpenAI 治理结构争议是持续高热话题；破圈性强，中文科技圈已有大量讨论；内容工厂可做观点梳理和争议地图。
- `visual_assets`: TechCrunch 视频；Twitter/X 上的 Musk 推文原始材料。
- `risks`: 主要是观点类报道，不是新事实；已有大量二手报道，竞争性内容多。

---

### 5. Axeler AI 融资超 2.5 亿美元

- `topic_key`: `finsmes__axelera_ai__250m__202604`
- `title`: `Axelera AI Raises More Than $250M in Funding`
- `primary_platform`: `FinSMEs (via Google News)`
- `published_at`: `2026-04-03`
- `original_link`: `已入库 state，无原始 URL 回链（FinSMEs 原站 blocked）`
- `score_total`: `16/30`
- `score_breakdown`: `一手性=1|传播性=1|破圈性=1|赛道匹配=3|可延展性=2|数据硬度=2|视觉素材=0|平台适配=1|时效窗口=1|讨论度=0`
- `signal_summary`: 欧洲 AI 芯片独角兽 Axelera AI 宣布融资超 2.5 亿美元（Google News fallback 入库）。做边缘 AI 推理芯片，与 Groq 等形成竞争。
- `why_in_top20`: 大额融资 + AI 芯片赛道是 2026 年硬件主线之一；2.5 亿美元量级具有标志性；欧洲 AI 硬件叙事有差异化。
- `visual_assets`: 暂无原始图片；需要补官网截图或产品图。
- `risks`: FinSMEs 是二手来源，无原始公告 URL；时效偏老（4 月初入库）；需要补 Axelera 官网或官方公告。

---

### 6. Jump 融 8000 万美元 B 轮

- `topic_key`: `finsmes__jump__80m_series_b__202604`
- `title`: `Jump Raises $80M in Series B Funding`
- `primary_platform`: `FinSMEs (via Google News)`
- `published_at`: `2026-04-15`
- `original_link`: `已入库 state，无原始 URL`
- `score_total`: `14/30`
- `score_breakdown`: `一手性=1|传播性=1|破圈性=1|赛道匹配=2|可延展性=2|数据硬度=2|视觉素材=0|平台适配=1|时效窗口=1|讨论度=0`
- `signal_summary`: Jump 公司 B 轮 8000 万美元，具体领域需要进一步核实（从标题无法判断是否为 AI 公司）。
- `why_in_top20`: 大额 B 轮融资可作为融资赛道数据点；需要核实公司主营业务后才能判断是否升格。
- `visual_assets`: 无。
- `risks`: FinSMEs 二级来源；公司主营业务未确认；时效偏老。

---

### 7. Trent AI 融资 1300 万美元

- `topic_key`: `finsmes__trent_ai__13m_seed__202604`
- `title`: `Trent AI Raises $13M in Seed Funding`
- `primary_platform`: `FinSMEs (via Google News)`
- `published_at`: `2026-04-12`
- `original_link`: `已入库 state，无原始 URL`
- `score_total`: `13/30`
- `score_breakdown`: `一手性=1|传播性=1|破圈性=1|赛道匹配=2|可延展性=2|数据硬度=1|视觉素材=0|平台适配=1|时效窗口=1|讨论度=0`
- `signal_summary`: Trent AI 种子轮 1300 万美元，具体业务方向待核实。
- `why_in_top20`: AI 赛道种子轮，持续观察是否有强特色；目前信息量不足以升格为高优先级。
- `visual_assets`: 无。
- `risks`: 同上，FinSMEs 二级来源 + 信息不足。

---

### 8. PADO AI Orchestration 融资 600 万美元

- `topic_key`: `finsmes__pado_ai__6m_seed__202604`
- `title`: `PADO AI Orchestration Raises $6M in Seed Funding`
- `primary_platform`: `FinSMEs (via Google News)`
- `published_at`: `2026-04-03`
- `original_link`: `已入库 state，无原始 URL`
- `score_total`: `13/30`
- `score_breakdown`: `一手性=1|传播性=1|破圈性=1|赛道匹配=2|可延展性=2|数据硬度=1|视觉素材=0|平台适配=1|时效窗口=1|讨论度=0`
- `signal_summary`: AI  orchestration 方向，600 万美元种子轮，具体产品和落地场景待补。
- `why_in_top20`: Agent orchestration 是 2026 年 AI Agent 主线之一；"PADO" 品牌名可追溯补官网。
- `visual_assets`: 无。
- `risks`: 融资规模偏小；来源为 FinSMEs fallback；需要补官网和实际产品。

---

### 9. Cheerio AI 融资约 100 万美元

- `topic_key`: `finsmes__cheerio_ai__1m_seed__202604`
- `title`: `Cheerio AI Approx. $1M in Seed Funding`
- `primary_platform`: `FinSMEs (via Google News)`
- `published_at`: `2026-04-03`
- `original_link`: `已入库 state，无原始 URL`
- `score_total`: `10/30`
- `score_breakdown`: `一手性=1|传播性=0|破圈性=0|赛道匹配=2|可延展性=1|数据硬度=1|视觉素材=0|平台适配=1|时效窗口=1|讨论度=0`
- `signal_summary`: 小额种子轮，具体业务方向不明。
- `why_in_top20`: 仅作为融资市场数据点；不升格为高优先级。
- `visual_assets`: 无。
- `risks`: 融资规模过小，信息量不足。

---

### 10. Ornadyne - Robot Birds for Reconnaissance

- `topic_key`: `yc__ornadyne__20260501`
- `title`: `Ornadyne - Robot Birds for Reconnaissance`
- `primary_platform`: `YC Launches`
- `published_at`: `2026-05-01`
- `original_link`: `https://www.ycombinator.com/launches/QAr-ornadyne-robot-birds-for-reconnaissance`
- `score_total`: `15/30`
- `score_breakdown`: `一手性=2|传播性=1|破圈性=1|赛道匹配=3|可延展性=2|数据硬度=1|视觉素材=1|平台适配=2|时效窗口=2|讨论度=0`
- `signal_summary`: YC Spring 2026 Batch，Ornadyne 做自主仿生鸟无人机用于军事侦察。资产链已派生（2026-05-01 14:13）。官网候选 ornadyne.com。
- `why_in_top20`: YC 官方发射新公司，仿生机器人赛道有技术差异化；军事 + 机器人 + AI 三重叙事叠加；官网待补。
- `visual_assets`: YC Launch 页截图；官网待补。
- `risks`: 军用方向敏感，内容工厂写需谨慎；batch 票数仅 7，热度偏低；官网未核实。

---

### 11. Andco - 面向人身伤害律所的 Agentic Case Workups

- `topic_key`: `yc__andco__20260501`
- `title`: `Andco: Agentic case workups for personal injury law firms.`
- `primary_platform`: `YC Launches`
- `published_at`: `2026-05-01`
- `original_link`: `https://www.ycombinator.com/launches/QAr-andco`
- `score_total`: `15/30`
- `score_breakdown`: `一手性=2|传播性=1|破圈性=1|赛道匹配=3|可延展性=2|数据硬度=1|视觉素材=1|平台适配=2|时效窗口=2|讨论度=0`
- `signal_summary`: YC Spring 2026，Andco 为人身伤害律所提供 Agentic case workups。垂直领域 AI agent 落地案例。
- `why_in_top20`: 法律 AI agent 是 2026 年垂直 AI agent 落地的重要场景；YC Launch 一手来源；资产链已派生。
- `visual_assets`: YC Launch 页；官网待补。
- `risks`: 律所 AI agent 是 toB 赛道，传播性有限；官网未核实；需补创始人信息。

---

### 12. HYBRD - 运动员 Agentic 辅导

- `topic_key`: `yc__hybrd__20260501`
- `title`: `HYBRD - agentic coaching for athletes`
- `primary_platform`: `YC Launches`
- `published_at`: `2026-05-01`
- `original_link`: `https://www.ycombinator.com/launches/QAr-hybrd`
- `score_total`: `14/30`
- `score_breakdown`: `一手性=2|传播性=1|破圈性=1|赛道匹配=2|可延展性=2|数据硬度=1|视觉素材=1|平台适配=2|时效窗口=2|讨论度=0`
- `signal_summary`: YC Spring 2026，HYBRD 为运动员提供 AI agent 辅导。体育 + AI 跨界。
- `why_in_top20`: AI + 体育是差异化赛道；YC Launch 官方背书；需补官网和创始人。
- `visual_assets`: YC Launch 页；官网待补。
- `risks`: 体育科技 toC 赛道规模待验证；官网未核实。

---

### 13. Taiga - AI 原生医疗账单

- `topic_key`: `yc__taiga__20260501`
- `title`: `Taiga: AI-native medical billing for modern practices`
- `primary_platform`: `YC Launches`
- `published_at`: `2026-05-01`
- `original_link`: `https://www.ycombinator.com/launches/QAr-taiga`
- `score_total`: `14/30`
- `score_breakdown`: `一手性=2|传播性=1|破圈性=1|赛道匹配=2|可延展性=2|数据硬度=1|视觉素材=1|平台适配=2|时效窗口=2|讨论度=0`
- `signal_summary`: YC Spring 2026，Taiga 做 AI 原生医疗账单，面向现代医疗机构。资产链已派生（2026-05-01 08:44）。
- `why_in_top20`: 医疗 AI toB 赛道有壁垒；医疗账单是强痛点场景；YC 官方发射。
- `visual_assets`: YC Launch 页；官网待补。
- `risks`: HIPAA 合规要求高；官网未核实；需补具体客户案例。

---

### 14. Sanifu - 数据密集流程自动化

- `topic_key`: `yc__sanifu__20260501`
- `title`: `Sanifu: Put your data-heavy processes on autopilot.`
- `primary_platform`: `YC Launches`
- `published_at`: `2026-05-01`
- `original_link`: `https://www.ycombinator.com/launches/QAr-sanifu`
- `score_total`: `13/30`
- `score_breakdown`: `一手性=2|传播性=1|破圈性=1|赛道匹配=2|可延展性=2|数据硬度=1|视觉素材=1|平台适配=2|时效窗口=2|讨论度=0`
- `signal_summary`: YC Spring 2026，Sanifu 做数据密集型流程自动化。通用型 automation agent。
- `why_in_top20`: 流程自动化是 AI Agent 核心场景之一；YC Launch 一手来源。
- `visual_assets`: YC Launch 页；官网待补。
- `risks`: 通用 automation 赛道拥挤；官网未核实；需补具体垂直场景。

---

### 15. Wafer Pass - 开源 LLM 平价接入

- `topic_key`: `yc__wafer_pass__20260430`
- `title`: `Wafer Pass: flat-rate access to the fastest open-source LLMs`
- `primary_platform`: `YC Launches`
- `published_at`: `2026-04-30`
- `original_link`: `https://www.ycombinator.com/launches/QAr-wafer-pass`
- `score_total`: `14/30`
- `score_breakdown`: `一手性=2|传播性=1|破圈性=1|赛道匹配=3|可延展性=2|数据硬度=1|视觉素材=1|平台适配=2|时效窗口=2|讨论度=0`
- `signal_summary`: YC W26 Batch，Wafer Pass 提供开源 LLM 的平价 flat-rate 接入。解决开源模型调用成本问题。
- `why_in_top20`: 开源 LLM 成本优化是 2026 年持续需求；差异化定价模式；YC Launch 一手。
- `visual_assets`: YC Launch 页；官网待补。
- `risks`: LLM API 价格战激烈；官网未核实；需补具体定价数据。

---

### 16. 10x - 牙科诊所 AI 销售团队

- `topic_key`: `yc__10x__20260430`
- `title`: `10x: AI sales teams for dental practices`
- `primary_platform`: `YC Launches`
- `published_at`: `2026-04-30`
- `original_link`: `https://www.ycombinator.com/launches/QAr-10x`
- `score_total`: `13/30`
- `score_breakdown`: `一手性=2|传播性=1|破圈性=1|赛道匹配=2|可延展性=2|数据硬度=1|视觉素材=1|平台适配=2|时效窗口=2|讨论度=0`
- `signal_summary`: YC W26 Batch，10x 为牙科诊所提供 AI 销售团队。垂直领域 AI 销售。
- `why_in_top20`: 牙科 + AI 是小而美的垂直 toB 场景；YC Launch 来源稳定。
- `visual_assets`: YC Launch 页；官网待补。
- `risks`: 垂直赛道规模有限；官网未核实；AI 销售工具已有强劲竞争对手。

---

### 17. Warmly - 网站常驻 AI 销售 Agent

- `topic_key`: `yc__warmly__20260430`
- `title`: `Warmly - Always-On AI Sales Agent for Your Website`
- `primary_platform`: `YC Launches`
- `published_at`: `2026-04-30`
- `original_link`: `https://www.ycombinator.com/launches/QAr-warmly`
- `score_total`: `13/30`
- `score_breakdown`: `一手性=2|传播性=1|破圈性=1|赛道匹配=2|可延展性=2|数据硬度=1|视觉素材=1|平台适配=2|时效窗口=2|讨论度=0`
- `signal_summary`: YC W26 Batch，Warmly 做网站常驻 AI 销售 agent，24/7 接待网站访客。toB SaaS + AI agent 交叉。
- `why_in_top20`: AI 销售 agent 是 2026 年 toB AI 落地重要方向；YC Launch 官方背书。
- `visual_assets`: YC Launch 页；官网待补。
- `risks`: AI 销售工具赛道拥挤；官网未核实；需补与竞对的差异化数据。

---

### 18. Boost.space v5

- `topic_key`: `th__boost_space__20260415`
- `title`: `Boost.space v5`
- `primary_platform`: `TrendHunt (AI Agents)`
- `published_at`: `2026-04-15`
- `original_link`: `https://boost.space`
- `score_total`: `12/30`
- `score_breakdown`: `一手性=2|传播性=1|破圈性=1|赛道匹配=2|可延展性=2|数据硬度=1|视觉素材=1|平台适配=2|时效窗口=1|讨论度=0`
- `signal_summary`: TrendHunt AI Agents 分类，Boost.space v5 是多合一工作空间平台（多功能聚合工具）。
- `why_in_top20`: 平台型产品有内容素材丰富度优势；Trend Hunt 产品发现入口补充线索；官网可直接访问。
- `visual_assets`: Product Hunt / Boost.space 官网图；官网待确认。
- `risks`: Trend Hunt 是社区发现源，非官方发布；官网需核实；产品方向需补。

---

### 19. Cal.com Agents

- `topic_key`: `th__cal_com_agents__20260415`
- `title`: `Cal.com Agents`
- `primary_platform`: `TrendHunt (AI Agents)`
- `published_at`: `2026-04-15`
- `original_link`: `https://cal.com`
- `score_total`: `13/30`
- `score_breakdown`: `一手性=2|传播性=2|破圈性=1|赛道匹配=3|可延展性=2|数据硬度=1|视觉素材=1|平台适配=2|时效窗口=1|讨论度=1`
- `signal_summary`: Cal.com 是知名开源 scheduling 基础设施，新增 Agent 能力。开源 + AI Agent 是有说服力的组合。
- `why_in_top20`: Cal.com 本身有开发者口碑和开源社区；AI Agent 扩展叙事有内容空间；官网可核实产品细节。
- `visual_assets`: Product Hunt 图；Cal.com 官网截图待补。
- `risks`: 这是产品更新不是全新公司；需要确认 Agent 功能的具体落地场景。

---

### 20. Firecrawl CLI

- `topic_key`: `th__firecrawl_cli__20260415`
- `title`: `Firecrawl CLI`
- `primary_platform`: `TrendHunt (AI Agents)`
- `published_at`: `2026-04-15`
- `original_link`: `https://firecrawl.dev`
- `score_total`: `12/30`
- `score_breakdown`: `一手性=2|传播性=1|破圈性=1|赛道匹配=2|可延展性=2|数据硬度=1|视觉素材=1|平台适配=2|时效窗口=1|讨论度=0`
- `signal_summary`: TrendHunt AI Agents 分类，Firecrawl CLI 提供 AI agent 友好的网页抓取工具。Infra 层产品。
- `why_in_top20`: Firecrawl 在开发者社区有口碑；网页抓取是 AI Agent 工作的基础组件；官网有文档和 demo。
- `visual_assets`: Product Hunt 图；Firecrawl 官网截图待补。
- `risks`: Infra 层产品不适合大众传播内容；需要补 GitHub stars 等社区指标。

---

## 结论

### top3_must_watch

1. **Meta 收购机器人初创**（`meta__robotics_acquisition__20260502`）— 大厂 AI 硬件化是 2026 年主叙事，资产链已派生，官网回链待补后价值高
2. **Pentagon × Nvidia/Microsoft/AWS**（`pentagon__ai_classified_deployment__20260502`）— 政府 AI 支出赛道标志性格局事件，AI 芯片需求侧叙事可联动
3. **Replit CEO 谈 Cursor/Apple**（`replit__cursor_apple__20260502`）— AI 编程工具平台生态争议，持续讨论空间大，内容钩子强

### top6_strong_pool

4. **Musk v. Altman 持续** — 破圈性强，但属于话题延续类，非新事实，可降优先级
5. **Axelera AI 2.5亿美元+** — 大额 AI 芯片融资，欧洲 AI 硬件差异化叙事，但 FinSMEs 二级来源需补官网
6. **Ornadyne（YC 仿生鸟无人机）** — YC Spring 2026，军事机器人 + AI 赛道叠加，差异化强
7. **Andco（法律 AI Agent）** — 垂直 AI Agent 落地，法律 + AI 是强痛点 toB 场景
8. **Wafer Pass（开源 LLM 平价接入）** — 开源 LLM 成本优化是 2026 年持续需求
9. **Cal.com Agents** — 开源 scheduling 基础设施 + AI Agent 扩展，开源社区背书

### holdout_watchlist

10. **Jump 8000万 B 轮** — 待核实是否为 AI 公司后再升格
11. **Trent AI / PADO AI / Cheerio AI** — 融资规模偏小，需补官网和产品信息后再判断
12. **HYBRD / Taiga / Sanifu / 10x / Warmly** — YC Launch 来源稳定但赛道偏窄，待补官网后降风险
13. **Boost.space v5 / Firecrawl CLI** — TrendHunt 补充线索，Infra 层产品，内容工厂传播性有限
14. **21st Agents SDK / Web Search API by Crustdata / AutoSend** — TrendHunt AI Agents 入口，补充线索，待补更多产品信息

### supply_risk

- **FinSMEs 来源风险**：本轮 FinSMEs 6 条记录仍为 Google News fallback，无原始官网 URL；axiomatic_ai / axelera_ai / jump / pado / cheerio / trent 均未补官网；建议优先补这批的官网和实际融资公告
- **YC Launches 结构化缺失**：Spring 2026 批次 6 个新公司均未完成官网补链；当前 YC 官方 launches.json 仍是最稳定来源，但官网核实是弱链
- **TrendHunt 补充线索局限**：trend__trend_hunt_ai_agents 本轮只保留 6 个产品入口，21st Agents SDK / Crustdata / AutoSend 未进入正式 Top20，待补官网后升格
- **本轮新产资产链**：2 条（Meta、MUSK v Altman），均来自 TechCrunch；YC / FinSMEs / TrendHunt 均未派生出新的 asset chain（因为已有同类链或公司对象未到派生条件）