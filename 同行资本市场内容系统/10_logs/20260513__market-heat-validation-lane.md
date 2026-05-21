# 市场内容热度验证报告 | 2026-05-13（补录）
> 验证时间：2026-05-13 22:55 | Lane：heat validation
> 执行命令：market_topic_capture_round.py --source-id trend__baidu_realtime --source-id trend__zhihu_hotlist --source-id trend__feigua_bilibili --source-id trend__newrank_ai_media_rank

---

## 执行结果

| 源 | 状态 |
|----|------|
| `trend__baidu_realtime` | ❌ 脚本未注册该源 |
| `trend__zhihu_hotlist` | ❌ 脚本未注册该源 |
| `trend__feigua_bilibili` | ❌ 脚本未注册该源 |
| `trend__newrank_ai_media_rank` | ❌ 脚本未注册该源 |

**脚本实际支持源（4个）：**
- `trend__yc_launches_ai`（YC 公司标签 AI）
- `trend__trend_hunt_ai_agents`（Product Hunt AI Agents）
- `web__techcrunch_ai`（TC 自动抓取）
- `web__finsmes_ai_gnews`（FinSMEs + Google News）

本次 cron 传入的 4 个源 ID 均不在脚本注册表中，导致所有源均跳过，产出为空（0 条）。

---

## 补采：百度热搜实时抓取

直接调用 web_fetch 抓取百度实时热搜，识别 AI / agent / 机器人相关条目：

### AI / 机器人相关热搜（2026-05-13 22:55 UTC+8）

| 排名 | 热搜标题 | 信号类型 |
|------|---------|---------|
| #7 | **"9.9元送全城" 无人车大战来了** | 🚗 无人车 / robotics + 商业化大战 |

**关键信号：无人车 pricing 大战（"9.9元送全城"）进入大众热搜，说明 autonomous vehicle 商业化在破圈，而非技术圈内部讨论。**

> 来源权重：百度热搜 = 大众破圈信号，非一级事实来源。

---

## 破圈共振评估

| 层次 | 今日信号 | 评估 |
|------|---------|------|
| 大众热搜（百度） | #7 无人车 pricing 大战 | ✅ 有直接破圈 |
| 问答讨论（知乎） | 无法访问（403） | ⚠️ 待补 |
| B站科技热（飞瓜） | 脚本未注册该源 | ⚠️ 待补 |
| 微信/竞品（新榜） | 脚本未注册该源 | ⚠️ 待补 |

**结论：** 脚本注册的 4 个内置源无法覆盖本次要求的 4 个大众热度源。AI/agent/robotics 在大众层面有 1 条直接破圈信号（无人车大战），其他层次待修复脚本后补采。

---

## 下一步动作

1. **优先级高**：修复 `market_topic_capture_round.py`，将 `trend__baidu_realtime` / `trend__zhihu_hotlist` / `trend__feigua_bilibili` / `trend__newrank_ai_media_rank` 四个源注册进脚本（需要爬虫/API 集成）
2. **立即补采**：对知乎 / B 站 / 新榜手动补采，完成完整的 heat validation lane
3. **Top20**：因源注册问题，本次未产出正式 Top20 初筛包

---

*本报告所有热度源数据仅作破圈验证信号，不作为最终事实来源。*