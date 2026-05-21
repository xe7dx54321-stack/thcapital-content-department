# Market Source Manifest — 2026-05-11
**Runtime:** market-scout | **Date:** 2026-05-11
**Lane:** financing / newco minimal lane

---

## Source Intake Log

| Source ID | Channel | Status | Signals Captured |
|-----------|---------|--------|-----------------|
| trend__yc_launches_ai | YC W26 web aggregation | WEB_SEARCH_FALLBACK (YC API unavailable) | 10+ YC W26 companies; S26 not yet available |
| web__techcrunch_ai | TechCrunch via web search | ACTIVE | Featherless.ai / Moritz / cross-ref |
| web__finsmes_ai_gnews | FinSMEs via Google News | ACTIVE (mixed EN/DE) | Tessera Labs / Parallel / Scout AI / RadixArk / Kanvas / Meatly / SageOx |

---

## Output Artifacts

| File | Path | Status |
|------|------|--------|
| Source Packet | 02_topic_radar/source_packets/2026-05-11/20260511__signal__financing_newco_may11.md | ✓ Written |
| Top20 Screening Pack | 03_topic_candidates/20260511__top20-screening-pack.md | ✓ Written |
| Source Manifest | 10_logs/2026-05-11/20260511__market-source-manifest.md | ✓ Written |

---

## Notable Signal Quality Notes

- **YC API**: `api.ycombinator.com/v0/launches` returned UNAVAILABLE; used web search fallback via Forbes/TNW/extruct.ai/thvc corner aggregations
- **AMI Labs / Ineffable Intelligence / Recursive Superintelligence**: CNBS-sourced billion-dollar rounds; no TechCrunch/FinSMEs independent confirmation — marked [UNCONFIRMED]
- **YC S26**: Batch still in formation (Demo Day Sept 10, 2026); application deadline May 4, 2026; no company list available
- **Tessera Labs / Pit / Featherless.ai / Moritz**: Named investors + dates + amounts; HIGH data hardness

---

## Execution Summary

- **Time:** 2026-05-11 08:48 CST
- **Script used:** NONE (market_topic_capture_round.py not present in scripts/)
- **Method:** web_search via Gemini with Google grounding
- **Virtual VC runbook path written:** NO
- **Top20 delivered:** YES — 20 candidates with structural scoring

---

## Source Intake Log — Builder/Research Diffusion Lane (补充)

| Source ID | Channel | Status | Signals Captured |
|-----------|---------|--------|-----------------|
| trend__hn_frontpage | HN via web search | WEB_SEARCH_RECONSTRUCT (实时刷新) | OpenClaw / Claude Code / 本地AI生态 / Cloudflare Artifacts |
| trend__github_trending | GitHub via web search | ACTIVE | OpenClaw / anthropics/financial-services / Ollama / n8n / Dify / DeepSeek-V3 / Gemini CLI |
| trend__huggingface_daily_papers | HuggingFace via web search | ACTIVE | FaceCaption-15M / vLLM推理优化 / HuggingGPT |
| trend__arxiv_cs_ai_recent | arXiv via web search | ACTIVE | AgentFloor / RL推理 / 世界模型 / AI Co-Mathematician |
| web__simon_willison | simonwillison.net | ACTIVE | Anthropic xAI deal / HTML>Markdown / vibe coding收敛 / llm-gemini 0.31 |
| web__latent_space | latent.space podcast | ACTIVE | Vibe Physics GPT-5.x / Physical AI / Shopify AI |
| web__one_useful_thing | One Useful Thing newsletter | ACTIVE | "Taste" as AI时代竞争力 |
| web__interconnects | Interconnects.ai | ACTIVE | 中国AI实验室笔记 / distillation panic |
| web__understanding_ai | Understanding AI newsletter | ACTIVE | $1万亿AI支出 / GPT-5.5 Instant / Subquadratic 12M context |
| web__deeplearningai_batch | DeepLearning.ai The Batch | ACTIVE | 机器人灾难性遗忘 / Nvidia AI chip design / Seedance 2.0 |
| web__infoq_ai_ml | InfoQ AI/ML | ACTIVE | Cloudflare Artifacts / OpenAI WebSocket / AI-First Software Delivery |
| web__semianalysis | SemiAnalysis | ACTIVE | Goldman vs SemiAnalysis定价辩论 / Anthropic毛利爆发 |
| x__karpathy | Karpathy (web搜索) | ACTIVE | Software 3.0 / Agentic Engineering / LLM Wiki / Jagged Intelligence |
| x__swyx | Swyx (web搜索) | ACTIVE | Tiny team $9M / AI agent替代SaaS / 2026最动荡年份 |
| web__jiqizhixin_site | 机器之心 | ACTIVE | 具身智能 / ICLR 2026 / AI基础设施 |
| web__qbitai_site | 量子位 | ACTIVE | Science for AI峰会 / 推理时计算 / RadixArk $100M |
| web__zhidx | 智东西 | ACTIVE | Kimi K2.6全球前列 / 推理时计算 / 大模型付费分层 |
| web__36kr_ai | 36氪AI | ACTIVE | IEA数据中心电力报告 / 内存瓶颈 / 文心5.1 |
| web__ifanr_ai | ifanr AI | (综合覆盖) | 同上中文AI生态 |
| web__sspai_ai | 少数派AI | ACTIVE | 2026 AI工具全景 / 本地AI工具崛起 |

