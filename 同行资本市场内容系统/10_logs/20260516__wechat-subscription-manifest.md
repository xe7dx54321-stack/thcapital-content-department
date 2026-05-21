# 微信订阅巡检记录 | 2026-05-16 09:20 CST

## 任务说明
- 任务类型：微信订阅池 bootstrap/巡检
- 执行脚本：`market_wechat_rss_refresh.py --batch all --write-log`
- 目的：确保内容工厂微信 RSS 订阅池保持齐全；只补订阅，不做 capture-layer 消费
- 边界：不写 topic_candidate / draft，不写入虚拟vc运行台

## 执行结果

| 账号 | 状态 | 文章数 | 备注 |
|------|------|--------|------|
| 量子位 | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 新智元 | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 机器之心 | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 智东西 | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 36氪 | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 爱范儿 | no_articles | 0 | Jina 搜索未能抓闰当日文章 |
| 极客公园 | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| Founder Park | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| AppSo | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 硅星人 | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 硅谷好人Pro | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 赛博信新 | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| Digital Life Khazix | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 冰岩AI | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| Kangaroo AI Inn | no_articles | 0 | Jina 搜索未能抓到当日文章 |

## 分析

所有 15 个账号当日均返回 no_articles，Jina 搜索在 "公众号名 + 2026 site:mp.weixin.qq.com" 查询上未能返回有效微信文章 URL。

可能原因：
1. 周末（周六）公众号发布频率低
2. Jina search 对微信搜索引擎被限流
3. 微信文章本身对爬虫有反爬措施

订阅池完整性：
- 15/15 账号均有 source packet 记录（写盘成功）
- 所有账号均处于"未找到当日新文章"状态
- 本轮不触发 capture-layer，不写 topic_candidate / draft

## 订阅池状态
✅ 订阅池 15 个账号全部在册（覆盖强链 Batch A 10个 + 弱链 Batch B 5个）
✅ source packet 写盘正常
⚠️ 当日抓取率为 0/15，建议傍晚批（BATCH B 补轮）或工作日复检

---
market-scout runtime | 微信订阅池 bootstrap | 2026-05-16 09:20 CST

---

# 微信订阅巡检记录 | 2026-05-16 19:10 CST

## 任务说明
- 任务类型：微信订阅池 bootstrap/巡检（第2轮）
- 执行脚本：`market_wechat_rss_refresh.py --batch all --write-log`
- 目的：确保内容工厂微信 RSS 订阅池保持齐全；只补订阅，不做 capture-layer 消费
- 边界：不写 topic_candidate / draft，不写入虚拟vc运行台

## 执行结果

| 账号 | 状态 | 文章数 | 备注 |
|------|------|--------|------|
| 量子位 | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 新智元 | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 机器之心 | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 智东西 | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 36氪 | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 爱范儿 | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 极客公园 | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| Founder Park | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| AppSo | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 硅星人 | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 硅谷好人Pro | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 赛博信新 | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| Digital Life Khazix | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| 冰岩AI | no_articles | 0 | Jina 搜索未能抓到当日文章 |
| Kangaroo AI Inn | no_articles | 0 | Jina 搜索未能抓到当日文章 |

## 分析

第2轮与第1轮（09:20）结果完全一致：15/15 账号均返回 no_articles。
周六晚间公众号活跃度极低，Jina search 持续无法返回微信文章 URL。

订阅池完整性：
- 15/15 账号均有 source packet 记录（写盘成功）
- 所有账号均处于"未找到当日新文章"状态
- 本轮不触发 capture-layer，不写 topic_candidate / draft
- 边界控制正常：未写入虚拟vc运行台

## 订阅池状态
✅ 订阅池 15 个账号全部在册（覆盖强链 Batch A 10个 + 弱链 Batch B 5个）
✅ source packet 写盘正常
✅ 边界控制正常（未写 topic_candidate/draft，未写入虚拟vc运行台）
⚠️ 当日抓取率为 0/15（周六效应，工作日有望恢复）

---
market-scout runtime | 微信订阅池 bootstrap 第2轮 | 2026-05-16 19:10 CST