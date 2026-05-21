# 平台任务单

- `date`: `2026-03-30`
- `owner`: `topic-planner`
- `generated_at`: `2026-03-30 16:05 CST`
- `input_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260330__top20-screening-pack__reworked.md`
- `reworked_pack_completed_at`: `2026-03-30 13:52 CST（#3 融资数字已修正 $500M/$4.3B/$8.5B+；#6 Voxtral 叙事已修正；#7 Harris/Maher 来源已替换 HBO Max/seat42f.com）`
- `top20_scorecard_ref`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260330__top20__stage-gate-scorecard.md`
- `scorecard_version`: `v4`
- `scorecard_generated_at`: `2026-03-30 13:40 CST`
- `scorecard_verdict`: `rework | 7.5/10 | continuity_only | top20_mini_slate`
- `scorecard_top3_authorization`: `✅ Top3（Sora/Carlini/llama.cpp）已由 scorecard v4 明确授权直接进入 platform-task，无需等待 #3/#6/#7 复评`
- `rework_pack_status`: `#3/#6/#7 补证已于 13:52 CST 完成（rework_completed=yes），但尚未经 market-editor 复评；Top3 不受此限，正常推进`
- `awaiting_re-evaluation`: `#3 Moonshot / #6 Voxtral / #7 Harris-Maher 三条待 market-editor 复评后方可升级至 premium_pass 或扩大任务单`
- `stage_gate_status`: `continuity_only`（依据 scorecard v4 13:40 CST）
- `stage_gate_rule`: `continuity_only limited task sheet：Top3 平台各 1 槽位；其余平台与 #3/#6/#7 写入 Holdout；#3/#6/#7 复评通过后可扩为 premium_pass 并恢复双槽位`

## 全局主池 Top6

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|---|---|---|---|---|
| 1 | `ai-video-sora-shutdown-openai-pivot` | 今日最强确定性锚点，适合先保留 | 官方 + 多主流媒体交叉确认，叙事弧完整，价值与可信度都最高 | 低 |
| 2 | `nicolas-carlini-claude-security-vulnerability-research` | 安全研究里程碑，平台传播张力强 | 一手 podcast、$370 万数字、人物势能强 | 中 |
| 3 | `llama-cpp-kv-rotation-pr21038-aime25` | 技术可信度最强的开源基础设施题 | GitHub PR 一手来源，适合知乎/技术向平台 | 中 |
| 4 | `moonshot-ai-1b-funding-kimi-claw-revenue` | 中国大模型融资强信号，但先不下发 | 方向正确，商业化叙事强 | 高：2025-12 融资数字存在 10 倍录入错误，待修正 |
| 5 | `voxtral-tts-mistral-ai-voice-cloning-open-source` | TTS 赛道有价值，但叙事需修 | Mistral AI 一手来源，易做视频/工具稿 | 中高：voice cloning 路线图表述待修 |
| 6 | `claude-code-no-coder-6-products一人公司叙事` | 一人公司故事能做引流，但不是本轮最高优先级 | 平台适配性强，适合后续补位 | 中：部分产品仍需补核验 |

## 六个主战场任务单

### `wechat`
#### Task 1
- `topic_key`: `ai-video-sora-shutdown-openai-pivot`
- `目标读者`: `科技从业者、投资人、AI 行业观察者`
- `切入角度`: `从 Sora 关停看 OpenAI 战略重心转移，以及 AI 视频赛道为何过早进入现实检验`
- `核心论点`: `Sora 的关停不是单一产品成败，而是 OpenAI 从消费级 AI 视频转向企业级与 coding 工具的战略信号。官方关停时间、Disney 合作取消与媒体多方确认，足够支撑一篇高确定性的深度稿。`
- `证据抓手`: `OpenAI 官方公告、Guardian、LA Times、CBS、Forbes；App 4/26 与 API 9/24 的具体节点；Disney $1B 合作取消`
- `source_ref_bundle`: `https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation | https://www.theguardian.com/technology/2026/mar/24/openai-ai-video-sora | https://www.latimes.com/entertainment-arts/business/story/2026-03-24/openai-will-shut-down-sora-why-what-to-know | https://www.cbsnews.com/news/sora-ai-openai-discontinues/ | https://www.forbes.com/sites/ronschmelzer/2026/03/24/openai-discontinues-ai-video-gen-app-sora/`
- `视觉建议`: `OpenAI 官方公告页截图 + 媒体报道拼图 + Sora 产品时间线`
- `为什么适合该平台`: `微信公众号最适合承接高可信、强分析、可建立品牌判断力的行业深度稿`

#### Task 2
- `status`: `disabled_for_continuity_only`
- `原因`: `本轮 continuity_only 只保留 1 个公众号槽位；等待 Moonshot 数字修正或 Voxtral 叙事修正后再恢复第二槽位`

