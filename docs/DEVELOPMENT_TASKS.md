# 后续开发任务清单

## 开发原则

- 每个 checkpoint 都要有目标、变更文件、验收方式和下一步建议。
- 先保证可运行、可检查、可交接，再扩大自动化范围。
- 不破坏 official lane、topic capture lane 和现有生成产物格式。
- generated artifacts 默认不进入 Git。
- 不提交 `.env`、本机绝对路径、cookie、token、数据库或本地运行态文件。
- live mode、真实平台 API、自动发布、长期记忆数据库必须分 checkpoint 灰度。

## Phase 0：已完成

- P0-001 到 P0-017 已完成，覆盖工程底座、路径配置、source registry、runtime manifest、official lane daily full run、quality gate 与 dashboard。

## Phase 1：已完成

- P1-001 到 P1-007 已完成，覆盖 evidence packet、topic cluster、value scoring、high-value candidate pool 与 phase1 daily pipeline。

## Phase 2：已完成

- P2-001 到 P2-008 已完成，覆盖 content brief、outline、draft、quality review、platform package、content workbench 与 phase2 daily pipeline。

## Phase 3：已完成

- P3-001 到 P3-009 已完成，覆盖 agent review queue、proponent / critic / judge、revision instructions、human exception queue、agent review dashboard 与 phase3 daily pipeline。

## Phase 4：已完成

- P4-001 到 P4-007 已完成，覆盖 publishing candidate queue、human feedback template、review outcome memory、rule update suggestions、learning loop dashboard 与 phase4 daily pipeline。

## Phase 5：已完成

- P5-001 到 P5-008 已完成，覆盖 head media pattern library、title/opening/structure pattern extraction、content recipe suggestions、pattern adapters、phase5 daily learning pipeline 与 learning daily pipeline。

## Phase 6：已完成

- P6-001 到 P6-011 已完成，覆盖 LLM provider config、prompt registry、mock/dry-run client、LLM agent 输出、run log、成本/错误追踪、人工评估模板与 phase6 daily pipeline。

## Phase 7：已完成

- P7-001 到 P7-011 已完成，覆盖 MiniMax/Claude live pilot、A/B comparison、daily scheduler、failure report、retry/fallback plan、weekly retro 与 phase7 daily pipeline。

## Phase 8：已完成

- P8-001 到 P8-008 已完成，覆盖 SQLite runtime store、artifact repository、publishing dry-run、human review console、cost budget guard、production runbook 与 phase8 daily pipeline。

## Phase 9：微信公众号内容工作台与 Chief Editor Agent v1

### P9-001：WeChat Workbench Data Builder v1

状态：Done。

目标：

- 构建前台可用数据结构。
- 汇总推荐选题、公众号文章、Agent 审核、发布候选和系统状态。

### P9-002：WeChat Article Preview Renderer v1

状态：Done。

目标：

- 渲染公众号文章 HTML 预览。
- 模拟真实公众号阅读状态。

### P9-003：WeChat Workbench Frontend v1

状态：Done。

目标：

- 生成极简本地前台。
- 展示今日选题、公众号文章预览和底部 AI 对话框。

### P9-004：Workbench Context Builder v1

状态：Done。

目标：

- 为 Chief Editor Agent 构建上下文。
- 包含当前文章、证据、Agent 审核、source guidance 和 routing guidance。

### P9-005：Chief Editor Agent v1

状态：Done。

目标：

- 识别用户编辑诉求。
- 输出结构化 intent 和 action plan。
- 默认 PLAN_ONLY，不自动执行。

### P9-006：Workbench Action Router v1

状态：Done。

目标：

- 将 Chief Editor Agent response 写入 pending action queue。
- 所有 action `do_not_auto_execute=true`。

### P9-007：Workbench Feedback Memory v1

状态：Done。

目标：

- 沉淀用户偏好。
- 为后续规则建议和自动修订提供输入。

### P9-008：Phase 9 Daily Workbench Pipeline v1

状态：Done。

目标：

- 新增 `make phase9-daily`。
- 串联 Phase 8、工作台数据、文章预览、上下文、前台和反馈记忆。

### P9-009：Phase 9 Closeout

状态：Done。

目标：

- 新增 Phase 9 closeout 报告。
- 更新项目状态和任务清单。
- 明确 Phase 10 入口。

