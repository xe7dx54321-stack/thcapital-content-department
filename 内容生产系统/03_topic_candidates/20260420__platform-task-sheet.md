# 20260420 平台任务单

- `date`: `2026-04-20`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-20 18:34 CST`
- `input_top5_board`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260420__daily-top8-to-top5.md`
- `input_scorecard`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260420__top20__stage-gate-scorecard.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `rework + continuity_only；mini_slate 条件成立；Top5 板 final；执行 limited task sheet：wechat 2 槽 + 另外 2 平台各 1 槽，其余写入 holdout`
- `morning_flash_overlap_check`: `已查：无重叠`

---

## 全局主池 Top6（来自 Top5 板 + Holdout 板）

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|---|---|---|---|---|
| 1 | `ram_shortage_ai_infra` | AI 产业叙事从"模型能力"切向"硬件供给"，算力瓶颈成新主线 | 全球 HBM 产能紧张 + DeepSeek 突围形成叙事对冲；AI Infra / 算力租赁 / 芯片创业均受直接驱动 | 缺 SK 海力士/美光/三星具体产能数字，需补证 |
| 2 | `claude_design_figma_disruption` | AI 产品层直接颠覆成熟工具第一个可量化信号（设计圈恐慌） | 有截图 / 用户反馈；一人公司 / Agent 替代 SaaS 叙事强；Figma 为私有公司，**须删股价数据** | 股价 7% 为不可验证数据（scorecard FATAL），须改为"设计圈负面讨论爆发"叙事 |
| 3 | `opus47_negative_reception` | Anthropic 模型口碑问题揭示能力边界真实状态 | 社区持续焦点；负面信号比正面更有传播力；用户反弹 = 商业竞争空隙 | 缺 Reddit/HN 具体帖子 URL，须补证 |
| 4 | `llama_cpp_speculative_checkpointing` | 本地推理基础设施重大更新，影响开发者 / 一人公司选型 | Apple Silicon M 系列友好；与"个人 AI 算力"叙事高度相关 | 缺具体 GitHub PR URL，须补 |
| 5 | `opus47_vs_qwen35b_replacement` | 社区自发对比 = 模型能力感知信号 | Qwen3.6-35B-A3B 国产开源突破侧面印证；Agent / builder 选型参考价值高 | 个例体验难量化；缺 LM Arena 客观评测数据 |
| 6 | `swiss_government_microsoft_independence`（holdout） | 政府侧去微软化 = 开源 / 本土软件机会窗口 | HN 热度真实；SaaS 替代叙事的政策维度 | 执行周期长；非 AI 原生话题 |
| 7 | `sima2_deepmind_agent`（holdout） | DeepMind SIMA 2 = 最接近通用数字 Agent 的官方公示 | 一手性强；AI Agent 赛道定义意义 | Demo 效果 ≠ 实际部署；日期须核实为 2025-11-13 |

---

## 三个最重要平台任务单（continuity_only 模式）

> `stage_gate_status=continuity_only`；最多覆盖 3 个最重要平台；每个平台先保 1 个任务槽位

| 优先级 | 平台 | topic_key | 核心产出目标 |
|---|---|---|---|
| 1 | `wechat` | `ram_shortage_ai_infra` | 完整叙事主稿：算力瓶颈重塑 AI 产业竞争格局 |
| 2 | `wechat` | `claude_design_figma_disruption` | 深度分析稿：设计工具圈恐慌（删股价后叙事） |
| 3 | `x` | `opus47_negative_reception` | 快讯 / 观点钩子：Opus 4.7 口碑翻车信号 |
| 4 | `zhihu` | `llama_cpp_speculative_checkpointing` | 技术选型分析：本地推理效率临界点 |
| 5 | `bilibili` | `opus47_vs_qwen35b_replacement` | 对比向内容：开源模型平权信号 |

> `xiaohongshu` 和 `toutiao` 本轮 0 个 active slot，候选题保留在 holdout 池，下轮可按需启用

---

## 六个主战场任务单

### `wechat`

#### Task 1
- `topic_key`: `ram_shortage_ai_infra`
- `目标读者`: AI 创业者、Agent 开发者、算力投资者、一人有公司
- `切入角度`: 从"算力瓶颈"这个被忽视的产业真相出发，而不是重复模型能力叙事
- `核心论点`: 全球 HBM 产能持续紧张正在重塑 AI 产业竞争格局——不是谁模型更强，而是谁先拿到算力。国产芯片突围的时机恰逢这个结构性窗口。
- `证据抓手`:
  - HN 原帖（可访问）：`https://news.ycombinator.com/item?id=47822414`
  - **scorecard 要求补证**：SK 海力士 / 美光 / 三星 HBM 产能具体数字
  - 关联叙事：DeepSeek V4 去 CUDA 化与算力瓶颈形成双线呼应（scorecard top20_mini_slate P0）
