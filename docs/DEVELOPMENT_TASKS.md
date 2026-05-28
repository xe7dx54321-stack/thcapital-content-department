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

目标：

- 为 pending actions 增加人工批准/拒绝/修改状态。
- 仍不自动发布。

### P10-002：Rewrite Action Executor v1

目标：

- 根据已批准的 rewrite action 生成候选修订稿。
- 不覆盖原稿。

### P10-003：Evidence Expansion Executor v1

目标：

- 根据 evidence expansion action 生成补证据任务。
- 不重写 fetcher。

### P10-004：Topic Replacement Executor v1

目标：

- 根据 topic replacement action 生成替换选题建议。
- 保留人工确认。

### P10-005：Versioned Article Preview v1

目标：

- 为原稿和候选修订稿生成版本化预览。

### P10-006：Workbench Interaction Server v1

目标：

- 建立只监听 `127.0.0.1` 的本地交互 server。
- 支持从页面提交 Chief Editor message。
