# OpenClaw 是一个信号｜2026 Long-Horizon Agent 投资地图

来源: https://mp.weixin.qq.com/s/EDJRZQLdNRs-gKzWFWigTQ

作者：Haina

过去两年，AI 产品的叙事一直围绕着一个关键词：辅助人类。直到 OpenClaw 的出现，这个共识开始真正被打破。这个由 PSPDFKit 创始人 Peter Steinberger 发起的开源项目，本质上像一个获得完整操作权限的数字替身：它可以翻阅邮箱、管理日历、在终端执行代码，在 Slack 和 Discord 上持续处理沟通任务。

这背后对应的是 AI Agent 正从软件走向劳动力。上一代 SaaS 的目标是提升效率，那么 Long-Horizon Agent 的目标是直接交付结果；定价逻辑也正在从 Seat 转向 Outcome，从卖工具走向 Selling Labor。

本文试图回答三个问题：

1. OpenClaw 的爆发，意味着 Agent 进入了怎样的新阶段？

2. 当模型能力逐渐提升，Long-Horizon Agent 的真正护城河在哪里？

3. 当 Agent 从 Coding 场景走向企业流程与现实世界，产业价值将向哪一层迁移？

当 AI 开始主动执行世界，而不只是理解世界时，一个新的产业周期才刚刚开始。

01

.

AI Agent 开始变成劳动力

OpenClaw 的爆发，一种新的 Agent 形态第一次被大众直观地看到：AI 不再只是回答问题，而是能够长期执行任务、跨系统行动，并逐步接近数字员工。这背后对应的，是 Long-Horizon Agent（长程智能体）的出现。

在 AI Agent 的语境中，Long-Horizon 最早源自强化学习中的决策视野：当一个 Agent 需要跨越长时间、多步骤才能获得最终结果时，传统算法往往失效。今天，随着推理模型与执行框架的成熟，这种长周期任务第一次开始在真实企业环境中落地。

技术上，Long-Horizon Agent 是更长的行动链：

•

能够将一个模糊目标拆解为多个子任务，并在数小时甚至数天内维持状态；

•

在执行过程中持续自我纠错，而不是按脚本机械运行；

•

通过深度推理与规划能力，处理真实世界中跨系统、跨角色的复杂流程。

更重要的变化是其经济属性。过去的软件市场，本质是按功能收费；当 Agent 开始直接交付结果，软件的定价逻辑、市场边界和护城河，都在发生结构性变化。

围绕这一变化，我们观察到三个正在加速成形的趋势。

1. Service-as-Software 带来 TAM 结构性变化

SaaS 的逻辑对应全球约 3-4 千亿美元的企业软件支出，而 AI Agent 解锁的是 13 万亿美元的劳动支出市场（仅美国）。这是 30x 的 TAM 扩张机会。

传统 SaaS 旨在提高人的效率，而 LHA 直接替代全职员工。这也是为什么越来越多公司开始采用 Outcome-based 定价：客户不再为功能付费，而是为解决的工单、完成的流程或节省的人力成本付费。软件的商业模型，从卖工具逐渐演变为 Selling Labor。比如 Sierra 和 Decagon 等玩家正在按 Outcome（成功解决的工单/对话）收费，将 Take Rate 直接挂钩于客户节省的人力成本。

我们现在处于 Agent 商业模式毛利改善的拐点。在 2024-2025 年，大多数 Agent 公司看起来更像人力外包公司。由于昂贵的底层模型成本 （COGS 占比约 70%） 和密集的人工干预 （HITL），毛利被压制在 40-50%，Long horizon 任务更会导致 Token 使用量爆炸增长。

拐点来自两个结构性变化：

第一是推理成本的对数级下降。

推理成本每 18 个月下降一个数量级，单位任务的经济模型开始发生翻转。

第二是 Reasoning Orchestrator 与分层调度的普及。

越来越多 Agent 将复杂规划交给高阶模型，而把执行步骤分配给更廉价的模型，从而显著降低成本结构。

Agent 的单位经济模型可能会很快从人力外包回归到软件产品，实现对传统服务业的降维打击。

2. 从 System of Record 到 System of Action：护城河开始改变

上一代企业软件的核心，是记录世界。Salesforce 之类的 System of Record 依赖用户不断输入数据，而这恰恰是企业不愿意做的事情。Long-Horizon Agent 则代表着 System of Action：软件不再只是记录，而是直接执行。

这种变化带来了新的护城河逻辑：Workflow Data Gravity。

