# 弱链自动补查报告 — 2026-05-19

**Runtime:** market-scout | **Date:** 2026-05-19 08:53 CST
**Sources:** trend__yc_launches_ai + web__techcrunch_ai + web__finsmes_ai_gnews
**Trigger:** cron/d7eb4d97-ff8d-4c03-a9af-3b10c3bd82ea — 市场内容弱链自动补查
**Note:** market_asset_query_resolution_round.py 不存在；本轮直接执行 web 搜索补查逻辑

---

## 执行摘要

本轮针对 2026-05-13 来源包中标记为「弱链 / 待补」对象执行 web 搜索补查。

**硬链接补获率：8/8（100%）** ✅
**维持弱链（无法稳定命中）：0/8** ✅

---

## 补查结果详情

### ✅ Andco — 官网确认为 andco.ai（YC S26）

| 维度 | 旧状态 | 新状态 |
|---|---|---|
| **官网** | 弱链，待补 | ✅ andco.ai（useandco.com 重定向至 andco.ai；多方确认） |
| **成立** | 2026（推测） | ✅ 2026，纽约 |
| **创始团队** | 技术+法律背景 | ✅ 维持（未查到具体姓名；不硬猜） |
| **产品** | AI agent 案例整理（医疗记录/警察报告/保险文件） | ✅ 维持 |
| **平台能力** | fax/email/mail/web/SMS/voice 多渠道自动收集 | ✅ 确认（官网描述） |
| **YC状态** | YC S26 入选 | ✅ ycombinator.com/companies/andco |
| **数据硬度** | ★★★☆☆ | ★★★★☆ |

**补查链路：** YC公司页 → andco.ai → pitchbook / extruct.ai

---

### ✅ Ornadyne — 官网确认为 ornadyne.com（YC S26）

| 维度 | 旧状态 | 新状态 |
|---|---|---|
| **官网** | 弱链，待补 | ✅ ornadyne.com（搜索结果直接确认；startuphub.ai 收录） |
| **融资金额** | 未确认 | ✅ $1M（YC + 自身来源） |
| **创始团队** | Geourg Kivijian（NASA JPL/Astrolab 背景），Armen Arakelyan（SpaceX Starship） | ✅ 确认（简历级） |
| **技术方向** | 自主仿生鸟类无人机（flapping-wing ornithopter） | ✅ 确认（hour-class 飞行时长，低声噪） |
| **赛道** | 军事侦察 / 国防科技 | ✅ 维持 |
| **市场定位** | 美国在 flapping-wing 领域落后欧洲/中国；目标重获技术领先 | ✅ 确认 |
| **数据硬度** | ★★★☆☆ | ★★★★☆ |

**补查链路：** YC公司页 → ornadyne.com → startuphub.ai

---

### ✅ Klaimee — 官网确认为 klaimee.ai（YC S26）

| 维度 | 旧状态 | 新状态 |
|---|---|---|
| **官网** | 弱链，待补 | ✅ klaimee.ai（klaimee.co 也存在；主站为 .ai） |
| **创始团队** | Ines Boutemadja（CEO，首位入选YC的阿尔及利亚女性），Julien Catonnet | ✅ 确认（简历级） |
| **产品** | AI agent E&O 保险 + 认证 + 最高 $50K 性能保证 | ✅ 确认（认证和保证在保险推出前先行） |
| **保险状态** | 全面责任险仍在开发 | ⚠️ 如实披露 |
| **目标市场** | 医疗/金融/法律/软件开发企业 | ✅ 确认 |
| ** underwriting 方法** | 公开数据扫描 + AI 治理评估 + 行为测试 | ✅ 确认 |
| **数据硬度** | ★★★☆☆ | ★★★★☆ |

**补查链路：** YC公司页 → klaimee.ai → arabfounders.net / founderland.ai / extruct.ai

---

### ✅ Kuli — 官网确认为 kuli.one（YC S26）

| 维度 | 旧状态 | 新状态 |
|---|---|---|
| **官网** | 弱链，待补 | ✅ kuli.one（G2 / YC / 多个营销媒体确认） |
| **创始团队** | Michael Hodara, Jonathan Hassan | ✅ 确认（未出现在 source packet 中，已补充） |
| **客户案例** | Disney, Nivea, Havas, Supercell | ✅ 确认（来源: 营销媒体；待独立核实） |
| **产品核心** | AI coworker 分析社交媒体视频内容（主动"观看"，非数据库查询） | ✅ 确认 |
| **效率提升** | 营销活动启动速度提升 4 倍 | ✅ 官网/媒体引用 |
| **数据硬度** | ★★★☆☆ | ★★★★☆（客户名单建议后续独立核实） |

**补查链路：** YC公司页 → kuli.one → g2.com / influencermarketinghub.com / aitools.inc

---

### ✅ Havoc AI — 官网确认为 havocai.com（Defense AI / $100M Series A）

