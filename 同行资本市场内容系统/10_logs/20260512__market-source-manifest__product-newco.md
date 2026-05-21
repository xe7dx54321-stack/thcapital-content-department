# 20260512 market-source-manifest — product / newco discovery lane
**Runtime:** market-scout | **Lane:** product / newco discovery | **Date:** 2026-05-12
**Trigger:** cron 11:12/17:12/20:12 | **Executed:** 2026-05-12 18:33 CST

---

## Source Manifest

| Source ID | Source Name | Capture Status | Output File |
|-----------|-------------|---------------|-------------|
| `trend__yc_launches_ai` | YC Launches (W26 anchor; S26 pending) | ✅ Full capture | `2026-05-12/__trend__yc_launches_ai__2026-05-12.md` |
| `web__techcrunch_ai` | TechCrunch AI Funding | ✅ Full capture | `2026-05-12/__web__techcrunch_ai__2026-05-12.md` |
| `web__finsmes_ai_gnews` | FinSMEs AI Tracker | ✅ Full capture (含今日新增) | `2026-05-12/__web__finsmes_ai_gnews__2026-05-12.md` |
| `trend__trend_hunt_ai_agents` | Trend Hunt AI Agents | ✅ Supplemental only | `2026-05-12/__trend__trend_hunt_ai_agents__2026-05-12.md` |

---

## Signal Count Summary

| Source | Total Signals | High Priority | New Today |
|--------|--------------|---------------|-----------|
| YC W26 (full list) | 30+ companies | Pocket / Hex Security / Stilta / Agentic Fabriq / Human Archive / OpenSpec | 6+ new candidates |
| TechCrunch | 8+ rounds | Sierra / Ineffable / Blitzy / Cognition / Factory / Nova / Fazeshift | 0 new today |
| FinSMEs | 10+ rounds | Robotera (>$200M) / Pillar (€12M) / Tolemy Bio (€1.4M) | 3 new today |
| Trend Hunt | 1 valid signal | Shoplazza Athena (May 12 launch) | 1 new today |
| **Total** | **50+ signals** | **15+ high priority** | **10+ new today** |

---

## Output Files

### Source Packets
- `/02_topic_radar/source_packets/2026-05-12/__trend__yc_launches_ai__2026-05-12.md`
- `/02_topic_radar/source_packets/2026-05-12/__web__techcrunch_ai__2026-05-12.md`
- `/02_topic_radar/source_packets/2026-05-12/__web__finsmes_ai_gnews__2026-05-12.md`
- `/02_topic_radar/source_packets/2026-05-12/__trend__trend_hunt_ai_agents__2026-05-12.md`

### Top20 Pack
- `/03_topic_candidates/20260512__top20-screening-pack__product-newco.md`

---

## New Signal Highlights (Today)

1. **Robotera** — >$200M人形机器人；SF Group/HSG/IDG领投；300+台已部署；欧洲扩张
2. **Pillar** — €12M seed；建筑后台AI OS；Earlybird+Base10领投
3. **Tolemy Bio** — €1.4M pre-seed；虚拟细胞AI；Cambridge+Barcelona
4. **Shoplazza Athena** — May 12发布；电商AI管理员；intent-based系统
5. **Pocket** — $27M ARR by YC W26 Demo Day；消费者硬件
6. **Hex Security** — AI主动安全测试；YC W26 standout
7. **Stilta** — AI专利研究助手；YC W26 standout

---

## Weak Chain Resolution Log

| Company | Target | Status |
|---------|--------|--------|
| Robotera | robotera.com | 🔍 需要补查 |
| Ineffable Intelligence | ineffable.ai | 🔍 需要补查 |
| RadixArk | radixark.com | 🔍 需要补查 |
| Pocket | pocket.com | 🔍 需要补查 |
| Pillar | pillar.com | 🔍 需要补查 |
| Tolemy Bio | tolemy.bio | 🔍 需要补查 |
| Hex Security | hexsecurity.ai | 🔍 需要补查 |
| Stilta | stilta.ai | 🔍 需要补查 |

---

## Lane Execution Notes

- runbook文件不存在（本计划中原定路径缺失）；实际按AGENTS.md执行手动抓取
- scripts目录只有`market_learning_memo_builder.py`和`market_wechat_deep_capture_round.py`；产品/newco专用脚本未找到
- YC S26尚未发榜（结果预期2026-06-05）；W26作为稳定锚点
- Trend Hunt仅保留单条有效信号（Athena），其余趋势描述作背景
- 未写入虚拟VC运行台；内容工厂隔离原则保持

---

*Manifest ID: 20260512__market-source-manifest__product-newco.md*
*Runtime: market-scout | Isolated from 虚拟VC研究线*