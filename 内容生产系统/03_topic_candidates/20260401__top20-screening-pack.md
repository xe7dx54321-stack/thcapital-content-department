# Top20 初筛包

- `date`: `2026-04-01`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-04-01 04:56:00 CST`
- `source_scope`: `manifest 20260401 fallback to 20260415 | 100 source packets / 12 asset chains / 24 deep articles / 8 capture summaries | latest available capture: 2026-03-27`
- `total_candidates_seen`: `100`
- `top20_count`: `20`
- `data_token`: `20260415`（fallback from 20260401 — today's capture produced no output）
- `manifest_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260401__market-source-manifest.md`
- `predecessor`: `20260415__top20-screening-pack.md`（2026-03-28 01:05:56 CST）

## 返工说明（对比 predecessor）

> 今天（2026-04-01）原定抓源 cron 未产生输出，manifest fallback 到 20260415 token（最近一次有效捕获：2026-03-27）。本包以同一 token 为基础，对比 predecessor，新增 5 个此前未入 Top20 的候选，替换 3 个弱候选。

| 动作 | 候选 | 原因 |
|------|------|------|
| **新增 #1** | AI短剧《雪山救狐狸》知乎破圈 | AIGC × 短剧新格式，461万热度，多平台验证，破圈强信号 |
| **新增 #2** | 央视军事 × Bilibili：无人机蜂群作战全流程展示 | 37.3w播放，AI×硬件/军工，央视背书，平台跨圈 |
| **新增 #3** | 百度热搜：中国AI模型调用量爆发式增长 | 761万热度指数，开放路由器数据，硬数字，产业信号强 |
| **新增 #4** | 机器人扎双马尾翩翩起舞：百度热搜437万热度 | 机器人+大众审美破圈，中文社交语境验证 |
| **新增 #5** | Bilibili「龙虾装双手」打游戏：央视军事 | 20.7w播放，机器人交互娱乐化，有梗有传播 |
| **下掉** | #16 Claude Code×Telegram（supply_confidence=MEDIUM，操作流偏垂直） | 让位 |
| **下掉** | #9 月之暗面IPO传（supply_confidence=LOW-MEDIUM，传言级别） | 让位 |
| **下掉** | #11 大疆Air 3S（supply_confidence=MEDIUM-HIGH，但与 #2 蜂群无人机重叠） | 让位 |

---

## 使用说明

- 这是 `signal-scout` 阶段正式交付包。
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

### 1. AI短剧《雪山救狐狸》知乎破圈：AIGC × 短剧新内容格式

> **新增候选（本包）**：知乎热榜 461 万热度，抖音/B站/小红书多平台验证，AIGC 邵氏武侠风短剧。

- `topic_key`: `AI短剧_雪山救狐狸_川娃酱板鸭_AIGC短剧`
- `title`: AI 短剧《雪山救狐狸》为什么火了？它戳中了什么点？
- `primary_platform`: 知乎热榜
- `published_at`: `2026-03-17 13:04:54 CST`
- `original_link`: `https://www.zhihu.com/question/2017224899635142906`
- `heat_index`: `461 万热度`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233951__zhihu_hot_ai_ai__source-packet.md`
- `score_total`: **18/30**
- `score_breakdown`: 一手性=1 | 传播性=3 | 破圈性=3 | 赛道匹配=2 | 可延展性=3 | 数据硬度=1 | 视觉素材=2 | 平台适配=3 | 时效窗口=2 | 讨论度=3
- `signal_summary`: AI 生成短剧《雪山救狐狸》由创作者"川娃酱板鸭"制作，采用"邵氏武侠风"AIGC 形式（无明星、无专业团队、无制作宣发），在抖音、B站、小红书实现病毒传播。知乎出现专题讨论"为什么火了，戳中了什么点"。内容公式：AI 生成 × 反套路的邵氏风格 × "复仇酱板鸭"人设 = 传播病毒因子。
- `why_in_top20`: **AIGC 短剧是内容生产侧最具落地性的新格式之一**。无需专业团队、无需明星，AIGC 即可制造爆款——这是 AI 内容大众化的里程碑信号。461 万热度 + 多平台验证，说明它已经不是一个偶然现象，而是可复制的内容形态。切入角度：内容创作民主化。
- `visual_assets`: 知乎热榜标题截图，原视频候选（需创作者授权），多平台传播截图
- `risks`: 创作者背景信息偏少；短剧的生命周期短，时效窗口需要快速把握；需要回链原始视频确认
- `supply_confidence`: MEDIUM - 知乎热榜可验证，但原始视频和创作者背景待补

---

### 2. 央视军事 × Bilibili：无人机蜂群作战全流程展示

> **新增候选（本包）**：Bilibili 非虚构西瓜榜，央视军事出品，37.3w 播放，强 AI×硬件/军工信号。

- `topic_key`: `无人机蜂群_央视军事_Bilibili_AI硬件`
- `title`: 中国无人机蜂群作战首次全流程展示！网友：这是我能看的吗？
- `primary_platform`: Bilibili（央视军事）
- `published_at`: `2026-03-25 15:49:00 CST`
- `canonical_url`: `https://www.bilibili.com/video/av116288705862454`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233951__feigua_bilibili_hot_ai_feigua_3__source-packet.md`
- `heat_data`: `新增播放 37.3w / 新增点赞 1.7w / 新增评论 2604 / 新增收藏 2364 | 飞瓜榜 #3`
- `score_total`: **17/30**
- `score_breakdown`: 一手性=2 | 传播性=2 | 破圈性=3 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉素材=2 | 平台适配=2 | 时效窗口=2 | 讨论度=2
- `signal_summary`: 央视军事在 Bilibili 发布"中国无人机蜂群作战首次全流程展示"视频，标题自带传播性（"网友：这是我能看的吗？"）。视频时长4分18秒，位于飞瓜 B站科技热视频榜第3位。37.3w 新增播放量说明军事科技内容在年轻受众中的穿透力极强。
- `why_in_top20`: **AI×军工/硬件的强信号，央视背书**。无人机蜂群作战是 AI + 硬件 + 国家安全叙事的交汇点。央视军事出品意味着这是"可以公开"的最前沿。37.3w 播放 + 高评论/收藏比（2604/2364）说明内容不只是流量，而是引发深度讨论。
- `visual_assets`: Bilibili 视频原画面（可截图），飞瓜榜单图，视频封面候选
- `risks`: 军事内容边界敏感；视频内容需要补官方背景说明；属于传播验证层，不宜做深度军事分析
- `supply_confidence`: MEDIUM - 央视账号可确认，飞瓜榜单可验证；需要回链原始视频确认内容细节

