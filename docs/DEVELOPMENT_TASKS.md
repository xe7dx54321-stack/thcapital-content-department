# 后续开发任务清单

## 开发原则

- 每轮只推进一个清晰 checkpoint。
- 每个 checkpoint 必须维护 `docs/PROJECT_STATE.md` 和本文件。
- 不重写现有 fetcher，除非该 checkpoint 明确要求。
- 不改变现有抓取脚本输出格式，除非已有验收方案覆盖。
- 不新增数据库、调度系统、retry/fallback、LLM 调用或新信源，除非 checkpoint 明确要求。
- generated artifacts 不进入 Git。

## Phase 0：工程地基修复与 official lane 稳定化

### 已完成

- P0-001 项目状态与健康检查底座。
- P0-002 路径硬编码审计工具。
- P0-002b 清理 path audit 生成产物入库问题。
- P0-003 路径配置化第一刀。
- P0-003b 修复/确认核心路径配置文件格式与验收链路。
- P0-004 HIGH 风险路径配置化第二刀。
- P0-005 Source Registry v1。
- P0-006 Source Health v1。
- P0-007 Source Runtime Health Adapter v1。
- P0-007b 补齐 Source Runtime Health 状态文档。
- P0-008 Runtime Manifest Contract v1。
- P0-009 Runtime Manifest Writer v1。
- P0-010 Official Lane Runtime Manifest Pilot Integration v1。
- P0-010b 补齐 official lane / runtime health generated artifacts ignore 规则。
- P0-011A Source Runtime Health Manifest Reader。
- P0-011B Official Lane Health Check Wrapper v1。
- P0-012 Official Lane Daily Entry v1。
- P0-013 Daily Source Run Summary v1。
- P0-014 Daily Official Lane Quality Gate v1。
- P0-014b 补齐 Quality Gate 状态文档。
- P0-015 Official Daily Dashboard v1。
- P0-015b 补齐 Official Daily Dashboard 状态文档。
- P0-016 Official Daily Full Run v1。
- P0-017 Phase 0 Closeout。

## Phase 0 验收标准

- `make doctor` 通过，或只有默认 network_check 跳过的 WARN。
- `make path-audit` 通过。
- `make sources-validate` 通过。
- `make source-health` 通过。
- `make manifest-validate` 通过。
- `make official-daily-full-run` 通过。
- official lane 能生成 runtime manifest、source runtime health、daily summary、quality gate、dashboard 和 full run summary。
- generated artifacts 不进入 Git。

## Phase 1：采集稳定性与结构化信息层

### P1-001：Official Lane Runtime Baseline 7-day Observation

目标：

- 连续 7 天记录 official lane daily full run 结果。
- 观察 source_count、total_items_found、quality gate status、missing_expected、error_hint_sources。
- 不改 fetcher，只建立 baseline。

验收：

- 每天保留 official daily full run 的 JSON/Markdown 本地报告。
- 形成 7-day baseline 汇总。
- 明确正常波动区间和异常阈值建议。

### P1-002：Source Registry Coverage Alignment

目标：

- 对齐 registry 17 个 source 与实际 official lane / topic capture lane 的 source_id。
- 明确哪些 source 已被 runtime manifest 覆盖，哪些仍只有 registry 配置。
- 输出 coverage gap 列表。

验收：

- source registry 中每个 source 都有 coverage 状态。
- official lane 已覆盖 source 与 registry source_id 显式对齐。
- topic capture lane 仍未 manifest 化的 source 有明确后续计划。

### P1-003：Evidence Packet v1

目标：

- 为抓取结果定义标准 evidence packet。
- 不直接写文章，先把信息结构化。
- 保存标题、来源、发布时间、原始链接、摘要、证据强度、可视素材提示等字段。

验收：

- 定义 evidence packet schema。
- 能从 official lane 或已有 packet 中生成样例 evidence packet。
- 不改变原始 fetcher 输出格式。

### P1-004：Topic Cluster v1

目标：

- 将 normalized evidence packet 聚类为 topic cluster。
- 支持按 company/product/model/research/theme 聚合。
- 为后续选题筛选和去重做准备。

验收：

- 能读取 evidence packet 样例。
- 能输出 topic cluster JSON/Markdown。
- 聚类逻辑可解释，且不依赖 LLM。

### P1-005：Value Scoring v1

目标：

- 基于 source authority、freshness、novelty、strategic relevance、market impact、technical substance、narrative potential、evidence strength 建立初步评分。
- 为 Top20/选题池提供结构化价值判断依据。

验收：

- 定义评分字段和权重初版。
- 对样例 topic cluster 输出评分。
- 评分报告能解释每个高分项原因和低分风险。

## 暂不开始

- 内容生成逻辑重写。
- 微信公众号、小红书、知乎等平台发布链路重构。
- 新信源接入。
- retry/fallback 执行系统。
- 数据库化。
- LLM 参与的自动写稿/改稿链路。
