# 平台任务单

- `date`: `2026-04-06`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-06 16:26 CST`
- `input_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260406__top20-screening-pack__reworked__hb2.md`
- `stage_gate_scorecard`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260406__top20__stage-gate-scorecard.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `Top20 scorecard 7.2/10 → continuity_only；最多覆盖 3 个最重要平台，每平台先保 1 个任务槽位，其余平台写入 Holdout`
- `continuity_decision_source`: `scorecard 明确裁定 continuity_output=top20_mini_slate，P0×3 + P1×3 + P2×6 = 有效候选 12 条`
- `wechat_draft_deadline`: `2026-04-06 19:00 CST`

---

## 全局主池 Top6（mini_slate 优先级排序）

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|---|---|---|---|---|
| 1 | `gemma-4-iphone-local-ai-20260406` | P0 / HN 440pts/Rank3 / App Store 全球可核实 | Gemma 4 周完整叙事核心锚点，iPhone 本地 LLM 可操作性强，读者收益明确 | App Store 区域描述偶有歧义，写作时用明确 global link 格式 |
| 2 | `eight-years-wanting-three-months-building-ai-20260406` | P0 / HN 635pts/Rank2 / 本窗口最强叙事体 | 8年酝酿→3月建成的时间张力极强，读者共情自然，不需要解释背景 | 原文时间戳 4/5，需在正文中注明 |
| 3 | `gemma-4-benchmark-destruction-20260406` | P0 / FoodTruckBench 硬数据 | 中国开源模型全线对比，数据硬，视觉化友好 | 需核实 FoodTruckBench 基准的具体测试集定义 |
| 4 | `openai-fall-investors-anthropic-20260406` | P1 / LA Times + HN 双平台 / 大资本叙事 | LA Times 独家 + HN 验证，叙事规模大，适合深度展开 | 原文时间戳 4/1，需在正文注明 |
| 5 | `lm-studio-gemma-4-local-claude-code-20260406` | P1 / HN 203pts/Rank9 / 生态工具链 | Gemma 4 生态第四层，开发者工具链叙事差异化高 | 需与 #1 区分角度，不重复 iPhone 切入 |
| 6 | `nanocode-claude-code-jax-tpu-20260406` | P1 / $200 开源替代 / GitHub repo 可查 | 开发者强信号，工程赛道信号稳定 | 信号跨平台传播性需进一步核实 |

---

## 三个最重要平台任务单

> **平台选择逻辑**：wechat（日间主线主战场，保证 2 篇公众号草稿箱）/ x（海外高热快速传播）/ xiaohongshu（中文深度社区），其余平台 holdout。

---

### `wechat`

#### Task 1
- `topic_key`: `gemma-4-iphone-local-ai-20260406`
- `目标读者`: 关注 AI 落地、对端侧 AI 和手机端 LLM 有好奇心的中文科技读者；认知门槛中低，适合大众传播
- `切入角度`: **"Gemma 4 已经在 iPhone 上跑起来了，差距正在拉开"** ——不是技术测评，而是"谁能先用上"的实操视角
- `核心论点`: Google Gemma 4 正式登陆 iPhone（App Store 全球版 id6749645337），本地 LLM 从极客玩具进入可操作阶段；Apple/Google 生态博弈出现新变量
- `证据抓手`: HN 440pts/Rank3 + App Store 全球链接（`https://apps.apple.com/us/app/google-ai-edge-gallery/id6749645337`）+ 百度/微博已有中文讨论
- `source_ref_bundle`: `top20-screening-pack HB2 #1`
- `angle_constraint`: 无特殊角度约束；注意 App Store 链接使用明确 US/global 格式
- `视觉建议`: 截图 App Store 页面 + Gemma 4 模型参数对比表（2B vs Qwen2.5-7B vs GPT-4 mini）；封面图：iPhone 运行 AI 的意象
- `为什么适合该平台`: 微信适合实操型、结论型内容；"能不能在 iPhone 上用"是天然强 hook；公众号可深度展开

#### Task 2
- `topic_key`: `eight-years-wanting-three-months-building-ai-20260406`
- `目标读者`: 创业者和对 AI 开发有深层兴趣的读者；追求叙事质感，不只是信息搬运
- `切入角度`: **"他等了8年才动手，3个月后就震惊了全世界——这次不是天才，是积累"** ——人物弧线 + 技术叙事
- `核心论点`: 一个 HN 635pts/Rank2 的高热帖子，揭示了"等待-积累-突破"的 AI 开发新路径；这次叙事主角不是资本，是个人开发者
- `证据抓手`: HN 635pts/Rank2 原帖 + HN 评论区高质量讨论 + 作者自述
- `source_ref_bundle`: `top20-screening-pack HB2`
- `angle_constraint`: **正文必须注明时间戳 4/5**（原文发布于 4月5日）；不等同于当日新鲜热讯
- `视觉建议`: 引用 HN 评论区的关键引述 + 开发者时间轴（8年→3月）可视化；封面图：沙漏 + AI 代码意象
- `为什么适合该平台`: 微信深度读者对"坚持与突破"叙事有天然共鸣；篇幅足够支撑人物弧线展开

