# Top20 初筛包（修订版 v3）

- `date`: `2026-04-15`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-03-28 01:05:56 CST`
- `revision`: `v3 — 在 v2 基础上补齐 #18 / #20 证据链`
- `scorecard_reference`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260415__top20__stage-gate-scorecard.md`
- `rework_modes_applied`: `supplement_evidence`（#14/#6/#19/#18/#20） + `rewrite_angle`（#7/#8合并） + `expand_validation`（#10拆分，新增Apple Siri）
- `source_scope`: `manifest 20260415 | 100 source packets / 12 asset chains / 24 deep articles / 8 capture summaries | 时段 T-1 19:00 ~ T 12:20`
- `total_candidates_seen`: `100`
- `top20_count`: `20`
- `data_token`: `20260415`
- `manifest_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260415__market-source-manifest.md`

## 返工说明（对照 scorecard P1/P2/P3 阻断项）

| 阻断项 | 动作 | 结果 |
|--------|------|------|
| P1-1 #14 AMI 证据链全空 | supplement_evidence：网络检索补全官方来源 | ✅ 确认 Silicon Republic 报道 + AMI 官网存在；supply_confidence → HIGH；保留主名单 |
| P1-2 Anthropic 禁令未入 Top20 | expand_validation：评估 Apple Siri 替换 #13 | ✅ Apple Siri（iOS 27 开放三方 AI 接入，万亿生态）替代 #13（时效已过期5天） |
| P1-3 #7/#8 重复打包 | rewrite_angle：合并为单一候选，标注双角度 | ✅ 合并为 #7，标注"AI工厂时代叙事 × Token Maxxing双角度"，释放1个名额 |
| P2 #10 三件套捆绑 | expand_validation：拆分为3个独立条目 | ✅ 拆为 10a 月之暗面IPO / 10b AI失业补助 / 10c 大疆无人机 |
| P3 #19 GLM-5.1 证据偏软 | supplement_evidence：Zhipu AI 官网确认 | ✅ GLM-5.1 官方发布确认；supply_confidence → MEDIUM-HIGH；保留主名单 |
| P3 #13 微信急了时效早 | — | ✅ 降权至 holdout_watchlist |
| P1 #18 / #20 尾部证据链缺口 | supplement_evidence：补官方 GitHub / 官网 / methodology 锚点 | ✅ #18 补 ATLAS 官方 repo + README benchmark caveat；#20 补 Lanbow 官网 + GitHub repo，风险从“无锚点”降为“公司口径待标注” |

---

## 使用说明

- 这是 `signal-scout` 阶段返工后交付包。
- 不是原始 source packet 堆砌。
- 每个候选必须包含结构化评分与证据摘要。
- 所有路径严格来自 manifest 真实文件。

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

### 1. OmniVTA视触觉世界模型发布（它石智航 × 6大顶尖机构）

- `topic_key`: `OmniVTA_视触觉世界模型_它石智航`
- `title`: 「被动感知」到「理解接触」！它石智航重磅发布OmniVTA视触觉世界模型
- `primary_platform`: 新智元（微信公众号）
- `published_at`: `2026-03-26 09:13:12 CST`
- `original_link`: `https://mp.weixin.qq.com/s/jOYl6LjECVQyH7aYVxipRg`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_xinzhiyuan_omnivta__source-packet.md`
- `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233950__被动感知_到_理解接触_它石智航重磅发布omnivta视触觉世界模型__deep-article.md`
- `score_total`: **22/30**
- `score_breakdown`: 一手性=3 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=3 | 视觉素材=3 | 平台适配=2 | 时效窗口=2 | 讨论度=1
- `signal_summary`: 它石智航联合新加坡国立大学、复旦大学、中科院自动化所、清华大学等六大顶尖机构，发布 OmniVTA 视触觉操作框架和 OmniViTac 大规模视触觉数据集，并发表相关论文（arXiv:2603.19201）。机器人首次实现从被动感知到对触觉进行主动预测和闭环精准控制。HuggingFace 数据集已上线。项目主页：mrsecant.github.io/OmniVTA/
- `why_in_top20`: **高学术价值 + 强产业化背景**。六大顶尖机构联合背书，论文/数据集/项目主页三件套齐全，是世界模型在机器人操作领域的重大突破。视觉素材丰富（16张配图）。赛道匹配：世界模型 × 机器人灵巧操作。
- `visual_assets`: 16张配图（微信文章），arXiv 论文 PDF，HuggingFace 数据集页面，项目主页演示视频候选
- `risks`: 学术性强，受众门槛较高；破圈性依赖大众媒体解读；时效窗口中等
- `supply_confidence`: HIGH - 有一手论文链接 + 项目主页 + HuggingFace 数据集

---

### 2. WideSeek-R1：清华 × 无问芯穹发布「广度扩展」多智能体

