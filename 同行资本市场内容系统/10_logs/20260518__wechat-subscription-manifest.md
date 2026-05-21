# 微信订阅巡检记录 | 2026-05-18 20:22 CST

## 任务说明
- 任务类型：微信订阅池 bootstrap/巡检（cron 触发 19:10）
- 执行脚本：`market_wechat_rss_refresh.py --batch a --write-log` + `--batch b --write-log`
- 目的：确保内容工厂微信 RSS 订阅池保持齐全；只补订阅，不做 capture-layer 消费
- 边界：不写 topic_candidate / draft，不写入虚拟vc运行台

---

## Batch A 执行结果（强链主账号）

| 账号 | 状态 | 文章数 | 备注 |
|------|------|--------|------|
| 量子位 | no_articles | 0 | Jina search 未抓到当日文章 |
| 新智元 | no_articles | 0 | Jina search 未抓到当日文章 |
| 机器之心 | no_articles | 0 | Jina search 未抓到当日文章 |
| 智东西 | no_articles | 0 | Jina search 未抓到当日文章 |
| 36氪 | no_articles | 0 | Jina search 未抓到当日文章 |
| 爱范儿 | no_articles | 0 | Jina search 未抓到当日文章 |
| 极客公园 | no_articles | 0 | Jina search 未抓到当日文章 |
| Founder Park | no_articles | 0 | Jina search 未抓到当日文章 |
| AppSo | no_articles | 0 | Jina search 未抓到当日文章 |
| 硅星人 | no_articles | 0 | Jina search 未抓到当日文章 |

**Batch A 结果：0/10 账号找到文章 | 0 篇总文章**

---

## Batch B 执行结果（弱/无效账号补轮）

| 账号 | 状态 | 文章数 | 备注 |
|------|------|--------|------|
| 硅谷好人Pro | no_articles | 0 | Jina search 未抓到当日文章 |
| 赛博信新 | no_articles | 0 | Jina search 未抓到当日文章 |
| Digital Life Khazix | no_articles | 0 | Jina search 未抓到当日文章 |
| 冰岩AI | no_articles | 0 | Jina search 未抓到当日文章 |
| Kangaroo AI Inn | no_articles | 0 | Jina search 未抓到当日文章 |

**Batch B 结果：0/5 账号找到文章 | 0 篇总文章**

---

## 综合分析

**当日抓取率：0/15 账号（0 篇文章）**

可能原因：
1. 晚间 20:22 已过微信公众号发布高峰时段（早晨 8-10 点），Jina search 对微信内容索引存在延迟
2. 晚间时段搜索引擎对微信公众平台内容索引质量进一步降低
3. 此模式与近期 cron 日志一致（Jina search 白天已表现不佳，晚间更甚）

**订阅池完整性：**
- 15/15 个账号 source packet 均已写盘（`02_topic_radar/source_packets/20260518__source__wechat__*.md`）
- 订阅池 15 个账号全部在册，盘面完整
- 边界控制正常：未触发 capture-layer、未写 topic_candidate/draft、未写入虚拟vc运行台

**结论：**
✅ 订阅池 15 个账号全部在册，盘面完整
✅ source packet 写盘正常
✅ 边界控制正常
⚠️ 当日抓取率为 0（Jina search 对微信内容索引质量在傍晚/夜间持续偏低，建议关注早晨时段的抓取效果）

---
market-scout runtime | 微信订阅池 bootstrap | 2026-05-18 20:22 CST