# 同行资本市场内容工厂 · 每日 Top 8 → Top 5 建议板
**Runtime:** market-editor（day_mainline裁判输出）| **Date:** 2026-05-13（周三）
**依据：** `20260513__top20__stage-gate-scorecard.md`（final，19:10 CST）
**continuity_decision:** `continuity_only` | **continuity_output:** `top20_mini_slate`
**生成时间：** 2026-05-13 19:11 CST

---

## 📋 前置依赖状态

| 依赖 | 路径 | 状态 |
|------|------|------|
| Top20 Scorecard | `10_logs/20260513__top20__stage-gate-scorecard.md` | ✅ final |
| Canonical Pack | `03_topic_candidates/20260513__top20-screening-pack.md` | ✅ final |
| Official Update Lane | `03_topic_candidates/20260513__top20-screening-pack__official-update-lane.md` | ✅ final |
| Financing / NewCo Lane | `03_topic_candidates/20260513__top20-screening-pack__financing-newco.md` | ✅ final |
| Product / NewCo Lane | `03_topic_candidates/20260513__top20-screening-pack__product-newco.md` | ✅ final |
| Redteam Review | `10_logs/20260513__top20__redteam-review.md` | ✅ final |
| topic_radar_brief | ❌ 脚本不存在（无 radar brief） | ⚠️ 无 |
| artifact_status 验真脚本 | ❌ 脚本不存在 | ⚠️ 无法 formal artifact 验真 |

> **supply gap 声明：** Canonical pack 20条最高仅23分，无任何 ≥8 分；本次 Top5 推进完全依赖 lane 包 P0 标的 + redteam priority matrix，不从 canonical pack 凑数。

---

## 🏆 Top 5 正式推荐标的

> 排序逻辑：P0 无条件进入 → P1 依修复状态进入 → 若不足5个 P0/P1，写实 supply gap，不凑数

| # | 标的 | 类型 | 赛道 | 来源 Lane | 融资数据 | 热度信号（heat） | 证据信号（evidence） | 推荐理由 | 裁判备注 |
|---|------|------|------|----------|----------|-----------------|---------------------|----------|----------|
| 1 | **阶跃星辰（StepFun）** | 中国大模型 | 多模态基础模型 | financing-newco / product-newco | 红队⭐⭐⭐⭐⭐ | 官方更新密度高；builder圈共振强 | 官方公告+媒体跟进；赛道稀缺性极高 | 中国基础模型赛道最接近 OpenAI/Anthropic 的标的；月之暗面竞品 | P0 · 无条件进入 |
| 2 | **月之暗面（Moonshot AI）** | 中国大模型 | 多模态基础模型 | financing-newco / product-newco | 红队⭐⭐⭐⭐⭐ | Kimi 产品热度持续；资本市场关注度高 | 官方公告+产品发布；$10B+估值有机构背书 | 中国大模型绝对龙头；Kimi C端落地验证商业模式 | P0 · 无条件进入 |
| 3 | **Anthropic × SpaceX Colossus 1** | 算力扩张 | AI Infra / 算力 | official-update-lane | 300MW+，220,000+ NVIDIA GPU，本月上线 | TechCrunch/VentureBeat/量子位等媒体高密度覆盖 | 官方公告（Colossus 1）；SpaceX官方确认 | 史上最大算力事件；直接提升 Claude Code rate limits；算力瓶颈破局者 | P0 · 无条件进入 |
| 4 | **Isomorphic Labs** | AI药物发现 | AI + Biotech | financing-newco / product-newco | $2.1B Series B；Thrive Capital连续领投；Alphabet/GV/MGX/Temasek/CapitalG | 红队⭐⭐⭐⭐；全球媒体覆盖 | TechCrunch来源；B-1 修正：投资方为 Alphabet 旗下 GV/CapitalG（非直接 Alphabet） | $2.1B 月度最高单笔；Demis Hassabis 背景背书；AI drug discovery 赛道破圈 | P0 · B-1 投资方描述需修正后进入 |
| 5 | **Sierra** | AI客户体验平台 | 企业软件 / Agent | product-newco | $950M Series B；$15B+估值；Bret Taylor+Clay Bavor | 红队⭐⭐⭐⭐；$950M大额B轮；VC圈高关注 | TechCrunch来源；Bret Taylor（Salesforce前CEO）+ Clay Bavor创始人背书 | 最高创始人组合；企业软件+AI双赛道；$15B估值验证市场空间 | P0 · 无条件进入 |

---

## 🔒 Holdout 3（次优先，不入 Top5，但保留在主推进序列边缘）

> 若 Top5 中任一标的出现信源污染或事实失真，按顺序从 Holdout 3 补位

