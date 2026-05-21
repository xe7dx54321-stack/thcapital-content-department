# source packet

## meta
- date: 2026-05-12
- source-id: trend__reddit_chatgpt_daily
- source-type: community-discussion (fallback: web search 替代 JSON API 直采)
- source-label: r/ChatGPT 热帖 / 2026-05-12
- 一手性: P1 / community-sourced (Reddit JSON 被屏蔽，降级至 web search 恢复)
- 稳定性: 中 (Reddit API 持续屏蔽，依赖 web search 作为 fallback)
- 抓取时间: 2026-05-12 01:42 UTC
- blocked: Reddit JSON API 403 → web search recovery

## 热帖信号 (2026-05-12 当天 / 近期)

### 1. GPT-5.5 vs GPT-5 Mini 路由混乱 — Plus 用户困惑
- **核心信息:**
  - ChatGPT Plus 订阅用户被静默路由至"GPT-5 mini"而非已选择的"GPT-5.5 Thinking"
  - Web 端始终默认 GPT-5 mini；Android app 正确使用 GPT-5.5 Thinking
  - 跨浏览器、无痕模式、登出重登均无法解决
  - 从 5 月 8-9 日开始，持续多天，OpenAI support 已escalate
- **社区情绪:** 强烈负面，用户感到被欺骗（隐性 model downgrade）
- **一手性:** P1（用户第一手投诉，多人确认）
- **信号类型:** 产品信任危机 / OpenAI 透明度问题

### 2. 图像生成质量大幅下降 — "SO GOOD" → "terrible"
- **核心信息:**
  - 多个用户报告 ChatGPT 图像生成质量在近一个月内"显著下降"
  - Pro 版本 vs 基础版本在图像质量上存在可感知差异（Pro 的 GPT-Image-2 支持 4K，基础版 1K）
  - 用户反映两个版本均"不稳定，会给出破损结果（broken results）"
  - 可能与"Image 2"版本推送有关
- **社区情绪:** 强烈负面，尤其 Pro 用户感到订阅价值受损
- **一手性:** P1（大量用户投诉，多 thread）
- **信号类型:** 产品体验退化 / 付费用户权益问题

### 3. Custom GPT 图像生成设置失效
- **核心信息:**
  - 用户在 Custom GPT 配置中关闭图像生成后，GPT 仍然持续生成图像
  - 问题从"Image 2"发布前后开始
  - Custom instructions 中的图像生成规则（如提供 alt text）仅在"regenerate"后才执行
  - 问题跨 GPT-5.5 Instant 和 Thinking 模型持续
- **社区情绪:** 挫败感（功能 bug 影响工作流）
- **一手性:** P1（用户报告）
- **信号类型:** 产品 bug / Custom GPT 生态问题

### 4. GPT-5 整体负面评价 — "horrible update" / "step back"
- **核心信息:**
  - 更广泛的讨论：GPT-5 是"可怕的更新"，比之前版本"退步"
  - 投诉点：幻觉增加、语气 patronizing、输入延迟、响应变慢
  - "auto-router"自动模型选择功能被批评为用户失去控制权
  - 在 reddit 多个版（r/ChatGPT, r/ChatGPTcomplaints）均有高热度帖子
  - 媒体已有报道（telecoms.com, economictimes 等引用"thousands trash GPT-5"）
- **社区情绪:** 大面积负面，媒体跟进中
- **一手性:** P1（用户社区） + P0.5（媒体转述）
- **信号类型:** 产品体验危机 / OpenAI 品牌风险

## 结构化字段

| 字段 | 值 |
|------|-----|
| 话题类别 | AI 产品体验危机 / 商业化问题 / 模型质量退化 |
| 一手性 | P1（用户投诉主体） |
| 传播性 | 高（Reddit + 媒体接力：economictimes / telecoms.com 均已报道） |
| 破圈性 | 高（大众用户关注，非技术圈） |
| 数据硬度 | 中（用户主观投诉为主，但规模大和媒体确认） |
| 视觉素材丰富度 | 中（有截图传播，Reddit 高热度） |
| 热点入口稳定性 | 中（Reddit API 屏蔽，但投诉规模足以通过搜索恢复） |

## 关键链接
- https://www.reddit.com/r/ChatGPT/comments/1sub8vc/chatgpt_is_useless_currently_im_having_problems/
- https://www.reddit.com/r/ChatGPTcomplaints/comments/1t0271k/sudden_unprompted_image_generation_attempts/
- https://www.reddit.com/r/ChatGPT/comments/1t9lywa/gpt55_thinking_selected_but_chatgpt_web_replies/
- https://www.reddit.com/r/ChatGPT/comments/1t2uhtv/pro_version_generates_better_images_than_base/
- https://www.reddit.com/r/ChatGPT/comments/1t9f3ki/image_generation_sucks_all_of_a_sudden/
- https://www.reddit.com/r/ChatGPT/comments/1t7hb1t/turning_image_generation_off_in_custom_gpt_does/
- https://www.reddit.com/r/ChatGPT/comments/1t9kdeg/image_gen_instructions_only_being_followed_after/
- https://www.telecoms.com/ai/openai-users-are-not-happy-about-gpt-5
- https://economictimes.indiatimes.com/news/international/us/thousands-trash-gpt-5-on-reddit-saying-chatgpts-big-update-is-horrible/articleshow/123192815.cms

## upstream 来源说明
- Reddit JSON API 直采: **失败（403 blocked）**
- 降级方案: web search 搜索 "site:reddit.com/r/ChatGPT May 2026" + 补充搜索 + 媒体交叉验证
- 降级后一手性: P1 维持（投诉规模大，媒体已跟进）

---
*market-scout | trend__reddit_chatgpt_daily | 2026-05-12 | 09:42 AM CST*