# 同行资本市场内容系统｜2026-03-25｜前台同步与展示层 runbook

## 1. 这份 runbook 的作用

这份 runbook 用来约束 `market-editor` 如何把内容工厂的真实运行状态，对前台群做**少量但关键**的同步。

它解决的是：

> 内容工厂已经在跑，但老板在飞书群里看不清今天到底做了什么、推进到了哪里、卡点是什么。

---

## 2. 当前 owner

- 对外唯一前台 bot：`market-editor`

当前阶段：

- `market-editor` 负责维护每日状态板
- `market-editor` 负责在前台群同步关键节点
- `market-editor` 负责把底层多对象状态压缩成老板可快速理解的摘要
- 角色边界与后台升级条件统一看：`/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260326_内容工厂多Agent责任矩阵.md`

---

## 3. 输入

只允许读取内容工厂自己的对象与日志：

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/04_approved_topics/`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/07_performance_reviews/`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/`

输出目录：

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/11_frontstage/`

禁止：

- 回写虚拟 VC 运行台
- 借研究线日志充当内容工厂展示层

---

## 4. 触发时机

只有下面几类情况，才值得前台同步：

1. 今日第一次形成 `Top 8 -> Top 5` 板子
2. 今日第一次形成 `approved_topic`
3. 某个 `Draft Pack` 状态进入 `ready / waiting_human_publish`
4. 出现明确 blocker
5. 出现明确待人工动作
6. 晚盘收口

如果只是底层补了一条链接、抓到一条 packet、修了一个小字段：

- 只更新状态板
- 不需要刷群

---

## 5. 执行步骤

### Step A：先刷新每日状态板

运行：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_frontstage_board_builder.py \
  --date $(date +%F) \
  --write
```

产出：

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/11_frontstage/YYYYMMDD__market-frontstage-board.md`

### Step B：读取状态板

重点看这几个 section：

- `组织边界`
- `关键决策与原因`
- `当前正式任务`
- `当前实际在做`
- `今日阶段性成果`
- `轻审批与提醒`
- `自动化边界`
- `下一阶段计划`
- `人类协助`
- `群同步草稿`

### Step C：判断是否需要发群

需要发群的情形：

- 有新的关键节点已经形成
- 有新的 blocker
- 有新的待人工动作
- 到晚盘收口

不需要发群的情形：

- 只是底层采集数量变化
- 只是状态板数字有小波动
- 没有新的业务推进节点

### Step D：发群时的格式

优先遵守：

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/templates/market_frontstage_group_sync_template.md`

要点：

- 只发压缩版
- 保留状态板路径
- 不把内部侦察细节倒给老板

### Step E：自动化驱动

为了让 `market-editor` 不用每次手动判断是否刷群，关键节点群同步统一通过下面这个 driver 触发：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_frontstage_group_sync.py \
  --date $(date +%F) \
  --write
```

说明：

- 这个脚本会先刷新 `11_frontstage/` 状态板
- 然后只对 `Top 5 / approved_topic / Draft Pack 关键推进 / waiting_human_publish / review pending / 供给不足` 这些真正关键节点做去重判断
- 没有新增关键节点时，只刷新状态板，不刷群
- 晚盘收口时，用 `--close-out` 追加一次当日总结
- 去重状态默认写在：`/Users/apple/Documents/同行资本内容部门/内容生产系统/11_frontstage/_sync_state/market_frontstage_sync_state.json`

---

## 6. 输出纪律

### 6.1 群同步必须回答 6 个问题

1. 当前有什么正式任务？
2. 当前实际在做什么？
3. 当前阶段性成果是什么？
4. 下一步要做什么？
5. 是否需要人类协助？
6. 为什么推这个题、为什么暂时放下另外几个？

### 6.2 群同步必须短

前台群只看：

- 业务推进
- 阶段结果
- 待人工动作
- 风险或 blocker

### 6.3 详细信息统一回到状态板

群里同步要同时给出：

- 状态板路径

必要时再给：

- 对应对象路径

---

## 7. 晚盘收口要求

如果当天已经有真实动作，晚盘至少要同步一次：

- 今日内容工厂做了什么
- 当前卡在哪
- 明天一上来先做什么

如果当天没有新增关键动作：

- 不强行发空转简报
- 但状态板仍应保持最新

---

## 8. 关键边界

- 不用群消息替代正式对象
- 不要把群里同步写成流水账
- 不要把 `market-scout` 直接暴露给老板
- 不要把研究线、IC 线、项目线任务混进内容工厂前台展示
- 不要让浏览器自动化在前台叙事里冒充“主流程能力”；它只能作为兜底手段被提及
