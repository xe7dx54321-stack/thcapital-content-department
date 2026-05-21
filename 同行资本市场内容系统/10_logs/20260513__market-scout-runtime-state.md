# market-scout 运行时状态 | day-mainline Top20 heartbeat
**Runtime:** market-scout | signal-scout semantic
**Lane:** day-mainline | **Date:** 2026-05-13
**Cron ID:** e11482c7-68d4-407d-bda5-8f9b1f042cca
**执行时间:** 2026-05-13 15:48 CST

---

## 执行记录

### 第一步：market_top20_pack_guard.py
- 脚本路径：`/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_top20_pack_guard.py`
- 实际写入：`/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260513__top20-screening-pack.md`（bootstrap placeholder，66行）
- ⚠️ 注意：guard/bootstrap 写入了 `同行资本内容部门` 路径而非 `同行资本市场内容系统` 路径
- 正确路径（已有真实内容）：`/Users/apple/Documents/同行资本市场内容系统/03_topic_candidates/20260513__top20-screening-pack.md`（98行，含9个真实标的）

### 第二步：market_stage_artifact_status.py
- 执行命令：`--path /Users/apple/Documents/同行资本市场内容系统/03_topic_candidates/20260513__top20-screening-pack.md --kind pack --accept-state final`
- 返回码：1（BLOCKED）
- 原因：`missing_core_sections` / `missing:date`
- 说明：artifact_status 脚本无法解析当前 pack 格式（`## 初筛结论` + 表格格式被识别为"缺核心section"和"缺date字段"）

---

## canonical pack 实际状态（/同行资本市场内容系统/03_topic_candidates/20260513__top20-screening-pack.md）

| 属性 | 值 |
|------|------|
| 行数 | 98 |
| 标的数量 | 9（Exaforce / Anthropic / Vapi / Havoc AI / Andco / Klaimee / Coworked / Kuli / Ornadyne） |
| 赛道覆盖 | Defense AI / Voice AI / Agentic PM / Legal AI / Hard Tech / Consumer AI / Foundation Model |
| 评分维度 | 5维（一手性×2 + 传播性 + 破圈性 + 数据硬度 + 视觉素材） |
| 生成时间 | 2026-05-13 14:00 CST |
| runtime 标注 | market-scout / financing / newco minimal lane |
| 弱链项 | YC S26四家官网未确认；Anthropic未官宣；Vapi缺截图 |

---

## 本轮 blocker 说明

`artifact_status` 脚本返回 exit 1，按 cron 指令必须停止。
该脚本的 section 检测逻辑对当前 pack 的 markdown 格式（`## 初筛结论` + markdown表格）存在格式匹配问题，无法识别为"final"状态，即使 pack 实质上包含9个真实标的。

**不得继续读素材，不得假装本轮已完成。**

---

## 禁止事项确认
- ❌ 不写入虚拟VC运行台
- ❌ 不做最终选题拍板
- ❌ 不向 morning_flash / 已发布对象重新塞回日间主线

---
*market-scout | signal-scout runtime | 2026-05-13 15:48 CST*