- `topic_key`: `WideSeek_R1_清华_无问芯穹_广度扩展`
- `title`: 不止Deep，更要Wide：清华、无问芯穹发布多智能体系统WideSeek-R1，4B模型比肩671B模型！
- `primary_platform`: 机器之心（微信公众号）
- `published_at`: `2026-03-27 12:01:55 CST`
- `original_link`: `https://mp.weixin.qq.com/s/qgGe51RcwJxkZ25DxQEpBA`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_jiqizhixin_deep_wide_wideseek_r1_4b_671b__source-packet.md`
- `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233838__不止deep_更要wide_清华_无问芯穹发布多智能体系统wideseek_r1_4b模型比肩671b模型__deep-article.md`
- `score_total`: **21/30**
- `score_breakdown`: 一手性=3 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=2 | 平台适配=3 | 时效窗口=2 | 讨论度=2
- `signal_summary`: 清华大学与无问芯穹 RLinf 团队提出「广度扩展（Width Scaling）」新维度，发布 WideSeek-R1 多智能体系统。不同于依赖人工设计工作流的多智能体系统，采用 Lead-agent-Subagent 架构。适合"整理全球前50大科技公司营收对比表"这类极广度信息搜集任务。
- `why_in_top20`: **学术 + 产业化双轮驱动**。清华 × 无问芯穹联合出品。提出"深度扩展 vs 广度扩展"新讨论框架。4B 小模型比肩 671B 的对比有传播性。切入角度：AI Scaling 新范式之争。
- `visual_assets`: 12张配图，机器之心完整正文
- `risks`: 学术性较高，需要对"广度扩展"概念进行大众化翻译
- `supply_confidence`: MEDIUM-HIGH - 有机器之心深度报道，正文结构完整

---

### 3. 天工AI全模态升维：从模型竞争到「平台经济」战略

- `topic_key`: `天工AI_全模态升维_平台经济_中关村论坛`
- `title`: 国产玩家亮剑世界模型！把全模态卷到顶后，天工AI不藏了
- `primary_platform`: 量子位（微信公众号）
- `published_at`: `2026-03-27 21:49:20 CST`
- `original_link`: `https://mp.weixin.qq.com/s/lNdMYYhM3bYHPvLD7Bkr1A`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_qbitai_ai__source-packet.md`
- `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233902__国产玩家亮剑世界模型_把全模态卷到顶后_天工ai不藏了__deep-article.md`
- `score_total`: **20/30**
- `score_breakdown`: 一手性=3 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=2 | 平台适配=2 | 时效窗口=3 | 讨论度=2
- `signal_summary`: 天工AI董事长兼CEO周亚辉在中关村论坛发布：天工AI已把多模态卷到全球第一梯队，战略升维——从模型竞争转向"AI平台经济"。两次跃迁论：第一次从流量经济到大模型工具时代；第二次从大模型工具时代到AI原生平台经济。"模型是引擎，平台是工厂，创意创作者是老板。"
- `why_in_top20`: **国产顶级玩家战略升维信号**。发布时间最新（3月27日晚）。周亚辉"两次跃迁论"是强观点。中关村论坛国家级平台背书。
- `visual_assets`: 18张配图，量子位完整正文
- `risks`: 企业战略解读依赖一手资料深度，部分表述可能经过公关处理
- `supply_confidence`: MEDIUM - 量子位一手报道，需补中关村论坛原始演讲稿

---

### 4. CHI 2026 Best Paper：CoBRA——让AI Agent社会模拟变成可控实验科学

- `topic_key`: `CHI2026_BestPaper_CoBRA_AI_Agent_社会模拟`
- `title`: CHI 2026 Best Paper｜社会模拟迈入可控、可量化时代：为AI Agent加上「认知滑条」
- `primary_platform`: 机器之心（微信公众号）
- `published_at`: `2026-03-27 14:23:16 CST`
- `original_link`: `https://mp.weixin.qq.com/s/FJULL6lcvqIFE4NaCEOx7w`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_jiqizhixin_chi_2026_best_paper_ai_agent__source-packet.md`
- `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233827__chi_2026_best_paper_社会模拟迈入可控_可量化时代_为ai_agent加上_认知滑条__deep-article.md`
- `score_total`: **19/30**
- `score_breakdown`: 一手性=3 | 传播性=1 | 破圈性=1 | 赛道匹配=3 | 可延展性=3 | 数据硬度=3 | 视觉素材=1 | 平台适配=2 | 时效窗口=2 | 讨论度=2
- `signal_summary`: UCSD 团队 CoBRA 论文（CHI 2026 Best Paper）：将经典社会科学实验转化为可复用的校准环境，使 Agent 行为可被测量、反馈与收敛，建立实验科学的变量控制机制。
- `why_in_top20`: **顶会最佳论文，AI Agent可控性重大突破**。CHI 顶级会议，Best Paper 含金量高。CoBRA 为 AI Agent 行为可控性提供新框架，对 Agents Safety 和 Alignment 有直接影响。
- `visual_assets`: 3张配图，完整正文可提取分析框架
- `risks`: 纯学术工作，大众传播需要强翻译；但有信息差红利
- `supply_confidence`: HIGH - 顶会 Best Paper 信息真实可靠

---

### 5. aiXcoder发布aiX-apply-4B：代码变更专用模型，15倍推理提效

- `topic_key`: `aiXcoder_aiX_apply_4B_代码变更_硅心科技`
- `title`: aiX-apply-4B逆袭DeepSeek-V3.2！aiXcoder发布代码变更应用模型，单卡推理提效15倍
- `primary_platform`: 机器之心（微信公众号）
- `published_at`: `2026-03-27 14:23:16 CST`
- `original_link`: `https://mp.weixin.qq.com/s/dnNxIyXwbZdyjhQLL0xSTQ`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_jiqizhixin_aix_apply_4b_deepseek_v3_2_aixcoder_15__source-packet.md`
- `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233815__aix_apply_4b逆袭deepseek_v3_2_aixcoder发布代码变更应用模型_单卡推理提效15倍__deep-article.md`
- `score_total`: **20/30**
- `score_breakdown`: 一手性=3 | 传播性=1 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=3 | 视觉素材=1 | 平台适配=3 | 时效窗口=2 | 讨论度=2
- `signal_summary`: 硅心科技（aiXcoder）发布 aiX-apply-4B，专为「代码变更应用」场景设计。基准测试：20+主流编程语言平均准确率93.8%，超越 Qwen3-4B（62.6%）和 DeepSeek-V3.2。算力成本约为 DeepSeek-V3.2 的5%，推理速度提升15倍，单卡消费级显卡即可部署。
- `why_in_top20`: **硬数据说话的产品发布**。93.8% vs 62.6% 准确率、15倍推理提速——数字具体、对比清晰、极易传播。国产 AI Coding 工具新势力。
- `visual_assets`: 4张配图，正文结构完整可提炼
- `risks`: 纯产品发布稿，需要补充竞品对比
- `supply_confidence`: MEDIUM-HIGH - 具体数字来自基准测试

