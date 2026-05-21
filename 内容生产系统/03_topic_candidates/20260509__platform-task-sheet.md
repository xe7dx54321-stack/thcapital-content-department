# 平台任务单 — 2026-05-09

- `date`: `2026-05-09`
- `owner`: `topic-planner`
- `generated_at`: `2026-05-09 16:24 CST`
- `input_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260509__top20-screening-pack__reworked.md`
- `top5_board`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260509__daily-top8-to-top5.md`
- `scorecard`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260509__top20__stage-gate-scorecard.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `rework + continuity_only；Top5 板为 final continuity_only；本单为 limited task sheet，wechat 2 槽 + 另外最多 2 个平台各 1 槽，其余写 holdout`
- `morning_flash_lane`: `no-op（bundle 3/8 under target，无重叠对象）`

---

## 全局主池 Top6（来自当日 Top5/Holdout 可追溯候选池）

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|---|---|---|---|---|
| 1 | `hn_frontpage_48066592_teaching_claude_why_20260509` | P0 continuity；Anthropic 官方研究，AI 安全 + 可解释性主线，高扩散，HN 实分 29 | AI 安全/可解释性是 builder/agent 主线的硬支撑，官方背书，无时效问题 | partial source：正文需补 Anthropic 官方博客全文；正文不得以 HN 标题层代替原始论证 |
| 2 | `36kr_ai_ipo_20260509` | P0 continuity；IPO 稀缺标的 + 高时效，blended=28 | 机器人 IPO 赛道稀缺性，中国制造业 AI 化信号 | scorecard P0-2 fatal：source packet 几乎全为站点导航垃圾文本；正文必须先补 IPO 公司名称/业务/财务数据，不得以导航页代替 |
| 3 | `openai_news_running_codex_safely_at_openai_20260509` | P1 continuity 升级；yes source，官方一手，AI 安全主线，blended=25 | Codex 是 AI coder 能力的真实战场；OpenAI 官方安全叙事与 builder 主线强共振 | 同源内容已三次出现在 OpenAI News slot（#13/#14/#15 去重后保留此条）；正文需补抓全文，不得仅凭标题写稿 |
| 4 | `hn_frontpage_48066524_ai_is_breaking_two_vulnerability_cultures_20260509` | P1 continuity；HN partial source，有扩散热度，有讨论空间 | 安全 / 文化交叉叙事天然适合微信改写和知乎展开 | partial source：HN 信号（32pts/1 comment）极弱；正文需补原始博客全文；不适合小红书（无中文传播证据） |
| 5 | `36kr_ai_deepseek_token_20260509` | P2 continuity；DeepSeek Token 重组，partial source，blended=25 | Token 价格战是 2026 年 AI 基础设施的核心叙事之一 | partial source；正文需补 Token 价格数据 / 市场份额原始来源 |
| 6 | `youtube_ai_dot_engineer_agentic_search_for_context_engineering_leonie_monigatti_elastic_20260509` | Holdout P2；Agentic Search 技术叙事，Elastic 官方博客，blended=23 | 搜索是 AI agent 落地的关键场景；Elastic 有品牌可信度 | YouTube 来源；正文需补 Elastic 官方博客原文；暂不适合今日主战场优先级 |

---

## 六个主战场任务单

### `wechat`

#### Task 1
- `topic_key`: `hn_frontpage_48066592_teaching_claude_why_20260509`
- `目标读者`: AI/Agent 开发者、创业者、一人大厂 builder；关注 AI 安全与产品竞争力平衡的从业者
- `切入角度`: Anthropic 主动公布"为什么 AI 会犯错"的内部研究 → 不是示弱，是 AI 安全的真正壁垒 → 对 builder 的启示：可解释性 = 下一代产品竞争力
- `核心论点`: 1）Claude Why 研究揭示了 AI 推理过程存在"隐性置信度错配"；2）Anthropic 将此公开是安全优先文化的体现；3）对开发者而言，理解 AI 的"不知道自己不知道"是构建可靠 agent 系统的必修课
- `证据抓手`: Anthropic 官方博客全文（需补抓）→ 原文关键数据：Claude 在复杂推理任务中的错误模式分类；对比 GPT-4 / Gemini 的同类研究
- `source_ref_bundle`:
  - 主源：`https://www.anthropic.com/research/teaching-claude-why`
  - 备用：`/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_062235__hn_frontpage_48066592_teaching_claude_why__source-packet.md`
- `视觉建议`: 封面图建议用 Claude 推理链示意图（Anthropic 官方配图优先）；内文插入"AI 不知道自己不知道"类比图；可做 3 格信息图展示错误模式分类
- `为什么适合该平台`: 微信适合深度叙事和完整论证；AI 安全 + builder 主线是同行资本的核心叙事轴；正文需要补全原始证据后才能发出，不得以 HN 标题 / 摘要代替

