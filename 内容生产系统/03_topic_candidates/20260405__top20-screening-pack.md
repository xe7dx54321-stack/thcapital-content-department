# Top20 初筛包

- `date`: `2026-04-05`
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: `2026-04-06 01:40 AM CST`
- `source_scope`: `2026-04-04 全天 + 04-05 全天（含 22:39 最终批次）至凌晨补查；新纳入 Claude Opus 4.6 订阅风波、Anthropic Three Agent Harness（InfoQ）、Google AI Edge LiteRT-LM（GitHub Trending）、Zml-smi GPU/TPU/NPU 监控（HN）、TigerFS PostgreSQL 文件系统`
- `total_candidates_seen`: `~120 个 source packets（04-04 全天 + 04-05 全天），精选 20 个进入 Top20`
- `top20_count`: `20`
- `rework_note`: `质量修正版：升格 Anthropic OpenClaw 定价为正式条目（原 supply_risk 遗漏）；移除 Week 14 Agent Action 重复条目（原同时出现在 top3 和 holdout）`

## 使用说明

- 这是 `signal-scout` 阶段正式交付包。
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

## Top20 候选

### 0+. Qwen3.6-397B-A17B Open Source Demand（新增，04-05 下午）
- `topic_key`: `qwen3_6_397b_open_source`
- `title`: `We absolutely need Qwen3.6-397B-A17B to be open source`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-04-04 23:50:40 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1sccpbj/we_absolutely_need_qwen36397ba17b_to_be_open/`
- `score_total`: `25/30`
- `score_breakdown`: `一手性=2 | 传播性=3 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉=2 | 平台适配=3 | 时效窗口=3 | 讨论度=3`
- `signal_summary`: `Reddit r/LocalLLaMA 日榜第 4 位热帖，用户强烈要求阿里开源 Qwen3.6-397B-A17B。帖子称该模型在真实任务中表现优于 GLM-5.1 和 Kimi-k2.5，首次感觉可以与 Claude Sonnet 比肩——"it feels as reliable as Claude in getting shit done end to end"。真实用户反馈而非 benchmark，传播性极强。`
- `why_in_top20`: `Qwen3.6 是中国开源模型重要节点；阿里是否开源的决定有高关注度；Reddit 社区讨论热度高（daily top 4）；内容可做开源 vs 闭源辩论视角`
- `visual_assets`: `Reddit 帖子截图；待回链 Qwen 官方页或模型卡`
- `risks`: `非官方确认；Qwen 官方暂无表态；需回链模型发布原文`

---

### 0+. DGX Spark NVFP4 6个月未交付（新增，04-05 下午）
- `topic_key`: `dgx_spark_nvfp4_not_delivered`
- `title`: `Don't buy the DGX Spark: NVFP4 Still Missing After 6 Months`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-04-05 01:22:19 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1scf1x8/dont_buy_the_dgx_spark_nvfp4_still_missing_after/`
- `score_total`: `23/30`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉=2 | 平台适配=3 | 时效窗口=3 | 讨论度=3`
- `signal_summary`: `Reddit 高热帖（r/LocalLLaMA 日榜第 3 位），自称拥有两台 DGX Spark 的用户详细控诉 NVIDIA 过度承诺、交付不足——NVFP4 6 个月后仍未作为成熟稳定功能交付。帖子正文有完整论据链：Blackwell + NVFP4 组合是购买理由，无 NVFP4 则硬件不成立。`
- `why_in_top20`: `NVIDIA 硬件质量问题有强新闻性；两台 DGX Spark 用户的真实体验有说服力；可做产品评测内容；科技硬件媒体关注`
- `visual_assets`: `Reddit 帖子截图；DGX Spark 产品页截图（待查）`
- `risks`: `单一用户声音，需更多佐证；NVIDIA 官方回应缺失`

---

### 0+. Gemma 4 31B FoodTruck Bench 第三名（新增，04-05 下午）
- `topic_key`: `gemma_4_31b_foodtruck_bench`
- `title`: `Gemma 4 31B beats several frontier models on the FoodTruck Bench`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-04-05 03:22:55 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1sci5h6/gemma_4_31b_beats_several_frontier_models_on_the/`
- `score_total`: `22/30`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉=2 | 平台适配=2 | 时效窗口=3 | 讨论度=3`
- `signal_summary`: `Reddit 热帖：Gemma 4 31B 在 FoodTruck Bench 取得第三名，击败 GLM 5、Qwen 3.5 397B 和所有 Claude Sonnet 模型。非主流 benchmark 但社区热度高，用户期待官方解释。`
- `why_in_top20`: `Gemma 4 延续 KV Cache fix 热度；非主流 benchmark 叙事有趣；Google 开放模型持续有话题`
- `visual_assets`: `Reddit Benchmark 结果截图`
- `risks`: `FoodTruck Bench 非权威 benchmark；需派生原始链接`

---

### 0+. NVIDIA National Robotics Week — Physical AI 研究突破（新增，04-05 上午）
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

### 1. GLM-5 nearly matched Claude Opus 4.6 at 11× lower cost
- `topic_key`: `glm5_benchmark_yc_bench`
- `title`: `We gave 12 LLMs a startup to run for a year. GLM-5 nearly matched Claude Opus 4.6 at 11× lower cost.`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-04-04 11:45:40 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/1sbyte4/we_gave_12_llms_a_startup_to_run_for_a_year_glm5/`
- `score_total`: `26/30`
- `score_breakdown`: `一手性=2 | 传播性=3 | 破圈性=3 | 赛道匹配=3 | 可延展性=3 | 数据硬度=3 | 视觉=2 | 平台适配=3 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `Reddit 高热帖，帖主构建 YC-Bench 基准——让 LLM 扮演模拟创业公司 CEO 运行一整年（数百轮决策）。GLM-5（智谱）在成本为 Claude Opus 4.6 约 1/11 的情况下效果接近。硬数据：12 个模型对比、运行一整年的长程任务、全程可复现。`
- `why_in_top20`: `模型能力对比有硬数据，跨中美模型叙事，有投资参考价值，内容可延展性强（快讯 + 深度解读 + 成本分析）`
- `visual_assets`: `Reddit 原帖有图表；Benchmark 结果页；待回链原帖补充截图`
- `risks`: `Reddit 帖子非官方 benchmark，需回链原项目页；评分 / comment count 暂不可见`

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

### 4. Anthropic charges extra for OpenClaw Claude Code usage（升格自 supply_risk）
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

---

### 5. Deeptune Raises $43M in Series A
- `topic_key`: `deeptune_series_a_43m`
- `title`: `Deeptune Raises $43M in Series A Funding`
- `primary_platform`: `FinSMEs`
- `published_at`: `2026-04-04`
- `original_link`: `来源: market_topic_capture_round 输出（jina reader 提取 TechCrunch/Finsmes）`
- `score_total`: `22/30`
- `score_breakdown`: `一手性=3 | 传播性=1 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=3 | 视觉=1 | 平台适配=2 | 时效窗口=3 | 讨论度=1`
- `signal_summary`: `AI 赛道，$43M Series A，硬数字，一级市场新融资信号。`
- `why_in_top20`: `大额 A 轮，AI 方向，内容工厂关于融资入口的稳定产出`
- `visual_assets`: `待查公司官网 / LinkedIn`
- `risks`: `公司官网、产品页尚未派生；赛道方向待补`

---

### 6. Jump Raises $80M in Series B
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

### 7. Gemma 4 KV Cache Bug Fixed
- `topic_key`: `gemma_4_kv_cache_fixed`
- `title`: `FINALLY GEMMA 4 KV CACHE IS FIXED`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-04-04`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/...`
- `score_total`: `21/30`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉=2 | 平台适配=2 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `Google Gemma 4 的 KV cache 长期 bug 被修复，LocalLLaMA 高热讨论，技术用户强烈关注。`
- `why_in_top20`: `Gemma 4 是当前最活跃的开放模型之一；bug fix 是开发者内容高点击话题`
- `visual_assets`: `Reddit 讨论截图；GitHub issue（待查）`
- `risks`: `技术细节需回链；一手性中等`

---

### 8. Gemma 4 Runs on MacBook Air 2020
- `topic_key`: `gemma_4_macbook_air_local`
- `title`: `running gemma 4 on my macbook air from 2020`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-04-04`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/...`
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

### 11. Apple Embarrassingly Simple Self-Distillation Improves Code Generation
- `topic_key`: `apple_self_distillation_code_generation`
- `title`: `Apple: Embarrassingly Simple Self-Distillation Improves Code Generation`
- `primary_platform`: `Reddit / r/LocalLLaMA`
- `published_at`: `2026-04-05 09:22:37 CST`
- `original_link`: `https://old.reddit.com/r/LocalLLaMA/comments/...`
- `score_total`: `20/30`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉=2 | 平台适配=2 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `Reddit 热帖：Apple 发布"Embarrassingly Simple Self-Distillation"技术，声称可提升代码生成能力。Apple 官方研究，LocalLLaMA 高热转发。`
- `why_in_top20`: `Apple 官方 AI 研究首次系统性分享；代码生成能力提升有开发者价值；Apple 开源/开放趋势延续`
- `visual_assets`: `Reddit 帖子截图；待查 Apple 论文原文`
- `risks`: `待查 Apple 官方论文 / 博客；代码层面的实际改进幅度待验证`

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

