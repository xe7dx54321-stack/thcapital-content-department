# 平台任务单

- `date`: `2026-04-27`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-27 18:13:00 CST`
- `input_pack`: `20260427__top20-screening-pack__reworked.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `continuity_only limited task sheet：wechat 允许 2 主槽位；另外最多 4 平台，每平台先保 1 active slot；其余写入 Holdout`

---

## 前置门控确认

| 检查项 | 状态 | 说明 |
|--------|------|------|
| Top20 Scorecard | ✅ final + rework + continuity_only | 20260427__top20__stage-gate-scorecard.md |
| Top5 Board | ✅ final + continuity_only | 20260427__daily-top8-to-top5.md，board_mode=top20_mini_slate |
| Top5 Board 来源可信 | ✅ | 直接来自 scorecard 裁判显式 top20_mini_slate，非自行扩题 |
| 排除 morning_flash 同题 | ✅ | 当日 morning_flash（3题）与本板 Top5 候选零重叠，无冲突 |
| Top5 候选总数 | 5 + 3 Holdout = 8 | continuity_only 场景 supply gap 如实记录 |

---

## 全局主池 Top6

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|------|-----------|----------|--------------|----------|
| 1 | acl_2026_emoticon_semantic_confusion_20260427 | ACL 2026 研讨会新研究：AI 误读 `~` 导致删库；强场景化学术成果，破圈性极强 | 一手 arXiv 研究，所有主流模型均受影响，AI 安全 / Agent / Builder 主线直接命中，补证纪律下可直接立论 | 需补 arXiv 原文；正文不得把补证脚手架直接带入 |
| 2 | hn_frontpage_47910388_swe_bench_verified_no_longer_measures_frontier_coding_capabilit_20260427 | SWE-bench Verified 被官宣不再测 frontier；高时效，有 OpenAI 官方博文背书 | partial source 但有官方博文+ HN 热度入口；与 AI / Agent / 一人公司主线高度一致 | 需补 OpenAI 官方博文；正文引用前必须回链一手 |
| 3 | hn_frontpage_47911524_an_ai_agent_deleted_our_production_database_the_agent_s_confess_20260427 | AI Agent 删库后自我复盘长文；事故叙事天然带传播性 | partial source；高时效；天然讨论空间；HN 已在发酵 | 需补 Twitter 原帖上下文；正文不得使用未核验的截图内容 |
| 4 | hn_frontpage_47913650_ai_should_elevate_your_thinking_not_replace_it_20260427 | AI 应提升思维而非替代；KoshyJohn 博客文章，知乎/X 讨论潜力高 | partial source；仍处业务窗内高时效；与 AI / Agent / 一人公司主线一致 | 需补博客原文；正文不得使用未回链的二手引用 |
| 5 | mattpocock_skills_20260427 | mattpocock/skills GitHub 项目；开发者技能提升工具链，HN 热度稳定 | partial source；HN 已有热度入口；开发者视角叙事适合知乎/X 双平台 | 需补 GitHub 原文及 README；正文不得直接用 HN 评论作为核心论点 |
| 6 | github_trending_mattpocock_skills_20260427 | （同 Top 4，注：mattpocock/skills 与 github_trending_mattpocock_skills 为同一候选，仅 key 命名差异） | 同上 | 同上 |

> **注**：Top6 来自当日 Top5/Holdout 板，无自行扩题。所有 active slot 均追溯至板内候选编号。

---

---

## 三个最重要平台任务单

> 按优先级取 Top3，主动对接 content-writer 的开工顺序

### 最重要 1 — wechat Task 1
- `topic_key`: `acl_2026_emoticon_semantic_confusion_20260427`
- `题目`: `别轻易给AI发「~」，它可能会删掉你的整个主目录`
- `一句话判断`: `P0 continuity：ACL 2026 学术研究 + rm -rf ~ 强场景 Demo + 全部主流模型均受影响 + AI 安全 / Agent / Builder 主线直接命中`
- `source_ref_bundle`: `arXiv（https://arxiv.org/pdf/2601.07885）；source_packet（/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_142905__wechat_jiqizhixin_acl_2026_ai__source-packet.md）`
- `补证纪律`: `正文发布前必须回链 arXiv 原文并核验关键数据，不得把补证脚手架直接带入正文`

