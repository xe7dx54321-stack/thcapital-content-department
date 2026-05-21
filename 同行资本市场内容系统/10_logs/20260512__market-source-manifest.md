# MARKET SOURCE MANIFEST — 2026-05-12
**Runtime:** market-scout | **Generated:** 2026-05-12 11:46（Asia/Shanghai）
**Lane:** product / newco discovery

---

## 信源覆盖状态

| Source ID | 类型 | 状态 | 文件 |
|----------|------|------|------|
| `trend__yc_launches_ai` | YC信源 | ✅ 直采（YC S26未发榜；W26历史库备用） | `20260512__signal__yc_s26_launches.md` |
| `web__techcrunch_ai` | TechCrunch | ✅ 直采（TC + The SaaS News + Mean CEO） | `20260512__signal__techcrunch_ai_funding.md` |
| `web__finsmes_ai_gnews` | FinSMEs | ✅ 直采（FinSMEs周报 + 外部交叉验证） | `20260512__signal__finsmes_ai_may2026.md` |
| `trend__trend_hunt_ai_agents` | Trend Hunt | ✅ 线索补充（仅保留agent产品发现补充） | `20260512__signal__trend_hunt_ai_agents.md` |

---

## 产出清单

| 类型 | 文件 |
|------|------|
| Source Packet ×4 | `02_topic_radar/source_packets/20260512__signal__yc_s26_launches.md` |
| | `02_topic_radar/source_packets/20260512__signal__techcrunch_ai_funding.md` |
| | `02_topic_radar/source_packets/20260512__signal__finsmes_ai_may2026.md` |
| | `02_topic_radar/source_packets/20260512__signal__trend_hunt_ai_agents.md` |
| Top20 初筛包 | `03_topic_candidates/20260512__top20-screening-pack__product-newco.md` |
| Asset Chain | `02_topic_radar/asset_chains/20260512__asset_chain__product_newco_discovery.md` |

---

## 关键数字

- 本轮捕获新公司/产品：20+ 个
- 新增首次出现信号：10+ 个（RadixArk / Pit / Kanvas Biosciences / ReFiBuy / Fifth Dimension / Circle Agent Stack / IBM Concert / Subquadratic / Basata / Performativ）
- 新增融资轮次：30+ 条
- YC S26：未发榜（申请截止2026-05-04；结果2026-06-05）
- 虚拟VC运行台写入：❌ 未写入
---

## CRON执行记录 — 13:12 CST（本次）

**Trigger:** cron:188b7dd0-51af-4df0-bb2f-f6b6df2cd2e8
**执行时间:** 2026-05-12 13:12（Asia/Shanghai）
**执行结果:** ⚠️ 脚本不存在；数据已通过早间运行完成

### 问题：捕获脚本缺失

| 期望脚本 | 实际状态 |
|---------|---------|
| `09_runbooks/scripts/market_topic_capture_round.py` | ❌ 不存在 |
| `09_runbooks/20260325__market-topic-capture-runbook.md` | ❌ 不存在 |

**现有脚本清单（09_runbooks/scripts/）：**
- `market_learning_memo_builder.py`
- `market_learning_pool_board_builder.py`
- `market_wechat_deep_capture_round.py`

### 数据状态

今日（2026-05-12）financing / newco minimal lane 数据已通过早间运行完成：
- Source packets ×4：✅ 已落盘
- Top20 初筛包（product / newco）：✅ 已生成
- Asset chain（product newco discovery）：✅ 已落盘
- Manifest：✅ 已生成（11:46 CST）

### 执行内容

本次 cron 触发后，通过手动 web_search / web_fetch 完成三个 source-id 的增量核查：

**YC S26 状态确认：**
- S26 申请截止：2026-05-04
- S26 结果公布：2026-06-05（预计）
- Demo Day：2026-09-10
- 当前 W26 历史库作为备用锚点

**TechCrunch AI（2026-05-12 增量确认）：**
- Sierra $950M Series B · $15B+ valuation — 确认
- Scout AI $100M Series A — 确认
- Ineffable Intelligence $1B+ seed — 确认（FinSMEs + Gov.uk 交叉）
- RadixArk $100M seed — 新增，Accel+Spark Capital 联合领投

**FinSMEs AI GNews Fallback（2026-05-12 确认）：**
- Kanvas Biosciences $48M Series A — 新增，DCVC+Lions Capital
- Nova Intelligence $31.5M Series A — SAP 官方合作
- Pit $16M seed — 新增，a16z 领投
- ReFiBuy $13.6M Series Seed — agentic commerce 新品类
- Cognition 融资谈判中 — $25B valuation

### 交付确认

| 交付物 | 路径 | 状态 |
|--------|------|------|
| YC信源 | `02_topic_radar/source_packets/20260512__signal__yc_s26_launches.md` | ✅ |
| TechCrunch信源 | `02_topic_radar/source_packets/20260512__signal__techcrunch_ai_funding.md` | ✅ |
| FinSMEs信源 | `02_topic_radar/source_packets/20260512__signal__finsmes_ai_may2026.md` | ✅ |
| Top20初筛包 | `03_topic_candidates/20260512__top20-screening-pack__product-newco.md` | ✅ |
| 资产链 | `02_topic_radar/asset_chains/20260512__asset_chain__product_newco_discovery.md` | ✅ |
| 弱链补查 | `02_topic_radar/asset_chains/20260512__asset_chain__weak_chain_resolution.md` | ✅ |
| 虚拟VC运行台 | `/Users/apple/Documents/虚拟vc项目开发规划/同行资本运行台/` | ❌ 未写入 |

---

## Official Update Lane — 15:38 CST（08:42批次）

**cron:** e11482c7-68d4-407d-bda5-8f9b1f042cca
**执行时间:** 2026-05-12 15:38 CST
**结果:** ✅ 完成

| Source ID | 类型 | 状态 |
|-----------|------|------|
| `web__openai_news` | OpenAI Blog | ✅ 实时验证（9条更新） |
| `web__google_blog_ai` | Google DeepMind | ✅ 已有抓取（23条更新） |
| `web__anthropic_news` | Anthropic News | ✅ 已有抓取（4条更新） |
| `web__deepmind_blog` | DeepMind Blog | ✅ 已有抓取 |
| `web__nvidia_blog` | NVIDIA Blog | ✅ 已有抓取（6条更新） |
| `web__xai_news` | xAI News | ⚠️ Cloudflare 403，P2替代处理 |
| `x__openai` | @OpenAI | P1 交叉 |
| `x__openaidevs` | @OpenAIDevs | P1 交叉 |
| `x__anthropic_ai` | @AnthropicAI | P1 交叉 |

### 本次新增关键信号
- OpenAI Deployment Company $4B+（贝恩/麦肯锡/埃森哲入局）
- Daybreak 安全平台（GPT-5.5三层安全模型栈）
- DALL-E 2/3 API 废弃（今日生效）
- xAI → SpaceXAI 重组（5月6日）
- Grok 下载-60%（深度伪造禁令后遗症）

### 交付物
- `02_topic_radar/source_packets/20260512__source__official-update-lane.md` ✅
- `10_logs/20260512__market-scout-runtime-state__official-update-lane.md` ✅

---

**runtime: market-scout | 隔离: ✅ | 一手性原则: ✅ 遵守**