如果说 Stripe 的优势来自支付数据，那么 Agent 的优势开始来自执行轨迹。每一次任务运行，都会积累 Corner Cases、人类修正记录与 API 调用路径，这些数据并不会出现在公开训练集中，却能显著提升在特定企业环境中的准确率。基于私有数据微调后的 Agent，Agent 在垂直场景中的表现，往往远超通用模型。这意味着客户切换成本极高，因为通用模型无法替代已经磨合好的 Agent。

像 Simular 这样的 Computer-Use Agent，通过直接操作操作系统，将原本不可结构化的鼠标与键盘行为转化为可学习的执行轨迹，逐渐构建起难以复制的数据壁垒。

这也引出了一个问题：当模型能力不断提升，稀缺的是 Intelligence，还是 Experience？

3. High Agency 与 Voice：当 Agent 开始主动工作

2026 年的交互将从被动响应转变为主动介入。未来的 Agent 不只是响应用户，而是持续观察环境、提出建议，并在获得授权后自动执行。理想状态下，它更像一名 S 级员工：发现问题、研究诊断、制定方案、执行任务，最后才请求审批。

High Agency 五层金字塔

例如现在的 Sales People 需手动操作 CRM；未来的 Agent 自动分析两年邮件，挖掘沉睡客户并起草跟进，用户只需点击 Approve。这极大地缩短了 Sales Cycle。

在这一过程中，Voice 正在从交互界面转变为数字员工的面孔。在医疗、保险与金融等高信任场景中，语音不只是 UI，而是合规与情绪管理的重要载体。Voice Agent 在遵守合规性方面甚至优于人类，因为它们不会像人类那样因疏忽违规。端到端语音推理模型正在让 Agent 能够实时理解情绪、处理复杂对话，并完成闭环流程。部分公司甚至通过刻意加入延迟与环境噪音，让 AI 的声音更接近真实人类，以降低心理距离。

Voice Agent + Proactive Agent 很可能是未来 AI Agent 员工的形态。

02

.

2026 Agent 投资逻辑

2026 年 Agent 的核心问题是价值会落在哪一层，我们应关注那些利用 Long-Horizon 能力解决高价值商业问题的公司。

过去两年，资本最拥挤的地方是 Coding Agent。这是一个封闭、确定性高的环境，也是 Agent 最容易跑通的起点。但随着封装能力提升，真正的机会正在从代码世界，迁移到企业流程与真实业务中。

从投资视角来看，我们关注这四条 thesis 下的公司：

1. Reasoning Orchestrators：能让 Agent“工作的更久”的 Infra

Agent 需要状态管理。很多情况下 Agent 执行任务失败，不是因为模型不够聪明，是因为它们无法在长时间任务中维持状态。

Long-Horizon Agent 是一种长生命周期的软件，它需要跨越数小时甚至数天执行，并在异步系统之间持续运行。Durable Execution 与 State Management 正在成为新的基础设施层。

公司如 Temporal 和 Inngest 保证了如果 Agent 跑到第 3 步服务器挂了，重启后能从第 3 步继续，而不是重头再来。这两家公司提供的 Durable Execution 确保了状态不丢失。Parallel Web Systems 代表了另一种基础设施方向：为 Agent 重构互联网本身。传统网页是为人类设计的，而 Agent 需要的是一个可预测、无噪音的执行环境。当 Agent 成为互联网的主要用户时，它需要一个不会弹窗、不会加载 CSS 垃圾的纯净环境，Agent-first Web 很可能成为新的流量入口。

2. Process Intelligence：模型能力会趋同，执行经验不会

Foundation Model 已经消化了大部分公开数据，剩下的价值，藏在企业内部的流程、日志与员工行为轨迹中。Execution Traces 的意义在于记录过程数据。比如谁能记录下“理赔专员在拒绝这个单子前，查阅了哪三份文档、在哪个格子里停顿了”，谁就有垂直模型壁垒。我们关注那些在执行过程中学习人类专家经验的公司，它们捕捉解决问题的路径。

公司如 Simular 累积了大量金融、医疗场景下操作老旧软件（EMR/Legacy Banking Systems）的视觉-动作数据，这是通用模型很难触碰的领域。摩根大通的案例极具代表性。它处理商业贷款不是靠聊天，而是靠看屏幕、填表格。Mimica 则通过观察员工屏幕，记录下看到 A 错误 -> 点击 B 按钮 -> 复制 C 代码的轨迹。将员工的隐性知识显性化为代码。这些 Trace 被直接转化为 Agent 的执行逻辑，相比传统 RPA，它捕捉的是人类决策路径。

3. Selling Labor ：真正的 Agent 公司卖结果

判断一家公司是否具备 Agent 潜力，一个简单标准是客户是在为软件付费，还是在为“少雇一个人”付费。我们更关注那些愿意按 FTE 或 Outcome 定价的公司，它们的毛利初期可能因 Token 消耗而不够好看，但具有极强的替代性。这个领域有很多 Vertical Specialist， 在特定高价值垂直领域（保险、法律、采购）实现 更高的准确率。

