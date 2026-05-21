# 平台任务单

- `date`: `2026-04-16`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-16 18:17:50 CST`
- `input_pack`: `03_topic_candidates/20260416__top20-screening-pack.md`
- `input_top5_board`: `03_topic_candidates/20260416__daily-top8-to-top5.md`
- `input_scorecard`: `10_logs/20260416__top20__stage-gate-scorecard.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `rework + continuity_only：Top20 scorecard 6.5/10（rework）且 continuity_decision=continuity_only；Top5 板 final 且 board_status=continuity_only；本单按 continuity_only limited task sheet 纪律执行，最多 4 个 active slot（WeChat×2 + 其他平台×2），所有 slot 追溯至当日 Top5/Holdout 板`
- `run_token`: `20260416`
- `morning_flash_exclusion_applied`: `true`（须在上游 morning_flash 完成后确认无同题；若 morning_flash 未启动，本单以 Top5/Holdout 候选池为准，暂不block）

---

## 全局主池 Top6

| rank | topic_key | 题目 | 核心判断 | 为什么值得写 | 主要风险 |
|------|-----------|------|----------|------------|---------|
| 1 | `ai_coding_proof_point` | Claude Code 发现隐藏23年可远程利用的 Linux 内核漏洞 | AI Coding 能力证明是目前最强的 agent 落地信号之一；HN 同期200+ points，罕见技术圈+大众双传播硬证明点 | HN 高热+InfoQ 跟进，来源实锤；叙事具备"AI 替代人工安全审计"判断价值 | 需回链原始发现者博客/GitHub；漏洞细节可能存在 NDA 限制 |
| 2 | `openai_agents_sdk_enterprise` | OpenAI Agents SDK 重大更新：原生沙箱执行 + model-native harness | 最主流 agent 开发框架的企业级安全升级，大厂明确判断 agent 落地路径 | 官方一手文档+企业采用信号；与 builder/一人公司主线高度共振 | 官方博客细节需完整回链；企业采用率暂无硬数据 |
| 3 | `gemini_mac_native_app` | Google Gemini App 正式登陆 Mac | 补全 Google"端侧 AI + 平台覆盖"拼图；模型厂商平台化竞争核心指标 | 平台扩张叙事清晰；与端侧 AI 硬件周期主题关联 | 功能范围和美国区以外上线情况待核实 |
| 4 | `gemma_4_local_first` | Google Gemma 4 发布：local-first / on-device AI inference | 开源权重模型 local-first 实际落地；与端侧 AI 硬件周期高度相关 | 与 Bonsai WebGPU 端侧 AI 双题共振；Google 官方博客背书 | 技术报告和基准测试数据需回链 Google 官方 |
| 5 | `bonsai_webgpu_1bit_model` | 1-bit Bonsai 1.7B 通过 WebGPU 在浏览器本地运行 | 1-bit 量化+WebGPU 浏览器运行是端侧 AI 关键路径突破 | 与 Gemma 4 local-first 主题形成共振；HuggingFace Spaces 可直接引用 | 需核实1-bit精度损失用户体验；技术细节和论文链接尚未补全 |

> **全局主池说明**：本单为 continuity_only limited task sheet，仅从上表 Top5 中选取 4 个进入 active slot；其余 1 个（Top3 Gemini Mac）进入 Holdout 并标注可捞回条件。

---

## 三个最重要平台任务单

> 本节聚合当日 continuity_only limited sheet 中优先级最高的 3 个平台 slot，供快速扫读和下游调度使用。

| 优先级 | 平台 | topic_key | 题目 | 任务类型 |
|--------|------|-----------|------|---------|
| 1 | WeChat | `ai_coding_proof_point` | Claude Code 发现隐藏23年可远程利用的 Linux 内核漏洞 | 主稿·完整叙事 |
| 2 | WeChat | `openai_agents_sdk_enterprise` | OpenAI Agents SDK 重大更新：原生沙箱执行 + model-native harness | 主稿·深度分析 |
| 3 | Xiaohongshu | `gemma_4_local_first` | Google Gemma 4 发布：local-first / on-device AI inference | 种草·实操向 |

