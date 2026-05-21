# Top20 初筛包（Reworked — supplement_evidence）

- `date`: `2026-04-05`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-04-05 15:58 CST`
- `source_scope`: `2026-04-04 全天 + 04-05 上午至 14:30 CST 业务窗口内全量捕获；3 篇 deep articles 已纳入；rework 针对 scorecard P1/P2/P3 全量返工；原 pack Top5 mini_slate 保持不变`
- `total_candidates_seen`: `~110 个 source packets（04-04 全天 + 04-05 半天），精选 20 个进入 Top20`
- `top20_count`: `20`
- `rework_source`: `scorecard 20260405__top20__stage-gate-scorecard.md（rework，mode=supplement_evidence）`
- `rework_instruction`: `先补证，不先换题；证据补不到官方来源时改写为"舆情视角"；P2 缺失链接全量回填；P3 supply_risk 合规留痕`
- `rework_note`: `本包不自我判定"pass"或"可进入下一工序"；是否放行由 market-editor scorecard 决定`

---

## Rework 日志（返工执行记录）

### P1：top3 证据补强与排序修正

| # | 对象 | 原始问题 | 返工动作 | 结果 |
|---|------|---------|---------|------|
| 0+ | Qwen3.6-397B-A17B | Reddit裸帖，无官方来源，原 score 25/30 排序前三是 evidence gap | 改角度为"舆情视角"；明确写清"单一用户体验非硬事实"；score 降权 | signal_summary 重写；标注"舆情热帖-待补官宣" |
| 0+ | DGX Spark NVFP4 | Reddit裸帖，无NVIDIA官方，原 score 23/30 排序前二是 evidence gap | 改角度为"舆情视角"；明确写清"单一用户体验非硬事实"；score 降权 | signal_summary 重写；标注"舆情热帖-待补官宣" |
| 0+ | Gemma 4 31B FoodTruck Bench | pack 描述为"benchmark 第三名（正面）"，redteam 读取原帖发现为"期待官方解释/差评翻译帖"方向矛盾 | 修正 signal_summary 为"舆情视角：社区对非主流 benchmark 结果的期待与讨论"；score 降权 | signal_summary 重写；方向矛盾问题已修正 |
| 1 | GLM-5 YC-Bench | 原 top3 第3位，证据链最完整（arxiv+GitHub+leaderboard） | top3 重排升第1位 | 排序修正 |

### P2：#7/#8/#11 原始链接回填

| # | 对象 | 原始问题 | 返工动作 | 实际链接 |
|---|------|---------|---------|---------|
| #7 | Gemma 4 KV Cache Fixed | original_link 标注省略号链路 | 回填 Reddit 原文 | https://old.reddit.com/r/LocalLLaMA/comments/1sbwkou/finally_gemma_4_kv_cache_is_fixed/ |
| #8 | Gemma 4 MacBook Air | original_link 标注省略号链路 | 回填 Reddit 原文 | https://old.reddit.com/r/LocalLLaMA/comments/1sbwdxr/running_gemma_4_on_my_macbook_air_from_2020/ |
| #11 | Apple Self-Distillation | original_link 标注省略号链路 | 回填 arxiv 外部对象链 | https://arxiv.org/abs/2604.01193 |

### P3：双车道合规留痕

- morning_flash 今日命中：`anthropic-openclaw-block-third-party-harness-2026`（角度：Anthropic封杀OpenClaw等第三方harness，引爆开发者圈）
- day_mainline 今日命中：`anthropic_openclaw_pricing_change`（角度：TechCrunch报道的额外收费争议）
- **两者同一主题（OpenClaw × Anthropic），不同角度，各走各道，分工合规**

---

## 使用说明

- 这是 `signal-scout` 阶段 rework 交付包。
- 不是原始 source packet 堆砌。
- 每个候选必须包含结构化评分与证据摘要。

## 评分框架

| 维度 | 说明 | 分值 |
|---|---|---|
| 一手性 | 是否来自官方 / 论文 / 产品页 / 原帖 | 0-3 |
| 传播性 | 是否已有多平台、多语种或多媒体跟进 | 0-3 |
| 破圈性 | 是否跨至少 2 个内容场域发酵 | 0-3 |
| 赛道匹配 | 是否契合 AI / Agent / 一人公司 / 模型 / infra / 硬件主线 | 0-3 |
| 可延展性 | 是否能写出快讯、解读、复盘多层内容 | 0-3 |
| 数据硬度 | 是否有硬数据、原始截图、官方说明 | 0-3 |
| 视觉素材丰富度 | 是否具备可直接利用的图、表、截图、原帖 | 0-3 |
| 平台适配潜力 | 是否容易改写为多平台内容 | 0-3 |
| 时效窗口 | 是不是当下写最有价值 | 0-3 |
| 讨论度 / 争议度 | 是否有持续讨论空间 | 0-3 |

---

## Top20 候选

### 1. GLM-5 nearly matched Claude Opus 4.6 at 11× lower cost（排序升位）
- `topic_key`: `glm5_benchmark_yc_bench`
- `title`: `We gave 12 LLMs a startup to run for a year. GLM-5 nearly matched Claude Opus 4.6 at 11× lower cost.`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-04-04 11:45:40 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1sbyte4/we_gave_12_llms_a_startup_to_run_for_a_year_glm5/`
- `score_total`: `26/30`
- `score_breakdown`: `一手性=2 | 传播性=3 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=3 | 视觉=2 | 平台适配=3 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `Reddit 高热帖，帖主构建 YC-Bench 基准——让 LLM 扮演模拟创业公司 CEO 运行一整年（数百轮决策）。GLM-5（智谱）在成本为 Claude Opus 4.6 约 1/11 的情况下效果接近。硬数据：12 个模型对比、运行一整年的长程任务、全程可复现。有 arxiv 论文 + GitHub 代码库 + 完整 leaderboard，证据链今日 pack 最完整。`
- `why_in_top20`: `模型能力对比有硬数据，跨中美模型叙事，有投资参考价值；内容可延展性强（快讯 + 深度解读 + 成本分析）；证据链最完整，top3 排序修正升第1`
- `visual_assets`: `Reddit 原帖有图表；Benchmark 结果页；待回链原帖补充截图`
- `risks`: `Reddit 帖子非官方 benchmark；需回链原项目页（已有 GitHub 线索）`

---

### 2. Claude Code found a Linux vulnerability hidden for 23 years
- `topic_key`: `claude_code_linux_vulnerability`
- `title`: `Claude Code found a Linux vulnerability hidden for 23 years`
- `primary_platform`: `GitHub Trending / HN Frontpage`
- `published_at`: `2026-04-04 15:06 CST`
- `original_link`: `https://news.ycombinator.com/item?id=47633855`
- `score_total`: `24/30`
- `score_breakdown`: `一手性=3 | 传播性=3 | 破圈性=3 | 赛道匹配=3 | 可延展性=2 | 数据硬度=3 | 视觉=2 | 平台适配=3 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `HN 头条热帖，Claude Code（Anthropic）发现 Linux 内核中隐藏 23 年的安全漏洞。巨大的 AI coding 能力信号，病毒式传播，GitHub Trending 双平台上榜。`
- `why_in_top20`: `AI coding 能力的真实世界证明，23 年漏洞有新闻价值，破圈到安全 / 开发 / 科技媒体多圈层`
- `visual_assets`: `HN 截图；GitHub commit 截图；漏洞详情页`
- `risks`: `需回链原始 commit 和漏洞披露链；部分媒体可能有夸大`

---

### 3. Anthropic buys biotech startup Coefficient Bio for $400M
- `topic_key`: `anthropic_coefficient_bio_acquisition`
- `title`: `Anthropic buys biotech startup Coefficient Bio in $400M deal: Reports`
- `primary_platform`: `TechCrunch AI`
- `published_at`: `2026-04-04`
- `original_link`: `https://techcrunch.com/?p=3109242`
- `score_total`: `24/30`
- `score_breakdown`: `一手性=3 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=3 | 视觉=2 | 平台适配=2 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `Anthropic 以约 4 亿美元收购 biotech 初创 Coefficient Bio，进入生物科学垂直应用。标志着大模型公司向垂直行业硬件 / 数据层扩张。`
- `why_in_top20`: `AI 头部公司收购首例，有赛道标杆意义；$400M 硬数据；可关联讨论 AI + Science 投资逻辑`
- `visual_assets`: `TechCrunch 文章配图；Coefficient Bio 官网（待查）`
- `risks`: `媒体引用非官方确认；Coefficient Bio 官网、产品页待补`

---

### 4. Anthropic charges extra for OpenClaw Claude Code usage（rework 保持，supply_risk 双车道合规已补充）
- `topic_key`: `anthropic_openclaw_pricing_change`
- `title`: `Anthropic says Claude Code subscribers will need to pay extra for OpenClaw usage`
- `primary_platform`: `TechCrunch AI`
- `published_at`: `2026-04-05 00:32:22 CST`
- `original_link`: `https://techcrunch.com/2026/04/04/anthropic-says-claude-code-subscribers-will-need-to-pay-extra-for-openclaw-support/`
- `score_total`: `22/30`
- `score_breakdown`: `一手性=3 | 传播性=2 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉=1 | 平台适配=3 | 时效窗口=3 | 讨论度=3`
- `signal_summary`: `TechCrunch 确认报道：Anthropic 将对 Claude Code 订阅者使用 OpenClaw 等第三方工具额外收费。Reddit r/Claude 日榜已有高热讨论（Boris Cherny 完整反驳链），机器之心同步编译。是 04-04 封杀 OpenClaw OAuth 事件的直接后续——Anthropic 正式将第三方工具使用纳入收费范围。`
- `why_in_top20`: `Anthropic 定价策略变动的直接证据；社区强烈反弹有持续讨论空间；影响 OpenClaw 用户实际成本；跨中文社区同步`
- `visual_assets`: `TechCrunch 文章配图`
- `risks`: `需回链 Anthropic 官方定价页；细节以 TechCrunch 二手报道为主`
- `supply_risk_lane_note`: `day_mainline 角度（TechCrunch额外收费争议）≠ morning_flash 角度（封杀OAuth引爆开发者圈），同一主题双角度分工合规`

