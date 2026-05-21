# 弱链补查报告 — 2026-05-11 自动补查轮次

**Runtime:** market-scout | **Date:** 2026-05-11 | **补查触发时间:** 2026-05-11 21:43 CST
**Sources:** trend__yc_launches_ai + web__techcrunch_ai + web__finsmes_ai_gnews
**执行目标:** 把当天仍为 query-only 的对象继续补获官网 / 公司社交 / demo/docs 候选链接

---

## 执行摘要

本轮对 `20260511__asset_chain__financing_newco_may11.md` 和 `20260511__asset_chain__product_newco_discovery.md` 中标注为「弱链」的对象执行补查。

**补查对象总数：10 个**
**成功补获官网/可直接访问：9 个（90%）**
**保留查询链（低置信度）：1 个（Scout AI — 备选 scoutco.ai）**
**硬判升级：0 个 — 未硬判任何信号不足对象**
**不写入虚拟VC运行台：✓ 严格遵守**

---

## 补查结果详情

### 1. Tessera Labs — ✅ 官网确认

| 字段 | 旧值（待验证） | 新值（已确认） |
|---|---|---|
| **官网** | tesseralabs.com（反推） | ✅ **https://www.tesseralabs.ai** |
| 状态 | ⚠️ 域名未验证 | ✅ 直接访问 200 OK |
| 产品方向 | SAP→S/4HANA 多智能体迁移 | 确认：vendor-agnostic multi-agent ERP platform |
| 融资 | $60M / a16z领投 | ✅ 确认（BusinessWire/Forbes/pulse2.com 多源） |
| 关键人 | Kabir Nagrecha (CEO) | ✅ PhD UC San Diego / ex-Meta/Novartis |
| 域名验证 | 误判为 tesseralabs.com | 已更正为 tesseralabs.ai |

**验证来源：** businesswire.com, Forbes, thesaasnews.com, techfundingnews.com, pulse2.com
**数据硬度：** ★★★★★ 高 — 多方交叉确认

---

### 2. Pit — ✅ 官网确认

| 字段 | 旧值（待补） | 新值（已确认） |
|---|---|---|
| **官网** | pit.ai 或 pit.com（反推，未确认） | ✅ **https://getpit.ai** |
| 状态 | ⚠️ 未验证 | ✅ 直接访问（来源确认） |
| 融资 | $16M Seed / a16z领投 | ✅ 确认（Forbes/NextWeb/techfundingnews.com） |
| 关键人 | Adam Jafer (CEO) | ✅ ex-Voi/Klarna/iZettle |
| 竞品区分 | — | ✅ 与 defunct fintech Pit.ai 完全独立（getpit.ai 为官方） |

**验证来源：** Forbes, TheNextWeb, techfundingnews.com, cxodigitalpulse.com, startuphub.ai, YC (ycombinator.com/companies/pit-ai)
**数据硬度：** ★★★★★ 高 — a16z领投+多家独立媒体

---

### 3. Scout AI — ✅ 官网确认（候选升级）

| 字段 | 旧值（待补） | 新值（已确认） |
|---|---|---|
| **官网** | scout.ai（未确认） | ✅ **https://www.scoutco.ai** |
| 状态 | ⚠️ 未捕获 | ✅ scoutco.ai（搜索确认） |
| 产品代号 | Fury (VLA model), Ox (autonomous vehicle) | ✅ Fury foundation model for unmanned warfare |
| 融资 | $100M Series A（PR Newswire） | ✅ Align Ventures + Draper Associates 联合领投 |
| 关键人 | Colby Adcock (CEO), Collin Otis (CTO) | ✅ 确认（oodaloop.com 独立采访验证） |
| 总部 | Sunnyvale, CA | ✅ 确认；测试设施在 Paso Robles, CA |

**验证来源：** oodaloop.com, americanentrepreneurship.com, techstrong.ai, paraform.com
**补充说明：** PR Newswire 来源确认 $100M Series A（Align+Draper）；另有一说 $11M Department of War contract 来源待独立验证；本报告不升级为投资结论
**数据硬度：** ★★★★☆ 高（融资）/ ★★★☆☆ 中（合同金额待验证）

---

### 4. AMI Labs — ✅ 官网确认

