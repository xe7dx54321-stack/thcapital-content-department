# 平台任务单

- `date`: `2026-04-21`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-21 19:28:30 CST`
- `run_token`: `20260421`
- `input_top20_scorecard`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260421__top20__stage-gate-scorecard.md`
- `input_top5_board`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260421__daily-top8-to-top5.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `rework + continuity_only → limited task sheet；wechat保2槽位，其余平台先各保1槽位，其余进holdout`

---

## 裁判结论

| 字段 | 值 |
|---|---|
| `stage_gate_status` | `continuity_only` |
| `scorecard_status` | `rework（score=7.0/10）` |
| `top5_board_status` | `final` + `continuity_only` |
| `本轮产出` | `limited task sheet` |
| `任务槽位上限` | `wechat×2 + 其余平台各×1 = 8 slots` |

**本轮不是 no-op**：Top5板已final，scorecard为rework+continuity_only，必须产出continuity_only limited task sheet。

---

## 全局主池 Top6（来自当日Top5/Holdout板，可溯源）

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|---|---|---|---|---|
| 1 | `hn_frontpage_47844431_roblox_cheat_ai_tool_brought_down_vercel_platform_20260421` | P0保底锁题·平台级事故·AI工具链可靠性警示 | AI Infra事故是builder圈高频讨论；Vercel故障具强传播性；HN高points；信号真实 | partial source仍需补webmatrices.com正文；工具名待确认 |
| 2 | `zhihu_hot_ai_ceo_ai_20260421` | P0保底锁题·钉钉CEO AI办公理念 | 知乎97万热度入口明确；天然讨论空间大；职场/AI交叉话题易出圈 | 正式写作前需核实原始来源；硬数据偏少 |
| 3 | `36kr_ai_claude_mythos_22_deepseek_20260421` | P2保底锁题·Claude Mythos开源·22岁天才 | 与AI/Agent/一人公司主线高度一致；开源事件有技术传播力 | partial source仍需补36Kr原文人物细节 |
| 4 | `jiqizhixin_site_3d_vast_anigen_aigc_siggraph_2026_tog_20260421` | P0保底锁题·VAST+HKU AniGen AIGC | SIGGRAPH 2026学术背书；3D资产生成贴近agent/具身智能主线 | partial source仍需补原始论文/团队细节 |
| 5 | `36kr_ai_sql_codex_openai_20260421` | P2保底锁题·Codex+终身记忆写SQL | AI编程效率工具；开发者圈关注度高；OpenAI品牌背书 | partial source仍需补OpenAI官方blog正文 |
| 6 | `hn_frontpage_47829178_claude_token_counter_now_with_model_comparisons_20260421` | P1备选·Claude Token Counter | HN points真实；与Claude/Agent主线一致；工具对比角度好写 | 来自Holdout#8；需补simonwillison.net正文后放行 |

---

## 六个主战场任务单

### `wechat`

#### Task 1
- `topic_key`: `hn_frontpage_47844431_roblox_cheat_ai_tool_brought_down_vercel_platform_20260421`
- `目标读者`: 开发者/技术管理者/AI Infra关注者
- `切入角度`: 以"Vercel平台级事故"为入口，从AI工具链可靠性视角切入，讨论当AI工具成为基础设施时的风险敞口
- `核心论点`: AI辅助编程工具正在进入平台级基础设施层；Vercel事故是一个警示信号——工具越深度集成，故障破坏力越大
- `证据抓手`: HN高points + webmatrices.com正文（待补证） + Vercel官方或HN评论中的工具身份确认
- `source_ref_bundle`:
  - `webmatrices.com正文（signal-scout补证后回链）`
  - `HN讨论帖：https://news.ycombinator.com/item?id=47844431`
  - `source_packet：/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260421_141959__hn_frontpage_47844431_a_roblox_cheat_and_one_ai_tool_brought_down_vercel_s_platform__source-packet.md`
- `视觉建议`: 平台故障示意图或HN截图，突出"AI工具→平台瘫掉"的因果链
- `为什么适合该平台`: 微信长文适合承载完整的事故复盘+技术判断叙事；技术管理者和开发者是高契合受众

#### Task 2
- `topic_key`: `zhihu_hot_ai_ceo_ai_20260421`
- `目标读者`: 职场人士/企业管理者/AI应用关注者
- `切入角度`: 从"AI替代白领工作"的真实案例切入，讨论钉钉CEO这一主张的合理性与边界
- `核心论点`: AI自动化办公不是伪命题，但"严禁人工"需要配套机制；这个案例暴露了AI落地过程中的激进与风险
- `证据抓手`: 知乎问题热度 + 来源可查的钉钉官方公告或内部传达记录（写稿前必须补一手来源）
- `source_ref_bundle`:
  - `知乎源问题：https://www.zhihu.com/question/2029565174948914400`
  - `source_packet：/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260420_225556__zhihu_hot_ai_ceo_ai__source-packet.md`
