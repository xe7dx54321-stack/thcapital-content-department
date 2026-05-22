# 后续开发任务清单

## 开发原则

- 每个 checkpoint 都要有目标、变更文件、验收方式和下一步建议。
- 先保证可运行、可检查、可交接，再扩大自动化范围。
- 不破坏 official lane、topic capture lane 和现有生成产物格式。
- generated artifacts 默认不进入 Git；需要共享时提取小型摘要。
- 不提交 `.env`、本机绝对路径、cookie、token、数据库或本地运行态文件。
- 自动发布、LLM 生成、真实平台 API、人工反馈学习都必须有独立 checkpoint。

## Phase 0：已完成

- P0-001 到 P0-017 已完成，覆盖工程底座、路径配置、source registry、runtime manifest、official lane daily full run、quality gate 与 dashboard。

## Phase 1：已完成

- P1-001 到 P1-007 已完成，覆盖 evidence packet、topic cluster、value scoring、high-value candidate pool 与 phase1 daily pipeline。

## Phase 2：已完成

- P2-001 到 P2-008 已完成，覆盖 content brief、outline、draft、quality review、platform package、content workbench 与 phase2 daily pipeline。

## Phase 3：已完成

- P3-001 到 P3-009 已完成，覆盖 agent review queue、proponent / critic / judge、revision instructions、human exception queue、agent review dashboard 与 phase3 daily pipeline。

## Phase 4：发布准备、反馈学习与策略迭代 v1

### P4-001：Publishing Candidate Queue v1

状态：Done。

目标：

- 将 Judge Gate 通过的内容进入发布候选队列。
- 不自动发布。
- 为每个 package 记录 publish readiness、platform、人工确认状态。

### P4-002：Human Feedback Capture v1

状态：Done。

目标：

- 生成人工反馈模板。
- 校验 human_action、human_score、publishing_candidate_id 和 title。
- 保持文件型反馈，不引入 UI 或数据库。

### P4-003：Review Outcome Memory v1

状态：Done。

目标：

- 汇总 publishing candidate、human feedback、judge/proponent/critic 结果。
- 以 JSON/Markdown 形式维护轻量历史记忆。

### P4-004：Rule Update Suggestion v1

状态：Done。

目标：

- 基于 outcome memory 生成规则调整建议。
- 不自动修改 value scoring、brief、outline、review rules。

### P4-005：Learning Loop Dashboard v1

状态：Done。

目标：

- 展示 publishing candidates、pending feedback、recent outcomes、feedback tags 和 rule suggestions。

### P4-006：Phase 4 Daily Pipeline v1

状态：Done。

目标：

- 新增 `make phase4-daily`。
- 串联 Phase 3 daily、publishing candidates、feedback template、feedback validation、outcome memory、rule suggestions 和 dashboard。

### P4-007：Phase 4 Closeout

状态：Done。

目标：

- 新增 Phase 4 closeout 报告。
- 维护项目状态和任务清单。

## Phase 5：头部内容学习反哺系统 v1

### P5-001：Head Media Pattern Library v1

状态：Done。

目标：

- 建立统一 pattern library 文件结构。
- 将当前内容资产中的可复用标题、开头、结构、角度和平台模式记录为模式库。

### P5-002：Title Pattern Extractor v1

状态：Done。

目标：

- 从 outlines、drafts、platform packages 中抽取标题模式。
- 识别 question、numbered_list、contrast、why_now、big_company、new_opportunity、risk_warning、how_to、trend_signal、case_study 等类型。

### P5-003：Opening Pattern Extractor v1

状态：Done。

目标：

- 抽取文章开头模式。
- 识别 news_first、contrarian、problem_solution、data_hook、scenario_hook、question_hook、executive_summary、trend_observation。

### P5-004：Article Structure Pattern Extractor v1

状态：Done。

目标：

- 抽取文章结构模式。
- 识别 news_analysis、trend_analysis、company_breakdown、technical_explainer、investment_logic、tool_guide、listicle、case_study。

### P5-005：Content Recipe Suggestion v1

状态：Done。

目标：

- 将 title/opening/structure patterns 转成 content recipe 建议。
- 不自动应用到规则文件。

### P5-006：Pattern-to-Brief / Pattern-to-Outline Adapter v1

状态：Done。

目标：

- 将模式库以建议形式反哺 content brief 和 outline。
- 只生成 adapter recommendations，不改写 latest briefs/outlines。

### P5-007：Phase 5 Daily Learning Pipeline v1

状态：Done。

目标：

- 新增 `make phase5-daily`。
- 串联 pattern library、title/opening/structure extractors、recipe suggestions 和 pattern adapters。

### P5-008：Phase 5 Closeout

状态：Done。

目标：

- 新增 Phase 5 closeout 报告。
- 明确 Phase 6 入口。

## 总入口

### learning-daily

状态：Done。

目标：

- 新增 `make learning-daily`。
- 串联 Phase 3、Phase 4、Phase 5 日常链路。

## Phase 6：真实 LLM Agent 接入与多 Agent 调优

### P6-001：LLM Provider Config v1

目标：

- 建立 LLM provider 配置。
- 支持 OpenAI / Anthropic / Gemini 等 provider 占位。
- 不把 API key 提交进 Git。
- 先支持 dry-run / mock mode。

### P6-002：Prompt Registry v1

目标：

- 管理 proponent / critic / judge / rewrite agent 的 prompt。
- 支持版本号、输入 schema、输出 schema。

### P6-003：LLM Proponent Agent v1

目标：

- 用真实 LLM 替换或增强规则型 proponent review。
- 保留规则型 fallback。

### P6-004：LLM Critic Agent v1

目标：

- 用真实 LLM 做建设性批评。
- 输出结构化 critic review。

### P6-005：LLM Judge Agent v1

目标：

- 用真实 LLM 做裁判决策。
- 保留人工抽检阈值。

### P6-006：LLM Rewrite Agent v1

目标：

- 根据 revision instructions 自动生成改稿建议。
- 不自动发布。

### P6-007：Agent Run Log / Cost / Error Tracking v1

目标：

- 记录每次 Agent 调用、耗时、状态、成本、错误。

### P6-008：Human-in-the-loop Agent Evaluation v1

目标：

- 比较规则型 Agent 与 LLM Agent 的差异。
- 记录人工对 Agent 输出的评分。
