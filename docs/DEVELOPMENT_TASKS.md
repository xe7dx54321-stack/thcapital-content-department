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

### P16-001：Live Methodology Brief Agent Pilot v1

状态：Done。

目标：

- 在显式 live env + allowlist 下，为 methodology-aware brief generation 增加旁路 live pilot。
- 输出 sidecar brief，不替换规则型 brief。

### P16-002：Live Methodology Draft Agent Pilot v1

状态：Done。

目标：

- 在显式 live env + allowlist 下，为 methodology-aware draft generation 增加旁路 live pilot。
- 输出 sidecar draft，不覆盖原稿。

### P16-003：Live Methodology Rewrite Agent Pilot v1

状态：Done。

目标：

- 根据 methodology article review 的低分项生成 live rewrite sidecar。
- 不替换 existing methodology rewrite versions。

### P16-004：Live Visual Prompt Agent Pilot v1

状态：Done。

目标：

- 在显式 live env + allowlist 下，为 visual prompt / design brief 增加旁路 live pilot。
- 不自动调用图片模型，不生成图片。

### P16-005：Live Output Quality Comparison v1

状态：Done。

目标：

- 对比 rule-based / methodology-generated / live-generated 输出质量。
- 只生成建议，不自动 use live。

### P16-006：Human Calibration Feedback Apply v1

状态：Done。

目标：

- 将人工方法论校准反馈转成可审阅建议，不自动修改配置。

### P16-007：Image Generation Manual Approval Queue v1

状态：Done。

目标：

- 建立图片生成的人工批准流。
- 只有用户明确批准和配置接口后才允许生成图片。
- 即使 APPROVED，本轮也不生成图片。

### P16-008：Workbench Live Pilot Panel v1

状态：Done。

目标：

- 在微信公众号工作台展示 live pilot 输出、quality comparison、calibration 和 image approval queue。

### P16-009：Phase 16 Daily Live Pilot Pipeline v1

状态：Done。

目标：

- 串联 Phase15、四个 live pilot、输出对比、校准板、图片生成审批队列和工作台刷新。
- 默认 dry-run，不自动发布，不自动生成图片，不自动替换主线产物。

### P16-010：Phase 16 Closeout

状态：Done。

目标：

- 新增 Phase 16 closeout 报告。
- 明确 Phase 17 入口。

## Phase 17：Approved Live Output Promotion & Manual Image Generation v1

### P17-001：Approved Live Brief/Draft Promotion v1

状态：Done。

目标：

- 将人工接受的 live brief / draft sidecar 提升为候选版本，不自动替换主线产物。

### P17-002：Live Rewrite Version Promotion v1

状态：Done。

目标：

- 将人工接受的 live rewrite sidecar 纳入 versioned rewrite workflow。

### P17-003：Manual Image Generation Executor v1

状态：Done。

目标：

- 只在人工批准后执行图片生成或人工设计请求。

### P17-004：Image Asset Library v1

状态：Done。

目标：

- 建立本地图片资产索引、来源说明和版权审查记录。

### P17-005：Article-with-Images Preview v1

状态：Done。

目标：

- 生成带图片占位/已批准图片的公众号预览。

### P17-006：Human Final Visual Review v1

状态：Done。

目标：

- 为最终图片使用建立人工视觉审核流程。

### P17-007：Workbench Image Asset Panel v1

状态：Done。

目标：

- 在微信公众号工作台展示 approved live promotion、manual image tasks、image asset library、article-with-images preview 和 final visual review。

### P17-008：Phase 17 Daily Visual Production Pipeline v1

状态：Done。

目标：

- 串联 Phase16、live promotion、manual image tasks、asset library、图文预览、视觉审查和工作台刷新。
- 不自动生成图片，不自动发布，不替换主线产物。

### P17-009：Phase 17 Closeout

状态：Done。

目标：

- 新增 Phase 17 closeout 报告。
- 明确 Phase 18 入口。

## Phase 18：Article-with-Images Final Candidate & Manual Publishing Pack v1