- `视觉建议`: 钉钉AI自动化流程简图或对比图（人工流程 vs AI自动流程）
- `为什么适合该平台`: 微信适合深度分析；这个话题有职场伦理维度，需要展开而非快讯

---

### `xiaohongshu`

#### Task 1
- `topic_key`: `jiqizhixin_site_3d_vast_anigen_aigc_siggraph_2026_tog_20260421`
- `目标读者`: 创作者/AI爱好者/对AIGC有兴趣的年轻用户
- `切入角度`: "一张图生成能动的3D资产"——把SIGGRAPH论文翻译成"普通人也能玩"的AIGC工具科普
- `核心论点`: AniGen让3D内容创作门槛降到地板；游戏/动画/具身智能的创作者都应该关注这个信号
- `证据抓手`: 即刻或机器之心公众号文章（补原始论文/团队介绍）+ SIGGRAPH 2026官方信息
- `source_ref_bundle`:
  - `机器之心源：https://www.jiqizhixin.com/`
  - `source_packet：/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260420_232917__jiqizhixin_site_3d_vast_anigen_aigc_siggraph_2026_tog__source-packet.md`
- `视觉建议`: Before/After对比图（静态图 → 3D动画资产），或AniGen生成效果展示
- `为什么适合该平台`: 小红书用户对视觉类AI工具敏感度高；强视觉展示+低门槛科普是平台天然语言

---

### `zhihu`

#### Task 1
- `topic_key`: `36kr_ai_claude_mythos_22_deepseek_20260421`
- `目标读者`: AI从业者/开发者/技术研究者
- `切入角度`: "22岁天才+融合DeepSeek思路"的技术架构解读——Mythos做对了什么，为什么值得开源
- `核心论点`: Mythos的核心创新在于把DeepSeek的长上下文思路工程化；这个开源项目对Agent架构有直接影响
- `证据抓手`: 36Kr原文（待补人物细节）+ GitHub开源页 + 相关技术讨论
- `source_ref_bundle`:
  - `36Kr源：https://www.36kr.com/p/3774954107650568`
  - `source_packet：/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260420_232917__36kr_ai_claude_mythos_22_deepseek__source-packet.md`
- `视觉建议`: Mythos架构简图（如果GitHub/官方有）或人物/团队信息图
- `为什么适合该平台`: 知乎的技术讨论深度与本话题高度匹配；技术架构分析是知乎强项

---

### `x`

#### Task 1
- `topic_key`: `36kr_ai_sql_codex_openai_20260421`
- `目标读者`: 开发者/工程师/AI编程工具重度用户
- `切入角度`: "动动嘴写SQL"是真实需求还是营销噱头？Codex+终身记忆的实际体验边界
- `核心论点`: 自然语言写SQL的障碍不在于生成能力，在于记忆上下文；OpenAI的解法有效但有上限
- `证据抓手`: 36Kr原文（待补OpenAI官方blog正文）+ 开发者社区对Codex的评价
- `source_ref_bundle`:
  - `36Kr源：https://www.36kr.com/p/3775077919130118`
  - `source_packet：/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260420_232917__36kr_ai_sql_codex_openai__source-packet.md`
- `视觉建议`: Codex SQL生成效果截图或命令行演示
- `为什么适合该平台`: X平台开发者浓度最高；"动动嘴写SQL"可以直接做成一条观点推文

---

### `bilibili`

#### Task 1
- `topic_key`: `hn_frontpage_47829178_claude_token_counter_now_with_model_comparisons_20260421`
- `目标读者`: B站开发者/AI爱好者观众
- `切入角度`: 从Token计数工具切入，做一期"AI模型到底怎么计费"的实用科普
- `核心论点`: Token计数是理解大模型成本的底层技能；Claude Token Counter提供了实用的对比视角
- `证据抓手`: simonwillison.net原文（待补证）+ 各模型Token计费标准对比
- `source_ref_bundle`:
  - `simonwillison源：https://simonwillison.net/2026/Apr/20/claude-token-counts/`
  - `source_packet：/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260420_232917__hn_frontpage_47829178_claude_token_counter_now_with_model_comparisons__source-packet.md`
- `视觉建议`: 各模型Token价格对比表或Claude Token Counter界面截图
- `为什么适合该平台`: B站用户爱看"工具测评+实用技巧"类视频；Token计数是实用选题

---

### `toutiao`

#### Task 1
- `topic_key`: `zhihu_hot_ai_ceo_ai_20260421`
- `目标读者`: 职场用户/泛科技读者
- `切入角度`: 以"钉钉CEO说以后不用写文档了"为标题钩子，做成"AI办公真的来了吗"的泛科技快讯
- `核心论点`: 钉钉的激进AI办公理念是一个信号：大厂正在把AI落地从实验变成强制
- `证据抓手`: 知乎热度数据 + 可查证的钉钉官方政策（写稿前必须补一手来源）
- `source_ref_bundle`:
  - `知乎源：https://www.zhihu.com/question/2029565174948914400`
  - `source_packet：/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260420_225556__zhihu_hot_ai_ceo_ai__source-packet.md`
