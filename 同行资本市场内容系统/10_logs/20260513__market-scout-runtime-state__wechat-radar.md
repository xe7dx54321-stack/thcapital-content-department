# market-scout 运行时状态 | 微信公众号雷达轮
**Runtime:** market-scout | signal-scout semantic
**Lane:** 微信公众号入口轮
**执行时间:** 2026-05-13 15:25 CST
**触发方式:** cron job (market-scout runtime heartbeat)

---

## 执行情况

### 脚本问题
| 脚本 | 状态 |
|------|------|
| `market_topic_capture_round.py` | ❌ 不存在 |
| `20260325__market-topic-capture-runbook.md` | ❌ 不存在 |
| `market_wechat_rss_refresh.py` | ❌ 不存在 |

**处理方式:** Web Search intake，直接调用 Google News via Gemini 抓取10个有效 source-id 内容

---

## 交付物

### Source Packets（10个有效 + 5个弱/无效）

| source-id | 状态 | 文件 |
|-----------|------|------|
| wechat__liangziwei | ✅ | 02_topic_radar/source_packets/20260513__source__wechat__liangziwei.md |
| wechat__xinzhiyuan | ✅ | 02_topic_radar/source_packets/20260513__source__wechat__xinzhiyuan.md |
| wechat__jiqizhixin | ✅ | 02_topic_radar/source_packets/20260513__source__wechat__jiqizhixin.md |
| wechat__zhidx | ✅ | 02_topic_radar/source_packets/20260513__source__wechat__zhidx.md |
| wechat__36kr | ✅ | 02_topic_radar/source_packets/20260513__source__wechat__36kr.md |
| wechat__ifanr | ✅ | 02_topic_radar/source_packets/20260513__source__wechat__ifanr.md |
| wechat__geekpark | ✅ | 02_topic_radar/source_packets/20260513__source__wechat__geekpark.md |
| wechat__founder_park | ✅ | 02_topic_radar/source_packets/20260513__source__wechat__founder_park.md |
| wechat__appsso | ✅ | 02_topic_radar/source_packets/20260513__source__wechat__appsso.md |
| wechat__guiguang_ai_tools | ✅ | 02_topic_radar/source_packets/20260513__source__wechat__guiguang_ai_tools.md |
| wechat__guixingren_pro | ⚠️ 弱 | 02_topic_radar/source_packets/20260513__source__wechat__guixingren_pro.md |
| wechat__saibo_chanxin | ⚠️ 弱 | 02_topic_radar/source_packets/20260513__source__wechat__saibo_chanxin.md |
| wechat__digital_life_khazix | ❌ | 02_topic_radar/source_packets/20260513__source__wechat__digital_life_khazix.md |
| wechat__bingan_gege_agi | ⚠️ 弱 | 02_topic_radar/source_packets/20260513__source__wechat__bingan_gege_agi.md |
| wechat__kangaroo_ai_inn | ❌ | 02_topic_radar/source_packets/20260513__source__wechat__kangaroo_ai_inn.md |

### 清单文件
- `10_logs/20260513__market-source-manifest__wechat-radar.md`

### Top20 初筛包
- `03_topic_candidates/20260513__top20-screening-pack__wechat-radar.md`

---

## 边界遵守

- ✅ 未写入虚拟VC运行台
- ✅ 未做最终选题拍板
- ✅ 未把媒体稿当投资结论
- ✅ 只做 source intake + 初筛结构化
- ✅ 今日 market_wechat_deep_capture_round.py 已于 13:05 运行（HIGH 14条，与本轮互补）

---

## 待办项（建议后续 cron / 人工处理）

1. **高优先:** 建 `market_topic_capture_round.py`，支持 `--source-id` 参数化
2. **高优先:** 建 `market_wechat_rss_refresh.py`，对接微信公众号直连抓取
3. **中优先:** 清理/确认 5 个弱/无效 source-id
4. **中优先:** 36kr 直连问题待修复（deep_capture 部分失败）
5. **低优先:** 补充 Founder Park / AppSo 垂直社区直连方案

---

*market-scout runtime | 2026-05-13 | 微信公众号雷达轮 | 不构成投资结论*
