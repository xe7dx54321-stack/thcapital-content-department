# Top20 Stage-Gate Scorecard | 2026-05-14 | day_mainline
> 生成时间：2026-05-14 17:00 CST | lane: day_mainline | runtime: market-editor (Top20裁判心跳窗)
> 审核对象：`20260514__top20-screening-pack__reworked.md` + `20260514__top20__redteam-review.md`
> 前置状态：pack=final ✅ | redteam=final ✅

---

## 裁判结论

| 字段 | 值 |
|------|------|
| status | rework |
| overall_score | 78/100 |
| decision_reason | P0数据失真×2 + P1叙事缺失×1；8个对象通过，但3个高优先级候选需返工后才能进入topic-planner |
| continuity_decision | continuity_only |
| continuity_output | top20_mini_slate |

---

## 单项评分矩阵

### ✅ premium_pass（8分+，可直接进入topic-planner）

| 排名 | 对象 | 综合分 | redteam结论 | 裁判意见 |
|------|------|--------|------------|---------|
| TOP2 | 字节豆包付费订阅68/200/500元/月 | 90 | ✅ 通过 | 数据硬度P1，传播破圈双满分，定价策略叙事清晰；进入主推进序列 |
| TOP3 | 阶跃星辰170亿人民币融资 | 89 | ✅ 通过 | P1多方核实，币种明确，产业资本+IPO三线叠加；进入主推进序列 |
| TOP4 | Kimi ARR超2亿美元 | 86 | ✅ 通过（隐含） | 商业化数据扎实，36氪首发；进入主推进序列 |
| TOP7 | OpenAI GPT-5.5 + Codex on NVIDIA | 86 | ⚠️ 需合并处理 | P1官方源，但与TOP8/12/15同属NVIDIA企业AI叙事；进入主推进序列，需在topic-planner层面做差异化策划 |
| TOP8 | NVIDIA + SAP企业级AI Agent | 83 | ⚠️ 需合并处理 | 同上；进入主推进序列但需与TOP7/12/15合并或差异化 |
| TOP9 | MiniMax ARR超1.5亿美元 | 81 | ✅ 通过（隐含） | P1财务数据扎实；进入主推进序列 |
| TOP10 | 智谱AI & MiniMax港股上市 | 80 | ✅ 通过（隐含） | 港股话题+财务双驱动；进入主推进序列 |
| TOP14 | OpenAI DeployCo | 76 | ✅ 通过（隐含） | P1官方，B2B平台化叙事；进入主推进序列 |

### ⚠️ borderline（6-7分，可进mini_slate但需条件修复）

| 排名 | 对象 | 综合分 | redteam结论 | 裁判意见 |
|------|------|--------|------------|---------|
| TOP18 | OpenAI B2B前沿企业报告 | 72 | ✅ 通过（隐含） | 72分刚好越线；P1官方报告，内容稳定；进入mini_slate conditional，优先级低于前8 |
| TOP13 | 百度文心大模型5.1 | 74 | ✅ 通过（红队明确） | LMArena1223分唯一性值得放大；进入mini_slate conditional |
| TOP17 | 无屏手环AI激活 | 69 | ✅ 通过（红队明确） | 视觉素材极强，69分略低但内容基本面成立；进入mini_slate conditional |
| TOP11 | NVIDIA Nemotron 3 Nano Omni | 79 | ⚠️ 需合并处理 | 与TOP7/8/12/15同源NVIDIA Blog；进入mini_slate conditional，标注合并需求 |
| TOP12 | NVIDIA + ServiceNow | 77 | ⚠️ 需合并处理 | 同上 |

### ❌ rework（需返回market-scout/topic-planner修复）

| 排名 | 对象 | 综合分 | redteam问题 | 返工责任方 |
|------|------|--------|------------|---------|
| TOP1 | Anthropic 500亿融资/估值6万亿 | 91 | P0致命数据矛盾：500亿美元≠6万亿美元；36氪原始为500亿人民币(~$70亿)；各方信源估值从$900亿到$1.2T不等，pack完全不标币种 | signal-scout + market-scout：必须查36氪原文确认币种，manifest中注明"估值存在多源差异待核实"，两数字分开标注 |
| TOP6 | DeepSeek 73亿美元融资 | 82 | P0量级错误：实际寻求7350 million USD（~$73.5亿≠73亿）；pack少了一个零；遗漏梁文峰跟投20亿人民币、国家大基金三期主导、腾讯阿里谈判等关键事实 | signal-scout + market-scout：更正为73.5亿美元(≈540亿人民币)，补全信源差异说明，补入梁文峰跟投+国家大基金三期背景 |
| TOP19 | xAI团队解散 | 73 | P1灾难性叙事遗漏：实际为xAI解散资产并入SpaceX、22万张GPU的Colossus集群转租给Anthropic、11位创始人全离职、马斯克公开承认"第一次没做好"；pack轻描淡写完全浪费本轮最具传播力事件 | topic-planner：必须重建叙事定调；market-scout：补充Colossus GPU转租、创始团队全部离职、梁文峰跟投等可查证事实 |

---

## P0/P1返工追踪