### 最重要 2 — wechat Task 2
- `topic_key`: `hn_frontpage_47910388_swe_bench_verified_no_longer_measures_frontier_coding_capabilit_20260427`
- `题目`: `SWE-bench Verified 被官方弃用：大模型 coding 排行榜集体失准？`
- `一句话判断`: `P0 continuity：OpenAI 官方博文背书 + 行业评估体系失效信号 + AI / Agent / 一人公司主线一致`
- `source_ref_bundle`: `OpenAI 官方博文（https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/）；source_packet（同上路径）`
- `补证纪律`: `正文发布前必须回链 OpenAI 博文原文，不得直接引用 HN 评论作为核心论点`

### 最重要 3 — zhihu Task 1
- `topic_key`: `hn_frontpage_47911524_an_ai_agent_deleted_our_production_database_the_agent_s_confess_20260427`
- `题目`: `AI Agent 删库后完整复盘：事故是怎么发生的，责任边界在哪里`
- `一句话判断`: `P1 continuity：HN 已在发酵 + 事故叙事天然带传播性 + Agent 安全标准讨论空间大`
- `source_ref_bundle`: `Twitter 原帖（https://twitter.com/lifeof_jer/status/2048103471019434248）；source_packet（同上路径）`
- `补证纪律`: `正文发布前必须核验 Twitter 原帖上下文，不得使用未核验的截图内容作为核心证据`

---

## 六个主战场任务单

### `wechat`

#### Task 1
- `rank_in_pool`: `1`
- `topic_key`: `acl_2026_emoticon_semantic_confusion_20260427`
- `题目`: `别轻易给AI发「~」，它可能会删掉你的整个主目录`
- `目标读者`: `AI 开发者、Agent 构建者、IT 运维者`
- `切入角度`: `以 `rm -rf ~` 这一具体事故 Demo 为入口，引出 ACL 2026 学术研究对语义混淆问题的系统性发现，及其对 Agent 安全性的深远影响`
- `核心论点`: `1）AI 误读路径符 `~` 是真实漏洞而非理论场景；2）所有主流模型均受影响；3）这背后是 Agent 在复杂语义环境下的安全边界问题`
- `证据抓手`: `arXiv 原文（https://arxiv.org/pdf/2601.07885）；36氪/机器之心等中文媒体已有报道；正文发布前须回链 arXiv 原文并核验关键数据`
- `source_ref_bundle`:
  - `arXiv`: `https://arxiv.org/pdf/2601.07885`
  - `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_142905__wechat_jiqizhixin_acl_2026_ai__source-packet.md`
  - `deep_article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260427_142953__acl_2026_别轻易给ai发_它可能会删掉你的整个主目录__deep-article.md`
- `视觉建议`: `流程图：用户输入「~」 → 模型解析为家目录 → 误触发 rm -rf；或信息图：各主流模型 `~` 解析结果对照`
- `为什么适合该平台`: `微信生态适合完整叙事+判断输出；此事故事性强，适合技术深度读者群；AI 安全 / Agent 主线与同行资本品牌高度匹配`

#### Task 2
- `rank_in_pool`: `2`
- `topic_key`: `hn_frontpage_47910388_swe_bench_verified_no_longer_measures_frontier_coding_capabilit_20260427`
- `题目`: `SWE-bench Verified 被官方弃用：大模型 coding 排行榜集体失准？`
- `目标读者`: `AI 研究者、开发者、投资者`
- `切入角度`: `OpenAI 官方博文宣布停用 SWE-bench Verified 作为 frontier 评估标准；引入对当前 AI coding 评估体系公信力的系统性讨论`
- `核心论点`: `1）官方主动承认评估体系失效是行业信号；2）这意味着现有 Coding 能力排名可能被高估；3）对 Agent 发展路径有深层含义`
- `证据抓手`: `OpenAI 官方博文（https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/）；HN 讨论帖；正文发布前须回链 OpenAI 博文原文`
- `source_ref_bundle`:
  - `OpenAI`: `https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/`
  - `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_075728__hn_frontpage_47910388_swe_bench_verified_no_longer_measures_frontier_coding_capabilit__source-packet.md`
