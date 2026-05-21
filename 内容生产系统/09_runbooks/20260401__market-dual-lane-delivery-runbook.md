# 同行资本市场内容系统｜双车道交付 Runbook

## 1. 目标

从 `2026-04-01` 起，内容工厂按两条正式交付车道运行：

- `晨间快反车道`
  - 目标：`06:50 CST` 前自动发布 1 篇聚合型微信公众号晨报
  - 方向：从 `8-10` 个热点事件中整理成“热点新闻早知道”式早报，优先抢第一屏信息位与解释权
  - 平台：只做 `wechat`
  - 发布模式：`auto_api`

- `日间主线车道`
  - 目标：`19:00 CST` 前把 2 篇成品稿放入公众号草稿箱，并同步生成对应飞书云文档
  - 方向：综合上一业务日全量信息，优先产业判断 / 一人公司实验 / 深度热点拆解
  - 平台：默认 `wechat`，其余平台按既有任务单与平台束扩展
  - 发布模式：`draft_only`

两条车道共用同一套资产体系：

- `approved-topic`
- `draft-pack`
- `publish-queue`
- `24h / 72h review`

区别不靠目录分叉，而靠元数据：

- `delivery_lane`
- `publish_mode`
- `delivery_deadline`
- `selection_scope`

---

## 2. 业务日口径

### 日间主线车道

- 业务日信息窗：`T-1 17:00 -> T 14:30`
- 该窗口内的全量 intake 用于：
  - `Top20`
  - `平台任务单`
  - `approved-topic`
  - `content heartbeat`
- 明确排除：
  - 已进入 `morning_flash` 车道并已交付的题

### 晨间快反车道

- 快反信息窗：`T-1 17:00 -> T 05:00`
- 目标不是“事实 100% 封闭”，而是：
  - 热度足够高
  - 时效足够强
  - 叙事足够清楚
  - 风险措辞可控

补充一条更准确的业务判断：

- **不是所有“事件发生超过 24h”的题都自动淘汰**
- 但若事件本身已超过第一波爆发窗口，想继续进入 `morning_flash`，必须至少满足以下其一：
  - 今天出现了新的官方进展 / 新硬信息 / 新争议点
  - 事件热度在今天仍明显加速，进入更大传播圈层，属于“第二波起飞”
  - 我们这次要回答的是一个**之前没交付过的新问题**，而不是把同一个角度再写一遍
- 若只是“昨天的热点今天还没完全凉”，但没有新进展、没有新角度、没有新的读者收益，就不该继续占晨间自动发布坑位

---

## 3. 晨间快反车道

### 3.1 立题

晨间快反不强制经过完整 `Top20 -> 平台任务单` 全链。

从 `2026-04-10` 起，`morning_flash` 的业务语义更新为：

- 内部 lane 名仍保持 `morning_flash`
- 但实际交付对象不再是“只选 1 个热点写成单篇”
- 而是每天固定产出 1 篇晨间聚合早报，汇总 `8-10` 个热点事件
- 标题与封面必须长期稳定，正文图可以没有，但结构必须强

正式起稿前，先生成当天晨间早报规格：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_morning_flash_roundup_spec.py \
  --date <RUN_DATE> \
  --write
```

规格文件会固定当天的：

- `topic_key`
- `title`
- `approved_angle`
- `planned_publish_at=06:50 CST`
- 标题 / 封面一致性规则
- 文章结构要求

推荐系列名默认使用：

- `AI早报｜4月10日`
- `AI早报｜4月11日`

封面也必须跟随同一模板，只允许更新日期角标，不能今天一个系列名、明天一个系列名。

允许直接用显式立题器生成正式 `approved-topic`：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_lane_approved_topic_builder.py \
  --topic-key <topic_key> \
  --title "<title>" \
  --approved-angle "<approved_angle>" \
  --platform wechat \
  --delivery-lane morning_flash \
  --publish-mode auto_api \
  --write
```

输出仍然是标准 `approved-topic` 卡，只是车道字段不同。

但从 `2026-04-02` 起，晨间立题前必须先过一层最近同题排重：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_recent_topic_guard.py \
  --topic-key <topic_key> \
  --title "<title>" \
  --approved-angle "<approved_angle>" \
  --delivery-lane morning_flash \
  --write
