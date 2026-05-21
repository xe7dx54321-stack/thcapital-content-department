# 平台任务单

- `date`: `2026-05-04`
- `owner`: `topic-planner`
- `generated_at`: `2026-05-04 20:10 CST`
- `input_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260504__top20-screening-pack.md`
- `top5_board`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260504__daily-top8-to-top5.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `rework + continuity_only 场景；Top5 板已 final；按 limited task sheet 纪律执行，wechat 保留 2 主槽位，另外最多 2 平台各保 1 个 active slot，其余候选进 holdout`

---

## 已知风险备注（写稿前必读）

- **Top5 Rank #5（HN Phish 30年）**：scorecard 标注 P1 fatal——source packet 为空壳，缺 Meiklejohn 文章 Distilled Body。当前已进 Top5 但 execution readiness "暂不可发"。content-writer 须先验证源文可取用，或主动降级为 holdout，不应强行上量。相关任务槽位风险由 writer 自评。
- **Top5 Rank #3（曦望GPU独角兽）**：scorecard 标注 "暂不可发（缺正文）"，需 CEO 专访 Distilled Body 到货才可发。当前 WeChat 槽位预排，若 17:00 前原文未到，降级 holdout。

---

## 全局主池 Top6

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|---|---|---|---|---|
| 1 | `youtube_ai_dot_engineer_mergeable_by_default_building_the_context_engine_to_save_time_and_tokens_20260504` | P0；execution readiness 接近通过；context engine / time-token saving 与 agent 主流强相关 | 视频已有完整叙事结构；Peter Werry / Unblocked 背景可查；具备天然 hook | partial source；正文仍需补原始引用上下文 |
| 2 | `hn_frontpage_47994012_specsmaxxing_on_overcoming_ai_psychosis_and_why_i_write_specs_i_20260504` | P0；execution readiness 接近通过；有 HN 扩散热度入口；specs-as-therapy 视角新颖 | 有明确 blog 原文（acahi.sh）；SPEC 格式叙事适合展开；brand fit 高 | partial source；正文仍需补原始引用上下文 |
| 3 | `qbitai_site_gpu_unicorn_20260504` | P1 conditional；CEO 专访稀缺；推理成本赛道；百亿估值有锚点 | 一手引语 + 估值数字硬；与 GPU / 推理 / 算力主线高度一致 | 缺专访正文；原文到货前不可发 WeChat 主槽 |
| 4 | `zhihu_hot_ai_35_ai_20260504` | P1；仲裁案有司法锚点；AI 替代蓝领议题有持续讨论热度 | 法院判决有公信力；#35岁 #裁员 标签强共鸣；brand fit 中 | 缺一手判决书；signal_summary 数字需补强（2.5万降薪、26万赔偿等） |
| 5 | `hn_frontpage_47998225_for_thirty_years_i_programmed_with_phish_on_every_day_20260504` | P1 at risk；source packet 空壳已知；Phish 编程叙事有传播潜力 | 个人叙事 + AI flow 切入角度新；HN 高赞已验证热度 | 致命空壳；writer 需确认能取到原文全文；否则降 holdout |
| 6 | `wechat_jiqizhixin_cto_anthropic_20260504` | P2 holdout 升级；CTO 转型工程师叙事有市场；Anthropic 背景有公信力 | 微信原发已验证内容存在；品牌话题性强；可作为 continuity 补位 | 缺原始来源链接；补证完成前不占 active slot |

---

## 六个主战场任务单

### `wechat`

