# Top 5 建议板 — 2026-05-21（day_mainline）
**生成时间：** 2026-05-21 17:25 CST
**来源：** `03_topic_candidates/20260521__top20-screening-pack__reworked.md`
**裁判评分卡：** `10_logs/20260521__top20__stage-gate-scorecard.md`（final，17:14 CST）
**裁判结论：** pass + premium_only，无 continuity lane，径直进入 Top 8→Top 5 流程
**stage-gate：** market-editor（stage-gate）

---

## 评分标准说明

| 字段 | 说明 |
|---|---|
| pack_score | Top20 初筛包原始得分 |
| judge_score | 裁判定性评分（来自 scorecard） |
| signal_type | **heat** = 市场热度/传播信号；**evidence** = 事实落地/执行信号 |
| decision | TOP5（主推）/ HOLDOUT3（备选）/ SKIP（本轮跳过） |

---

## Top 5 主推板

### 🥇 #1｜OpenAI Codex + NVIDIA GB200
- **URL：** https://blogs.nvidia.com/blog/openai-codex-gpt-5-5-ai-agents/
- **source packet：** `03_topic_candidates/20260521__top20-screening-pack__reworked.md` #1
- **pack_score：** 47（Top20 第1）
- **judge_score：** 9/10
- **signal_type：** heat + evidence（双信号：传播热度 + 企业级落地执行）
- **heat signal：** NVIDIA 官方博客；GB200 NVL72 基础设施；内部 10000+ 人实际使用；与 OpenAI 联合发布
- **evidence signal：** 企业级 AI Agent 已在生产环境落地（千级用户），不是公测或愿景
- **裁判备注：** 无争议 TOP1，两类信号兼具，下一工序直接推进

---

### 🥈 #2｜NVIDIA SAP Trust
- **URL：** https://blogs.nvidia.com/blog/sap-specialized-agents/
- **source packet：** `03_topic_candidates/20260521__top20-screening-pack__reworked.md` #2
- **pack_score：** 39（Top20 第2）
- **judge_score：** 8/10
- **signal_type：** evidence（企业级 Agent 安全标准确立）
- **heat signal：** 官方合作；企业级叙事
- **evidence signal：** NVIDIA OpenShell 嵌入 SAP Business AI Platform；企业级 Agent 安全标准确立；已有标杆客户
- **裁判备注：** 企业安全基础设施，到达 content-writer 前需 topic-planner 补商业 hook

---

### 🥉 #3｜Parloa 语音 Agent
- **URL：** https://openai.com/index/parloa
- **source packet：** `03_topic_candidates/20260521__top20-screening-pack__reworked.md` #4
- **pack_score：** 36（Top20 第4）
- **judge_score：** 8/10
- **signal_type：** heat（GPT-5.4 生产级 + 语音 Agent 平台破圈）
- **heat signal：** GPT-5.4 生产级落地；OpenAI 官方页面收录；AMP 平台已有商业客户
- **evidence signal：** AI Agent Management Platform（AMP）；GPT-5.4 生产级（非公测）
- **裁判备注：** OpenAI 官方背书，语音 Agent 平台有强 B2B 叙事，补强商业场景

---

### #4｜OpenAI Voice 模型家族
- **URL：** https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api
- **source packet：** `03_topic_candidates/20260521__top20-screening-pack__reworked.md` #5
- **pack_score：** 36（Top20 第5）
- **judge_score：** 8/10
- **signal_type：** evidence（技术突破 + API 落地）
- **heat signal：** OpenAI 官方发布；语音模型新品；实时语音 Agent 技术突破
- **evidence signal：** GPT-Realtime-2（GPT-5级推理）+ Translate + Whisper；API 接口已开放；生产可用
- **裁判备注：** 技术落地信号强，content-writer 可直接写产品评测视角

---

### #5｜NVIDIA Nemotron 3 Nano Omni
- **URL：** https://blogs.nvidia.com/blog/nemotron-3-nano-omni-multimodal-ai-agents/
- **source packet：** `03_topic_candidates/20260521__top20-screening-pack__reworked.md` #3
- **pack_score：** 32（Top20 第3）
- **judge_score：** 8/10
- **signal_type：** evidence（开源多模态模型 + 6个 leaderboard 第一）
- **heat signal：** NVIDIA 官方发布；开源模型新品；多模态 Agent
- **evidence signal：** 统一视觉/音频/语言；6个 leaderboard 第一；已开放下载
- **裁判备注：** 开源多模态 Agent 模型，RLHF 对齐有新意，技术内容可写深