```

若报告中 `recent_duplicate_status=fail`，或命中近 `120h` 内已发 / 待发高相似同题，则不得锁题，必须换下一个候选。

补充规则：

- 日更型晨间聚合早报属于**固定系列栏目**
- 同一系列在不同日期重复出现是合法的，不应被 recent-topic guard 误杀
- 但**同一天**的重复立题 / 重复入队仍然必须拦截

这里的含义不是“同一事件永远不能再写”，而是：

- **同一事件的同一问题、同一收益承诺、同一叙事层**，短期内不能重复消费
- 如果确实是第二波爆发，且回答的是一个新问题，可以保留，但必须在 `approved_angle` 里把“这次新增了什么”写清楚

### 3.2 写稿与桥接

1. 用标准 `market_draft_pack_builder.py` 生成 / 更新 `draft-pack`
2. 写成可直接发布的 `wechat.md`
3. 补齐：
   - `publish-readiness.md`
   - `wechat-html-handoff.md`
   - `inline-visual-plan.md`
4. 进入 `publish_queue`
5. 由 Windows 桥接自动送入公众号草稿箱

晨间聚合早报的正文结构固定为：

1. 开头引子
   - 一句交代今天这篇是什么
   - 自然带出同行资本的简介 / 观察视角
2. `太长不看`
   - `8-10` 个事件
   - 每个事件是“子标题（20字内）+ 50字内概要”
   - 这里必须自然埋一个钩子，鼓励读者继续往下看
3. `详细阐述版`
   - 与 `太长不看` 使用完全一致的子标题顺序
   - 每条 `300-400` 字
   - 讲清事实 + 影响 + 我们怎么看
4. 文末收束
   - 回扣前文钩子
   - 给出今日最值得继续盯的一条主线

额外要求：

- 写作风格不由系统写死；业务岗必须先读最新风格路由表，再自行决定调用哪套公众号 style skill
- 正文默认不写“量子位报道 / 36氪跟进 / 智东西发文”这类二手媒体名表述；若要交代信源，优先回到官方或原始链接，并把来源留在 citation / source packet 层
- 正文图不是硬要求；若没有真正提升信息密度的图，可以不放
- 若要放图，优先放信息压缩图、时间线、关系图，而不是装饰图

### 3.3 自动发布三闸门

晨间稿只有在以下三道闸门都通过时，才允许自动调用 `freepublish/submit`：

1. `technical_preflight`
2. `reviewer checklist`
3. `leader checklist`

其中 `technical_preflight` 不只检查桥接与媒体素材，还必须拦住两类硬问题：

- `recent_topic_duplicate_guard=fail`
- `public_copy_no_internal_scaffolding=fail`

也就是说，晨间稿如果已经和最近 120 小时内的已发 / 待发对象高度重合，或者正文里混入“已确认 / 仍需验证”这类内部核验脚手架，就算桥接成功也不能自动发布。

另外，如果晨间 guard 命中了上述**结构性硬阻断**，系统应自动把该 queue item 从 `waiting_human_publish` 降为 `deferred`，避免展示台和发布队列继续把它误当成“待发成品”。

#### 技术预检脚本

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_morning_flash_preflight.py \
  --queue-item <queue_item_path> \
  --write
```

会在对应 `draft-pack` 目录下生成：

- `morning-flash-preflight.md`
- `morning-flash-reviewer-checklist.md`
- `morning-flash-leader-checklist.md`

#### 自动发布闸门

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_morning_flash_publish_guard.py \
  --date <RUN_DATE> \
  --write
```

该脚本只放行满足以下条件的 queue item：

- `delivery_lane=morning_flash`
- `publish_mode=auto_api`
- `status=waiting_human_publish`
- `technical_preflight_status=pass`
- `reviewer checklist=pass`
- `leader checklist=pass`

通过后才允许调用：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_wechat_publish_submit.py \
  --queue-item <queue_item_path> \
  --write
```

### 3.4 晨间补签 / 补发重试窗

`06:50` 不是晨间线的唯一一次机会。

从 `2026-04-02` 起，晨间线正式增加一个自动重试窗：

- 红队签核：持续重跑到 `08:45`
- 领导签核：持续重跑到 `08:55`
- 自动发布闸门：持续重跑到 `08:30`

这层重试主要覆盖两类真实生产故障：

- `Windows` 副机短时离线 / 休眠 / `Syncthing` 短暂断开，导致 `result.json` 晚到
- 桥接稍晚成功，`media_id` 补回时已经错过 `06:50` 前后的首次闸门

