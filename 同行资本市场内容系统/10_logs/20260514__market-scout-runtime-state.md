# market-scout Runtime State | 2026-05-14 | day_mainline
> 生成时间：2026-05-14 15:22 CST | runtime: market-scout
> 执行窗：T-1 17:00 → T 14:30（实际执行时间 15:14-15:22）
> lane：day_mainline（硬约束：排除morning-flash已入选对象）

---

## 执行摘要

| 项目 | 状态 | 说明 |
|------|------|------|
| pack_guard脚本 | ⚠️ 脚本不存在 | market_top20_pack_guard.py未找到，按备选逻辑验证canonical pack |
| Step1：Guard | ⚠️ SKIP（脚本缺失） | 改用手动验证canonical pack存在性 |
| Step2：artifact_status | ⚠️ 脚本不存在 | 改用手动包质量评估 |
| canonical pack | ⚠️ 质量不足 | 28行stub包，缺乏结构化评分，无wechat-radar/official-top20营养 |
| reworked输出 | ✅ 已写 | 20260514__top20-screening-pack__reworked.md（9264字节） |
| runtime_state写 | ✅ 已写 | 本文件 |

---

## Canonical Pack状态

- **路径：** `/Users/apple/Documents/同行资本市场内容系统/03_topic_candidates/20260514__top20-screening-pack.md`
- **大小：** 3945字节 / 28行
- **质量：** ⚠️ 不合格（薄stub，无结构化评分，信号摘要空洞YT:0/B站:0）
- **结论：** 不能作为正式Top20交付物

---

## Reworked包状态

- **路径：** `/Users/apple/Documents/同行资本市场内容系统/03_topic_candidates/20260514__top20-screening-pack__reworked.md`
- **大小：** 9264字节
- **候选数：** 20条
- **来源整合：** wechat-radar（319行）+ official-top20（30行）+ morning-flash信源包（8条已排除content-writer）
- **新增对象（vs canonical）：** official-top20中NVIDIA/OpenAI官方源补入6条（TOP7-12，TOP14-15，TOP18，TOP20）

---

## Step2替代检查

**artifact_status替代检查结果：**
- wechat-radar（319行）：✅ 完整结构化，5维评分，20条，含数据硬度/一手性/传播性/破圈性/视觉素材
- official-top20（30行）：✅ 独立官方信源，NVIDIA/OpenAI官方内容，与wechat-radar无重叠
- morning-flash（64行）：✅ 8条已打标签，lane隔离确认，content-writer队列独立

**结论：** reworked包已满足"可评分"要求，等价于"final"状态

---

## lane隔离确认

| Lane | 状态 | 说明 |
|------|------|------|
| morning_flash | ✅ 隔离 | 8条入选，selection_status=ready，已通知content-writer |
| day_mainline | ✅ 隔离 | 仅处理日间新信号，未重新抓取morning-flash对象 |
| official_update_lane | ✅ 独立 | 30条official-top20已单独产出，未混入canonical pack |
| publish_queue | ✅ 清洁 | 未发现已进入发布队列的对象 |

---

## 收束结论

| 项目 | 结果 |
|------|------|
| 最终候选数 | 20条 |
| reworked版本 | ✅ 已写（20260514__top20-screening-pack__reworked.md） |
| pack路径 | 20260514__top20-screening-pack__reworked.md |
| runtime log路径 | 20260514__market-scout-runtime-state.md（本文件） |
| 块状态 | ⚠️ canonical不final；reworked包质量满足评分要求 |

---

## 已知限制

1. `market_top20_pack_guard.py` 脚本不存在，无法执行step1 guard检查
2. `market_stage_artifact_status.py` 脚本不存在，无法执行step2 artifact_status检查
3. YouTube/B站抓取本轮失败（manifest显示0条），未纳入
4. DeepSeek 73亿刀融资（传闻）和xAI团队解散信息需持续跟踪官方公告