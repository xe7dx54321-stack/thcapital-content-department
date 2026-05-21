# 市场内容弱链自动补查报告 | 2026-05-16

> 生成时间：2026-05-16 20:27 CST  
> 触发来源：cron:d7eb4d97-ff8d-4c03-a9af-3b10c3bd82ea  
> 执行内容：弱链自动补查（asset query resolution）  
> 执行对象：trend__yc_launches_ai / web__techcrunch_ai / web__finsmes_ai_gnews  

---

## 执行摘要

今日（2026-05-16）共处理 **4 个 asset chain 对象**，均为 2026-05-15 媒体来源派生产物。经弱链补查，结果如下：

| 对象 | 官网/官方账号 | Demo/Docs | 媒体/品牌素材 | 结论 |
|---|---|---|---|---|
| OpenAI ChatGPT Finance | ✅ 已有（chat.openai.com） | ✅ 已有（product内） | ✅ 已有 | **充分链接**，query chain 保留 |
| Osaurus | ✅ 已有 + 新验证 | ⚠️ 无独立 docs/demo | ✅ 官网截图 | **充分链接**，docs/demo缺失但无硬阻断 |
| Rapido | ✅ 已有 | ✅ App Store | ⚠️ 待补充 | **充分链接**，视觉素材可补 |
| Runway | ✅ 已有 | ✅ Gen-4.5 demo | ✅ 官网媒体包 | **充分链接**，GWM-1 tech paper 保留 query |

**结论：4 个对象均已进入"可消费"状态，无 query-only 低置信度硬阻断对象。**

---

## 逐对象补查记录

---

### 1. OpenAI — ChatGPT Finance Launch

**资产ID**: `20260516__openai__chatgpt_finance_launch`  
**信号来源**: web__techcrunch_ai  

**既有硬链（已确认）**:
- 产品页：chat.openai.com — sidebar Finances tab ✅
- Plaid 集成：12,000+ 金融机构 ✅
- 新闻稿：OpenAI 官方 2026-05-15 ✅
- Hiro 收购：OpenAI 收购 Hiro 团队（April 2026）✅

**补查 next_hops**:

| 优先级 | 查询目标 | 结果 | 置信度 | 结论 |
|---|---|---|---|---|
| high | ChatGPT Finance privacy policy Plaid data | TC报道确认Plaid合作；隐私政策未公开 | 中 | 保留 query chain，不硬判 |
| high | Hiro startup OpenAI acquisition details | TC + General Catalyst/Ribbit/Restive 背书 | 高 | Hiro 为真实收购，信号成立 |
| medium | ChatGPT Finance GPT-5.5 benchmark finance | GPT-5.5 model + finance benchmark with experts 已在TC文中 | 高 | 信号可信 |

**最终状态**: ✅ 充分链接，query chain 完整保留，无低置信度硬阻断。

---

### 2. Osaurus — macOS AI Server

**资产ID**: `20260516__osaurus__mac_ai_server`  
**信号来源**: web__techcrunch_ai  

**既有硬链（已确认）**:
- 官网：https://osaurus.ai/ ✅
- GitHub：https://github.com/osaurus-ai/osaurus ✅ （新验证：live，readme 可访问，5.3k stars）
- LinkedIn 创始人：https://www.linkedin.com/in/tdpae/ ✅

**补查 next_hops**:

| 优先级 | 查询目标 | 结果 | 置信度 | 结论 |
|---|---|---|---|---|
| medium | Osaurus AI demo video YouTube | **未找到** | 低 | 无独立 demo video 确认 |
| medium | osaurus.ai documentation site | **不存在**（GitHub readme 即为唯一文档） | — | 无独立 docs site，架构通过 GitHub 理解 |
| low | Osaurus Twitter/X account | **未查到官方账号**（仅有 cofounder 个人账号） | 低 | 无官方社媒账号，但不影响核心信号 |

**资产更新**:
- GitHub 确认 live：Own your AI — Native Swift / MLX / MIT license / 114k downloads / autonomous execution / cryptographic identity
- 官网确认 live：产品截图、产品定位清晰
- 无独立 docs site（GitHub readme 即为主要文档入口）
- 无 demo video
- 无官方 Twitter/X 账号

**最终状态**: ✅ 充分链接（官网 + GitHub 双重确认），无低置信度硬阻断。docs/demo 缺失作为非阻断性备注保留。

---

### 3. Rapido — $240M Series Funding

**资产ID**: `20260516__rapido__240m_series`  
**信号来源**: web__techcrunch_ai  