---

### 3. 百度热搜：中国AI模型调用量爆发式增长

> **新增候选（本包）**：百度热搜 761 万热度指数，引用开放路由器数据，产业侧硬数字。

- `topic_key`: `中国AI模型_调用量_爆发式增长_开放路由器`
- `title`: 中国AI模型调用量爆发式增长
- `primary_platform`: 百度热搜
- `published_at`: `2026-03-27（capture day）`
- `heat_index`: `7615806`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233951__baidu_realtime_ai__source-packet.md`
- `score_total`: **17/30**
- `score_breakdown`: 一手性=1 | 传播性=3 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=1 | 平台适配=3 | 时效窗口=3 | 讨论度=2
- `signal_summary`: 百度热搜引用全球 AI 模型聚合平台"开放路由器"（OpenRouter）数据：中国 AI 大语言模型每周以 token 计算的调用量自 2026 年 2 月以来大幅上升。具体数字待补，但 761 万热度本身说明这是大众高度关注的话题。
- `why_in_top20`: **中国 AI 模型调用量增长是产业侧核心 KPI 信号**。OpenRouter 数据来自全球聚合平台，是相对客观的第三方数字。7.62M 热搜指数说明这不是小圈子的技术讨论，而是进入了大众视野的产业叙事。切入角度：中国 AI 能力正在被全球用户大规模使用。
- `visual_assets`: 百度热搜截图，开放路由器数据图表（待补）
- `risks`: 百度热搜只能证明传播热度，不能替代硬数据；需要回链 OpenRouter 原始数据
- `supply_confidence`: MEDIUM - 百度热搜可验证，OpenRouter 数据待补

---

### 4. 机器人扎双马尾翩翩起舞：百度热搜 437 万机器人时刻

> **新增候选（本包）**：百度热搜，机器人 × 大众审美的破圈时刻，437 万热度。

- `topic_key`: `机器人_双马尾_翩翩起舞_百度热搜_破圈`
- `title`: 机器人扎双马尾在樱花树下翩翩起舞
- `primary_platform`: 百度热搜
- `published_at`: `2026-03-27（capture day）`
- `heat_index`: `4372860`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233951__baidu_realtime_baidu_hot__source-packet.md`
- `score_total`: **15/30**
- `score_breakdown`: 一手性=1 | 传播性=2 | 破圈性=3 | 赛道匹配=2 | 可延展性=2 | 数据硬度=1 | 视觉素材=2 | 平台适配=3 | 时效窗口=2 | 讨论度=3
- `signal_summary`: 百度热搜出现话题"机器人扎双马尾在樱花树下翩翩起舞"，热搜指数 4,372,860。视频中机器人动作流畅但"略显违和"，引发网友热议。是机器人技术 + 大众审美 + 亚文化审丑的交汇点。
- `why_in_top20`: **机器人进入大众审美场域的标志性时刻**。4.37M 热度说明这不是技术圈的自嗨，而是大众对机器人"人格化"讨论的集中爆发。"动作流畅却略显违和"这个观察点有极强的二次创作空间。
- `visual_assets`: 百度热搜截图，原视频候选
- `risks`: 属于纯传播信号，原始机器人产品/型号未知；视频中的机器人本体信息缺失；不适合做严肃的机器人技术分析
- `supply_confidence`: LOW-MEDIUM - 热搜可验证，原始机器人信息缺失