Serval 是一个典型案例。客户付费是因为它可以直接替代 IT 支持人员。当工程师在 Slack 里请求权限时，Agent 在几秒内完成审批、执行与审计闭环。客户（如 Verkada）明确将其价值锚定在节省了多少个 FTE。

Distyl AI 的逻辑是高接触交付 + 平台化沉淀。早期通过 Forward Deployed Engineers 深度参与客户业务，一旦模式稳定，就能形成高毛利的 Service-as-Software 结构。它像 AI 时代的 Palantir，但交付节奏更快。比如他在给 T-Mobile 做账单预测，给 Elevance Health 做医疗预授权。

在垂直领域中，WithCoverage、Corgi 与 Omnea 等公司把 Long-Horizon 能力应用到保险审计与采购流程中。这些任务低频、高价值、复杂度高，是 Agent 最具替代性的场景。

4. Voice Agents：劳动力的面孔

在 Selling Labor 的语境下，Voice 是 Agent 面向现实世界的接口。Reasoning Orchestrator 是大脑，System of Action 是手脚，那么 Voice 就是那个能够直接面对人类客户、处理复杂情绪并完成闭环的数字面孔。

2026 年领先的 Voice Agent 不再采用传统的 STT-LLM-TTS 链路，而是端到端的原生音频推理，延迟压到 300ms 以内，支持随时打断。同时，很多 Long-Horizon 任务是情绪驱动的，比如理赔电话中客户的焦虑与愤怒。能够处理情绪的 Agent，其任务完成率往往显著高于传统聊天机器人。

一个典型的 Long-Horizon Agent 堆栈

以上四个维度可以将 Long-Horizon Agent 从底层基建到最终交付串起来：

以 Insurance 为例子，可以这样拆解一个理赔 Agent

•

Interface （11labs/Retell AI）: 客户在车祸现场极其焦虑，打入电话。Agent 毫秒级响应，语气冷静且富有同理心，安抚客户并提取关键事实。

•

Brain （Distyl/Custom Model）: 后台模型根据提取的事实，通过 RAG 检索该用户的保单条款，并结合当地交通法规进行推理。

•

Eyes & Hands （Simular）: 模型判断需要通过系统，但保险系统是 20 年前的老古董，没有 API。Agent 启动虚拟环境，操控鼠标登录后台，完成审批并生成 PDF。

•

Safety Net （Temporal）: 在生成 PDF 时系统崩溃。Temporal 捕捉到异常，自动重试，确保流程不中断，无需人工介入。

•

Evolution （Mimica）: 整个流程被记录为 Trace。如果这次 Agent 处理得好，这个 Trace 会在今晚自动加入微调数据集，明天 Agent 会更聪明。

03

.

Long-Horizon Agent 全景图

基于任务环境的封闭度与交付层级，我们把 Agent 市场划分为以下领域，每个领域都有机会诞生多家独角兽公司：

横轴 Task Environment（从纯代码/数字环境 -> 企业工作流 -> 物理世界/复杂环境）

纵轴 Value Delivery Layer（从基础设施 -> 平台工具 -> 端到端服务）

横轴体现环境复杂度，从左到右，Agent 所面对的环境越来越开放，也越来越嘈杂。

左侧（Code / Structured Data）是纯逻辑世界。环境封闭、反馈明确，代码要么跑通，要么报错。这是 Agent 最早爆发的领域，也是过去两年资本最拥挤的地方。

中轴（GUI / SaaS / Documents）是企业流程的灰色地带。这里既有 API，也有文档和鼠标操作，规则并不完全明确，但商业价值极高。这也是 Selling Labor 真正开始成立的主战场。

右侧（Open Internet / World）代表真实世界的复杂环境。弹窗、反爬虫、语音情绪与非结构化交互同时存在。这是 Voice Agent 与 Open Web Agent 的领地，也是技术难度最高、但长期分发权可能最大的方向。

纵轴体现价值交付层级，从下往上，Agent 离最终业务结果越来越近。

底部（Infra / Tooling）提供 Durable Execution、连接能力与稳定性，是“卖铲子”的基础设施层。

中部（OS / Models）Agent 的大脑与操作系统，负责推理与任务编排。

顶部（App / Platform）真正替代人工、按结果收费的 Selling Labor 层，也是企业愿意付最高预算的地方。

这张图体现了 Agent 生态的价值正在发生迁移。过去两年资本拥挤在图表的左侧（Software Engineering），这里的环境是封闭且高度结构化的 Code，竞争已成红海。2026 重心会移向中轴线。这里是 GUI 和 SaaS 的混合环境，噪音适中，但商业价值最高。