重试窗的纪律如下：

- **不重新立题**
- **不新增第二篇晨间稿**
- 只允许继续处理当天同一个 `morning_flash + auto_api + wechat` 对象
- 一旦桥接结果补回、`technical_preflight` 转为 `pass`，红队 / 领导 / publish guard 必须自动继续推进
- 若到重试窗结束仍未满足三闸门，则不再自动正式发布，但已入草稿箱的对象继续保留给人工兜底

---

## 4. 日间主线车道

### 4.1 选题

仍沿用原有主线：

- `Top20`
- `平台任务单`
- `platform lock bridge`
- `approved-topic`

但统一改成：

- 输入窗口：`T-1 17:00 -> T 14:30`
- 排除 `morning_flash`
- 交付目标：`19:00` 前 2 篇公众号成品入草稿箱

### 4.2 写稿

日间主线继续走：

- `approved-topic -> draft-pack`
- `content polish`
- `redteam`
- `market-editor scorecard`
- `publish_queue`

`market_content_heartbeat_queue.py` 现在只会消费：

- `delivery_lane=day_mainline`

不会再把晨间快反题拉回主线二次加工。

### 4.3 发布

日间主线默认不自动正式发布。

只要求把同一份成品同时推入公众号草稿箱和飞书云文档，创始人手工选择并发布。

若 Windows 草稿箱桥接暂时不可用，飞书云文档作为手动复制发布的兜底出口。

### 4.3.1 交付完成汇报

`19:00` 后，一旦系统确认当日 `day_mainline` 对象已经：

- 成功进入微信草稿箱
- 飞书云文档已同步完成

前台 bot 必须主动汇报一条交付完成消息，并附上飞书云文档链接。

### 4.4 草稿箱晚间补投窗

`19:00` 是日间主线的主 deadline，但不是草稿箱桥接的最后一次机会。

从 `2026-04-02` 起，日间主线增加一层晚间补投窗，硬截止到 `21:30`：

- 只服务 `day_mainline + wechat`
- 只处理已经进入 `waiting_human_publish` 的当天 queue item
- 只补“草稿箱还没真正落进去”的对象
- 不新增 backlog，不回补历史 pack，不临时换题

补投窗的正式动作：

1. 先跑 `market_wechat_bridge_reconcile.py --write`
2. 再跑 `market_pipeline_reconcile.py --date <RUN_DATE> --write`
3. 若同日 `wechat` queue item 仍未拿到草稿 `media_id / publish_url`，运行：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_day_mainline_delivery_retry.py \
  --date <RUN_DATE> \
  --limit 5 \
  --write
```

这一步会只对同日 `day_mainline + wechat + waiting_human_publish` 且仍未桥接成功的对象，重建一次 bridge request，继续尝试把稿件送入公众号草稿箱。

到 `21:30` 仍未成功入草稿箱，就停止当天补投，不再拖到更晚；后续只保留状态回填与人工兜底。

---

## 5. 手工发布回填

日间主线如果由创始人手工发布，需要把结果正式写回系统。

脚本：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_human_publish_record.py \
  --queue-item <queue_item_path> \
  --publish-url <optional_url> \
  --confirmed-by founder \
  --write
```

效果：

- queue item 状态改为 `published`
- 记录人工发布时间
- 若暂无 URL，则显式写 `human_publish_url_backfill=required`
- 自动刷新 publish queue board
- 同步更新 `approved-topic` / `draft-pack-card`

建议后续把这条命令接进 Feishu bot，让“我发了这篇”变成一条正式业务事件。

---

## 6. 结果回流

正式结果回流只认两种主链：

- `晨间快反`：`freepublish/submit` 自动发布
- `日间主线`：`market_human_publish_record.py` 显式确认手工发布

后续统一进入：

- `24h review`
- `72h review`
- 学习池沉淀

不再依赖“老板发完后系统猜测是否已发布”。

---

## 7. 纪律

- 晨间自动发稿，必须三闸门齐全，禁止裸发
- 日间主线判断，必须使用完整业务日窗口，禁止只看自然日半截 intake
- `morning_flash` 与 `day_mainline` 不能混题、不能重复入队
- 手工发布不等于口头说明，必须回填 queue item
- 所有展示台与 dashboard 默认按业务日口径展示，不按自然日裁切
