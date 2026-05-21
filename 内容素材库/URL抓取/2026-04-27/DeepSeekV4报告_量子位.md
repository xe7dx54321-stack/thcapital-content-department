# DeepSeek V4技术报告详解 — 484天换代全公开
# Raw Archive — 2026-04-27

**Source**: 量子位
**URL**: https://www.qbitai.com/2026/04/406809.html
**Fetched**: 2026-04-27T03:28:01+00:00
**Fetch Method**: curl_cffi:chrome131
**Usable**: ✅
**Trigger-type**: 大模型 / DeepSeek
**Priority**: ⭐ HIGH

---

## 正文摘要

DeepSeek V4"迟到"半年，发布后好评如潮。核心两条：

**第一条：百万token上下文全面开源，KV cache大幅缩减**
- V4-Pro和V4-Flash，1.6万亿参数/2840亿参数，上下文都是1M
- 1M场景下，V4-Pro的单token FLOPs只有V3.2的27%，KV cache只有10%
- 亚马逊硬件师GPD表示，这意味着DeepSeek可能解决当前的HBM短缺问题

**第二条：国产芯片适配，已经支持华为算力，预计下半年昇腾950超节点批量上市**

**四大技术预期，三个落地，一个留给V5：**
- mHC（流形约束超连接）：2025年12月31日上传arXiv，梁文锋挂名。进了V4 ✅
- Engram（条件记忆模块）：1月DeepSeek联合北大发布。没进V4，留给V5
- DualPipe：V3老伙计，继续用 ✅
- Muon优化器：从Kimi那边借的 ✅

**V4架构三大升级：**
1. 引入mHC（Manifold-Constrained Hyper-Connections）强化残差连接
2. 设计hybrid attention架构，CSA和HCA交替叠加，解决长文效率问题
3. 采用Muon作为主优化器

**关键数据：**
- V4-Flash: 43层，隐藏维度4096，MoE 1个shared expert + 256个routed experts，每token激活6个，总参数284B，激活13B
- V4-Pro: 61层，隐藏维度7168，MoE 1个shared expert + 384个routed experts，每token激活6个，总参数1.6T，激活49B
- 预训练数据量：V4-Flash 32T Token，V4-Pro 33T Token（对比V3的14.8T，翻了一倍多）

**实验结论：**
- 开源领先：SimpleQA-Verified上V4-Pro-Max拿到57.9，K2.6是36.9，GLM-5.1是38.1，领先所有开源模型20个百分点
- 匹敌闭源：Codeforces rating 3206，超过了GPT-5.4的3168和Gemini-3.1-Pro的3052，在人类选手榜单上排名第23
- 差距仍在：HLE上V4-Pro-Max 37.7，Gemini-3.1-Pro 44.4，Claude-Opus-4.6-Max 40.0。约3-6个月gap

**V4-Flash-Max可能被低估：** 只激活13B参数，推理任务上能打平GPT-5.2和Gemini-3.0-Pro，代码和数学甚至超过K2.6-Thinking。

**DeepSeek研究员陈德里在x上：** "DeepSeek-V3：2024年12月26日。DeepSeek-V4：2026年4月24日。484天后，我们谦卑地分享这份爱心的劳动。一如既往，我们始终坚持长期主义和全民开源。AGI属于每个人。"
