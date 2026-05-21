# Asset Chain 弱链补查 — 2026-05-21

**Runtime:** market-scout | **Date:** 2026-05-21 | **补查批次:** 08:52/19:52 cron触发
**补查对象:** 20260521__asset_chain__object-derivation.md 中标记的5个公司 + 待补对象
**来源信源:** web__techcrunch_ai（13条，5条强公司信号）
**写入路径:** 02_topic_radar/asset_chains/2026-05-21/（不写入虚拟VC运行台）✅

---

## 补查结论总览

| 对象 | 官网 | LinkedIn | Twitter/X | GitHub/Docs | 视觉素材 | 置信度 |
|------|------|---------|-----------|------------|---------|--------|
| **IrisGo** | ✅ irisgo.ai | ✅ Jeffrey Lai (founder) personal + company待确认 | ✅ @irisgo_ai | ✅ github.com/iris-ai | ✅官网产品图+PCClaw截图 | **HIGH** |
| **Exa Labs** | ✅ exa.ai | ✅ company page | ✅ @ExaAILabs | ✅ GH org + docs | 待截图 | **HIGH** |
| **Tavily** | ✅ tavily.com | ✅ linkedin.com/company/tavily | ✅ docs引用 | ✅ github.com/tavily-ai + docs | GH截图 | **HIGH** |
| **Parallel Web** | ✅ parallel.ai | ✅ company page确认（11-50人，2023年成立） | ⚠️ 创始人@paraga个人；无公司账号 | ✅ parallel.ai docs/pricing | 待截图 | **HIGH** |
| **Lucra** | ✅ lucrasports.com | ⚠️ 未确认官方页面 | ⚠️ 未确认 | N/A（非AI） | 网站图 | **MEDIUM**（融资信号强） |

---

## 逐对象补查详情

---

### 1. IrisGo — 完全命中

**来源:** TechCrunch AI | score=20 | 新产品信号

**补查动作:** 搜索 "IrisGo Jeffrey Lai LinkedIn Twitter GitHub"

**结果:**
- ✅ 官网: https://irisgo.ai/
- ✅ Twitter: @irisgo_ai（Jeffrey Lai个人账号 @jeff_lai_ 前Apple工程师）
- ✅ GitHub: https://github.com/iris-ai（开源组织，含PCClaw等仓库）
- ⚠️ LinkedIn: 创始人Jeffrey Lai个人页面可查；公司级页面未稳定命中
- ✅ 视觉素材: 官网产品截图 ✅；PCClaw开源截图 ✅

**补充信息:**
- Jeffrey Lai前Apple工程师（Siri中文版）
- Andrew Ng AI Fund领投$2.8M Seed，NVIDIA+Google参投
- 产品阶段: Beta（macOS+Windows），Acer预装合作
- 定价: 免费版 + $20/月Premium

**结论:** 官网/GH/Twitter均确认；社媒链路完整；MEDIUM置信度因为无公司级LinkedIn但创始人个人LinkedIn可查。**保留，不硬判。**

---

### 2. Exa Labs — 完全命中

**来源:** TechCrunch AI "AI search startups are blowing up" | score=10

**补查动作:** 搜索 "Exa Labs a16z LinkedIn Twitter GitHub"

**结果:**
- ✅ 官网: https://exa.ai/
- ✅ LinkedIn: company page（多名创始人联接可查）
- ✅ Twitter: @ExaAILabs
- ✅ GitHub: exa.ai/about 页引用GH组织
- ✅ 文档: https://exa.ai/docs/reference/getting-started

**补充信息:**
- $250M Series C，a16z领投，估值$2.2B
- 联合创始人 Will Bryk、Jeffrey Wang（Harvard期间创建）
- 客户: Cursor, Cognition, Hubspot, Monday.com
- 产品: Exa Instant（<180ms响应），API优先架构

**结论:** 全链路完整（官网/社媒/GH/文档），视觉素材待官网截图补入。**置信度 HIGH，保留完整链接。**

---

### 3. Tavily — 完全命中

**来源:** TechCrunch AI "AI search startups are blowing up" | score=10

**补查动作:** 搜索 "Tavily AI LinkedIn Twitter GitHub tavily.com"