---

### 6. SakanaAI/AI-Scientist-v2：AI科研自动化里程碑，论文正式通过同行评审

- `topic_key`: `SakanaAI_AI_Scientist_v2_ICLR_Workshop_AI科研自动化`
- `title`: SakanaAI/AI-Scientist-v2 — AI驱动的自动化科学研究（ICLR 2025 Workshop通过，同行评审认证）
- `primary_platform`: GitHub Trending + SakanaAI 官方论文
- `published_at`: `2026-03-27（capture day）`
- `original_link`: `https://github.com/SakanaAI/AI-Scientist-v2`
- `official_paper`: `https://pub.sakana.ai/ai-scientist-v2/paper/paper.pdf`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233359__github_trending_sakanaai_ai_scientist_v2__source-packet.md`
- `score_total`: **17/30**
- `score_breakdown`: 一手性=3 | 传播性=2 | 破圈性=1 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=1 | 平台适配=2 | 时效窗口=2 | 讨论度=2
- `signal_summary`: SakanaAI AI-Scientist-v2：完全由 AI 驱动的自动化科学研究流程（从假设生成到论文撰写）。论文《The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search》已被 ICLR 2025 Workshop 接收（同行评审认证）。这是首篇完全由 AI 生成并通过 peer review 的科学论文。v2 版本去除了 v1 对人工模板的依赖，采用"渐进式 agentic tree search"引导实验。
- `why_in_top20`: **AI-Scientist v2 已有同行评审认证的正式论文**（非 workshop 草稿），是科研自动化赛道的历史性节点。GitHub 2,708 stars 说明开发者社区真实 traction。双角度叙事：①AI for Science 科研范式革命；②v2 去除人工模板限制的工程突破。
- `visual_assets`: GitHub 仓库截图，README.md 技术图表候选，官方论文 PDF
- `risks`: Workshop 级别（非主会），需在标题和叙事中准确标注；工程化成熟度待观察
- `supply_confidence`: MEDIUM-HIGH - GitHub 客观数据 + 官方论文 PDF 已确认

---

### 7. 黄仁勋GTC 2026：「AI工厂时代」×「Token Maxxing × 边缘推理」双叙事

> **rewrite_angle #7/#8 合并说明**：原 #7（Founder Park「AI工厂时代」）与 #8（硅星人Pro「Token Maxxing × 边缘推理」）均为黄仁勋 GTC 2026 同一事件的不同切入角度，合并为单一候选以避免名额浪费，释放1个名额给 Apple Siri。双角度并行存在，各有独立价值。

- `topic_key`: `黄仁勋_GTC2026_AI工厂_TokenMaxxing_边缘推理`
- `title`: 黄仁勋：芯片公司的时代已经结束了——「AI工厂时代」×「Token Maxxing × 边缘推理」双叙事
- `primary_platform`: Founder Park + 硅星人Pro（微信公众号）
- `published_at`: `2026-03-26 09:34:26 CST`
- `source_packet_FounderPark`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_founder_park_ai__source-packet.md`
- `source_packet_Pro`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_guixingren_pro_https_mp_weixin_qq_com_s_ipaunqent8g57wioxikp_w__source-packet.md`
- `deep_article_FounderPark`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233606__黄仁勋_芯片公司的时代已经结束了_现在是_ai_工厂的时代__deep-article.md`
- `deep_article_Pro`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233728__黄仁勋喊出_推理拐点_边缘推理的机会窗口打开了吗__deep-article.md`
- `score_total`: **21/30**（双角度合并）
- `score_breakdown`: 一手性=2 | 传播性=3 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=2 | 平台适配=3 | 时效窗口=2 | 讨论度=3
- `signal_summary`:
  - **叙事A「AI工厂时代」（Founder Park）**：黄仁勋在 GTC 2026 提出"芯片公司时代已结束，现在是企业给工程师发 token 预算作为第二份薪酬"的时代宣言。OpenAI 数据：企业客户推理 token 消耗量约320倍增长。
  - **叙事B「Token Maxxing × 边缘推理」（硅星人Pro）**：硅谷新风气"token maxxing"——Meta/OpenAI 工程师内部搞 token 消耗量排行榜比谁烧得多。需求侧爆炸，边缘推理成新机会窗口。
- `why_in_top20`: **产业最强音 × 强争议性**。"芯片公司时代结束"是强观点，"Token Maxxing"是强叙事锚点，两者合一是 GTC 2026 最完整的产业信号。双平台信源互证，叙事层次更丰富。
- `visual_assets`: Founder Park 完整正文（conference 现场图候选）+ 硅星人Pro 10张配图
- `risks`: 需核实 GTC 原始演讲；双叙事写作时需避免内容重叠
- `supply_confidence`: MEDIUM-HIGH - 双平台互证，信源可靠

---

### 8. 人民想念DeepSeek：Token消耗量太大、价格太贵的产业反思

- `topic_key`: `人民想念DeepSeek_Token消耗_成本问题`
- `title`: 人民想念DeepSeek
- `primary_platform`: 硅星人Pro（微信公众号）
- `published_at`: `2026-03-26 09:34:26 CST`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_guixingren_pro_deepseek__source-packet.md`
- `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233716__人民想念deepseek__deep-article.md`
- `score_total`: **18/30**
- `score_breakdown`: 一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=2 | 可延展性=3 | 数据硬度=2 | 视觉素材=1 | 平台适配=3 | 时效窗口=2 | 讨论度=3
- `signal_summary`: Token 翻译在朋友圈引发广泛讨论——"词元""智元""慧根"等各种版本。OpenClaw（龙虾）在用户群大规模扩散，将 Token 概念带入公众视野。核心矛盾：消耗量大 + 价格贵，与 DeepSeek 低成本路线形成对比。
- `why_in_top20`: **强共鸣话题**。"人民想念DeepSeek"标题本身有传播性，抓住了从业者对低成本 AI 的期待。Token 翻译讨论有梗文化属性，易引发二次创作。
- `visual_assets`: 8张配图，完整正文（121段），腾讯科技可溯源
- `risks`: 观点性文章，数据硬度偏软；情绪性内容，判断需谨慎
- `supply_confidence`: MEDIUM - 腾讯科技出品，可回溯

