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

## Phase 8：生产化运行、数据库化长期记忆与发布集成 v1

### P8-001：SQLite Runtime Store v1

状态：Done。

目标：

- 建立本地 SQLite runtime store。
- 记录 pipeline run、agent run、source health、content artifact index。
- 不替换现有 JSON/Markdown 产物，先做同步索引。

### P8-002：Content / Agent Result Repository v1

状态：Done。

目标：

- 为 evidence、brief、draft、review、publish candidate、agent output 建立统一 repository API。
- 保持文件产物可读、可导出。

### P8-003：Publishing API Dry-run Adapter v1

状态：Done。

目标：

- 建立微信公众号 / 小红书发布 API 的 dry-run adapter。
- 不真实发布。
- 只验证字段、素材、平台包结构。

### P8-004：Human Review UI / Console v1

状态：Done。

目标：

- 给人工审核、反馈、发布候选确认提供轻量本地 console。
- 不绕过 human confirmation。

### P8-005：Cost Budget Guard v1

状态：Done。

目标：

- 统一读取 agent run log 与 provider config。
- 检查每日成本预算和调用次数上限。
- 超限时建议 dry-run / fallback，不自动修改配置。

### P8-006：Production Runbook v1

状态：Done。

目标：

- 整理生产化运行手册。
- 包括调度、密钥、本地备份、失败恢复、人工审核、发布 dry-run 和成本控制。

### P8-007：Phase 8 Daily Production Pipeline v1

状态：Done。

目标：

- 新增 `make phase8-daily`。
- 串联 Phase 7、runtime store、artifact repository、publishing dry-run、human review console 和 cost guard。

### P8-008：Phase 8 Closeout

状态：Done。

目标：

- 新增 Phase 8 closeout 报告。
- 更新项目状态和任务清单。
- 明确 Phase 9 入口。

## Phase 9：真实发布集成与人机协作 UI

### P9-001：Publishing Platform Credential Config v1

目标：

- 建立发布平台凭证配置结构。
- 凭证只从环境变量读取。
- 不提交 token、cookie、session 或 `.env`。

### P9-002：Wechat Draft API Dry-run to Sandbox v1

目标：

- 先对接微信草稿 API 的 sandbox / dry-run 入口。
- 不直接发布。
- 保留人工确认。

### P9-003：Xiaohongshu Manual Package Export v1

目标：

- 生成小红书人工发布包。
- 包括标题、正文、标签、图片 brief、证据和风险提示。
- 不调用真实发布 API。

### P9-004：Review Console UI v2

目标：

- 将 human review console 升级为更易用的人机协作界面。
- 支持候选筛选、确认、反馈记录和导出。

### P9-005：Production Backup / Restore v1

目标：

- 为 runtime store 和关键 generated artifacts 建立本地备份/恢复流程。
- 不上传外部服务。

### P9-006：Multi-day Analytics Dashboard v1

目标：

- 汇总多日 pipeline、content、agent、feedback、cost 数据。
- 支持观察质量变化和系统稳定性。
