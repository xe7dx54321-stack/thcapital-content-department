# 同行资本市场内容系统｜2026-03-25｜融资信号线审计

## 1. 结论先说

`daily financing` 这条线**不是没加**，而是已经在 seed 设计里存在，只是之前还没有被单独审计说明。

这轮复核后，结论如下：

- **已接入且已实测跑通的稳定入口**
  - `trend__yc_launches_ai`
  - `web__techcrunch_ai`
  - `web__finsmes_ai_gnews`
  - `web__itjuzi`
- **已纳入体系但当前仍高阻力的战略入口**
  - `web__finsmes_ai`
  - `web__theinformation_briefings`
- **产品发现补充入口**
  - `trend__trend_hunt_ai`

所以这条线当前不是“没有”，而是：

> **已经具备稳定主干，但还保留若干高价值高阻力源待后续增强。**

---

## 2. 本轮实测结果

### 2.1 `YC Launches`

- 测试路径：直连 `https://www.ycombinator.com/launches.json`
- 结果：可稳定拿到结构化 JSON
- 业务价值：
  - 适合发现新产品、新公司、新业务模式
  - 很适合作为“融资/新公司/新项目”入口

### 2.2 `TechCrunch AI`

- 测试路径：`Jina reader`
- 结果：可稳定拿到 AI 类目页
- 业务价值：
  - 对新融资、新产品、新公司报道敏感
  - 适合作为 daily financing/newco 主盘的一部分

### 2.3 `FinSMEs AI`

- 测试路径：direct + Jina
- 结果：仍然落到安全验证页
- 当前判断：
  - 业务价值高
  - 但暂不适合作为 daily 默认入口

### 2.4 `FinSMEs` fallback

- 测试路径：Google News `site:finsmes.com artificial intelligence funding` RSS
- 结果：可稳定拿到 `FinSMEs` 融资标题流
- 当前判断：
  - 可作为 blocked source 的受控 fallback
  - 只适合做融资入口，不适合直接当最终事实证据

### 2.5 `Trend Hunt / Product Hunt Mirror`

- 测试路径：`https://trend-hunt.com/api/search`
- 结果：可稳定返回产品列表与基础结构化字段
- 当前判断：
  - 更偏 `product discovery`
  - 可补充新产品/新工具入口
  - 但不应直接当作“融资事实证明”

### 2.6 `IT 桔子`

- 测试路径：
  - `itjuzi.com` 行业 / 库页直连
  - `Jina reader` 直连 `itjuzi.com` 页面
  - `IT 桔子` 公开 AI 融资报告 PDF → `Jina reader`
- 结果：
  - 直连库页与 Jina 页面链路均被 `412 Precondition Failed` 挡住
  - 公开 PDF 报告可稳定抓取，且能拿到融资规模、轮次结构、地域分布、细分赛道融资概览
- 当前判断：
  - 已经可以作为**国内融资数据库线的公开官方兜底入口**
  - 适合补中国 AI 融资的结构化背景层
  - 但还不能替代 `IT 桔子` live database 的实时 company/event 查询

---

## 3. 当前推荐运行方式

每天跑融资线时，优先按下面的顺序：

1. `YC Launches`
2. `TechCrunch AI`
3. `FinSMEs` fallback
4. `IT 桔子` 公开报告
5. 如需补充新产品热度，再看 `Trend Hunt / Product Hunt Mirror`
6. 对发现的新对象，必须继续做派生链：
   - 公司官网
   - 创始人 / 公司社交账号
   - demo / docs / repo
   - 后续融资或客户证明

注意：

> **入口页只是发现线索，不是最终对象。**

真正能进入后续分析的，是派生出来的对象链，而不是一篇“某公司融资了”的快讯本身。

---

## 4. 当前仍存在的缺口

1. `FinSMEs AI` 官方原站仍未直连打通
2. `IT 桔子` live database / company page 仍会被 `412` 挡住，当前只能先跑公开报告层
3. `The Information Briefings` 仍不适合自动化主盘
4. 融资事实与产品价值还需要更系统的 cross-check

---

## 5. 当前最终判断

融资线当前状态可以定义为：

> **主干已上线、可每天使用；中国融资背景层已补上 IT 桔子公开报告兜底，但实时数据库层仍待后续增强。**