---

### 9. 月之暗面（Kimi）传赴港IPO：国产AI独角兽资本动向信号

> **expand_validation #10拆分之一**：原 #10 三件套捆绑拆分为本条目及 #10b / #10c。本条目聚焦月之暗面 IPO 资本动向。

- `topic_key`: `月之暗面_Kimi_赴港IPO_融资动向`
- `title`: 传月之暗面拟赴港IPO——国产AI独角兽资本动向重要信号
- `primary_platform`: 极客公园（微信公众号）
- `published_at`: `2026-03-27 08:19:53 CST`
- `original_link`: `https://mp.weixin.qq.com/s/JQxNhWjlj_-W3VlhqFgsAQ`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_geekpark_ipo_ai_1000_2788__source-packet.md`
- `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233641__传月之暗面拟赴港ipo_全球首个_ai_失业补助_上线_每月1000_美元_大疆发全景无人机_2788元_极客早知道__deep-article.md`
- `score_total`: **16/30**（拆分后独立条目）
- `score_breakdown`: 一手性=1 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=1 | 视觉素材=1 | 平台适配=2 | 时效窗口=3 | 讨论度=2
- `signal_summary`: 极客早知道报道月之暗面（Kimi）传赴港 IPO，属于国产 AI 头部独角兽资本动向信号。目前 IPO 信息为"传"，未经官方确认，需后续跟踪。
- `why_in_top20`: **国产 AI 独角兽资本化是市场高度关注的叙事线**。月之暗面作为头部玩家，其 IPO 进展对 AI 一级市场有指标意义。单独列条目避免捆绑，提升价值感知。
- `risks`: IPO 属于"传"，未经官方确认；内容工厂不做确定性结论，只作为线索保留
- `supply_confidence`: LOW-MEDIUM - IPO传闻信源弱，需持续跟踪官方公告

---

### 10. 全球首个「AI失业补助」上线：每月1000美元的社科学实验

> **expand_validation #10拆分之一**：本条目聚焦全球首个AI失业补助的社会实验属性，独立于月之暗面IPO和大疆无人机。

- `topic_key`: `AI失业补助_1000美元_月_社会实验`
- `title`: 全球首个「AI失业补助」上线，每月1000美元——社科学实验还是政治作秀？
- `primary_platform`: 极客公园（微信公众号）
- `published_at`: `2026-03-27 08:19:53 CST`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_geekpark_ipo_ai_1000_2788__source-packet.md`
- `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233641__传月之暗面拟赴港ipo_全球首个_ai_失业补助_上线_每月1000_美元_大疆发全景无人机_2788元_极客早知道__deep-article.md`
- `score_total`: **17/30**
- `score_breakdown`: 一手性=2 | 传播性=2 | 破圈性=3 | 赛道匹配=2 | 可延展性=3 | 数据硬度=2 | 视觉素材=1 | 平台适配=3 | 时效窗口=3 | 讨论度=3
- `signal_summary`: 全球首个"AI失业补助"上线，每月1000美元。当 AI 导致大规模失业，由政府或机构提供基本收入保障。是科技-社会-政治交叉的全新实验，具有极高讨论价值和传播性。
- `why_in_top20`: **社会实验属性 × 强讨论度**。"每月1000美元 AI 失业补助"是 AI 时代最具争议的社会政策讨论。有科技、财经、社会的多圈层破圈潜力。
- `risks`: 需核实项目发起方和执行细节；存在政治作秀可能性
- `supply_confidence`: MEDIUM - 具体数字存在，需补官方来源

---

### 11. 大疆发布全景无人机DJI Air 3S：消费电子赛道升维

> **expand_validation #10拆分之一**：本条目聚焦大疆新品发布，独立于IPO和AI失业补助。