### P9-010：WeChat Workbench UI Polish v1

状态：Done。

目标：

- 打磨本地微信公众号工作台 UI/UX。
- 支持点击左侧选题切换文章。
- 增加阅读模式 / 审稿模式切换。
- 优化公众号文章预览和 Chief Editor 协作入口。
- 为 Phase 10 action execution 做体验准备。

## Phase 10：Workbench Action Execution 与稿件自动修订 v1

### P10-001：Manual Action Approval v1

状态：Done。

目标：

- 为 pending actions 增加人工批准/拒绝/修改状态。
- 仍不自动发布。

### P10-002：Rewrite Action Executor v1

状态：Done。

目标：

- 根据已批准的 rewrite action 生成候选修订稿。
- 不覆盖原稿。

### P10-003：Evidence Expansion Executor v1

状态：Done。

目标：

- 根据 evidence expansion action 生成补证据任务。
- 不重写 fetcher。

### P10-004：Topic Replacement Executor v1

状态：Done。

目标：

- 根据 topic replacement action 生成替换选题建议。
- 保留人工确认。

### P10-005：Versioned Article Preview v1

状态：Done。

目标：

- 为原稿和候选修订稿生成版本化预览。

### P10-006：Workbench Interaction Server v1

状态：Done。

目标：

- 建立只监听 `127.0.0.1` 的本地交互 server。
- 支持从页面提交 Chief Editor message。

### P10-007：Phase 10 Daily Action Pipeline v1

状态：Done。

目标：

- 串联 Phase 9、approval board、action executors、versioned preview 和 feedback memory。
- 不自动批准 action。

### P10-008：Phase 10 Closeout

状态：Done。

目标：

- 新增 Phase 10 closeout 报告。
- 明确 Phase 11 入口。

## Phase 11：Workbench Closed-loop Automation 与质量回归 v1

### P11-001：Version Comparison Scoring v1

状态：Done。

目标：

- 比较原稿和新版本质量。
- 输出标题、开头、逻辑、证据、公众号可读性、投资人视角、风险控制评分。

### P11-002：Human Accept / Reject Version v1

状态：Done。

目标：

- 人工决定是否接受候选版本。
- `ACCEPT` 不等于发布，也不覆盖原稿。

### P11-003：Article Version Memory v1

状态：Done。

目标：

- 记录版本变更、来源 action、自动评分、人工决策和 lessons。

### P11-004：Action Effectiveness Analytics v1

状态：Done。

目标：

- 分析哪些 action_type 提高了质量，哪些容易失败。
- 为后续 prompt/rule 调整提供证据。

### P11-005：Prompt / Rule Regression Dashboard v1

状态：Done。

目标：

- 汇总 prompt/rule 回归风险。
- 只生成建议，不自动修改配置。

### P11-006：Workbench UI Version Review Panel v1

状态：Done。

目标：

- 在工作台中展示版本评分、改进点、退化点、人工决策状态和 review CLI。

### P11-007：Phase 11 Daily Quality Loop Pipeline v1

状态：Done。

目标：

- 串联 Phase 10、version scoring、review board、version memory、action analytics、regression dashboard 和工作台刷新。

### P11-008：Phase 11 Closeout

状态：Done。

目标：

- 新增 Phase 11 closeout 报告。
- 明确 Phase 12 入口。

## Phase 12：Selected Version Promotion 与工作台闭环执行 v1

### P12-001：Accepted Version Promotion v1

状态：Done。

目标：

- 将人工接受的新版本提升为候选最终稿。
- 不自动发布，不覆盖历史原稿。

### P12-002：Final Article Candidate Builder v1

状态：Done。

目标：

- 从 accepted version 生成 final article candidate。
- 保留来源 action、版本评分和人工决策记录。

### P12-003：Human Final Publish Checklist v1

状态：Done。

目标：

- 生成发布前人工 checklist。
- 包含事实、证据、标题承诺、风险披露和平台格式检查。

### P12-004：Final Candidate Memory v1

状态：Done。

目标：

- 记录 final candidate 历史、checklist 状态和 lessons。
- 不把 final candidate 视为已发布。

### P12-005：Multi-day Version Analytics v1

状态：Done。

目标：

- 汇总多日版本改稿、接受率、promotion、final candidate 数量和质量趋势。

### P12-006：Workbench Final Review Panel v1

