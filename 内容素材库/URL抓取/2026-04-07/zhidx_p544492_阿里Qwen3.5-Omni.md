# raw: 阿里Qwen3.5-Omni登场：看懂50分钟《老友记》
- **source**: zhidx
- **url**: https://www.zhidx.com/p/544492.html
- **fetched_at**: 2026-04-06T20:31:39+00:00
- **trigger_type**: 产品发布
- **entity**: 阿里千问Qwen3.5-Omni
- **usable**: true
- **fetch_method**: curl_cffi:chrome131

## 正文摘要

阿里发布Qwen3.5-Omni全模态模型（Plus/Flash/Light三种尺寸），215项音频/音视频SOTA，超越Gemini-3.1 Pro。

**核心能力：**
- 原生理解文本/图片/音频/音视频输入，以文本+音频双模态输出
- 支持256k长上下文 + 超过10小时音频 + 400秒720P视频（1FPS）
- 39种国内方言 + 74种语言
- 音色克隆+7种国内方言+29种语言音频合成

**性能数据：**
- 215项音频/音视频理解/推理/交互任务 SOTA
- 通用音频理解/推理/识别/翻译/对话超越Gemini-3.1 Pro
- 音视频理解达Gemini-3.1 Pro水平
- 处理50分钟《老友记》约1分钟，完整覆盖时间线，叙事感强

**技术架构：**
- Thinker-Talker分工架构（Thinker负责理解，Talker负责表达）
- Hybrid-Attention MoE（混合注意力MoE）替代传统单模态架构
- TMRoPE编码位置信息
- RVQ编码替代DiT运算
- ARIA技术（自适应速率交错对齐）提升语音合成自然度

**交互能力：**
- 语义打断（不会被"嗯嗯"打断，但能响应真实提问）
- 原生网络搜索+复杂FunctionCall
- 端到端语音控制和对话

**价格（阿里云百炼API）：**
- 音频输入：4.96元/百万tokens
- 文本/图片/视频输入：0.8元/百万tokens
- 输出（文本+音频）：61.322元/百万tokens
- 仅输出文本：9.6元/百万tokens
