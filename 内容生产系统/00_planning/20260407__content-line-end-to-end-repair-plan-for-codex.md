# 同行资本市场内容系统｜内容线全链路修复方案（Codex 内部施工文档）

- `created_at`: `2026-04-07`
- `owner`: `Codex`
- `usage`: `内部施工方案；用于连续修复内容线，不面向老板直接汇报`
- `scope`: `复盘窗口 2026-04-02 ~ 2026-04-07；覆盖内容线输入、选题、锁题、成稿、发布、前台汇报全链路`
- `status`: `phase1_frontstage_truth_closed__top5_chain_installed__awaiting_live_observation`
- `last_updated`: `2026-04-07 13:02 CST`

## 0.1 当前施工进度

### 已完成

- `approved-topic` 已接入锁题真相字段：`lock_truth / source_top5_board_path / source_top5_board_status`
- 前台板已改成按真实状态暴露 `Top5 缺失 / Top5 背书缺失 / final gate 阻断 / dirty queue`
- `n/a` 脏发布对象已从正常待发布列表剥离，单独暴露为队列清洁问题
- 前台群 `routine issues` 已改成按真实阻断项汇报，不再把“有没有 approved-topic”误报成“今天会交付”
- `waiting_human_publish` 摘要已去重到话题级，并改成“发布任务”口径，避免跨平台重复 topic 造成伪重复展示
- `Top5` 真伪判断已统一为“板子内存在可用 candidate_key”，不再用“文件存在”冒充 ready
- `Top5` 缺失或空板时，`market_platform_lock_bridge.py` 现在会正式阻断，不再偷渡 approved-topic
- `platform-task-sheet -> approved-topic` 物化时，已强制校验 active task slots / Top6 池必须属于当日 Top5/Holdout 候选池
- 日间 cron 已补入正式 `Top 8 -> Top 5` 生成 heartbeat，平台任务单 prompt 也已改成“无 Top5 不继续”
- `Top5 / platform-task` 上游排班已后移：Top20 redteam/score、Top5、platform-task/redteam 心跳窗不再在前置产物出现前提前结束
- continuity limited task sheet 已具备 `Top5 missing` 时的 truthful same-day recovery 物化能力：只在 `continuity_only + limited_task_sheet` 下允许落 `fallback_task_sheet_only` approved-topic
- `market_content_heartbeat_queue.py` 已改成默认 `same-day only`，不再自动回退历史 backlog；仅在显式 `--allow-backlog` 时才允许历史库存补位
- continuity 版平台任务单解析已补齐老格式兼容：支持 `三个最重要平台任务单`、`Task 1 — 已锁题`、旧版 Top6 多列表格与 HB2 reworked pack 的 mini_slate topic_key 提取

### 正在进行

- 观察 `Top5` 新 heartbeat 的真实日内落地产物
- 观察平台任务单是否开始稳定引用当日 Top5，而不是继续写出脱链对象
- 观察 `same-day recovery` 是否只在 continuity_only + Top5 缺失时触发，且前台能如实暴露 `fallback_task_sheet_only`
- 观察 `19:00` 前是否能优先拿到 same-day 对象，而不是重新掉回 backlog

### 下一步

- 若 live run 仍缺 Top5，则继续补 `Top5` redteam / scorecard 子阶段或增强 prompt 约束
- 补齐 fallback publish-safe 与 deadline 保底机制

## 0. 本方案要解决什么

本轮不是修一个 bug，而是把内容线从“每天都在跑，但经常 deadline 挂零、状态失真、需要老板人工托底”修成“即便老板不介入，也能在业务日内稳定产出”。

这份方案只围绕 5 个结果负责：

1. `deadline 不再失守`
2. `老板不帮忙定题时，系统也能自己锁题`
3. `成稿真正能达到 publish-ready，而不是假闭环`
4. `晨间线和白天线都能给出明确、可信、可追责的最终结论`
5. `前台展示和 bot 汇报只反映真实状态，不再提前报喜`

---

## 1. 当前诊断结论

### 1.1 结论摘要