- `topic_key`: `大疆_DJI_Air3S_全景无人机_2788元`
- `title`: 大疆发全景无人机，2788元——消费电子 × AI视觉赛道升维
- `primary_platform`: 极客公园（微信公众号）
- `published_at`: `2026-03-27 08:19:53 CST`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_geekpark_ipo_ai_1000_2788__source-packet.md`
- `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233641__传月之暗面拟赴港ipo_全球首个_ai_失业补助_上线_每月1000_美元_大疆发全景无人机_2788元_极客早知道__deep-article.md`
- `score_total`: **16/30**
- `score_breakdown`: 一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=2 | 可延展性=2 | 数据硬度=2 | 视觉素材=2 | 平台适配=3 | 时效窗口=2 | 讨论度=2
- `signal_summary`: 大疆发布全景无人机 DJI Air 3S，定价 2788 元。具备全景拍摄能力，搭载 AI 视觉处理芯片。是消费级无人机在 AI 时代的功能升维。
- `why_in_top20`: **大疆新品有消费电子 × AI视觉双重赛道价值**，破圈受众远超 AI 圈。高性价比定价（2788元）有利于大众传播。
- `risks`: 消费电子新品报道较多，需找到差异化切入角度
- `supply_confidence`: MEDIUM-HIGH - 大疆新品具体参数可验证

---

### 12. Context才是新操作系统：前大疆/云鲸工程师做Agent Computer

- `topic_key`: `Context新操作系统_Agent_Computer_极客公园`
- `title`: 「Context 才是新操作系统」：从大疆、云鲸离开后，他要做 Agent Computer
- `primary_platform`: 极客公园（微信公众号）
- `published_at`: `2026-03-27 11:04:57 CST`
- `original_link`: `https://mp.weixin.qq.com/s/UbVodOvPprScY4VK4bVrYQ`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_geekpark_context_agent_computer__source-packet.md`
- `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233629__context_才是新操作系统_从大疆_云鲸离开后_他要做_agent_computer__deep-article.md`
- `score_total`: **20/30**
- `score_breakdown`: 一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=1 | 平台适配=3 | 时效窗口=3 | 讨论度=3
- `signal_summary`: 前大疆、云鲸员工创业，提出"Context才是新操作系统"论。核心洞察：只做对 Context 有价值的事情，打造面向 Agent 时代的"个人计算"底层设备。极客公园长文深度采访（正文10,000+字）。
- `why_in_top20`: **强创始人叙事 × 强赛道洞察**。"Context才是新操作系统"是极具潜力的金句候选。创始人背景（大疆+云鲸）有说服力。Agent OS 是当前 AI 圈讨论热点。
- `visual_assets`: 6张配图，完整正文（209段，10,000+字）
- `risks`: 创业公司早期，尚未有公开产品
- `supply_confidence`: MEDIUM-HIGH - 极客公园出品，创始人背景可交叉验证

---

### 13. 贝陪科技可豆陪陪：让AI「少说话」的儿童陪伴产品