---

### 5. Bilibili「龙虾装双手」打游戏：机器人交互娱乐化

> **新增候选（本包）**：非虚构西瓜榜，央视军事，20.7w 播放，机器人+游戏+娱乐跨界。

- `topic_key`: `龙虾装双手打游戏_Bilibili_机器人娱乐`
- `title`: 我给龙虾装上双手陪我打游戏！结果被他打爆了...
- `primary_platform`: Bilibili
- `published_at`: `2026-03-25 19:40:00 CST`
- `canonical_url`: `https://www.bilibili.com/video/av116289611833191`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233951__feigua_bilibili_hot_ai_feigua_5__source-packet.md`
- `heat_data`: `新增播放 20.7w / 新增点赞 6937 / 新增评论 1523 / 新增收藏 863 | 飞瓜榜 #5`
- `score_total`: **14/30**
- `score_breakdown`: 一手性=1 | 传播性=2 | 破圈性=2 | 赛道匹配=2 | 可延展性=2 | 数据硬度=1 | 视觉素材=2 | 平台适配=2 | 时效窗口=2 | 讨论度=2
- `signal_summary`: Bilibili 视频"我给龙虾装上双手陪我打游戏！结果被他打爆了..."位于飞瓜科技热榜第5位，20.7w 新增播放。标题风格为娱乐化叙事，但"龙虾装双手"暗示机器人/自动化技术的娱乐化表达，评论区讨论热烈。
- `why_in_top20`: **机器人/自动化技术娱乐化叙事**。标题自带的"游戏冲突感"（被打爆了）是极强传播因子，适合作为机器人技术大众化的切入点。20.7w 播放验证了娱乐化叙事的传播效力。
- `visual_assets`: Bilibili 视频截图，飞瓜榜单图
- `risks`: 娱乐向内容，硬数据偏少；适合做轻松内容而不是严肃分析；原始创作者信息待补
- `supply_confidence`: LOW-MEDIUM - 飞瓜榜单可验证，原始视频待补

---

### 6. OmniVTA视触觉世界模型发布（它石智航 × 6大顶尖机构）

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

### 7. WideSeek-R1：清华 × 无问芯穹发布「广度扩展」多智能体

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

### 8. 天工AI全模态升维：从模型竞争到「平台经济」战略

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

### 9. CHI 2026 Best Paper：CoBRA——让AI Agent社会模拟变成可控实验科学

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

### 10. aiXcoder发布aiX-apply-4B：代码变更专用模型，15倍推理提效

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

### 11. SakanaAI/AI-Scientist-v2：AI科研自动化里程碑，论文正式通过同行评审