状态：Done。

目标：

- 将 final candidate 与 checklist 接入微信公众号工作台。
- 支持复制最终标题、正文和人工发布步骤。

### P12-007：Phase 12 Daily Finalization Pipeline v1

状态：Done。

目标：

- 串联 Phase 11、promotion、final candidate、checklist、memory、analytics 和工作台刷新。
- 不自动 accept，不自动 publish，不调用公众号 API。

### P12-008：Phase 12 Closeout

状态：Done。

目标：

- 新增 Phase 12 closeout 报告。
- 明确 Phase 13 入口。

## Phase 13：Workbench UI Server v2 与最终人工发布协作 v1

### P13-001：Workbench UI Server v2

状态：Done。

目标：

- 将当前静态工作台升级为更顺滑的本地交互服务。
- 继续只监听本机，不部署云端。
- 提供工作台数据、Chief Editor、final review、publish session 和 metrics 的本地白名单接口。

### P13-002：Interactive Final Review Actions v1

状态：Done。

目标：

- 支持在本地工作台中完成 final candidate 的人工确认动作。
- 所有动作仍写入文件型记录。
- 不发布、不调用平台 API。

### P13-003：Manual Publish Session Tracker v1

状态：Done。

目标：

- 记录人工复制、排版、预览、发布前确认过程。
- 不接公众号 API，不自动发布。
- 支持 create、mark-published、cancel、defer。

### P13-004：Post-publish Manual Metrics Input v1

状态：Done。

目标：

- 支持人工录入阅读、点赞、在看、转发等发布后表现数据。
- 不自动抓取平台数据。
- 生成表现数据看板和辅助 performance rating。

### P13-005：Content Performance Memory v1

状态：Done。

目标：

- 将发布后表现和内容版本、选题、标题、证据质量关联起来。
- 沉淀 title/opening pattern 和内容表现 lessons。

### P13-006：Performance-to-Learning Feedback Loop v1

状态：Done。

目标：

- 把内容表现反馈到选题、标题、开头、结构、规则建议和 Chief Editor 偏好中。
- 所有建议 `auto_apply=false`，不自动改配置。

### P13-007：Workbench Performance Panel v1

状态：Done。

目标：

- 在工作台展示人工发布 session、表现指标、performance memory 和学习反馈。
- 保留静态 HTML 的 CLI 命令复制 fallback。

### P13-008：Phase 13 Daily Performance Pipeline v1

状态：Done。

目标：

- 串联 Phase 12、发布 session board、metrics board、performance memory、learning feedback 和工作台刷新。
- 不自动创建 session，不自动录入 metrics，不自动发布。

### P13-009：Phase 13 Closeout

状态：Done。

目标：

- 新增 Phase 13 closeout 报告。
- 明确 Phase 14 入口。

## Phase 14：Content Strategy Methodology Core v1

### P14-001：Topic Selection Methodology v1

状态：Done。

目标：

- 建立统一的选题方法论。
- 定义 8 个核心维度、一票否决项和进入写作链路前的问题清单。

### P14-002：Article Quality Methodology v1

状态：Done。

目标：

- 建立统一的公众号文章质量方法论。
- 定义 10 个质量标准、结构组件和空泛表达识别。

### P14-003：Content Strategy Recipes v1

状态：Done。

目标：

- 建立趋势判断、产业链预期、公司拆解、技术路线、产品战略、投资框架 6 类打法。
- 与既有 title/opening/structure pattern 模块衔接。

### P14-004：Methodology-based Topic Scoring v1

状态：Done。

目标：

- 在原 value scoring 之外新增方法论选题评分。
- 输出 WRITE / WATCH / HOLD / REJECT 和推荐 recipe。

### P14-005：Methodology-based Article Review v1

状态：Done。

目标：

- 用文章方法论评审当前 draft、final candidate 和 rewrite version。
- 输出弱点、空泛表达、缺失结构和重写优先级。

### P14-006：Chief Editor Methodology Adapter v1

状态：Done。

目标：

- 为 Chief Editor 构建方法论上下文。
- 让 Chief Editor 的 action plan 引用选题/文章方法论。

### P14-007：Workbench Methodology Panel v1

状态：Done。

目标：

- 在微信公众号工作台展示选题方法论评分、文章方法论评分、推荐 recipe 和重写优先级。