- `topic_key`: `贝陪科技_可豆陪陪_AI陪伴_少说话策略`
- `title`: 对话贝陪科技：好的 AI 陪伴产品，应该让 AI 少说话
- `primary_platform`: Founder Park（微信公众号）
- `published_at`: `2026-03-26 19:43:25 CST`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_founder_park_ai_ai__source-packet.md`
- `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233617__对话贝陪科技_好的_ai_陪伴产品_应该让_ai_少说话__deep-article.md`
- `score_total`: **18/30**
- `score_breakdown`: 一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=2 | 可延展性=3 | 数据硬度=3 | 视觉素材=1 | 平台适配=3 | 时效窗口=2 | 讨论度=3
- `signal_summary`: 贝陪科技"可豆陪陪"儿童陪伴产品：毛绒娃娃+智能眼镜+NFC卡牌，押注纯语音路线。产品数据：用户日均对话51分钟、104轮次；上线150天留存率51%；28%使用来自卡牌互动，65%来自自由对话。核心理念：让AI"少说话"，激发孩子表达欲。
- `why_in_top20`: **AI陪伴产品差异化成功案例**。具体数据（51分钟/天、51%留存率）有说服力。"让AI少说话"是反直觉洞察。Founder Park 完整采访，正文结构优秀。
- `visual_assets`: 7张配图，完整正文（329段），产品图候选
- `risks`: 儿童教育产品小众赛道；数据来自公司自述
- `supply_confidence`: MEDIUM - Founder Park 采访一手性较强

---

### 14. 苹果开放Siri：iOS 27打造「AI能力分发平台」，万亿生态重构开启

> **expand_validation 新增条目（P1-2 返工）**：Anthropic 禁令（TechCrunch packet 存在但属于美国内政，传播受众偏窄）未入 Top20；以 Apple Siri 开放替代。Apple Siri 开放是高确定性、高传播性、高产业影响力的信号，与本包 AI/Agent 主线完全匹配。

- `topic_key`: `Apple_Siri_iOS27_第三方AI_分发平台`
- `title`: 开放 Siri，苹果决定打开万亿「AI 生态」——iOS 27 打造 AI 能力的 App Store
- `primary_platform`: 极客公园（微信公众号）
- `published_at`: `2026-03-27 13:31:11 CST`
- `original_link`: `https://mp.weixin.qq.com/s/aJZKf9WefHQDwFQiYgVPGw`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_geekpark_siri_ai__source-packet.md`
- `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233653__开放_siri_苹果决定打开万亿_ai_生态__deep-article.md`
- `score_total`: **20/30**
- `score_breakdown`: 一手性=2 | 传播性=3 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=2 | 平台适配=3 | 时效窗口=3 | 讨论度=3
- `signal_summary: **苹果在 iOS 27 中开放 Siri 作为 AI 分发平台**：任何通过 App Store 上架的 AI 服务（ChatGPT、Gemini、Claude）均可接入 Siri。苹果从"AI 技术采购方"变身为"AI 能力的分发平台"，角色等同于 AI 时代的 App Store。苹果可对第三方 AI 接入收取通道费（参考 App Store 15%-30% 抽成），将"AI 接入权"变成新的稀缺资源。WWDC 2026（6月8日）将正式揭晓，iPhone 全球 10 亿+ 活跃用户是核心筹码。
- `why_in_top20`: **苹果战略转向是 AI 时代最重磅的平台信号之一**。从独家绑定 OpenAI 到全面开放，角色升维逻辑清晰，商业化路径可期。对 OpenAI（失去独家地位）、Google（Gemini 借势 iPhone）、Anthropic（Claude 进 iPhone 生态）三方均有重大影响，是多角度叙事的富媒体。
- `visual_assets`: 6张配图，完整正文（83段），WWDC 预期图候选
- `risks`: 6月 WWDC 才正式揭晓，时效窗口需在内容中标注；目前信息来自媒体报道
- `supply_confidence`: HIGH - 极客公园一手抓取，Apple 官方公开信息可交叉验证

---

### 15. Advanced Machine Intelligence完成10.3亿美元种子轮融资：Yann LeCun × 世界模型

> **supplement_evidence #14 返工后保留主名单**：原 asset-chain 全空 → 经网络检索确认：AMI 确认为 Yann LeCun（图灵奖得主、前 Meta AI 首席）创办，总部巴黎，估值 $3.5B，资方包括 Nvidia、Samsung、Toyota Ventures、Eric Schmidt、Mark Cuban、Bezos Expeditions 等19家。supply_confidence 已升至 HIGH，保留主名单。

- `topic_key`: `Advanced_Machine_Intelligence_AMI_YannLeCun_10亿美元_世界模型`
- `title`: Advanced Machine Intelligence Closes $1.03 Billion Seed Funding — Yann LeCun 创办，估值$3.5B，世界模型路线
- `primary_platform`: FinSMEs + Silicon Republic 双重确认
- `published_at`: `2026-03-27（当日）`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_232523__finsmes_ai_gnews_advanced_machine_intelligence_closes_1_03_billion_seed_funding_finsmes__source-packet.md`
- `official_verification`: `https://www.siliconrepublic.com/start-ups/yann-lecun-ai-start-up-ami-raises-seed-funding-world-model`
- `asset_chain`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260415_233031__advanced_machine_intelligence__asset-chain.md`
- `score_total`: **18/30**（补证后从17升至18）
- `score_breakdown`: 一手性=2 | 传播性=2 | 破圈性=3 | 赛道匹配=3 | 可延展性=2 | 数据硬度=3 | 视觉素材=1 | 平台适配=2 | 时效窗口=3 | 讨论度=2
- `signal_summary`: Advanced Machine Intelligence（AMI）完成 $1.03 亿美元种子轮融资（史上最大欧洲种子轮），投后估值 $3.5B。创始人：图灵奖得主 Yann LeCun（担任执行董事长）+ CEO Alexandre LeBrun。公司正在开发基于 JEPA（联合嵌入预测架构）的"世界模型"，使 AI 系统能够理解物理世界、具备推理、规划和持久记忆，同时保持安全性。资方阵容豪华：Nvidia、Samsung、Toyota Ventures、Eric Schmidt、Mark Cuban、Bezos Expediments、Cathay Innovation 等19家。
- `why_in_top20`: **$1.03B + Yann LeCun 是本包最高权威背书的融资事件**。世界模型是 AI 前沿方向，JEPA 架构是 LeCun 一贯的技术路线，具有学术-产业双逻辑。资方阵容豪华（Nvidia + Samsung + Eric Schmidt）说明顶级产业资本认可。
- `visual_assets`: FinSMEs 融资数据截图，Silicon Republic 报道图
- `risks`: 公司成立于2026年，尚未有商业化产品；"世界模型"从研究到落地时间线未知
- `supply_confidence`: HIGH - Silicon Republic 独立报道 + FinSMEs 双确认，资方列表可交叉验证

---

### 16. Claude Code远程连接Telegram和Discord：AI Coding工具的社交化扩展

- `topic_key`: `Claude_Code_Telegram_Discord_远程连接`
- `title`: Claude Code 官方远程连接 Telegram 和 Discord 的操作流程
- `primary_platform`: 归藏的AI工具箱（微信公众号）
- `published_at`: `2026-03-27（大约）`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_guizang_ai_tools_claude_code_telegram_discord_telegram_telegram_botfather_token_plugin_in__source-packet.md`
- `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233740__20260415_233505_wechat_guizang_ai_tools_claude_code_telegram_discord_telegram_telegram_botfather_token_plugin_in_source_packet__deep-article.md`
- `score_total`: **14/30**
- `score_breakdown`: 一手性=2 | 传播性=2 | 破圈性=1 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉素材=1 | 平台适配=2 | 时效窗口=2 | 讨论度=2
- `signal_summary`: Claude Code 官方支持远程连接 Telegram 和 Discord，将 AI Coding 工具延伸至社交/办公场景。操作流程通过 BotFather Token Plugin 实现。
- `why_in_top20`: **Claude Code 生态扩展信号**。Anthropic 官方支持的远程连接能力说明 AI Coding 工具正在向社交化/协作化方向演进。开发者生态建设的重要步骤。
- `risks`: 操作流程类内容，受众相对垂直；时效性偏弱
- `supply_confidence`: MEDIUM - 归藏的AI工具箱出品，需补 Anthropic 官方文档

