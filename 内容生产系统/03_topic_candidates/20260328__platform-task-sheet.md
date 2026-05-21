# 平台任务单

- `date`: `2026-03-28`
- `owner`: `topic-planner`
- `generated_at`: `2026-03-28 14:04:16 CST`（14:10 CST 填入主池 + 12 槽位）
- `reworked_at`: `2026-03-28 20:55 CST`（P1 返工：supplement_evidence + rewrite_angle；后续补做 P0 一致性修复：移除 2 个不在当日 Top20 内的越界 topic_key，恢复 Top20 → 平台任务单 链路一致）
- `input_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260328__top20-screening-pack.md`
- `stage_gate_status`: `pass`
- `rework_reference`: `10_logs/20260328__platform-task-sheet__stage-gate-scorecard.md`（7.5/10 → rework，P1 三项已修复）
- `top20_gate_status`: `pass（返工后 ~8.0/10，20260328 13:14 CST）`

---

## 全局主池 Top6

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|---|---|---|---|---|
| 1 | `softbank-openai-ipo-signal` | SoftBank $40B 贷款是 2026 年 OpenAI IPO 的强信号 | JPMorgan + Goldman Sachs 联合背书，数据硬（$40B + 投行名称）；IPO 预期对 AI 一级市场估值、融资竞品格局、算力投入影响深远 | 仍是 TechCrunch 解读，非软银 / OpenAI 官方公告；需回链 SEC 文件交叉验证 |
| 2 | `kunlun-agi-three-models-2026` | 昆仑万维一口气发布 3 个模型并亮出 2026 AGI 战略，是国产大模型竞争进入“矩阵战 + 路线战”的强信号 | 中文大厂密集动作 + 3 个模型同期发布 + AGI 时间表表态 + 中关村论坛官方背书，既有产业讨论价值，也有国产模型竞争格局观察窗口 | 需回链昆仑万维官方发布会或官方公告；具体模型参数和能力仍待验证 |
| 3 | `turboquant-qwen-macbook-air` | Google TurboQuant 量化算法让 Qwen 3.5-9B 在普通 MacBook Air 本地跑通 20K context，AI 普惠硬件门槛降至消费级 | 开源推理效率硬突破（+22.8% decode，PPL 不变）；MacBook Air 即可运行，命中"AI 普惠"主线；话题跨 developer / 消费者双圈层 | Reddit 二手验证，需回链 TurboQuant 原论文 / Google 官方博客 |
| 4 | `aibuildai-mle-bench-top` | AIBuildAI 把“让 AI 自动构建 AI 模型”这件事推进到可 benchmark 的阶段，Agent 正开始吃掉部分建模工作流 | 学术 + 工业级 benchmark 验证 + AutoML + AI Agent 交叉赛道；MLE-Bench 榜单第一让话题不仅能讲概念，还能讲结果 | 需回链 UCSD 论文或 GitHub repo；中文报道可能存在信息衰减 |
| 5 | `unsloth-studio-major-update` | Unsloth Studio 重大更新：50+ 功能，推理速度追平 llama-server，llama.cpp 预编译安装体积降 50% | 硬数据密集（50+ 功能、速度提升 20-30%）；开发者生态信号；开源效率赛道持续升温；Beta 一周即重大更新迭代快 | 商业产品更新，需回链 GitHub 官方 release notes |
| 6 | `kv-dequant-turboquant-detail` | llama.cpp 实现 KV Dequant 压缩，跳过 90% V dequant，P5 Max 上 +22.8% decode at 32K context | TurboQuant 技术实现细节；benchmark 数据完整（代码 + 论文 + GitHub）；与主包 #3 强关联，形成"全景 + 深度"梯度 | 技术深，CV 受众有限；CUDA 版本未完成 |

---

## 六个主战场任务单

### `wechat`