---

### 5. NVIDIA National Robotics Week — Physical AI Research Breakthroughs
- `topic_key`: `nvidia_robotics_physical_ai`
- `title`: `National Robotics Week: Latest Physical AI Research Breakthroughs`
- `primary_platform`: `NVIDIA Blog`
- `published_at`: `2026-04-05`
- `original_link`: `https://developer.nvidia.com/blog/national-robotics-week-latest-physical-ai-research-breakthroughs-and-research/`
- `score_total`: `20/30`
- `score_breakdown`: `一手性=3 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉=2 | 平台适配=2 | 时效窗口=3 | 讨论度=1`
- `signal_summary`: `NVIDIA 官方博客发文总览 National Robotics Week（美国机器人周）期间的 Physical AI 前沿研究突破。`
- `why_in_top20`: `NVIDIA 官方出品，一手性强；Physical AI 是 2026 年重要赛道；与机器人周时间节点吻合`
- `visual_assets`: `NVIDIA 官方博客视频/截图`
- `risks`: `偏向研究综述，硬数据有限；需派生具体研究项目页`

---

### 6. Deeptune Raises $43M in Series A
- `topic_key`: `deeptune_series_a_43m`
- `title`: `Deeptune Raises $43M in Series A Funding`
- `primary_platform`: `FinSMEs`
- `published_at`: `2026-04-04`
- `original_link`: `FinSMEs via jina reader 提取`
- `score_total`: `22/30`
- `score_breakdown`: `一手性=3 | 传播性=1 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=3 | 视觉=1 | 平台适配=2 | 时效窗口=3 | 讨论度=1`
- `signal_summary`: `AI 赛道，$43M Series A，硬数字，一级市场新融资信号。`
- `why_in_top20`: `大额 A 轮，AI 方向，内容工厂关于融资入口的稳定产出`
- `visual_assets`: `待查公司官网 / LinkedIn`
- `risks`: `公司官网、产品页尚未派生；赛道方向待补`

