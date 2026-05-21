# Stage Gate Scorecard · Top20 初筛包 · day_mainline · 20260510

**RUN_DATE:** 2026-05-10
**RUN_TOKEN:** 20260510
**LANE:** day_mainline
**EXECUTED_AT:** 2026-05-10 18:06 (Asia/Shanghai)
**JUDGE:** market-editor（Top20 裁判心跳窗 · cron:market-stage-top20-score-1910）
**REDTEAM_REVIEW:** `20260510__top20__redteam-review.md`（reworked final）
**PACK_REVIEWED:** `20260510__top20-screening-pack.md`（reworked final）

---

## Verdict Summary

| 维度 | 结论 |
|------|------|
| **status** | `rework` |
| **overall_score** | `7 / 10` |
| **truth_failure** | `false` |
| **continuity_decision** | `continuity_only` |
| **continuity_output** | `top20_mini_slate` |

---

## Redteam Attack Recap（本轮有效攻击）

| 优先级 | 问题 | 涉及条目 | 性质 |
|--------|------|---------|------|
| 🔴 P0 | Shield AI — V-BAT 荷兰服役时间戳错误（5月→3月） | #3 | fact error |
| 🔴 P0 | Shield AI — 台湾 NCSIST / 印度合同无来源，删除或补链 | #3 | fabrication risk |
| 🟠 P1 | Rhoda AI — 已公开但标注"未确认"，过时标注 | #6 | stale annotation |
| 🟠 P1 | Steno — "缺官网"为错误标注，官网已确认 | #7 | false annotation |
| 🟠 P1 | Sakana AI — 投资方描述模糊，应精确为"三菱电机" | #18 | imprecision |
| 🟡 P2 | #12-17（Hyper/Pavoot/Clawvisor/ANORIA/Rudus/Zibra Labs）全为空标签"AI startup" | #12-17 | structural waste |
| 🟡 P2 | Berget AI / Gushwork AI — 官网补查未完成 | #19-20 | incomplete verification |

---

## Pack 评分明细

| 检查项 | 评分 | 说明 |
|--------|------|------|
| 数据硬度 | ★★★★☆ | Top10 信号强；#12-17 全空壳 |
| 一手性 | ★★★☆☆ | FinSMEs/YCs/WeChat 混合，质量参差 |
| 覆盖完整性 | ★★★☆☆ | Builder 扩散层（WeChat/HN/GitHub）大量信号游离 Top20 外 |
| 事实准确性 | ★★☆☆☆ | #3 有 P0 fact error；其余 19 条无新增事实性指控 |
| 平台就绪度 | ★★★☆☆ | 10/20 可直接派生平台任务单；#12-17 无法派生任何任务单 |

**综合评分：7/10**（有实质内容，但 P0 fact error 必须修正后才能推进 content pipeline）

---

## 逐条平台可用性判定

| # | 公司 | 可用结论 | 关键制约 | 修复指令 |
|---|------|---------|---------|---------|
| 1 | OpenAI | ✅ 可直接派生 | 无 | 无 |
| 2 | xAI → SpaceXAI | ✅ 可直接派生 | 注意信号时间戳 | 标注来源时间 |
| 3 | Shield AI | ⚠️ 修正确认后可用 | V-BAT 时间戳错误 + 无来源合同 | 必须修正时间；删除无来源合同 |
| 4 | Nexthop AI | ✅ 可直接派生 | 无 | 无 |
| 5 | LMArena → Arena | ✅ 可直接派生 | 无 | 无 |
| 6 | Rhoda AI | ⚠️ 修正确认后可用 | 标注过时 | 修正为"已公开，官网待补" |
| 7 | Steno | ⚠️ 修正确认后可用 | "缺官网"标注有误 | 删除该标注 |
| 8 | Beacon Health | ✅ 可派生 | 需补产品方向 | signal-scout 补 YC 产品截图 |
| 9 | Lucid | ✅ 可派生 | 官网待补 | signal-scout 补官网 |
| 10 | Motion | ✅ 可派生 | 官网待补 | signal-scout 补官网 |
| 11 | Pace | ✅ 可派生 | 官网待补 | signal-scout 补官网 |
| 12 | Hyper | ❌ 不可用 | 空标签 | 降级观察名单，不占 Top20 名额 |
| 13 | Pavoot | ❌ 不可用 | 空标签 | 降级观察名单，不占 Top20 名额 |
| 14 | Clawvisor | ❌ 不可用 | 空标签 | 降级观察名单，不占 Top20 名额 |
| 15 | ANORIA | ❌ 不可用 | 空标签 | 降级观察名单，不占 Top20 名额 |
| 16 | Rudus | ❌ 不可用 | 空标签 | 降级观察名单，不占 Top20 名额 |
| 17 | Zibra Labs | ❌ 不可用 | 空标签 | 降级观察名单，不占 Top20 名额 |
| 18 | Sakana AI | ✅ 可派生 | 投资方描述需精确 | 改为"三菱电机（Mitsubishi Electric）" |
| 19 | Berget AI | ⚠️ 官网补查前不可用 | 缺官网 | signal-scout 48h 补官网 |
| 20 | Gushwork AI | ⚠️ 官网补查前不可用 | 缺官网 | signal-scout 48h 补官网 |