- 从 `2026-04-02` 到 `2026-04-07`，内容线没有形成稳定的自动自治交付能力。
- 前台板连续多日 `published_items_today = 0`，这意味着从“业务结果”口径看，系统持续失守。
- `Top5` 正式产物连续缺失，系统没有形成真正稳定的自动锁题机制。
- 晨间线连续失败，不是一个点的问题，而是 `内容脚手架污染 + bridge 断链 + 图片未进 HTML + checklist 状态错乱` 的复合系统病。
- 白天线即便上游 `Top20 / platform-task-sheet` 通过，也会在 `content-pack` 层晚于 deadline 被打回。
- 输入层从 `274 -> 86 -> 44 -> 40 -> 36` 快速塌陷，且 `2026-04-07` 出现核心源批量 soft fail。
- 发布队列已经从“当日交付出站口”退化成“历史积压大厅”，脏状态对象和旧 backlog 混在一起。
- 前台 bot 对外回报存在“未收口先报喜”的管理问题，放大了系统正在正常交付的假象。

### 1.2 本轮最核心的系统病

不是“写手不行”，也不是“某个脚本单点坏了”，而是以下 4 类系统病同时存在：

1. `硬门不够硬`
2. `状态机不统一`
3. `发布链与成稿链耦合方式错误`
4. `前台回报早于真实最终放行`

---

## 2. 施工总原则

### 2.1 真相优先于好看

- 前台板、bot 汇报、publish queue、approved-topic 必须以真实最终状态为准。
- 不允许“实际上还没过终门，但前台先说今天会交付”。

### 2.2 单一最终放行门

- `content-pack publish-ready` 才是白天线的真实交付门。
- `morning final verdict` 才是晨间线的真实发布门。
- 上游 `Top20 / platform-task-sheet / approved-topic` 都只能算中间态，不等于可发。

### 2.3 业务日口径优先

- 所有统计、筛选、前台展示、Top20 评比、白天线锁题，统一使用业务日窗口，不再混用自然日口径。

### 2.4 continuity 是保底，不是偷渡

- `continuity_only` 只能生成“应急候选板”或“保底对象”，不能伪装成 premium pass。
- 不允许用 continuity 产物偷偷物化正式 approved-topic。

### 2.5 历史 backlog 与当日业务彻底隔离

- 当日板只看当日业务日对象。
- 历史 backlog 单独归池，不能继续污染老板的判断。

### 2.6 不允许因为某一环不到 8 分导致整天挂零

- 目标仍然是 `premium >= 8`。
- 但系统必须有正式的 `publish-safe fallback` 机制，保证当天至少产出一篇达最低发布安全标准的稿件，而不是整天归零。

---

## 3. 问题总表与对应修复思路

## 3.1 P0 问题：直接导致 deadline 失守或挂零

### P0-1｜`Top5` 连续缺失，锁题机制失效

**现象**

- `top5_board_status` 连续多日为 `missing`
- 前台持续提示“若要继续推进成稿，需先拍板今日选题”
- 一旦老板不介入，系统容易挂零

**根因**

- `Top20 -> Top5 -> approved-topic` 没有形成硬产物链
- `Top5` 可能在记忆里存在，但没有真正对象化落盘
- approved-topic 构建器没有强依赖 Top5 正式产物

**修复思路**

1. 新增 `Top5 正式对象` 作为锁题前的必经产物
2. `approved-topic` 只能从 `Top5 board` 生成，不能直接从 platform-task-sheet 或 continuity mini slate 物化
3. `Top5 missing` 时，禁止任何“今日已自动锁题”的前台口径
4. 把 `老板拍板 / 自动锁题` 收敛为一个字段，不允许同时出现冲突表达

**触点**

- `09_runbooks/scripts/market_platform_task_sheet_to_approved.py`
- `09_runbooks/scripts/market_approved_topic_builder.py`
- `09_runbooks/scripts/market_lane_approved_topic_builder.py`
- `09_runbooks/scripts/market_platform_lock_bridge.py`
- `11_frontstage/*market-frontstage-board.md`

**验收标准**

- 每个业务日必须有一份正式 `Top5` 文件
- 没有 `Top5` 时，系统不得出现“已锁题”的正式对象
- 老板不拍板时，系统仍可完成自动锁题