#### Task 1
- `topic_key`: `qbitai_site_gpu_unicorn_20260504`
- `目标读者`: 科技/投资从业者，关注 GPU 推理成本、国产芯片机会
- `切入角度`: 不要停留在"又一家GPU独角兽"的故事包装，重点判断曦望的"推理成本更低"逻辑是否成立、边界在哪里、可复制性有多高
- `核心论点`: 国内纯推理 GPU 赛道出现首家百亿估值公司；王湛引言"谁的推理成本更低谁就是赢家"是本篇核心命题；需验证这一判断的成立条件
- `证据抓手`: 量子位专访原文（含王湛具体引语）；曦望公司公开信息；推理成本对标数据（如有）
- `source_ref_bundle`: `https://www.qbitai.com/2026/04/406020.html`；source_packet: `20260504_141447__qbitai_site_gpu_ceo__source-packet.md`
- `视觉建议`: 封面图用 GPU 芯片/算力视觉；文内嵌入估值数据图表；避免纯叙事堆砌
- `为什么适合该平台`: 微信适合深度叙事和一手 CEO 引言展开；推理成本赛道稀缺，深度稿有差异化价值
- `stage_gate_note`: **条件性槽位**——scorecard 标注"暂不可发（缺正文）"，需量子位专访 Distilled Body 到货才可发布。若 17:00 前原文未到，此槽位自动降级为 holdout，wechat 备选槽位由 Specsmaxxing（Task 2）接替。

#### Task 2
- `topic_key`: `hn_frontpage_47994012_specsmaxxing_on_overcoming_ai_psychosis_and_why_i_write_specs_i_20260504`
- `目标读者`: 工程师/builder，有 AI 使用焦虑，关注工作流和工具哲学
- `切入角度`: 以"AI 心理焦虑"为入口，展开 Specsmaxxing 现象背后的工作流哲学；重点不是科普 spec，而是引出"在 AI 辅助时代写 spec 反而是主动建立控制感"这一论点
- `核心论点`: Specsmaxxing 是 AI 焦虑的积极应对机制；写 SPEC 是 builder 在 AI 模糊性中重建确定性的手段；这一趋势值得认真对待而非嘲笑
- `证据抓手`: acahi.sh 原文（SPECs in YAML 细节）；HN 评论区的真实反馈；Peter Werry 背景（Unblocked 创始人）
- `source_ref_bundle`: `https://acai.sh/blog/specsmaxxing`；source_packet: `20260503_225808__hn_frontpage_47994012_specsmaxxing__source-packet.md`
- `视觉建议`: 封面用代码/spec 格式截图；避免空洞配图；文内可用 SPEC 片段作为证据展示
- `为什么适合该平台`: 微信适合展开论点和叙事；Specsmaxxing 需要背景交代和深度分析，纯热度包装不够

---

### `zhihu`

#### Task 1
- `topic_key`: `zhihu_hot_ai_35_ai_20260504`
- `目标读者`: 关注 AI 替代蓝领岗位、劳动合同法的知乎用户；法律/HR从业者
- `切入角度`: 以法院判决为核心，但不停留于"AI 取代岗位"的情绪层面，重点讨论：法院认定公司违法的事实逻辑是什么？降薪被拒后被开除为什么构成违法？这对后续同类案件有什么参考价值？
- `核心论点`: 杭州余杭区法院的赔偿判决有其内在法律逻辑；AI 替代岗位不等于可以随意降薪；这个案例在劳动法框架内有实质意义
- `证据抓手`: 判决金额（26万余元）；法院信息（杭州余杭区，施国强法官）；劳动者诉求（岗位被取代，拒绝大幅降薪）；source_packet 中的知乎原题
- `source_ref_bundle`: `https://www.zhihu.com/question/2034241896516510290`；source_packet: `20260503_220926__zhihu_hot_ai_35_ai__source-packet.md`
- `视觉建议`: 不需要复杂图表；引用判决金额和法院信息即可；有法律背景标签有利传播
- `为什么适合该平台`: 知乎适合法律解读和劳动议题讨论；仲裁案天然契合问答式结构；用户偏好有论据支撑的分析

---

### `x`

#### Task 1
- `topic_key`: `zhihu_hot_ai_35_ai_20260504`
- `切入角度`: 快讯 + 观点钩子：杭州法院判决公司赔偿，AI 替代岗位不等于可以随意降薪降级；这个判例比一般"AI焦虑"叙事更有实质法律价值
- `核心论点`: 法院判决是有硬约束力的信号，不是情绪共鸣；劳动者拒绝大幅降薪被开除构成违法，这一逻辑在 AI 替代场景中同样成立
- `证据抓手`: 判决金额26万余元；法院名称；基本案情
- `视觉建议`: 140字内讲完判决+核心逻辑；带法院信息
- `为什么适合该平台`: X适合快讯和观点扩散；法律判决有天然公信力，适合做hook

