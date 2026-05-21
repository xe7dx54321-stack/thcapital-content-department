# 平台任务单 — Day Mainline

- `date`: `2026-04-25`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-25 18:42:00 CST`
- `input_top20_scorecard`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260425__top20__stage-gate-scorecard.md`
- `input_top5_board`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260425__daily-top8-to-top5.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `rework + continuity_only；Top5板为continuity recovery板；本单为limited task sheet`
- `excluded_overlap_check`: `morning_flash（6 items, 20260425__morning-flash-source-bundle.md）已检查；Vision Banana未进入morning_flash，不触发同题排除；其余Top5候选与morning_flash重叠但被纳为continuity保底，符合limited sheet规则`

---

## 全局主池 Top6（来自当日Top5/Holdout建议板）

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|---|---|---|---|---|
| 1 | ai-agent-ecosystem | 涂鸦"班长"对话：AI Agent生态共赢叙事，180万开发者/10亿设备数据为锚 | Agent落地贴近产业，生态视角有差异化；明星创始人背书利于传播；微信主战场核心题 | 媒体二次加工，一手性弱；需补TUYA官网开发者大会截图+180万开发者原链 |
| 2 | deepseek-v4-benchmark | 实测DeepSeek-V4烧1000万token，4条具体发现（智能体编程/IMO/过度思考/价格缓存） | 当周最热模型话题；实测内容在开发者社区强传播；HF官方博客+实测双源交叉 | P1：signal_summary缺具体发现；降温"登顶"叙事；补26张截图具体结论 |
| 3 | deepseek-v4-technical | DeepSeek V4四大技术秘方（梁文锋），benchmark降温为"逼近第一梯队" | 模型发布是最硬一手信源；创始人公开技术路线对投资研究直接价值；科技+资本双圈破圈 | 候选6重叠需淘汰；降温"登顶"叙事；补HF博客架构层分析 |
| 4 | minimax-cannes-ai-art | MiniMax登上戛纳：AI与艺术的全球和解 | 中国AI公司出海标志性事件；AI+艺术跨圈层好题材；戛纳天然高关注度 | P2：无官方来源；数据点不足；需补MiniMax戛纳官方新闻稿 |
| 5 | vision-banana-google-ai-vision | 谷歌Vision Banana刷新2D/3D多项SOTA，何恺明谢赛宁参与 | Google发布+多项SOTA强一手信号；学术圈背书提升可信度；跨学术+产业破圈 | P2：媒体二次报道，需回链Google Research/arXiv；量子位编辑叙事可能放大 |
| 6（holdout） | ai-car-evolution | 大模型上车两年复盘：为什么「真·AI汽车」现在才出现？ | AI+汽车硬核赛道；两年复盘视角有深度；行业问题意识强 | 优先级低于Top5主槽位；缺具体车型/厂商数据 |

---

## 六个主战场任务单

### `wechat`

#### Task 1
- `topic_key`: `ai-agent-ecosystem`
- `目标读者`: AI从业者、开发者、创业者；关心Agent落地和产业生态的投资者
- `切入角度`: 以涂鸦"班长"对话事件为入口，深挖：这个信号对Agent/builder/一人公司主线意味着什么，生态共赢的逻辑是什么
- `核心论点`: AI Agent时代需要生态协同而非单点突破；涂鸦的180万开发者/10亿设备是当前最具体的生态证明；这个对话揭示的产业逻辑值得深入拆解
- `证据抓手`: 对话原文关键引述；涂鸦官网开发者大会截图；180万开发者/10亿设备原始链接；产品落地数据
- `source_ref`: `https://mp.weixin.qq.com/s/2UoLRM7TydnnQ-dhcUQtzg`
- `视觉建议`: 涂鸦产品截图；对话现场图片；生态协同结构图（开发者/设备/场景三角关系）
- `为什么适合该平台`: 微信适合承载完整叙事+深度判断；此对话有产业纵深，值得3000字以上展开；创始人对谈形式在微信传播有优势