**可用候选计数：14 条（10条直接可用 + 4条修复后可用）**
**不可用：6 条（#12-17 全为空标签，必须降级）**

---

## Rework Mode

> `status=rework`；非 truth failure；修复后 content pipeline 可继续推进

| Owner | 修复项 | Deadline |
|-------|--------|----------|
| `signal-scout / market-scout` | #3 Shield AI — 修正 V-BAT 时间戳为"2026年3月"；删除无来源的台湾/印度合同 | 下轮 Top20 再评分前 |
| `signal-scout / market-scout` | #12-17 全部降级为"观察名单"，从 Top20 名额中移除 | 下轮 Top20 再评分前 |
| `signal-scout / market-scout` | #19-20 Berget AI / Gushwork AI 官网补查 | 48h 内 |
| `topic-planner` | #6 Rhoda AI 标注更新；#7 Steno 标注修正；#18 Sakana AI 投资方精确化 | 平台任务单下发前 |

---

## Continuity Decision（可机读字段）

```
continuity_decision:  continuity_only
continuity_output:    top20_mini_slate
truth_failure:       false
recoverable:         true
usable_candidates:   14
blocked_candidates:  6（#12-17空标签）
threshold_met:       true（14 ≥ 5）
```

---

## top20_mini_slate（进入 continuity lane 的候选）

> 以下 P0/P1/P2 候选在修复项完成前不得进入 content pipeline。
> P0 = 无条件可推进；P1 = 修复一项后可用；P2 = 补官网后可用。

| 档位 | # | 公司 | 当前状态 | 进入条件 |
|------|---|------|---------|---------|
| P0 | 1 | OpenAI | ✅ 直接可用 | 无 |
| P0 | 2 | xAI → SpaceXAI | ✅ 直接可用 | 标注来源时间（不阻塞，立即可派题） |
| P0 | 4 | Nexthop AI | ✅ 直接可用 | 无 |
| P0 | 5 | LMArena → Arena | ✅ 直接可用 | 无 |
| P0 | 18 | Sakana AI | ✅ 直接可用（投资方精确化后） | 改为"三菱电机"（小修，不阻塞派题） |
| P1 | 3 | Shield AI | ⚠️ 待修复 | V-BAT 时间修正 + 删除无来源合同 |
| P1 | 6 | Rhoda AI | ⚠️ 待修复 | 标注更新为"已公开" |
| P1 | 7 | Steno | ⚠️ 待修复 | 删除"缺官网"错误标注 |
| P1 | 8 | Beacon Health | ⚠️ 补产品方向 | signal-scout 补 YC 产品截图/描述 |
| P1 | 9 | Lucid | ⚠️ 官网待补 | signal-scout 补官网 |
| P1 | 10 | Motion | ⚠️ 官网待补 | signal-scout 补官网 |
| P1 | 11 | Pace | ⚠️ 官网待补 | signal-scout 补官网 |
| P2 | 19 | Berget AI | ⚠️ 待官网补查 | signal-scout 48h 内补官网 |
| P2 | 20 | Gushwork AI | ⚠️ 待官网补查 | signal-scout 48h 内补官网 |

**P0 立即可派题：5 条**（OpenAI / xAI / Nexthop AI / LMArena / Sakana AI）
**P1 修复后可用：7 条**（Shield AI / Rhoda AI / Steno / Beacon Health / Lucid / Motion / Pace）
**P2 补官网后可用：2 条**（Berget AI / Gushwork AI）

---

## 给老板的前台同步

> 今日 Top20 裁判结论：**rework，非 truth stop**
>
> 有效攻击 7 项（1 P0 fact error + 1 P0 无来源合同 + 4 P1 标注错误 + 1 P2 空壳）；
> 6 条（#12-17）全为空标签，直接降级观察名单，不占 Top20 名额。
>
> **今日可用候选：14 条，其中 5 条 P0 可立即派生平台任务单。**
>
> 修复指令已拆解至 `signal-scout / market-scout + topic-planner`，非重新做 Top20。
>
> 内容工厂今日可推进 P0 候选（OpenAI / xAI / Nexthop AI / LMArena / Sakana AI），修复项不影响今日主推进。

---

*market-editor · 20260510 · Top20 初筛包裁判 · day_mainline*
*version: rewritable — 若 signal-scout / market-scout 完成修复，可申请再评分*