#### Task 1
- `topic_key`: `softbank-openai-ipo-signal`
- `目标读者`: 投资机构从业者、一级市场 VC/PE、AI 赛道创业者与关注者
- `切入角度`: 产业资本视角——SoftBank $40B 贷款的结构与时机，解读为 OpenAI IPO 预备动作；波及软银自身 tech 投资组合、AI 一级市场估值锚定
- `核心论点`: JPMorgan + Goldman Sachs 联合提供 12 个月无担保贷款，信号意义强于普通融资；这步落子与 OpenAI 可能的 2026 年 IPO 直接相关，且对整个 AI 一级市场的估值基准有传导效应
- `证据抓手`: TC 原文数据（$40B、投行名称、12 个月期限）；可补充：SoftBank Vision Fund 现有持仓结构、OpenAI 历次融资估值曲线
- `source_ref_bundle`:
  - `primary`: https://techcrunch.com/2026/03/27/why-softbanks-new-40b-loan-points-to-a-2026-openai-ipo/
  - `sec_backup`: 检索 SoftBank 近期 8-K 或 IPO 相关 SEC 披露（如有）
  - `multi_source`: JPMorgan + Goldman Sachs 联席贷款结构（TC 原文 + Morningstar + TechInAsia 多源确认）
- `视觉建议`: 软银 + OpenAI 双 logo 合成图；融资估值曲线时间轴；JPMorgan + Goldman Sachs 双投行标识；人民币 / 美元双币种标注
- `为什么适合该平台`: 微信深度长文天然适合金融 + 产业交叉分析；受众有深度阅读习惯，能承接 IPO 预期推演与估值逻辑推导

#### Task 2
- `topic_key`: `kunlun-agi-three-models-2026`
- `目标读者`: 关注国产大模型竞争格局的投资人、科技从业者、AI 创业者与深度读者
- `切入角度`: 国产大模型战略视角——不是又发了一个模型，而是一家中国大厂一次性把“模型矩阵 + AGI 时间表”同时摆上桌
- `核心论点`: 昆仑万维在中关村论坛一口气发布 3 个模型并亮出 2026 AGI 战略，说明国产大模型竞争正在从单点能力比拼，转向“产品矩阵 + 路线叙事 + 战略节奏”的组合战
- `证据抓手`: 机器之心原文中的 3 模型发布信息；中关村论坛现场信息；可补昆仑万维官方公告 / 发布会材料 / 高管公开表述
- `source_ref_bundle`:
  - `primary`: https://mp.weixin.qq.com/s/g5-Y-7H1hfovmyBcB6WSqQ
  - `forum_context`: 中关村论坛现场发布信息 / 媒体跟进稿
  - `official_hint`: 昆仑万维官方公告或发布会材料（待补）
- `视觉建议`: 中关村论坛现场图；“3 个模型 + 2026 AGI”结构卡；昆仑万维战略时间线；国产大模型梯队位置图
- `为什么适合该平台`: 微信适合承接“事件 + 背景 + 战略判断”三段式分析；昆仑这条不仅能讲热度，还能讲国产大模型竞争格局

---

### `xiaohongshu`

#### Task 1
- `topic_key`: `turboquant-qwen-macbook-air`
- `目标读者`: 关注 AI 效率工具的个人用户、开发者、知识工作者、在校学生
- `切入角度`: 实用教程 + AI 普惠叙事——你的 MacBook Air 也能跑 AI 大模型了；Google TurboQuant 量化算法降门记（附实操路径）
- `核心论点`: TurboQuant 让 Qwen 3.5-9B 在普通 MacBook Air（M4, 16GB）上跑通 20000 token context；以前不可能，现在一键可行；atomic.chat 开源工具加持
- `证据抓手`: Reddit 帖子实操结果；20000 token context 测试数据；M4 MacBook Air 硬件规格；atomic.chat 开源工具
- `source_ref_bundle`:
  - `primary`: https://old.reddit.com/r/LocalLLaMA/comments/1s5kdu0/google_turboquant_running_qwen_locally_on_macair/
  - `turboquant_github`: https://github.com/TheTom/turboquant_plus
  - `tool`: https://atomic.chat（atomic.chat 开源工具，需回链完整 GitHub 地址）
- `视觉建议`: Before/After 对比图（MacBook Air + Qwen 运行界面）；量化算法原理简化图；M4 芯片规格标注；小红书封面大字："MacBook Air 跑 AI 大模型"（吸引眼球）
- `为什么适合该平台`: 小红书强视觉 + 教程类内容天然扩散；"MacBook 跑大模型"具话题性；个人开发者 / 学生受众活跃