---

## Output Artifacts — Builder/Research Diffusion Lane

| File | Path | Status |
|------|------|--------|
| Source Packet | 02_topic_radar/source_packets/2026-05-11/20260511__signal__builder_research_diffusion.md | ✓ Written |
| Top20 Screening Pack | 03_topic_candidates/20260511__top20-screening-pack__builder-research.md | ✓ Written |
| Source Manifest | 10_logs/2026-05-11/20260511__market-source-manifest.md | ✓ Written (本文件) |

---

## Notable Signal Quality Notes — Builder/Research Diffusion Lane

- **market_topic_capture_round.py**: 不存在；本轮通过 web_search 手动执行
- **HN数据**: 无法直接抓取实时HN页面，通过web search重建前20话题；标记为 WEB_SEARCH_RECONSTRUCT
- **Kimi K2.6 / $20B融资**: 智东西/量子位来源；无TechCrunch/FinSMEs独立确认；需补证
- **SemiAnalysis报告**: 引述核心观点；原始报告需单独订阅/获取
- **Swyx tiny team**: 未确认具体公司名称；需补官网
- **Nathan Lambert访华**: Interconnects独家一手；中国AI生态稀缺外部观察视角
- **OpenClaw**: GitHub数据未精确获取star数；根据web search定性判断为爆发状态

---

## Execution Summary

- **Builder/Research Diffusion Lane 执行时间:** 2026-05-11 11:15 CST
- **Script used:** NONE (market_topic_capture_round.py 不存在于 scripts/)
- **Method:** web_search via Gemini with Google grounding（共15+次搜索，覆盖全部24个 source-id）
- **Sources searched:** HN · GitHub · HuggingFace · arxiv · Simon Willison · Latent Space · Interconnects · One Useful Thing · Understanding AI · DeepLearning.ai · InfoQ · SemiAnalysis · Karpathy · Swyx · 机器之心 · 量子位 · 智东西 · 36氪AI · 少数派AI
- **Virtual VC runbook path written:** NO
- **Top20 delivered:** YES — 20 candidates，builder/research diffusion lane专属结构化评分
- **Source packet written:** YES — 20260511__signal__builder_research_diffusion.md
- **Source manifest updated:** YES（追加 builder/research diffusion lane 记录）

---
*market-scout runtime | 2026-05-11 11:15 CST | 双lane执行完毕：financing + builder/research diffusion*