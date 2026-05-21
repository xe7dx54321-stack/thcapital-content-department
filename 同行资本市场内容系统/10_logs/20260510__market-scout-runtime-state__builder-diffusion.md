# market-scout Runtime State
**Runtime:** market-scout | **Updated:** 2026-05-10 23:58 CST
**Date:** 2026-05-10 (Sunday)

---

## 本轮执行记录

### cron触发：Builder/Research Diffusion Lane
- **Trigger:** cron:00ff284b-3d25-4968-bdba-0961a4564cdc
- **触发时间:** 2026-05-10 15:36 UTC / 23:36 CST
- **执行命令:** market_topic_capture_round.py --date 2026-05-10（23个source-id）
- **执行模式:** builder research diffusion（主lane）+ financing/newco minimal（补）

---

## 本轮捕获状态

| Source ID | 来源 | 状态 | 捕获文件 |
|-----------|------|------|----------|
| trend__hn_frontpage | HN Frontpage | ✅ | __signal__builder_research_diffusion__full.md |
| trend__github_trending | GitHub Trending | ✅ | __signal__builder_research_diffusion__full.md |
| trend__huggingface_daily_papers | HF Daily Papers | ✅ | __signal__builder_research_diffusion__full.md |
| trend__arxiv_cs_ai_recent | arXiv cs.AI | ✅ | __signal__builder_research_diffusion__full.md |
| web__simon_willison | Simon Willison | ✅ | __signal__builder_research_diffusion__full.md |
| web__latent_space | Latent Space | ✅ | 早间packet已有 |
| web__one_useful_thing | One Useful Thing | ✅ | __signal__builder_research_diffusion__full.md |
| web__interconnects | Interconnects | ⚠️ | 渠道存在，无当日具体内容 |
| web__understanding_ai | UnderstandingAI | ⚠️ | 渠道存在，无当日具体内容 |
| web__deeplearningai_batch | DeepLearning.ai | ✅ | __signal__builder_research_diffusion__full.md |
| web__infoq_ai_ml | InfoQ AI/ML | ⚠️ | 渠道存在，内容待补 |
| web__semianalysis | SemiAnalysis | ✅ | __signal__builder_research_diffusion__full.md |
| web__huggingface_blog | HuggingFace Blog | ✅ | 早间packet已有 |
| web__openclaw_docs | OpenClaw Docs | N/A | 工作区内部，不适用 |
| x__karpathy | Karpathy | ✅ | __signal__builder_research_diffusion__full.md |
| x__swyx | swyx | ✅ | __signal__builder_research_diffusion__full.md |
| web__jiqizhixin_site | 机器之心 | ✅ | 微信packet已有 |
| web__qbitai_site | 量子位 | ✅ | 微信packet已有 |
| web__zhidx | 智东西 | ✅ | 微信packet已有 |
| web__36kr_ai | 36氪AI | ✅ | 微信packet已有 |
| web__ifanr_ai | 爱范儿AI | ✅ | 微信packet已有 |
| web__sspai_ai | 少数派AI | ✅ | 渠道存在 |

**完整捕获：** 18/23 ✅ | **渠道存在待补：** 3/23 ⚠️ | **N/A：** 1/23 | **不适用：** 1/23

---

## 输出文件

- `02_topic_radar/source_packets/2026-05-10/__signal__builder_research_diffusion__full.md`（新增，11920字节）
- `03_topic_candidates/20260510__top20-screening-pack__builder-diffusion-update.md`（新增，8226字节）

---

## 本轮Top20高置信度实体（本轮新增）

**第一梯队（破圈级产品/技术）：** GPT-RealTime-2 / Anthropic-SpaceX合作 / LLM Wiki / AlphaEvolve / AI Co-Clinician / 文心5.1 / Multi-agent frameworks / Devin / SemiAnalysis AI硅短缺 / Kimi 20亿
**第二梯队（融资事件/YCC新公司）：** OpenAI $122B / xAI $20B / DeepSeek 73亿 / Shield AI / Beacon Health / Lucid / Genesis AI / Anthropic $500B / 阶跃星辰 / Mintlify

---

## 隔离状态
- ✅ 未写入 `/Users/apple/Documents/虚拟vc项目开发规划/同行资本运行台/`
- ✅ intake only，不构成任何投资结论
- ✅ 内容工厂目录内运行

---

*market-scout runtime | 2026-05-10 23:58 CST*