Software Engineering

Coding Agent 是 Long-Horizon Agent 最先跑通的场景。 境封闭、反馈明确，因此 Agent 最先在这里从 Copilot → Autopilot，开始接管“写、跑、改、测、上线”的全链路。

但从投资视角看，这个赛道同时有一个结构性矛盾：

它是最容易证明价值的领域，也是最容易被封装吞噬差异化的领域。

爆发会发生在这里，利润和护城河未必留在这里。因此，我们把 Software Engineering 拆成三类，对应三种不同的赢家逻辑。

Drawn by ChatGPT

1） Vibe Coding：把写软件变成表达需求，天花板取决于可靠性与分发

需求侧的爆发正在显著快于供给侧工程师的增量，越来越多创始人、运营和销售开始自己构建工具，这成为 Vibe Coing 产品能快速跑出来的核心原因。但一旦进入企业的核心业务系统，可靠性、权限管理、审计能力以及成本控制会迅速成为主要瓶颈。因此，未来的赢家要么掌握强分发入口（如 IDE 或平台级入口），要么将“可控性”本身产品化，包括版本管理、测试机制、权限体系与可回滚能力。

代表性公司：Emergent

Emergent 团队背景兼具 Dunzo 联创与 Amazon SageMaker 核心成员，技术与商业化基因明确；同时获得 Lightspeed、Google、SoftBank Vision Fund 2 等顶级资本支持。产品上线仅 90 天 ARR 即达 $15M、7 个月冲至 $50M，显示出强劲的早期增长势能。用户以开发者，中小企业，创始人为主，被非技术创始人广泛用于构建 MVP。不过目前使用场景仍以 SMB 内部工具与原型为主，长期护城河与生产级可靠性仍有待验证。

2） End-to-End Agent：从“会写代码”到“会交付结果”

这一类产品想做的事情是像真实工程师一样，完成任务拆解、环境配置、调试、测试、提交 PR，部署上线。

这里我会把玩家分成两种路线：

•

IDE inside-out（Cursor / Replit）：从开发者入口出发，把 Agent 融进日常工作流，用人类监督换取可靠性。

•

Agent outside-in（Devin / OpenHands）：数字工程师，强调更强自治与端到端交付。

代表公司：Cursor / Replit / OpenHands

Cursor 的核心价值是 Agent-native 的开发工作流入口：通过 Composer 将代码编辑器升级为可进行跨文件理解、终端操作与多步骤规划的半自主开发环境。相比完全自动化路线，Cursor 押注“人类在环”的长链路协作，这让它在真实生产场景中的 adoption 明显更快。

Replit 的战略从在线 IDE 转向 From Idea to Deployment 的 AI App Builder

，通过 Replit Agent 把环境配置、前后端开发、数据库与云部署整合成一个连续长流程，降低了非专业开发者构建应用的门槛。其差异化在于强社区与教育基因带来的分发优势，使其更偏向 prosumer → SMB 的自下而上渗透路径。相比 Cursor 的 developer-first 定位，Replit 更接近应用生成平台，试图成为 AI 时代的低门槛软件生产基础设施。

OpenHands 试图把“自主软件工程 Agent”从 demo 推向企业级基础设施。

其亮点在于从单 Agent 扩展到上千 Agent 并发协作，强调在沙盒环境中真正执行任务（写代码、跑 CLI、浏览网页），而非仅生成建议；同时与 AMD 的合作强化了端侧推理和成本结构优势。团队兼具 Google 工程背景与学术顶尖 AI 研究者，在 developer-native 生态中具备较强技术公信力。

3） Remediation：写代码成本接近 0，维护与稳定变成新的劳动预算

随着 AI 生成的代码指数级增长，

维护代码和保证系统稳定的成本在急剧上升。

Remediation 是 Selling Labor 在开发者工具领域的落地：AI SRE、自动化修复、代码审查、迁移与技术债清理。在 Software Engineering 里，我更看好 Remediation 的付费韧性，因为它更直接对应企业稳定性预算，不是开发者的工具预算。

代表公司：

Resolve / Traversal 代表 AI SRE 方向

Resolve 将 AI Agent 引入生产工程，把传统 SRE 从“被动告警处理”升级为多代理自主运维系统。核心亮点在于跨代码、基础设施与遥测数据的上下文推理能力，能够自动分流告警、定位根因并生成带生产环境语境的修复代码，压缩 MTTR。创始团队来自 Splunk 可观测性核心层，叠加 OpenTelemetry 生态背景，使其更像 Observability → Autonomous Ops 的延伸。

