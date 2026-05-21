# 红队评审 — 平台任务单
**Runtime:** redteam-reviewer | **Date:** 2026-05-13（周三）| **Heartbeat:** day_mainline 续脉
**任务单:** `03_topic_candidates/20260513__platform-task-sheet.md`
**上游:** `03_topic_candidates/20260513__daily-top8-to-top5.md`（final，19:11 CST）
**stage_gate_status:** `continuity_only` | **任务单生成时间:** 19:14 CST
**验真状态:** ⚠️ `market_stage_artifact_status.py` 脚本不存在；本评审以人工文件审读代替

---

## ⚠️ 阻塞级问题（BLOCKERS — 不得发布前解决）

### 🔴 B-1: Isomorphic Labs 投资方描述错误已跨三个文件污染

**链路：**
- `financing-newco.md`（上游筛选包）→ 写入 `Alphabet/GV/CapitalG/MGX/Temasek/CapitalG`
- `20260513__daily-top8-to-top5.md`（Top5 board）→ 复制同样错误并声明 B-1 修正需求
- `platform-task-sheet.md` Slot X-1 → 再次复制错误并标注 B-1 未完成

**问题本质：** "Alphabet" 本身不是 Isomorphic Labs 的直接投资者；GV（Google Ventures）和 CapitalG（Google Capital）是 Alphabet 旗下独立基金，B-1 修正是将 `Alphabet/GV/CapitalG` 改为 `GV/CapitalG（Alphabet 旗下）`。

**为什么是 BLOCKER：** Slot X-1 的"核心论点"直接写入投资方 logo 墙推荐；若 content-writer 按当前任务单写稿，错误的投资方归因会进入发布内容，违反信源准确性纪律。

**当前任务单处理：** 仅标注"⚠️ B-1 修正未完成—发布前需确认"，但没有给出修复路径，也没有说明谁负责执行。

**红队要求：** signal-scout 修复 financing-newco.md 投资方字段 → Top5 board 重评 Isomorphic Labs 评分 → task sheet 更新 Slot X-1 投资方描述。三步缺一不可，且 task sheet 需在 B-1 落地前将 Isomorphic Labs 降为"待发布"状态。

---

## 🔴 source_ref_bundle 质量问题

**问题：** 任务单声明 `source_ref_bundle` 锚点（如"官方公告 + builder 圈共振"、"TechCrunch 来源"），但实际检查发现：

- `market_stage_artifact_status.py` 脚本 **不存在**于 `09_runbooks/scripts/`，意味着无法通过脚本验证任何 artifact 的状态
- 任务单自己承认："⚠️ artifact_status 验真脚本不存在；本单以上游 Top5 board final 为前提"

**影响：** 所有 source_ref 均为叙事性声明，无脚本验证回路。这是系统层级的 `source_ref_bundle` 缺失，不是单个标的的问题。

**建议：** market-editor 记录此系统债务，优先补全验真脚本；若本轮无法补全，需在任务单加注"source_ref 待 content-writer 发布前自行验证"。

---

## 🟡 平台错配 / 浪费问题

### 🟠 XHS × Bilibili 同一事件：差异化不足，平台浪费

**现状：**
| 平台 | Slot | 标的 | 切入角度 | 证据抓手 |
|------|------|------|---------|---------|
| Xiaohongshu | XHS-1 | Anthropic × SpaceX | 史上最大算力集群：一张图读懂 Colossus 1 | SpaceX官方 / TechCrunch / 量子位 |
| Bilibili | BILI-1 | Anthropic × SpaceX | 算力即权力：为什么这个算力集群改变AI游戏规则 | 同上（220,000+ GPU） |

**核心问题：** 两个 slot 引用完全相同的 evidence anchor（SpaceX官方 + 量子位 + TechCrunch），产出几乎相同的数据点（220,000+ GPU）。唯一的"差异化"是标题叙事风格（B站风格 vs 轻科普），但内容正文极可能高度重复。

**为什么是问题：** continuity_only 模式下只有 7 个 slot；XHS 和 BILI 各占 1 个 slot，但读者（刷到两篇相似内容的用户）会感知为内容农场重复产出。这直接伤害两个平台的粉丝粘性和算法推荐权重。

**红队建议（不要求修改任务单，只要求标注给 market-editor）：** XHS-1 和 BILI-1 至少有一个需要差异化到不同事件（例如 XHS 保留 Colossus 1，BILI 改到 NVIDIA × IREN 算力事件，或 xAI Grok 4.3 的 Oracle OCI 发布）；或者两个 slot 可以针对同一事件但做完全不同的叙事锚点（XHS 做"算力集群规模可视化对比图"驱动，BILI 做"Colossus 1 如何影响 B站 AI 创作者生态"）。

---

## 🟡 角度问题

