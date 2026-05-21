# market-scout Runtime State — 2026-05-18

## 基础信息
- **runtime**: market-scout / day-mainline-top20-pack
- **执行时间**: 2026-05-18 15:04 CST
- **RUN_DATE**: 2026-05-18
- **RUN_TOKEN**: 20260518
- **业务窗**: T-1 17:00 → T 14:30（已过窗，执行正常）

## 阶段门检查
| 步骤 | 状态 | 详情 |
|---|---|---|
| top20_pack_guard.py | ✅ PASS | 产出 20260518__top20-screening-pack.md (4255 bytes) |
| artifact_status (pack=final) | ✅ PASS | EXIT_CODE=0，pack 已 final |

## Top20 包质量评估
- **canonical pack**: `/Users/apple/Documents/同行资本市场内容系统/03_topic_candidates/20260518__top20-screening-pack.md`
- **候选总数**: 20
- **最强候选**: #1 Ibogaine/PTSD (BBC Future, score=15, 新产品信号)
- **score≥5 候选数**: 6 (#1–#6)
- **score=0 候选数**: 14 (#7–#20)
- **结构性问题**: #7–#20 为 HN trending 捕获，均 score=0，市场信号偏弱

## 有限强化轮操作记录
1. **wechat 源扫描**: 全部 16 个微信源（36kr、机器之心、冰岩AI、极客公园等）当日无新文章（RSS/搜索限流）
2. **official_lane 扫描**: 官方源存在但当日数据包为空或无有效 market 信号
3. **HN front page 验证**: HN Top10 均已在 pack 中(#5 Semble、#9 GenCAD、#12 RK3562、#14 Mozilla VPN、#15 Tesla Solar、#16 VoltClock 等)，无遗漏强信号
4. **Top1 候选补读**: Ibogaine/PTSD BBC Future URL web 访问受限，无法深度补读；保留原判断
5. **替换决策**: 未触发（0 个强替换候选发现）

## 替换/重排结论
- **reworked 版本**: ❌ 未写
- **canonical pack 修改**: ❌ 未改
- **替换数**: 0（未找到 score 明显更高的新候选）

## 候选信号摘要
| 排名 | 对象 | 信号类型 | 质量 |
|---|---|---|---|
| #1 | Ibogaine/PTSD (BBC Future) | 新治疗方案 | ⭐ 强 |
| #2 | 16 bytes x86 sound | 技术 hacker | 中 |
| #3 | ThinkPad history | 品牌历史 | 低 |
| #4 | F-18 airshow crash | 新闻事件 | 低 |
| #5 | Semble code search | AI 开发者工具 | 中 |
| #6 | AI process speed essay | 观点文章 | 中 |
| #7–#20 | HN trending items | misc | 低（score=0） |

## 最终交付
- **Top20 pack**: `/Users/apple/Documents/同行资本市场内容系统/03_topic_candidates/20260518__top20-screening-pack.md` ✅ final
- **runtime log**: 本文件
- **reworked**: ❌ 无
- **pack 最终候选数**: 20（结构性问题已记录，待下轮 prompt 优化采集质量）