---

### `x`

#### Task 1
- `topic_key`: `gemma-4-benchmark-destruction-20260406`
- `目标读者`: 关注 AI 基准测试、模型性能对比的全球开发者 / 研究者社区；英语为主
- `切入角度`: **"FoodTruckBench doesn't lie — Gemma 4 just ran the table"** ——数据说话，简洁有力
- `核心论点`: Gemma 4 在 FoodTruckBench 上全线屠榜，中国开源模型对比数据一并呈现；这是本周最硬的AI基准新闻
- `证据抓手`: FoodTruckBench 原始数据 + HN / Twitter 讨论 + 中国模型对比数据
- `source_ref_bundle`: `top20-screening-pack HB2`
- `angle_constraint`: 无特殊角度约束；引用数据需注明测试集定义
- `视觉建议`: 基准测试排名表 / 柱状图；简洁封面图：数据板 + Gemma 4 logo
- `为什么适合该平台`: X/Twitter 适合短平快的硬数据传播；一句话结论 + 数据截图 = 最高效 tweet storm 素材

---

### `xiaohongshu`

#### Task 1
- `topic_key`: `openai-fall-investors-anthropic-20260406`
- `目标读者`: 关注 AI 投资动态、对 OpenAI 转型感兴趣的小红书读者；需要降低认知门槛
- `切入角度`: **"OpenAI 的投资人开始'用脚投票'了——LA Times 独家爆料背后"** ——投资动作切入，适合小红书"吃瓜"心理
- `核心论点`: LA Times 独家报道 OpenAI 投资人结构变化，Anthropic 成为新宠；这不是阴谋论，是机构行为逻辑的合理推断
- `证据抓手`: LA Times 原文 + HN 双平台讨论 + 量子位 / 机器之心中文传播
- `source_ref_bundle`: `top20-screening-pack HB2`
- `angle_constraint`: **正文必须注明时间戳 4/1**（原文发布于4月1日）；正文不得出现"已确认 Sora 是弃子"，只写"圈内流传"；不得用"曝光"类动词
- `视觉建议`: 投资人关系图（简化版）+ LA Times 报道截图；封面图：OpenAI vs Anthropic 牌桌意象
- `为什么适合该平台`: 小红书用户对"大公司内斗 / 投资流向"有强烈好奇；图表化呈现降低理解门槛

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: **否**
- `理由`: 当前 mini_slate 12 条均不具备百家号 SEO 关键词优势；Gemma 4 相关内容已有大量先行百家号文章，同行资本此时入场难以竞争；其余话题偏叙事深度，非关键词驱动型
- `承接哪篇主稿更优`: 若后续 Gemma 4 簇话题持续发酵，优先以 `gemma-4-iphone-local-ai-20260406` 为主稿做 SEO 镜像，而非单独立项

---

## Holdout 清单（剩余 9 条 mini_slate 候选）

### `gemma-4-benchmark-destruction-20260406`
- `为什么能进最终池`: P0，FoodTruckBench 硬数据，视觉化友好
- `为什么这轮没选`: 已锁入 x Task 1；今日 wechat 草稿箱限额已满（2篇）
- `什么时候可捞回`: 明日 morning_flash 或 day_mainline 续期；若 FoodTruckBench 数据有新进展则优先重评

### `lm-studio-gemma-4-local-claude-code-20260406`
- `为什么能进最终池`: P1，HN 203pts/Rank9，Gemma 4 生态工具链
- `为什么这轮没选`: continuity_only 模式 3 平台上限已用完；需与 #1 差异化切角后独立成篇
- `什么时候可捞回`: 明午间续期；writer 需提供与 #1 的明确差异化方案后方可开写

### `nanocode-claude-code-jax-tpu-20260406`
- `为什么能进最终池`: P1，$200 开源替代，GitHub repo 可查，工程赛道信号稳定
- `为什么这轮没选`: 同上，3 平台上限已用完
- `什么时候可捞回`: 明午间续期；需补 GitHub repo 链接确认