### P18-001：Visual-approved Final Article Candidate v1

状态：Done。

### P18-002：WeChat Copy Pack with Image Slots v1

状态：Done。

### P18-003：Manual Publishing Checklist with Visual Assets v1

状态：Done。

### P18-004：Post-publish Visual Performance Input v1

状态：Done。

### P18-005：Visual Strategy Learning Feedback v1

状态：Done。

### P18-006：Workbench Publishing Pack Panel v1

状态：Done。

### P18-007：Phase 18 Daily Publishing Pack Pipeline v1

状态：Done。

### P18-008：Phase 18 Closeout

状态：Done。

## Phase 19：Real Publishing Operations & Content Calendar v1

### P19-001：Manual Publishing Session Calendar v1

状态：Done。

### P19-002：Content Queue Priority Board v1

状态：Done。

### P19-003：Weekly Publishing Rhythm Planner v1

状态：Done。

### P19-004：Published Article Archive v1

状态：Done。

### P19-005：Post-publish Metrics Review Board v1

状态：Done。

### P19-006：Content Ops Closeout v1

状态：Done。

### P19-007：Workbench Content Ops Panel v1

状态：Done。

### P19-008：Phase 19 Daily Ops Pipeline v1

状态：Done。

### P19-009：Phase 19 Closeout

状态：Done。

## Phase 20：Content Ops Quality Hardening & Real-world Trial v1

### P20-001：One-week Trial Run Protocol v1

状态：Done。

### P20-002：Content Ops Failure Handling v1

状态：Done。

### P20-003：Publishing Checklist Regression v1

状态：Done。

### P20-004：Workbench UX Cleanup v1

状态：Done。

### P20-005：Operator Runbook v1

状态：Done。

### P20-006：Phase 0-19 System Closeout v1

状态：Done。

### P20-007：Phase 20 Daily Hardening Pipeline v1

状态：Done。

### P20-008：Phase 20 Closeout

状态：Done。

## Phase 21：One-week Real Trial Execution v1

### P21-001：Day 1 Trial Run

状态：Done。

### P21-002：Day 2 Trial Run

状态：Done。

### P21-003：Day 3 Trial Run

状态：Done。

### P21-004：Day 4 Trial Run

状态：Done。

### P21-005：Day 5 Trial Run

状态：Done。

### P21-006：Weekly Trial Retrospective

状态：Done。

### P21-007：Trial Fix Pack

状态：Done。

### P21-008：Phase 21 Closeout Report

状态：Done。

### P21-009：Phase 21 Trial Pipeline

状态：Done。

### P21-010：Workbench Trial Panel

状态：Done。

## Phase 22：Trial Fix Implementation & Stable Ops v1

### P22-001：High-severity Trial Fixes

状态：Done。

### P22-002：Workbench Friction Fixes

状态：Done。

### P22-003：Queue / Calendar Calibration

状态：Done。

### P22-004：Publishing Pack Readiness Repair

状态：Done。

### P22-005：Trial Closeout to Stable Ops

状态：Done。

### P22-006：Post-publish Feedback Integration

状态：Done。

### P22-007：Phase22 Daily Ops Pipeline

状态：Done。

### P22-008：Phase22 Closeout

状态：Done。

## Phase 23：High-priority Ops Issue Resolution & Stable Trial Readiness v1

### P23-001：High-priority Recurring Issue Resolution Plan v1

状态：Done。

### P23-002：Quick Fix Candidate Executor v1

状态：Done。

### P23-003：Content Queue Readiness Repair v1

状态：Done。

### P23-004：Publishing Calendar Readiness Calibration v1

状态：Done。

### P23-005：Trial Day Status Stabilizer v1

状态：Done。

### P23-006：Issue Resolution Verification Board v1

状态：Done。

### P23-007：Stable Trial Readiness Gate v1

状态：Done。

### P23-008：Workbench Stable Ops Panel v1

状态：Done。

### P23-009：Phase 23 Daily Stability Pipeline v1

状态：Done。