#### Task 2
- `topic_key`: `36kr_ai_ipo_20260509`
- `目标读者`: 关注中国 AI / 机器人赛道的投资者、从业者、分析师
- `切入角度`: 机器人 IPO 赛道升温 + 中国制造业 AI 化进入收获期；这家公司比宇树更早 IPO 说明什么？
- `核心论点`: 1）机器人 IPO 窗口已开，稀缺标的受到二级市场关注；2）IPO 时间线反映公司商业化成熟度；3）赛道内公司管线对比（需补一手数据）
- `证据抓手`: 36氪原文（需补全站点导航层，获取公司名称/业务/财务数据）；Unitree 招股书公开数据做对比参照
- `source_ref_bundle`:
  - 主源：`https://www.36kr.com/p/3800408468959745`
  - 备用：`/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_230717__36kr_ai_ipo__source-packet.md`
- `视觉建议`: 封面图建议做 IPO 时间线对比（宇树 vs 该公司 vs 其他机器人标的）；插入行业赛道图谱
- `为什么适合该平台`: 36氪深度商业分析是微信读者熟悉的叙事模式；正文必须在补全 IPO 公司名称/财务数据后才能发出，当前 source packet 状态不可直接引用
- `补证触发条件`: signal-scout 补全 IPO 公司实质内容后自动解除阻断；补证完成前 content-writer 不得以此为核心卖点

---

### `xiaohongshu`

#### Task 1
- `topic_key`: `hn_frontpage_48066524_ai_is_breaking_two_vulnerability_cultures_20260509`
- `目标读者`: 对 AI 安全感兴趣的中文互联网用户；对"漏洞文化"概念有好奇心的普通读者
- `切入角度`: "AI 正在打破两种漏洞文化"——安全研究员 / 开发者 / 普通用户对 AI 失误的容忍逻辑完全不同；这是一个被 AI 放大的认知撕裂
- `核心论点`: 1）传统软件有" Responsible Disclosure"文化；AI 时代这个边界模糊了；2）两种文化冲突 → 普通用户觉得 AI 失误应该"零容忍"，开发者知道这是不可能的；3）这个裂缝在 AI 产品化中被放大
- `证据抓手`: Jeff TK 博客原文（需补全 HN 高赞讨论语境）；可对比传统 CVSS 漏洞评分 vs AI 失误的模糊地带
- `source_ref_bundle`:
  - 主源：`https://www.jefftk.com/p/ai-is-breaking-two-vulnerability-cultures`
  - 备用：`/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_062235__hn_frontpage_48066524_ai_is_breaking_two_vulnerability_cultures__source-packet.md`
- `视觉建议`: 封面用"两种文化冲突"类比图；可做"安全研究员 vs 普通用户"的双视角信息图；小红书版本侧重故事感而非技术深度
- `为什么适合该平台`: 小红书擅长"认知冲突 / 观点撕裂"类话题；但本话题无中文 HN 传播证据，属于文化翻译型选题；正文需补原始博客全文确保内容深度

---

### `x`

#### Task 1
- `topic_key`: `openai_news_running_codex_safely_at_openAI_20260509`
- `目标读者`: AI 开发者、技术从业者、关注 OpenAI 实际进展的专业社区
- `切入角度`: OpenAI 官方发布 Codex 安全运行白皮书 → Codex 已在生产环境部署 → AI coding agent 的安全问题从理论进入实战
- `核心论点`: 1）Codex 是目前最接近生产级别的 AI coding agent；2）OpenAI 主动发布安全运行报告说明安全与性能已可兼顾；3）对国内 AI coding 赛道的启示
- `证据抓手`: OpenAI 官方博客全文（需补抓）；可对照 GitHub Copilot Enterprise 安全报告
- `source_ref_bundle`:
  - 主源：`https://openai.com/index/running-codex-safely`
  - 备用：`/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260508_062235__openai_news_running_codex_safely_at_openai__source-packet.md`
- `视觉建议`: 封面用 Codex 架构图（OpenAI 官方图优先）；140 字快讯钩子 + 链接到全文；可附 Codex 安全报告核心数据点列表
- `为什么适合该平台`: X/Twitter 是 AI 技术从业者获取一手信息的首选；OpenAI 官方来源在 X 上有天然传播势能；适合快讯 + 观点钩子，图文要求简洁

---

### `zhihu`

（今日无 active slot；候选已在小红书 / X 分散；如需扩展参见 holdout）

### `bilibili`

（今日无 active slot；候选池无 B 站原生热点；参见 holdout）

### `toutiao`

（今日无 active slot；候选池无头条原生热点；参见 holdout）

---

## 三个最重要平台任务单

### 第一优先级｜Teaching Claude Why — wechat 主稿

- `topic_key`: `hn_frontpage_48066592_teaching_claude_why_20260509`
- `平台`: wechat
- `任务类型`: 深度叙事主稿
- `核心判断`: P0 continuity；Anthropic 官方研究 + AI 安全主线 + 高扩散潜力；blended=29；品牌贴合度高；补证条件已注触发
- `今日可开始条件`: signal-scout 补抓 Anthropic 官方博客全文后立即解锁
- `风险`: 补证未完成前不得以 HN 标题代替原始论证

### 第二优先级｜Running Codex safely at OpenAI — X 快讯 + 钩子