#### Task 2
- `topic_key`: `unsloth-studio-major-update`
- `目标读者`: AI 开发者、效率工具爱好者、关注开源 LLMs 的技术人员
- `切入角度`: 新工具发现 + 效率提升——Unsloth Studio 更新了，推理速度追平 llama-server，安装体积还降一半；本周最值得试的开源工具
- `核心论点`: Unsloth Studio Beta 发布一周即重大更新：50+ 新功能，推理速度提升 20-30%，llama.cpp 预编译安装体积降 50%，Tool calling 改进，MacOS CPU 支持，uv 一行安装；下月 MLX/AMD/API
- `证据抓手`: Reddit 帖子详细 changelog；GitHub unslothai/unsloth；速度对比 benchmark
- `source_ref_bundle`:
  - `primary`: https://old.reddit.com/r/LocalLLaMA/comments/1s56q9g/new_unsloth_studio_release/
  - `github`: https://github.com/unslothai/unsloth
- `视觉建议`: Unsloth Studio 界面截图；changelog 可视化（速度提升数字突出）；安装体积对比图（降 50%）；小红书风格封面："这个开源工具让 AI 快了一倍"
- `为什么适合该平台`: 小红书技术爱好者对新工具敏感；视觉化 changelog 适合图文展示；"快一倍"类标题在小红书高点击率

---

### `zhihu`

#### Task 1
- `topic_key`: `aibuildai-mle-bench-top`
- `目标读者`: 软件开发者、AI 工程师、ML 从业者、关注 Agent 自动化边界的技术社区
- `切入角度`: 技术深拆 + 范式判断——当 AI 不再只是帮你写代码，而是开始自己搭模型、跑实验、冲榜单，这意味着什么
- `核心论点`: AIBuildAI 把“自然语言描述任务 → 自动构建 AI 模型”推进到可 benchmark 的层级，并拿到 OpenAI MLE-Bench 榜单第一；这不是又一个 Agent demo，而是 AI 正在侵入建模与实验工作流本身
- `证据抓手`: UCSD / AIBuildAI 论文或 repo；OpenAI MLE-Bench 榜单位置；机器之心中文报道中的 benchmark 描述与应用场景
- `source_ref_bundle`:
  - `primary`: https://mp.weixin.qq.com/s/8sb5CpBLb3PEQ7IGY6A5ug
  - `paper_hint`: UCSD 论文 / GitHub repo（待补）
  - `benchmark_hint`: OpenAI MLE-Bench 榜单信息（待补）
- `视觉建议`: MLE-Bench 榜单截图；AIBuildAI 工作流图；“人写模型 vs AI 自动搭模型”对比图；知乎风格结构图卡
- `为什么适合该平台`: 知乎技术社区对“Agent 正在替代哪类专业工作”很敏感；AIBuildAI 兼具技术深度和范式讨论价值，适合长答案拆解

#### Task 2
- `topic_key`: `kunlun-agi-three-models-2026`
- `目标读者`: 关注国产模型路线、AI 产业趋势与大厂战略判断的高学历读者、从业者、创业者
- `切入角度`: 产业深度分析——昆仑万维为什么要在同一时间抛出 3 个模型和 2026 AGI 战略：这不是发新品，而是向市场宣示自己的路线图
- `核心论点`: 真正值得看的不是“又发了几个模型”，而是国产大模型公司已经开始把模型矩阵、AGI 节奏和平台位置一起打包叙述；中关村论坛给了它官方舞台，也让这次动作具备了行业信号意义
- `证据抓手`: 机器之心原文中的 3 模型信息与高层表态；中关村论坛场景；可补昆仑官方稿与更完整技术参数
- `source_ref_bundle`:
  - `primary`: https://mp.weixin.qq.com/s/g5-Y-7H1hfovmyBcB6WSqQ
  - `forum_context`: 中关村论坛现场发布信息 / 媒体跟进稿
  - `official_hint`: 昆仑万维官方公告或发布会材料（待补）
- `视觉建议`: 3 模型信息对比卡；“模型竞争 → 平台竞争”逻辑图；中关村论坛现场图；知乎风格路线判断示意图
- `为什么适合该平台`: 知乎适合把大厂动作从“新闻”拆成“竞争路线图”；昆仑这条既能回答“发生了什么”，也能回答“为什么这件事重要”

---

### `x`