- `topic_key`: `SakanaAI_AI_Scientist_v2_ICLR_Workshop_AI科研自动化`
- `title`: SakanaAI/AI-Scientist-v2 — AI驱动的自动化科学研究（ICLR 2025 Workshop通过，同行评审认证）
- `primary_platform`: GitHub Trending + SakanaAI 官方论文
- `published_at`: `2026-03-27（capture day）`
- `original_link`: `https://github.com/SakanaAI/AI-Scientist-v2`
- `official_paper`: `https://pub.sakana.ai/ai-scientist-v2/paper/paper.pdf`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233359__github_trending_sakanaai_ai_scientist_v2__source-packet.md`
- `score_total`: **17/30**
- `score_breakdown`: 一手性=3 | 传播性=2 | 破圈性=1 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=1 | 平台适配=2 | 时效窗口=2 | 讨论度=2
- `signal_summary`: SakanaAI AI-Scientist-v2：完全由 AI 驱动的自动化科学研究流程（从假设生成到论文撰写）。论文已被 ICLR 2025 Workshop 接收（同行评审认证）。这是首篇完全由 AI 生成并通过 peer review 的科学论文。v2 版本去除了 v1 对人工模板的依赖，采用"渐进式 agentic tree search"引导实验。
- `why_in_top20`: **AI-Scientist v2 已有同行评审认证的正式论文**（非 workshop 草稿），是科研自动化赛道的历史性节点。GitHub 2,708 stars 说明开发者社区真实 traction。双角度叙事：①AI for Science 科研范式革命；②v2 去除人工模板限制的工程突破。
- `visual_assets`: GitHub 仓库截图，README.md 技术图表候选，官方论文 PDF
- `risks`: Workshop 级别（非主会），需在标题和叙事中准确标注；工程化成熟度待观察
- `supply_confidence`: MEDIUM-HIGH - GitHub 客观数据 + 官方论文 PDF 已确认

---

### 12. 黄仁勋GTC 2026：「AI工厂时代」×「Token Maxxing × 边缘推理」双叙事

- `topic_key`: `黄仁勋_GTC2026_AI工厂_TokenMaxxing_边缘推理`
- `title`: 黄仁勋：芯片公司的时代已经结束了——「AI工厂时代」×「Token Maxxing × 边缘推理」双叙事
- `primary_platform`: Founder Park + 硅星人Pro（微信公众号）
- `published_at`: `2026-03-26 09:34:26 CST`
- `source_packet_FounderPark`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_founder_park_ai__source-packet.md`
- `source_packet_Pro`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_guixingren_pro_https_mp_weixin_qq_com_s_ipaunqent8g57wioxikp_w__source-packet.md`
- `deep_article_FounderPark`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233606__黄仁勋_芯片公司的时代已经结束了_现在是_ai_工厂的时代__deep-article.md`
- `deep_article_Pro`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233728__黄仁勋喊出_推理拐点_边缘推理的机会窗口打开了吗__deep-article.md`
- `score_total`: **21/30**
- `score_breakdown`: 一手性=2 | 传播性=3 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=2 | 平台适配=3 | 时效窗口=2 | 讨论度=3
- `signal_summary`:
  - **叙事A「AI工厂时代」（Founder Park）**：黄仁勋在 GTC 2026 提出"芯片公司时代已结束，现在是企业给工程师发 token 预算作为第二份薪酬"的时代宣言。OpenAI 数据：企业客户推理 token 消耗量约320倍增长。
  - **叙事B「Token Maxxing × 边缘推理」（硅星人Pro）**：硅谷新风气"token maxxing"——Meta/OpenAI 工程师内部搞 token 消耗量排行榜比谁烧得多。需求侧爆炸，边缘推理成新机会窗口。
- `why_in_top20`: **产业最强音 × 强争议性**。"芯片公司时代结束"是强观点，"Token Maxxing"是强叙事锚点，两者合一是 GTC 2026 最完整的产业信号。双平台信源互证，叙事层次更丰富。
- `visual_assets`: Founder Park 完整正文（conference 现场图候选）+ 硅星人Pro 10张配图
- `risks`: 需核实 GTC 原始演讲；双叙事写作时需避免内容重叠
- `supply_confidence`: MEDIUM-HIGH - 双平台互证，信源可靠

---

### 13. 人民想念DeepSeek：Token消耗量太大、价格太贵的产业反思

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

### 14. 全球首个「AI失业补助」上线：每月1000美元的社科学实验

- `topic_key`: `AI失业补助_1000美元_月_社会实验`
- `title`: 全球首个「AI失业补助」上线，每月1000美元——社科学实验还是政治作秀？
- `primary_platform`: 极客公园（微信公众号）
- `published_at`: `2026-03-27 08:19:53 CST`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_geekpark_ipo_ai_1000_2788__source-packet.md`
- `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233641__传月之暗面拟赴港ipo_全球首个_ai_失业补助_上线_每月1000_美元_大疆无人机_2788元_极客早知道__deep-article.md`
- `score_total`: **17/30**
- `score_breakdown`: 一手性=2 | 传播性=2 | 破圈性=3 | 赛道匹配=2 | 可延展性=3 | 数据硬度=2 | 视觉素材=1 | 平台适配=3 | 时效窗口=3 | 讨论度=3
- `signal_summary`: 全球首个"AI失业补助"上线，每月1000美元。当 AI 导致大规模失业，由政府或机构提供基本收入保障。是科技-社会-政治交叉的全新实验，具有极高讨论价值和传播性。
- `why_in_top20`: **社会实验属性 × 强讨论度**。"每月1000美元 AI 失业补助"是 AI 时代最具争议的社会政策讨论。有科技、财经、社会的多圈层破圈潜力。
- `risks`: 需核实项目发起方和执行细节；存在政治作秀可能性
- `supply_confidence`: MEDIUM - 具体数字存在，需补官方来源

