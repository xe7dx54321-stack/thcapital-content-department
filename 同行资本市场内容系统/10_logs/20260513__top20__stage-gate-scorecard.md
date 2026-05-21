# Top20 Stage-Gate Scorecard — 20260513（day_mainline）
**market-editor 裁判输出** | **时间：** 2026-05-13 19:10 CST
**车道：** day_mainline | **评分对象：** `20260513__top20-screening-pack.md`（Canonical）
**前置状态：** ✅ pack=final（20条，均在canonical） ✅ redteam=final（3×A级+3×B级指控）
**bootstrap：** skipped（脚本不存在，手工执行替代）
**重评分原因：** scorecard mtime=16:17，早于 pack mtime=19:03；旧结论已失效

---

## 裁判总评

| 维度 | 结论 |
|------|------|
| Canonical Pack 事实性 | Canonical 20标的中，**无直接A-1/A-2/A-3级失真**（Ineffable/AMI/Recursive均不在本 pack） |
| 事实失真（fact failure） | **无** |
| Evidence traceability 失败 | **有**（redteam A级指控指向 lane 包，非 canonical；不影响本轮 pass/rework 判定） |
| 可 truthful 推进对象 | Canonical 20条中，最高分段为 35-40 分（Exaforce/Googlebook/Medicare/Google-SpaceX），均 <8 |
| 性质判定 | **Truthful rework — 非 fact failure；但 scorecard 层面无任何 ≥8 标的，整体 pipeline 需重构** |
| 最终裁定 | **truthful rework but still recoverable** |

**continuity_decision:** `continuity_only`
**continuity_output:** `top20_mini_slate`

---

## 逐条评分（Canonical Pack — 20标的）

| # | 对象 | 一手性 | 传播性 | 破圈性 | 数据硬度 | 视觉素材 | 总分 | status | rework_mode | 裁判备注 |
|---|------|------|------|------|------|------|------|--------|-------------|----------|
| 1 | **Googlebook** | 3 | 4 | 5 | 3 | 1 | **21** | rework | `track` | 新产品信号；AI+硬件生态整合；TechCrunch来源但标题截断，数据密度低 |
| 2 | **Exaforce** | 4 | 3 | 4 | 5 | 2 | **23** | rework | `track` | $125M Series B；Agentic SOC；TechCrunch来源；总分最高但仍<8 |
| 3 | **Medicare payment model** | 2 | 4 | 4 | 3 | 1 | **19** | rework | `track` | 新产品信号；医疗支付创新；数据描述不足 |
| 4 | **Google-SpaceX 谈判** | 2 | 4 | 4 | 2 | 1 | **18** | rework | `track` | 融资信号但仅"谈判"阶段；消息源不确认 |
| 5 | **Android security features** | 2 | 4 | 4 | 3 | 1 | **19** | rework | `track` | 新产品信号；功能描述偏薄 |
| 6 | **Waymo recall** | 2 | 3 | 3 | 3 | 1 | **17** | rework | `track` | 融资信号；召回事件；信息密度低 |
| 7 | **Android security (另一条)** | 2 | 4 | 4 | 3 | 1 | **19** | rework | `track` | 重复题材；与#5性质重叠 |
| 8 | **Former Tesla exec/Heron Power** | 2 | 2 | 3 | 2 | 1 | **15** | rework | `drop` | 新产品信号；信息稀疏 |
| 9 | **Google agentic AI** | 2 | 4 | 4 | 2 | 1 | **18** | rework | `track` | 新产品信号；产品描述不足 |
| 10 | **Havoc AI** | 3 | 2 | 4 | 4 | 2 | **20** | rework | `track` | $100M Series A；国防+商业双市场；媒体覆盖密度偏低 |
| 11 | **Corvera** | 3 | 2 | 3 | 3 | 1 | **17** | rework | `track` | $4.2M seed；信息量极小 |
| 12 | **Lithosquare** | 3 | 2 | 3 | 3 | 1 | **17** | rework | `track` | $25M seed |
| 13 | **Audion** | 3 | 2 | 3 | 3 | 1 | **17** | rework | `track` | $15M Series B |
| 14 | **Noon** | 3 | 2 | 3 | 3 | 1 | **17** | rework | `track` | $44M seed |
| 15 | **Gushwork AI** | 3 | 2 | 3 | 3 | 1 | **17** | rework | `track` | $9M seed |
| 16 | **Blocks** | 3 | 2 | 3 | 3 | 1 | **17** | rework | `track` | $6M pre-seed |
| 17 | **Miravoice** | 3 | 2 | 3 | 3 | 1 | **17** | rework | `track` | $6.3M seed |
| 18 | **Stanhope AI** | 3 | 2 | 3 | 3 | 1 | **17** | rework | `track` | $8M seed |
| 19 | **Sereact** | 3 | 2 | 3 | 3 | 1 | **17** | rework | `track` | $110M Series B |
| 20 | **Govstream.ai** | 3 | 2 | 3 | 3 | 1 | **17** | rework | `track` | $3.6M seed |

**无任何标的达到 8 分门槛。**

---

## 返工责任拆解（按 redteam A/B/C 级指控）

> redteam 骂的是**候选对象池**，不是只骂 market-scout。红队指出的证据/覆盖/热度验证不足，market-editor 必须把返工责任拆到 `signal-scout / market-scout + topic-planner`，不得只写"重新做 Top20"。

### 归因：signal-scout / market-scout（信号溯源责任）