### TOP1 — Anthropic
- 根因：信源币种未核实即写入，数据前后矛盾
- 修复方向：分开标注融资额(USD)与估值(USD)，注明差异来源
- owner：signal-scout + market-scout
- 修复后目标分：维持91，但需数据硬核实

### TOP6 — DeepSeek
- 根因：数字少了一个零，遗漏关键背景
- 修复方向：更正为73.5亿美元，补全国家大基金三期+梁文峰跟投+腾讯阿里谈判背景
- owner：signal-scout + market-scout
- 修复后目标分：维持82，数据硬度从⚠️P2-P3升级至P1

### TOP19 — xAI
- 根因：叙事轻描淡写，遗漏核心事件骨架
- 修复方向：重建叙事为"xAI解散并入SpaceX，22万卡超算拱手让给Anthropic"；补充创始团队全出走的具体信息
- owner：topic-planner（叙事定调）+ market-scout（事实补全）
- 修复后目标分：预计85+（本轮最佳叙事机会，返工后传播性评分有望冲破90）

---

## top20_mini_slate（可进入continuity lane的候选）

> 本次 pack 共20条；其中8条 premium_pass，5条 borderline conditional，3条 rework，4条因redteam重复源问题建议合并处理

### 主推进序列（premium pass + borderline中最强对象，9条）

| 优先级 | 排名 | 对象 | 综合分 | 进入条件 |
|--------|------|------|--------|---------|
| P0 | TOP2 | 字节豆包付费订阅 | 90 | 无条件通过 |
| P0 | TOP3 | 阶跃星辰170亿人民币融资 | 89 | 无条件通过 |
| P0 | TOP4 | Kimi ARR超2亿美元 | 86 | 无条件通过 |
| P0 | TOP7 | OpenAI GPT-5.5 + Codex on NVIDIA | 86 | 无条件通过，NVIDIA差异化策划 |
| P1 | TOP8 | NVIDIA + SAP | 83 | 通过，需与TOP7/12/15差异化 |
| P1 | TOP9 | MiniMax ARR | 81 | 无条件通过 |
| P1 | TOP10 | 智谱/MiniMax港股 | 80 | 无条件通过 |
| P2 | TOP14 | OpenAI DeployCo | 76 | 通过，优先级低于P1 |
| P2 | TOP13 | 百度文心5.1 | 74 | 通过，"唯一进入LMArena榜单国产模型"叙事放大 |

### continuity lane（rework对象修复后升级）

| 优先级 | 排名 | 对象 | 修复触发条件 | 预计升级后分 |
|--------|------|------|-------------|------------|
| P1 | TOP19 | xAI解散并入SpaceX | topic-planner重建叙事 + market-scout补实可查证事实 | 85+ |
| P1 | TOP1 | Anthropic | signal-scout核实36氪原文币种并重新标注 | 88+ |
| P2 | TOP6 | DeepSeek | signal-scout更正数字并补全背景 | 84+ |

### 建议合并处理的NVIDIA族（4条）

| 排名 | 对象 | 综合分 | 合并建议 |
|------|------|--------|---------|
| TOP7 | OpenAI GPT-5.5 + Codex on NVIDIA | 86 | 建议与TOP8/12/15合并为1篇深度分析《企业AI Agent平台战争》，或明确各条差异化角度 |
| TOP8 | NVIDIA + SAP | 83 | 同上 |
| TOP11 | NVIDIA Nemotron 3 Nano Omni | 79 | 同上 |
| TOP12 | NVIDIA + ServiceNow | 77 | 同上 |

---

## 裁判综合评语

本轮 pack 存在3个P0数据/叙事事故（TOP1/TOP6/TOP19），直接拖累整体评分至78分。但其余对象质量较高，8条 premium pass 中 TOP2(豆包) 和 TOP3(阶跃星辰) 具备强传播力和数据硬度，是今日日间主线的核心推进对象。

TOP19（xAI）虽评分仅73，但redteam指出的叙事缺失才是核心问题——本轮最具戏剧张力的事件被轻描淡写，这是机会损失而非事实错误。修复后预计升至85+，应优先处理。

redteam同时指出TOP7/8/11/12/15五来自NVIDIA Blog同源的问题，提醒 topic-planner 在策划阶段做差异化，避免企业级AI Agent内容同质化。

当前 scorecard 状态：**rework**，整体不满足 pass 条件；但9条主推进序列 + 3条continuity lane修复升级路径清晰，不触发 truth stop。

---

## continuity_decision 裁定依据

- `status=rework`：P0数据/叙事事故3条，必须返工
- `continuity_decision=continuity_only`：pack中有9条达到 pass 标准，3条 rework 对象有明确修复路径，无 truth failure
- `continuity_output=top20_mini_slate`：主推进序列9条 + continuity lane 3条，覆盖全量20条候选的升降级路径
- `premium pass`（8条，continuity_output=none）：TOP2/3/4/7/8/9/10/14，直接进入 topic-planner
- `truthful rework but still recoverable`（TOP1/6/19）：数字/叙事可修正，无事实捏造，进入 continuity lane

---

*本 scorecard 由 market-editor 裁判心跳窗自动生成 | 2026-05-14 17:00 CST*
*如需撤稿重查，请联系 market-editor 发起 rework 流程*
*continuity_output = top20_mini_slate | 主推进序列 = 9条 | continuity lane = 3条*