Traversal 的差异化在于把 AI SRE 从简单自动化升级为基于因果推理的复杂系统分析：通过并行 Agent 群进行统计测试与因果建模，穿透日志与指标噪音定位深层系统问题，并可自动执行修复方案。相比传统 observability 工具，它强调无供应商锁定和跨系统分析能力，试图成为多云环境下的智能调度层。团队背景偏学术 AI 与强化学习，叠加 Sequoia 与 Kleiner Perkins 的支持，使其更像是 infra-native 的研究型公司，押注复杂系统调试这一高技术壁垒方向。

CodeRabbit / Sweep 更像把重复性维护外包给 AI，对中低复杂任务更有效。

Sweep AI 聚焦

工单级自主编码 Agent

，定位为“初级开发者替身”，通过 Fire-and-Forget 模式自动阅读代码库、生成 PR，并根据 CI/CD 反馈自我迭代直至通过测试。其亮点在于明确切入高频但低创造性的 GitHub Issue 场景，把 AI 从辅助写代码推进到可执行任务层，降低资深工程师处理琐碎工作的时间成本。目前产品在定义清晰的小任务中表现稳定，但在复杂架构推理上仍受限，更接近开发流程中的自动化执行层。

Enterprise Action Systems

Enterprise Action Systems 的定义是

，在企业内部碎片化、非线性、充满例外的脏活累活中，Agent 不只做建议与摘要，而是

接管工作执行闭环

（识别意图 → 拉取上下文 → 校验权限与合规 → 调用系统执行 → 生成审计/回滚），直接替代人力。

这类市场我们认为会在 2026 变成主战场，有三个原因：

1. 价值锚定清晰：节省的是 FTE / BPO / 工单成本；

2. 环境复杂但可控：比开放互联网噪音小，但比纯代码世界更接近真实业务；

3. 落地门槛高意味着护城河更厚：需要权限、审计、集成、灰度、回滚、异常处理，单点模型能力很难直接替代。

Drawn by ChatGPT

1） Horizontal Ops：企业执行层，从一个部门切入，向 Everything Ops 扩张

这类公司通常从 IT/HR/Finance 的工单与流程切入，用统一的 Agent 执行层覆盖多个部门，最终目标是成为企业内部的“行动中枢”。

代表公司：

Serval 把 ITSM 从记录系统升级为 AI-native 的 System of Action：用户只需在 Slack 中用自然语言描述需求，AI 即可生成并执行可审计的 workflow code，实现权限管理、审批与自动化闭环。营收 18 个月内爆发式增长、很多客户直接停用传统 ITSM，证明其切中了企业 Ops 自动化的代际更替窗口，但长期护城河仍取决于是否能成为 Agent 的 System of Record。

Ema 想把 AI Agent 产品化为 Universal AI Employee，通过 Persona 化数字员工（客服、文档专员、数据科学家等）让企业像雇人一样部署 AI。其 Generative Workflow Engine 与多模型融合架构强调长流程任务拆解与合规可靠性，在金融、客服和 HR 场景已实现 70%+ 自动化率与明确 ROI。Ema 押注结果导向定价与角色化交付，目标成为企业内部的 AI Workforce Layer。

Relevance AI 的定位是低代码 Agent OS，专注于构建与编排多 Agent 团队，帮助企业把复杂工作流拆解成可持续运行的长期任务系统。其差异化在于强调 orchestration 与可视化操作，适合非深度工程团队快速搭建 AI 自动化体系。

2） Custom Delivery：高接触交付 + 平台化沉淀，解决数据孤岛和复杂流程

将 AI Agent 用于企业的核心流程，缺少的一环是“把数据、系统、人、合规绑成闭环”的工程能力。因此这类公司以 Palantir 式 FDE（Forward Deployed Engineering）推进：先用交付解决冷启动，再把重复模式沉淀成平台组件。

代表公司：

Distyl AI 由前 Palantir Technologies 成员 Arjun Prakash 与 Derek Ho 创立，定位为高复杂度企业工作流的定制化 Agent 构建与交付平台，通过与 OpenAI 的战略合作将大模型嵌入 Fortune 500 核心业务流程。其模式更接近咨询 + SaaS 的混合形态：早期依靠高接触工程团队解决数据孤岛与合规问题，再逐步沉淀为可复用平台组件。当前优势在于能快速落地传统 SaaS 难以覆盖的复杂场景（如供应链预测、账单预警），但长期规模化取决于交付模式能否从项目制过渡到产品化。

Mimica 由前 Palantir Technologies 工程师 Tuhin Shroff 与 AI 背景的 Raphael Holca-Lamarre 创立，专注于 Task Mining 与自动化生成，通过后台观察员工操作自动发现复杂流程，并生成 RPA 脚本或标准流程文档。客户集中在 Liberty Mutual、Goodyear、Merck、DHL 等高合规传统行业。其价值在于解决企业自动化最难的“流程发现”阶段，能快速证明成本节省，但产品仍偏向效率优化层，是否能成为长期系统入口仍需观察。