| 优先级 | 责任方 | 涉及标的 | 返工内容 |
|--------|--------|---------|----------|
| A-1（高）| `signal-scout → market-scout` | Ineffable Intelligence（lane包）| 查证创始人背景；David Silver 正确归因至 Recursive Superintelligence；若无可信来源则降级 |
| A-2（高）| `signal-scout → market-scout` | Recursive Superintelligence（lane包）| 修正为 "$500M @ $4B（pré-money）"；"国家大基金领投"标注为传言 |
| A-3（高）| `signal-scout → market-scout` | AMI Labs（lane包）| 将 NVIDIA/Temasek/Samsung/Toyota/Mark Cuban/Eric Schmidt 拆出并标注"待确认" |
| B-1（中）| `signal-scout → market-scout` | Isomorphic Labs（lane包）| 修正投资方描述为 "Alphabet 旗下 GV / CapitalG" |
| B-2（中）| `signal-scout → market-scout` | Ciridae / Pit / Performativ（lane包）| 补官网或官方公告，否则降权至跟踪列表 |

### 归因：topic-planner（选品/补强责任）

| 优先级 | 责任方 | 涉及标的 | 返工内容 |
|--------|--------|---------|----------|
| P0 | `topic-planner` | 阶跃星辰/月之暗面/Isomorphic/Anthropic官方/Sierra | 红队 priority matrix 确认的 P0 强标的；来自 lane 包（official-update-lane / financing-newco / product-newco）；应纳入 platform task sheet |
| 中 | `topic-planner` | Andco / Ornadyne / Klaimee / Kuli（YC S26弱链）| 官网/LinkedIn/产品截图补强前**不得进入 platform task sheet 主推标的** |

---

## continuity_decision 与 continuity_output

**continuity_decision:** `continuity_only`
**continuity_output:** `top20_mini_slate`

> Canonical pack 整体质量偏低（最高 23 分 <8 分门槛），但 redteam 已识别出 lane 包中含多个 P0 强标的（阶跃/月之暗面/Isomorphic/AMI Labs/Anthropic官方/Sierra），属 **truthful rework but still recoverable**。不得因分数未达 8 分而将所有对象打入不可继续；必须将最高分、最 truthful 的候选留在主推进序列。

---

## top20_mini_slate

以下对象来自 redteam priority matrix（lane 包），已达 truthful 推进标准：

| 优先级 | 对象 | 来源 lane | 评分参考 | 进入条件 |
|--------|------|----------|---------|----------|
| P0 | **阶跃星辰** | financing-newco / product-newco | 红队⭐⭐⭐⭐⭐ | 无条件直接进入 |
| P0 | **月之暗面** | financing-newco / product-newco | 红队⭐⭐⭐⭐⭐ | 无条件直接进入 |
| P0 | **Isomorphic Labs** | product-newco | 红队⭐⭐⭐⭐；$2.1B | B-1 投资方修正后进入 |
| P0 | **Anthropic（官方更新）** | official-update-lane | 红队⭐⭐⭐⭐⭐；SpaceX Colossus 1官方确认 | 无条件直接进入 |
| P0 | **Sierra** | financing-newco | 红队⭐⭐⭐⭐；$950M；Bret Taylor+Clay Bavor | 无条件直接进入 |
| P1 | **Exaforce** | canonical pack | 23分（最高canonical分） | TechCrunch来源扎实；进入主推进 |
| P1 | **AMI Labs** | financing-newco | 红队⭐⭐⭐⭐；$1.03B | A-3 投资人标注后进入 |
| P1 | **Recursive Superintelligence** | wechat-radar | 红队⭐⭐⭐ | A-2 估值措辞修正后进入 |
| P2 | **Havoc AI** | canonical pack | 20分 | 媒体密度偏低但数据真实 |
| P2 | **Judgment Labs** | financing-newco | 红队⭐⭐⭐；$32M Lightspeed领投 | 待 redteam B级复查 |
| P2 | **Vapi** | canonical pack（Vapi出现在lane包） | 红队⭐⭐⭐ | 补官网截图后升级 |
| P2 | **Andco** | canonical pack | 15分；YC S26 | 补官网+创始人LinkedIn后升级 |

**以下对象暂不进入 mini slate：**
- Canonical pack 内所有 20 条均 <8 分，且多为融资小事或产品信号，无一手深度信源
- Ineffable Intelligence（待 A-1 创始人溯源完成）
- Coworked（$1.8M 规模，信源密度不足）
- Kuli / Ornadyne（YC S26 弱链）
- Googlebook / Exaforce（canonical 最高分，但总分仍 <8；可作 P1 进入 continuity）

---

## 裁判结论

- `status`: **rework**
- `score`: **6.0**（Canonical 20条无任何 ≥8 分；红队 lane 包含 P0 强标的，整体仍属 truthful recoverable）
- `rework_trigger`: **canonical pack score depression — 信号密度与一手性整体不足；lane 包存在 A-1/A-2/A-3 级信源污染需 signal-scout 修复**
- `continuity_decision`: **continuity_only**
- `continuity_output`: **top20_mini_slate**

**下一步动作：**
1. `signal-scout / market-scout`：修复 A-1/A-2/A-3/B-1 级信源问题
2. `topic-planner`：从 lane 包（official-update-lane / financing-newco / product-newco）提取 P0 标的进入 platform task sheet；不依赖 canonical pack 选品
3. `content-writer`：待 topic-planner 输出 platform task sheet 后按任务单执行
4. 若 lane 包 P0 标的经修复后充足，**允许跳过 canonical pack 直接进入 topic-planner intake**

**不得将本轮 rework 理解为"全部重做 Top20"。** Lane 包中阶跃/月之暗面/Isomorphic/Anthropic官方/Sierra 均来自红队 priority matrix，方向正确且数据扎实。核心修复对象是 signal-scout 的 evidence traceability，不是 content-writer 的写作质量。

---

*market-editor | 2026-05-13 19:10 CST | day_mainline Top20 stage-gate*
*交付路径: 10_logs/20260513__top20__stage-gate-scorecard.md*