### P0-2｜白天线上游 pass，不代表最终能交付

**现象**

- `Top20` 和 `platform-task-sheet` 过了 8 分
- 但 `content-pack` 在 19:00 后继续被打回
- 前台看起来可交付，实际草稿箱挂零

**根因**

- 真实最终放行门没有被明确建成系统硬门
- 平台任务单 pass 后，系统和前台都把它当成“今晚必交”
- `content-pack` 作为真实终门，却没有获得同级别的治理地位

**修复思路**

1. 明确白天线最终交付定义：只有 `content-pack >= 8 且 publish-ready=pass` 才算真实交付
2. 前台与 bot 汇报只能在该终门通过后宣告“今晚会入草稿箱”
3. 对 `Top20 / platform-task-sheet / approved-topic / content-pack` 增加统一 `stage_truth` 语义
4. 在 `market_pipeline_reconcile.py` 中增加“上游已过、下游未过”的红灯提示，不允许继续粉饰为交付中

**触点**

- `09_runbooks/scripts/market_pipeline_reconcile.py`
- `09_runbooks/scripts/market_pipeline_integrity_report.py`
- `09_runbooks/scripts/market_stage_artifact_status.py`
- `09_runbooks/scripts/market_frontstage_board_builder.py`

**验收标准**

- 任何对象若 `content-pack < 8`，前台不得展示为“今晚将入草稿箱”
- 每天 19:00 的“是否交付成功”只由 content-pack + publish-ready 决定

### P0-3｜continuity 被误用为正式推进通道

**现象**

- 低于 8 分的 Top20 / platform-task-sheet 仍在继续往后推进
- continuity mini slate 被后续流程当成准正式对象使用

**根因**

- continuity 没有被严格限制在“保底不停产”范围
- 产物语义不清，和 premium 通道混在一起

**修复思路**

1. continuity 对象统一改名为 `fallback_slate / limited_task_sheet`
2. continuity 产物默认禁止写入正式 approved-topic
3. 若真的启用保底发布，必须走独立的 `fallback_publish_safe` 状态，不可伪装 premium
4. 前台板新增 `premium_status` 与 `fallback_status` 两行，避免混淆

**触点**

- `09_runbooks/scripts/market_platform_task_sheet_to_approved.py`
- `09_runbooks/scripts/market_approved_topic_builder.py`
- `09_runbooks/scripts/market_frontstage_board_builder.py`

**验收标准**

- continuity 产物不会再直接出现在正式 approved-topic 中
- premium 与 fallback 在展示和队列中可明确区分

### P0-4｜晨间线没有稳定的最终 verdict 机制

**现象**

- 晨间线经常内容本身已经达标，但因为 bridge、result.json、图片、checklist 等原因挂掉
- 有时是内容层失败，有时是基础设施失败，有时两者同时失败

**根因**

- 晨间线没有一张统一的“最终结论卡”
- `technical_preflight`、`reviewer_checklist`、`leader_checklist`、bridge 状态分散在多处
- 没有把 `内容失败` 与 `infra 失败` 明确拆开

**修复思路**

1. 为晨间线新增统一的 `final verdict` 产物
2. verdict 强制输出以下 4 类状态：
   - `publish_success`
   - `blocked_by_content`
   - `blocked_by_infra`
   - `blocked_by_mixed_failure`
3. 把 `request.json / result.json / media_id / rendered_html_img_count / checklist pass/fail` 汇总到同一张卡
4. 8:30 前可以按规则重试，8:30 后必须给出终结 verdict，不再黑箱挂死

**触点**

- `09_runbooks/scripts/market_morning_flash_preflight.py`
- `09_runbooks/scripts/market_morning_flash_publish_guard.py`
- `09_runbooks/scripts/market_wechat_bridge_reconcile.py`
- `09_runbooks/scripts/market_manual_wechat_rescue.py`

**验收标准**

- 每个晨间对象都能落一张最终 verdict 卡
- 老板只看这一张卡，就能知道到底是内容问题还是桥接问题

### P0-5｜内容线缺少正式保底机制，导致整天可能挂零

**现象**

- 某个环节卡住，整天就可能没有公众号成品
- 目前“保底”更多依赖人工介入或临时判断

