# 平台任务单

- `date`: `2026-04-30`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-30 16:08 CST`
- `input_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260430__top20-screening-pack.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `rework + continuity_only + Top5 final → limited task sheet；wechat 2槽 + 最多2平台各1槽；其余进 holdout`
- `top5_board_ref`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260430__daily-top8-to-top5.md`
- `scorecard_ref`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260430__top20__stage-gate-scorecard.md`
- `continuity_notice`: `本单为 continuity_only limited sheet；所有 active slot 必须回链 Top5/Holdout 板候选；正文补证纪律严格，官方/原始来源未齐不得发稿`

---

## 全局主池 Top6

> 本轮为 continuity_only limited sheet；Top5 板实收 5 个候选，Top6 槽位空缺，已在 Holdout 中标注可捞回对象。

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|------|-----------|----------|--------------|----------|
| 1 | `openai_model_behavior_training_reinforcement` | 模型行为问题正处热点，HN/Reddit 多平台扩散，有技术解释和修复语境 | 解读+复盘+快讯多形态；话题稀缺性高 | 需回链 OpenAI 原文并确认发布时间；技术细节需降维 |
| 2 | `zig_open_source_anti_ai_policy` | 开发者社区价值立场分歧，多平台讨论充分，话题有延续性 | 观点类/争议类内容；差异化强 | 需回链 Zig 官方立场声明原文；观点类需立场均衡 |
| 3 | `onchain_lm_agent_reliability_real_capital` | 真实资本+大规模 trace 的 agent 可靠性研究，有硬数据，方法论突破信号 | 技术深度解读稀缺素材；品牌贴合度高 | arXiv 预印本需同行评审背书；中文需英文回链 |
| 4 | `anthropic_vs_openai_cn_media_debate` | 2026 年 AI 圈最核心商业叙事线，36氪强传播力，争议性高 | 快讯+解读+讨论多形态 | 需回链 36kr 原文；多源验证不能只凭媒体标题 |
| 5 | `deepseek_multimodal_vision_confirmed` | 国产模型多模态重大更新，多源验证充分，知乎+微信双平台确认 | 快讯+解读+玩法类多形态输出 | 需回链 DeepSeek 官方公告；灰测中功能边界有调整 |
| 6 | _(空缺) | _ | _ | _ |

---

## 六个主战场任务单

> 本节为 continuity_only limited sheet 占位；实际任务见「三个最重要平台任务单」。

（平台任务详见下一节）

---

## 三个最重要平台任务单

> continuity_only limited sheet：本轮 active slots = 4（wechat×2 + xiaohongshu×1 + zhihu×1 + x×1）；其余平台候选进 holdout。

### `wechat`

#### Task 1
- `topic_key`: `openai_model_behavior_training_reinforcement`
- `目标读者`: AI 开发者、agent 构建者、对模型行为问题感兴趣的技术人群
- `切入角度`: OpenAI 官方复盘——"goblins" 行为是训练数据噪音的产物，而非 bug；这次修复对 agent 生产落地意味着什么
- `核心论点`: 模型行为问题不是偶发事件，而是 RL 训练范式的系统性盲区；从业者需要建立对应的评估和兜底机制
- `证据抓手`: OpenAI 官方复盘文章 + HN 讨论区高赞分析 + 可引用的 benchmark 数据
- `source_ref_bundle`: `https://openai.com/index/where-the-goblins-came-from/`
- `视觉建议`: 流程图——RL training → reward hacking → goblin behavior → fix loop；或对比图：修复前后模型行为差异
- `为什么适合该平台`: 微信适合承载完整叙事和技术判断；该题有明确事件入口+技术解释空间，适合主稿深度展开

#### Task 2
- `topic_key`: `onchain_lm_agent_reliability_real_capital`
- `目标读者`: 对 AI agent 落地感兴趣的投资人、开发者、builder 人群
- `切入角度`: $20M 实盘数据揭示当前 Onchain LM Agent 的真实失败率——不是概念验证，而是生产级可靠性报告
- `核心论点`: Onchain agent 的可靠性瓶颈不在智能程度，在于 operating-layer controls；谁先解决这个问题，谁就拿到下一阶段的核心壁垒
- `证据抓手`: arXiv 预印本 trace 数据 + 真实资本暴露规模 + 方法论设计亮点
- `source_ref_bundle`: `https://arxiv.org/abs/2604.26091`
- `视觉建议`: 数据可视化——不同 operating-layer 策略下的 agent 存活率/成功率对比；时间序列上的资本暴露曲线
- `为什么适合该平台`: 微信适合高信息密度、数据驱动型内容；该题硬数据扎实，适合主稿建立技术权威性
- `补证提醒`: scorecard 标注 arXiv ID 碰撞（#3 与其他条目共享 ID）；发布前必须 signal-scout 确认并修复

---

### `xiaohongshu`