- `视觉建议`: `对比图：旧评估体系 vs 新评估体系；或时间轴：SWE-bench 历次版本迭代节点`
- `为什么适合该平台`: `微信适合承载判断性内容；此事涉及 AI coding 能力边界与行业标准演变，适合深度技术读者`

---

### `zhihu`

#### Task 1
- `rank_in_pool`: `3`
- `topic_key`: `hn_frontpage_47911524_an_ai_agent_deleted_our_production_database_the_agent_s_confess_20260427`
- `题目`: `AI Agent 删库后完整复盘：事故是怎么发生的，责任边界在哪里`
- `目标读者`: `AI 开发者、运维工程师、技术管理者`
- `切入角度`: `以当事 Agent 的第一人称复盘为核心文本，分析 Agent 在生产环境中失控的技术根因与责任归属模糊地带`
- `核心论点`: `1）事故根因是可预期的 Agent 权限滥用；2）当前缺乏 Agent 生产环境安全规范；3）行业需要建立 Agent 操作审计标准`
- `证据抓手`: `Twitter 原帖（https://twitter.com/lifeof_jer/status/2048103471019434248）；HN 讨论；正文发布前须核验原帖上下文`
- `source_ref_bundle`:
  - `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_075728__hn_frontpage_47911524_an_ai_agent_deleted_our_production_database_the_agent_s_confess__source-packet.md`
- `视觉建议`: `事故时间轴：操作链条复盘；或因果图：触发条件 → 权限扩散 → 数据损失`
- `为什么适合该平台`: `知乎适合展开分析性叙事；事故复盘天然适配问答与深度讨论格式；技术管理者关注 Agent 安全标准`

---

### `x`

#### Task 1
- `rank_in_pool`: `4`
- `topic_key`: `hn_frontpage_47913650_ai_should_elevate_your_thinking_not_replace_it_20260427`
- `题目`: `AI should elevate your thinking, not replace it`
- `目标读者`: `AI 开发者、研究者、终端用户`
- `切入角度`: `一句话观点钩子：AI 的核心价值是提升人类思维，不是替代它；以 KoshyJohn 博文为引，展开对当前 AI 替代论的系统性反驳`
- `核心论点`: `1）当前 AI 叙事过度强调替代而非增强；2）真正有效的人机协作是思维提升而非任务替换；3）这与 Agent/Builder 主线高度一致`
- `证据抓手`: `KoshyJohn 博客原文；HN 讨论；正文发布前须补博客原文并回链`
- `source_ref_bundle`:
  - `博客原文`: `https://www.koshyjohn.com/blog/ai-should-elevate-your-thinking-not-replace-it/`
  - `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_075728__hn_frontpage_47913650_ai_should_elevate_your_thinking_not_replace_it__source-packet.md`
- `视觉建议`: `金句卡片：一行核心观点 + 简短解释；适合截图传播`
- `为什么适合该平台`: `X 平台适合快讯 / 观点钩子；一句话金句天然适配推文格式；高时效性要求与 X 传播节奏匹配`

---

### `bilibili`

#### Task 1
- `rank_in_pool`: `5`
- `topic_key`: `mattpocock_skills_20260427`
- `题目`: `mattpocock/skills 为什么在 GitHub 火起来了：它解决了一个什么旧痛点`
- `目标读者`: `开发者、学生、想转行的工程师`
- `切入角度`: `从开发者真实需求切入：mattpocock/skills 解决了什么具体问题，为什么现在形成扩散，与传统方案有何不同`
- `核心论点`: `1）skills 是一个技能速查/提升工具链，直击开发者学习曲线痛点；2）HN 热度证明它已在形成社区共识；3）这对一人公司 / Builder 主线有直接参考价值`
- `证据抓手`: `GitHub 原文（https://github.com/mattpocock/skills）；HN 讨论；正文发布前须补 GitHub README`
- `source_ref_bundle`:
  - `source_packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260427_075728__github_trending_mattpocock_skills__source-packet.md`