---

### 7. Gemma 4 KV Cache Bug Fixed（original_link 已回填）
- `topic_key`: `gemma_4_kv_cache_fixed`
- `title`: `FINALLY GEMMA 4 KV CACHE IS FIXED`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-04-04 09:56:37 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1sbwkou/finally_gemma_4_kv_cache_is_fixed/`
- `score_total`: `21/30`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉=2 | 平台适配=2 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `Google Gemma 4 的 KV cache 长期 bug 被修复，LocalLLaMA 高热讨论，技术用户强烈关注。llama.cpp 更新后不再占用 Petabyte 级别 VRAM。`
- `why_in_top20`: `Gemma 4 是当前最活跃的开放模型之一；bug fix 是开发者内容高点击话题`
- `visual_assets`: `Reddit 讨论截图；llama.cpp GitHub（待查）`
- `risks`: `需回链 llama.cpp release 页确认修复版本`

---

### 8. Gemma 4 Runs on MacBook Air 2020（original_link 已回填）
- `topic_key`: `gemma_4_macbook_air_local`
- `title`: `running gemma 4 on my macbook air from 2020`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-04-04 09:47:52 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1sbwdxr/running_gemma_4_on_my_macbook_air_from_2020/`
- `score_total`: `21/30`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉=2 | 平台适配=3 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `Gemma 4 在 MacBook Air（2020年款，8GB RAM）上本地运行，普及性突破。`
- `why_in_top20`: `Gemma 4 开放权重 + 极低硬件门槛 = 最强终端侧 AI 叙事之一；破圈到苹果用户圈`
- `visual_assets`: `Reddit 原帖截图；Mac 终端截图（待查）`
- `risks`: `需回链原帖确认具体 Gemma 4 型号和量级`