**根因**

- 没有系统化定义 `premium` 和 `fallback publish-safe`
- heartbeats 轮数、时间闸门、降级策略没有统一规则

**修复思路**

1. 定义两套终态：
   - `premium_publish_ready`: `>= 8`
   - `fallback_publish_safe`: `>= 7 且 truth-safe 且无 scaffold 且图片/排版/桥接可用`
2. 增加白天线时间闸门：
   - `15:30` Top5 必须落地
   - `16:30` approved topics 必须形成
   - `17:30` 若仍无 premium 成稿，自动启动 fallback lane
   - `19:00` 目标交付 2 篇 premium；若做不到，至少 1 篇 fallback publish-safe 不挂零
3. 增加每轮 heartbeat 次数，但只对关键对象启用，不无脑加压
4. fallback 不允许写安全/硬核证据题，只允许热点拆解、信号观察、产业判断类可保守表达的对象

**触点**

- `09_runbooks/scripts/market_content_heartbeat_queue.py`
- `09_runbooks/scripts/market_day_mainline_delivery_retry.py`
- `09_runbooks/scripts/market_stage_job_runner.py`
- `09_runbooks/scripts/market_publish_continuity_queue.py`

**验收标准**

- 白天线不再因为某一对象低于 8 分导致全天挂零
- fallback 发布有清晰标签，不污染 premium 学习样本

---

## 3.2 P1 问题：强依赖人工、状态失真、导致老板判断被污染

### P1-1｜输入层明显塌陷，且核心源批量 soft fail

**现象**

- intake 从 274 快速降到 36
- Anthropic、DeepMind、xAI、NVIDIA、OpenAI、OpenAIDevs、AnthropicAI 等核心源批量 `exit status 35`
- `deep_articles = 0`

**根因**

- source 健康度没有被正式治理
- 核心源抓取失败后，系统没有自动切换稳定兜底策略
- 输入层只统计总量，不审每个源是否退化

**修复思路**

1. 建立 `source health scorecard`
2. 对每个一级源定义：
   - expected_min_packets
   - fail_threshold
   - fallback_strategy
   - stale_threshold
3. 将 `web-access` 作为核心失败源的正式兜底通道，而不是临时人工外挂
4. 抓取 summary 不只写“拿到多少条”，还要写“哪些核心源掉了”
5. 增加重复源去重与机器之心等重复 bug 治理
6. 将输入层 KPI 正式写死：
   - `source_packets_business_day >= 100`
   - `primary_source_packets >= 30`
   - `deep_articles >= 6`
   - `核心一级源 soft fail <= 2`

**触点**

- `09_runbooks/scripts/market_topic_capture_round.py`
- `09_runbooks/scripts/market_daily_source_manifest.py`
- `09_runbooks/scripts/market_topic_radar_brief_builder.py`
- `09_runbooks/scripts/market_public_intake_board_builder.py`
- `09_runbooks/scripts/market_source_strategy_defs.py`
- `09_runbooks/scripts/market_wechat_deep_capture_round.py`

**验收标准**

- 连续 3 个业务日达到 `100+` intake
- source health board 能清楚指出是“源掉了”还是“今天确实没热点”

### P1-2｜旧话题回流、时效性判断失真

**现象**

- 旧热点在几天后重新被拉回选题池
- `published_at`、事件发生时间、热度上升时间没有被统一判断

**根因**

- `recent_topic_guard` 只看“是否撞题”，没有区分“事件已过期但热度仍在”这类情况
- 缺少 `event_age`、`heat_age`、`already_covered` 的综合判断

**修复思路**

1. 给所有候选新增 3 个字段：
   - `event_started_at`
   - `heat_detected_at`
   - `already_covered_at`
2. recent topic guard 不再做二元判断，而是做分层处理：
   - `hard_block`: 近期已发且无新进展
   - `re-angle_allowed`: 已发过但出现新进展或新角度
   - `late_but_hot`: 事件旧，但热度正在上升
3. 对晨间线和白天线使用不同口径：
   - 晨间线更重 `event_age`
   - 白天线更重 `heat_age + narrative novelty`

**触点**

