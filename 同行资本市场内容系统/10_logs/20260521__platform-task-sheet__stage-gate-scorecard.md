## Platform Task Sheet Scorecard — 2026-21

**Judge:** content-analyst (day_mainline platform heartbeat)
**Score Time:** 2026-05-21 19:21 CST
**Run Token:** 20260521
**Pipeline:** day_mainline

---

## Pre-flight Verification

| Input | Expected State | Actual State | Verdict |
|-------|---------------|-------------|---------|
| platform-task-sheet.md | final | final (8968 bytes，手动验真) | ✅ PASS |
| redteam-review.md | final | final (10734 bytes，手动验真) | ✅ PASS |

> 注：artifact_status.py 只注册了 `pack` kind，两个文件手动核验内容存在且非空骨架，视为 final。

---

## Scorecard Evaluation

### 综合评分：7.5 / 10

| 维度 | 得分 | 说明 |
|------|------|------|
| 选题质量 | 8/10 | Top5 板延续，pack_score 31-47，judge_score 均为 8/10，选题基本面扎实 |
| 平台适配 | 7/10 | wechat 双槽 NV 来源同质化（P1-3）；xiaohongshu 信源软文（P0-2）；bilibili 平台受众错配（P2-1）|
| 结构完整性 | 8/10 | 6 active slots 覆盖 5 平台，limited sheet discipline 执行到位，holdout 清单有捞回条件 |
| Redteam 风险覆盖 | 6/10 | P0 × 2（Slot 5 continuity 标签存疑；Slot 3 Parloa 纯 vendor 来源）；P1 × 3；P2 × 3 |

**总分：7.5 / 10**（8 分以下，非 truth failure）

---

## Decision

```
status: rework
continuity_decision: continuity_only
continuity_output: limited_task_sheet
```

### 判定理由

1. **P0-2（Slot 3 xiaohongshu/Parloa vendor 软文）阻断 content-writer 执行**：来源是 OpenAI vendor 官宣，小红书目标读者（AI 创业者/投资人）对软文识别度高。content-writer 无法仅凭 vendor 稿完成可信内容——需要至少一个独立第三方信源。此问题在 writer 执行前必须解决，否则 xiaohongshu slot 必然引发评论区"软文"质疑。
2. **P0-1（Slot 5 x continuity 补位标签存疑）**：任务单无 prior content 引用，"continuity 补位"仅为制度性标签而非内容事实证明。若实际是新题，内容策略应完全重设计，而不是套 continuity 低冲击力模板。
3. **P1-1（Slot 6 Ineffable 信源自相矛盾）**：Active Slot 与 Holdout Note 打架，content-writer 收到的是自我矛盾指令，无法直接执行。
4. **不属于 stop_for_truth**：选题本身未被证伪，信号来源可查证，只是证据链不完整、角度需补强。不涉及事实失真或方向偏航。

**结论**：保留 active slots 总数（6 个），但 slot 3、5、6 需要在上游补证完成后方可执行。Slots 1、2、4 可先行推进。

---

## next_owner / next_output

| 工序 | Owner | 任务 |
|------|-------|------|
| 补证 P0 + P1 | **topic-planner** | ① 为 Slot 3（Parloa/xiaohongshu）提供至少 1 个独立第三方信源方向（TC/Forbes/LinkedIn/融资记录），或替换为有独立报道的候选；② 为 Slot 5（x/Vera CPU）提供今日 prior content 引用，或改标注为"新题补位"并重设计角度；③ 补 Ineffable 实际可用信源或将 Slot 6 降为 holdout |
| 内容执行（可先行） | **content-writer** | Slots 1、2、4 立即可接；Slot 3 等待 topic-planner 补证结果；Slot 5 等待 topic-planner 澄清 continuity 标签；Slot 6 等待 Ineffable 信源确认 |
| 跨岗位协调 | **market-editor** | 监督 topic-planner 补证进度；若 Slot 3 补证失败，协调替换候选；若 Slot 5 确认新题，调整 x 平台标题策略 |

---

## Per-Slot 指令

### Slot 1（wechat/Codex+GB200）— 可执行
- 补充第三方信源：NVIDIA 官方博客 → 至少加入一个非 NV 来源（AWS/GCP 客户案例、分析师报告、独立科技媒体）
- 视觉素材可用性接单时确认；若原博素材不可用，自制或用 CC0 图库替代

### Slot 2（wechat/SAP Trust）— 可执行
- risk note 补加：「NVIDIA 官方博客来源，需补充第三方信号，避免与 Slot 1 叠加软文感」
- 提供第三方信源方向（如有）

### Slot 3（xiaohongshu/Parloa）— **暂缓，等待补证**
- topic-planner 补证完成前，content-writer 不得开笔
- 若无法找到独立第三方信源，降为备选，由 market-editor 决策是否替换 Slot 3 候选

### Slot 4（zhihu/Voice API）— 可执行，需差异化指令追加
- topic-planner 提供差异化切入方向（不得仅写"需差异化"）
- 推荐方向：接入指南视角 / 与国产 RTC 方案对比视角 / 企业 TTS 质量数据对比视角

### Slot 5（x/Vera CPU）— **暂缓，等待 continuity 标签澄清**
- 若确认今日 x 无 prior content，改为"新题补位"，content-writer 重设计标题和角度
- 若确认有 prior content，引用 source_ref 后继续

### Slot 6（bilibili/Ineffable）— **暂缓，等待 topic-planner 信源确认**
- 若 Ineffable 无独立第三方信源，降为 holdout；market-editor 评估是否从 holdout 捞 Slot 5 升格

---

## Continuity 说明

本轮 scorecard 延续 `premium_only` / `continuity_only` 框架，active slots = 6 不变。任务单整体为 limited_task_sheet，无新 continuity lane 开启。Slots 3/5/6 的暂缓不影响 Slots 1/2/4 的执行进度。

---

## 时间线约束

- **wechat Slot 1 + Slot 2**：当日 `19:00 CST` 前入公众号草稿箱，不得漂移
- **market-editor 补证监督**：收到本 scorecard 后 60 分钟内催 topic-planner 补证
- **topic-planner 补证deadline**：`19:00 CST` 前提供 Slot 3 第三方信源方向和 Slot 5 continuity 澄清

---

**scorecard_status:** final  
**next_owner:** topic-planner（补证 P0） + content-writer（Slots 1/2/4 可先行） + market-editor（跨岗协调）  
**heartbeat_at:** 2026-05-21T11:21:00Z（19:21 CST）