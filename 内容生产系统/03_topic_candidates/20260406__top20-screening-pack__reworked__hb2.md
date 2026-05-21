# Top20 初筛包（返工版 HB2 — 市场内容心跳收束）

- `date`: `2026-04-06`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-04-06 15:50:00 CST`
- `source_scope`: `T-1 17:00 ~ T 14:30`
- `total_candidates_seen`: `40 source packets + 21 capture summaries + 1 asset chain`
- `top20_count`: `20`
- `delivery_lane`: `day_mainline`
- `pack_type`: `__reworked`
- `rework_round`: `HB2（市场内容-Top20心跳收束窗）`
- `predecessor_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260406__top20-screening-pack__reworked.md`
- `scorecard_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260406__top20__stage-gate-scorecard.md`
- `evidence_supplement`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260406__top20_rework_evidence_supplement.md`
- `manifest_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260406__market-source-manifest.md`

---

## ⚠️ 返工声明

- **本包不得自判"已过线 / 可进入下一工序"**；是否放行由 `market-editor` 最新 scorecard 决定
- **本包性质**：HB2 心跳收束包，仅记录返工补证进展，不重写完整 Top20 列表
- **补位说明**：本轮评估 14:30 前 manifest 新增条目，未发现需补入 Top20 的强信号
- **rework_mode 执行记录**：严格按 scorecard 裁定顺序：supplement_evidence 先 → rewrite_angle 次 → expand_validation 次 → replace_topic 仅在 fatal、失真或已过时时触发

---

## HB2 返工动作记录

| # | 对象 | 原问题 | 返工动作 | HB2 结论 |
|---|---|---|---|---|
| #6 | Linux 内核维护者 | P2-B：10份/天 仅量子位来源 | expand_validation | ✅ **补证完成**：Greg KH 本人直接引述"5-10 per day"，一手锚点已确立 |
| #1 | Gemma 4 iPhone | P2-A：App Store 荷兰区链接 | supplement_evidence | ✅ **核实完成**：NL 链接自动重定向 US/global，App ID 6749645337 为全球版 |
| #14 | 黄仁勋访谈 | P1-A fatal：零原始链接 | supplement_evidence | ❌ **无法补证**：维持 HOLD |
| #16 | Claude 4小时 | partial capture | supplement_evidence | ⏳ **待 content-writer 深抓**：超出 market-scout 补证范围 |
| #19 | AI记忆年轻人 | partial capture | supplement_evidence | ⏳ **待 content-writer 深抓**：超出 market-scout 补证范围 |
| #10 | OpenAI 土豆 | rewrite_angle 执行 | rewrite_angle | ℹ️ **已在上一返工包执行**，正文需 content-writer 严格按角度约束写作 |
| #12 | Copilot ToS | rewrite_angle 执行 | rewrite_angle | ℹ️ **已在上一返工包执行**，正文需 content-writer 严格按角度约束写作 |
| #17 | DeepSeek 审查 | rewrite_angle 执行 | rewrite_angle | ℹ️ **已在上一返工包执行**，正文需 content-writer 严格按角度约束写作 |
| 补位 | 14:30 前新强信号 | — | — | ✅ **评估完成**：manifest 内 14:14 Real-time AI audio/video 已在上一包替换 #18；12:18 知乎 Karpathy 知识库 评估后决定不补入（见下方） |

---

## #6 补证详情（expand_validation 完成）

### 一手锚点确认

| 层级 | 来源 | URL | 关键引述 |
|---|---|---|---|
| **Greg KH 本人直接引述** | The Register | `https://www.theregister.com/2026/03/26/greg_kroahhartman_ai_kernel/` | "volume of reports to the kernel security list had skyrocketed from **two or three per week a couple of years ago** to **five to ten per day**" |
| HN 社区验证 | Hacker News | `https://news.ycombinator.com/item?id=47547849`（60pts，2026-03-28 前后） | 标题："AI bug reports went from junk to legit overnight, says Linux kernel czar" |
| 社区持续讨论 | Reddit r/singularity / r/LinuxUncensored | 多帖 | "Linux kernel developers are receiving record-high AI bug reports" |

### 给 content-writer 的引用指引

- **可直接引用**：Greg KH "five to ten per day" 原话，附 The Register 链接
- **量子位定位**：中文传播层，置信度由"需补一手"升级为"有据可查"
- **降引用风险**：已消除，补证完成

### evidence_supplement 路径

`/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260406__top20_rework_evidence_supplement.md`

---

## #1 App Store 链接核实（supplement_evidence 完成）

### 链接验证结果