- `09_runbooks/scripts/market_recent_topic_guard.py`
- `09_runbooks/scripts/market_topic_key_registry.py`
- `09_runbooks/scripts/market_lane_approved_topic_builder.py`

**验收标准**

- 不再出现明显已经过时的旧题被当日主线重新拉起
- 对“旧事件新角度”可以保留合法通道，不是一刀切

### P1-3｜publish queue 污染严重，无法反映当日业务真相

**现象**

- 队列中堆着大量 3 月底和 4 月初的旧对象
- 存在 `n/a` 脏对象
- waiting_human_publish 与 deferred 混在一起

**根因**

- 历史 backlog 未清理
- queue builder 没有做脏对象清扫
- 当前板没有区分“当日出站口”和“历史积压池”

**修复思路**

1. 队列拆分为 3 池：
   - `today_delivery_queue`
   - `human_action_backlog`
   - `historical_deferred_archive`
2. `n/a` 对象增加 scrubber，自动清除或隔离
3. 超过阈值的 deferred 历史对象自动归档，不再出现在老板看的主板上
4. 当日前台只展示 `today_delivery_queue`

**触点**

- `09_runbooks/scripts/market_publish_queue_builder.py`
- `09_runbooks/scripts/market_publish_queue_archive.py`
- `09_runbooks/scripts/market_frontstage_board_builder.py`

**验收标准**

- 老板在前台只会看到当日业务日相关队列
- 不再出现 `n/a` 作为正式对象

### P1-4｜前台 bot 存在“提前报喜”

**现象**

- 还没过最终门，就对外同步“19:00 前一定入草稿箱”
- 实际到点后对象仍被打回

**根因**

- 前台同步脚本没有绑定真实最终状态
- 管理层汇报发生在“执行判断”阶段，而不是“最终事实”阶段

**修复思路**

1. 定义前台同步的允许口径：
   - `已发生`
   - `已通过`
   - `已阻塞`
   - `待人工动作`
2. 禁止使用：
   - “预计会交付”
   - “应该没问题”
   - “问题都很小，不影响今晚交付”
3. 只有在 `publish-ready=pass` 后，才允许同步“即将入草稿箱”
4. 日常汇报严格按你已经确认的节奏执行：
   - 早 `09:00`
   - 晚 `22:00`
   - 只报问题

**触点**

- `09_runbooks/scripts/market_frontstage_group_sync.py`
- `09_runbooks/scripts/market_frontstage_board_builder.py`

**验收标准**

- 前台再也不会出现“先说今晚能交，后面又回退”的情况

---

## 3.3 P2 问题：质量、展示、执行纪律问题

### P2-1｜content-pack 常见硬伤没有被系统前置拦截

**常见问题**

- scaffold 残留
- 本地相对路径图片未转可发布格式
- `slot_1/slot_2` 图位计划与正文不一致
- 关键判断缺数字锚点
- GitHub / arXiv / CVE / commit / 原帖锚点缺失
- 图文不符

**根因**

- content-pack 的校验主要靠 reviewer 人眼，而不是规则化 validator
- topic type 不同，但证据要求没有结构化模板

**修复思路**

1. 为 content-pack 建立 `mandatory validator`
2. 按选题类型建不同 schema：
   - `security`
   - `benchmark`
   - `company_event`
   - `hot_topic_reaction`
   - `industry_judgment`
3. 每类 schema 写明必填项
4. 将以下问题前置为脚本校验：
   - scaffold tokens
   - image references
   - inline visual slot count
   - required anchors count
   - unresolved placeholders

**触点**

- `09_runbooks/scripts/market_content_hygiene_guard.py`
- `09_runbooks/scripts/market_content_pack_truth.py`
- `09_runbooks/scripts/market_draft_pack_builder.py`
- `09_runbooks/scripts/market_content_polish_builder.py`

**验收标准**

- scaffold 不再进入草稿箱
- 图位计划与正文至少数量一致
- 高风险题材若缺关键锚点，无法进入 publish-ready

### P2-2｜图片链路与 HTML 渲染链路仍不稳

**现象**

- 图片在 markdown 中存在，但进草稿箱后丢失
- `rendered_html_img_count = 0`
- 图文数量与计划不一致

**根因**