- `source_ref_bundle`: `HN + 待补 HBM 三大厂产能数据 + Cerebras/GPU 交货周期（market-scout 补）`
- `视觉建议`: 算力产业链图谱（境外 HBM 三巨头 vs 国产算力突围双线对照）
- `为什么适合该平台`: 微信承担完整叙事，是本轮最高影响力出口

#### Task 2
- `topic_key`: `claude_design_figma_disruption`
- `目标读者`: 设计师、一人有公司、Agent/SaaS 投资人
- `切入角度`: **严格删除股价数据**（scorecard FATAL：Figma 为私有公司无股价），改为"设计工具圈恐慌"传播现象分析
- `核心论点`: Claude Design 功能引发设计社区大规模讨论——不是股价数字，而是工作流正在被重新定义的信号。对一人公司而言，这意味着"AI 替代 SaaS"从概念进入实战。
- `证据抓手`:
  - **scorecard FATAL 修复**：必须删除"股价下跌 7%"数据
  - 补证要求：36 氪 / 机器之心 Claude Design 具体文章 URL
  - 设计圈社媒讨论截图（Twitter/X / Reddit 设计师社区）
- `source_ref_bundle`: `待补 36 氪/机器之心文章 + 设计圈社媒讨论`
- `视觉建议`: Claude Design 功能截图 vs 设计圈 reaction 对照图
- `为什么适合该平台`: 微信提供深度分析场景，适合把"现象"展开为"趋势判断"

---

### `x`

#### Task 1
- `topic_key`: `opus47_negative_reception`
- `目标读者`: AI 开发者、模型评测社区、Anthropic 关注者
- `切入角度`: "升级后翻车"这个具体时刻，是用户对 AI 能力边界最诚实的反馈窗口
- `核心论点`: Opus 4.7 发布后社区大规模负面反馈，揭示大模型能力提升遭遇瓶颈的信号——同时也是 Qwen3.6 等竞品的进攻窗口。
- `证据抓手`:
  - **scorecard 要求补证**：Reddit/HN 具体 Opus 4.7 负面帖子 URL
  - 36kr 原文（部分可访问）：`https://www.36kr.com/p/3770733959496194`
- `source_ref_bundle`: `Reddit/HN 待补 + 36kr`
- `视觉建议`: Opus 4.7 vs 4.6 用户反馈对比；Qwen3.6-35B 性价比对照
- `为什么适合该平台`: X 是 AI 开发者社区核心战场，快讯 + 观点钩子传播效率最高

---

### `zhihu`

#### Task 1
- `topic_key`: `llama_cpp_speculative_checkpointing`
- `目标读者`: 本地推理开发者、Apple Silicon 用户、Llama.cpp 贡献者 / 爱好者
- `切入角度`: 这不是普通版本更新——speculative checkpointing 在 M 系列芯片上的效率提升，代表"个人 AI 算力"从不可能到可能的临界点
- `核心论点`: llama.cpp 合并 speculative checkpointing 后，本地推理效率显著提升，尤其是 Apple Silicon。对 Agent 构建者和一人公司而言，本地模型已足够支撑大量工作流
- `证据抓手`:
  - **scorecard 要求补证**：GitHub 具体 PR URL（Reddit 链接不具体）
  - r/LocalLLaMA 社区讨论
- `source_ref_bundle`: `GitHub PR（待补）+ r/LocalLLaMA`
- `视觉建议`: M系列芯片推理效率提升示意；llama.cpp 架构图
- `为什么适合该平台`: 知乎技术受众浓度高，适合技术原理 + 实用选型指南结合

---

### `bilibili`

#### Task 1
- `topic_key`: `opus47_vs_qwen35b_replacement`
- `目标读者`: AI 爱好者、模型选型用户、B 站科技区观众
- `切入角度`: 社区用户自发"换模型"行为背后的逻辑：不是因为 Opus 4.7 差，而是因为 Qwen3.6 已经足够好——这是一个"开源模型平权"的信号
- `核心论点`: 用户主动从 Opus 4.7 切换到 Qwen-35B-A3B，核心不是"哪个更强"，而是"性价比和本地部署能力"已经改变选型逻辑。国产开源模型进入实用窗口
- `证据抓手`:
  - **scorecard 要求补证**：Reddit 具体帖子 URL + LM Arena 量化数据
  - r/LocalLLaMA 社区自发对比帖
