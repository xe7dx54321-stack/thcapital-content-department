# 后续开发任务清单

## 开发原则

- 小步交付，每个 checkpoint 都要有目标、变更文件、验收方式和下一步建议。
- 优先维护工程底座、状态文档、检查工具和运行观测，再扩展业务能力。
- 不大规模重写已有抓取主链路，尤其不破坏 official lane 和 topic capture lane 的现有输出。
- generated artifacts 默认不进入 Git；需要共享时提取小型摘要。
- 不提交 `.env`、本机绝对路径、cookie、token、数据库或本地运行态文件。

## Phase 0：已完成

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

## Phase 1：采集稳定性与信息结构化 v1

### P1-001：Official Lane Runtime Baseline v1

状态：Done。

目标：

- 把 official daily full run 的关键指标追加到 baseline。
- 同一天重复运行更新同一条 record。
- 支撑后续 7 天/30 天稳定性观察。

验收：

- `make runtime-baseline` 可生成 baseline JSON/Markdown。
- baseline 记录 status、quality gate、items、missing expected、dashboard status 等核心指标。

### P1-002：Source Registry Coverage Alignment v1

状态：Done。

目标：

- 对齐 `config/sources.yaml` 与 latest official runtime manifest / source runtime health。
- 标记 covered、registry-only、runtime-only 和 alias 命名差异。
- 不修改 fetcher source_id。

验收：

- `make source-coverage` 可生成 coverage alignment 报告。
- runtime-only source 与 registry-only source 被明确展示。

### P1-003：Evidence Packet v1

状态：Done。

目标：

- 从 official packet item 生成标准 evidence packet。
- 规则型抽取 title、url、summary、event_type、entities、domain_tags 和基础分值。
- 不使用 LLM，不生成文章。

验收：

- `make evidence-packets` 可生成合法 JSON/Markdown。
- evidence packets 可以为空，但脚本不能崩溃。

### P1-004：Topic Cluster v1

状态：Done。

目标：

- 基于 evidence packet 做规则型聚类。
- 优先使用 company/product/model 实体交集，其次使用 event_type + title token。
- 不使用 embedding 或向量库。

验收：

- `make topic-clusters` 可生成合法 JSON/Markdown。
- topic clusters 可以为空，但脚本不能崩溃。

### P1-005：Value Scoring v1

状态：Done。

目标：

- 对 topic cluster 进行规则型价值评分。
- 评分维度包括 source authority、freshness、novelty、strategic relevance、market impact、technical substance、narrative potential、evidence strength。
- 输出 score band 和 recommended action。

验收：

- `make value-scores` 可生成合法 JSON/Markdown。
- `config/value_scoring_rules.json` 保存 v1 评分权重。

### P1-006：Daily High-Value Candidate Pool v1

状态：Done。

目标：

- 将 scored clusters 转成每天可读的 high-value candidate pool。
- Markdown 展示 summary、top candidates、details、key evidence 和 risks / missing info。
- 不进入成品内容生产。

验收：

- `make high-value-candidates` 可生成候选池 JSON/Markdown 和 frontstage board。

### P1-007：Phase 1 Closeout

状态：Done。

目标：

- 新增 Phase 1 closeout 报告。
- 新增 `make phase1-daily` 总入口。
- 明确 Phase 1 v1 的能力边界和 Phase 2 入口。

验收：

- `make phase1-daily` 可串联 Phase 1 v1 全链路。
- generated artifacts 不进入 Git。

## Phase 1 验收标准

- `python3 -m py_compile` 对新增 scripts 和 modules 全部通过。
- `make official-daily-full-run` 可运行。
- `make runtime-baseline` 可运行。
- `make source-coverage` 可运行。
- `make evidence-packets` 可运行。
- `make topic-clusters` 可运行。
- `make value-scores` 可运行。
- `make high-value-candidates` 可运行。
- `make phase1-daily` 可运行。
- `make doctor`、`make path-audit`、`make sources-validate`、`make source-health`、`make source-runtime-health`、`make manifest-validate` 继续可运行。
- Phase 1 generated artifacts 不进入 Git。

## Phase 2：内容生产质量链路

### P2-001：Content Brief Builder v1

目标：

- 从 high-value candidates 生成 content brief。
- brief 包含核心事实、为什么重要、证据、反方观点、适合平台、推荐内容类型。
- 不直接生成文章。

### P2-002：Outline Builder v1

目标：

- 从 content brief 生成结构化大纲。
- 支持公众号长文、小红书短内容等不同平台的 outline 形态。
- 不直接写成品稿。

### P2-003：Draft Writer v1

目标：

- 在 evidence 与 outline 约束下生成初稿。
- 明确保留来源证据、未确认信息和禁止幻觉规则。

### P2-004：Fact / Evidence Check v1

目标：

- 对 draft 中的事实、数字、引用和结论做 evidence check。
- 输出可修订问题清单，而不是直接发布。

### P2-005：Platform Packaging v1

目标：

- 将通过检查的内容打包为微信公众号、小红书等平台格式。
- 处理标题、摘要、封面提示、标签和发布前 checklist。
