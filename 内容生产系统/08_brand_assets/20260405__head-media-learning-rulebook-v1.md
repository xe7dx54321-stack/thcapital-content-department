# 头部号学习规则手册 v1

- `generated_at`: `2026-04-05 22:42:09 CST`
- `date`: `2026-04-05`
- `sample_count`: `8`
- `ready_topic_count`: `3`
- `sample_source_mix`: `机器之心×4、智东西×3、Founder Park×1`
- `source_board`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/11_frontstage/20260405__head-media-learning-board.snapshot.json`

## 一眼结论

- 先用判断或反差把人拉住，再在前 10%-15% 内补齐背景。
- 证据要早，不要让读者一直听抽象判断。
- 图片要承担证明、解释、换气三种职责，而不是只做装饰。
- 写稿时优先补证、补背景、补图，而不是遇到问题就直接换题。
- 学习不只反哺写稿岗，还要反哺 source / seed / topic 三层，持续校正“今天该追什么题”。

## 题材 × 人群 × 文风匹配表

| 题材类型 | 目标人群 | 推荐表达 | 应该做什么 | 避免什么 |
| --- | --- | --- | --- | --- |
| 事件科普 / 热点解释 | 刚听说这件事、但上下文还不完整的泛 AI 读者 | 先用白话把对象、变化、why now 讲清，再保留少量必要术语做精确表达。 | 判断先行，但前 10%-15% 内补齐背景和证据锚点。 | 一上来堆框架、堆术语，让读者半天不知道发生了什么。 |
| 产品推荐 / 工具体验 | 想马上试、想知道值不值得用的实操型读者 | 按场景、动作、收益来写；可以用体验叙述，但核心是降低试用门槛。 | 多放界面截图、流程卡、前后对比，用真实操作感替代空泛形容词。 | 只有“很好用 / 很惊艳”的感受，没有步骤、边界和证据。 |
| 产业判断 / 商业分析 | 从业者、投资人、对商业含义敏感的高意图读者 | 保持判断力度，但所有专业表达都要回到业务含义、商业变量和风险边界。 | 财务、竞争、分发、供给链等术语可以用，但要解释“这对谁有影响”。 | 把文章写成抽象行业评论，读者读完不知道能带走什么判断。 |
| 教程 / Builder 拆解 | 开发者、产品经理、AI builder、人群更愿意为方法买单 | 过程感优先，写清怎么判断、怎么验证、卡在哪、适用边界是什么。 | 多用步骤卡、结构图、变量表，给人“看完能照着做”的感觉。 | 只给结论不给路径，只晒结果不说前提。 |
| 观点 / 争议型题材 | 已经感知到热度、想看更高层判断的人 | 第一屏亮立场，但立刻补证据和边界，避免把“敢说”写成“乱说”。 | 把误判点、反直觉点和证据链一并前置。 | 只有态度没有证据，或者只用狠话制造情绪。 |

## 选题判断复盘

| 视角 | 题材带 | 样本数 | 代表对象 | 为什么会被选中 |
| --- | --- | --- | --- | --- |
| 头部号样本 | 模型 / 研究进展 | 5 | 大模型SFT后效果≠RL潜力！港科大、阿里提出自适应冷启动新范式；AI 视频生成的战场如何从「模型秀场」转向「工作流」？ | 这类题能代表前沿，但需要快速翻译成“到底多了什么能力、对谁有影响”。 |
| 头部号样本 | 综合 / 其他 | 2 | 全网开骂！Claude订阅「封杀」OpenClaw，想用龙虾？得加钱！；11人，年入3000万美元，被OpenAI收购了 | 这类题材目前还偏混合，说明系统需要继续积累更稳定的分类经验。 |
| 头部号样本 | 机器人 / 硬件 / 具身智能 | 2 | 从任务专用到通用智能：基础模型重塑具身导航；机器人舞姿爆红背后：具身智能行业“卡脖子”难题，终于有了新解法 | 这类题自带强画面和具象对象，但如果没有用户 stakes，容易只剩酷炫而缺少转译。 |
| 头部号样本 | 视频 / 多模态 / 语音 | 1 | AI 视频生成的战场如何从「模型秀场」转向「工作流」？ | 这类题更容易被头部号选中，因为天然有产品感、演示感和大众入口。 |
| 我们已下发主池 | 开源 / Infra / 推理优化 | 3 | We gave 12 LLMs a startup to run for a year. GLM-5 nearly matched Cla… | 这类题适合做专业壁垒和品牌判断，但首屏必须更早翻译成普通读者能感知的意义。 |
| 我们已下发主池 | 模型 / 研究进展 | 2 | We gave 12 LLMs a startup to run for a year. GLM-5 nearly matched Cla… | 这类题能代表前沿，但需要快速翻译成“到底多了什么能力、对谁有影响”。 |
| 我们已下发主池 | 机器人 / 硬件 / 具身智能 | 2 | Anthropic buys biotech startup Coefficient Bio in $400M deal: Reports… | 这类题自带强画面和具象对象，但如果没有用户 stakes，容易只剩酷炫而缺少转译。 |
| 我们已下发主池 | 安全 / 风险 / 漏洞 | 1 | Claude Code found a Linux vulnerability hidden for 23 years | 这类题兼具反常识、风险感和专业背书，既适合传播，也适合建立判断力。 |

## 今天我们的主池与差异化判断

| 状态 | 主题 | 题材带 | 为什么保留 |
| --- | --- | --- | --- |
| 已下发 | We gave 12 LLMs a startup to run for a year. GLM-5 nearly matched Claude Opus 4.6 at 11× lower cost. | 开源 / Infra / 推理优化 / 模型 / 研究进展 | 模型能力对比有硬数据，跨中美模型叙事，有投资参考价值；内容可延展性强（快讯 + 深度解读 + 成本分析）；证据链最完整，top3 排序修正升第1 |
| 已下发 | Claude Code found a Linux vulnerability hidden for 23 years | 安全 / 风险 / 漏洞 / 开源 / Infra / 推理优化 | AI coding 能力的真实世界证明，23 年漏洞有新闻价值，破圈到安全 / 开发 / 科技媒体多圈层 |
| 已下发 | Anthropic buys biotech startup Coefficient Bio in $400M deal: Reports | 机器人 / 硬件 / 具身智能 / 开源 / Infra / 推理优化 | AI 头部公司收购首例，有赛道标杆意义；$400M 硬数据；可关联讨论 AI + Science 投资逻辑 |
| 已下发 | Anthropic says Claude Code subscribers will need to pay extra for OpenClaw usage | 行业落地 / 医疗 / 场景翻译 | Anthropic 定价策略变动的直接证据；社区强烈反弹有持续讨论空间；影响 OpenClaw 用户实际成本；跨中文社区同步 |
| 已下发 | National Robotics Week: Latest Physical AI Research Breakthroughs | 机器人 / 硬件 / 具身智能 / 模型 / 研究进展 | NVIDIA 官方出品，一手性强；Physical AI 是 2026 年重要赛道；与机器人周时间节点吻合 |
| 池内待捞回 | Deeptune Raises $43M in Series A Funding | 融资 / 商业化 / 资本信号 / 机器人 / 硬件 / 具身智能 | 大额 A 轮，AI 方向，内容工厂关于融资入口的稳定产出 |

## 战略号轮转补位

| 来源 | 状态 | 当前学习对象 / 阻塞 | 主链记录 | 说明 |
| --- | --- | --- | --- | --- |
| 赛博禅心 | 历史回看 | 飞书出了官方 CLI，消息、文档、日历、邮箱都能用 Agent 操作了 | source_packet=4 / deep_article=4 | 该号近 7 天内暂无新 deep article，暂回看最近一篇高质量样本，避免战略学习断档。 |
| 数字生命卡兹克 | 历史回看 | 刚刚，飞书CLI开源，Claude Code也可以丝滑操控飞书了。 | source_packet=4 / deep_article=4 | 该号近 7 天内暂无新 deep article，暂回看最近一篇高质量样本，避免战略学习断档。 |
| 饼干哥哥AGI | 历史回看 | OpenClaw的最佳省钱攻略：几十块的方舟Coding Plan直接让跨境 AI 团队成本降了 90% | source_packet=4 / deep_article=3 | 该号近 7 天内暂无新 deep article，暂回看最近一篇高质量样本，避免战略学习断档。 |
| 袋鼠帝AI客栈 | 轮转补位 | 终于找到免费的本地Agent了！量大管饱，真干活～ | source_packet=4 / deep_article=1 | 主学习池仍按业务窗采样；该号本轮通过近 7 天轮转补位进入学习池，不污染当天主样本。 |

## 裁判结论

- 头部号这轮更偏 `模型 / 研究进展×5、综合 / 其他×2`，说明它们优先抓“普通读者能立刻感到 stakes”的题材。
- 我们当前已下发主池更偏 `开源 / Infra / 推理优化×3、模型 / 研究进展×2`，说明系统这轮更偏一手性、可防守性和品牌判断力。
- 裁判结论不是谁绝对更好，而是两边各赢一部分：头部号在传播势能和大众转译上更强，我们在可核验与可防守性上更稳。后续应保持“硬信号主池 + 大众 stakes 补位池”双轨，而不是二选一。
- 当前 ready 库里还有 `xreal_ar_glasses_ipo_hk_2026` 这类历史题，和今天 task sheet 已下发对象不完全同频，所以学习板后续必须同时对照“当日 task sheet + 当前 ready 稿”，不能只看现成库存。
- 头部号漏斗外题材：`综合 / 其他`｜全网开骂！Claude订阅「封杀」OpenClaw，想用龙虾？得加钱！；11人，年入3000万美元，被OpenAI收购了｜头部号在 `综合 / 其他` 连续给出样本，而我们的 Top6 主池还没覆盖，优先检查 seed / source lane 是否漏了，而不是先认定这题不值得做。
- 头部号漏斗外题材：`视频 / 多模态 / 语音`｜AI 视频生成的战场如何从「模型秀场」转向「工作流」？｜头部号在 `视频 / 多模态 / 语音` 连续给出样本，而我们的 Top6 主池还没覆盖，优先检查 seed / source lane 是否漏了，而不是先认定这题不值得做。
- 我们的差异化题材：`安全 / 风险 / 漏洞`｜Claude Code found a Linux vulnerability hidden for 23 years｜我们在 `安全 / 风险 / 漏洞` 上主动保留了更硬的一手题，但这类题一旦脱离大众语境，draft / hook / context 就必须更早补“普通人为什么该关心”。

## 岗位落地表

| 岗位 / 能力 | 现在怎么接收学习结果 |
| --- | --- |
| source-capture / citation | 每轮执行前读取规则手册里的“漏题 / 共识题”，优先补原始链接、截图和中文工作摘要，不让二手摘要直接进候选池。 |
| seed-refresh / source-scouting | 用规则手册里的“头部号今天在追什么”和“我们漏掉了什么”更新 watchlist 与动态搜源规则。 |
| signal-scout / topic-radar | 每轮执行前读取规则手册，把“确定性 + 普通读者 stakes + 题材覆盖”一起带入 Top20 / Top5 筛选。 |
| topic-approval / brand-context | 锁题时显式写清楚：为什么跟头部号同题，或为什么故意不跟；同时提醒平台束、背景桥接、证据抓手和图证计划。 |
| hook / context / draft-pack / audience | 生成初稿前读取规则手册，把题材 × 人群 × 文风匹配，以及差异化题材的背景桥接要求写进平台初稿。 |
| visual-intelligence / renderer / repurpose | 把头部号图文节奏、截图优先级和平台呈现方式转成具体视觉槽位和 handoff 资产。 |
| content-polish / review / postmortem | 精修和复盘时对照规则手册，继续更新下一轮优化项，而不是把学习停在总结层。 |

## 选题复盘反哺动作

| Owner | 下轮必须落成什么动作 |
| --- | --- |
| seed-refresh / source-scouting | 若头部号连续两轮在某题材高频而我们的 Top6 没覆盖，下轮必须补至少 2 个对应来源或动态搜源规则。 |
| source-capture / citation | 准备补位的题材必须先补一手原链、截图和中文工作摘要，再交给 radar，不允许只拿二手摘要就入池。 |
| topic-radar | 筛 Top20 时同时看“确定性”和“普通读者 stakes”，避免候选池只剩硬核技术题。 |
| topic-approval | 当最终锁的是和头部号不同的题，必须显式写明“我们为什么不跟”和“我们靠什么打赢”。 |
| draft-pack / hook / context / render | 如果坚持更垂直的差异化题，首屏必须更早补背景、利益相关性和图证，不然再好的选题也会输在转译层。 |

## 当前待优化项

- `背景桥接还要再早`｜`topic-approval + draft-pack + content-polish`｜`待优化`｜优先补对象、事件、why now，不先换题；冷启动读者必须在前屏内知道你在说什么。
- `把题材 × 人群 × 文风匹配持续沉淀到岗位规则`｜`content-analyst + core skills`｜`待优化`｜继续把长期学习结果写进稳定规则手册，并让 topic-radar、draft-pack、content-polish、visual-intelligence 每次执行时显式加载。
- `把选题判断复盘前置到 seed / source / topic 三层`｜`source-capture + seed-refresh + topic-radar + topic-approval`｜`待优化`｜让 source-capture、seed-refresh、topic-radar、topic-approval 执行前显式读取规则手册中的选题复盘，并把共识题 / 漏题 / 差异化题写回下一轮动作。