#### Task 1
- `topic_key`: `kv-dequant-turboquant-detail`
- `目标读者`: 开发者社区、技术评论者、开源 AI 爱好者
- `切入角度`: 技术快评——跳过 90% V dequant，+22.8% decode：TurboQuant 具体实现细节首次曝光，llama.cpp 推理效率突破进入深水区
- `核心论点`: KV dequant 占 decode 时间 40%，通过利用 attention sparsity 跳过 90% V dequant，P5 Max 上实现 +22.8% decode 提升——benchmark 数据完整（PPL 不变、NIAH 7/9→9/9），CUDA 移植进行中；这不只是数字，是开源推理效率进入深水区的明确信号
- `证据抓手`: Reddit 主线帖子（含详细 benchmark）；GitHub `https://github.com/TheTom/turboquant_plus`；论文链接；NIAH 测试数据
- `source_ref_bundle`:
  - `primary`: https://old.reddit.com/r/LocalLLaMA/comments/1s56g07/skipping_90_of_kv_dequant_work_228_decode_at_32k/
  - `github`: https://github.com/TheTom/turboquant_plus
- `视觉建议`: benchmark 数据截图（NIAH 7/9→9/9）；+22.8% 数字突出；GitHub repo 截图；X 风格：技术数据 + 一句话结论
- `为什么适合该平台`: X 是开发者社区高浓度平台；量化算法开源技术细节在 X 有高浓度受众；NIAH 测试数据可作图传播

#### Task 2
- `topic_key`: `turboquant-qwen-macbook-air`
- `目标读者`: 开发者社区、技术评论者、开源 AI 爱好者
- `切入角度`: 技术快评——TurboQuant + Qwen 在 MacBook Air 本地跑通 20K context：开源量化算法突破消费级硬件壁垒，AI 普惠再下一城
- `核心论点`: Google 量化算法开源 + Qwen 组合在消费级硬件上实现以前只有高算力设备才有的 context 长度；atomic.chat 加持；开源生态快速跟进
- `证据抓手`: Reddit 帖子 + benchmark 数据（20000 token context）；M4 MacBook Air 规格；atomic.chat 开源工具
- `source_ref_bundle`:
  - `primary`: https://old.reddit.com/r/LocalLLaMA/comments/1s5kdu0/google_turboquant_running_qwen_locally_on_macair/
  - `turboquant_github`: https://github.com/TheTom/turboquant_plus
- `视觉建议`: benchmark 截图（20000 token context）；MacBook Air 运行实拍关键帧；atomic.chat 界面截图（三选一，优先发 benchmark 数据截图，数字最抓眼球）
- `为什么适合该平台`: X 是开发者社区高浓度平台；TurboQuant + Qwen 技术组合具讨论深度；量化算法开源路线在 X 有受众

---

### `bilibili`

#### Task 1
- `topic_key`: `turboquant-qwen-macbook-air`
- `目标读者`: 程序员、学生、科技爱好者、关注 AI 工具的年轻受众
- `切入角度`: 实机演示 + 技术解读——MacBook Air 跑 Qwen 大模型：TurboQuant 量化算法全解析（视频演示 + 原理讲解）
- `核心论点`: TurboQuant 量化算法 patch 进 llama.cpp，在普通 MacBook Air（M4, 16GB）上跑通 Qwen 3.5-9B，20000 token context；以前不可能，现在可以；附 atomic.chat 开源工具实操
- `证据抓手`: Reddit 实操数据 + benchmark；M4 MacBook Air 规格；atomic.chat GitHub
- `source_ref_bundle`:
  - `primary`: https://old.reddit.com/r/LocalLLaMA/comments/1s5kdu0/google_turboquant_running_qwen_locally_on_macair/
  - `turboquant_github`: https://github.com/TheTom/turboquant_plus
  - `tool`: https://atomic.chat（atomic.chat 开源工具，需回链完整 GitHub 地址）
- `视觉建议`: B 站封面：MacBook Air + Qwen 运行界面 + 大字"消费级硬件跑大模型"；视频结构：原理简述（2 min）+ 实机演示（3 min）+ 开源工具介绍（2 min）+ 未来展望（1 min）
- `为什么适合该平台`: B 站强视觉 + 实机演示需求；技术科普视频高完播率；MacBook Air 受众与 B 站用户重叠度高