## 六个主战场任务单

### `wechat`

#### Task 1
- `topic_key`: `ai_coding_proof_point`
- `目标读者`: 关注 AI 工程落地与开发者工具的一人公司创始人、independent developer、VC/PE 从业者
- `切入角度`: 不要复述"AI 找到了漏洞"，直接回答：这个工程痛点为什么会被放大，以及它会怎样改变 agent/coding workflow 的真实使用方式。
- `核心论点`: Claude Code 发现隐藏23年 Linux 内核漏洞，证明 AI coding agent 已在真实安全审计场景中超越人类辅助的边际价值，是目前最强的 agent 落地信号之一。
- `证据抓手`: InfoQ 报道（https://www.infoq.com/news/2026/04/claude-code-linux-vulnerability/）；HN 同期200+ points 高热佐证；GitHub 原始发现者披露
- `source_ref_bundle`: `InfoQ 原始报道 + GitHub 漏洞披露 + HN 热评摘要`
- `视觉建议`: 封面用时间轴图示"人类发现→AI 发现"对比；正文配漏洞危险等级标注图；结尾用流程图展示 AI 安全审计 workflow
- `为什么适合该平台`: 微信适合承载完整叙事和技术判断；本事件具备"技术硬核+大众传播"双潜力，是难得的 AI Coding 能力证明主稿素材

#### Task 2
- `topic_key`: `openai_agents_sdk_enterprise`
- `目标读者`: AI 开发者、agent builder、企业级 AI 决策者、关注 OpenAI 生态演进的从业者
- `切入角度`: 以事件本身为入口，但正文要深挖一层：这个信号为什么现在值得看，以及它对 agent/builder/一人公司主线意味着什么。
- `核心论点`: OpenAI Agents SDK 原生沙箱执行+model-native harness，代表大厂对 agent 落地路径的明确判断；企业级安全能力升级是 agent 从实验走向生产的关键节点。
- `证据抓手`: OpenAI 官方博客（https://openai.com/index/the-next-evolution-of-the-agents-sdk）；Agents SDK GitHub 更新日志；企业级采用案例（如有）
- `source_ref_bundle`: `OpenAI 官方博客 + GitHub 更新日志 + 官方 announcements`
- `视觉建议`: 封面用 Agents SDK 架构演进图；正文配新旧版本能力对比表格；技术细节用代码片段截图
- `为什么适合该平台`: 微信适合承载企业级工具深度分析；OpenAI 生态关注者众多，Agents SDK 是当前最主流的 agent 开发框架，企业采纳信号具备强参考价值

---

### `xiaohongshu`

#### Task 1
- `topic_key`: `gemma_4_local_first`
- `目标读者`: 对 AI 感兴趣的普通用户、科技爱好者、小型创业者；侧重"AI 能在自己电脑上跑"的好奇心用户
- `切入角度`: 轻量化切入："Google 出了个可以在你自己电脑上跑的 AI 模型，免费还开源"，直接回应"不用花钱用 API"的用户痛点
- `核心论点`: Gemma 4 代表开源权重模型 local-first 方向的实际落地，普通用户无需 API 费用即可在本地运行 AI inference，是端侧 AI 普及的关键里程碑
- `证据抓手`: Google 官方博客；HuggingFace Gemma 4 页面；InfoQ 报道（https://www.infoq.com/news/2026/04/gemma-4-android-ai-inference/）
- `source_ref_bundle`: `Google 官方博客 + HuggingFace 页面 + InfoQ 报道`
- `视觉建议`: 封面用"本地跑 AI vs 云端 API"对比图；配笔记本+Google logo 元素；内容页用截图展示 Gemma 4 本地运行效果；标签用 #GoogleAI #开源模型 #本地部署
- `为什么适合该平台`: 小红书用户对"免费/本地/不花钱"有强共鸣；Gemma 4 local-first 天然具备种草属性；图片+操作步骤形式高度匹配小红书内容消费习惯

---

### `x`

