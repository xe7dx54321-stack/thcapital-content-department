# 平台任务单

- `date`: `2026-04-11`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-11 18:47 CST`
- `input_top5_board`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260411__daily-top8-to-top5.md`
- `input_scorecard`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260411__top20__stage-gate-scorecard.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `continuity_only limited task sheet — wechat 2 主槽位 + 最多 2 个平台各 1 个 active slot；其余候选进入 Holdout`
- `morning_flash_exclusion_check`: `无 morning_flash 冲突对象`

---

## 全局主池 Top6（来自 Top5 Board + Holdout，追溯可查）

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|---|---|---|---|---|
| 1 | `hn_frontpage_47717587_openai_backs_illinois_bill` | OpenAI 反对伊利诺伊州 AI 责任法案 | 高热事件 + 政策信号 + Agent 开发者影响；赛道契合 AI/一人公司主线 | partial source；正文必须先补 Wired 原文关键引语截图 |
| 2 | `hn_frontpage_47722096_molotov_cocktail_hurled_at_sam_altman` | 有人向 Sam Altman 住所投掷燃烧瓶 | 高热事件 + 创始人安全叙事 + 行业情绪放大器 | partial source；正文必须先补 NYT 原文关键引语截图 |
| 3 | `rowboatlabs_rowboat` | GitHub trending 开源 Agent 框架 | 高热扩散 + 开发者工具赛道 + 解决团队协作痛点 | partial source；需补 README 产品定位 + GitHub 截图 |
| 4 | `multica_ai_multica` | GitHub trending Agent 协作工具 | 中高热 + 赛道契合 + 差异化定位"TURN CODING AGENTS INTO REAL TEAMMATES" | partial source；需补 README 首句 + 截图 |
| 5 | `glm_5_1_code_arena` | GLM 5.1 在 Code Arena 开源模型排名登顶 | 中高热 + 开源模型竞争格局 + 赛道契合 | Reddit 一手性弱；正文必须先补 Code Arena 原始结果链接 |
| 6 | `mythos_openai_researcher_anthropic_roommate` | OpenAI 研究员称其 Anthropic 前室友对 Mythos"上头" | 高热 Reddit 扩散 + Mythos SWE-bench 93.9% 硬数据 + 赛道契合 | Reddit 一手性弱；需补 Mythos 官方 benchmark 来源 |

**额外 Holdout 候选：**
| topic_key | 说明 |
|---|---|
| `founder_park_3_18_agent` | 中文 wechat 源 Founder Park 月度 Agent 推荐盘；赛道契合 |
| `openai_working_with_files` | OpenAI Academy 一手源；无需额外补证即可 publish-ready；赛道契合 |

---

---

## 三个最重要平台任务单（continuity_only limited — wechat 2 + xiaohongshu/zhihu 各 1）

## 六个主战场任务单

### `wechat`

#### Task 1 — 主稿（Active Slot 1）
- `topic_key`: `hn_frontpage_47717587_openai_backs_illinois_bill`
- `题目`: `OpenAI 为什么要力推这个法案？它可能是最懂"AI 开发者"诉求的一次政策试探`
- `目标读者`: `AI 开发者、独立 builder、关注 AI 政策环境的硬核受众`
- `切入角度`: `从法案具体条款出发，解释为什么这个"免责边界"对 Agent 经济有直接影响`
- `核心论点`: `① 法案核心是让 AI 实验室对"模型自身行为"免责，而非对使用结果免责；② 这对依赖 AI 能力构建产品的 builder 来说是一把双刃剑；③ 政策信号背后是 AI 行业对监管边界的主动试探`
- `证据抓手`: `Wired 报道原文关键引语 + HN 社区讨论高赞观点 + 法案文本摘要`
- `source_ref_bundle`: 
  - Wired 原文（archive.ph 反查）
  - HN thread: `https://news.ycombinator.com/item?id=47717587`
  - 法案原文摘要