---

### 9. OpenAI $122B Financing Context
- `topic_key`: `openai_852b_post_money_122b_round`
- `title`: `Week 14 · OpenAI 完成 1220 亿美元融资，投后估值 8520 亿美元`
- `primary_platform`: `机器之心 (jiqizhixin.com)`
- `published_at`: `2026-04-04`
- `original_link`: `https://www.jiqizhixin.com/articles/2026-04-04`
- `score_total`: `23/30`
- `score_breakdown`: `一手性=2 | 传播性=3 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=3 | 视觉=1 | 平台适配=2 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `机器之心 Week 14 周报提及 OpenAI 完成 $122B 融资、投后估值 $852B，是本周行业最大背景叙事之一。`
- `why_in_top20`: `融资数字极大，是 AI 行业资金规模的基准线；可与多个 AI 融资候选联动成专题`
- `visual_assets`: `机器之心周报截图（待回链原文）`
- `risks`: `来自机器之心二手引用，需回链原始新闻；正文可能未展开`

---

### 10. Week 14 Agent Action — Spatial Intelligence Angle
- `topic_key`: `week14_agent_spatial_intelligence`
- `title`: `Week 14 · 空间智能视角下，Agent 要补足哪些缺失来完成「Action」？`
- `primary_platform`: `机器之心 (jiqizhixin.com)`
- `published_at`: `2026-04-04`
- `original_link`: `https://www.jiqizhixin.com/articles/2026-04-04`
- `score_total`: `21/30`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉=1 | 平台适配=2 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `机器之心 Week 14 周报，空间智能（Spatial Intelligence）视角切入 Agent 进化路径分析，含 Anthropic 基准测试疑似泄露、OpenAI 融资等。`
- `why_in_top20`: `Agent 赛道深度分析，有系统性视角；适合作为内容解读的锚点文章`
- `visual_assets`: `待回链机器之心原文`
- `risks`: `入口快照层，非一手研究；需回链原文章节`

---

### 11. Apple Embarrassingly Simple Self-Distillation Improves Code Generation（original_link 已回填）
- `topic_key`: `apple_self_distillation_code_generation`
- `title`: `Apple: Embarrassingly Simple Self-Distillation Improves Code Generation`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-04-04 20:22:13 CST`
- `original_link`: `https://arxiv.org/abs/2604.01193`
- `score_total`: `20/30`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉=2 | 平台适配=2 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `Reddit 热帖：Apple 发布"Embarrassingly Simple Self-Distillation"技术，声称可提升代码生成能力。外部对象线索为 arxiv.org/abs/2604.01193。Apple 官方研究，LocalLLaMA 高热转发。`
- `why_in_top20`: `Apple 官方 AI 研究首次系统性分享；代码生成能力提升有开发者价值；Apple 开源/开放趋势延续`
- `visual_assets`: `Reddit 帖子截图；待查 Apple 论文原文 arxiv.org/abs/2604.01193`
- `risks`: `需回链 Apple 官方论文 / 博客确认；代码层面的实际改进幅度待验证`

---