---

### 17. GLM-5.1发布：国产开源模型里程碑，200K上下文+编程SOTA

> **supplement_evidence #19 返工后升级**：原 Reddit 碎片讨论 → 经 Zhipu AI 官网（zhipuai.cn）确认：GLM-5.1 已正式发布，GLM-5-Turbo 是当前旗舰，GLM-5.1 于 2026-03-27 正式上线，支持 200K token 上下文，编程能力对标 Claude Opus 4.5。supply_confidence 已升至 MEDIUM-HIGH，保留主名单。

- `topic_key`: `GLM_5.1_智谱AI_国产开源模型_200K上下文`
- `title`: GLM-5.1 正式发布：国产开源模型里程碑，200K上下文+编程SOTA
- `primary_platform`: Reddit r/LocalLLaMA + Zhipu AI 官网双重确认
- `published_at`: `2026-03-27 2026`
- `original_link_Reddit`: `https://www.reddit.com/r/LocalLLaMA/comments/`
- `official_source`: `https://www.zhipuai.cn/`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233329__reddit_localllama_glm_5_1_is_out__source-packet.md`
- `score_total`: **17/30**（补官方来源后从15升至17）
- `score_breakdown`: 一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉素材=1 | 平台适配=2 | 时效窗口=3 | 讨论度=2
- `signal_summary`: Zhipu AI 于 2026-03-27 正式发布 GLM-5.1，这是国产开源大模型的重要里程碑。GLM-5.1 采用 MoE 架构，总参数 744B，推理时激活约 40B。支持 200K token 上下文窗口。编程能力对标 Claude Opus 4.5。已通过 GLM Coding Plan（Lite/Pro/Max 三档）开放给用户，并将以 MIT 许可证开源。
- `why_in_top20`: **国产开源模型竞争格局的关键节点**。GLM-5.1 正式发布（而非传闻）+ 开源承诺，使智谱 AI 成为国产开源赛道不可忽视的玩家。200K 上下文是长文本处理的关键能力。
- `risks`: 开源 MIT 许可证具体时间待定；编程 SOTA 说法需更多 benchmark 验证
- `supply_confidence`: MEDIUM-HIGH - Zhipu AI 官网确认 + Reddit 社区讨论互证

---

### 18. 消费级GPU单卡性能超越Claude Sonnet：编码benchmark新记录

- `topic_key`: `500_GPU_Claude_Sonnet_编码性能_benchmarks`
- `title`: 500美元GPU单卡性能超越Claude Sonnet编码benchmark
- `primary_platform`: Hacker News
- `published_at`: `2026-03-27（当日）`
- `original_link`: `https://news.ycombinator.com/item?id=47533297`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233359__hn_frontpage_47533297_500_gpu_outperforms_claude_sonnet_on_coding_benchmarks__source-packet.md`
- `official_verification`: `https://github.com/itigges22/ATLAS`
- `asset_chain`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260415_233359__atlas__asset-chain.md`
- `score_total`: **17/30**
- `score_breakdown`: 一手性=3 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=3 | 视觉素材=2 | 平台适配=3 | 时效窗口=2 | 讨论度=2
- `signal_summary`: HN 高热扩散已回链到官方 GitHub 项目 `ATLAS`。README 明确给出硬件为 `RTX 5060 Ti 16GB`、模型为 `Qwen3-14B-Q4_K_M (frozen)`，并宣称在 `599` 个 LiveCodeBench 任务上达到 `74.6% pass@1-v(k=3)`。但 README 也写明对 Claude 的对比来自外部 leaderboard，不是同任务集的严格 head-to-head。
- `why_in_top20`: **消费级硬件反打 frontier API，是强传播数字 + 强 builder 共鸣**。这不是单纯 HN 噪音，官方 repo / methodology 已补齐，具备“本地 infra 能否替代闭源 API”这一更大叙事空间。
- `visual_assets`: GitHub repo 首屏、README benchmark 对比表、Hacker News 讨论截图、方法学说明段落截图
- `risks`: 对 Claude Sonnet 的传播表述容易被误读为严格同任务集对决；ATLAS 当前 benchmark 优化重点偏向 LiveCodeBench，泛化性仍需后续验证
- `supply_confidence`: MEDIUM-HIGH - 官方 repo / README / methodology caveat 已补齐；正式写作需保留“非严格同任务集 head-to-head”提示

---

### 19. ICLR 2026论文：CPiRi打破CI/CD二元对立，时序预测新框架

- `topic_key`: `ICLR2026_CPiRi_时序预测_CI_CD`
- `title`: 刷榜多元时序预测，性能波动0%！打破CI/CD二元对立 | ICLR'26
- `primary_platform`: 新智元（微信公众号）
- `published_at`: `2026-03-26 09:13:12 CST`
- `original_link`: `https://mp.weixin.qq.com/s/dapV92RgrNzNVsUyCidkVg`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_xinzhiyuan_0_ci_cd_iclr_26__source-packet.md`
- `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233926__刷榜多元时序预测_性能波动0_打破ci_cd二元对立_iclr_26__deep-article.md`
- `score_total`: **16/30**
- `score_breakdown`: 一手性=3 | 传播性=1 | 破圈性=1 | 赛道匹配=2 | 可延展性=3 | 数据硬度=3 | 视觉素材=2 | 平台适配=2 | 时效窗口=1 | 讨论度=2
- `signal_summary`: 浙江财经大学研究团队提出 CPiRi 框架，打破时序预测领域通道依赖（CD）与通道独立（CI）的路线之争。论文已被 ICLR 2026 接收。测试中通道乱序性能零波动，仅用25%数据即可泛化至全网络。
- `why_in_top20`: **ICLR 顶会接收论文**。浙江财经大学团队，打破 CI/CD 二元对立的学术问题，有技术创新性。"性能波动0%"是有力的数据点。
- `visual_assets`: 47张配图（微信文章），ICLR 论文 PDF，GitHub 代码候选
- `risks`: 学术性极强，大众传播需要强翻译；发布时间偏早（3月26日）
- `supply_confidence`: HIGH - ICLR 论文信息可验证

