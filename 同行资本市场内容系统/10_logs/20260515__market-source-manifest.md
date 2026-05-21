# Market Source Manifest 2026-05-15

## 执行摘要

| 项目 | 状态 |
|---|---|
| market_topic_capture_round | ✅ 完成（微信来源跳过，非微信来源正常抓取） |
| market_wechat_rss_refresh Batch A | ❌ 0/10 公众号找到文章 |
| market_wechat_deep_capture_round | ❌ 0/14 篇内容成功抓取 |
| Top20 初筛包 | ✅ 已生成，含 20 条结构化条目 |
| Learning Memo | ✅ 已生成 |

## 来源清单

### 非微信来源 ✅
| 来源文件 | 条目数 | 状态 |
|---|---|---|
| 20260515__src-trend__hn_frontpage.json | 30 | ✅ 有分 |
| 20260515__src-trend__bilibili_popular_all.json | 20 | ✅ 有分 |
| 20260515__src-trend__zhihu_hotlist.json | 20 | ✅ 有分 |
| 20260515__src-trend__baidu_realtime.json | 20 | ✅ 有分 |
| 20260515__src-web__techcrunch_ai.json | 20 | ✅ 有分 |
| 20260515__src-trend__newrank_ai_media_rank.json | — | ⚠️ 无条目 |

### 微信来源 ❌（系统性失败）
| 账号 | 公众号名 | Batch A RSS | Deep Capture |
|---|---|---|---|
| wechat__liangziwei | 量子位 | ❌ 0篇 | ❌ 失败 |
| wechat__xinzhiyuan | 新智元 | ❌ 0篇 | ❌ 失败 |
| wechat__jiqizhixin | 机器之心 | ❌ 0篇 | ❌ 失败 |
| wechat__zhidx | 智东西 | ❌ 0篇 | ❌ 失败 |
| wechat__36kr | 36氪 | ❌ 0篇 | ❌ 失败 |
| wechat__ifanr | 爱范儿 | ❌ 0篇 | ❌ 失败 |
| wechat__geekpark | 极客公园 | ❌ 0篇 | ❌ 失败 |
| wechat__founder_park | Founder Park | ❌ 0篇 | 未测 |
| wechat__appsso | AppSo | ❌ 0篇 | 未测 |
| wechat__guiguang_ai_tools | 硅星人 | ❌ 0篇 | 未测 |
| wechat__guixingren_pro | 硅谷好人Pro | 未测 | 未测 |
| wechat__saibo_chanxin | 赛博信新 | 未测 | 未测 |
| wechat__digital_life_khazix | Digital Life Khazix | 未测 | 未测 |
| wechat__bingan_gege_agi | 冰岩AI | 未测 | 未测 |
| wechat__kangaroo_ai_inn | Kangaroo AI Inn | 未测 | 未测 |

## Top20 评分分布
- HIGH: 4（Anthropic融资、DeepSeek融资、阶跃星辰融资、Claude Code）
- MEDIUM: 9（百度文心5.1、苹果AirPods H90、无屏手环AI、OpenAI Codex移动端等）
- LOW: 7

## 关键发现
- 微信入口系统性阻塞：所有 Batch A 账号 RSS 返回 0 篇，Deep Capture 14篇全部失败
- HN 提供最高质量信号：85分帖、大量 developer discussion
- 科技媒体（36氪/机器之心/智东西）融资新闻标签有效但正文无法抓取
- 中国 AI 公司大额融资（DeepSeek 73亿美元、阶跃星辰 170亿人民币）进入 HIGH

## 输出文件
- Top20 包: `03_topic_candidates/20260515__top20-screening-pack.md`
- Learning Memo: `11_frontstage/20260515__head-media-learning-memo.md`
- 日志: `10_logs/20260515__wechat-rss-refresh__batch-a.log`