- 内容层、handoff 层、bridge 层三方对图片状态的理解不一致
- 缺少一张“图片已真正进入发布包”的确定性状态卡

**修复思路**

1. 统一图片状态字段：
   - `asset_exists`
   - `asset_selected`
   - `asset_embedded_in_handoff`
   - `asset_uploaded_to_wechat`
   - `asset_rendered_in_html`
2. publish-ready 必须检查 `rendered_html_img_count >= planned_required_images`
3. 对桥接结果增加图片对账日志

**触点**

- `09_runbooks/scripts/market_visual_capture_helper.py`
- `09_runbooks/scripts/market_wechat_bridge_enqueue.py`
- `09_runbooks/scripts/market_wechat_bridge_reconcile.py`
- Windows 侧 `wechat_bridge_consumer.py`

**验收标准**

- 草稿箱里的图片数量与 handoff 计划一致
- 不再出现“本地看着有图，公众号正文里全没了”

### P2-3｜业务日口径和展示口径曾经混乱

**现象**

- intake 和白天线筛题曾经混用自然日与业务日

**根因**

- 板层口径和执行口径没有统一从同一个 business-day helper 读取

**修复思路**

1. 所有板、队列、筛选逻辑统一调用 `market_business_day.py`
2. 在对象元信息里固化 `business_day_window`

**触点**

- `09_runbooks/scripts/market_business_day.py`
- `09_runbooks/scripts/market_frontstage_board_builder.py`
- `09_runbooks/scripts/market_public_intake_board_builder.py`
- `09_runbooks/scripts/market_topic_capture_round.py`

**验收标准**

- 展示、选题、锁题、交付全部使用同一业务日窗口

---

## 4. 修复工程分层设计

## 4.1 工作流 A｜输入层修复

**目标**

- 恢复 `100+ / business day` 的高时效 intake
- 恢复一级源稳定性
- 提高深抓比例

**动作**

1. 源级健康分层
2. 核心源失败兜底切换
3. 重复源治理
4. capture summary 加入“退化原因”
5. 把 source KPI 写进前台和 ops board

## 4.2 工作流 B｜选题与锁题链修复

**目标**

- 每天稳定形成 `Top8 -> Top5 -> approved-topic`
- 不依赖老板手动拍板也能锁题

**动作**

1. Top5 正式对象化
2. recent topic / event age / heat age 三元治理
3. continuity 与 premium 分道
4. auto-lock 逻辑收敛为唯一真相源

## 4.3 工作流 C｜成稿终门修复

**目标**

- content-pack 成为真实终门
- 成稿的常见硬伤在 publish 前就被规则拦住

**动作**

1. content type schema
2. scaffold / image / anchor validator
3. publish-ready 定义统一
4. fallback publish-safe 定义统一

## 4.4 工作流 D｜晨间线修复

**目标**

- 6:30 尽量自动发
- 8:30 前要么成功，要么给出明确终结原因

**动作**

1. final verdict 卡
2. bridge 内容分责
3. retry 窗口显式化
4. 晨间老题与重复题策略升级

## 4.5 工作流 E｜发布层与队列修复

**目标**

- 发布队列只反映真实出站状态
- 历史 backlog 与当日业务隔离

**动作**

1. today queue / backlog / archive 三池拆分
2. `n/a` scrubber
3. human action 队列与 system queue 分离

## 4.6 工作流 F｜前台板与汇报修复

**目标**

- 前台板只说真话
- 老板一眼能看懂今天到底卡在哪

**动作**

1. 统一字段语义
2. premium / fallback / blocked 分层展示
3. 问题导向汇报
4. 管理层口径改为结果导向

---

## 5. 施工顺序

## Phase 1｜止血（最高优先，先把“天天挂零”止住）

1. 白天线最终交付门统一到 `content-pack publish-ready`
2. 前台禁用“提前报喜”口径
3. continuity 改造成明确的 fallback 通道
4. Top5 正式对象化
5. queue 脏状态清洗，主板只看当日业务

**阶段验收**

- 老板不介入时，系统也能形成当天锁题
- 前台不再出现“已承诺交付但实际没过终门”

## Phase 2｜恢复输入与选题自治

