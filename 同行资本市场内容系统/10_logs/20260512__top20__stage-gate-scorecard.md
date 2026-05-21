# Top20 Stage-Gate Scorecard — 20260512（day_mainline）
**market-editor 裁判输出** | **时间：** 2026-05-12 16:05 CST
**车道：** day_mainline | **评分对象：** `20260512__top20-screening-pack.md`（Canonical）
**前置状态：** ✅ pack=final ✅ redteam=final | **bootstrap：** skipped（脚本不存在）

---

## 裁判总评

| 维度 | 结论 |
|------|------|
| 候选池质量 | 高；Top10 有独立 web 搜索交叉验证，可信 |
| P0 事实性错误 | **无**（红队未发现 P0 级事实性失真） |
| P1 精确性问题 | 4项（NVIDIA金额框架/Pit创始人/Kanvas赛道/DeepSeek-V4参数） |
| 可 truthful 推进对象 | ≥14 个（Top20 中 70% 候选满足 ≥6.5 且无非事实障碍） |
| 最终裁定 | **truthful rework but still recoverable** |

**continuity_decision:** `continuity_only`
**continuity_output:** `top20_mini_slate`

---

## 逐条评分

| # | 对象 | 评分 | status | rework_mode | 裁判备注 |
|---|------|------|--------|-------------|----------|
| 1 | Ineffable Intelligence | 7.5 | rework | `completeness` | 信号强；视觉素材红队修正为★★☆☆☆；无产品/无官网截图，需补强视觉素材方可下游使用 |
| 2 | OpenAI Deployment Company | 8.5 | pass | — | Top1 五维满分；$4B+规模+19家合作方+OpenAI控股；premium pass |
| 3 | NVIDIA $30B → OpenAI | 7 | rework | `framing` | 金额框架描述需修正：$30B是Rubin平台量产采购承诺，非全部流向OpenAI；红队P1级；修正后重评 |
| 4 | Sierra | 8.5 | pass | — | Top2 五维满分；$15B+估值+Bret Taylor+Clay Bavor；premium pass |
| 5 | ByteDance UI-TARS | 8.5 | pass | — | 33K⭐+多模态GUI agent+三规格；五维强；premium pass |
| 6 | Karpathy "Agentic Engineering" | 8 | pass | — | Software 3.0核心叙事+广泛共鸣；premium pass |
| 7 | Blitzy | 7.5 | rework | `completeness` | 信号强；$1.4B估值+3000+AI agents；视觉素材★★★☆☆略有空间；补强后达pass |
| 8 | Anthropic $1T 估值探索 + "dreaming" | 7.5 | rework | `completeness` | 信号强；新一轮目标近$1T+品牌差异化叙事；补注"dreaming"session来源后可 pass |
| 9 | Cognition | 7.5 | rework | `completeness` | 融资谈判+$25B估值；coding agent标杆；补官方确认后重评 |
| 10 | Scout AI | 7 | rework | `framing` | 信号有；补"Fury VLA model+$11M DoW合同"精准叙事；原描述"防御AI+自主软件"过于宽泛 |
| 11 | Nova Intelligence | 6.5 | rework | `completeness` | 信号有；$31.5M Series A+SAP官方合作；补创始人/客户详情后可 pass |
| 12 | RadixArk | 7.5 | rework | `completeness` | 信号强；$100M seed+Accel+Spark联合领投；补官网+背书详情后可 pass |
| 13 | Kanvas Biosciences | 5.5 | rework | `track` | 赛道描述有误：是 biotech（微生物组+空间生物学AI用于免疫疗法），非"AI肿瘤治疗平台"；赛道修正确认后重新 intake |
| 14 | GPT-5.5 静默降级 Mini | 8 | pass | — | 事实清楚+广泛投诉+品牌危机叙事；premium pass |
| 15 | Gemma 4 | 7.5 | rework | `completeness` | 模型强；coding能力超越竞品；补Google官方blog来源后可 pass |
| 16 | Pit | 5 | rework | `completeness` | 仅"Vo i+Klarna高管"无法支撑人设叙事；补创始人姓名+背景后方可 downstream 使用；当前无法进入 mini slate |
| 17 | Claude / Anthropic 无广告承诺 | 6.5 | rework | `completeness` | 信号有价值；补Anthropic官方公告链接+Plus功能对比数据后可 pass |
| 18 | LangChain Interrupt 2026 | 6.5 | rework | `framing` | 活动明日揭幕（5/13）；内容工厂角度须调整为"预热前瞻"而非"活动报道" |
| 19 | Circle Agent Stack | 5.5 | rework | `completeness` | "官方发布"来源不明确；需确认是CircleCI新产品线还是上市公司Circle新产品；来源确认前不可 downstream |
| 20 | DeepSeek-V4 | 6 | rework | `verification` | "1.6T MoE，激活49B/token"参数未获官方确认；DeepSeek官方发布的是V4系列非独立"V4"；需官方blog或HF确认后重评 |