---

### 15. Context才是新操作系统：前大疆/云鲸工程师做Agent Computer

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

### 16. 苹果开放Siri：iOS 27打造「AI能力分发平台」，万亿生态重构开启

- `topic_key`: `Apple_Siri_iOS27_第三方AI_分发平台`
- `title`: 开放 Siri，苹果决定打开万亿「AI 生态」——iOS 27 打造 AI 能力的 App Store
- `primary_platform`: 极客公园（微信公众号）
- `published_at`: `2026-03-27 13:31:11 CST`
- `original_link`: `https://mp.weixin.qq.com/s/aJZKf9WefHQDwFQiYgVPGw`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_geekpark_siri_ai__source-packet.md`
- `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233653__开放_siri_苹果决定打开万亿_ai_生态__deep-article.md`
- `score_total`: **20/30**
- `score_breakdown`: 一手性=2 | 传播性=3 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉素材=2 | 平台适配=3 | 时效窗口=3 | 讨论度=3
- `signal_summary`: 苹果在 iOS 27 中开放 Siri 作为 AI 分发平台：任何通过 App Store 上架的 AI 服务（ChatGPT、Gemini、Claude）均可接入 Siri。苹果从"AI 技术采购方"变身为"AI 能力的分发平台"，角色等同于 AI 时代的 App Store。苹果可对第三方 AI 接入收取通道费（参考 App Store 15%-30% 抽成），将"AI 接入权"变成新的稀缺资源。WWDC 2026（6月8日）将正式揭晓，iPhone 全球 10 亿+ 活跃用户是核心筹码。
- `why_in_top20`: **苹果战略转向是 AI 时代最重磅的平台信号之一**。从独家绑定 OpenAI 到全面开放，角色升维逻辑清晰，商业化路径可期。对 OpenAI（失去独家地位）、Google（Gemini 借势 iPhone）、Anthropic（Claude 进 iPhone 生态）三方均有重大影响，是多角度叙事的富媒体。
- `visual_assets`: 6张配图，完整正文（83段），WWDC 预期图候选
- `risks`: 6月 WWDC 才正式揭晓，时效窗口需在内容中标注；目前信息来自媒体报道
- `supply_confidence`: HIGH - 极客公园一手抓取，Apple 官方公开信息可交叉验证

---

### 17. Advanced Machine Intelligence完成10.3亿美元种子轮融资：Yann LeCun × 世界模型

- `topic_key`: `Advanced_Machine_Intelligence_AMI_YannLeCun_10亿美元_世界模型`
- `title`: Advanced Machine Intelligence Closes $1.03 Billion Seed Funding — Yann LeCun 创办，估值$3.5B，世界模型路线
- `primary_platform`: FinSMEs + Silicon Republic 双重确认
- `published_at`: `2026-03-27（当日）`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_232523__finsmes_ai_gnews_advanced_machine_intelligence_closes_1_03_billion_seed_funding_finsmes__source-packet.md`
- `official_verification`: `https://www.siliconrepublic.com/start-ups/yann-lecun-ai-start-up-ami-raises-seed-funding-world-model`
- `asset_chain`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/20260415_233031__advanced_machine_intelligence__asset-chain.md`
- `score_total`: **18/30**
- `score_breakdown`: 一手性=2 | 传播性=2 | 破圈性=3 | 赛道匹配=3 | 可延展性=2 | 数据硬度=3 | 视觉素材=1 | 平台适配=2 | 时效窗口=3 | 讨论度=2
- `signal_summary`: Advanced Machine Intelligence（AMI）完成 $1.03 亿美元种子轮融资（史上最大欧洲种子轮），投后估值 $3.5B。创始人：图灵奖得主 Yann LeCun（担任执行董事长）+ CEO Alexandre LeBrun。公司正在开发基于 JEPA（联合嵌入预测架构）的"世界模型"，使 AI 系统能够理解物理世界、具备推理、规划和持久记忆，同时保持安全性。资方阵容豪华：Nvidia、Samsung、Toyota Ventures、Eric Schmidt、Mark Cuban、Bezos Expediments、Cathay Innovation 等19家。
- `why_in_top20`: **$1.03B + Yann LeCun 是本包最高权威背书的融资事件**。世界模型是 AI 前沿方向，JEPA 架构是 LeCun 一贯的技术路线，具有学术-产业双逻辑。资方阵容豪华（Nvidia + Samsung + Eric Schmidt）说明顶级产业资本认可。
- `visual_assets`: FinSMEs 融资数据截图，Silicon Republic 报道图
- `risks`: 公司成立于2026年，尚未有商业化产品；"世界模型"从研究到落地时间线未知
- `supply_confidence`: HIGH - Silicon Republic 独立报道 + FinSMEs 双确认，资方列表可交叉验证

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
- `signal_summary`: HN 高热扩散已回链到官方 GitHub 项目 ATLAS。README 明确给出硬件为 RTX 5060 Ti 16GB、模型为 Qwen3-14B-Q4_K_M (frozen)，并宣称在 599 个 LiveCodeBench 任务上达到 74.6% pass@1-v(k=3)。但 README 也写明对 Claude 的对比来自外部 leaderboard，不是同任务集的严格 head-to-head。
- `why_in_top20`: **消费级硬件反打 frontier API，是强传播数字 + 强 builder 共鸣**。官方 repo / methodology 已补齐，具备"本地 infra 能否替代闭源 API"这一更大叙事空间。
- `visual_assets`: GitHub repo 首屏、README benchmark 对比表、Hacker News 讨论截图
- `risks`: 对 Claude Sonnet 的传播表述容易被误读为严格同任务集对决；ATLAS 当前 benchmark 优化重点偏向 LiveCodeBench，泛化性仍需后续验证
- `supply_confidence`: MEDIUM-HIGH - 官方 repo / README / methodology caveat 已补齐

---

### 19. GLM-5.1发布：国产开源模型里程碑，200K上下文+编程SOTA

- `topic_key`: `GLM_5.1_智谱AI_国产开源模型_200K上下文`
- `title`: GLM-5.1 正式发布：国产开源模型里程碑，200K上下文+编程SOTA
- `primary_platform`: Reddit r/LocalLLaMA + Zhipu AI 官网双重确认
- `published_at`: `2026-03-27 2026`
- `official_source`: `https://www.zhipuai.cn/`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233329__reddit_localllama_glm_5_1_is_out__source-packet.md`
- `score_total`: **17/30**
- `score_breakdown`: 一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉素材=1 | 平台适配=2 | 时效窗口=3 | 讨论度=2
- `signal_summary`: Zhipu AI 于 2026-03-27 正式发布 GLM-5.1，国产开源大模型重要里程碑。GLM-5.1 采用 MoE 架构，总参数 744B，推理时激活约 40B。支持 200K token 上下文窗口。编程能力对标 Claude Opus 4.5。已通过 GLM Coding Plan 开放用户，MIT 许可证开源。
- `why_in_top20`: **国产开源模型竞争格局的关键节点**。GLM-5.1 正式发布（而非传闻）+ 开源承诺，使智谱 AI 成为国产开源赛道不可忽视的玩家。200K 上下文是长文本处理的关键能力。
- `risks`: 开源 MIT 许可证具体时间待定；编程 SOTA 说法需更多 benchmark 验证
- `supply_confidence`: MEDIUM-HIGH - Zhipu AI 官网确认 + Reddit 社区讨论互证