### 🟠 WeChat W1 × W2：两个中国大模型寡头角度边界模糊

**现状：**
- W1（阶跃星辰）：切入角度 = "中国多模态基础模型格局：月之暗面之外的另一个千亿估值玩家，赛道稀缺性"
- W2（月之暗面）：切入角度 = "中国大模型商业化验证：Kimi C 端落地是估值最强支撑"

**问题：** W1 的核心论点是"阶跃与月之暗面构成双寡头格局"，但 W2 的核心论点是"Kimi 商业化验证支撑估值"。两个 slot 都把对方作为论据的一部分，但角度没有清晰区分"为什么读这篇而不是另一篇"。

**读者链路风险：** 读者读完 W1 后感觉"月之暗面也差不多这样"，读完 W2 后感觉"阶跃星辰好像也差不多"。点击率可能互相侵蚀而不是叠加。

**红队建议：** 任务单需要更明确的差异化指令：
- W1 重点：技术能力矩阵（多模态 benchmark 对比）+ 估值逻辑（为什么千亿不是泡沫）
- W2 重点：Kimi 产品数据（DAU/留存）+ 商业化路径（ToC vs ToB）+ 估值机构背书来源

当前 W2 的切入角度描述过于接近 W1，需要 content-writer 在写作时主动拉开。

---

## ✅ 做对的地方（正面清单）

### ✓ 无 morning_flash 冲突
今日无 `morning_flash` 文件，任务单未包含任何已锁/已发布题。红队确认无撞题。

### ✓ Holdout 解释清晰，捞回条件具体
Exaforce（H1）：需补强官网/demo 截图 + 媒体数据 → 由 market-scout 负责
AMI Labs（H2）：A-3 投资人标注污染 → signal-scout 修复后由 topic-planner 重评
OpenAI Daybreak（H3）：平台任务有富余槽位时评估，优先级低于 Exaforce

每条 holdout 都有明确的触发条件和责任 owner，没有"暂时搁置"类的模糊处理。

### ✓ Supply Gap 诚实声明
任务单声明：canonical pack 20条最高 23 分，无 ≥8 分；本次 Top5 推进依赖 lane 包 P0 标的。诚实说明了内容供给不足的现实，没有凑数。

### ✓ stage_gate_status=continuity_only 纪律遵守
WeChat 2 + 4 平台各 1 = 7 slot；未强制要求六平台覆盖，未因每个平台只保留一个 slot 而机械判错。红队认可此判断。

### ✓ B-1 风险已显式标注
Isomorphic Labs 的投资方描述问题已在 Slot X-1 显式标注"⚠️ B-1 修正未完成—发布前需确认"。虽然修正未落地（仍属 BLOCKER），但标注行为本身是正确的系统响应。

---

## 🔍 附加观察（低优先级，不影响通过/打回判定）

1. **StepFun "P0 无条件进入"说法略松：** 任务单 W1 Slot 声明"P0·无条件进入"，但红队无法在本轮验证 StepFun 的"$10B+ 估值"数据来源和"融资密度最高"的具体数字。建议 content-writer 写作前自行交叉验证。
2. **XHS-1 视觉建议"必须可视化"是对的：** 任务单明确标注"算力集群规模对比图（必须，可视化驱动）"，这对小红书平台是正确的判断。
3. **Isomorphic Labs 在 X 平台的字符限制适配：** $2.1B 的"史上最大单笔 AI 药物发现融资"叙事在 X（Twitter）平台很适合 280 字 thread 格式，角度选择合理。

---

## 📋 红队结论

| 维度 | 评级 | 核心问题 |
|------|------|---------|
| 阻塞级风险 | 🔴 2个 | B-1 污染链路未断；source_ref_bundle 验真脚本缺失 |
| 平台错配 | 🟠 1个 | XHS × BILI 同一事件差异化不足 |
| 角度设计 | 🟠 1个 | W1 × W2 边界模糊 |
| 覆盖完整性 | ✅ | continuity_only 模式下覆盖最佳业务窗标的 |
| Holdout 纪律 | ✅ | 清晰、具体、可执行 |
| Supply gap 诚实度 | ✅ | 无凑数 |
| morning_flash 隔离 | ✅ | 无冲突 |

**综合判定：** 因 B-1 BLOCKER 未解决，任务单在 Isomorphic Labs Slot X-1 维度存在信源污染风险。建议 market-editor 将 Isomorphic Labs 降为"待发布"状态，等待 signal-scout 完成 B-1 修复后重新升格；其余 6 个 slot（W1、W2、XHS-1、ZH-1、BILI-1、TT-1）可进入 content-writer 环节。

---

*redteam-reviewer | 2026-05-13 19:20 CST | day_mainline platform redteam heartbeat*
*验真脚本: market_stage_artifact_status.py 不存在（人工替代审读）*