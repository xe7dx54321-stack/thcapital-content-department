# 同行资本市场内容系统｜X Source Registry

## 1. 用途

记录 X / Twitter 上需要长期监控的 source。

适合收录：

- 创始人
- tool builder
- AI agent 产品方
- KOL
- 媒体账号
- 趋势观察号

---

## 2. 表结构

| source_key | source_name | source_type | handle_or_url | region | language | signal_quality | citation_reliability | capture_method | status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| x__openai | OpenAI | company | @OpenAI | global | en | high | high | jina-reader / x-auth-fallback | active | 已验证可稳定拿到 profile 与近期帖文摘录；硬信息优先回链 OpenAI 原文 |
| x__openaidevs | OpenAI Devs | tool_builder | @OpenAIDevs | global | en | high | high | jina-reader / x-auth-fallback | active | 适合补 API / SDK / devtool 更新，必要时回链官方 docs |
| x__anthropic_ai | Anthropic | company | @AnthropicAI | global | en | high | high | jina-reader / x-auth-fallback | active | 适合补官方社交快讯，但正式引用仍以 Anthropic 原站为准 |
| x__karpathy | Andrej Karpathy | kol | @karpathy | global | en | high | medium | jina-reader / x-auth-fallback | active | 已验证可稳定拿观点片段；适合作为方法论 / 观点线索源 |
| x__swyx | swyx | kol | @swyx | global | en | high | medium | jina-reader / x-auth-fallback | active | AI engineer / agent infra / 社区桥梁型强源，适合抓观点与产品提及 |
| x__hwchase17 | Harrison Chase | tool_builder | @hwchase17 | global | en | high | medium | jina-reader / x-auth-fallback | active | agent builder、框架与开发者讨论价值高 |
| x__langchainai | LangChain | company | @LangChainAI | global | en | medium | medium | jina-reader / x-auth-fallback | candidate | agent framework / builder 案例和能力更新 |
| x__levelsio | Pieter Levels | founder | @levelsio | global | en | medium | low | jina-reader / x-auth-fallback | candidate | 一人公司 / build in public 邻接高热观察源，暂保留为观察位 |