### P23-010：Phase 23 Closeout

状态：Done。

## Phase 24：Stable Ops Trial & Content Quality Calibration v1

### P24-001：Stable Trial Day 1

状态：Done。

### P24-002：Stable Trial Day 2

状态：Done。

### P24-003：Stable Trial Day 3

状态：Done。

### P24-004：Content Quality Calibration from Trial

状态：Done。

### P24-005：Ops-to-Methodology Feedback

状态：Done。

### P24-006：Stable Ops Readiness Review

状态：Done。

### P24-007：Workbench Stable Trial Panel

状态：Done。

### P24-008：Phase 24 Daily Stable Trial Pipeline

状态：Done。

### P24-009：Phase 24 Closeout

状态：Done。

## Phase 25：Stable Daily Ops Baseline & Operator Acceptance v1

### P25-001：Stable Daily Ops Baseline

状态：Done。

### P25-002：Operator Acceptance Checklist

状态：Done。

### P25-003：Daily Ops Command Simplification

状态：Done。

### P25-004：Stable Workbench Baseline

状态：Done。

### P25-005：Content Factory v1 Closeout

状态：Done。

### P25-006：Phase 25 Daily Baseline Pipeline

状态：Done。

### P25-007：Phase 25 Closeout

状态：Done。

## Phase 26：Upstream Intelligence Acquisition Reinforcement v1

### P26-001：Source Coverage Gap Audit

状态：Done。

### P26-002：High-value Source Expansion Plan

状态：Done。

### P26-003：Multi-lane Hot Signal Capture

状态：Done。

### P26-004：Fallback Search & Backfill Queue

状态：Done。

### P26-005：Daily Hot Material Pool

状态：Done。

### P26-006：Hot Material Quality Gate

状态：Done。

### P26-007：Workbench Hot Material Panel

状态：Done。

### P26-008：Stable Daily Ops Integration

状态：Done。

### P26-009：Phase 26 Daily Acquisition Pipeline

状态：Done。

### P26-010：Phase 26 Closeout

状态：Done。

## Phase 27：Selected Source Connector Implementation v1

### P27-001：P0 Source Connector Selection

状态：Done。

### P27-002：RSS / Official Blog Connector Hardening

状态：Done。

### P27-003：GitHub / HuggingFace / arXiv Lightweight Connector

状态：Done。

### P27-004：Manual URL Backfill Ingestion

状态：Done。

### P27-005：Connector Output Normalization

状态：Done。

### P27-006：Connector Regression and Source Health Gate

状态：Done。

### P27-007：Hot Material Pool Connector Integration

状态：Done。

### P27-008：Workbench Connector Health Panel

状态：Done。

### P27-009：Phase 27 Daily Connector Pipeline

状态：Done。

### P27-010：Phase 27 Closeout

状态：Done。

## Phase 28：Source Connector Expansion & Evidence Enrichment v1

### P28-001：P0 Connector Reliability Improvement

状态：Done。

### P28-002：Evidence Packet Enrichment from Connector Items

状态：Done。

### P28-003：Topic Candidate Promotion from Hot Materials

状态：Done。

### P28-004：Connector Freshness and Dedup Regression

状态：Done。

### P28-005：Acquisition-to-Content Bridge

状态：Done。

### P28-006：Workbench Evidence & Topic Promotion Panel

状态：Done。

### P28-007：Stable Daily Ops Acquisition Integration

状态：Done。

### P28-008：Phase 28 Daily Enrichment Pipeline

状态：Done。

### P28-009：Phase 28 Closeout

状态：Done。

## Phase 29：OpenClaw Source Migration & Signal Lane Integration v1

### P29-001：OpenClaw Source Inventory Import

状态：Done。

### P29-002：OpenClaw Source Risk Classification

状态：Done。

### P29-003：P0/P1 Migration Plan

状态：Done。

### P29-004：Reddit / YC / TechCrunch / FinSMEs / Newsletter / Chinese Media Metadata Connector

状态：Done。

### P29-005：Weak Signal Safety Gate