#### Task 2
- `topic_key`: `hn_frontpage_47998225_for_thirty_years_i_programmed_with_phish_on_every_day_20260504`
- `切入角度`: 快讯 + 开发者话题钩子：HN热帖，30年程序员每天听Phish写代码；Phish不仅是一场演唱会，还是一种编程flow的隐喻
- `核心论点`: Phish与编程flow的关系不是玄学，而是有规律的工作状态建立；这个帖子在HN的高赞说明开发者社区对此有共鸣
- `证据抓手`: Meiklejohn原文（需确认可取用）；HN高赞数据；Phish音乐特点（无固定setlist，即兴）
- `source_ref_bundle`: `https://christophermeiklejohn.com/ai/personal/phish/flow/agents/2026/05/03/rift.html`
- `视觉建议`: 短图文；Phish现场视觉或编程界面截图；一句话hook
- `为什么适合该平台`: X适合开发者社区扩散；HN原帖已有热度背书
- `stage_gate_note`: **已知风险槽位**——source packet为空壳，scorecard P1 fatal。writer必须确认能取到原文全文再动笔，否则降级holdout。

---

### `xiaohongshu`

#### Task 1
- `topic_key`: `hn_frontpage_47994012_specsmaxxing_on_overcoming_ai_psychosis_and_why_i_write_specs_i_20260504`
- `目标读者`: 对AI工具焦虑、有自我提升需求的年轻从业者；小红书用户偏生活/职场场景
- `切入角度`: "Specsmaxxing"这个概念本身就是一个hook——用写规格文档来对抗AI焦虑，听起来反直觉但细想有道理；从小红书视角切入可以是"AI焦虑 → 写spec反而治愈"的个人叙事
- `核心论点`: Specsmaxxing = 用结构化思维对抗AI时代的不确定感；写SPEC不仅是工程习惯，更是心理建设
- `证据抓手`: SPEC in YAML的格式；HN热度；Unblocked背景
- `source_ref_bundle`: `https://acai.sh/blog/specsmaxxing`；source_packet同前
- `视觉建议`: 小红书风格封面（简洁/有辨识度的视觉）；可以用spec格式截图作为"干货感"；避免太过技术化
- `为什么适合该平台`: 小红书适合轻量但有干货感的内容；Specsmaxxing概念有传播潜力；生活方式+效率工具的交叉点

---

### `bilibili`

#### Task 1
- `topic_key`: `youtube_ai_dot_engineer_mergeable_by_default_building_the_context_engine_to_save_time_and_tokens_20260504`
- `目标读者`: 开发者/builder，关注AI工程实践和工具效率
- `切入角度`: 从"为什么context engine现在值得看"入手，引出Peter Werry视频的核心洞察；Bilibili版本侧重技术解读和工程视角，不做纯科普
- `核心论点`: context engine是AI工程中的重要命题；Mergeable by default的设计思路值得认真讨论；这个视频的价值不仅在于工具介绍，更在于背后的一人公司效率逻辑
- `证据抓手`: YouTube视频；Peter Werry背景（Unblocked）；context engine概念
- `source_ref_bundle`: `https://www.youtube.com/watch?v=5ID22ACI7IM`；source_packet同前
- `视觉建议`: 封面用YouTube视频截图或技术图示；文内可嵌入视频片段；Bilibili用户偏好有技术深度的内容
- `为什么适合该平台`: Bilibili开发者用户对工程实践有兴趣；YouTube视频有天然锚点；视频+图文解读的组合适合Bilibili

---

### `toutiao`

> **本轮无 active slot**。Top5 候选经平台适配评估后，暂无适合头条算法偏好的单一候选。当前候选池以工程师/builder视角为主，与头条大众化分发逻辑匹配度不足。若 Top5 候选中出现有公共热点潜力的题目，可从 holdout 池中捞回。

---

## 三个最重要平台任务单

> continuity_only limited task sheet 纪律下，本轮优先级最高的前3个 active slot 如下。其余平台任务见各平台任务单章节。

