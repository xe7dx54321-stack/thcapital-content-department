# source packet

## meta
- date: 2026-05-12
- source-id: trend__reddit_localllama_daily
- source-type: community-discussion (fallback: web search 替代 JSON API 直采)
- source-label: r/LocalLLaMA 热帖 / 2026-05-12
- 一手性: P1 / community-sourced (Reddit JSON 被屏蔽，降级至 web search 恢复)
- 稳定性: 中 (Reddit API 持续屏蔽，依赖 web search 作为 fallback)
- 抓取时间: 2026-05-12 01:42 UTC
- blocked: Reddit JSON API 403 → web search recovery

## 热帖信号 (2026-05-12 当天 / 近期)

### 1. Llama 4 Scout — 10M token context + MoE + 多模态
- **核心信息:** Llama 4 Scout 突破性特性：MoE 架构（推理时只激活部分参数）、10M token 超大上下文窗口、原生多模态（图文）、约 12GB VRAM 即可运行
- **社区情绪:** 高度兴奋，视为消费级硬件上的重大突破
- **一手性:** P1（Meta 官方发布后社区验证）
- **信号类型:** 产品能力突破 / 硬件门槛降低

### 2. Gemma 4 vs Qwen 3.6 — Coding/Tool Use 能力对比
- **核心信息:**
  - Gemma 4 在 coding 和 tool-assisted tasks 上表现令用户失望，容易陷入循环
  - Qwen 3.6 在 coding / tool use 上更可靠、更持续
  - Gemma 4 assistant 版本在 MacBook Pro M4 上获得速度好评
  - llama.cpp 后端上 Gemma 4 有"发疯"输出问题
- **社区情绪:** 偏负面于 Gemma 4 coding 场景；Qwen 3.6 获正面验证
- **一手性:** P1（用户第一手体验，非官方评测）
- **信号类型:** 模型能力对比 / 开发者选型参考

### 3. Grok 3 — 推理/Coding 优势 + 基准争议
- **核心信息:**
  - Grok 3 在数学推理和 coding benchmarks 上表现突出，给予更多"思考时间"后更优
  - 自报基准遭到社区质疑，需要独立验证
  - 有研究用于 radiology 诊断报告生成（ lexical diversity + coherence 领先）
- **社区情绪:** 谨慎乐观，保留对基准可信度的质疑
- **一手性:** P2（xAI 官方 + 第三方验证混合）
- **信号类型:** 模型能力 / 推理专用场景

### 4. Mistral Small 3.1 — 最佳质量-VRAM 比率
- **核心信息:**
  - Mistral Small 3.1 被社区认为提供最佳质量-VRAM 比率，14GB RAM 即可接近 70B 模型效果
  - Devstral Small 24B 推荐用于复杂 agentic coding 任务
  - 较新的 Mistral Large 模型收到部分负面反馈（表现不如早期型号如 Nemo）
- **社区情绪:** Mistral Small 3.1 稳定好评；较新大型号褒贬不一
- **一手性:** P1（用户实测）
- **信号类型:** 硬件受限场景最优选择 / 小厂差异化

### 5. 社区排名快照 (Early May 2026)
| 模型 | 评级 | 适用场景 |
|------|------|---------|
| Qwen 3.6 27B | 顶级 dense model | Coding |
| Llama 3.3 70B / Qwen3 72B | 强竞争者 | 英文推理 |
| Llama 4 Scout | 最佳性价比 | 长上下文 + MoE 效率 |
| Mistral Small 3.1 | 最佳 VRAM 效率 | 硬件受限用户 |
| Mistral Large 3 | A tier | 通用 |
| Llama4-Maverick | A- tier | 通用 |
| Grok 3 | 待独立验证 | 推理专用 |

## 结构化字段

| 字段 | 值 |
|------|-----|
| 话题类别 | Open-source LLM / 模型对比 / 本地部署 |
| 一手性 | P1 |
| 传播性 | 高（Reddit 超活跃社区） |
| 破圈性 | 中（主要在开发者圈，但 Llama 4 Scout 有大众媒体潜力） |
| 数据硬度 | 中（用户主观体验为主，基准数据部分存疑） |
| 视觉素材丰富度 | 低（文本讨论为主，无产品截图在该 lane 直接捕获） |
| 热点入口稳定性 | 中（Reddit API 持续屏蔽，依赖搜索 fallback） |

## 关键链接
- https://www.reddit.com/r/LocalLLaMA/comments/1t7rco2/those_of_you_who_like_gemma4_models_how_are_you/
- https://www.reddit.com/r/LocalLLM/comments/1t5ys13/the_gemma4_assistant_models_feel_like_magic/
- https://www.reddit.com/r/LocalLLM/comments/1t73w81/gemma_is_going_absolutely_insane/
- https://www.reddit.com/r/LocalLLaMA/comments/1t14yhr/your_local_llm_predictions_and_hopes_for_may_2026/
- https://www.reddit.com/r/LocalLLaMA/comments/1t9xzdv/any_news_or_hope_of_qwen36_14b_and_9b_distills/

## upstream 来源说明
- Reddit JSON API 直采: **失败（403 blocked）**
- 降级方案: web search 引擎搜索 "site:reddit.com/r/LocalLLaMA May 2026" + 补充搜索
- 降级后一手性: P1 → 维持 P1（用户第一手体验），但缺少精确 upvote count / post URL

---
*market-scout | trend__reddit_localllama_daily | 2026-05-12 | 09:42 AM CST*