1. source health scorecard
2. 核心源软失败兜底
3. business-day 全链统一
4. old topic / duplicate / late-but-hot 规则升级

**阶段验收**

- 连续 3 个业务日达到 `100+ intake`
- `Top5` 每天按时落地

## Phase 3｜修晨间线

1. 晨间 final verdict 卡
2. bridge 与内容故障拆责
3. 8:30 前终结规则
4. 图片对账

**阶段验收**

- 晨间线不再黑箱挂掉
- 失败时能准确知道是 content fail 还是 infra fail

## Phase 4｜修成稿质量与视觉链路

1. content schema
2. scaffold validator
3. image state machine
4. publish-ready truth gate

**阶段验收**

- 草稿箱中不再出现脚手架文本、裂图、错图、空图

## Phase 5｜收口观测与治理

1. 加问题日报板
2. 加 source / gate / deadline KPI
3. 固化 runbook 与验收流程

**阶段验收**

- 系统进入“日常自动跑 + 只在异常时报警”的稳态

---

## 6. 关键时间门与目标口径

### 6.1 晨间线

- `05:00` 前：晨间候选冻结
- `06:30`：目标自动发布
- `06:30 ~ 08:30`：仅允许有限重试
- `08:30`：必须产出 final verdict，不再继续拖

### 6.2 白天线

- `14:30`：输入收盘
- `15:30`：Top5 必须落地
- `16:30`：approved-topic 必须形成
- `17:30`：若无 premium 成稿，启动 fallback lane
- `19:00`：目标 2 篇 premium 成稿入草稿箱
- `19:00` 硬底线：至少 1 篇 fallback publish-safe，不允许挂零
- `21:30`：只允许补投窗，不允许回写成“当天已准时交付”

---

## 7. 验收指标

## 7.1 结果指标

- `连续 5 个业务日无挂零`
- `连续 5 个业务日 Top5 正式落地`
- `连续 3 个业务日 intake >= 100`
- `晨间线 final verdict 覆盖率 100%`
- `发布队列主板无 n/a 脏对象`

## 7.2 过程指标

- `source soft fail` 核心源每日不超过 2 个
- `content-pack < 8 仍被前台承诺交付` 次数 = 0
- `scaffold 泄漏入草稿箱` 次数 = 0
- `图片计划数 > HTML 实际渲染数` 的对象数 = 0
- `approved-topic 无 Top5 来源` 次数 = 0

---

## 8. 需要我优先落地的模块清单

按优先级排序，后续施工先打这些点：

1. `market_frontstage_board_builder.py`
2. `market_frontstage_group_sync.py`
3. `market_platform_task_sheet_to_approved.py`
4. `market_approved_topic_builder.py`
5. `market_publish_queue_builder.py`
6. `market_pipeline_reconcile.py`
7. `market_content_hygiene_guard.py`
8. `market_content_pack_truth.py`
9. `market_morning_flash_preflight.py`
10. `market_morning_flash_publish_guard.py`
11. `market_wechat_bridge_reconcile.py`
12. `market_topic_capture_round.py`
13. `market_daily_source_manifest.py`
14. `market_recent_topic_guard.py`
15. `market_day_mainline_delivery_retry.py`

---

## 9. 施工纪律

### 9.1 不做的事

- 不为了展示层好看而单独美化
- 不增加新的业务线
- 不用更多 agent 叠复杂度掩盖状态机问题
- 不允许继续让历史 backlog 污染当日判断

### 9.2 每完成一层必须验证

每个工作流结束后必须验证：

1. `对象有没有真的落盘`
2. `前台板有没有同步成真实状态`
3. `脚本自动跑时会不会再次退化`
4. `老板不介入时链路能不能自己走完`

---

## 10. Codex 的执行顺序约束

后续真正开始改时，严格按下面顺序，不擅自跳步：

1. `先修前台真相与最终放行门`
2. `再修 Top5 / 锁题链`
3. `再修 fallback 保底机制`
4. `再修输入层与源健康`
5. `再修晨间 bridge + verdict`
6. `再修 content-pack 规则化校验`
7. `最后收口队列、报表、runbook`

只有当前一步验证通过，才进入下一步。