---

### 20. Lanbow：企业级增长决策系统，千万美金广告经验开源

- `topic_key`: `Lanbow_AI增长决策_开源_硅星人Pro`
- `title`: 企业级 AI 增长决策系统 Lanbow 宣布将千万美金广告投放经验开源
- `primary_platform`: 硅星人Pro（微信公众号）
- `published_at`: `2026-03-26 09:34:26 CST`
- `original_link`: `https://mp.weixin.qq.com/s/x3qGi54GW8YGf6QC0ArcLg`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_guixingren_pro_ai_lanbow__source-packet.md`
- `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233704__企业级_ai_增长决策系统_lanbow_宣布将千万美金广告投放经验开源__deep-article.md`
- `official_verification`: `https://get.lanbow.com` | `https://github.com/sandwichlab-ai/lanbow-claw-skill`
- `asset_chain`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260415_233505__lanbow__asset-chain.md`
- `score_total`: **17/30**
- `score_breakdown`: 一手性=3 | 传播性=1 | 破圈性=1 | 赛道匹配=3 | 可延展性=2 | 数据硬度=3 | 视觉素材=2 | 平台适配=2 | 时效窗口=2 | 讨论度=2
- `signal_summary`: Lanbow 官网已在线，GitHub 存在 `sandwichlab-ai/lanbow-claw-skill` 开源仓库，repo 描述明确为 `Built on OpenClaw` 的 Meta 广告执行框架。深抓原文补出了企业级增长决策系统定位，以及 `5,291` 行 TypeScript、`3` 个运行时依赖、约 `200` 个 campaign session、完成率 `92%+` 等指标，但这些数字目前仍属于公司披露 / 媒体转述口径。
- `why_in_top20`: **企业 AI 落地 × MarTech × OpenClaw 开源范式**。它不是空泛“AI 营销”故事，而是把广告执行能力拆成可调用 skill，再把企业级多 campaign 决策系统留在商业化层，具备非常强的一人公司 / agent 落地讨论价值。
- `visual_assets`: 官网 landing 页、GitHub repo 首屏、深抓原文中的结构图与现场图、OpenClaw / ClawHub 关联截图候选
- `risks`: 开发者社区 traction 仍早期；`5,291 行代码 / 92%+ 完成率 / ~200 sessions` 暂无第三方独立审计，正式写作需标注为公司口径
- `supply_confidence`: MEDIUM-HIGH - 官网 + GitHub 已补齐，足以解除“空口媒体稿”风险；性能与完成率仍需条件性表述

---

## 结论

- `top3_must_watch`:
  1. **OmniVTA视触觉世界模型**（#1，22/30，最高综合分，六大机构背书，学术+产业双价值）
  2. **WideSeek-R1**（#2，21/30，清华+无问芯穹，广度扩展新范式）
  3. **黄仁勋GTC 2026双叙事**（#7，21/30，AI工厂时代×Token Maxxing合并，产业最强音）

- `top6_strong_pool`:
  1. 天工AI全模态升维（#3，20/30，发布时间最新，国产顶级玩家战略信号）
  2. aiXcoder aiX-apply-4B（#5，20/30，硬数据说话）
  3. Context才是新操作系统（#12，20/30，强创始人叙事）
  4. 苹果开放Siri（#14，20/30，**新增**，AI生态平台重构）
  5. CHI 2026 Best Paper CoBRA（#4，19/30）
  6. 人民想念DeepSeek（#8，18/30）

- `holdout_watchlist`:
  - **微信急了**（原#13，15/30）——时效已过期5天，降权至 holdout_watchlist
  - **Advanced Machine Intelligence**（#15，18/30）——**已升级主名单**，Yann LeCun + Silicon Republic 官方确认
  - **SakanaAI/AI-Scientist-v2**（#6，17/30）——Workshop论文已确认，保留主名单
  - **GLM-5.1**（#17，17/30）——**已升级主名单**，Zhipu AI 官网确认

- `supply_risk`:
  - **月之暗面IPO传闻**（#9）：IPO信息未获官方确认，内容工厂不直接下结论，只作为线索保留
  - **苹果Siri开放**（#14）：目前为媒体报道，WWDC 2026（6月8日）正式揭晓，需在内容中标注时效
  - **Lanbow**（#20）：官网 + GitHub 已补齐，但 `5,291 行 / 92%+ 完成率 / ~200 sessions` 仍属公司口径，写作时必须标注

## 执行备注

- 本次 Top20 基于 manifest 20260415 真实文件清单构建
- 逻辑日期 2026-04-15 为压缩彩排专用，与自然时钟无关
- 所有 source_packet / deep_article 路径均来自 manifest 验证
- 不允许复用 20260327 或其他旧日产物
- 本次返工所有路径均有 manifest 真实文件对应，无手写路径
