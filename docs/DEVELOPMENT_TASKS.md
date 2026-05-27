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

## Phase 7：真实 LLM Live Mode 灰度与自动调度 v1

### P7-001：MiniMax Proponent Live Adapter Pilot v1

状态：Done。

目标：

- 为 `llm_proponent_agent` 增加 MiniMax live adapter。
- 默认仍 dry-run。
- live 必须显式启用。
- API key 只从环境变量读取。
- live 失败 fallback。
- 所有调用写 agent run log。

### P7-002：Claude Critic Live Adapter Pilot v1

状态：Done。

目标：

- 为 `llm_critic_agent` 增加 Claude live adapter。
- 默认仍 dry-run。
- live 必须显式启用。
- API key 只从环境变量读取。
- live 失败 fallback。
- 所有调用写 agent run log。

### P7-003：Claude Judge Live Adapter Pilot v1

状态：Done。

目标：

- 为 `llm_judge_agent` 增加 Claude live adapter。
- 只做旁路 judge，不覆盖 rule judge。
- 记录 rule / LLM comparison。
- 冲突进入 human spot-check 建议。

### P7-004：Claude Rewrite Live Pilot v1

状态：Done。

目标：

- 为 `llm_rewrite_agent` 增加 Claude live adapter。
- 只生成改稿建议，不覆盖原稿。
- 输出 suggestion-only 字段与 do-not-auto-apply 标记。

### P7-005：LLM Agent A/B Comparison v1

状态：Done。

目标：

- 比较 rule / mock / live 输出质量。
- 统计 judge conflict、critic severity difference、fallback、cost 和 human spot-check items。

### P7-006：Daily Scheduler v1

状态：Done。

目标：

- 建立本地调度文档和入口。
- 不自动安装 cron / launchd。
- 不自动启用 live。

### P7-007：Failure Notification v1

状态：Done。

目标：

- 生成失败通知报告。
- 汇总 pipeline、agent、live、fallback 和成本提示。
- 不接真实微信/邮件推送。

### P7-008：Retry / Fallback Runner v1

状态：Done。

目标：

- 基于 source runtime health 和 failure report 生成 retry/fallback plan。
- 不重写 fetcher。
- 不自动大规模补抓。

### P7-009：Weekly Content Retro v1

状态：Done。

目标：

- 每周复盘 high-value candidates、publishing queue、人工反馈、Agent 输出质量和规则建议。

### P7-010：Phase 7 Daily Pipeline v1

状态：Done。

目标：

- 新增 `make phase7-daily`。
- 串联 phase6 dry-run safe pipeline、live pilot readiness、A/B comparison、scheduler dry-run、failure report、retry plan 和 weekly retro。

### P7-011：Phase 7 Closeout

状态：Done。

目标：

- 新增 Phase 7 closeout 报告。
- 更新项目状态和任务清单。
- 明确 Phase 8 入口。

## Phase 8：生产化运行、数据库化长期记忆与发布集成

### P8-001：SQLite Runtime Store v1

目标：

- 建立本地 SQLite runtime store。
- 记录 pipeline run、agent run、source health、content artifact index。
- 不替换现有 JSON/Markdown 产物，先做同步索引。

### P8-002：Content / Agent Result Repository v1

目标：

- 为 evidence、brief、draft、review、publish candidate、agent output 建立统一 repository API。
- 保持文件产物可读、可导出。

### P8-003：Publishing API Dry-run Adapter v1

目标：

- 建立微信公众号 / 小红书发布 API 的 dry-run adapter。
- 不真实发布。
- 只验证字段、素材、平台包结构。

### P8-004：Human Review UI / Console v1

目标：

- 给人工审核、反馈、发布候选确认提供轻量本地 UI 或控制台入口。
- 不绕过 human confirmation。

### P8-005：Cost Budget Guard v1

目标：

- 统一读取 agent run log 与 provider config。
- 在 live 调用前检查每日成本预算和调用次数上限。
- 超限时自动降级为 dry-run / fallback。

### P8-006：Production Runbook v1

目标：

- 整理生产化运行手册。
- 包括调度、密钥、本地备份、失败恢复、人工审核、发布 dry-run 和成本控制。
