# Redteam Review

- `date`: `2026-05-03`
- `stage`: `platform-task-sheet`
- `owner`: `redteam-reviewer`
- `review_target`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260503__platform-task-sheet.md`
- `generated_at`: `2026-05-03 18:10:00 CST`
- `review_posture`: `repair-first`
- `minimum_verification_done`: `partial`
- `checked_sources_or_actions`: `source_ref_bundle 链路核查 / 平台 slot 分配合理性检查 / 补证纪律核查 / 时效窗口评估 / board_mode 一致性检查`
- `topic_preservation_judgment`: `keep_and_fix`

## 总评

- `结论`: `今日平台任务单整体逻辑清晰，4 个 active slot 均来源 top20_mini_slate，board_mode 遵守 continuity_only 约束。但存在两个需要立即修复的结构性问题：（1）DeepSeek V4 时效窗口偏老（4月24日），需要 content-writer 在写稿前确认叙事仍有竞争力；（2）所有条目仍为 partial source，content-writer 必须补官方截图方可动笔。`
- `是否建议放行`: `有条件放行——4 个 active slot 均保留，但 content-writer 必须先完成补证动作才能算正式进入 drafting 阶段。`
- `最危险问题`: `DeepSeek V4（4月24日）距今已 9 天，若明日 Kimi K2.6 或 Qwen 新 benchmark 发布，此条价格叙事可能瞬间过时——但当前包并未触发任何新模型替代风险的预警机制。`
- `问题类型`: `repairable`
- `是否建议直接换题`: `no`
- `默认补救路径`: `补官方截图 / 时效风险预警 / 角度预调`

## 高优先级问题（必须修）

### P1：DeepSeek V4 时效窗口风险未被显式记录
- `问题`: `DeepSeek V4 首现于 Simon Willison 博客（4月24日），至今已 9 天。platform-task-sheet 在"主要风险"栏提到"需确认无更强新模型替代叙事"，但未制定具体的确认机制或触发换题条件。`
- `问题定性`: `fatal（若不处理）`
- `为什么严重`: `今天是5月3日，若明天（5月4日）Kimi K2.6 或 Qwen 新 benchmark 发布，DeepSeek V4 的价格叙事会被瞬间替代——届时已在 drafting 的稿件将面临角度推翻或直接废弃。`
- `我已经核查了什么`: `已确认截至今日 18:00，尚无 Kimi K2.6 / Qwen 新 benchmark 的官方发布记录；当前最强竞争模型动态仍以 DeepSeek V4 为最新可引用节点。`
- `会伤害什么结果`: `content-writer 在 DeepSeek V4 上耗费 2-3 小时 drafting，若明日被替代，时间成本浪费，且今日 19:00 死线前可能没有足够时间切换话题。`
- `优先补救动作`: `topic-planner 应在 platform-task-sheet 中补一条明确的"时效风险触发条件"：若明日 09:00 前有任何模型新 benchmark 发布，DeepSeek V4 条目自动降为 holdout，ruvnet/ruflo 候补升档。`
- `若补救失败，再考虑什么`: `content-writer 缩短 DeepSeek V4 篇幅，优先完成 VS Code 条目（时效更新、Github PR 一手锚点更强）。`

### P2：所有条目仍为 partial source，content-writer 补证纪律不明确
- `问题`: `4 个 active slot 的 source_ref_bundle 均标注 partial source 状态，platform-task-sheet 在"裁判备注"第1条写明"不得把 HN 评论、媒体报道等二手脚手架直接带进正文"，但未给出各条目的具体补证动作项（哪些页面需要截图）。`
- `问题定性`: `fatal（对内容可信度）`
- `为什么严重`: `content-writer 若不等补证直接动笔，很可能以 source packet 摘要作为事实依据——一旦发布后被读者查证发现引用偏差（如 DeepSeek 定价页面数字不准确），账号公信力受损。`
- `我已经核查了什么`: `已核对 4 个 active slot 的 primary_anchor 是否为可截图的官方/原始来源：DeepSeek V4→simonwillison.net（✅），VS Code→github.com/microsoft/vscode/pull/310226（✅），agent harness→mendral.com blog（✅），Flue→flueframework.com（✅）。`
- `会伤害什么结果`: `各平台发布后若核心引用数字/事实出错，需发更正声明，伤害账号专业形象。`
- `优先补救动作`: `platform-task-sheet 中对每个 active slot 补一条明确的"补证清单"，列明必须截图的官方页面；content-writer 动笔前必须完成截图并存入对应 draft pack assets。`
- `若补救失败，再考虑什么`: `若时间紧迫无法完成全部补证，降级该条目为"观点型写作"（明确标注"本文观点基于公开报道整理，数字以官方为准"），不做硬事实引用。`

## 中优先级问题（建议修）

- `问题`: `ruvnet/ruflo（GitHub Trending，36k stars）进入 holdout，但 holdout 说明只写了"视觉素材获取成本高"和"Xiaohongshu 本轮 slot 未开"，未给出明确的"什么条件下可捞回"的时间触发点。`
- `建议`: `补一条触发条件：若明日（5月4日）signal-scout 在 Top20 初筛包里再次抓到 ruvnet/ruflo 出现在 Trending 前三，则自动触发 topic-planner 复评，Xiv 和 Xiaohongshu 各留 1 个 active slot 给它。`

- `问题`: `WeChat Task 2（VS Code Co-Authored-by）切入角度为"开发者愤怒：consent 问题而非技术问题"——这个角度需要 HN 评论截图作为社区情绪证据，但补证清单里未列明需要哪些 HN 评论。`
- `建议`: `补证清单应列明：PR #310226 diff 截图（证明代码变更）+ HN Top3 评论截图（证明社区反弹烈度）。`

## 亮点（避免误杀）

- `值得保留的优点`: `4 个 active slot 均直接回链 top20_mini_slate，无临时扩题，board_mode 纪律遵守良好；VS Code 条目有 GitHub PR #310226 硬链接，一手性在 4 条中最强；X 平台选 agent harness outside sandbox，切当前 AI infra 安全焦虑，市场空白。`
- `为什么不该直接否掉`: `本轮 platform-task-sheet 结构完整，slot 分配有逻辑，board_mode 约束被尊重；主要问题都是"补证纪律需强化"而非"话题选错"。`

## 优先补救顺序

1. topic-planner 在 platform-task-sheet 中补"DeepSeek V4 时效风险触发条件"（今日 19:00 前）
2. topic-planner 对每个 active slot 补"补证清单"（今日 19:00 前）
3. content-writer 完成 4 个 active slot 的补证截图后开始 drafting（可与步骤1/2并行）

## 给 `market-editor` 的裁判提示

- `建议评分区间`: `7-8（满分按内容化就绪程度；当前包逻辑完整但补证未动笔，不能算 draft-ready）`
- `建议 rework_mode`: `supplement_evidence`
- `建议联动岗位`: `topic-planner（补触发条件+补证清单）+ content-writer（补证截图后动笔）`
- `是否建议保留原对象返工`: `yes`
- `低于8分的核心原因`: `补证未完成=内容可信度未经验证，不可视为 draft-ready；DeepSeek V4 时效风险未做机制性防控。`
- `若放行，需接受的风险`: `content-writer 若跳过补证直接动笔，发布后若被读者查证可能引发公信力危机。`
- `只有什么情况下才建议换题`: `DeepSeek V4 若在明日 09:00 前确认被新模型叙事替代，触发换题条件；其余条目暂不建议换。`