状态：Done。

### P29-006：OpenClaw Signal Normalization & Hot Material Integration

状态：Done。

### P29-007：Workbench Source Migration Panel

状态：Done。

### P29-008：Stable Daily Ops Source Supply Upgrade

状态：Done。

### P29-009：Phase 29 Daily Migration Pipeline

状态：Done。

### P29-010：Phase 29 Closeout

状态：Done。

## Phase 30：OpenClaw Migrated Signal Evidence Backfill & Topic Activation v1

### P30-001：OpenClaw Signal Evidence Backfill

状态：Done。

### P30-002：Weak Signal Confirmation Workflow

状态：Done。

### P30-003：Migrated Source Topic Candidate Promotion

状态：Done。

### P30-004：OpenClaw-to-Content Regression Gate

状态：Done。

### P30-005：OpenClaw Evidence / Topic Workbench Panel

状态：Done。

### P30-006：Stable Daily Ops OpenClaw Activation Integration

状态：Done。

### P30-007：Source Registry Proposal Sidecar

状态：Done。

### P30-008：Phase 30 Daily Activation Pipeline

状态：Done。

### P30-009：Phase 30 Closeout

状态：Done。

## Phase 31：Autonomous Content Factory Runtime & End-to-End Daily Orchestration v1

### P31-001：Autonomous Runtime Configuration

状态：Done。

### P31-002：Persistent Scheduler State & Execution Ledger

状态：Done。

### P31-003：Internal Scheduler & Job Registry

状态：Done。

### P31-004：End-to-End Daily Pipeline Graph

状态：Done。

### P31-005：Retry / Backoff / Checkpoint / Idempotency

状态：Done。

### P31-006：Network & VPN-aware Acquisition Routing

状态：Done。

### P31-007：Missed-run Recovery & Catch-up

状态：Done。

### P31-008：Runtime Heartbeat & Failure Notification

状态：Done。

### P31-009：Runtime Control API / CLI

状态：Done。

### P31-010：Workbench Runtime Control Center

状态：Done。

### P31-011：macOS launchd Bootstrap & Runbook

状态：Done。

### P31-012：OpenClaw Scheduling Coexistence Guard

状态：Done。

### P31-013：Autonomous End-to-End Dry Run

状态：Done。

### P31-014：Phase 31 Closeout

状态：Done。

## Phase 31B：Mac mini Autonomous Runtime Go-Live & Observation v1

### P31B-001：Go-Live Preflight Audit

状态：Done。

### P31B-002：OpenClaw Conflict Resolution & Rollback Pack

状态：Done。

### P31B-003：macOS LaunchAgent Production Installation

状态：Done。

### P31B-004：Runtime Startup / Heartbeat / Restart Validation

状态：Done。

### P31B-005：Real Scheduler Trigger Validation

状态：Done。

### P31B-006：Missed-run & Catch-up Live Validation

状态：Done。

### P31B-007：Duplicate-run / Idempotency Live Validation

状态：Done。

### P31B-008：Workbench Autonomous Runtime Acceptance

状态：Done。

### P31B-009：Go-Live Safety & Cost Observation

状态：Done。

### P31B-010：Go-Live Acceptance Gate

状态：Done。

### P31B-011：Phase 31B Closeout

状态：Done。

## Phase 32：Autonomous Topic-to-Article Production Activation v1

进入条件：Phase31B go-live gate 为 `GO_LIVE_APPROVED` 或 `GO_LIVE_WITH_WARNINGS` 且 blocking_failures=0。

### P32-001：Confirmed Topic Scoring

状态：Planned。

### P32-002：Automated Topic Selection

状态：Planned。

### P32-003：Automated Brief Generation

状态：Planned。

### P32-004：Automated Outline / Draft Generation

状态：Planned。

### P32-005：Multi-Agent Review and Rewrite

状态：Planned。

### P32-006：Final Candidate Workbench Delivery

状态：Planned。

### P32-007：Autonomous Content Production Regression Gate

状态：Planned。