#### Task 2
- `topic_key`: `unsloth-studio-major-update`
- `目标读者`: AI 开发者、效率工具爱好者、开源社区成员
- `切入角度`: 新工具速览 + 实操演示——Unsloth Studio 重大更新：一周刷 50+ 功能，推理速度追平 llama-server（视频 + 操作演示）
- `核心论点`: Unsloth Studio Beta 一周内重大更新：50+ 功能 + 速度提升 20-30% + 安装体积降 50%；llama.cpp 预编译 + uv 一行安装；下月 MLX/AMD/API；视频演示核心新功能
- `证据抓手`: Reddit 帖子详细 changelog；GitHub unslothai/unsloth；speed benchmark
- `source_ref_bundle`:
  - `primary`: https://old.reddit.com/r/LocalLLaMA/comments/1s56q9g/new_unsloth_studio_release/
  - `github`: https://github.com/unslothai/unsloth
- `视觉建议`: B 站封面：Unsloth Studio 界面 + "50+ 新功能" + "速度快一倍"大字；视频结构：新功能速览（3 min）+ 速度对比实测（2 min）+ 安装教学（1 min）
- `为什么适合该平台`: B 站开发者内容高受众；"新工具实测"是 B 站科技板块高热度题材；速度对比实测可视化强

---

### `toutiao`

#### Task 1
- `topic_key`: `softbank-openai-ipo-signal`
- `目标读者`: 财经关注者、科技爱好者、关注 AI 大事件的大众读者
- `切入角度`: 大事件 + 数字故事——软银借出 400 亿美元，OpenAI 2026 年要上市了？华尔街两大投行联手操刀，AI 资本局生变
- `核心论点`: JPMorgan + Goldman Sachs 联合向 SoftBank 提供 12 个月无担保贷款 $40B；这笔钱的走向与 OpenAI 2026 IPO 高度相关；华尔街顶级投行已下场布局 AI 资本市场
- `证据抓手`: TC 原文数据；$40B + 两大投行名称 + 12 个月期限；OpenAI IPO 预期时间线
- `source_ref_bundle`:
  - `primary`: https://techcrunch.com/2026/03/27/why-softbanks-new-40b-loan-points-to-a-2026-openai-ipo/
- `视觉建议`: 头条封面：大数字"$400亿" + 软银 + OpenAI 双 logo；数字突出华尔街两大投行；图文结构：事件（1段）+ 数字解读（1段）+ IPO 预期（1段）+ 结尾悬念
- `为什么适合该平台`: 头条大众财经受众；$400亿 + IPO + 顶级投行组合具强吸引力；大事件解读 + 数字故事化写法契合头条算法偏好

#### Task 2
- `topic_key`: `kv-dequant-turboquant-detail`
- `目标读者`: 关注 AI 技术进展的科技爱好者、开发者、内容创作者
- `切入角度`: 技术故事化——AI 大模型推理加速新突破：TurboQuant 具体怎么做到 22.8% 提速的？（兼顾深度与可读性）
- `核心论点`: 开发者发现 KV dequant 占 decode 时间 40%，通过利用 attention sparsity 跳过 90% V dequant，P5 Max 上实现 +22.8% decode 提升；PPL 不变，NIAH 测试 7/9 → 9/9；CUDA 移植进行中
- `证据抓手`: Reddit 帖子含详细技术指标 + benchmark；GitHub: https://github.com/TheTom/turboquant_plus；论文链接
- `source_ref_bundle`:
  - `primary`: https://old.reddit.com/r/LocalLLaMA/comments/1s56g07/skipping_90_of_kv_dequant_work_228_decode_at_32k/
  - `github`: https://github.com/TheTom/turboquant_plus
- `视觉建议`: 头条封面：技术原理简化图（dequant 时间占比 → 跳过 90% → 提速 22.8%）；PPL 不变标注；NIAH 测试对比；兼顾专业感与可读性
- `为什么适合该平台`: 头条可接受中等深度技术内容；"提速 22.8%"数字具传播性；技术 + 开源叙事契合头条科技板块

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: **是**
- `理由`: SoftBank → OpenAI IPO 是高搜索量、强时效性的金融 + AI 交叉事件，百家号用户搜索行为中"AI IPO / 软银 / OpenAI 上市"类词群覆盖潜力大，需独立落地页承接 SEO 流量
- `承接哪篇主稿更优`: 建议镜像 `softbank-openai-ipo-signal`（wechat Task 1），改写为更符合百度搜索偏好的标题 + 正文结构（关键词前置、数据结构化）
- `百家号附加题`: **暂留空**——SK hynix IPO（赛道匹配，TechCrunch 背书，需补 SK hynix 官方公告或韩交所文件后方可升格）；STADLER 案例**已排除**（Top20 返工 P1 已将其一手性从 3 降至 1.5，低于 Top6 门槛，且 STADLER 官网/LinkedIn 均无独立公告，不宜作为百家号 SEO 承接主体）