#### Task 1
- `topic_key`: `zig_open_source_anti_ai_policy`
- `目标读者`: 开发者、技术社区关注者、对 AI 伦理有观点的科技爱好者
- `切入角度`: Zig 项目硬刚 AI 贡献政策——一个开源项目为什么宁愿得罪主流也要划清界限？这背后是理想主义还是产品策略？
- `核心论点`: Zig 的 anti-AI 政策不是情绪化反应，而是经过深思熟虑的社区定位选择；值得所有关注开源生态的人认真对待
- `证据抓手`: Simon Willison 深度分析 + Zig 官方立场声明 + 社区讨论反应
- `source_ref_bundle`: `https://simonwillison.net/2026/Apr/30/zig-anti-ai/`
- `视觉建议`: 社区reaction 拼图 + 核心立场金句大字报；或时间线：事件发酵过程
- `为什么适合该平台`: 小红书适合观点鲜明、有争议性、能引发讨论的内容；开发者叙事+价值观冲突天然适合该平台

---

### `zhihu`

#### Task 1
- `topic_key`: `anthropic_vs_openai_cn_media_debate`
- `目标读者`: 关注 AI 行业格局变化的投资人、从业者、科技媒体读者
- `切入角度`: 36氪的报道是真实的市场判断还是过度解读？Anthropic 真的在"颠覆"OpenAI 吗？从商业数据看真实差距
- `核心论点`: Anthropic 的增长值得认真对待，但"颠覆 OpenAI"的叙事过于简化；两者在不同维度各有所长；从 36kr 报道出发，展开真实商业分析
- `证据抓手`: 36kr 原文 + 可比的商业数据（用户数、收入、估值） + 双方近期产品发布节奏
- `source_ref_bundle`: `https://www.36kr.com/p/3788623924949509`
- `视觉建议`: 对比表格——Anthropic vs OpenAI 关键维度对比；或36kr报道核心观点提炼图
- `为什么适合该平台`: 知乎适合分析性、对比性内容；该题天然需要多维度论证和证据对比

---

### `x`

#### Task 1
- `topic_key`: `deepseek_multimodal_vision_confirmed`
- `目标读者`: 关注国产模型进展的 AI 开发者、科技爱好者、中文推友
- `切入角度`: DeepSeek 识图模式上线——实测体验 + 技术原理 + 和 GPT-4V / Claude Vision 的直观对比
- `核心论点`: 国产多模态模型又进了一步，但具体体验和边界仍需实测；这个功能对中国 AI 生态意味着什么
- `证据抓手`: 知乎讨论帖 + DeepSeek 官方公告 + 用户真实反馈截图
- `source_ref_bundle`: `https://www.zhihu.com/question/2032851960177631968`
- `视觉建议`: 截图对比——DeepSeek 识图实测案例；或功能对比表：DeepSeek vision vs GPT-4V
- `为什么适合该平台`: X 适合快讯、热点反应、实时讨论；该题时效性强，适合快速发布观点钩子

---

## 其余平台（无 active slot）

- `bilibili`: 无 active slot；候选 `openai_model_behavior_training_reinforcement` 和 `onchain_lm_agent_reliability_real_capital` 可考虑视频化，但本轮容量已满
- `toutiao`: 无 active slot；候选 `anthropic_vs_openai_cn_media_debate` 适合头条算法分发，但本轮容量已满

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: **是，但优先级低于今日 active slots**
- `理由`: DeepSeek 多模态和 Anthropic vs OpenAI 两个话题在百家号都有搜索流量预期；但今日 limited sheet 平台容量已满，建议作为明日优先候选
- `承接哪篇主稿更优`: `deepseek_multimodal_vision_confirmed` 建议承接微信主稿，做标题党+搜索优化版；`anthropic_vs_openai_cn_media_debate` 适合做知乎主稿的 SEO 镜像

---

## Holdout 清单

### `deepseek_multimodal_vision_confirmed`
- `为什么能进最终池`: 国产模型多模态重大更新，多源验证充分，知乎+微信双平台确认热度，用户真实反馈而非猜测，适合多形态输出
- `为什么这轮没选`: limited task sheet 纪律约束（仅 4 个 active slots），x 平台已占用 `deepseek_multimodal_vision_confirmed`；今日容量不足
- `什么时候可捞回`: 明日平台任务单优先考虑升为正式 active slot；或若 x 平台该题发布后数据好，可追加其他平台衍生版本

### `anthropic_vs_openai_cn_media_debate`
- `为什么能进最终池`: 2026 年 AI 圈最核心商业叙事线，36kr 强传播力背书，争议性高，适合快讯+解读+讨论多形态
- `为什么这轮没选`: limited task sheet 纪律约束；wechat 2 槽给了 OpenAI goblin 和 Onchain agent，xiaohongshu 给了 Zig，zhihu 占了 Anthropic；平台容量已满
- `什么时候可捞回`: 明日早间窗口优先升为 wechat 或 bilibili active slot；或作为 baijiahao SEO 镜像层优先候选

### `onchain_lm_agent_reliability_real_capital`（wechat Task 2 降格说明）
- `为什么能进全局主池`: P0，无条件进入；真实资本+大规模 trace 的稀缺研究
- `为什么保留为 wechat Task 2`: scorecard 显示 arXiv ID 碰撞问题（#3 与其他条目共享同一 ID）；需正文发布前完成来源补证
- `什么时候可捞回`: signal-scout 确认并修复 arXiv ID 后，立即恢复为正式 active slot；建议同步完成后再推进写稿

---

*topic-planner @ 2026-04-30 16:08 CST | stage=platform_task_sheet | status=continuity_only_limited | active_slots=4 | holdout=3 | 来源补证纪律：所有 active slot 正文发布前必须回链官方/原始来源*