---

## 返工责任拆解（redteam 指出的非 P0 问题，非 fact failure）

| 责任人 | 负责对象 | 返工内容 |
|--------|---------|----------|
| `signal-scout / market-scout` | #3 NVIDIA/#10 Scout AI/#18 LangChain | 金额框架修正确认、VLA model + DoW合同溯源、活动时效角度标注 |
| `topic-planner` | #16 Pit/#1 Ineffable/#19 Circle Agent Stack | 补创始人背景、视觉素材规格确认、产品来源追溯 |
| `topic-planner` | #13 Kanvas Biosciences | 赛道修正为 biotech（微生物组+空间生物学AI）+ 重新 intake |
| `topic-planner` | #20 DeepSeek-V4 | 官方发布页参数确认（DeepSeek blog / HuggingFace） |

---

## top20_mini_slate

以下对象已达到 truthful 推进标准，可进入 day_mainline 主推进序列：

| 优先级 | # | 对象 | 评分 | 进入条件 |
|--------|---|------|------|----------|
| P0 | 2 | OpenAI Deployment Company | 8.5 | 无条件，直接下游 |
| P0 | 4 | Sierra | 8.5 | 无条件，直接下游 |
| P0 | 5 | ByteDance UI-TARS | 8.5 | 无条件，直接下游 |
| P0 | 6 | Karpathy "Agentic Engineering" | 8 | 无条件，直接下游 |
| P0 | 14 | GPT-5.5 静默降级 Mini | 8 | 无条件，直接下游 |
| P1 | 1 | Ineffable Intelligence | 7.5 | 视觉素材规格降维确认（★★☆☆☆）+官网/产品截图补强后升入 P0 |
| P1 | 7 | Blitzy | 7.5 | 补 $1.4B 估值来源 + 已落地 Global 2000 具体客户名称 |
| P1 | 8 | Anthropic $1T 估值 + "dreaming" | 7.5 | 补"dreaming" session 官方来源公告链接 |
| P1 | 12 | RadixArk | 7.5 | 补官网（radixark.com）+ Accel/Spark 联合领投详情页 |
| P2 | 9 | Cognition | 7.5 | cognition.dev 官网确认 + $25B 融资落地验证 |
| P2 | 15 | Gemma 4 | 7.5 | 补 Google DeepMind 官方 blog 来源页 |
| P2 | 3 | NVIDIA $30B → OpenAI | 7 | 修正金额框架描述（Rubin平台量产承诺非全局）+ 补 $400B+ 全局承诺说明 |
| P2 | 10 | Scout AI | 7 | 补"Fury VLA model + $11M DoW合同"精准叙事角度 |
| P2 | 11 | Nova Intelligence | 6.5 | 补创始人姓名 + Festo/KION 具体落地案例 |
| P2 | 17 | Claude / Anthropic 无广告承诺 | 6.5 | 补 Anthropic 官方公告 + Plus 功能对比数据 |
| P2 | 18 | LangChain Interrupt 2026 | 6.5 | 加注"预热前瞻"角度标注，时效逻辑修正 |
| P2 | 20 | DeepSeek-V4 | 6 | 官方发布页确认参数（DeepSeek blog / HuggingFace release note） |

**以下对象暂不进入 mini slate，需修复后重新 intake：**
- #13 Kanvas Biosciences（赛道修正未完成）
- #16 Pit（创始人背景缺失）
- #19 Circle Agent Stack（产品来源未确认）

---

## 裁判结论

- `status`: **rework**
- `rework_trigger`: truthful but not yet downstream-ready；非 fact failure，是 completeness/framing/verification/track 问题
- `continuity_decision`: **continuity_only**（有 ≥14 个可 truthful 推进对象，5 个已达 premium 标准）
- `continuity_output`: **top20_mini_slate**（17 个对象进入 conditional 主推进序列）

---

*market-editor | 2026-05-12 16:05 CST | day_mainline Top20 stage-gate*