---

## P1 返工记录

| 返工项 | 级别 | 动作 | 结果 |
|---|---|---|---|
| P1-1 TurboQuant GitHub（xiaohongshu T1） | P1 | `supplement_evidence` | ✅ 补全为 `https://github.com/TheTom/turboquant_plus`；atomic.chat 链接标注待补 |
| P1-1 TurboQuant GitHub（bilibili T1） | P1 | `supplement_evidence` | ✅ 补全为 `https://github.com/TheTom/turboquant_plus`；atomic.chat 链接标注待补 |
| P1-1 TurboQuant GitHub（x T2） | P1 | `supplement_evidence` | ✅ 补全为 `https://github.com/TheTom/turboquant_plus`；P2-4 视觉建议已同步补全 |
| P1-2 STADLER 百家号升权错误 | P1 | `supplement_evidence` | ✅ 从百家号建议中移除 STADLER；百家号附加题改为暂留空（SK hynix IPO 待补证后升格） |
| P1-3 SoftBank IPO 多平台重复 | P1 | `rewrite_angle` | ✅ 最终以一致性修复后的版本为准：zhihu T1 改为 `aibuildai-mle-bench-top`，wechat T2 / zhihu T2 改为 `kunlun-agi-three-models-2026`，SoftBank IPO 仅保留 wechat T1 + toutiao T1，且所有 Top6 / 槽位均回到当日 Top20 池内 |
| P0-4 Top20 链路一致性修复 | P0 | `align_with_top20_pool` | ✅ 移除不在 `20260328__top20-screening-pack.md` 内的 `viktor-zeta-slack-ai-agent` / `codex-openai-multi-agent-dev-platform`；恢复 Top20 → 平台任务单 的严格优中选优关系 |

---

## Holdout 清单

### `stadler-chatgpt-enterprise`
- `为什么能进最终池`: OpenAI 官网案例仍有参考价值；230 年老企业 + ChatGPT 改造知识工作的叙事具话题性；企业 AI 落地是持续热门赛道
- `为什么这轮没选`: 核心风险——STADLER 官方无此公告（STADLER 主业为垃圾分拣 AI，与 OpenAI 报道的知识管理场景存在用途偏差），来源可信度不足；STADLER（德国）≠ Stadler Rail（瑞士）品牌混淆风险高；一手性从 3 → 1，降权后综合评分 17/30 低于 Top6 门槛
- `什么时候可捞回`: 若 STADLER 官方发布公告或媒体跟进确认，或 OpenAI 官网补充官方客户证言链接，则可重新升权进入主池

### `openai-sora-meta-court-resistance`
- `为什么能进最终池`: AI 基础设施扩张阻力叙事强（82 岁老太太拒绝 $2600 万征地补偿）；Meta 诉讼是真实法律事件；跨平台讨论潜力大（techcrunch 播客已有传播）
- `为什么这轮没选`: 数据硬度偏低（播客内容，缺单一核心数据点）；Meta 诉讼需回链法院文件；当前主池 6 个话题已覆盖 IPO/Agent/开源效率/开发者平台/硬件，容量已满
- `什么时候可捞回`: 若 Meta 诉讼有法院判决进展，或数据中心用地争议有后续新闻，可补证后进入下一轮主池候选

### `vcs-betting-ai-next-wave-sora-killed`
- `为什么能进最终池`: 投资叙事强；VC 持续押注 vs OpenAI 关闭 Sora 的矛盾具讨论深度；TechCrunch Equity 播客背书
- `为什么这轮没选`: 播客内容一手性低（1/3）；数据硬度偏低；与 `softbank-openai-ipo-signal`（SC1）存在叙事重叠（均涉及 OpenAI IPO / 资本回报预期）；主池容量有限
- `什么时候可捞回`: 若有 VC 新一轮 AI 投资数据（如 GPU 算力投入统计），可作为补充证据升级后进入