### 17. AICE Power — Energy Sensors Cut Bills 30%
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

### 18. 当下的AI是不是被过度神化了？（知乎热帖，14:30 前补入）
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
- `score_breakdown`: `一手性=3 | 传播性=2 | 破圈性=2 | 赛道匹配=2 | 可延展性=2 | 数据硬度=2 | 视觉=2 |- `risks`: `需回链原始信源；情绪性讨论可能掩盖硬数据`

---

## 结论

- `top3_must_watch`:
  1. **Qwen3.6-397B-A17B 开源呼声** — 阿里是否开源的决定高关注；Reddit 真实用户体验称"首个可与 Claude Sonnet 比肩的开源模型"；破圈中美 AI 圈
  2. **DGX Spark NVFP4 6个月未交付** — NVIDIA 过度承诺有强新闻性；两台机器用户的详细控诉论据链完整；科技硬件媒体天然关注
  3. **GLM-5 nearly matched Claude Opus 4.6 at 11× lower cost** — Top3 保留，硬基准数据，跨中美模型叙事

- `top6_strong_pool`:
  4. Claude Code found Linux vulnerability hidden for 23 years（AI coding 真实世界证明）
  5. Anthropic buys biotech startup Coefficient Bio $400M（AI 头部垂直扩张标杆）
  6. Anthropic charges extra for OpenClaw Claude Code usage（TechCrunch 确认，升格自 supply_risk）
  7. Gemma 4 31B FoodTruck Bench 第三名（Google 开放模型热度延续）
  8. NVIDIA National Robotics Week / Physical AI（NVIDIA 官方节点文）
  9. OpenAI $122B 融资背景（行业规模基准线）

- `holdout_watchlist`:
  10. Deeptune $43M Series A（大额融资信号）
  11. Jump $80M Series B（AI infra）
  12. Replicas — End-to-End Background Coding Agents（YC 新上榜）
  13. Velt — Audit Trail for AI agents（Agent infraware）
  14. Kinro AI — Insurance Sales Agents（垂直行业）
  15. PADO AI $6M Seed（AI 编排方向）
  16. Anthropic PAC（AI 政治化新叙事）
  17. Gemma 4 KV Cache Fix（开发者高热）
  18. Gemma 4 on MacBook Air 2020（终端侧 AI 普及叙事）
  19. Apple Self-Distillation for Code Generation（Apple 官方研究首分享）
  20. ~~LM Studio Malware Accusation~~ → 知乎「AI 过度神化」替换（未证实 vs 真实舆论趋势）

- `supply_risk`:
  - 机器之心 SFT vs RL deep article（3 篇 deep article 已落入资产体系，可供后续深度内容派生）
  - mRNA Language Models across 25 Species $165（HN 热帖，生命科学 AI 交叉，partial 源）
  - LM Studio Malware 候选降入 holdout 备选（Reddit 单一指控，未经证实）
  - 多个 YC / FinSMEs 候选尚未派生官网 / 产品页 / demo，需后续补链
  - 部分候选（如 Cheereo AI ~$1M）方向待确认，不宜直接升级为投资判断
  - **本包不含 morning_flash 已交付题**：morning_flash 车道今日无在途项，双车道隔离合规
  - 夜间新增 InfoQ / GitHub Trending / HN 批次（22:39）已完成纳入，质量修正确认
  - 建议次日继续：YC 候选官网派生、FinSMEs 融资对象一跳补链、Anthropic Three Agent Harness 原文章节回链

---

---

## 夜间新增候选（22:39 批次，01:40 AM CST 补入）

### 21. Anthropic Three Agent Harness — Long Running Full Stack AI Development（新增）
- `topic_key`: `anthropic_three_agent_harness`
- `title`: `Anthropic's Designs Three Agent Harness Supports Long Running Full Stack AI Development`
- `primary_platform`: `InfoQ AI/ML`
- `published_at`: `2026-04-05`
- `original_link`: `https://www.infoq.com/news/2026/04/anthropic-three-agent-harness-ai/`
- `score_total`: `22/30`
- `score_breakdown`: `一手性=3 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=3 | 数据硬度=2 | 视觉=1 | 平台适配=2 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `InfoQ 报道 Anthropic 设计了三 Agent协作框架（Three Agent Harness），支持长时间运行的完整技术栈 AI 开发。工程实践层面的 Agent 架构设计，InfoQ 背书。`
- `why_in_top20`: `Anthropic 工程实践披露，Agent 架构演进的重要信号；InfoQ 是工程师受众入口；与 Agent 赛道高度匹配`
- `visual_assets`: `InfoQ 页面截图`
- `risks`: `需回链 Anthropic 官方博客或文档；InfoQ 快照层一手性有限`

---

### 22. Google AI Edge LiteRT-LM — GitHub Trending（新增）
- `topic_key`: `google_ai_edge_litert_lm`
- `title`: `google-ai-edge/LiteRT-LM`
- `primary_platform`: `GitHub Trending`
- `published_at`: `2026-04-05`
- `original_link`: `https://github.com/google-ai-edge/LiteRT-LM`
- `score_total`: `21/30`
- `score_breakdown`: `一手性=3 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉=1 | 平台适配=2 | 时效窗口=3 | 讨论度=2`
- `signal_summary`: `Google AI Edge 仓库 LiteRT-LM，GitHub Trending，1,359 总 stars，今日新增 113 stars。Google 官方边缘 AI 推理运行时。`
- `why_in_top20`: `Google 官方开源 AI 推理框架；边缘 AI / 端侧 AI 是 2026 年主线之一；GitHub Trending 真实 traction 背书`
- `visual_assets`: `GitHub README 截图`
- `risks`: `需派生 README / docs 确认产品成熟度`