| 维度 | 旧状态 | 新状态 |
|---|---|---|
| **官网** | 弱链，待补 | ✅ havocai.com（Leidos 合作公告独立确认） |
| **成立** | 未确认 | ✅ 2024 |
| **总部** | Providence, Rhode Island | ✅ 确认 |
| **合作方** | Leidos（海上/空中自主架构），Hanwha，SAIC | ✅ 确认（Leidos 官网 + havocai.com 双重确认） |
| **产品** | 全域协作自主软件（海上/空中/陆地） | ✅ 维持 |
| **单操作员能力** | 可同时管理数千个自主资产 | ✅ 来源稿核心数据；维持 |
| **资金用途** | 技术创新 + 多域自主栈 + 商业+国防双市场 | ✅ 维持 |
| **数据硬度** | ★★★★☆ | ★★★★★ |

**补查链路：** FinSMEs → Leidos官网（havocai.com 合作公告）→ havocai.com/newsroom

---

### ✅ Coworked — 官网确认为 coworked.ai（Boston / $1.8M）

| 维度 | 旧状态 | 新状态 |
|---|---|---|
| **官网** | 弱链，待补 | ✅ coworked.ai（官网 + prnewswire 双重确认） |
| **产品名** | "Harmony" | ✅ 确认（全称 Coworked Harmony） |
| **创始团队** | Shawn Harris, Ravi Linganuri, Dr. Sulak Soysa | ✅ 确认（来源 packet 未提及，已补充） |
| **融资金额** | $1.8M Seed | ✅ 确认 |
| **投资方** | Open Opportunity Fund + Two Ravens VC 联合领投；Techstars + Underdog Labs 参投 | ✅ 确认（来源 packet 未详列） |
| **产品定位** | AI project manager coworker（不限 license / 不增 dashboard） | ✅ 维持 |
| **PMI 背景数据** | 2030 年全球需 2500 万项目经理 | ✅ 来自 PMI 报告 |
| **数据硬度** | ★★★☆☆ | ★★★★☆ |

**补查链路：** FinSMEs → coworked.ai → prnewswire / thesaasnews / vcnewsdaily

---

### ✅ Exaforce — 官网确认为 exaforce.com（$125M Series B）

| 维度 | 旧状态 | 新状态 |
|---|---|---|
| **官网** | 弱链，待补 | ✅ exaforce.com（多方确认；yourstory / govinfosecurity 独立报道） |
| **融资轮次** | 来源稿称 Series A；实为 Series B | ⚠️ 更正：Series B，$125M |
| **累计融资** | 未确认 | ✅ $200M（含本轮） |
| **投资方** | HarbourVest（领投），Peak XV，Mayfield，Khosla Ventures，Seligman Ventures，AICONIC | ✅ 确认（来源 packet 仅提部分，本轮补全） |
| **创始团队** | Ankur Singla（CEO，前 Volterra 创始人，已出售给 F5） | ✅ 确认 |
| **成立** | 2023 | ✅ 确认 |
| **产品** | Agentic SOC 平台 + MDR 服务（Exabots 24/7） | ✅ 维持 |
| **数据硬度** | ★★★★☆ | ★★★★★ |

**补查链路：** TechCrunch → exaforce.com → yourstory / govinfosecurity

---

### ✅ Vapi — 官网确认为 vapi.ai（$50M Series B）

| 维度 | 旧状态 | 新状态 |
|---|---|---|
| **官网** | 弱链，待补 | ✅ vapi.ai（docs.vapi.ai / vapi.ai/platform 多路径确认） |
| **赛道** | Voice AI / 对话式 AI 基础设施 | ✅ 维持 |
| **产品** | 开发者工具包（语音转文本/LLM/语音合成自由组合，低延迟） | ✅ 维持 |
| **应用场景** | 客户支持 / 销售自动化 | ✅ 维持 |
| **数据硬度** | ★★★★☆ | ★★★★★ |

**补查链路：** TechCrunch → vapi.ai → docs.vapi.ai / lindy.ai / retellai.com

---

## 补充说明：Anthropic $50B 轮次

**来源 packet 状态：** 疑似未官宣，市场预期/媒体推测性质。

**本轮补查结论：** 仍无官方确认。该轮次规模史无前例（$50B 单笔），若坐实将改写行业格局，但现阶段证据不足以作硬判断。

**建议：** 保留为「市场传闻 / 待官宣」标签，不写入正式初筛包。

---

## 总结：弱链补查状态

| 对象 | 赛道 | 官网确认 | 数据硬度（后） | 备注 |
|---|---|---|---|---|
| Andco | Legal AI Agent | ✅ andco.ai | ★★★★☆ | YC S26 |
| Ornadyne | Defense Drone Tech | ✅ ornadyne.com | ★★★★☆ | YC S26，flapping-wing |
| Klaimee | AI E&O Insurance | ✅ klaimee.ai | ★★★★☆ | YC S26，保险在途 |
| Kuli | AI Marketing | ✅ kuli.one | ★★★★☆ | YC S26，客户名单待核实 |
| Havoc AI | Defense Autonomy | ✅ havocai.com | ★★★★★ | $100M Series A |
| Coworked | Agentic PM | ✅ coworked.ai | ★★★★☆ | $1.8M Seed |
| Exaforce | Agentic SOC | ✅ exaforce.com | ★★★★★ | $125M Series B |
| Vapi | Voice AI | ✅ vapi.ai | ★★★★★ | $50M Series B |

**本轮无维持弱链对象。**
**无硬判官网场景。**
**无写入虚拟VC运行台。**

---
*market-scout | signal-scout runtime | 2026-05-19 08:53 CST*