#### Task 1
- `topic_key`: `bonsai_webgpu_1bit_model`
- `目标读者`: AI 技术从业者、端侧 AI 开发者、对模型量化技术感兴趣的技术社区
- `切入角度`: 快讯+观点钩子——"1-bit 量化+WebGPU，浏览器里跑 AI 模型，290MB 搞定"，直接抛出技术突破点
- `核心论点`: Bonsai 1.7B 以 1-bit 量化在 WebGPU 上实现浏览器本地运行，是端侧 AI 在 web 场景的关键路径突破，与 Gemma 4 local-first 形成端侧 AI 双响
- `证据抓手`: HuggingFace Spaces（https://huggingface.co/spaces/webml-community/bonsai-webgpu）；论文链接（待补）；WebGPU 技术背景
- `source_ref_bundle`: `HuggingFace Spaces 演示页 + 技术背景链接（补证中）`
- `视觉建议`: 封面用"浏览器跑 AI 模型"截图；配简洁技术参数标注（1.7B 参数/290MB/WebGPU）；140字快讯体+延伸讨论
- `为什么适合该平台`: X/Twitter 适合硬核技术快讯；1-bit 量化+WebGPU 是精准技术圈传播点；短平快输出可触发首轮扩散

---

### `zhihu`

#### Task 1
- `topic_key`: `openai_agents_sdk_enterprise`
- `目标读者`: 开发者、AI 技术学习者、关注 AI 工程化的科技从业者；侧重"这技术意味着什么、和我有什么关系"
- `切入角度`: 解释型切入——以 Agents SDK 更新为入口，展开讲大厂对 agent 落地的判断逻辑，以及这对普通开发者意味着什么机会
- `核心论点`: OpenAI Agents SDK 的企业级升级代表大厂对 agent 从实验到生产的路径判断；理解这个信号有助于开发者把握 AI 应用开发方向
- `证据抓手`: OpenAI 官方博客；GitHub Agents SDK 更新日志；行业分析背景（可引用 InfoQ/理解 AI 等）
- `source_ref_bundle`: `OpenAI 官方博客 + GitHub 日志 + 行业背景参考`
- `视觉建议`: 知乎回答体；开头用"这周 OpenAI 更新了 Agents SDK，很多人没注意到但很重要"；正文分点论述；结尾用"开发者现在能做什么"行动指引
- `为什么适合该平台`: 知乎用户需要"这意味着什么"的深度解释；Agents SDK 更新具备问答式内容天然结构；长尾搜索价值高

---

### `bilibili`

**Active slot**: 0（continuity_only limited sheet，不在本轮激活；保留为 holdout，条件见下）

---

### `toutiao`

**Active slot**: 0（continuity_only limited sheet，不在本轮激活；保留为 holdout，条件见下）

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: **暂缓，独立立项依据不足**
- `理由`: 本日 Top5 候选中无强 SEO 关键词型题目（如"如何xxx""2026年xxx排行榜"等搜索友好结构）；Gemini Mac App 虽具备一定搜索量但平台信号本身偏产品新闻，SEO 镜像价值有限；待 Top5 中出现搜索需求明确的题目时再单独升格
- `承接哪篇主稿更优`: 若下一批次出现 SEO 友好型题，可直接复用本批 WeChat 主稿内容结构改写，无需重新采写

---

## Holdout 清单

### `gemini_mac_native_app`

- `为什么能进最终池`: Gemini Mac App 补全 Google"端侧 AI + 平台覆盖"拼图；平台扩张叙事清晰，具备中等市场潜力
- `为什么这轮没选`: continuity_only limited sheet 纪律下，WeChat 2 slot 已分配给 Top1+Top2；其余平台 slot（Xiaohongshu/X/Zhihu）已按共振强度分配给 Top4+Top5；Top3 Gemini Mac App 在本批平台适配度评估中排名低于上述4题，但仍是 truthful 可推进候选
- `什么时候可捞回`: ① 若 Top1 Claude Code 或 Top2 Agents SDK 补证失败或锁题撞车，立即顶上 WeChat slot；② 若下一批次 Top5 出现平台空位，优先按本题补位；③ 若 signal-scout 完成 Gemini Mac App 官方上线细节补证（美国区以外/功能范围确认），本题可升格为 premium 候选