| 测试 | URL | 结果 |
|---|---|---|
| 荷兰区（HN 原始链接） | `https://apps.apple.com/nl/app/google-ai-edge-gallery/id6749645337` | ✅ 重定向至 US/global |
| 全球推荐格式 | `https://apps.apple.com/us/app/google-ai-edge-gallery/id6749645337` | ✅ App 存在，直接可访问 |
| 错误 ID（曾被建议为替代） | `https://apps.apple.com/app/google-ai-edge-gallery/id6749645335` | ❌ 404 Not Found |

### App 信息确认

- **App 名称**：Google AI Edge Gallery
- **App ID**：`id6749645337`（正确）
- **开发者**：Google LLC
- **描述**："Private, Fast, Offline AI / Only for iPhone / Free"
- ** tagline**：运行全球最强大开源 LLM 的首选平台

### 结论

scorecard 中"荷兰区链接"描述不准确：NL 链接自动重定向至美国区，实际即为全球可访问链接。建议写作时使用明确格式：`https://apps.apple.com/us/app/google-ai-edge-gallery/id6749645337`

---

## 14:30 前新候选评估

### 评估对象：知乎 Karpathy 个人知识库（12:18 CST）

- **manifest 路径**：`/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260406_121837__zhihu_hot_ai_karpathy__source-packet.md`
- **时间窗口**：✅ 在 14:30 前
- **平台**：知乎热榜（中文传播层，非一手）
- **内容**：如何评价 Karpathy 提出的个人知识库架构

**评估结论：不补入 Top20**

理由：
1. 知乎条目为"如何评价..."讨论帖，非 Karpathy 原始帖；一手性需追溯 Karpathy 博客/推文
2. 无同步 HN/Reddit 英文圈讨论，信号跨平台传播性不足
3. 当前 Top20 以 Gemma 4 簇为主叙事，补入 Karpathy 会分散核心主线
4. 可保留在明日候选观察池

### 评估对象：Real-time AI audio/video on M3 Pro + Gemma E2B（14:14 CST）

已在上一返工包（2026-04-06 15:10）替换原 #18 Per-Layer Embeddings，本轮维持不变。

---

## 仍需下游工序处置的项目

以下项目在本包中仍为 **pending 状态**，超出 market-scout 补证能力，需在平台任务单中标注由 content-writer 处置：

| # | 对象 | 待处置 | 具体要求 |
|---|---|---|---|
| #14 | 黄仁勋访谈 | 维持 HOLD | 补原始访谈链接才可申请复评 |
| #16 | Claude 4小时血洗最安全系统 | 深抓全文 | content-writer 需补原始 36kr/量子位 文章全文链接 |
| #19 | AI记忆年轻人 | 深抓全文 | content-writer 需确认产品名/团队/项目链接 |
| #10 | OpenAI 土豆 | 严格按角度写作 | 稿内不得出现"已确认 Sora 弃子"，需执行"迷雾：代号猜测"角度约束 |
| #12 | Copilot ToS | 严格按角度写作 | 不得以"今日曝光"为钩子，改为"旧ToS引发新争议" |
| #17 | DeepSeek 审查 | 严格按角度写作 | 正文需写"DeepSeek 官方截至发稿未回应"，不得以"已确认审查"呈现 |
| #18' | Real-time AI 多模态 | 补 Reddit 热度数 | Reddit score/comment_count 被 403 遮挡，writer 引用时注明"热度待核实" |

---

## 返工后评分预估调整

> ⚠️ 以下为 market-scout 自评，不等于 scorecard 裁定

| # | 对象 | HB2 后评分变化 | 理由 |
|---|---|---|---|
| #6 | Linux 内核维护者 | 20→21/27 | expand_validation 完成，一手锚点确立，数据硬度提升 |
| #1 | Gemma 4 iPhone | 维持 22/27 | App Store 全球链接确认，risks 消除一项 |

---

## morning_flash 排除确认

- ✅ 已确认 manifest 中无任何 source_packet 来自 `morning_flash` 车道
- ✅ 本包 Top20 对象无与已发布/已交付 morning_flash 题重复
- ✅ 无 14:30 后新条目被补入

---

## 交付约束

- **不得自行放行**：本包为 market-scout HB2 心跳收束返工包，是否进入下一工序由 market-editor 最新 scorecard 决定
- **补证范围**：仅覆盖 scorecard 指出的可补强项；HOLD / 深抓级需求已在平台任务单标注
- **不越权**：不把 content-writer / redteam / market-editor 职责纳入本包

---

*market-scout｜2026-04-06 15:50 CST｜day_mainline HB2 heartbeat*
*runtime: market-scout | isolation: 与虚拟VC研究线隔离*
