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

## Phase 14：内容表现驱动的选题与写作策略优化 v1

### P14-001：Performance-aware Topic Scoring v1

目标：

- 将人工录入的真实发布表现作为选题评分的参考信号。
- 只生成 scoring suggestion，不自动覆盖 value scoring rules。

### P14-002：Performance-aware Title Pattern Update v1

目标：

- 基于高表现和低表现内容更新标题模式优先级建议。
- 不自动改 title pattern registry。

### P14-003：Performance-aware Opening Strategy Update v1

目标：

- 分析不同开头模式与阅读、在看、转发的关系。
- 输出 opening strategy 建议。

### P14-004：Performance-aware Evidence Strategy v1

目标：

- 评估证据强度与发布后表现之间的关系。
- 区分“证据不足”和“标题/开头弱”导致的低表现。

### P14-005：Chief Editor Preference Profile v1

目标：

- 将人工反馈、版本接受记录和发布表现合并为 Chief Editor 偏好画像。
- 辅助后续主编 Agent 更贴近用户判断。

### P14-006：Weekly Strategy Review Board v1

目标：

- 每周汇总选题、标题、开头、证据、结构和 Agent action 的表现。
- 为人工策略复盘提供看板。