- `视觉建议`: `时间轴：法案提出 → OpenAI 表态 → 社区反应 → 潜在影响；信息图：免责边界 vs 使用责任对比`
- `为什么适合该平台`: `微信适合承载深度政策解读 + 开发者视角的完整叙事，一文讲清来龙去脉与实质影响`

#### Task 2 — 主稿（Active Slot 2）
- `topic_key`: `hn_frontpage_47722096_molotov_cocktail_hurled_at_sam_altman`
- `题目`: `Sam Altman 住所遭袭击：这不是八卦，是 AI 行业恐惧情绪的一次集中投射`
- `目标读者`: `AI 行业从业者、关注科技公司创始人安全的受众`
- `切入角度`: `从事件本身延伸到 AI 行业从业者面临的安全风险与社会压力`
- `核心论点`: `① 事件本身是高热新闻，但真正值得看的是它折射出的行业焦虑；② AI 行业高速扩张带来的社会摩擦正在加剧；③ 这对行业声誉和从业者心态的长期影响`
- `证据抓手`: `NYT 报道原文关键引语 + 安全事件背景 + 科技领袖风险案例`
- `source_ref_bundle`:
  - NYT 原文（archive.ph 反查）
  - HN thread: `https://news.ycombinator.com/item?id=47722096`
  - 延伸：科技领袖遇袭事件背景
- `视觉建议`: `事件还原时间轴 + 科技领袖安全风险图谱 + 行业扩张与社会摩擦关系图`
- `为什么适合该平台`: `微信适合深度解读安全事件背后的行业情绪与长期影响，完整叙事而非快讯`

---

### `xiaohongshu`

#### Task 1（Active Slot 1）
- `topic_key`: `mythos_openai_researcher_anthropic_roommate`
- `题目`: `OpenAI 员工为什么会对 Anthropic 的"前室友"产品这么上头？`
- `目标读者`: `关注 AI 工具和 Agent 产品的年轻从业者、科技爱好者`
- `切入角度`: `从 Reddit 热帖的八卦感出发，引出 Mythos 的硬核技术数据`
- `核心论点`: `① 八卦背后有硬数据：ays Mythos SWE-bench 93.9%、Terminal-Bench 82%；② 为什么一个"前室友"做的产品能让 OpenAI 研究员"上头"；③ 这折射出 Agent 工具赛道竞争有多激烈`
- `证据抓手`: `Mythos SWE-bench 93.9%、Terminal-Bench 82% 原始来源 + Code Arena 对比数据 + Reddit 热帖截图`
- `source_ref_bundle`:
  - Reddit thread: `https://old.reddit.com/r/ClaudeAI/comments/1shs4ej/`
  - Mythos benchmark 数据（待 content-writer 补充官方来源）
- `视觉建议`: `工具对比图：Mythos vs 同赛道竞品 benchmark；小剧场式截图展示 Reddit 热帖；SWR/终端场景示意`
- `为什么适合该平台`: `小红书适合八卦感 + 硬数据混合叙事，用"为什么上头"这个钩子带出技术内容`

---

### `zhihu`

#### Task 1（Active Slot 1）
- `topic_key`: `openai_working_with_files`
- `题目`: `ChatGPT 文件处理能力升级意味着什么？从工程实现看 AI 工具化趋势`
- `目标读者`: `关注 AI 工程能力、AI 应用开发的技术受众`
- `切入角度`: `从 OpenAI Academy 原文的一手信息出发，分析文件处理能力背后的技术路径`
- `核心论点`: `① ChatGPT working with files 功能从工程上是 Agent 能力的基础模块；② 这类工具化能力正在成为 AI 平台的标配竞争点；③ 对 builder 来说这意味着什么`
- `证据抓手`: `OpenAI Academy 一手源原文 + 功能说明`
- `source_ref_bundle`:
  - OpenAI Academy: `https://openai.com/academy/working-with-files`
- `视觉建议`: `功能演示截图 + ChatGPT Agent 工具链图示`
- `为什么适合该平台`: `知乎适合技术向分析，需要有工程视角的展开和讨论空间`

---

### `x`