### `xiaohongshu`
#### Task 1
- `topic_key`: `nicolas-carlini-claude-security-vulnerability-research`
- `目标读者`: `AI 爱好者、科技从业者、对 AI 安全感兴趣的普通用户`
- `切入角度`: `"Claude 比顶级安全研究员还会找漏洞？" 用 $370 万漏洞收益和 Carlini 本人背书讲一个可传播的技术人物故事`
- `核心论点`: `Carlini 这条线兼具人物势能、金钱数字和 AI 能力边界三重传播抓手，适合做成 3-5 页图文短稿。小红书优先讲“AI 已经开始替代顶级人类专家的一部分工作”这个强钩子。`
- `证据抓手`: `Security Cryptography Whatever podcast、Listennotes 镜像、$3.7M 漏洞利润、Google Scholar 67.2k 引用数`
- `source_ref_bundle`: `https://securitycryptographywhatever.com/2026/03/25/ai-bug-finding/ | https://www.listennotes.com/podcasts/security/ai-bug-finding-with-nicholas-5VTxWZ_BL40/`
- `视觉建议`: `Carlini 引用数截图 + podcast 页面截图 + "$370 万" 大字封面`
- `为什么适合该平台`: `小红书适合“人物 + 反常识 + 金额数字”的轻量传播型内容，这条比 Moonshot 和 llama.cpp 更容易出首波互动`

#### Task 2
- `status`: `disabled_for_continuity_only`
- `原因`: `本轮 continuity_only 只保留 1 个小红书槽位；Claude Code 一人公司叙事留作下一轮补位`

### `zhihu`
#### Task 1
- `topic_key`: `llama-cpp-kv-rotation-pr21038-aime25`
- `目标读者`: `AI 研究者、工程师、模型推理优化关注者`
- `切入角度`: `为什么一个 KV rotation PR 值得被当作今日高优先级技术题：从 AIME25 推理性能损失恢复看量化优化新方向`
- `核心论点`: `llama.cpp PR #21038 有 GitHub 一手信源和可解释的技术机制，虽然受众垂直，但在知乎最容易沉淀成高质量技术解读，且能体现同行资本对 AI infra 的判断力。`
- `证据抓手`: `GitHub PR #21038、AIME25 基准描述、KV rotation 机制说明`
- `source_ref_bundle`: `https://github.com/ggerganov/llama.cpp/pull/21038 | https://old.reddit.com/r/LocalLLaMA/comments/1s720r8/`
- `视觉建议`: `PR 截图 + AIME25 关键数字图表 + KV rotation 简图`
- `为什么适合该平台`: `知乎是本轮 continuity 里最适合承接技术可信度内容的平台，能避免把技术题硬塞到泛流量平台`

#### Task 2
- `status`: `disabled_for_continuity_only`
- `原因`: `本轮 continuity_only 只保留 1 个知乎槽位；Carlini 可在下一轮 premium lane 恢复后作为知乎备选`

### `x`
- `status`: `holdout_for_continuity_only`
- `原因`: `本轮先保留中文主阵地 3 平台；X thread 可在 premium lane 恢复后用 Sora 或 llama.cpp 补上`

### `bilibili`
- `status`: `holdout_for_continuity_only`
- `原因`: `视频产能占用更重；Voxtral 叙事仍待修，暂不在 continuity_only 阶段开视频槽位`

### `toutiao`
- `status`: `holdout_for_continuity_only`
- `原因`: `Moonshot 题材更适合头条，但融资数字未修正前不应下发；先留待补证后恢复`

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: `否（本轮不单独立题）`
- `理由`: `continuity_only 阶段仅保 3 平台最小可运行面；Sora 主稿（wechat）作为本轮唯一确定 Premium 锚点，百家号 SEO 镜像优先承接此稿`
- `承接哪篇主稿更优`: `wechat / ai-video-sora-shutdown-openai-pivot（Sora 关停 22/30，Premium 级全球锚点）`
- `百家号 SEO 镜像升格条件`: `#3 Moonshot 复评通过后，该融资题可独立作为中国大模型赛道 SEO 锚点进入 baijiahao；届时建议双镜像（Sora + Moonshot）`

## Holdout 清单

### `moonshot-ai-1b-funding-kimi-claw-revenue`
- `为什么能进最终池`: `中国大模型融资与商业化强信号，方向正确（$1B 融资目标 $18B 估值）；Kimi Claw 20 天超 2025 全年 + 8280% 月增，商业化叙事强；#3 融资数字已于 13:52 CST 修正`
- `为什么这轮没选`: `rework 已完成（$500M / $4.3B / $8.5B+），但尚未经 market-editor 复评；scorecard v4 尚未将本条纳入 mini_slate；Top3 以外需等待新一轮评分方可升格`
- `什么时候可捞回`: `market-editor 复评通过（预期 8+）后，优先补回 wechat 第二槽位或 toutiao；可作为中国大模型主战场核心锚点`

### `voxtral-tts-mistral-ai-voice-cloning-open-source`
- `为什么能进最终池`: `Mistral AI 开源 TTS + 3秒克隆 + CC许可 + 9语言 + 与 XTTS 竞争，核心叙事强；赛道匹配高；#6 Voxtral 叙事已于 13:52 CST 修正（删"社区修复"，改为"voice cloning 官方尚在路线图"）`
- `为什么这轮没选`: `rework 已完成，但尚未经 market-editor 复评；当前 continuity_only 阶段仅保 Top3；视频槽位（bilibili）在复评前暂不开放`
- `什么时候可捞回`: `market-editor 复评通过后，优先回补 bilibili 或 x 平台；Mistral AI 开源 TTS 视频适配性强`

### `claude-code-no-coder-6-products一人公司叙事`
- `为什么能进最终池`: `一人公司 / AI 创业叙事有天然引流价值，小红书适配强`
- `为什么这轮没选`: `本轮 continuity_only 只保 3 平台 1 槽位，优先级低于 Sora / Carlini / llama.cpp`
- `什么时候可捞回`: `下一轮 premium lane 恢复双槽位时，优先补回 xiaohongshu`