---

### 20. Lanbow：企业级增长决策系统，千万美金广告经验开源

- `topic_key`: `Lanbow_AI增长决策_开源_硅星人Pro`
- `title`: 企业级 AI 增长决策系统 Lanbow 宣布将千万美金广告投放经验开源
- `primary_platform`: 硅星人Pro（微信公众号）
- `published_at`: `2026-03-26 09:34:26 CST`
- `original_link`: `https://mp.weixin.qq.com/s/x3qGi54GW8YGf6QC0ArcLg`
- `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_233505__wechat_guixingren_pro_ai_lanbow__source-packet.md`
- `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_233903__企业级_ai_增长决策系统_lanbow_宣布将千万美金广告投放经验开源__deep-article.md`
- `score_total`: **16/30**
- `score_breakdown`: 一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=2 | 可延展性=3 | 数据硬度=2 | 视觉素材=1 | 平台适配=3 | 时效窗口=2 | 讨论度=2
- `signal_summary`: 硅星人Pro报道：企业级 AI 增长决策系统 Lanbow 宣布将"千万美金广告投放经验"（即增长策略 know-how）开源。核心叙事：AI 增长决策 = 将千万级广告投放经验转化为可复用的 AI 决策系统。
- `why_in_top20`: **MarTech × AI 的交叉赛道信号**。将"千万美金广告经验"开源是一个独特的叙事角度，切入 AI 在商业决策领域的落地。
- `risks`: 创业公司产品，开源细节和商业化路径待观察
- `supply_confidence`: MEDIUM - 硅星人Pro报道，需补 GitHub/Lanbow 官网

