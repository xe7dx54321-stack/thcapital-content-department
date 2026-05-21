# Market Source Manifest — 2026-05-12 弱链补查

**Runtime:** market-scout | **Date:** 2026-05-12 08:55 CST
**Trigger:** cron/d7eb4d97-ff8d-4c03-a9af-3b10c3bd82ea

---

## 本次执行文件清单

| 文件路径 | 类型 | 状态 |
|---|---|---|
| `02_topic_radar/asset_chains/20260512__asset_chain__weak_chain_resolution.md` | 弱链补查报告 | ✅ 新建 |
| `02_topic_radar/asset_chains/20260511__asset_chain__product_newco_discovery.md` | 原始资产链（弱链来源） | 引用 |
| `02_topic_radar/asset_chains/20260511__asset_chain__financing_newco_may11.md` | 原始资产链（弱链来源） | 引用 |

---

## 弱链补查执行摘要

**补查对象数：** 9（来自 2026-05-11 两份资产链中的未确认/待补对象）
**成功升级硬链接：** 8/9
**维持弱链：** 1/9（EigenCube AI）

---

## 补查覆盖信源

| source-id | 说明 |
|---|---|
| trend__yc_launches_ai | YC W26 launches 产品补充 |
| web__techcrunch_ai | TechCrunch AI funding报道 |
| web__finsmes_ai_gnews | FinSMEs AI融资追踪 |

---

## 关键升级对象（官网补获）

| 对象 | 新补获官网 | 域名拼写纠正 |
|---|---|---|
| Tessera Labs | tesseralabs.ai | — |
| Beacon Health | beaconhealth.ai | — |
| Fazeshift | fazeshift.com | — |
| XCaliber Health | xcaliberhealth.ai | — |
| Pit | pit.com | — |
| Scout AI | scoutco.ai | — |
| Martini | martini.film | c47martini.film → martini.film |
| Shofo | shofo.ai | shofoshofo.ai → shofo.ai |

---

## 弱链维持对象

| 对象 | 状态 | 处理方式 |
|---|---|---|
| EigenCube AI | 无法稳定命中官网 | 保留查询链；不硬判；不写入虚拟VC运行台 |

---

*Manifest ID: market-source-manifest__weak-chain-2026-05-12*
*Runtime: market-scout | Not written to 虚拟VC运行台*