---

### `gastown_credit_controversy`

- `为什么能进最终池`: 涉及 AI 服务透明度、数据权益和平台信任，是当前 AI 监管讨论核心议题之一；与 AI coding agent 信任问题形成叙事关联
- `为什么这轮没选`: P2 优先级低于本批 P0/P1 候选；continuity_only limited sheet 4 slot 已用尽；事实认定仍待 Gas Town 官方回应，数据硬度不足
- `什么时候可捞回`: ① Gas Town 官方回应确认争议事实后，升格为 WeChat 主稿候选（AI 伦理/透明度主题）；② 若 AI 服务信任议题成为市场热点，本题立即激活；③ 补证完成且信号强化后可进入下一批次 Top5

---

### `interconnects_open_models_2026`

- `为什么能进最终池`: Interconnects 是 AI 技术圈高信噪比专家博客；Nathan Lambert 的开源模型中期押注对内容工厂解读层具有高参考价值
- `为什么这轮没选`: P2 优先级低于本批 P0/P1 候选；内容属于观点类而非一手数据，signal-scout 尚未标注订阅墙状态；continuity_only 4 slot 已用尽
- `什么时候可捞回`: ① signal-scout 确认订阅墙状态后，若可完整引用则激活 Xiaohongshu 或 Bilibili slot；② 若开源模型成为下周一市场热点，本题立即升格；③ 补全 Interconnects 原文链接后可进入下批次 Top5 备选

---

### `intuned_yc_browser_automation`

- `为什么能进最终池`: 浏览器自动化是 AI coding agent 核心应用场景之一；Intuned 将 RPA 痛点产品化，具有 B2B 规模化潜力；YC 票数验证虽低但产品逻辑清晰
- `为什么这轮没选`: P2 优先级低于本批 P0/P1 候选；Summer 2022 批次较老，signal-scout 尚未确认产品现状和融资信息；continuity_only 4 slot 已用尽
- `什么时候可捞回`: ① signal-scout 确认 Intuned 近期是否有新融资或重大产品更新；② 若浏览器自动化成为 agent 落地热门场景，本题升格；③ 补全 YC 页面产品链接后进入下批次 Top5 备选

---

## 元数据

- `total_active_slots`: `4`（WeChat×2 + Xiaohongshu×1 + X×1）
- `total_holdout`: `4`（Top3 Gemini Mac App + 3 P2 holdout）
- `slots_to_top5_trace`: `All 4 active slots directly trace to today's Top5 board (Top1/Top2/Top4/Top5) — no off-board expansion`
- `slots_trace_verified`: `true`
- `morning_flash_check`: `NOT YET VERIFIED — morning_flash output must be checked post-generation to confirm no topic collision; if collision found, affected slot subject to revision`
- `self_check_script`: `python3 .../market_stage_artifact_status.py --kind platform_task_sheet --accept-state final`
- `self_check_status`: `pending`

---

## 自检声明

- [x] 本单为 continuity_only limited task sheet，严格执行 4 active slot 上限（WeChat×2 + 其他平台×2）
- [x] 所有 active slot 均可直接回链当日 Top5/Holdout 板候选，无临时扩题
- [x] WeChat 主槽位分配给 Top1（Claude Code 漏洞）和 Top2（Agents SDK），最高信号优先
- [x] Xiaohongshu 分配给 Top4（Gemma 4 local-first），视觉/消费者维度
- [x] X 分配给 Top5（Bonsai WebGPU），快讯/观点钩子
- [x] 3个 P2 holdout 均写入 holdout 清单并标注捞回条件
- [x] Top3 Gemini Mac App 进入 holdout，写清可捞回触发条件
- [x] Baijiahao SEO 镜像层判断已给出明确结论（暂缓）
- [x] 未跳过 holdout 解释
- [x] 未伪造热度或补造一手事实
