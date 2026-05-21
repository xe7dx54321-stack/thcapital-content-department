# Top20 Stage-Gate Scorecard — 2026-05-11（day_mainline）
**裁判：** market-editor
**执行时间：** 2026-05-11 16:38 CST
**前置确认：** pack=final ✅（08:53 CST） · redteam=final ✅（14:53 CST）
**Scorecard 刷新依据：** cron heartbeat · 现有 scorecard（15:05 CST）经核验内容完整，今日 pack/redteam 均无新进展，无需推翻原判
**状态：** rework

---

## 一、裁判结论

| 字段 | 值 | 说明 |
|------|----|------|
| `status` | `rework` | Pack 无 P0 truth failure；P1 级问题（赛道偏差 / 引用缺链 / 视觉缺图 / source manifest 缺失）影响多个候选的可信推进 |
| `rework_mode` | `continuity_only` | Top10 主体无事实性错误；P1 问题均有明确修复路径，允许 content-writer 在修正条件内推进 |
| `continuity_decision` | `continuity_only` | 10 个候选经 redteam 回读无 truth failure，可进入 continuity lane |
| `continuity_output` | `top20_mini_slate` | 见第二节 mini_slate 表格 |

---

## 二、top20_mini_slate（可进入 continuity lane 的候选）

> **进入条件：** 修复 P1 问题后可直接派发平台任务单
> **排除标准：** ① P0 truth failure ② 事实严重偏离 ③ 无任何 truthful 推进路径

| # | 公司 | 平台就绪度 | 进入条件（rework_action） | Owner |
|---|------|-----------|--------------------------|-------|
| 1 | **Tessera Labs** | 高 | 无条件通过 | — |
| 2 | **Parallel** | 高 | 无条件通过 | — |
| 3 | **Scout AI** | 高 | 无条件通过 | — |
| 4 | **Featherless.ai** | 高 | 补 GitHub repo + 官网产品截图；source manifest 标注视觉来源 | signal-scout |
| 5 | **Pocket** | 中高 | 必须补 `$27M ARR` 引用链（Sacra Research / YC Demo Day 披露截图）；空引则 content-writer 不得使用 | signal-scout + topic-planner |
| 6 | **RadixArk** | 高 | 无条件通过 | — |
| 7 | **Pit** | 高 | 无条件通过 | — |
| 8 | **AMI Labs** | 中 | 初筛理由必须补注"研究导向 · commercial applications not expected for several years"；不得以当下热点包装 | market-scout + topic-planner |
| 9 | **Moritz** | 中 | 赛道标注修正为"AI legal ops / 律师协作平台"；不得再用"AI-native law firm" | market-scout + topic-planner |
| 10 | **Agentic Fabriq** | 中 | source manifest 补 Okta vs. AI agent 痛点对比说明；补官网/GitHub 截图 | signal-scout + topic-planner |

**Mini-slate 计数：** 10 个候选 · 均无 P0 truth failure · 全部有 truthful 推进路径

---

## 三、P1 返工责任拆解（不得只写"重做 Top20"）

> **裁判口径：** redteam 骂的是候选对象池，不是只骂 market-scout。返工责任必须拆分到 signal-scout / market-scout + topic-planner。