- `视觉建议`: 钉钉AI办公流程图或职场+AI对比图
- `为什么适合该平台`: 头条用户偏好即时热点快讯；钉钉CEO话题有强新闻性，适合快讯格式

---

## 三个最重要平台任务单（按优先级排序）

### 1. `wechat` / Task 1 — Vercel平台事故
- `topic_key`: `hn_frontpage_47844431_roblox_cheat_ai_tool_brought_down_vercel_platform_20260421`
- `目标读者`: 开发者/技术管理者/AI Infra关注者
- `切入角度`: AI工具链可靠性警示——平台级事故视角
- `核心论点`: AI辅助编程工具正在进入平台级基础设施层；Vercel事故是警示信号
- `证据抓手`: HN高points + webmatrices.com正文（待补）
- `source_ref_bundle`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260421_141959__hn_frontpage_47844431_a_roblox_cheat_and_one_ai_tool_brought_down_vercel_s_platform__source-packet.md`

### 2. `wechat` / Task 2 — 钉钉CEO AI办公理念
- `topic_key`: `zhihu_hot_ai_ceo_ai_20260421`
- `目标读者`: 职场人士/企业管理者/AI应用关注者
- `切入角度`: AI替代白领工作的真实案例分析
- `核心论点`: AI自动化办公不是伪命题，但"严禁人工"需要配套机制
- `证据抓手`: 知乎97万热度 + 可查证来源（写稿前必须补一手）
- `source_ref_bundle`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260420_225556__zhihu_hot_ai_ceo_ai__source-packet.md`

### 3. `x` / Task 1 — Codex+终身记忆写SQL
- `topic_key`: `36kr_ai_sql_codex_openai_20260421`
- `目标读者`: 开发者/工程师/AI编程工具重度用户
- `切入角度`: 自然语言写SQL的真实体验边界
- `核心论点`: 自然语言写SQL的障碍不在于生成能力，在于记忆上下文；OpenAI解法有效但有上限
- `证据抓手`: 36Kr原文（待补OpenAI官方blog）+ 开发者社区评价
- `source_ref_bundle`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260420_232917__36kr_ai_sql_codex_openai__source-packet.md`

---

## `baijiahao` SEO镜像层判断

- `是否需要单独立题`: **否**
- `理由`: 本轮Top5/Holdout板中题目多属技术工具/开发者视角，天然不适合百家号泛科技用户；当前无强SEO搜索量信号出现；不立镜像层，将资源集中主战场。
- `承接哪篇主稿更优`: 如后续出现"钉钉AI办公"相关搜索流量，可由wechat Task 2内容做SEO镜像；其余题目暂不需要。

---

## Holdout清单

### `36kr_ai_figma_claude_design_20260421`
- `为什么能进最终池`: Figma+Claude Design话题有真实市场影响（Figma市值变化）；属于AI设计工具主线
- `为什么这轮没选`: 主战场slots已满；本轮优先覆盖平台级事故/AI办公理念/开发者工具类话题；Figma题可降权
- `什么时候可捞回`: 若Top5中主槽位补证失败或内容展开不足，或出现Figma相关新热点，立即捞回

### `hn_frontpage_47834565_qwen3_6_max_preview_smarter_sharper_still_evolving_20260421`
- `为什么能进最终池`: Qwen3.6-Max是国产头部模型动态；HN真实讨论；AA-Intelligence Index=52量化信号（需补文件级证据）
- `为什么这轮没选`: Top20 scorecard标注Index=52无文件级证据，属补证未完成状态；本轮保守处置
- `什么时候可捞回`: signal-scout补证Index=52文件级证据（r/LocalLLaMA原帖正文+AA-Intelligence页面）后，立即捞回进入X或小红书槽位

---

## artifact_status 自检

| artifact | path | expected_state | 自检结果 |
|---|---|---|---|
| `Top20 scorecard` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260421__top20__stage-gate-scorecard.md` | `final` | ✅ rework但continuity_only输出有效 |
| `Top5 board` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260421__daily-top8-to-top5.md` | `final` | ✅ final + continuity_only |
| `Platform task sheet` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260421__platform-task-sheet.md` | `final` | ⏳ 等待artifact_status脚本验证 |

---

## 平台任务槽位汇总

| 平台 | Slot 1 | Slot 2 | 状态 |
|---|---|---|---|
| `wechat` | Vercel平台事故（Task 1） | 钉钉CEO AI办公（Task 2） | ✅ |
| `xiaohongshu` | VAST+AniGen AIGC（Task 1） | — | holdout |
| `zhihu` | Claude Mythos开源（Task 1） | — | holdout |
| `x` | Codex+SQL记忆（Task 1） | — | holdout |
| `bilibili` | Claude Token Counter（Task 1） | — | holdout |
| `toutiao` | 钉钉CEO AI办公（Task 1） | — | 与wechat Task 2同题复用 |

**所有8个active slots均直接回链至当日Top5/Holdout板候选，无临时扩题。**