---

### 23. Zml-smi — Universal GPU/TPU/NPU Monitoring Tool（新增）
- `topic_key`: `zml_smi_gpu_tpu_npu_monitor`
- `title`: `Zml-smi: universal monitoring tool for GPUs, TPUs and NPUs`
- `primary_platform`: `HN Frontpage`
- `published_at`: `2026-03-31`
- `original_link`: `https://zml.ai/posts/zml-smi/`
- `score_total`: `20/30`
- `score_breakdown`: `一手性=3 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉=1 | 平台适配=2 | 时效窗口=2 | 讨论度=1`
- `signal_summary`: `HN 头条，Zml-smi 是统一监控 GPU、TPU、NPUs 的工具，解决多硬件环境下的监控割裂问题。61 points on HN。`
- `why_in_top20`: `AI infraware；HN 工程师受众验证；解决多硬件监控痛点`
- `visual_assets`: `HN 截图；zml.ai 产品页`
- `risks`: `HN 热度中等（61 points）；需派生官网确认用户规模`

---

### 24. TigerFS — PostgreSQL as Filesystem for AI Agents（新增）
- `topic_key`: `tigerfs_postgresql_filesystem`
- `title`: `TigerFS Mounts PostgreSQL Databases as a Filesystem for Developers and AI Agents`
- `primary_platform`: `InfoQ AI/ML`
- `published_at`: `2026-04-05`
- `original_link`: `https://www.infoq.com/news/2026/04/tigerfs-postgresql-filesystem/`
- `score_total`: `19/30`
- `score_breakdown`: `一手性=3 | 传播性=1 | 破圈性=1 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉=1 | 平台适配=2 | 时效窗口=2 | 讨论度=1`
- `signal_summary`: `InfoQ 报道 TigerFS 将 PostgreSQL 数据库挂载为文件系统，供开发者和 AI Agent 使用。开发者工具 + AI Agent 工作流交叉。`
- `why_in_top20`: `AI Agent 工作流基础设施；PostgreSQL 生态延伸；差异化开发者工具`
- `visual_assets`: `InfoQ 页面截图`
- `risks`: `InfoQ 快照层一手性有限；需派生官网`