---

## Holdout 3 备选板

### 🔻 #6｜Vera CPU（备选第1）
- **URL：** https://blogs.nvidia.com/blog/vera-cpu-delivery/
- **source packet：** `03_topic_candidates/20260521__top20-screening-pack__reworked.md` #6
- **pack_score：** 31（Top20 第6）
- **judge_score：** 8/10
- **signal_type：** evidence（全新硬件品类量产交付）
- **heat signal：** NVIDIA 首款 Agent 专用 CPU；首批交付 Anthropic / OpenAI / SpaceXAI / Oracle
- **evidence signal：** 量产交付（非纸面发布）；全新硬件品类确立
- **进板条件：** 若 Top 5 中任一对象在 topic-planner 阶段被判定 supply gap，则 Vera CPU 补位
- **supply gap 触发条件：** 5个主推对象中有 ≥2 个存在信源弱/无商业场景/无数据支撑问题

---

### 🔻 #7｜Ineffable + NVIDIA RL基础设施（备选第2）
- **URL：** https://blogs.nvidia.com/blog/ineffable-intelligence-reinforcement-learning-infrastructure/
- **source packet：** `03_topic_candidates/20260521__top20-screening-pack__reworked.md` #9
- **pack_score：** 29（Top20 第9）
- **judge_score：** 8/10
- **signal_type：** evidence（RL 基础设施投资）
- **heat signal：** 新一代 RL 基础设施；NVIDIA 联合投资
- **evidence signal：** 模型训练层基础设施；RL 技术栈方向确立
- **进板条件：** 若行业叙事需要"AI 基础设施"长线布局，Ineffable 可作备选；弱于 Dell/DeployCo 的企业落地信号
- **supply gap 触发条件：** 当 Top 5 中企业级 Agent 叙事过于集中，需要 RL 层补充视角时启用

---

### 🔻 #8｜OpenAI Dell 合作（备选第3）
- **URL：** https://openai.com/index/dell-codex-enterprise-partnership
- **source packet：** `03_topic_candidates/20260521__top20-screening-pack__reworked.md` #7
- **pack_score：** 29（Top20 第7）
- **judge_score：** 8/10
- **signal_type：** evidence（企业本地 Agent 部署合规场景）
- **heat signal：** OpenAI + Dell 联合；企业本地化；安全合规叙事
- **evidence signal：** Codex 企业本地化；混合云/本地部署已有标杆；合规场景落地
- **进板条件：** 与 #2 SAP Trust 叙事互补；若 topic-planner 发现"企业合规"角度未被充分覆盖，Dell 补位
- **supply gap 触发条件：** 当"企业本地部署"角度缺失，而市场关注度高时启用

---

## 供给缺口说明（supply gap）

**Top 8→Top 5 强候选清单：** #1/#2/#3/#4/#5/#6/#9/#7（pack_score 29-47）
- 达到 8 分以上的强候选共 8 个，恰好覆盖 Top 5 + Holdout 3
- 剩余 12 个 Top20 对象均因 score ≤ 25 或 redteam 降权至 6/10 及以下，本轮不具竞争力
- **无 supply gap，无须凑数**

---

## pipeline 状态

| 工序 | 状态 | 产出 |
|------|------|------|
| Top20 初筛包 Reworked | ✅ final | `20260521__top20-screening-pack__reworked.md` |
| Top20 裁判评分卡 | ✅ final | `20260521__top20__stage-gate-scorecard.md` |
| **Top 5 建议板** | **✅ final** | **本文档** |
| platform-task-sheet | ⏳ 待 topic-planner | — |
| content-pack | ⏳ 待 content-writer | — |
| redteam + scorecard | ⏳ 待 redteam-reviewer | — |

---

## 下一步 Owner

| 动作 | Owner | 截止 |
|------|-------|------|
| 生成 platform-task-sheet（基于 Top 5 主推板） | topic-planner | 2026-05-21 19:00 CST 前 |
| 生成 content-pack | content-writer | 接收到 task-sheet 后 |
| 红队骂稿（content-pack 完成后） | redteam-reviewer | 收到 content-pack 后 |
| 裁判评分卡（content-pack 红队后） | market-editor | 收到红队骂稿后 |

---

**19:00 CST deadline 有效（当前 17:25，仍有窗口）**