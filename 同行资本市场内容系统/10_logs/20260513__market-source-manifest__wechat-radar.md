# 市场内容微信公众号雷达 — 真实文件清单
**执行时间:** 2026-05-13 15:19 CST（cron触发）
**执行方式:** Web Search（Google News via Gemini）替代不存在的 market_topic_capture_round.py
**目标lane:** 微信公众号入口轮 | 数据窗口：T日

---

## ❌ 脚本缺失报告

| 脚本 | 状态 | 备注 |
|------|------|------|
| `market_topic_capture_round.py` | ❌ 不存在 | 09_runbooks/scripts/ 目录下无此文件 |
| `20260325__market-topic-capture-runbook.md` | ❌ 不存在 | runbook目录中无此文件 |
| `market_wechat_rss_refresh.py` | ❌ 不存在 | TOOLS.md提及但实际不存在 |
| `market_wechat_deep_capture_round.py` | ✅ 存在 | 今日13:05已运行（HIGH硬编码14条） |

**改用策略:** Web Search intake，绕过缺失脚本，直接落 source packet

---

## 本轮执行记录

### source_id 执行状态

| source-id | 中文名 | 执行结果 | 硬数据质量 |
|-----------|--------|---------|-----------|
| `wechat__liangziwei` | 量子位 | ✅ 完成 | P1-P2 |
| `wechat__xinzhiyuan` | 新智元 | ✅ 完成 | P2 |
| `wechat__jiqizhixin` | 机器之心 | ✅ 完成 | P1（学术向） |
| `wechat__zhidx` | 智东西 | ✅ 完成 | P1（融资首发） |
| `wechat__36kr` | 36氪 | ✅ 完成 | P1（分析+首发） |
| `wechat__ifanr` | 爱范儿 | ✅ 完成 | P2（产品观察） |
| `wechat__geekpark` | 极客公园 | ✅ 完成 | P1（直连首发） |
| `wechat__founder_park` | Founder Park | ✅ 完成 | P2（社区内容） |
| `wechat__appsso` | AppSo | ✅ 完成 | P1-P2混合 |
| `wechat__guiguang_ai_tools` | 硅星人 | ✅ 完成 | P1（数据+首发） |
| `wechat__guixingren_pro` | 硅谷好人Pro | ⚠️ 弱 | P3（背景信息） |
| `wechat__saibo_chanxin` | 赛博信新 | ⚠️ 弱 | 无专属信号 |
| `wechat__digital_life_khazix` | Digital Life Khazix | ❌ 零信号 | 无数据 |
| `wechat__bingan_gege_agi` | 冰岩AI | ⚠️ 弱 | 无专属信号 |
| `wechat__kangaroo_ai_inn` | Kangaroo AI Inn | ❌ 零信号 | 无数据 |

**有效source-id（9/15）:** 量子位、新智元、机器之心、智东西、36氪、爱范儿、极客公园、Founder Park、AppSo、硅星人

**弱/无效source-id（6/15）:** 硅谷好人Pro、赛博信新、Digital Life Khazix、冰岩AI、Kangaroo AI Inn

---

## 今日 Source Packet 文件清单

| 文件 | 路径 |
|------|------|
| 量子位 | 02_topic_radar/source_packets/20260513__source__wechat__liangziwei.md |
| 新智元 | 02_topic_radar/source_packets/20260513__source__wechat__xinzhiyuan.md |
| 机器之心 | 02_topic_radar/source_packets/20260513__source__wechat__jiqizhixin.md |
| 智东西 | 02_topic_radar/source_packets/20260513__source__wechat__zhidx.md |
| 36氪 | 02_topic_radar/source_packets/20260513__source__wechat__36kr.md |
| 爱范儿 | 02_topic_radar/source_packets/20260513__source__wechat__ifanr.md |
| 极客公园 | 02_topic_radar/source_packets/20260513__source__wechat__geekpark.md |
| Founder Park | 02_topic_radar/source_packets/20260513__source__wechat__founder_park.md |
| AppSo | 02_topic_radar/source_packets/20260513__source__wechat__appsso.md |
| 硅星人 | 02_topic_radar/source_packets/20260513__source__wechat__guiguang_ai_tools.md |
| 硅谷好人Pro（弱） | 02_topic_radar/source_packets/20260513__source__wechat__guixingren_pro.md |
| 赛博信新（弱） | 02_topic_radar/source_packets/20260513__source__wechat__saibo_chanxin.md |
| Digital Life Khazix（无效） | 02_topic_radar/source_packets/20260513__source__wechat__digital_life_khazix.md |
| 冰岩AI（弱） | 02_topic_radar/source_packets/20260513__source__wechat__bingan_gege_agi.md |
| Kangaroo AI Inn（无效） | 02_topic_radar/source_packets/20260513__source__wechat__kangaroo_ai_inn.md |

---

## 强链 Top15 事件（可进入 Top20 初筛包）

1. 阶跃星辰 170亿人民币融资（智东西/36氪首发）
2. 月之暗面 20亿美元融资（36氪/智东西首发）
3. DeepSeek 首次外部融资 500亿元估值（⚠️传言，待核实）
4. 无问芯穹 7亿元+融资（硅星人/智东西首发）
5. 维他动力Vbot 5亿元Pre-A轮（极客公园首发）
6. Recursive Superintelligence 5亿美元（极客公园首发）
7. TML-Interaction-Small发布（量子位/新智元报道）
8. Google Android → Intelligence System（爱范儿报道）
9. 苹果AirPods H90带摄像头（爱范儿报道）
10. DeepSeek V4 Flash 2840亿参数Mac可运行（量子位报道）
11. 何恺明1.05亿参数非自回归模型（量子位报道）
12. OpenAI GPT-Realtime-2/Translate/Whisper三模型（量子位报道）
13. 快手可灵分拆融资200亿美元估值（⚠️传言）
14. 百度文心5.1发布（量子位，P1官方）
15. 智元机器人四款本体+四款大模型（新智元报道）

---

## 弱链未决项

| 未决项 | 状态 | 建议 |
|--------|------|------|
| DeepSeek 500亿融资估值 | ⚠️ P3传言，波动大 | 跟踪国家大基金/幻方官方公告 |
| 快手可灵 200亿估值 | ⚠️ P3传言 | 等待正式公告 |
| 苹果AirPods H90 | P2媒体综合 | 跟踪苹果官方发布会 |
| Anthropic 500亿美元新融资 | 前序深抓失败 | 待36kr直连修复 |
| 字节豆包付费订阅 | 前序深抓失败 | 待36kr直连修复 |

---

## 边界遵守确认

- ✅ 未写入虚拟VC运行台
- ✅ 未做最终选题拍板
- ✅ 未把媒体稿当投资结论（DeepSeek/可灵等明确标注⚠️）
- ✅ 只做了 source intake + 初筛结构化
- ✅ 今日deep_capture已运行（HIGH硬编码14条），与本轮互补

---

## 建议：脚本建设优先级

1. **高优先:** 创建 `market_topic_capture_round.py`，支持 `--source-id` 参数化抓取
2. **高优先:** 创建 `market_wechat_rss_refresh.py`，对接微信公众号RSS/BAE接口
3. **中优先:** 清理/确认 6 个弱/无效 source-id（guixingren_pro/saibo_chanxin/digital_life_khazix/bingan_gege_agi/kangaroo_ai_inn）
4. **低优先:** 补充 Founder Park / AppSo 等垂直社区的直连抓取方案

---

*market-scout runtime | 微信公众号雷达清单 | 2026-05-13 | 不构成投资结论*
