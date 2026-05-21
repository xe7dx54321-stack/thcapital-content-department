# 同行资本市场内容系统｜下一阶段执行计划（Codex 内部施工文档）

- `created_at`: `2026-04-02`
- `owner`: `Codex`
- `usage`: `内部执行清单；用于长任务续接、上下文丢失后的快速恢复，不面向老板直接汇报`
- `status`: `first_batch_completed`

## 0. 本轮唯一执行顺序

严格按老板确认的优先级执行，不擅自重排：

1. `发布结果回流系统`
2. `包装引擎`
3. `研究第二层对象正式化`
4. `留言区 -> 正式需求入口`

明确不做：

- 暂不推进 `内容工厂 <-> VC` 系统联动
- 暂不扩展新的业务线
- 暂不为“展示更好看”单独做无业务价值改造

---

## 1. 执行总原则

### 1.1 结果先于概念

- 优先改正式生产链里的脚本、cron、board、review，而不是只写想法文档。
- 每完成一层，都要验证它是否真的能进入已有链路自动运行。

### 1.2 尽量复用现有对象

- 优先复用：
  - `06_publish_queue/`
  - `07_performance_reviews/`
  - `11_frontstage/`
  - `07_wechat_bridge_outbox/`
  - `18_research_workbenches/`
  - `00_control_tower/`
- 避免额外新建平行目录，除非现有目录无法承载。

### 1.3 先打通骨架，再补丰富度

- 先保证“能自动跑通、状态可信、可追踪”。
- 再补更丰富的指标、包装样式和业务入口。

---

## 2. Priority 1｜发布结果回流系统

## 2.1 目标

把公众号每篇文章发布后的真实结果正式接回系统，至少形成：

- `24h / 72h review`
- 可追踪的 performance board
- 对选题、标题、包装、发布时间的学习反馈

第一阶段必须覆盖：

- `阅读`
- `分享`
- `在看`
- `点赞`
- `评论数`
- `收藏`
- `完读率 / 阅读时长`
- `账号层涨粉（日级）`
- `人工补充的私聊 / 项目线索 / 特殊反馈`

## 2.2 已知现状

- 已有 `market_wechat_result_backfill.py`
- 已有 `market_content_review_builder.py`
- 已有 `market-performance-board`
- 已有 `market_human_publish_record.py`
- 当前主要断点：
  - 手动发布的队列项如果缺 `actual_publish_at / publish_url`，结果回流会被挡住
  - 还没有自动 cron 定时跑 `wechat_result_backfill`
  - 涨粉、私聊、项目线索还没有正式字段和回填入口
  - review 更像 skeleton，缺实际结果学习输入

## 2.3 必做任务

- [x] 修复 `manual publish` 场景下的回流门槛
- [x] 让 `actual_publish_at` 可由人工确认记录或保守推断补齐
- [x] 增加 `followers` 日级数据回流
- [x] 增加 `manual feedback / lead signal` 回填入口
- [x] 把 manual feedback 合并进 review 与 performance board
- [x] 新增 / 调整 cron，让 `wechat_result_backfill` 成为正式生产任务
- [x] 写 runbook，明确“手动发布后怎么让系统知道”

## 2.4 验证标准

- 任何一篇 `published` 的公众号稿件，只要有人确认发布时间，就必须在系统里进入 `24h / 72h` 追踪。
- 即使拿不到永久链接，也不能让整条 review 链挂掉。
- 第二天 `08:00 CST` 后，系统能自动尝试拉取官方结果。
- 结果板能明确区分：
  - `waiting_publish`
  - `waiting_t_plus_one`
  - `ready`
  - `manual_feedback_pending`
  - `official_api_blocked`

---

## 3. Priority 2｜包装引擎

## 3.1 目标

把“品牌条、导语钩子、封面/头图、小标题样式、文末 CTA、公众号入口”从零散人工发挥，升级为可复用的正式包装层。

## 3.2 已知现状

- Windows 侧 `wechat_bridge_consumer.py` 已有：
  - 品牌卡片
  - 关注卡片
  - 一级 / 二级标题样式
- 当前缺口：
  - 默认品牌信息仍偏基础
  - 包装结构没有被显式做成“引擎规则”
  - `title 3版 / lead 2版 / CTA 模块 / section 样式策略` 还没进入统一资产
  - 渲染层和内容层的规范还没完全对齐