### P14-008：Methodology-to-Performance Feedback Alignment v1

状态：Done。

目标：

- 将 performance feedback 与方法论维度对齐。
- 只生成建议，不自动修改 config/prompt/rules。

### P14-009：Phase 14 Daily Methodology Pipeline v1

状态：Done。

目标：

- 串联 Phase 13、方法论验证、选题评分、文章评审、Chief Editor 方法论上下文、表现对齐和工作台刷新。

### P14-010：Phase 14 Closeout

状态：Done。

目标：

- 新增 Phase 14 closeout 报告。
- 明确 Phase 15 入口。

## Phase 15：Methodology-driven Content Generation & Visual Strategy v1

### P15-001：Methodology-aware Brief Builder v1

状态：Done。

目标：

- 让 content brief 直接引用选题方法论、文章方法论和推荐 recipe。
- 输出 core question、core judgment、why now、expectation gap、证据计划和 visual opportunities。

### P15-002：Methodology-aware Outline Builder v1

状态：Done。

目标：

- 让 outline 按 recipe 和文章结构组件组织。
- 每节明确 section question、section claim、证据对齐和 visual slot。

### P15-003：Methodology-aware Draft Writer v1

状态：Done。

目标：

- 让 draft writer 按文章质量方法论生成更高判断密度的稿件。
- 输出 title options、opening、body、closing、visual slots 和 methodology self check。

### P15-004：Methodology-aware Rewrite Executor v1

状态：Done。

目标：

- 让 rewrite executor 按方法论评分的弱点和优先级执行改稿。
- 只生成 methodology rewrite version，不覆盖原稿。

### P15-005：Article Visual Strategy Methodology v1

状态：Done。

目标：

- 建立公众号文章图片策略方法论。
- 定义 cover visual、concept diagram、value chain map、timeline chart、comparison visual、framework diagram、process flow、evidence snapshot 等图片类型。

### P15-006：Visual Plan Builder v1

状态：Done。

目标：

- 为每篇公众号文章生成 visual plan。
- 明确每张图的 placement、information job、source strategy 和 quality checks。

### P15-007：Image Prompt & Asset Request Builder v1

状态：Done。

目标：

- 根据 visual plan 生成 image prompt、design brief 和 asset request。
- 不自动生成图片，不自动调用图片模型。

### P15-008：Methodology Regression Test Set v1

状态：Done。

目标：

- 建立固定方法论回归测试样例。
- 覆盖好/坏选题、强/弱标题、强/弱开头、逻辑、证据和视觉计划。

### P15-009：Human Methodology Calibration Board v1

状态：Done。

目标：

- 提供人工校准方法论判断、文章弱点、content recipe、视觉计划和图片需求的看板。

### P15-010：Workbench Generation & Visual Panel v1

状态：Done。

目标：

- 在微信公众号工作台展示 methodology brief、outline、draft status、visual plan 和 image asset requests。
- 阅读模式保持干净，图片策略只在审稿/右侧面板展示。

### P15-011：Phase 15 Daily Generation Pipeline v1

状态：Done。

目标：

- 串联 Phase 14、methodology generation、visual methodology、visual plan、image asset requests、regression tests、calibration board 和工作台刷新。
- 不自动生成图片，不自动发布，不自动修改 config/prompt/rules。

### P15-012：Phase 15 Closeout

状态：Done。

目标：

- 新增 Phase 15 closeout 报告。
- 明确 Phase 16 入口。

## Phase 16：Methodology-driven Live Agent Generation Pilot v1

### P16-001：Live Methodology Brief Agent Pilot

目标：

- 在显式 live env + allowlist 下，为 methodology-aware brief generation 增加旁路 live pilot。

### P16-002：Live Methodology Draft Agent Pilot

目标：

- 在显式 live env + allowlist 下，为 methodology-aware draft generation 增加旁路 live pilot。

### P16-003：Live Visual Prompt Agent Pilot

目标：

- 在显式 live env + allowlist 下，为 visual prompt / design brief 增加旁路 live pilot。

### P16-004：Human Calibration Feedback Apply v1

目标：

- 将人工方法论校准反馈转成可审阅建议，不自动修改配置。

### P16-005：Image Generation Manual Approval Flow v1

目标：

- 建立图片生成的人工批准流。
- 只有用户明确批准和配置接口后才允许生成图片。