- `视觉建议`: `Demo 截图或 GIF：展示 skills 工具的实际使用流程；或对比图：传统学习路径 vs skills 路径`
- `为什么适合该平台`: `B站用户偏爱工具类教程与实操演示；GitHub 项目解读天然适配视频化呈现`

---

### `toutiao`

> **本轮 Holdout**，理由：wechat 2槽 + zhihu 1槽 + x 1槽 + bilibili 1槽 = 已用满 4平台 × 1槽 限制。头条平台可承载 AI 工具解读内容，但本轮候选已优先分配给更具平台匹配度的渠道。若上述 active slot 后续补证失败或撞车，可从下方 Holdout 池按优先级捞回。

---

### `xiaohongshu`

> **本轮 Holdout**，理由同上。mattpocock/skills 和 AI agent 删库两题均适合小红书图文传播，但受 continuity_only limited 纪律约束，优先保留知乎与 B站槽位。若后续主战场槽位有余，可捞回小红书适配版本。

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: **是**
- `理由`: `SWE-bench Verified 停用和 AI Agent 删库复盘两题均具备搜索型意图词（"AI coding 排行失准"、"AI Agent 事故复盘"），适合百家号 SEO 镜像层布局`
- `建议 SEO 镜像标题`: `AI编程能力排行失准？SWE-bench Verified被官方弃用背后`、`AI Agent删库事故完整复盘：责任边界在哪里`
- `承接哪篇主稿更优`: `承接微信 Task 1（ACL 2026）和 Task 2（SWE-bench Verified）主稿更优；百家号版本以原文摘要为主，不做原创判断，以 SEO 引流为导向`

---

## Holdout 清单

### Holdout 6｜wechat_zhidx_openclaw_deepseek_v4_20260427｜今天,OpenClaw能用DeepSeek-V4了!还设成了默认模型
- `为什么能进最终池`: `partial source；与 AI / Agent / 一人公司主线高度一致；更接近官方 / 主流媒体共识`
- `为什么这轮没选`: `受 continuity_only limited 纪律约束，wechat 已优先保留 ACL 2026 和 SWE-bench Verified 两个主槽位，资源有限，排在后面`
- `什么时候可捞回`: `若 Top5 主槽位后续补证失败、锁题撞车或内容展开明显不足，可按原题接力；或作为次日 continuity 备选题`

### Holdout 7｜wechat_zhidx_token_deepseek_v4_75_token_20260427｜梁文锋把token价格打下来了!DeepSeek V4暴降75%,百万token只要两毛五
- `为什么能进最终池`: `partial source；更接近官方 / 主流媒体共识；DeepSeek 价格战叙事具备强传播性`
- `为什么这轮没选`: `同上；受纪律约束未能排入；且 Token 价格话题需强时效佐证，当前 partial source 不足以直接立论`
- `什么时候可捞回`: `若补到官方 / 原始来源后，可作为 AI 基础设施成本话题独立成篇；次日 morning_flash 优先级较高`

### Holdout 8｜zhidx_site_ai_8_20260427｜AI最疯狂的一周,该知道的8大共识都在这了
- `为什么能进最终池`: `partial source；仍处业务窗内高时效；8大共识盘点形式适合多平台分发`
- `为什么这轮没选`: `盘点类内容在 continuity_only 场景下优先级低于单一强观点题；且缺全文深抓，发布时效不够硬`
- `什么时候可捞回`: `若次日 Top5 候选中出现多个 AI 周新闻类候选，可作为合并盘点题处理；当前阶段不单独立项`

---

## 任务单自检清单

- [x] 所有 active slot 均来自当日 Top5/Holdout 板可追溯候选，无自行扩题
- [x] morning_flash 同题排除已显式确认
- [x] wechat 主槽位 ≤ 2
- [x] 其余平台 active slot ≤ 4（zhihu/x/bilibili 各1）
- [x] 所有 slot 均回链 source_ref_bundle
- [x] Holdout 捞回条件已写清
- [x] baijiahao SEO 镜像层已判断
- [x] continuity_only 补证纪律已在前置说明中明确