- `source_ref_bundle`: `Reddit（待补）+ LM Arena 数据（待补）`
- `视觉建议`: Opus 4.7 vs Qwen3.6-35B 能力雷达图对比；社区切换讨论切片
- `为什么适合该平台`: B 站适合视频化呈现对比； bilibili 科技区用户对"哪个模型更好用"话题接受度高

---

### `xiaohongshu`
- **本轮 0 个 active slot**
- 备选题保留在 holdout；若本轮 4 个主槽位补证顺利，下轮可启用

### `toutiao`
- **本轮 0 个 active slot**
- 备选题保留在 holdout；若本轮 4 个主槽位补证顺利，下轮可启用

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: **是，推荐**
- `理由`: `ram_shortage_ai_infra` 是本轮受众最宽、AI Infra 搜索意图最清晰的主线，适合百家号 SEO 长尾覆盖。百家号用户对"AI 算力""芯片"等关键词有持续搜索需求，且与去 CUDA 化叙事可形成内部互链
- `承接哪篇主稿更优`: 优先镜像 `wechat Task 1（ram_shortage_ai_infra）`；次选镜像 `wechat Task 2（claude_design_figma_disruption）`，但须先完成 FATAL 修复（删股价）

---

## Holdout 清单

### `swiss_government_microsoft_independence`
- `为什么能进最终池`: 政府侧去微软化 = 开源 / 本土软件机会窗口；HN 热度真实；SaaS 替代叙事的政策维度，与信创 / 去美化横向可比
- `为什么这轮没选`: 本轮 wechat 2 槽已被 ram_shortage 和 claude_design 饱和占用；其余平台槽位优先给了 AI 原生话题；瑞士政府 IT 周期偏长，非当日最强信号
- `什么时候可捞回`: 若 wechat Task 1/2 任一补证失败、锁题撞车或展开不足，按原题接力；或下一轮升级为 P1 主动题时重新进入

### `sima2_deepmind_agent`
- `为什么能进最终池`: DeepMind 官方发布，一手性最强；是 AI Agent 赛道目前最接近"通用数字 Agent"的产品公示，对 Agent 叙事有定义价值
- `为什么这轮没选`: scorecard 标注日期须修正为 2025-11-13（时效重新核实后才能激活）；本轮 Agent 叙事已由 opus47_negative_reception + opus47_vs_qwen35b 覆盖；平台槽位有限
- `什么时候可捞回`: signal-scout 修正日期为 2025-11-13 后，且确认是研究预览 vs 正式产品阶段；若正式产品发布则升级为 P1 并优先进入下一轮 Top5

---

## 补证任务（供 signal-scout / market-scout 追踪）

| 任务编号 | topic_key | 要求 | 责任方 | 截止 |
|---|---|---|---|---|
| C-01 | `ram_shortage_ai_infra` | 补 SK 海力士/美光/三星 HBM 产能具体数字 | signal-scout + market-scout | 2026-04-21 12:00 CST |
| C-02 | `claude_design_figma_disruption` | **删除股价数据**（Figma 私有公司）；补 36 氪/机器之心文章 URL | signal-scout | 即时 |
| C-03 | `opus47_negative_reception` | 补 Reddit/HN 具体 Opus 4.7 负面帖子 URL | signal-scout | 即时 |
| C-04 | `llama_cpp_speculative_checkpointing` | 补具体 GitHub PR URL | signal-scout | 即时 |
| C-05 | `opus47_vs_qwen35b_replacement` | 补 Reddit 帖子 URL + LM Arena 量化数据 | signal-scout | 即时 |
| C-06 | `sima2_deepmind_agent` | 修正日期为 2025-11-13；核实研究预览 vs 正式产品 | signal-scout | 下一轮复评前 |

---

## 平台任务单自评

- `active_slots_count`: 5（wechat×2 + x×1 + zhihu×1 + bilibili×1）
- `holdout_count`: 2（swiss_government + sima2）
- `xiaohongshu_slots_this_round`: 0
- `toutiao_slots_this_round`: 0
- `pua_triggered`: 未触发（任务框架已清晰，无连续返工）
- `scorecard_cross_validation`: 已执行——Figma 股价 FATAL 已在 Task 2 平台任务中标注删除，content-writer 严禁引用股价数据