3） Vertical Specialist：在高合规/高价值/强行业 know-how 场景里替代 FTE

当流程与风险高度行业化（保险、医疗、采购、财务），横向工具很难吃透细节。垂直公司通常更容易在一个岗位上实现端到端替代，并拿到更高的 outcome 定价。

代表公司：

Finance / Procurement：Sema4.ai（财务文档流）、Omnea（采购与供应商治理）

Sema4.ai 由前 Cloudera / Docker CEO Rob Bearden 与 Robocorp 创始团队推动，定位为企业级 Agent 执行平台，重点解决财务与合规类长流程任务。其技术路径是将 Rasa 的对话理解与 Robocorp 的 Python 自动化结合，使 Agent 能直接运行 Runbooks 与 Actions，而不是停留在建议层；客户如 Koch Industries 已用于发票自动化。

Omnea 由前 Tessian 高管 Ben Freeman 与 Ben Allen 创立，聚焦 Source-to-Pay 采购流程的 AI 化摄入与编排，目标是成为企业供应商数据与风险管理的统一入口。客户包括 Spotify 与 MongoDB。其差异点在于将采购需求入口、合同续约与风险治理整合到单一系统，但当前价值更多体现为流程效率与数据集中，是否能成为长期采购系统替代者仍需时间验证。

Insurance：WithCoverage（Broker 替代）、Corgi（AI 原生 Carrier）、Further AI（核保/理赔自动化

）

WithCoverage 由 Opendoor 联创 JD Ross 与前 Bain/Compound 团队成员 Max Brenner 创立，定位为替代传统保险 broker 的 AI-native 风险管理平台。公司通过固定费用（flat-fee）模式与 AI 风险审计引擎，为成长型公司提供保险组合优化与理赔管理，试图把以佣金驱动的经纪业务转为更透明的软件化服务。客户集中在高增长科技公司，核心优势在于成本优化与流程数字化，但本质仍属于 broker 层，护城河更多来自客户关系与数据积累。

Corgi 是一家 AI 原生保险 carrier，直接设计产品并承担赔付风险。创始人 Nico Laqua 与 Emily Yuan 背景偏创业与运营，团队规模约 70 人，获得 Y Combinator 与 Kindred Ventures 等投资，总融资约 $108M。产品强调从承保到理赔的端到端自动化，并针对初创公司不同融资阶段提供模块化保障（D&O、Cyber、AI liability 等）。与 broker 型公司相比，其核心变量在于风控与定价模型是否能长期优于传统保险公司。

Computer Use & Prosumer

OpenClaw 让大众第一次直观感受到 Agent 的高自治，Computer Use（看屏幕+动鼠标）是它背后最关键的能力，也是现在最大的卡点之一。从投资角度，我会把 Computer Use 赛道理解为让 Agent 穿透企业里那 80% 没有 API 的遗留系统与碎片化流程，个人用户从而拥有可外包的数字双手。

Computer Use 是在高噪音环境里做长程任务：弹窗、反爬、页面改版、权限、验证码、网络抖动、多人协作软件的状态切换。这使得：

•

可靠性门槛极高：一次长链路任务里，任意一步失败都会导致全流程崩溃。

•

成本结构更敏感：视觉理解 + 多轮尝试会带来 token/推理成本爆炸。

•

安全与合规是硬门槛：越接近“动手执行”，越需要可审计、可回滚、可授权的控制平面。

Drawn by ChatGPT

1） OS Level：系统级接管，价值高但交付重

OS 级 Agent 的重点是操作本地应用与企业老系统（Excel、SAP、EHR、Citrix、各种古董后台），直击企业流程的最后一公里，但集成、权限与交付复杂度更高。

代表公司：

Simular 由前 Google DeepMind 研究员 Ang Li 与 Jiachen Yang 创立，定位为本地端 Computer-Use Agent，直接在 Mac/Windows 上操作 Excel、SAP、EHR 等桌面软件。公司强调 on-device 与可控执行，通过 Agent S2 架构与记忆机制支持长链路任务，并加入微软 Windows 365 for Agents 计划，路径更偏企业 IT 自动化而非消费级助手。

Manus 定位为通用 Autonomous Agent，强调从 research 到 output 的端到端执行能力，被视为“Execution Layer”路线的代表之一。公司在被 Meta 收购前已获得 Benchmark 支持，其策略是尽量减少人工介入完成复杂任务。但随着大模型厂商不断内化 agentic 能力，这类通用执行层产品面临平台竞争压力。