### `openai-fall-investors-anthropic-20260406`（Task 2 in xiaohongshu）
- `为什么能进最终池`: P1，LA Times + HN 双平台，大资本叙事，信号强
- `为什么这轮没选`: 仅锁入 xiaohongshu Task 1，未分配 wechat 槽位
- `什么时候可捞回`: wechat 草稿箱若在 19:00 前有空余，可追加一篇；否则明日续期

### `linux-kernel-ai-vulnerability-flood-20260406`
- `为什么能进最终池`: P2，Greg KH 一手锚点，开发者共情叙事，引用强度指引已完成
- `为什么这轮没选`: P2 级，3 平台上限已用完；今日 wechat 已锁定 2 篇 Gemma 4 簇深度稿
- `什么时候可捞回`: 明日 morning_flash（开发者细分受众）或 day_mainline 续期
- **`引用强度指引（必须遵守）`**: 正文写"据 The Register 引述 Greg KH 的观测"，不得写"AI 每天产生 10 份漏洞报告"作为硬数据

### `openai-new-model-tudou-not-gptx-20260406`
- `为什么能进最终池`: P2，Gemma 4 簇外延叙事，HN 讨论热度高
- `为什么这轮没选`: 3 平台上限已用完
- **`angle_constraint（必须遵守）`**: 正文不得出现"Sora是弃子（已确认）"；只写"圈内流传代号 tudou，尚未官宣"；不得用"曝光"类动词
- `什么时候可捞回`: 明午间续期；角度约束通过后才可开写

### `realtime-ai-audio-video-m3-pro-gemma-e2b-20260406`
- `为什么能进最终池`: P2，GitHub repo 有，Gemma 4 生态第四层
- `为什么这轮没选`: 3 平台上限已用完；信号较 #1/#2/#3 偏弱
- **`evidence_constraint（必须注明）`**: 引用时注明"Reddit 热度待核实"（score 被 403 遮挡）
- `什么时候可捞回`: Reddit 热度核实后升级 P1；明续期

### `copilot-entertainment-only-microsoft-tos-20260406`
- `为什么能进最终池`: P2，ToS 硬数据，风险叙事有传播性
- `为什么这轮没选`: 3 平台上限已用完
- **`angle_constraint（必须遵守）`**: 去"今日曝光"框架，改为"旧 ToS 引发新争议"；正文不得以"突发"为钩子
- `什么时候可捞回`: 明午间续期

### `deepseek-censorship-debate-20260406`
- `为什么能进最终池`: P2，争议性高，HN 讨论活跃
- `为什么这轮没选`: 3 平台上限已用完；证据基础偏薄
- **`angle_constraint（必须遵守）`**: 正文写"DeepSeek 官方截至发稿未回应"；不得以"已确认审查"呈现
- `什么时候可捞回`: 明午间续期；需 content-writer 深抓并确认引用边界

---

## P3 Pending（需 content-writer 深抓后方可重评）

| topic_key | 待处置 | 前置条件 |
|---|---|---|
| `claude-4-hour-global-secure-system-breach-20260406` | 深抓 36kr 原文全文；正文降"震惊"框架；"最安全系统"不得作为绝对化措辞 | content-writer 补原始链接后由 editor 复评 |
| `ai-memory-architecture-young-founders-20260406` | 补产品名/团队/项目链接；正文去掉"常春藤辍学"具体标签 | content-writer 补链接后由 editor 复评 |

---

## morning_flash 已锁题排除确认

- ✅ 本任务单未混入任何 morning_flash 车道已交付题
- ✅ #14 黄仁勋 fatal replace_topic，永久排除，不进入任何平台任务
- ✅ manifest 无 morning_flash 源混入

---

## 返工说明（供 content-writer / redteam 注意）

1. **wechat Task 1 & Task 2 均为 Gemma 4 簇核心稿**，需 writer 在两篇之间做明确差异化：Task1 = 实操可运行视角，Task2 = 叙事人物弧线视角；不得写成同题重复
2. **x Task 1 (benchmark)** 与 wechat Task 1 共享同一数据源，需在 x 上做极致简化（数据 + 一句话结论），不在 x 发长文
3. **xiaohongshu Task 1 (OpenAI investors)** 的 angle constraint 是 scorecard 红队升级核心点，writer 必须严格执行，不得以任何形式软化
4. **Holdout 9 条均保留在 continuity pool**，明日可由 topic-planner 优先从 holdout 中填补新平台槽位

---

*topic-planner｜2026-04-06 16:26 CST｜day_mainline continuity_only limited_task_sheet*
*runtime: topic-planner | workspace: workspace-topic-planner*