| 字段 | 旧值（待补） | 新值（已确认） |
|---|---|---|
| **官网** | 未直接捕获 | ✅ **https://amilabs.xyz** |
| 状态 | ⚠️ 未捕获 | ✅ amilabs.xyz 直接确认 |
| 全称 | AMI Labs | Advanced Machine Intelligence (AMI) Labs |
| 关键人 | Yann LeCun (Executive Chairman) | ✅ Alex LeBrun (CEO) |
| 总部 | Paris | ✅ Paris HQ；另设 New York, Montreal, Singapore |
| 产品方向 | "World Models" | ✅ 确认：action-conditioned world models for physical world AI |

**验证来源：** amilabs.xyz, polytechnique.edu, indiatimes.com, Medium, grokipedia.com
**数据硬度：** ★★★★★ 高 — 官网直接+多学术/媒体独立确认

---

### 5. Kanvas Biosciences — ✅ 官网确认

| 字段 | 旧值（待补） | 新值（已确认） |
|---|---|---|
| **官网** | 未直接捕获 | ✅ **https://www.kanvasbio.com** |
| 产品方向 | 空间生物学 | ✅ 更正：microbiome-based therapeutics / spatial mapping platform |
| 技术来源 | — | ✅ Cornell University exclusive license |
| 总部 | — | ✅ Princeton, New Jersey |
| 融资 | $48M Series A（DCVC+Lions Capital） | ✅ 确认（biospace.com + PR Newswire） |

**验证来源：** kanvasbio.com, biospace.com, prnewswire.com, cornell.edu
**重要更正：** 原 asset chain 描述为"空间生物学"偏宽泛；官网确认为 microbiome therapeutics 赛道
**数据硬度：** ★★★★☆ 高 — 官网+VC背书+学术源

---

### 6. Beacon Health — ✅ 官网确认

| 字段 | 旧值（待补） | 新值（已确认） |
|---|---|---|
| **官网** | beaconhealth.ai（待验证） | ✅ **https://www.beaconhealth.ai** 直接访问 200 OK |
| 产品方向 | AI employees 自动化初级护理后台 | ✅ 确认：预防筛查/预先授权/转诊/风险调整 |
| 落地 | 40,000 患者群体 | ✅ 确认（独立医师协会合作） |

**验证来源：** beaconhealth.ai 直接访问, YC page
**数据硬度：** ★★★★☆ 高 — YC官方+官网双重确认

---

### 7. Fazeshift — ✅ 官网确认

| 字段 | 旧值（待补） | 新值（已确认） |
|---|---|---|
| **官网** | fazeshift.com（推测） | ✅ **https://www.fazeshift.com** |
| 创始团队 | — | ✅ Caitlin Leksana (CEO, Harvard), Timmy Potter (CTO, MIT) |
| 融资 | $17M Series A / $22M 累计（F-Prime领投） | ✅ 确认 |
| 产品方向 | AI agents 自动化 AR 工作流 | ✅ 端到端 order-to-cash；90%+任务自主处理 |

**验证来源：** fazeshift.com, fprimecapital.com, ycombinator.com/companies/fazeshift, fintech.global
**数据硬度：** ★★★★☆ 高 — YC+官网+F-Prime三方确认

---

### 8. XCaliber Health — ✅ 官网确认

| 字段 | 旧值（待补） | 新值（已确认） |
|---|---|---|
| **官网** | xcaliberhealth.com（推测） | ✅ **https://www.xcaliberhealth.ai** |
| 产品 | "Agentic OS for healthcare admin" | ✅ Merlin AI agents；自动处方补充/转诊协调/日程管理 |
| 规模 | $6.5M Seed | ✅ 每日处理 8M+ chart updates / 160k+ EHR updates |
| 覆盖 | — | ✅ 700,000+ 患者基础 |
| 投资方 | ManchesterStory | ✅ 确认 |

**验证来源：** xcaliberhealth.ai, morningstar.com, hitconsultant.net, pulse2.com, briefglance.com
**数据硬度：** ★★★★☆ 高 — 官网+Morningstar+多家媒体

---

### 9. Meatly — ✅ 官网确认

| 字段 | 旧值（待补） | 新值（已确认） |
|---|---|---|
| **官网** | 未确认 | ✅ **https://meatly.pet** |
| 赛道 | 培育肉 | ✅ 更精确：cultivated chicken for pet food（欧洲首个授权销售） |
| 产品 | — | ✅ Chick Bites（与 THE PACK 合作）；已在 Pets at Home 伦敦店上市 |
| 监管 | — | ✅ 欧洲首个获授权培育肉宠物食品公司 |
| 投资方 | — | ✅ Pets at Home |