---

### 25. Claude Opus 4.6 — Subscription Cancelled = Faster?（新增，高度相关）
- `topic_key`: `claude_opus_4_6_rate_limit_weird`
- `title`: `Today I got to experience Opus 4.6 blazing fast without rate limits — right after my Max 5x subscription expired`
- `primary_platform`: `Reddit / r/ClaudeAI`
- `published_at`: `2026-04-05 09:44:45 CST`
- `original_link`: `https://old.reddit.com/r/ClaudeAI/comments/1scqyh8/today_i_got_to_experience_opus_46_in_a_blazing/`
- `score_total`: `23/30`
- `score_breakdown`: `一手性=2 | 传播性=2 | 破圈性=2 | 赛道匹配=3 | 可延展性=2 | 数据硬度=2 | 视觉=2 | 平台适配=2 | 时效窗口=3 | 讨论度=3`
- `signal_summary`: `Reddit r/ClaudeAI 用户称其 Max 5x 订阅过期（与 OpenClaw 访问被撤销时间吻合）后，反而体验到了 Opus 4.6 的极速访问，25 分钟未遭遇任何速率限制。帖子引发关于 Claude 订阅等级与速率限制机制关联的热烈讨论。`
- `why_in_top20`: `与 Anthropic 额外收费 OpenClaw 事件高度关联；速率限制机制的争议性问题；社区讨论度高；OpenClaw/Anthropic 叙事线的延续`
- `visual_assets`: `Reddit 帖子截图`
- `risks`: `单一用户体验，需更多佐证；Anthropic 官方未解释机制`