#### Task 2
- `topic_key`: `deepseek-v4-benchmark`
- `目标读者`: AI开发者、技术决策者；关注大模型能力和成本变化的投资者
- `切入角度`: 实测切入，用4条具体发现（智能体编程60分钟自主/IMO难题优缺点/轻量级任务过度思考翻车/价格上调+缓存降成本）做叙事锚点，不要停留于"惊喜/意外"的感性描述
- `核心论点`: DeepSeek-V4实测揭示大模型推理的工程真实：benchmark登顶不等于实际好用；4条具体发现构成对模型能力的真实画像
- `证据抓手`: 实测原文4条具体结论；HuggingFace官方博客模型规格；token消耗记录/截图佐证
- `source_ref`: `https://mp.weixin.qq.com/s/2QGjDDibkYA3yef35PTBZw`
- `视觉建议`: benchmark对比图表（若有）；token消耗截图；实测过程关键画面
- `为什么适合该平台`: 微信适合深度评测类内容；实测有具体数据支撑，3000字左右能完整呈现；开发者群体在微信有高质量讨论基础

---

### `x`

#### Task 1
- `topic_key`: `deepseek-v4-technical`
- `目标读者`: 科技投资者、AI研究者、开发者社区；关注模型技术突破和投资价值的人群
- `切入角度`: 技术叙事+投资视角；梁文锋公开四大技术秘方，benchmark降温为"逼近第一梯队"，破"登顶"叙事；核心是技术路线背后的投资逻辑
- `核心论点`: DeepSeek V4技术路线公开揭示：中国基础模型正在逼近第一梯队；梁文锋的策略是把技术公开作为生态壁垒；这对算力投资和模型层有直接影响
- `证据抓手`: HF博客benchmark数据（SWE Verified 80.6）；梁文锋对话原文；技术路线架构图
- `source_ref`: `https://mp.weixin.qq.com/s/gTsIKShVuhhHKI_yCraLcQ`
- `视觉建议`: benchmark榜单截图；技术架构简图；梁文锋引述金句
- `为什么适合该平台`: X适合快讯+观点钩子；技术叙事+投资逻辑的结合体最适合140字以外延伸；破"登顶"叙事有推转传播潜力

---

### `zhihu`

#### Task 1
- `topic_key`: `deepseek-v4-benchmark`
- `目标读者`: 技术背景读者、研究者、深度讨论参与者；关注AI模型实际能力和局限性的社区
- `切入角度`: 实测4条具体发现展开为知乎式深度讨论：智能体编程/IMO/过度思考/价格缓存；不做"惊喜/意外"的感性总结，做可验证的工程画像
- `核心论点`: DeepSeek-V4实测揭示：大模型benchmark表现与实际工程可用性存在落差；4条具体发现构成对模型能力的诚实评估，对"登顶"叙事降温
- `证据抓手`: 实测原文具体结论；HF官方模型文档；token消耗原始截图
- `source_ref`: `https://mp.weixin.qq.com/s/2QGjDDibkYA3yef35PTBZw`
- `视觉建议`: benchmark对比表；实测结论摘要图；技术讨论配图
- `为什么适合该平台`: 知乎适合解释/对比/问答式内容；实测数据+深度分析在知乎有稳定受众；破"登顶"叙事引发技术圈讨论

---

### `bilibili`

#### Task 1
- `topic_key`: `deepseek-v4-technical`
- `目标读者`: 科技爱好者、开发者、关注AI前沿的年轻受众；视频内容重度消费者
- `切入角度`: 梁文锋公开四大技术秘方+benchmark降温叙事；做成"中国AI模型真实进展"科普视频，有别于"登顶"自媒体的夸张叙事
- `核心论点`: DeepSeek V4的技术路线公开揭示中国AI在基础模型层的真实进展；破"登顶"叙事，做"逼近第一梯队"的诚实解读；这对中国AI投资叙事有长期影响
- `证据抓手`: HF博客技术架构分析；梁文锋技术路线引述；benchmark数据（SWE Verified 80.6）
- `source_ref`: `https://mp.weixin.qq.com/s/gTsIKShVuhhHKI_yCraLcQ`
- `视觉建议`: 技术架构动画；benchmark数据可视化；梁文锋引述金句字幕
- `为什么适合该平台`: B站适合科普+深度内容；技术路线+投资逻辑的结合体适合10-15分钟视频；破"登顶"叙事有讨论传播潜力

---

### `toutiao`