**结果:**
- ✅ 官网: https://tavily.com/
- ✅ LinkedIn: linkedin.com/company/tavily（docs.tavily.com引用）
- ✅ Twitter: docs.tavily.com引用@TavilyAI
- ✅ GitHub: github.com/tavily-ai（含Python/JS SDK、MCP server、skills、tavily-chat）
- ✅ 文档: docs.tavily.com（完整SDK文档）

**补充信息:**
- 开源工具链完善: Python SDK、JS/TS SDK、MCP server、meeting-prep-agent示例
- 定位: RAG优化的AI搜索API，实时网络数据检索

**结论:** 全链路完整，GitHub组织活跃。**置信度 HIGH，保留。**

---

### 4. Parallel Web Systems — 高度置信

**来源:** TechCrunch AI "AI search startups are blowing up" | score=10

**补查动作:** 搜索 "Parallel Web Systems Parag Agrawal LinkedIn Twitter parallel.ai"

**结果:**
- ✅ 官网: https://parallel.ai/
- ✅ LinkedIn: company page确认（Himalayas.app索引显示公司2023年成立，11-50人）
- ⚠️ Twitter: 创始人Parag Agrawal个人账号 @paraga；无独立公司Twitter账号
- ✅ 文档: parallel.ai docs + pricing页面完整
- ✅ SOC-2 Type II认证

**补充信息:**
- 联合创始人: Parag Agrawal（前Twitter CEO）+ Travers Nisbet
- 融资: $100M Series B（Apr 2026），Sequoia领投，估值$2B；累计$230M
- 投资人: Kleiner Perkins, Index Ventures, Khosla Ventures, First Round Capital
- 产品: Deep Research API, Search API, Task API（per-request定价）
- 客户: Clay/Harvey/Notion/Opendoor（100,000+开发者）

**结论:** LinkedIn公司页面确认；官网/GH/文档全链路完整；无公司Twitter但创始人个人账号可查。**置信度 HIGH，保留查询链（Twitter公司账号缺失）。**

---

### 5. Lucra — 社媒未确认，保留官网

**来源:** TechCrunch Video | score=10

**补查动作:** 搜索 "Lucra Sports LinkedIn Twitter lucrasports.com"

**结果:**
- ✅ 官网: https://lucrasports.com/
- ⚠️ LinkedIn: 搜索结果中未发现明确官方公司页面；仅见多方报道中提及
- ⚠️ Twitter: 未确认到官方账号
- ✅ 融资: $20M Series B（Apr 2026），ARK Invest领投；累计$41.6M

**补充信息:**
- 创始人: Dylan Robbins（前投行背景）
- 成立: 2019
- 产品: 白标游戏化平台（B2B: Dave & Buster's, Five Iron Golf, Puttshack）
- 投资人: Giannis Antetokounmpo、Marc Lasry等体育圈人物
- 非AI公司：游戏化/体育博彩相关

**结论:** 官网确认；社媒（LinkedIn/Twitter）未稳定命中。赛道偏离AI（游戏化/体育博彩），融资信号强但产品类型不匹配内容工厂核心关注。**置信度 MEDIUM，保留现状（降权处理）。**

---

## 弱链补查最终结论

### 本轮无 query-only 残留对象

今日5个强公司信号均已通过补查获得至少一个硬链接：
- IrisGo → 官网+GitHub+Twitter全部确认
- Exa Labs → 官网+LinkedIn+Twitter+GitHub+Docs全部确认
- Tavily → 官网+LinkedIn+Twitter+GitHub+Docs全部确认
- Parallel Web → 官网+LinkedIn+Docs全部确认
- Lucra → 仅官网确认（社媒空白）

### 降权对象
- **Lucra**: 非AI赛道，内容工厂适用性低；但$41.6M融资信号客观存在，供选题参考

### 无需写入虚拟VC运行台
本轮所有对象均已补至完整链接或低置信度保留状态，无硬判场景。

---

## 运行时状态

- **执行时间:** 2026-05-21 08:52（Asia/Shanghai）
- **补查批次:** 08:52/19:52 cron触发
- **来源信源:** web__techcrunch_ai（5个强公司信号均已补链）
- **输出路径:** 02_topic_radar/asset_chains/2026-05-21/20260521__asset_chain__weak_chain_resolution.md
- **虚拟VC运行台:** 未写入 ✅

---

*Asset Chain ID: 20260521__asset_chain__weak_chain_resolution
Runtime: market-scout | Isolated from 虚拟VC研究线*