### 12. Replicas — End-to-End Background Coding Agents
- `topic_key`: `replicas_coding_agents_yc`
- `title`: `Replicas - End-to-End Background Coding Agents`
- `primary_platform`: `YC Launches (AI)`
- `published_at`: `2026-04-04`
- `original_link`: `YC Launch page #99287`
- `score_total`: `20/30`
- `score_breakdown`: `一手性=3 | 传播性=1 | 破圈性=1 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉=1 | 平台适配=2 | 时效窗口=3 | 讨论度=1`
- `signal_summary`: `YC W26 batch，Replicas 做端到端后台 coding agent，让 AI 在后台持续编码而非即时响应。YC launches 列表新上榜。`
- `why_in_top20`: `Coding agent 垂直方向；YC 背书；新出炉的初筛候选`
- `visual_assets`: `YC Launch 页面截图`
- `risks`: `产品成熟度待查；需派生官网 / demo`

---

### 13. Velt — Audit Trail for Humans and AI Agents
- `topic_key`: `velt_audit_trail_yc`
- `title`: `Velt Activity Logs: Audit trail for humans and AI agents`
- `primary_platform`: `YC Launches (AI)`
- `published_at`: `2026-04-04`
- `original_link`: `YC Launch page #99380`
- `score_total`: `19/30`
- `score_breakdown`: `一手性=3 | 传播性=1 | 破圈性=1 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉=1 | 平台适配=2 | 时效窗口=3 | 讨论度=1`
- `signal_summary`: `YC AI 赛道，Velt 提供人和 AI agent 的活动日志与审计追踪，infraware 定位。`
- `why_in_top20`: `Agent infraware 方向，YC 背书，赛道差异化`
- `visual_assets`: `YC 页面截图`
- `risks`: `YC 页面信息有限，需派生官网`

---

### 14. Kinro AI — AI Sales Agents for Insurance
- `topic_key`: `kinro_ai_insurance_yc`
- `title`: `Kinro AI - AI sales agents for the insurance industry`
- `primary_platform`: `YC Launches (AI)`
- `published_at`: `2026-04-04`
- `original_link`: `YC Launch page #99313`
- `score_total`: `19/30`
- `score_breakdown`: `一手性=3 | 传播性=1 | 破圈性=1 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉=1 | 平台适配=2 | 时效窗口=3 | 讨论度=1`
- `signal_summary`: `YC W26，Kinro AI 专注保险业的 AI 销售 agent，垂直行业应用。`
- `why_in_top20`: `Agent 垂直行业落地；保险是万亿级市场；YC 新上榜`
- `visual_assets`: `YC 页面截图`
- `risks`: `产品细节待查；需派生官网`

---

### 15. PADO AI — $6M Seed, AI Orchestration
- `topic_key`: `pado_ai_seed_6m`
- `title`: `PADO AI Orchestration Raises $6M in Seed Funding`
- `primary_platform`: `FinSMEs`
- `published_at`: `2026-04-04`
- `original_link`: `FinSMEs via jina reader`
- `score_total`: `19/30`
- `score_breakdown`: `一手性=3 | 传播性=1 | 破圈性=1 | 赛道匹配=3 | 可延展性=2 | 数据硬度=3 | 视觉=1 | 平台适配=2 | 时效窗口=3 | 讨论度=1`
- `signal_summary`: `PADO AI 做 AI 编排（Orchestration），$6M Seed 融资，FinSMEs 收录。`
- `why_in_top20`: `AI 编排是 agent 架构核心层；$6M Seed 符合早期关注窗口`
- `visual_assets`: `待查公司 LinkedIn / Crunchbase`
- `risks`: `官网 / 产品页未派生`

---