| # | 标的 | 类型 | 赛道 | 来源 Lane | 融资数据 | 热度信号（heat） | 证据信号（evidence） | Holdout 理由 |
|---|------|------|------|----------|----------|-----------------|---------------------|--------------|
| H1 | **Exaforce** | 公司 | Agentic SOC / SIEM | product-newco | $125M Series B；$725M估值 | TechCrunch来源；安全agent赛道快速成形 | TechCrunch来源；评分23分（canonical pack最高） | canonical pack 最高分，但总分仍<8；B轮大额但媒体密度中等；进入需补强 |
| H2 | **AMI Labs** | 公司 | 世界模型 | financing-newco | $1.03B Seed（欧洲最大seed）；Yann LeCun执行主席 | 红队⭐⭐⭐⭐；$1.03B超大额seed | TechCrunch来源；A-3 投资人标注（NVIDIA/Temasek/Samsung/Toyota/Mark Cuban/Eric Schmidt 待确认） | 赛道强，金额高；但 A-3 级信源污染需 signal-scout 修复；修复前不得进入发布队列 |
| H3 | **OpenAI Daybreak** | 官方更新 | AI 安全 / 合作 | official-update-lane | 官方发布（5/12）+ TAC 体系 | 官方博客+欧盟委员会合作；AI安全监管话题破圈 | 官方一手来源；跨政府合作信号 | 官方更新强，但属企业更新而非融资标的；视平台任务需要可升级 |

---

## ❌ 未进入推荐（含不可推进对象）

| 标的 | 排除原因 | 是否可修复 |
|------|---------|-----------|
| Canonical pack 内20条全部 | 最高23分，无≥8分；一手性/数据硬度不足 | 需 market-scout 重新溯源，不在本次 continuity 范围 |
| Ineffable Intelligence | A-1：创始人 David Silver 正确归因至 Recursive Superintelligence，非 Ineffable | 待 signal-scout 修复 A-1 后降级 |
| Recursive Superintelligence | A-2：估值"$500M @ $4B（pré-money）"需修正；"国家大基金领投"标注传言 | 待 signal-scout 修复 A-2 |
| AMI Labs（完整版） | A-3：$1.03B 投资人列表（NVIDIA/Temasek/Samsung/Toyota/Mark Cuban/Eric Schmidt）需拆分并标注待确认 | 待 signal-scout 修复 A-3 |
| Ciridae / Pit / Performativ | B-2：缺官网或官方公告 | 待 market-scout 补强 |
| YC S26 弱链（Andco / Ornadyne / Klaimee / Kuli） | 官网/LinkedIn/产品截图未补强 | 待 topic-planner 补强前不得进入 platform task sheet |
| Havoc AI | canonical pack 20分；$100M Series A 数据真实但媒体密度偏低 | 可进入 P2 待选，需 topic-planner 评估 |

---

## 🔗 关键链接 / Source Packet Path

| 标的 | Source Packet |
|------|--------------|
| 阶跃星辰 | `03_topic_candidates/20260513__top20-screening-pack__financing-newco.md` / `product-newco.md` |
| 月之暗面 | `03_topic_candidates/20260513__top20-screening-pack__financing-newco.md` |
| Anthropic × SpaceX | `03_topic_candidates/20260513__top20-screening-pack__official-update-lane.md` |
| Isomorphic Labs | `03_topic_candidates/20260513__top20-screening-pack__financing-newco.md` / `product-newco.md` |
| Sierra | `03_topic_candidates/20260513__top20-screening-pack__product-newco.md` |
| Exaforce | `03_topic_candidates/20260513__top20-screening-pack__product-newco.md` |
| AMI Labs | `03_topic_candidates/20260513__top20-screening-pack__financing-newco.md` |
| OpenAI Daybreak | `03_topic_candidates/20260513__top20-screening-pack__official-update-lane.md` |

---

## 📌 下一步 owner

| 动作 | Owner | 前提条件 |
|------|-------|---------|
| 修复 A-1（Ineffable 创始人溯源） | signal-scout / market-scout | 无 |
| 修复 A-2（Recursive 估值措辞） | signal-scout / market-scout | 无 |
| 修复 A-3（AMI Labs 投资人标注） | signal-scout / market-scout | 无 |
| 修复 B-1（Isomorphic 投资方描述） | signal-scout / market-scout | 无 |
| B-1 完成后 → Isomorphic 进入 platform task sheet | topic-planner | A-3 投资人标注完成 |
| 补强 Exaforce 官网/demo | market-scout | 无 |
| 补强 YC S26 弱链官网/截图 | market-scout | 无 |
| 基于本板输出 platform task sheet | topic-planner | 本板 final 后 |

---

## ❗ Supply Gap 诚实声明

本次 Top 5 推进依赖 **lane 包 P0 标的（3个中国大模型 + 1个算力事件 + 1个大额融资）**，canonical pack 20条无任何 ≥8 分标的。

若排除中国大模型（阶跃/月之暗面），纯 non-中文 全球标的仅有 **Anthropic × SpaceX + Isomorphic Labs + Sierra = 3个**，**不足5个**。

本次 **不凑数**，Holdout 3 中的 Exaforce / AMI Labs 在信源修复完成前不得顶替进入 Top5。

---

*market-editor | 2026-05-13 19:11 CST | day_mainline Top 5 board（continuity_only 模式）*
*生成路径: 03_topic_candidates/20260513__daily-top8-to-top5.md*
*依据 scorecard: 10_logs/20260513__top20__stage-gate-scorecard.md*
*⚠️ artifact_status 验真脚本不存在；本板以上游 scorecard final 为前提*