### `hn-claude-folder-anatomy`
- `为什么能进最终池`: HN 388 分 / 194 评论，高热 developer 内容；Claude Code 生态深度覆盖；prompt 配置管理实用价值高
- `为什么这轮没选`: 视觉素材弱（仅博客配图）；技术细分受众，传播性受限；缺乏硬数据点；平台适配偏 developer 小众圈层
- `什么时候可捞回`: 若原博客文章有更完整配图或补充 GitHub 仓库链接，可作为 developer 垂直内容圈层补充候选

### `chatgpt-plus-cancellation`
- `为什么能进最终池`: 真实用户负面反馈；ChatGPT Plus 付费留存压力信号；产品体验恶化是行业关注点
- `为什么这轮没选`: 单一个案（1/15 TechCrunch 来源），缺乏更多样本交叉验证；情绪成分较高；数据点分散
- `什么时候可捞回`: 若有更多用户反映（如 Reddit 多帖汇总、第三方调研数据），可作为 AI 产品留存话题的证据补充

### `claude-pro-billing-anomaly`
- `为什么能进最终池`: Claude Pro 计费透明度问题；Anthropic 运营压力信号；付费用户权益话题
- `为什么这轮没选`: 单一个案，可信度有限；Anthropic 官方无回应；整体评分 14/30，低于主池门槛
- `什么时候可捞回`: 若 Anthropic 官方回应或更多用户反映，可进入产品体验话题候选

### `gan-style-claude-prompt`
- `为什么能进最终池`: prompt 工程技巧有实用价值；Mac Mini 一人 AI 工作站话题潜在关联；HN/Reddit 有传播
- `为什么这轮没选`: 技巧类内容时效窗口短（1/3 时效性评分）；非产品或公司新闻；短期热度难以持续
- `什么时候可捞回`: 作为 prompt 工程系列内容的一篇，而非独立话题；低优先级

### `sk-hynix-ipo-rammageddon`
- `为什么能进最终池`: AI 硬件基础设施；HBM 芯片赛道高热；$100-140 亿 IPO 规模大；TechCrunch 背书
- `为什么这轮没选`: 媒体解读为主（TechCrunch），一手性低（1/3）；需回链 SK hynix 官方公告或韩交所文件；赛道匹配但当前主池已有 2 个硬核 tech 题
- `什么时候可捞回`: 若 SK hynix 官方确认 IPO 计划或提交韩交所文件，可升级为硬信息进入下一轮主池
- `百家号补充`: SK hynix IPO 适合百家号"AI 芯片 / 半导体"长尾词，可作为 SEO 镜像附加候选

### `agi-is-here-emotion`
- `为什么能进最终池`: 社区情绪信号反映用户对 AGI 进展的强烈情绪；"AGI is here"高热标题具传播性
- `为什么这轮没选`: 内容空洞（正文仅表情符号）；无实质内容讨论；信号质量极低（11/30）；不适合作为内容选题主体
- `什么时候可捞回`: 作为"AI 用户情绪"佐证参考，不作为主稿；极低优先级

---

## 执行备注

- **主池 6 个话题已锁定**，12 个平台槽位均已分配具体任务，无凑数
- **待补证项**（建议 content-writer 在写作时处理）：
  - SoftBank IPO：回链 SoftBank / SEC 官方披露
  - TurboQuant + Qwen：回链 TurboQuant 原论文 / Google 官方博客
  - Codex OpenAI：回链 OpenAI 官方 blog post（如有）
  - SK hynix IPO：回链 SK hynix 官方公告或韩交所文件
- **视觉资产优先级**：B 站两篇需视频制作；小红书两篇需图文制作；其余平台封面图制作
- **百家号 SEO 镜像**：主镜像 SoftBank IPO（wechat Task 1 镜像）；附加题暂留空（SK hynix IPO 补证后可升格）；STADLER 已排除
- **当前 stage_gate_status**：`pass` — P1 阻断项已关闭，且已完成 Top20 → 平台任务单 一致性修复，可进入 `approved_topic` 物化
- **P1 返工执行时间**：2026-03-28 15:04 CST