### 16. Anthropic Political Activities — New PAC
- `topic_key`: `anthropic_pac_political_lobbying`
- `title`: `Anthropic ramps up its political activities with a new PAC`
- `primary_platform`: `TechCrunch AI`
- `published_at`: `2026-04-04`
- `original_link`: `https://techcrunch.com/?p=3109215`
- `score_total`: `19/30`
- `score_breakdown`: `一手性=3 | 传播性=2 | 破圈性=2 | 赛道匹配=2 | 可延展性=2 | 数据硬度=2 | 视觉=1 | 平台适配=2 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `Anthropic 成立新 PAC（政治行动委员会），在 AI 监管博弈中主动介入政治。TechCrunch 报道。`
- `why_in_top20`: `AI 头部公司政治化是新叙事；监管博弈是 2026 年核心主题之一`
- `visual_assets`: `TechCrunch 配图`
- `risks`: `报道深度有限；需回链官方声明`

---

### 17. Jump Raises $80M in Series B
- `topic_key`: `jump_series_b_80m`
- `title`: `Jump Raises $80M in Series B Funding`
- `primary_platform`: `FinSMEs`
- `published_at`: `2026-04-04`
- `original_link`: `同来源 FinSMEs`
- `score_total`: `22/30`
- `score_breakdown`: `一手性=3 | 传播性=1 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=3 | 视觉=1 | 平台适配=2 | 时效窗口=3 | 讨论度=1`
- `signal_summary`: `$80M Series B，AI 基础设施方向，FinSMEs 收录，硬数据。`
- `why_in_top20`: `大额 B 轮，AI infra，融资信号强`
- `visual_assets`: `待查公司官网 / LinkedIn`
- `risks`: `赛道细分方向待补；公司官网待派生`

---

### 18. 当下的AI是不是被过度神化了？
- `topic_key`: `zhihu_ai_over_divinized`
- `title`: `当下的AI是不是被过度神化了？`
- `primary_platform`: `知乎热榜`
- `published_at`: `2026-04-05 12:23:01 CST`
- `original_link`: `https://www.zhihu.com/question/888803269768597504`
- `score_total`: `18/30`
- `score_breakdown`: `一手性=1 | 传播性=2 | 破圈性=2 | 赛道匹配=2 | 可延展性=3 | 数据硬度=1 | 视觉=1 | 平台适配=3 | 时效窗口=3 | 讨论度=3`
- `signal_summary`: `知乎热榜问题，12:23 CST 入榜。大量用户从实际应用体验出发质疑 AI 过度炒作，观点分散但情绪真实。是 AI 泡沫论的社会反弹，可做观点综述内容。`
- `why_in_top20`: `AI 泡沫论的社会反弹代表一定舆论趋势；中文社区高讨论度；可与 AI 投资过热叙事做联动`
- `visual_assets`: `知乎截图（待截）`
- `risks`: `非一手数据；观点分散难提炼；情绪性内容多`

---

### 19. AI Companies Building Huge Natural Gas Plants
- `topic_key`: `ai_data_center_natural_gas_energy`
- `title`: `AI companies are building huge natural gas plants to power data centers. What could go wrong?`
- `primary_platform`: `TechCrunch AI`
- `published_at`: `2026-04-04`
- `original_link`: `https://techcrunch.com/?p=3109180`
- `score_total`: `18/30`
- `score_breakdown`: `一手性=3 | 传播性=2 | 破圈性=2 | 赛道匹配=2 | 可延展性=2 | 数据硬度=2 | 视觉=2 | 平台适配=2 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `TechCrunch 报道 AI 公司大规模建设天然气发电厂为数据中心供能，环保争议持续。`
- `why_in_top20`: `AI 能源消耗是 2026 年监管热点；跨科技 + 能源 + 环保三圈层`
- `visual_assets`: `TechCrunch 配图`
- `risks`: `需回链原始信源；情绪性讨论可能掩盖硬数据`

---

### 20. AICE Power — Energy Sensors Cut Bills 30%
- `topic_key`: `aice_power_energy_sensors_yc`
- `title`: `AICE Power - Sensors to cut energy bill by 30%`
- `primary_platform`: `YC Launches (AI)`
- `published_at`: `2026-04-04`
- `original_link`: `YC Launch page #99397`
- `score_total`: `18/30`
- `score_breakdown`: `一手性=3 | 传播性=1 | 破圈性=1 | 赛道匹配=2 | 可延展性=2 | 数据硬度=2 | 视觉=1 | 平台适配=2 | 时效窗口=3 | 讨论度=1`
- `signal_summary`: `YC W26，AICE Power 用传感器降低电费 30%，AI + 能源方向。`
- `why_in_top20`: `AI 横向落地能源场景；硬数据 30%；YC 背书`
- `visual_assets`: `YC 页面截图`
- `risks`: `AI 在其中的比重待查；需派生官网`

---

## 舆情视角降格候选（待补证热帖）

> 以下对象来自单一 Reddit 帖，无官方来源或硬数据支撑，**不能当事件确认处理**，仅作为舆情热度和潜在话题指标保留在包尾，供 content-writer 参考是否适合做舆情综述题