| P1 问题 | 责任方 | 具体返工动作 | 完成标准 |
|--------|--------|--------------|----------|
| Pocket $27M ARR 来源缺链 | signal-scout → 补 Sacra Research / YC Demo Day 披露截图；topic-planner → 任务单引用链标注 | Sacra Research 报告页截图 或 YC Demo Day 披露页面 | 引用链可回查；content-writer 不得空引 |
| AMI Labs 商业化时间线误导 | market-scout → 初筛理由补注"研究导向，商业化数年以后"；topic-planner → 任务单时效预期提示 | 原文写入初筛包 + 任务单备注 | 读者不会预期近期商业化 |
| Moritz 赛道标注偏差 | market-scout → 修正赛道为"AI legal ops / 律师协作平台" | 替换赛道标注文字 | 无"law firm"字样误导 |
| Agentic Fabriq 标签简化 + 视觉缺图 | signal-scout → source manifest 补 Okta 市场教育路径 vs AI agent 实际痛点；补官网/GitHub 截图 | Okta 类比说明写入 manifest + 截图入资产包 | content-writer 有足够上下文写图 |
| Featherless.ai 视觉缺图 | signal-scout → 补 GitHub repo + 官网产品截图 | 同上 | 同上 |
| Source manifest 整体缺失 | market-scout → 补建 source manifest，对应每条信号原始链接 | 格式：`- [公司] → [媒体来源1] / [来源2]` | 可机读；market-editor 可回查每条信号 |

---

## 四、被打出 mini_slate 的候选（含降级原因）

| # | 公司 | 降级原因 | 返工方向 |
|---|------|----------|----------|
| 11 | Marloo | 一手性★★★★★，但赛道信息密度低 + 视觉★☆☆☆☆ | signal-scout 补官网截图 + 客户背书；否则降出 |
| 12 | VOYGR | YC W26 AI maps 新品，包内信息极简，无视觉 | signal-scout 补 demo/官网截图 |
| 13 | Panthalassa | 数据硬度★★★★★，但视觉★☆☆☆☆ + 赛道抽象 | signal-scout 补海上平台实景图 |
| 14 | Terranox AI | YC W26，赛道极窄（铀矿+AI），无合同背书 | signal-scout 补 YC batch 文件 + 矿山/政府合同 |
| 15 | Kanvas Biosciences | 赛道★★★☆☆ + 视觉★★☆☆☆，无明确 AI 差异化 | signal-scout 补官网 + AI biotech 具体场景 |
| 16 | Ineffable Intelligence | $1.1B seed Quartz/SiliconRepublic 非主流 VC 媒体，缺独立验证 + 视觉★☆☆☆☆ | signal-scout 补主流 VC/媒体确认报道 |
| 17 | Maven | YC W26 voice agent payments 新品，赛道信息极简 | signal-scout 补官网 + 产品截图 |
| 18 | Astranis | prior 周期二手摘录，今日包无新信号 | signal-scout 确认是否有今日新进展；沿用旧数据须标注日期 |
| 19 | SageOx | $15M seed 信息贫乏，赛道"AI startup"过于宽泛 | signal-scout 补官网 + 赛道确认；否则降出 |
| 20 | Meatly | 非 AI 核心资产（AgBio/FoodTech），混入 Top20 AI 包逻辑不一致 | topic-planner 降出 Top20，划入"其他"类 |

---

## 五、最终评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 数据硬度 | 8/10 | Top10 有多方独立源；#15–20 信息贫乏或未确认 |
| 一手性 | 8/10 | FinSMEs/YC 官方信号为主；CNBS 升级有据可查 |
| 平台就绪度 | 7/10 | Top10 可推进；#11–20 整体拖后腿 |
| 来源可追溯性 | 6/10 | 缺 source manifest；P1 返工后需重验 |
| **综合得分** | **7.25/10** | |

**裁定：** `status=rework` · `rework_mode=continuity_only` · `continuity_decision=continuity_only` · `continuity_output=top20_mini_slate`

---

## 六、note

- `market_stage_bootstrap.py` 本次不存在，已跳过；前置确认以人工核验替代。
- `market_stage_artifact_status.py` 本次不存在；pack（08:53 CST）/ redteam（14:53 CST）状态经人工读取确认为 final。
- 现有 scorecard（15:05 CST）与当前 cron 执行（16:38 CST）内容一致，今日 pack/redteam 均无新进展，原判维持。
- 红队 P1 返工责任已显式拆分至 `signal-scout / market-scout + topic-planner`，不得以"重做 Top20"笼统处理。

*market-editor 裁判 | 2026-05-11 16:38 CST | heartbeat refresh*