2） Browser Level / Web Automation：分发更快，但容易被平台规则卡住

浏览器级 Agent 更轻，更容易触达 prosumer，也更容易做订阅。但它最大的风险来自开放互联网本身：反爬、验证码、站点改版、登录态、支付与风控。

代表公司：

Yutori 由前 Meta FAIR 研究员团队创立，开发 Autonomous Web Agents，用于跨网站执行监控与自动化操作（价格跟踪、表单填写等）。Radical Ventures 与 Felicis 投资 $15M Seed，产品 Scouts 强调长周期网页任务与可靠执行，目前仍处于 Beta 阶段。其优势在研究团队与 web-native agent 架构，但实际价值仍依赖任务稳定性与清晰 prompt 设计。

Twin 由前 Dreem 创始人 Hugo Mercier 与 Joao Justi 创立，专注 Headless Browser Automation，通过视觉与 Action Model 自动操作网页 UI，试图将传统 RPA 升级为 AI-native web automation。

Infrastructure

决定 Agent 能不能在企业里落地的有三个现实的问题：

能不能跑得久、跑得稳、跑得可控。

Long-Horizon Agent 要跨越数小时/数天、穿过异步系统、处理故障重试、记录审计轨迹，还要在关键节点可回滚、可接管。这些能力要靠基础设施堆出来。

在 Landscape 里，Infrastructure 是决定上层 App 能否从 Demo 走向规模化交付的地基。

Drawn by ChatGPT

1) Agent-first Web & Environment

Long-Horizon Agent 的第一步是获取信息，但现实互联网对 Agent 极不友好：噪音、反爬、弹窗、结构混乱、内容封闭。这一层的价值是把对 Agent 来说不可控的 Web 变成可执行的环境。

代表公司：

Parallel Web Systems：代表 Web for AI Agents”路线。把互联网改造成 Agent 可用的执行面：更稳定的抓取/搜索 API、更可控的交互、更强的溯源与置信度机制。其产品是 Agent-first 的网页浏览与搜索基础设施，为 AI Agent 提供不同于人类网页的搜索、抓取与交互 API，解决 Agent 在真实 Web 环境中的可用性与稳定性问题。

2) Workflow orchestration

Long-Horizon 任务需要跨系统的状态管理、重试策略、幂等性、可观测性。Temporal、Inngest 和 LangChain 等公司通过提供 Durable Execution 基础设施，解决了 Agent 在长时程任务中维持状态、处理故障和自动重试的难题；UiPath 和 Zapier 等传统自动化巨头利用其庞大的 API 连接器生态，正在从基于规则的线性流程向动态的 AI 代理编排转型。

代表公司：

Temporal 由 Maxim Fateev 与 Samar Abbas 创立，为长时间运行的业务流程提供 Durable Execution 引擎，解决的是分布式系统中状态管理与失败恢复的底层问题。相比传统 workflow 工具，它更像基础设施层，开发者通过 SDK 把业务逻辑写成可恢复的状态机，由引擎保证任务在重启、超时或服务故障后仍能继续执行。

Inngest 定位为更轻量的 workflow orchestration 平台，强调“默认 durable”的事件驱动执行模型。与 Temporal 相比，它减少了基础设施复杂度，主打 serverless 与 runtime-agnostic，使开发者可以为 AI 工作流、后台任务或 Agent 编排快速加入重试、恢复和可观察性。优势在于上手门槛低、贴近现代开发栈，长期差异化取决于能否在 AI orchestration 场景中建立开发者生态。

3) Model as an agent

将深度 Reasoning、代码生成与 Computer Use 能力内化到模型权重中，构建能够直接接管浏览器、终端或桌面的 Agent。

代表公司：

Imbue 由 Kanjun Qiu 与 Josh Albrecht 创立，定位更接近研究型 AI lab，核心押注是“推理能力作为长期护城河”。公司自研 Imbue 70B 推理基础模型，并通过 Sculptor 界面探索多 Agent 协同编码环境，同时开源 CARBS 等训练基础设施工具，强调从模型到执行环境的全栈研发路径。获得 Nvidia、Astera、Eric Schmidt 等支持并拥有大规模 H100 集群，战略上不急于商业化，更多在与 OpenAI 和 Anthropic 的底层研究方向形成竞争。

Reflection AI 由前 DeepMind 研究员 Misha Laskin 与 Ioannis Antonoglou 创立，重点研究带有“reflection”机制的长链路推理模型，目标是提升自主编码与高自治软件执行能力。公司获得 Nvidia 领投的大规模融资（总计约 $2.13B，估值 $8B）。与大型模型公司类似，其战略既向上探索 Agent 化应用能力，也向下将工具调用与 workflow 编排内化为模型能力，目前仍处于偏前沿研究阶段，商业化路径尚未完全明确。