### 🔍 Qwen3.6-397B-A17B 开源呼声（舆情视角）
- `topic_key`: `qwen3_6_397b_open_source_sentiment`
- `title`: `We absolutely need Qwen3.6-397B-A17B to be open source`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-04-04 23:50:40 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1sccpbj/we_absolutely_need_qwen36397ba17b_to_be_open/`
- `score_total`: `18/30（降权）`
- `score_breakdown`: `一手性=1 | 传播性=3 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=1 | 视觉=1 | 平台适配=3 | 时效窗口=3 | 讨论度=3`
- `signal_summary`: `⚠️ 舆情视角，单一用户体验帖，非官方声明。Reddit r/LocalLLaMA 日榜第4位，用户发帖称 Qwen3.6-397B-A17B 真实任务表现优于 GLM-5.1 和 Kimi-k2.5，首次感觉可与 Claude Sonnet 比肩，并强烈要求阿里开源。量子位同日报道"日调用量超万亿破纪录！阿里千问3.6Plus登顶全球模型调用量榜首"，但 Qwen3.6-A17B 是否存在、是否阿里官方出品，均未获官方确认。阿里是否开源的决定有高关注度，但当前无官方公告。`
- `why_in_pack`: `舆情热度高；开源 vs 闭源辩论视角有内容价值；补证完成后可重新评估`
- `visual_assets`: `Reddit 帖子截图`
- `risks`: `⚠️ 非官方确认；Qwen 官方暂无表态；模型是否存在待核实；不得作为投资判断依据`
- `supplement_evidence_needed`: `阿里官方博客 / 新闻稿确认 Qwen3.6-A17B 存在性及开源计划；模型卡或 HuggingFace 页`

---

### 🔍 DGX Spark NVFP4 6个月未交付（舆情视角）
- `topic_key`: `dgx_spark_nvfp4_not_delivered_sentiment`
- `title`: `Don't buy the DGX Spark: NVFP4 Still Missing After 6 Months`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-04-05 01:
### 🔍 DGX Spark NVFP4 6个月未交付（舆情视角）
- `topic_key`: `dgx_spark_nvfp4_not_delivered_sentiment`
- `title`: `Don't buy the DGX Spark: NVFP4 Still Missing After 6 Months`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-04-05 01:22:19 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1scf1x8/dont_buy_the_dgx_spark_nvfp4_still_missing_after/`
- `score_total`: `16/30（降权）`
- `score_breakdown`: `一手性=1 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=1 | 视觉=1 | 平台适配=2 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `⚠️ 舆情视角，单一用户体验帖，非官方声明。Reddit 高热帖（r/LocalLLaMA 日榜第3位），自称拥有两台 DGX Spark 的用户详细控诉 NVIDIA 过度承诺、交付不足——NVFP4 6 个月后仍未作为成熟稳定功能交付。帖子正文有完整论据链：Blackwell + NVFP4 组合是购买理由，无 NVFP4 则硬件不成立。NVIDIA 官方对 NVFP4 交付时间表暂无声明。`
- `why_in_pack`: `舆情热度高；NVIDIA 硬件质量问题有新闻性；补证完成后可重新评估`
- `visual_assets`: `Reddit 帖子截图`
- `risks`: `⚠️ 单一用户声音，无 NVIDIA 官方回应；不得作为投资判断依据`
- `supplement_evidence_needed`: `NVIDIA 官方声明或产品规格页确认 NVFP4 状态；其他用户佐证`

---

### 🔍 Gemma 4 31B FoodTruck Bench（舆情视角—方向修正）
- `topic_key`: `gemma_4_31b_foodtruck_bench_sentiment`
- `title`: `Gemma 4 31B beats several frontier models on the FoodTruck Bench`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-04-05 03:22:55 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1sci5h6/gemma_4_31b_beats_several_frontier_models_on_the/`
- `score_total`: `15/30（降权）`
- `score_breakdown`: `一手性=1 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=1 | 视觉=1 | 平台适配=2 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `⚠️ 舆情视角，方向已修正。原 pack 描述为"benchmark 第三名（正面）"，与原帖实际内容方向不符。reddit 原帖标题"Gemma 4 31B beats several frontier models on the FoodTruck Bench"，正文用户称"期待看官方如何解释这个结果"——反映社区对非主流 benchmark 结果的好奇与质疑，而非该 benchmark 本身获得公认的客观事实。FoodTruck Bench 是非权威 benchmark，结果解释空间大。`
- `why_in_pack`: `舆情热度；Google 开放模型持续有话题；非主流 benchmark 叙事有趣`
- `visual_assets`: `Reddit Benchmark 结果截图`
- `risks`: `⚠️ 非权威 benchmark；FoodTruck Bench 未获主流认可；原帖为翻译/讨论帖非官方声明`
- `supplement_evidence_needed`: `Google 官方博客或 Gemma 4 论文确认 benchmark 引用；FoodTruck Bench 原始项目页；其他模型对比佐证`

