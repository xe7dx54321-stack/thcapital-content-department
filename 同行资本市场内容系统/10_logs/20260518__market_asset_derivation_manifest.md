# Derivation Manifest | 2026-05-18 | market_asset_derivation_round

**运行时:** market-scout | 2026-05-18 20:22 CST
**触发:** cron 08:32/19:32 (market_asset_derivation)
**输入源:** web__techcrunch_ai (16 items); wechat__founder_park (无当日更新); finsmes/yc_launches (当日无新条目)
**目标:** 当日融资 / NewCo 入口 → 对象一跳派生

---

## 本轮抓取状态

| source-id | 当日状态 | 条目数 |
|-----------|---------|--------|
| trend__yc_launches_ai | ❌ 无当日条目 | 0 |
| web__techcrunch_ai | ✅ 有条目 | 16 |
| web__finsmes_ai_gnews | ❌ 无当日条目 | 0 |
| wechat__founder_park | ❌ 无当日新文章 | 0 |
| wechat__36kr / 其他 | ❌ 无当日新文章 | 0 |

---

## 派生对象（3个）

### 1. LetinAR — 韩国AR光学组件商 ✅ 强信号
- **TC标题:** South Korea's LetinAR is building optics behind AI glasses
- **融资:** $18.5M（KDB + Lotte Ventures），2027 IPO
- **官网:** letinar.com（live）
- **核心技术:** PinTILT™ AR光学模组
- **下游客户:** Meta Ray-Ban / Google Android XR / Samsung / Apple
- **资产路径:** `asset_chains/20260518__asset_chain__LetinAR__ar_optics.md`
- **评分:** ⭐⭐⭐⭐⭐ 进 Top20

### 2. Nectar Social — Agentic Marketing OS ✅ 强信号（资产链需补）
- **TC标题:** Marketing operating system Nectar Social raises $30M Series A led by Menlo
- **融资:** $30M Series A，Menlo Ventures + Anthology Fund（Anthropic）
- **官网:** nectarsocal.com ❌ 域名失效，需重新定位
- **创始人:** Misbah + Farah Uraizee（前Meta，姐妹组合）
- **客户:** Liquid Death / Figma / e.l.f Beauty
- **资产路径:** `asset_chains/20260518__asset_chain__Nectar_Social__30m_seriesA.md`
- **评分:** ⭐⭐⭐⭐ 进 Top20（资产链需补证）

### 3. Lake Tahoe Energy Crunch — 趋势/事件稿 ⚠️ 降级
- **TC标题:** Silicon Valley's vacationland needs a new energy provider just as AI is driving prices up
- **信号:** score=15 + signal_reasons=[新产品信号]（误判，实际是趋势/能源事件稿）
- **处理:** 保留为 topic cluster 背景素材，不作为 NewCo 对象处理
- **无明确公司/项目信号：** 是事件叙事，不是产品发布

---

## 跳过对象（无明确公司/项目信号）

| # | TC标题 | 跳过原因 |
|---|--------|---------|
| 1 | Why trust is a big question at the Elon Musk-OpenAI trial | 已有公司（OpenAI）诉讼叙事，无新公司信号 |
| 2 | If you're giving a commencement speech in 2026, maybe don't mention AI | 趋势/哲学文章，无公司信号 |
| 3 | TechCrunch Mobility: The AI skills arms race is coming for automotive | 行业趋势文章，无具体公司/项目信号 |
| 4 | The haves and have nots of the AI gold rush | 趋势分析，无公司信号 |
| 5 | Research repository ArXiv will ban authors for a year | 已有机构（ArXiv）政策新闻 |
| 6 | The offline desk gadget that actually got me to sit up straight | 消费品评测，无创业公司信号 |
| 7 | OpenAI co-founder Greg Brockman takes charge of product strategy | 已有公司（OpenAI）内部人事报道 |
| 8 | $60B AI chip darling Cerebras almost died early on... | 已有公司（Cerebras）历史叙事 |
| 9 | Users turn to jailbreaking their older Kindles as Amazon ends support | 已有公司（Amazon）政策新闻 |
| 10 | RJ Scaringe has raised more than $12B across three startups | 人物（RJ Scaringe）叙事，不是具体公司 |
| 11 | General Catalyst posted VC rage bait | VC机构文章，无新公司信号 |
| 12 | Tesla reveals two Robotaxi crashes | 已有公司（Tesla）事故新闻 |
| 13 | OpenAI launches ChatGPT for personal finance | 已有公司（OpenAI）产品功能扩展 |

---

## 下跳查询（待下一轮补查）

| 对象 | 待查项目 | 状态 |
|------|---------|------|
| LetinAR | LinkedIn / Crunchbase / Twitter | 🔍 |
| Nectar Social | 真实官网URL（nectarsocal.com失效）| ⚠️ 紧急 |
| Nectar Social | 创始人 LinkedIn / Crunchbase | 🔍 |

---

## 输出文件

- `asset_chains/20260518__asset_chain__LetinAR__ar_optics.md`
- `asset_chains/20260518__asset_chain__Nectar_Social__30m_seriesA.md`
- `10_logs/20260518__market_asset_derivation_manifest.md`（本文件）

**边界检查:** 未写入虚拟VC运行台 ✅