**验证来源：** meatly.pet, petfoodindustry.com
**数据硬度：** ★★★☆☆ 中 — 官网+行业媒体；赛道独特性高但体量偏细分

---

### 10. Terranox AI — ✅ 官网确认

| 字段 | 旧值（待补） | 新值（已确认） |
|---|---|---|
| **官网** | 未确认 | ✅ **https://terranox.ai** |
| YC W26 | Batch W26 | ✅ Demo Day 参与确认 |
| 产品方向 | AI + 铀矿勘探 | ✅ 训练于 70+ 年 geoscience data；North America uranium targets |
| 投资方 | — | ✅ YC, Climate Capital, Spot VC |
| 融资 | — | ⚠️ 未单独确认（YC + 种子轮次融资规模未披露） |

**验证来源：** terranox.ai, ycombinator.com/companies/terranox-ai, extruct.ai, foundevo.com, pitchbook.com
**数据硬度：** ★★★☆☆ 中 — YC官方+官网确认；具体融资规模待补充

---

## 补查成果矩阵

| 对象 | 原状态 | 补查后状态 | 官网 | 数据硬度 |
|---|---|---|---|---|
| Tessera Labs | ⚠️ tesseralabs.com（误） | ✅ 确认 | tesseralabs.ai | ★★★★★ |
| Pit | ⚠️ 未确认 | ✅ 确认 | getpit.ai | ★★★★★ |
| Scout AI | ⚠️ scout.ai（未确认） | ✅ scoutco.ai | scoutco.ai | ★★★★☆ |
| AMI Labs | ⚠️ 未捕获 | ✅ 确认 | amilabs.xyz | ★★★★★ |
| Kanvas Biosciences | ⚠️ 未捕获 | ✅ 确认 | kanvasbio.com | ★★★★☆ |
| Beacon Health | ⚠️ 推测域名 | ✅ 直接访问 | beaconhealth.ai | ★★★★☆ |
| Fazeshift | ⚠️ 推测域名 | ✅ 确认 | fazeshift.com | ★★★★☆ |
| XCaliber Health | ⚠️ 推测域名 | ✅ 确认 | xcaliberhealth.ai | ★★★★☆ |
| Meatly | ⚠️ 未捕获 | ✅ 确认 | meatly.pet | ★★★☆☆ |
| Terranox AI | ⚠️ 未捕获 | ✅ 确认 | terranox.ai | ★★★☆☆ |

**本轮补查硬链接补获率：9/10（90%）**
**保留查询链（未硬判）：1/10（10%）— Scout AI 合同金额 $11M（Department of War）仍为单源**

---

## 未升级对象（遵守不硬判原则）

### Scout AI — $11M Department of War 合同
- **现状：** PR Newswire 提及 $11M contract；oodaloop.com 采访提及$100M Series A
- **补查结果：** scoutco.ai 已确认，$100M Series A（Align+Draper）已多方确认
- **保留原因：** $11M 合同金额仅来自 PR Newswire，oodaloop.com 采访未提；未做独立交叉验证
- **处理方式：** 保留查询链 → "首年获得 Department of War 合同（来源：PR Newswire，待验证）"
- **数据硬度：** ★★★☆☆ — 融资已确认 / 合同金额存疑

---

## 重要更正记录

| 对象 | 原错误描述 | 更正内容 |
|---|---|---|
| Tessera Labs | 官网 tesseralabs.com | 正确为 tesseralabs.ai |
| Kanvas Biosciences | 空间生物学（宽泛） | microbiome therapeutics（精确） |
| Pit | 可能为 pit.com | 正确为 getpit.ai；与 defunct fintech Pit.ai 完全独立 |
| Scout AI | scout.ai | scoutco.ai |
| AMI Labs | 未捕获 | amilabs.xyz |

---

## 输出物路径

| 交付物 | 路径 |
|---|---|
| 补查报告（本文） | `10_logs/20260511__market-weak-chain-resolution-supplement.md` |
| 原始 asset chain (financing) | `02_topic_radar/asset_chains/20260511__asset_chain__financing_newco_may11.md` |
| 原始 asset chain (product) | `02_topic_radar/asset_chains/20260511__asset_chain__product_newco_discovery.md` |

---

*Generated by market-scout runtime | 2026-05-11 21:43 CST*
*本文件仅供内容工厂内部使用，不写入虚拟VC运行台*
*弱链补查原则：不硬判、不升级信号不足对象、保留查询链与低置信度结论*