#### Task 1
- `topic_key`: `ai-agent-ecosystem`
- `目标读者`: 泛科技读者、对AI产业动态有广泛兴趣的受众；头条流量人群
- `切入角度`: 涂鸦"班长"对话的产业意义：AI Agent生态共赢不是概念，是180万开发者和10亿设备的具体现实；AI时代的生态竞争逻辑变了
- `核心论点`: 涂鸦对话揭示：AI Agent时代的竞争单位是生态，不是单品；从180万开发者到10亿设备，生态协同效应正在形成；这对中国AI产业有直接影响
- `证据抓手`: 对话原文关键引述；涂鸦开发者生态数据；产品落地场景截图
- `source_ref`: `https://mp.weixin.qq.com/s/2UoLRM7TydnnQ-dhcUQtzg`
- `视觉建议`: 生态结构图；产品场景截图；对话现场图片
- `为什么适合该平台`: 头条推荐算法偏向产业动态和硬数据；涂鸦对话有产业标签，适合泛流量分发

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: 是，但降优先级
- `理由`: DeepSeek V4相关内容（benchmark+technical）在百家号有搜索流量；涂鸦Agent话题次之；Vision Banana不适合百家号（学术性过强）
- `承接哪篇主稿更优`: 优先承接 `deepseek-v4-technical` 微信稿，做SEO镜像；次选 `ai-agent-ecosystem` 微信稿
- `执行建议`: 百家号不做独立创作，只做微信主稿的SEO优化版本（标题+描述+关键词调整）；不单独开题

---

## 三个最重要平台任务单

### 🥇 第一优先 — `wechat` 主稿（ai-agent-ecosystem）

- `平台`: 微信
- `topic_key`: `ai-agent-ecosystem`
- `优先级`: P0
- `目标读者`: AI从业者、开发者、创业者；关心Agent落地和产业生态的投资者
- `切入角度`: 以涂鸦"班长"对话事件为入口，深挖：这个信号对Agent/builder/一人公司主线意味着什么，生态共赢的逻辑是什么
- `核心论点`: AI Agent时代需要生态协同而非单点突破；涂鸦的180万开发者/10亿设备是当前最具体的生态证明；这个对话揭示的产业逻辑值得深入拆解
- `证据抓手`: 对话原文关键引述；涂鸦官网开发者大会截图；180万开发者/10亿设备原始链接；产品落地数据
- `source_ref`: `https://mp.weixin.qq.com/s/2UoLRM7TydnnQ-dhcUQtzg`
- `视觉建议`: 涂鸦产品截图；对话现场图片；生态协同结构图（开发者/设备/场景三角关系）
- `执行注意`: continuity_only路径；正文必须先补关键一手/原始证据，再展开判断；不得把补证脚手架带进正文

### 🥈 第二优先 — `wechat` 主稿（deepseek-v4-benchmark）

- `平台`: 微信
- `topic_key`: `deepseek-v4-benchmark`
- `优先级`: P0
- `目标读者`: AI开发者、技术决策者；关注大模型能力和成本变化的投资者
- `切入角度`: 实测切入，用4条具体发现（智能体编程60分钟自主/IMO难题优缺点/轻量级任务过度思考翻车/价格上调+缓存降成本）做叙事锚点，不要停留于"惊喜/意外"的感性描述
- `核心论点`: DeepSeek-V4实测揭示大模型推理的工程真实：benchmark登顶不等于实际好用；4条具体发现构成对模型能力的真实画像
- `证据抓手`: 实测原文4条具体结论；HuggingFace官方博客模型规格；token消耗记录/截图佐证
- `source_ref`: `https://mp.weixin.qq.com/s/2QGjDDibkYA3yef35PTBZw`
- `视觉建议`: benchmark对比图表（若有）；token消耗截图；实测过程关键画面
- `执行注意`: continuity_only路径；signal_summary补全前须先补4条具体发现再开写；降温"登顶"叙事

### 🥉 第三优先 — `x` 快讯/观点（deepseek-v4-technical）

