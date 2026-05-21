# Asset Chain — 2026-05-13（Product / NewCo Discovery Lane）
**Runtime:** market-scout | **Date:** 2026-05-13 | **Lane:** product + newco discovery
**Input Source:** `20260513__source_packet__product_newco_discovery.md`
**Output:** `20260513__top20_screening_pack__product-newco.md`

---

## Asset Chain 执行记录

### Step 1 — 原始入口抓取（4 sources）

| # | Source ID | 类型 | 抓取结果 |
|---|-----------|------|---------|
| 1 | `trend__yc_launches_ai` | YC launches S26 | 18 AI公司，5高优先级（已融资） |
| 2 | `web__techcrunch_ai` | TC报道 | 6 deals（Sierra/Blitzy/Exaforce/DeepInfra/Corgi/Tessera/Astrocade） |
| 3 | `web__finsmes_ai_gnews` | FinSMEs融资追踪 | 9 deals（Isomorphic/Ineffable/Exaforce/Havoc/Kanvas/Webidoo等） |
| 4 | `trend__trend_hunt_ai_agents` | Trend Hunt agent产品 | 6产品线索，保留1条补充（AgentCore Payments） |

### Step 2 — 关键公司一跳派生

| 公司 | 派生方向 | 候选链接 |
|------|---------|---------|
| **Isomorphic Labs** | 官网 + 融资公告 | ycombinator.com/companies/isomorphic-labs; isomorphic-labs.com |
| **Ineffable Intelligence** | 官网 + 创始人 | ycombinator.com/companies/ineffable-intelligence |
| **Sierra** | 官方产品页 | sierrainteractive.com |
| **Exaforce** | YC页 + 官方 | ycombinator.com/companies/exaforce |
| **Blitzy** | YC页 | ycombinator.com/companies/blitzy-1 |
| **AgentCore Payments** | AWS blog + 技术文档 | aws.amazon.com/blogs/aws/... |

### Step 3 — 结构化初筛（Top20）

| # | 对象 | 来源Lane | 金额信号 | 优先级 |
|---|------|---------|---------|--------|
| 1 | Isomorphic Labs | FinSMEs | $2.1B | 🔵 |
| 2 | Ineffable Intelligence | FinSMEs | $1B+ | 🔵 |
| 3 | Sierra | TC/FM | $950M | 🔵 |
| 4 | Exaforce | YC/TC/FM | $125M | 🔵 |
| 5 | Blitzy | TC/FM | $200M | 🔵 |
| 6 | Corgi Insurance | TC/FM | $160M | 🔵 |
| 7 | DeepInfra | TC/FM | $107M | 🔵 |
| 8 | Havoc AI | FinSMEs | $100M | 🔵 |
| 9 | Kanvas Biosciences | YC/FM | $48M | 🟡 |
| 10 | Tessera Labs | TC/FM | $60M | 🟡 |
| 11 | Astrocade | TC/FM | $56M | 🟡 |
| 12 | Webidoo | FinSMEs | $25M | 🟡 |
| 13 | Knit Health | FinSMEs | $11.6M | 🟢 |
| 14 | AgentCore Payments | Trend Hunt | 产品信号 | 🟡 |
| 15 | Light Anchor | YC | YC早期 | 🟢 |
| 16 | flowscope | YC | YC早期 | 🟢 |
| 17 | ReasonBlocks | YC | YC早期 | 🟢 |
| 18 | Chronicle Labs | YC | YC早期 | 🟢 |
| 19 | Clawvisor | YC | YC早期 | 🟢 |
| 20 | CrewAI | Trend Hunt | 产品信号 | 🟢 |

### Step 4 — 弱链补查计划

| 对象 | 待补项 | 优先级 |
|------|-------|--------|
| Isomorphic Labs | 官网 / 融资公告 | 高 |
| Ineffable Intelligence | 官网 / 创始人David Silver | 高 |
| AgentCore Payments | 技术规格 / 定价页 | 中 |
| Exaforce | 官网 / demo / 技术blog | 中 |

---

## 一跳派生验证记录

| 对象 | 派生类型 | 状态 |
|------|---------|------|
| YC pages（Exaforce/Blitzy/Havoc AI/Kanvas等） | YC官方公司页 | ✅ |
| Sierra官方页 | 官方产品页 | ✅ |
| AgentCore Payments | AWS blog + TC报道 | ✅ |
| Isomorphic Labs | FinSMEs来源确认 | ✅ |

---

## 今日关键发现

1. **AI drug discovery** 成为月度最高融资：Isomorphic $2.1B（Demis Hassabis背景）
2. **Agentic SOC赛道** 快速成形：Exaforce领头，Chronicle Labs + Clawvisor补强
3. **Agent financial infrastructure** 新品类：AgentCore Payments（AWS+Coinbase+Stripe）
4. **YC S26 AI密度极高**：15+ AI公司覆盖 devtool / enterprise / autonomy / 安全

---

## 输出文件

| 文件 | 路径 |
|------|------|
| Source Packet | `02_topic_radar/source_packets/2026-05-13/20260513__source_packet__product_newco_discovery.md` |
| Top20 初筛包 | `03_topic_candidates/20260513__top20-screening-pack__product-newco.md` |
| Asset Chain（本文） | `02_topic_radar/asset_chains/2026-05-13/20260513__asset_chain__product_newco_discovery.md` |
| Source Manifest | `10_logs/20260513__market-source-manifest.md` |