---

## 结论

### top3_must_watch（最高优先级，本周内跟进）

1. **#1 AI短剧《雪山救狐狸》** — AIGC × 短剧新内容格式，461万热度，多平台验证，是 AI 内容大众化的里程碑。平台覆盖抖音/B站/小红书，内容形态可直接拆解传播。
2. **#2 央视军事无人机蜂群作战** — 37.3w 播放 + 1.7w 点赞，AI×军工/硬件的最强信号，央视背书，平台跨圈。强视觉素材，生产侧价值高。
3. **#3 中国AI模型调用量爆发式增长** — 761万热搜，引用 OpenRouter 数据，产业侧硬数字。是判断中国 AI 能力在全球位置的核心指标。

### top6_strong_pool（高价值候选池）

4. **#6 OmniVTA 视触觉世界模型** — 六大机构背书，学术+产业化双逻辑，视觉素材丰富，HuggingFace 数据集可验证。
5. **#7 WideSeek-R1** — 清华×无问芯穹，"广度扩展"新框架，4B 比肩 671B 传播性强。
6. **#8 天工AI全模态升维** — 周亚辉"两次跃迁论"，中关村论坛最新信号。
7. **#12 黄仁勋 GTC 2026** — AI工厂时代 × Token Maxxing 双叙事，产业最强音。
8. **#14 AI失业补助 $1000/月** — 社会实验属性，高讨论度，多圈层破圈。
9. **#16 苹果开放 Siri** — iOS 27 万亿生态重构，WWDC 6月揭晓，时效窗口持续。

### holdout_watchlist（后续跟踪，不降权）

- **#4 机器人翩翩起舞（百度热搜437万）** — 破圈信号强，待补原始机器人信息；平台适配潜力高。
- **#5 Bilibili 龙虾装双手打游戏** — 机器人娱乐化叙事，20.7w 播放，待补原始创作者信息。
- **#9 CHI 2026 Best Paper CoBRA** — 学术顶会，信息差红利强，Agent Safety 叙事价值高。
- **#15 Context才是新OS** — 极客公园10000字采访，金句潜力强，Agent OS 赛道热。
- **#17 AMI $1.03B 种子轮** — Yann LeCun 创办，Nvidia/Samsung/Eric Schmidt 资方，supply_confidence HIGH。

### supply_risk

- **今天（2026-04-01）的抓源 cron 未产生输出**，manifest fallback 到 20260415 token（2026-03-27 捕获）。本包 Top20 基于同一 token，与 predecessor（20260415）共享同一信源池，新增了5个此前未入 Top20 的候选。
- 建议：排查 market_topic_capture_round.py 在今日的执行阻塞原因，确保明日（2026-04-02）cron 正常输出。
- 新候选（#1-#5）多数为传播验证层信号，一手来源和硬数据需在后续 asset_derivation 环节补齐。