#### 今日无 Active Slot
- **说明**：x 平台适合快讯和观点钩子，但本轮 continuity_only 候选以 wechat 深度稿为主，知乎已承接技术分析；x 平台可由 content-writer 根据 wechat 草稿截取观点钩子发布，无需独立主槽位
- **候选池（Holdout）**：rowboat、multica、GLM 5.1 均可供 x 快讯使用

---

### `bilibili`

#### 今日无 Active Slot
- **说明**：bilibili 适合视频化叙事，本轮 continuity_only 候选均无视频素材储备，强行开槽会导致内容空洞
- **候选池（Holdout）**：若 rowboat 或 multica 后续有 demo/gif 截图到位，可优先考虑 bilibili 视频化

---

### `toutiao`

#### 今日无 Active Slot
- **说明**：toutiao 依赖推荐算法分发，本轮候选偏开发者 / 深度用户，与头条泛受众匹配度有限
- **候选池（Holdout）**：GLM 5.1 若有强国产 AI 话题性，可优先考虑 toutiao

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: **否**
- `理由`: `本轮 continuity_only 候选均为事件性 / 新闻性内容，非科普型长尾 SEO 题；百度 SEO 镜像层更适合拆解本轮 wechat 草稿的已发布内容，而非并行独立生产`
- `承接哪篇主稿更优`: `OpenAI backs Illinois bill 一文政策解读深度足够，可拆解为"AI 开发者必知的政策边界"系列 SEO 文，在 baijiahao 以结构化 FAQ 形式发布`

---

## Holdout 清单

### `rowboatlabs_rowboat`
- **为什么能进最终池**: GitHub trending，扩散热度高，赛道契合 AI/Agent 主线，与一行代码 start 经济高度相关
- **为什么这轮没选**: partial source；本轮 wechat 2 槽位已被 Illinois bill 和 Sam Altman 占据；知乎已承接技术分析，无多余平台槽位；x/bilibili/toutiao 本轮均无独立 Active Slot
- **什么时候可捞回**: ① signal-scout 补齐 README 产品定位 + GitHub 截图后；② 若 wechat Task 1 或 Task 2 补证失败或撞期；③ 优先进入次日 wechat 或 bilibili 槽位

### `multica_ai_multica`
- **为什么能进最终池**: GitHub trending，差异化定位"TURN CODING AGENTS INTO REAL TEAMMATES"，赛道契合度高
- **为什么这轮没选**: 同 rowboat；本轮平台槽位已用尽；与 rowboat 存在赛道重叠，优先保 rowboat（更高热）
- **什么时候可捞回**: ① signal-scout 补齐 README 首句定位 + fluidcad.io 截图后；② 若 rowboat 补证失败或展开不足；③ 优先进入 x 快讯或 bilibili

### `glm_5_1_code_arena`
- **为什么能进最终池**: 开源模型竞争格局清晰，Code Arena 排名有量化指标，赛道契合
- **为什么这轮没选**: Reddit 一手性弱；scorecard 明确 holdout；本轮无头条受众匹配槽位；需补 Code Arena 原始链接方可 publish-ready
- **什么时候可捞回**: signal-scout 找到 Code Arena 原始结果页面或 GLM 官方发布后，优先进入 toutiao（国产 AI 相关性）或 wechat 补位

### `founder_park_3_18_agent`
- **为什么能进最终池**: 中文一手源，赛道高度契合，月度 Agent 推荐盘点有收藏价值
- **为什么这轮没选**: 中文内容与小红书匹配度高，但本轮 xiaohongshu 槽位已给 Mythos（赛道更热）；wechat 2 槽位已满；zhihu 技术分析槽位已给 OpenAI working with files
- **什么时候可捞回**: 若 Mythos 补证失败或 wechat 有空余槽位，可直接替换；或次日 xiaohongshu 主槽位

---

*topic-planner | 2026-04-11 18:47 CST*
*stage_gate_status: continuity_only — limited task sheet*
*上游 scorecard: rework（7/10）— top20_mini_slate；Top5 board: final + continuity_only*
*所有 Active Slot 均可追溯至 20260411__daily-top8-to-top5.md Top5/Holdout 候选池*
