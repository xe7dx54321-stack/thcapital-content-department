# 市场内容信源清单 — 2026-05-11

**Runtime:** market-scout | **Date:** 2026-05-11 | **Lane:** product / newco discovery
**Generated:** 2026-05-11 12:50 CST

---

## 今日执行概况

| 动作 | 状态 | 说明 |
|------|------|------|
| trend__yc_launches_ai | ✅ 完成 | YC W26 batch信源补获（10个AI公司） |
| web__techcrunch_ai | ✅ 完成 | TechCrunch + FinSMEs融资报道 |
| web__finsmes_ai_gnews | ✅ 完成 | FinSMEs周报（~2026-05-01）7个融资事件 |
| trend__trend_hunt_ai_agents | ✅ 完成 | Trend Hunt补充线索（agent产品发现趋势） |
| asset derivation | ✅ 完成 | 17/20 硬链接补获（85%） |
| Top20 初筛包 | ✅ 完成 | 20个product/newco对象结构化评分 |
| 脚本执行 | ⚠️ 跳过 | market_topic_capture_round.py 不存在 |

---

## 实际写入文件清单

### Source Packets (4个)
- `02_topic_radar/source_packets/2026-05-11/__trend__yc_launches_ai__2026-05-11.md`
- `02_topic_radar/source_packets/2026-05-11/__web__techcrunch_ai__2026-05-11.md`
- `02_topic_radar/source_packets/2026-05-11/__web__finsmes_ai_gnews__2026-05-11.md`
- `02_topic_radar/source_packets/2026-05-11/__trend__trend_hunt_ai_agents__2026-05-11.md`

### Asset Chain (1个)
- `02_topic_radar/asset_chains/20260511__asset_chain__product_newco_discovery.md`

### Top20 初筛包 (1个)
- `03_topic_candidates/20260511__top20-screening-pack__product-newco.md`

---

## Source Packet 统计

| Source ID | 信号数 | 关键公司/对象 |
|-----------|--------|--------------|
| trend__yc_launches_ai | 14个对象（含YC batch survivors） | Beacon Health / Corelayer / Pace / C47martini.film / Shofoshofo.ai / Fenrock AI / Axion |
| web__techcrunch_ai | 12个对象 | Sierra / Blitzy / Ineffable Intelligence / Factory / Nova Intelligence |
| web__finsmes_ai_gnews | 7个融资事件 | Ineffable ($1.1B) / Blitzy ($200M) / Nova ($40M) / Fazeshift ($17M) / Tekst (€11.5M) / XCaliber ($6.5M) / Corvera ($4.2M) |
| trend__trend_hunt_ai_agents | 5+趋势方向（补充线索） | AI Super Agents / agent-first product discovery / no-code multi-agent orchestration |

---

## 强信号对象（Top5）

1. **Ineffable Intelligence** — $1.1B seed / $5.1B valuation | David Silver (DeepMind) | reinforcement learning superlearner | UK government背书
2. **Blitzy** — $200M Series B / $1.4B valuation | autonomous software dev platform | blitzy.com | 3,000+ AI agents | 数十家Global 2000落地
3. **Sierra** — $950M Series B / $15B+ valuation | AI agents for CX | Bret Taylor + Clay Bavor | 最高背书组合
4. **Nova Intelligence** — $40M | agentic AI platform for SAP | novaintelligence.com | SAP官方合作 | Festo/KION客户
5. **Beacon Health** — YC W26 | AI agents for primary care | 40,000患者群体已落地 | Mark Pothen创始人

---

## 弱链补查清单

| 对象 | 待补项 | 优先级 |
|------|--------|--------|
| Ineffable Intelligence | 官网最终确认（ineffable.limited vs ineffable.ai） | HIGH |
| Blitzy | 产品截图/demo视频；客户名单 | HIGH |
| Beacon Health | 官网确认；产品截图 | HIGH |
| C47martini.film / Pace / Motion / Lucid | YC slug验证；官网补获 | MEDIUM |
| Shofoshofo.ai | 官网补获；视频数据集产品形态 | MEDIUM |
| Axion | 卫星AI具体产品形态 | MEDIUM |

---

## 隔离确认

- ✅ 无内容写入 `/Users/apple/Documents/虚拟vc项目开发规划/同行资本运行台/`
- ✅ 无任务挂到 data-star runtime
- ✅ 所有文件写入内容工厂目录：`/Users/apple/Documents/同行资本市场内容系统/`

---

*Manifest ID: market-source-manifest__product-newco-discovery__2026-05-11*
*Runtime: market-scout | Isolated from 虚拟VC研究线*