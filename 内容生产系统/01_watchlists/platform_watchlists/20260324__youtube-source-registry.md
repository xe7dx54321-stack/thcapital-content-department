# 同行资本市场内容系统｜YouTube Source Registry

## 1. 用途

记录 YouTube 上需要长期监控的频道、节目和访谈源。

适合收录：

- 创业者频道
- tool demo 频道
- AI 访谈节目
- 产品发布频道
- 讲 workflow / skill / stack 的内容号

---

## 2. 表结构

| source_key | source_name | source_type | handle_or_url | region | language | signal_quality | citation_reliability | capture_method | status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| youtube__openai | OpenAI | company | https://www.youtube.com/feeds/videos.xml?channel_id=UCXZCJLdBC09xxGZ6gcdrc6A | global | en | high | high | youtube-feed / transcript | active | 官方发布会、demo、产品说明，一手视频源 |
| youtube__ycombinator | Y Combinator | media | https://www.youtube.com/feeds/videos.xml?user=YCombinator | global | en | high | medium | youtube-feed / transcript | active | 创始人访谈、新产品和 build-in-public 素材密度高 |
| youtube__googledeepmind | Google DeepMind | company | https://www.youtube.com/@GoogleDeepMind | global | en | high | high | youtube-channel / transcript | active | 模型、研究、机器人和 demo 适合拆内容角度 |
| youtube__aidotengineer | AI Engineer | media | https://www.youtube.com/@aiDotEngineer | global | en | high | medium | youtube-channel / transcript | active | agent 实操、workflow、stack 教学密度高 |
| youtube__latent_space_pod | Latent Space Pod | media | https://www.youtube.com/@LatentSpacePod | global | en | high | medium | youtube-channel / transcript | active | 长访谈、观点演化和 builder 内容互补强 |
| youtube__langchain | LangChain | tool_builder | https://www.youtube.com/@LangChain | global | en | medium | medium | youtube-channel / transcript | active | agent builder 教学、案例、框架更新 |