Voice Agents

Voice Agent 的进步体现在实时性、情绪、可控性。

2026 年领先的 Voice Agent 不再满足于传统 STT→LLM→TTS 的拼装链路，而是走向更端到端、更低延迟的实时架构。其一是 <300ms 的端到端响应：越接近人类对话节奏，越能减少打断、跑题与挂断。Barge-in（随时打断）的能力：客户一句“等一下”“不是这个”，系统能立刻停、立刻转向。

在理赔、催收、预约、出院随访等场景里，交流包括了在情绪波动中推动流程前进。能处理愤怒、焦虑、紧迫感的 Agent，能显著提升任务完成率。

另外，Voice 一旦进入金融/医疗，就是企业生产系统：录音与审计、PII/PHI 处理、转人工策略、黑名单/敏感词、权限与风控。Fallback 机制非常关键，当模型异常、听不清、情绪升级时如何降级处理。

Drawn by ChatGPT

代表公司：

•

End-to-End Speech Infrastructure: 11labs/Cartesia/Sesame AI

ElevenLabs 由 Piotr Dabkowski 与 Mati Staniszewski 创立，最初以高质量 TTS 出圈，正在向 Voice Agent 与多模态语音平台转型，试图成为企业级语音入口层。公司通过 API 与内容生态（媒体、本地化、AI 招聘等）建立分发优势，其核心护城河在于语音质量与开发者 adoption，而不是单一模型能力。随着 OpenAI 与 Anthropic 推进实时语音能力，ElevenLabs 的长期定位更像 voice infrastructure 层，需要持续扩展到 orchestration 与 agent runtime 才能避免被基础模型能力内化。

Cartesia 聚焦极低延迟语音基础设施，其 Sonic 系列模型强调 <100ms 的响应与拟人化表达，定位偏 API 层而非应用层。团队背景来自实时系统与语音研究方向，策略是成为实时语音交互的性能基线，尤其适用于实时客服与机器人场景。

Sesame AI 把语音从工具升级为“Always-On Companion”，开发 Maya、Miles 等语音伴侣设备，试图把语音 Agent 推向硬件与长期交互场景。公司获得 a16z、Sequoia 等支持，核心赌注在于情感化语音体验与持续上下文，而不是企业语音 API。其战略更接近消费级 Voice OS，成败取决于是否能建立设备与生态，而非单一模型优势。

•

Vertical Voice OS:

HappyRobot/Further AI/Hippocratic AI

HappyRobot 由 Pablo Palafox 等创立，专注物流行业的 Voice Operating System，将语音 Agent 深度绑定 TMS 与调度流程，解决司机沟通、费率确认等高频任务。Sequoia、Accel 等投资支持其垂直化路线，其优势在于行业语义理解与执行闭环，而不是通用语音能力。

Further AI 切入保险行业，通过语音代理自动处理核保与理赔流程，例如催补资料与客户沟通。团队具保险与技术双背景，融资规模较早期，定位更偏 workflow automation 而非基础语音模型。其优势在于结合保单结构化解析与语音交互，但目前仍属于垂直自动化层，护城河取决于与保险系统的深度集成。

Hippocratic AI 由 Munjal Shah 等医疗与技术背景团队创立，目标是构建合规优先的 AI Nurse，用语音完成随访与患者监测。a16z、Kleiner Perkins、NVIDIA 等投资支持其医疗方向，强调安全性与医疗级数据治理，而非通用语音体验。其优势在于垂直监管与医疗流程理解，但 adoption 依赖医疗机构对自动化语音的信任与合规验证周期。

•

Voice Agent Infra: Retell

Retell 起初是语音机器人 no-code 工具，逐步转型为语音 Agent 生成平台，通过接入实时模型实现通话逻辑、脚本与 CRM 集成的一键生成。团队规模小但迭代速度快，更像 voice orchestration 层而非模型公司。当前优势在于稳定性与开发体验，但长期风险是底层 realtime 能力被模型厂商原生整合后，其平台价值需要向 workflow 与企业集成延伸。

排版：夏悦涵

延伸阅读

国产模型春节大考：来自 MiniMax、GLM、Seedance 开发者的一线复盘｜Best Ideas

当人读不懂 AI 代码，Traversal 如何做企业运维的 AI 医生？

深度讨论 OpenClaw：高价值 Agent 解锁 10x Token 消耗，Anthropic 超越微软之路开启｜Best Ideas

How To Play AI Beta：拾象 2026 AGI 投资思考开源

OpenAI 关键九问：2026 AI 战局升级后迎来叙事反转