# 微信订阅巡检记录 | 2026-05-20 19:38 CST

## 任务说明
- 任务类型：微信订阅池 bootstrap/巡检（cron 触发 19:10）
- 执行脚本：`market_wechat_rss_refresh.py --batch all --write-log`
- 目的：确保内容工厂微信 RSS 订阅池保持齐全；只补订阅，不做 capture-layer 消费
- 边界：不写 topic_candidate / draft，不写入虚拟vc运行台

---

## 执行结果（全量账号）

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
| 硅谷好人Pro | no_articles | 0 | Jina search 未抓到当日文章 |
| 赛博信新 | no_articles | 0 | Jina search 未抓到当日文章 |
| Digital Life Khazix | no_articles | 0 | Jina search 未抓到当日文章 |
| 冰岩AI | no_articles | 0 | Jina search 未抓到当日文章 |
| Kangaroo AI Inn | no_articles | 0 | Jina search 未抓到当日文章 |

**当日抓取率：0/15 账号（0 篇总文章）**

---

## 订阅池完整性确认

- 15/15 个账号 source packet 全部写盘（`02_topic_radar/source_packets/20260520__source__wechat__*.md`）
- 订阅池 15 个账号全部在册，盘面完整
- 边界控制正常：未触发 capture-layer、未写 topic_candidate/draft、未写入虚拟vc运行台

---

## 已知系统性问题

Jina search 全天对微信公众号内容（`site:mp.weixin.qq.com`）收录质量系统性偏低，今日三次 cron（09:10 / 13:10 / 19:10）均返回 0 篇文章。这是工具层限制，非账号/订阅池问题。

如需改善抓取率，可考虑：
1. 评估切换至 `wechat_OG` 微信公众号阅读器或其他微信专用接口
2. 下午/傍晚时段手动触发 `market_wechat_deep_capture_round.py` 补充深抓

---

market-scout runtime | 微信订阅池 bootstrap | 2026-05-20 19:38 CST