- `平台`: X
- `topic_key`: `deepseek-v4-technical`
- `优先级`: P1
- `目标读者`: 科技投资者、AI研究者、开发者社区；关注模型技术突破和投资价值的人群
- `切入角度`: 技术叙事+投资视角；梁文锋公开四大技术秘方，benchmark降温为"逼近第一梯队"，破"登顶"叙事；核心是技术路线背后的投资逻辑
- `核心论点`: DeepSeek V4技术路线公开揭示：中国基础模型正在逼近第一梯队；梁文锋的策略是把技术公开作为生态壁垒；这对算力投资和模型层有直接影响
- `证据抓手`: HF博客benchmark数据（SWE Verified 80.6）；梁文锋对话原文；技术路线架构图
- `source_ref`: `https://mp.weixin.qq.com/s/gTsIKShVuhhHKI_yCraLcQ`
- `视觉建议`: benchmark榜单截图；技术架构简图；梁文锋引述金句
- `执行注意`: continuity_only路径；不做登顶叙事，做逼近第一梯队诚实解读；适合140字以外延伸

---

## Holdout 清单

### `vision-banana-google-ai-vision`
- `为什么能进最终池`: Google发布+多项SOTA强信号；何恺明/谢赛宁参与背书；跨学术+产业双圈破圈性强
- `为什么这轮没选`: continuity_only limited sheet纪律约束（wechat 2槽，其余4平台各1槽）；视觉类话题在当前主槽位优先级低于Agent和DeepSeek
- `什么时候可捞回`: ①Top5主槽位补证失败导致任务撞车；②vision-banana出现新的Google官方公告或arXiv论文；③第二日Top5板有空间

### `minimax-cannes-ai-art`
- `为什么能进最终池`: 中国AI公司出海标志性事件；AI+艺术跨圈层好题材；戛纳天然高关注度
- `为什么这轮没选`: continuity_only limited sheet纪律约束；MiniMax官方来源未补，P2问题尚未解决；与涂鸦Agent同属生态话题，避免同质化
- `什么时候可捞回`: signal-scout补MiniMax戛纳官方新闻稿+出海数字后；或次日Top5板有空间时从holdout优先捞入

### `ai-car-evolution`
- `为什么能进最终池`: AI+汽车硬核赛道；两年复盘视角有深度；行业问题意识强
- `为什么这轮没选`: continuity_only limited sheet纪律约束；主槽位饱和；具体车型/厂商数据不足（P2未解）
- `什么时候可捞回`: signal-scout补极氪/特斯拉/华为AI上车官方来源≥2个后；或次日Top5板有空间

### `meta-amazon-ai-chip-deal`
- `为什么能进最终池`: 本bundle唯一primary_source=true；Meta采购大单反映算力投资趋势；TechCrunch英文权威源
- `为什么这轮没选`: continuity_only limited sheet纪律约束；X平台已有deepseek-v4-technical任务；英文科技话题在中文平台流量转化率存疑；Amazon/Meta官方公告尚未补证
- `什么时候可捞回`: 补Amazon/Meta官方公告后；或X平台需要算力赛道内容时优先捞入

### `claude-code-regression-anthropic-confirmed`
- `为什么能进最终池`: Anthropic官方确认是关键转折点；builder工具链信号；讨论持续性好
- `为什么这轮没选`: continuity_only limited sheet纪律约束；主槽位饱和；Anthropic官方博客/GitHub issue尚未补证
- `什么时候可捞回`: signal-scout补Anthropic官方确认原链后；次日Top5板有空间时优先捞入

---

## 任务单生产说明

- `本次平台槽位`: wechat×2 + x×1 + zhihu×1 + bilibili×1 + toutiao×1 = 6 active slots
- `来源追溯`: 6个active slots全部来自20260425 Top5/Holdout建议板候选，零临时扩题
- `morning_flash排除`: morning_flash（6 items）已全部检查；Vision Banana未进入morning_flash，不触发同题排除；Top5中与morning_flash重叠的候选（ai-agent-ecosystem/deepseek-v4-benchmark/deepseek-v4-technical/minimax-cannes-ai-art/ai-car-evolution）均已在Top5板中标注为continuity recovery保底，本次纳入任务单符合continuity_only路径
- `百家号`: 不独立开题，SEO镜像降优先级
- `supply_note`: Top20原包槽位9-20全空；本次limited task sheet 6槽来自8个可用候选，缺口说明已在holdout清单体现

---

*本任务单由 topic-planner 依据 20260425 Top20 scorecard（final, rework, continuity_only）和 Top5建议板（final, continuity_only）生成。*