- `topic_key`: `openai_news_running_codex_safely_at_openai_20260509`
- `平台`: X
- `任务类型`: 快讯 / 观点钩子 + 全文链接
- `核心判断`: P1 continuity 升级 yes source；OpenAI 官方一手；AI coding agent 安全叙事；blended=25；正文需补抓 OpenAI 官方博客全文
- `今日可开始条件`: 补抓 OpenAI 博客全文后可立即发布 X 版本；正文深度稿可并行补证
- `风险`: 同源内容三连去重后保留此条，不得重复发

### 第三优先级｜比宇树机器人更早上春晚的公司，要敲钟 IPO 了 — wechat 深度分析

- `topic_key`: `36kr_ai_ipo_20260509`
- `平台`: wechat
- `任务类型`: 深度分析主稿（secondary slot）
- `核心判断`: P0 continuity；IPO 稀缺标的；blended=28；但 scorecard 明确 P0-2 fatal：source packet 全为站点导航垃圾文本
- `今日可开始条件`: **阻断状态**——必须等 signal-scout 补全 IPO 公司名称 / 业务 / 财务数据；补证前 content-writer 不得以此为核心卖点
- `风险`: fatal evidence gap；若今日补证完成，顺位替换 36kr DeepSeek Token 进入 wechat slot 2

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: **否**
- `理由`: 本日主池候选（Teaching Claude Why / 36kr AI IPO / Running Codex / AI vulnerability cultures / DeepSeek Token）均属于"解读型 / 分析型"内容而非"事件型 / 数据型"内容；SEO 镜像层优先承载有明确搜索意图答案的事件型 / 数据型选题；本日候选不具备足够的独立搜索价值，适合作为主稿的 SEO 导流段落而非独立百家号文章
- `承接哪篇主稿更优`: 若未来某日有"DeepSeek Token 价格数据"或"机器人 IPO 标的对比"类数据型选题，可考虑升格；今日不立

---

## Holdout 清单

### `36kr_ai_deepseek_token_20260509`
- `为什么能进最终池`: DeepSeek Token 价格战是 2026 年 AI 基础设施核心叙事之一；36kr 来源在中国市场有认知基础；blended=25 居 Top20 中位
- `为什么这轮没选`: continuity_only limited sheet 已用满 wechat 2 + xiaohongshu 1 + X 1 共 4 个 active slot；DeepSeek Token 与 AI vulnerability cultures 存在部分叙事重叠（均涉及 AI 行业结构性变化）；Token 价格数据 source packet 仍为 partial
- `捞回条件`: 当任意 active slot 补证失败或撞车时，优先接力；补证条件：signal-scout 提供 Token 价格原始数据 / 市场份额对比

### `youtube_ai_dot_engineer_agentic_search_for_context_engineering_leonie_monigatti_elastic_20260509`
- `为什么能进最终池`: Agentic Search 是 AI agent 落地的关键技术路径；Elastic 官方博客有品牌可信度；HN 有讨论热度
- `为什么这轮没选`: YouTube 来源正文获取难度高；内容为技术博客改写，非视频原生；暂不适合任何主战场的今日优先级
- `捞回条件`: signal-scout 补抓 Elastic 官方博客全文后重新评估；优先进入 zhihu 或 bilibili 的技术深解读槽位

### `google_blog_ai_see_what_happens_when_creative_legends_use_ai_to_make_ads_for_small_busi_20260509`
- `为什么能进最终池`: Google 官方营销案例，yes source，AI + 创意营销主线有品牌价值
- `为什么这轮没选`: continuity_only limited slot 已满；该话题更偏营销创意而非 AI 技术 / 商业分析，与同行资本 builder 主线贴合度弱
- `捞回条件`: 若强候选补证失败需要替换，且 signal-scout 能补全该案例的 AI 实际效果数据，可作为小红书创意类内容替补

### `wechat_jiqizhixin_shidai_shaotuan_20260509`
- `为什么能进最终池`: 知乎 370 万热度具参考价值；MiniMax 用户疑问具代表性；问答形式适合微信改写
- `为什么这轮没选`: scorecard 无该题归类（来源为 wechat 公众号二次抓取，非 Top20 原生）；泛娱乐 / 流量明星赛道与同行资本 builder 主线贴合度弱；mini_slate 5 个候选已充分占用有限 active slot
- `捞回条件`: signal-scout 补全 MiniMax 官方技术说明后，若该题能升级为"大模型对话能力实证分析"则可重新评估；目前暂缓

---

## 纪律检查清单

- [x] `stage_gate_status=continuity_only` 已在文档头注明确认
- [x] wechat active slots ≤ 2（实际 2 个）
- [x] 非 wechat 平台 active slots ≤ 2（实际 xiaohongshu 1 + X 1 = 2 个）
- [x] 所有 active slot 均直接回链到 Top5/Holdout 板候选，无临时扩题
- [x] 已排除 morning_flash 同题（morning_flash 本轮 no-op，无重叠对象）
- [x] 所有 partial source 候选均标注补证触发条件
- [x] 36kr AI IPO 在文档内明确标注 fatal evidence gap，不得绕过补证直接写稿
- [x] holdout 均附捞回条件
- [x] baijiahao 给出明确"不立"判断及理由