---

## 文化侧写补充（18:13 CST 新增）

### 纸扎AI全家桶 — AI 渗透中国祭祀文化
- `topic_key`: `zhihu_paper_ai_s offerings_tomb_sweeping`
- `title`: `今年清明「纸扎AI全家桶」火了，人们给祖宗烧 DeepSeek 等热门大模型，反映出怎样的情感需求？`
- `platform`: `知乎热榜`
- `published_at`: `2026-04-01 15:51:59 CST`（在清明节期间发酵，4月5日仍居热榜）
- `captured_at`: `2026-04-05 17:49:28 CST`
- `heat`: `89 万热度`
- `signal_summary`: `知乎热榜问题：电商平台清明推出含 DeepSeek、OpenClaw、ChatGPT 纸质扎制的"AI纸扎全家桶"，售价 35.9 元起，消费者在祭祀时"烧给祖宗"。商家描述：不是简单的纸扎，而是"阴间也用 AI"。知乎用户在问题下讨论"情感需求""科技与传统融合""对逝者的情感补偿"。`
- `文化信号价值`: `AI 已足够深入中国日常生活，以至于成为祭祀文化的组成元素。DeepSeek、OpenClaw 在清明语境中的并置，反映这些品牌（尤其是 OpenClaw）在科技用户群体中的认知度已达文化符号级别。`
- `content_factory价值`: `AI 品牌破圈到文化层，这是内容写作的高点击角度，可做"AI 在中国有多渗透"主题的内容。`
- `risks`: `非产品 / 非融资 / 非技术信号，内容工厂仅作为文化背景参考，不作为主赛道候选处理。`