**既有硬链（已确认）**:
- 官网：https://www.rapido.bike/ ✅
- App Store iOS：https://apps.apple.com/in/app/rapido-auto-bike-share/id1180531014 ✅
- Google Play：✅
- LinkedIn：https://www.linkedin.com/company/rapido/ ✅
- Wikipedia：https://en.wikipedia.org/wiki/Rapido_(company) ✅

**补查 next_hops**:

| 优先级 | 查询目标 | 结果 | 置信度 | 结论 |
|---|---|---|---|---|
| medium | Rapido founder Aravind Sanka LinkedIn | 创始人 Aravind Sanka LinkedIn 存在且可验证 | 高 | 创始人信息可补充至 asset chain |
| medium | Rapido B2B enterprise technology platform 2026 | 无 B2B technology platform 公开信息 | 低 | 保留 query，不硬判 |
| low | Rapido brand assets press kit | 未查到公开 press kit | 低 | 视觉素材补充渠道待挖掘 |

**新增确认**:
- LinkedIn 官方账号：https://www.linkedin.com/company/rapido/ ✅（已在硬链中）
- 创始人 LinkedIn：Aravind Sanka LinkedIn ✅（新发现，可补充）

**最终状态**: ✅ 充分链接，无低置信度硬阻断。融资信号来源（Prosus + TC）可信，资产完整。

---

### 4. Runway — World Models vs Google

**资产ID**: `20260516__runway__world_models_vs_google`  
**信号来源**: web__techcrunch_ai  

**既有硬链（已确认）**:
- 官网：https://runwayml.com/ ✅
- Research Blog：https://runwayml.com/news ✅（新验证：live，有 Runway Agent 推广内容）
- LinkedIn：https://www.linkedin.com/company/runwayml/ ✅
- Twitter/X：https://twitter.com/runwayml ✅
- GitHub：https://github.com/runwayml ✅

**补查 next_hops**:

| 优先级 | 查询目标 | 结果 | 置信度 | 结论 |
|---|---|---|---|---|
| high | Runway GWM-1 technical paper arXiv | **未找到**公开 paper | 中 | 保留 query，GWM-1 来自 TC 报道与官网 blog，信号可信 |
| medium | Runway Gen-4.5 benchmark vs Sora vs Veo | Gen-4.5 demo 已在官网；benchmark 数据未公开 | 中 | 保留 query |
| medium | Runway Characters API pricing | Runway Agent 产品在 app.runwayml.com；定价未公开 | 中 | 保留 query |

**新增确认**:
- Runway Research Blog live，Gen-4.5 demo 可访问 ✅
- Characters API 入口：app.runwayml.com/agent ✅（新发现）
- Runway Agent 50% off Pro 活动确认 ✅

**最终状态**: ✅ 充分链接，无低置信度硬阻断。GWM-1 world model 信号来源（TC + 官网 blog）可信，tech paper 未发布不影响当前信号。

---

## 未解决查询链（保留）

以下查询目标在本次补查中未能命中稳定官网/官方账号，按 runbook 要求**保留 query chain，不硬判结论**：

| 对象 | 查询 | 优先级 | 当前状态 |
|---|---|---|---|
| OpenAI ChatGPT Finance | Privacy policy / Plaid data handling details | high | 保留 |
| Osaurus | Demo video / YouTube | medium | 保留 |
| Rapido | B2B enterprise platform 2026 | medium | 保留 |
| Runway | GWM-1 arXiv technical paper | high | 保留 |
| Runway | Gen-4.5 benchmark vs Sora/Veo | medium | 保留 |
| Runway | Characters API pricing | medium | 保留 |

---

## 补查结论

**今日 4 个 asset chain 对象均已进入"可消费"状态，无 query-only 低置信度硬阻断。**

- OpenAI ChatGPT Finance：官网/产品内 demo / Plaid 合作 / Hiro 收购 — 充分
- Osaurus：官网 + GitHub live 双重验证 — 充分（无 docs/demo 为非阻断性备注）
- Rapido：官网 + App Store + LinkedIn + Wikipedia — 充分
- Runway：官网 + Research Blog + Twitter/GitHub — 充分（GWM-1 paper 保留 query）

**本次补查未发现需要强制降级或拒绝的对象。所有 query chain 均以保留 query 形式维护，不写入低置信度结论，不写入虚拟 VC 运行台。**

---

*market-scout weak-chain resolution | 2026-05-16 20:27 CST | 完成 | 4/4 objects fully linked*