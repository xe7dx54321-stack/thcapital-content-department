# 日间主线 Top 8 → Top 5 建议板 | 2026-05-14 | day_mainline

> 生成时间：2026-05-14 19:59 CST | lane: day_mainline | runtime: market-editor (Top5心跳窗)
> 数据源：10_logs/20260514__top20__stage-gate-scorecard.md (final ✅)
> 关联Top20包：03_topic_candidates/20260514__top20-screening-pack__reworked.md
> 关联红队报告：10_logs/20260514__top20__redteam-review.md

---

## 裁判结论

| 字段 | 值 |
|------|------|
| scorecard_status | rework |
| continuity_decision | continuity_only |
| continuity_output | top20_mini_slate |
| top5_decision | premium_only（来自scorecard主推进序列） |
| top5_count | 5 |
| holdout_count | 3 |
| no_op_reason | N/A — 有9条主推进序列可供推进 |

---

## Top 5 正式建议（按综合分倒序）

### 🥇 TOP 1 — 字节豆包付费订阅（68/200/500元/月）

| 字段 | 值 |
|------|------|
| 综合分 | **90/100** |
| 热度信号 | 付费订阅三档定价，B端C端双线破圈能力极强 |
| 证据信号 | P1数据来源，36氪首发，数据硬度P1 |
| 传播潜力 | 破圈满分，定价策略叙事清晰 |
| 平台适配 | wechat/x/xiaohongshu/bilibili/toutiao 全平台适配 |
| 信源 | 36氪原始报道 → 见 pack TOP2 |
| 下一工序 | topic-planner（立即启动） |

> **裁判意见：** 本轮数据最硬、传播力最强对象。无条件进入主推进序列。topic-planner 应优先处理。

---

### 🥈 TOP 2 — 阶跃星辰完成170亿人民币融资

| 字段 | 值 |
|------|------|
| 综合分 | **89/100** |
| 热度信号 | 170亿人民币大额融资，产业资本+IPO三线叠加 |
| 证据信号 | P1多方核实，币种明确 |
| 传播潜力 | 产业资本背书+IPO预期双驱动 |
| 平台适配 | wechat/x/xiaohongshu/bilibili/toutiao |
| 信源 | market-scout source packet → 见 pack TOP3 |
| 下一工序 | topic-planner（立即启动） |

> **裁判意见：** 融资规模大、背景清晰，进入主推进序列无争议。

---

### 🥉 TOP 3 — Kimi（AI）ARR超2亿美元

| 字段 | 值 |
|------|------|
| 综合分 | **86/100** |
| 热度信号 | ARR超2亿美元，商业化里程碑明确 |
| 证据信号 | 36氪首发，商业化数据扎实 |
| 传播潜力 | 数字具象，投资人/创业者双圈关注 |
| 平台适配 | wechat/x/xiaohongshu/bilibili |
| 信源 | 36氪 → 见 pack TOP4 |
| 下一工序 | topic-planner（立即启动） |

> **裁判意见：** 数字型叙事，易加工，建议与豆包、阶跃做差异化角度策划。

---

### TOP 4 — OpenAI GPT-5.5 + Codex on NVIDIA

| 字段 | 值 |
|------|------|
| 综合分 | **86/100** |
| 热度信号 | OpenAI官方发布，P1企业级AI叙事 |
| 证据信号 | P1官方源 |
| 传播潜力 | B2B平台化叙事，企业AI认知门槛高但受众精准 |
| 平台适配 | wechat/x/xiaohongshu/toutiao |
| 信源 | OpenAI官方/NVIDIA Blog → 见 pack TOP7 |
| 下一工序 | topic-planner（需与TOP8/12/15做差异化策划） |

> **裁判意见：** 与TOP8/11/12/15同源NVIDIA Blog，redteam建议在topic-planner层面做差异化。需明确本条核心角度是"OpenAI×NVIDIA"而非泛企业AI。

---

### TOP 5 — 智谱AI & MiniMax 港股上市

| 字段 | 值 |
|------|------|
| 综合分 | **80/100** |
| 热度信号 | 港股上市+财务数据双驱动，国内AI估值重估叙事 |
| 证据信号 | P1财务数据，港股话题叠加 |
| 传播潜力 | 兼具财务严肃性与市场话题性 |
| 平台适配 | wechat/x/toutiao |
| 信源 | market-scout source packet → 见 pack TOP10 |
| 下一工序 | topic-planner（立即启动） |