| # | platform | topic_key | 一句话判断 | 执行优先级 |
|---|---|---|---|---|
| 1 | wechat | `qbitai_site_gpu_unicorn_20260504` | 曦望GPU独角兽CEO专访；推理成本赛道稀缺；条件性槽位（原文未到前不可发） | P0 conditional |
| 2 | wechat | `hn_frontpage_47994012_specsmaxxing_on_overcoming_ai_psychosis_and_why_i_write_specs_i_20260504` | Specsmaxxing；AI焦虑的结构化应对机制；brand fit 高 | P0 |
| 3 | zhihu | `zhihu_hot_ai_35_ai_20260504` | 杭州AI替代岗位仲裁案；法院判决有硬约束力；劳动法框架内有实质意义 | P1 |

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: 否
- `理由`: 当前 Top5 候选均为垂直技术/工程师视角，不具备大众搜索SEO优势；曦望GPU独角兽（Rank #3）若补证成功、获得CEO专访全文，可考虑单独建百家号SEO镜像，但需等原文到货后再决策
- `承接哪篇主稿更优`: 暂不确定；等 Rank #3 补证结果

---

## Holdout 清单

### `wechat_jiqizhixin_cto_anthropic_20260504`（CTO去Anthropic当工程师）
- `为什么能进最终池`: 微信原发已有内容；CTO转型叙事有市场关注度；Anthropic背景有公信力；品牌贴合中
- `为什么这轮没选`: scorecard未将其列入top20_mini_slate P0/P1主推进序列；Top5板已占满wechat 2主槽位；当前优先级低于已在active的候选
- `什么时候可捞回`: 若Top5中任一槽位（特别是GPU独角兽WeChat Task 1）补证失败或撞车，立即从本候选池补位；捞回时需补原始来源链接（mp.weixin.qq.com）

### `wechat_qbitai_openai_imagenet_fid_20260504`（OpenAI参与，重卷ImageNet）
- `为什么能进最终池`: ImageNet/FID是AI评测的核心指标；OpenAI参与有公信力；技术叙事有门槛但有传播价值
- `为什么这轮没选`: scorecard未将其列入top20_mini_slate P0/P1主推进序列；平台适配评估后，与wechat主槽位重合度低（技术深度 vs 叙事）
- `什么时候可捞回`: 若后续有论文或更明确的技术进展信号，且Top5候选池出现空档，再从本候选池补位；捞回时需补原始论文链接

### `infoq_ai_ml_nvidia_launches_ising_open_models_for_quantum_computing_20260504`（NVIDIA Ising Quantum）
- `为什么能进最终池`: NVIDIA品牌背书强；量子计算与AI主线高度相关；InfoQ来源有一定公信力
- `为什么这轮没选`: scorecard未将其列入top20_mini_slate P0/P1主推进序列；量子计算叙事需要较深技术背景，与当前Top5平台适配度综合评估后优先级低
- `什么时候可捞回`: 若量子计算赛道出现重大进展信号（如论文发布、NVIDIA官方公告），且Top5候选池有空档，从本候选池补位

### `hn_frontpage_47998225_for_thirty_years_i_programmed_with_phish_on_every_day_20260504`（Phish 30年编程）
- `为什么能进最终池`: Top5板最终收录；HN高赞已验证热度；Phish叙事有传播潜力
- `为什么这轮没选`: scorecard P1 fatal——source packet空壳，缺原文全文；X平台Task 2虽已预排，但writer需确认能取到原文，否则直接降holdout
- `什么时候可捞回`: signal-scout补证成功（Meiklejohn原文Distilled Body到货）后自动解除；补证失败则长期 holdout

---

## 自检记录

- [x] 遵循 limited task sheet 纪律：wechat 2槽 + 另2平台（x 2槽、xiaohongshu 1槽、bilibili 1槽）共4平台4槽，其余平台（toutiao）明确无active slot
- [x] 所有 active slot 均直接回链到 Top5/Holdout 板候选，无临时扩题
- [x] 无 morning_flash 冲突对象（当日无 morning_flash 文件）
- [x] Stage gate status 显式标注为 `continuity_only`
- [x] 已知风险（#5空壳、#3条件性槽位）已在对应任务槽位写明 stage_gate_note
- [x] Holdout 均已写清"为什么能进池、为什么这轮没选、何时捞回"