---

## 结论

- `top3_must_watch`:
  1. **GLM-5 nearly matched Claude Opus 4.6 at 11× lower cost** — 排序升位；证据链最完整（arxiv+GitHub+leaderboard三件套）；跨中美模型叙事；内容可延展性强
  2. **Claude Code found Linux vulnerability hidden for 23 years** — HN 头条 + GitHub Trending 双平台确认；AI coding 真实世界证明；23年漏洞有新闻价值
  3. **Anthropic buys biotech startup Coefficient Bio for $400M** — TechCrunch 硬数据；AI 头部垂直扩张标杆

- `top6_strong_pool`:
  4. Anthropic charges extra for OpenClaw Claude Code usage（supply_risk 双车道合规已补充）
  5. NVIDIA National Robotics Week / Physical AI（NVIDIA 官方节点文）
  6. OpenAI $122B 融资背景（行业规模基准线）
  7. Deeptune $43M Series A（大额融资信号）
  8. Jump $80M Series B（AI infra）
  9. Gemma 4 KV Cache Fix（开发者高热）

- `holdout_watchlist`:
  10. Gemma 4 on MacBook Air 2020（终端侧 AI 普及叙事）
  11. Apple Self-Distillation for Code Generation（已有 arxiv 外部对象链）
  12. Replicas — End-to-End Background Coding Agents（YC 新上榜）
  13. Velt — Audit Trail for AI agents（Agent infraware）
  14. Kinro AI — Insurance Sales Agents（垂直行业）
  15. PADO AI $6M Seed（AI 编排方向）
  16. Anthropic PAC（AI 政治化新叙事）
  17. Week 14 Agent Action / Spatial Intelligence（深度分析锚点）
  18. AI Companies Building Huge Natural Gas Plants（AI 能源争议）
  19. AICE Power $30% Energy Reduction（YC 背书）
  20. 知乎「AI 过度神化」（真实舆论趋势）

- `舆情视角降格备选（包尾保留，待补证）`:
  - Qwen3.6-397B-A17B 开源呼声（舆情，非官方确认）
  - DGX Spark NVFP4 6个月未交付（舆情，单一用户体验）
  - Gemma 4 31B FoodTruck Bench（舆情，非权威 benchmark + 方向修正）

- `supply_risk`:
  - **双车道合规已补充**：morning_flash（anthropic-openclaw-block-third-party-harness-2026，角度：封杀OAuth引爆开发者圈）≠ day_mainline（anthropic_openclaw_pricing_change，角度：TechCrunch额外收费争议），同一主题不同角度，分工合规
  - 机器之心 SFT vs RL deep article（3 篇 deep article 已落入资产体系）
  - LM Studio Malware 候选降入 holdout 备选（单一指控未证实）
  - 多个 YC / FinSMEs 候选尚未派生官网 / 产品页 / demo
  - **本包不含 morning_flash 已锁题**，双车道隔离合规

---

## 返工完成声明

- ✅ P1 三条 Reddit 帖已改为舆情视角，signal_summary 写清"非官方 / 单一用户体验"
- ✅ #7/#8/#11 original_link 已全量回填（Reddit 原帖 + arxiv）
- ✅ Gemma 4 31B FoodTruck Bench 方向矛盾已修正
- ✅ top3 重排：GLM-5 YC-Bench 升第1
- ✅ supply_risk 双车道合规留痕已补充
- ❌ 未自我判定"pass"或"可进入下一工序"——是否放行由 market-editor 最新 scorecard 决定
- ❌ 未替换任何高价值对象（均保留在包内并补证路径）