> **裁判意见：** 港股上市时间线若能确认具体季度，叙事张力更强，建议topic-planner补充。

---

## Holdout 3（次级备选，等Top5消化后跟进）

| 排名 | 对象 | 综合分 | 热度信号 | 证据信号 | 进入条件 |
|------|------|--------|---------|---------|---------|
| H1 | OpenAI DeployCo | 76 | B2B平台化叙事，P1官方 | 官方发布 | 前5条中有任意一条热度不及预期时优先顶上 |
| H2 | MiniMax ARR超1.5亿美元 | 81 | 财务里程碑，AI商业化 | P1财务数据 | 与TOP5（智谱/MiniMax港股）做角度区分后使用 |
| H3 | 百度文心大模型5.1 | 74 | LMArena1223分唯一国产模型 | 红队明确通过 | "唯一进入LMArena榜单国产模型"角度优先 |

> **裁判意见：** H2与TOP5存在MiniMax同源风险，topic-planner需差异化处理。H3叙事角度鲜明（"唯一国产"），适合单独成篇。

---

## ⚠️ NVIDIA 族合并风险提示

> scorecard 指出 TOP7/8/11/12/15 同源 NVIDIA Blog，存在内容同质化风险。当前 TOP5 板仅纳入 TOP7（OpenAI GPT-5.5 + Codex on NVIDIA）一条，TOP8 暂未入板。

| 同源族 | 排名 | 综合分 | 当前状态 |
|--------|------|--------|---------|
| NVIDIA企业AI族 | TOP7 | 86 | ✅ Top5 第一梯队 |
| NVIDIA企业AI族 | TOP8 | 83 | ❌ 未入板（归入HOLD） |
| NVIDIA企业AI族 | TOP11 | 79 | ❌ 未入板 |
| NVIDIA企业AI族 | TOP12 | 77 | ❌ 未入板 |

**建议：** topic-planner 收到本板后，先确认TOP7的角度定位；若确认以"OpenAI×NVIDIA"为核心角度，TOP8/11/12 内容可作为背景资料引用，避免独立成篇造成同质化。

---

## Continuity Lane 对象（不在本轮推进范围，等待 rework）

> 以下对象仍处于 rework 状态，market-scout/topic-planner 正在修复中，修复完成后另开窗口推进。

| 排名 | 对象 | scorecard评分 | 返工原因 | 预计升级分 | 预计进入 |
|------|------|-------------|---------|-----------|---------|
| TOP19 | xAI解散并入SpaceX | 73 | P1叙事缺失，Colossus GPU转租、创始团队全出走的核心事实被淹没 | 85+ | 下一窗口Top5 |
| TOP1 | Anthropic 500亿估值 | 91 | P0数据矛盾：500亿美元≠6万亿美元，币种未核实 | 88+ | 下一窗口Top5 |
| TOP6 | DeepSeek 73亿美元融资 | 82 | P0量级错误：应为73.5亿美元，遗漏梁文峰跟投/国家大基金三期 | 84+ | 下一窗口Top5 |

> TOP19（xAI）是本轮最具传播张力的事件，返工后预计评分85+，应优先处理。

---

## artifact_status 自检

```
artifact: 20260514__daily-top8-to-top5.md
kind: top5_board
stage: day_mainline
run_token: 20260514
status: pre_final_review
top5_entries: 5 (TOP2/TOP3/TOP4/TOP7/TOP10)
holdout_entries: 3 (H1/H2/H3)
heat_signal_present: ✅ 每条含 heat_signal + evidence_signal
link_or_packet_path: ✅ 每条含信源指向
supply_gap_note: N/A — 强候选充足（9条主推进序列）
continuity_lane_separated: ✅ TOP1/6/19 归入 continuity lane，不在本板推进
nvidia_dedup_risk_flagged: ✅ 已标注 TOP7/8/11/12 同源风险
self_check: PASS (preliminary)
```

---

*本 board 由 market-editor Top5心跳窗生成 | 2026-05-14 19:59 CST*
*前置 scorecard：10_logs/20260514__top20__stage-gate-scorecard.md ✅ final*
*下一工序：topic-planner 接收本板并启动策划*