## 3.3 必做任务

- [x] 把包装标准落成正式 runbook / rulebook
- [x] 固化公众号头部品牌条默认文案
- [x] 固化文末 CTA 模块的几种模式
- [x] 给 `draft-pack` 增加包装资产位：
  - `title options`
  - `opening hook options`
  - `cta mode`
  - `section style hint`
- [x] 升级 `wechat_bridge_consumer.py` 的默认渲染样式
- [x] 校对 `wechat-html-handoff` 与渲染器规则的一致性

## 3.4 验证标准

- 即使内容写稿 agent 没主动写品牌条，最终公众号成稿也会自动带正确品牌头部。
- 小标题视觉效果明显比旧版更强，但不花哨、不廉价。
- 文末 CTA 不再靠临时发挥，而是按场景调用。

---

## 4. Priority 3｜研究第二层对象正式化

## 4.1 目标

继续按既有路线推进，不重起炉灶，把 VC 研究从“能产出研究”升级为“能持续维护判断”。

## 4.2 这轮只做四类对象

- `thesis evidence append`
- `sector watch note`
- `weekly sector brief`
- `research backlog`

## 4.3 必做任务

- [x] 核对运行台中是否已有半成品对象 / 历史模板
- [x] 统一这四类对象的目录与命名纪律
- [x] 明确每类对象的 owner、输入、产出、晋级条件
- [x] 把它们接进 `00_control_tower` 与 `18_research_workbenches`
- [x] 至少补一版总 runbook，保证后续不会失忆后重造

## 4.4 验证标准

- `analyzer-li / analyzer-wang / lead` 都有明确使用边界
- workbench 不会只停留在 `collecting / active`，而是有正式第二层承接物
- 这些对象能在控制塔中被看到，而不是只散落在 workbench

---

## 5. Priority 4｜留言区 -> 正式需求入口

## 5.1 目标

先把基础骨架搭好，不急着上线重流量业务。

## 5.2 现阶段范围

第一阶段只做：

- 留言需求分类模型
- 正式对象模板
- 人工 / 半自动回填入口
- 后续接微信接口或网页抓取时所需的数据契约

明确暂不追求：

- 立即高频自动消费真实留言
- 复杂的自动回复或自动派单

## 5.3 必做任务

- [x] 设计留言需求四分类对象
- [x] 设计留言入队模板
- [x] 设计留言 -> 内容 / 研究 / 项目 / 商务 的路由规则
- [x] 预留 cron / bot 接口位，但先不强接真实流量

---

## 6. 执行顺序（本轮）

### Step A

先完成 Priority 1 的骨架修复与生产接线：

- `wechat_result_backfill`
- `manual publish record`
- `manual feedback record`
- `cron`
- `runbook`

### Step B

再推进 Priority 2 的包装引擎：

- `包装规则文档`
- `wechat 渲染器升级`
- `draft pack 包装位`

### Step C

再推进 Priority 3 的研究第二层对象：

- 先文档与模板
- 再控制塔接线

### Step D

最后搭好 Priority 4 的留言入口骨架：

- 只搭对象与路由，不强接真实流量

---

## 7. 续接说明

如果长任务中断，恢复时优先按这个顺序检查：

1. 当前做到哪个 Priority
2. `cron` 是否已接上
3. 对应 `runbook / script / board` 是否已经有正式产物
4. 是否已经做过真实 dry-run / py_compile / 本地验证

若只剩少量收尾，不要重新大改架构，优先把现有链条闭合。

---

## 8. 本轮收口结果

- Priority 1：已完成
  - 手动发布确认、bridge 侧官方结果、24h / 72h review、performance board 已接通。
- Priority 2：已完成
  - 品牌头部、开篇钩子、CTA、标题 / 小标题包装位已进入正式包装层。
- Priority 3：已完成
  - 新增 `research_second_layer_board.md`、builder、总 runbook，并已接进 `lead_control_tower_refresh.py`。
- Priority 4：已完成第一阶段骨架
  - 已新增 `12_public_intake_requests/`、正式模板、录入脚本、看板 builder 与 runbook。
  - 当前仍保持 `manual_first_phase`，不直接对接高频真实留言自动抓取。
