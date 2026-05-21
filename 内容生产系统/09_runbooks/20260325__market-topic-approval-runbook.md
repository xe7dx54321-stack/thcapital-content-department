# 同行资本市场内容系统｜2026-03-25｜Topic Approval 与 Approved Topic 流转

## 1. 这份 runbook 的作用

这份 runbook 用来承接创始人对 `Top 8 -> Top 5` 建议单的明确拍板动作。

### 2026-04-09 更新：day_mainline 改为 founder-pick 合约

- `day_mainline` 不再允许平台任务单自动锁题。
- 每个业务日 `17:40 CST` 先由前台 bot 汇报 2 个推荐题，并可附 1 个候补题。
- 每个题必须单独成卡，卡内至少包含：
  - 中文一句话题目
  - 150 字以内内容展开
  - 本轮使用的公众号风格 skill
  - 封面 + 正文图的大纲
- 创始人在飞书里回复“选第几个”后，系统才允许创建 `approved_topic`。
- 若 `18:00 CST` 前没有收到明确回复，系统默认选择 `推荐 1`。
- 选题一旦确认，后续目标是 `19:00 CST` 前把同一份成品稿同时落到微信草稿箱和飞书云文档。
- `19:00 CST` 后，前台 bot 必须补一条交付完成汇报，并带上飞书云文档链接，作为 Windows 草稿箱链路之外的兜底出口。

它解决的是：

> 老板回复了“选第几个、改成什么角度、做哪些平台”，系统如何立刻把这个决定固化成一个正式的 `approved_topic`。

## 2. 当前 owner

- 对外唯一前台 bot：`market-editor`

当前阶段：

- `market-editor` 负责接收创始人的确认
- `market-editor` 负责把确认动作固化成 `approved_topic`
- `Draft Pack` 仍属于下一阶段，但 `approved_topic` 必须把写作范围交代完整

## 3. 合法输入

只有在出现明确确认动作时，才允许创建 `approved_topic`：

- `选第 2 个`
- `选第 7 个，捞回来`
- `第 3 个改成机构视角`
- `第 1 个只做微信和知乎`
- `选第 5 个，做公众号 + B站专栏 + 百家号`
- `选第 2 个，微信不做，先上头条和小红书`
- `选第 4 个，重点强调商业闭环`

以下都不算合法确认：

- `这个不错`
- `先看看`
- `再想想`
- `你再优化一下`

## 4. 输入来源

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/YYYYMMDD__daily-top8-to-top5.md`
- 创始人的明确确认语句

## 5. 执行步骤

1. 先确定引用的是哪一张 board
   - 优先用创始人显式指定的 board
   - 否则默认用最新一张 daily board

2. 解析确认动作
   - 选中了第几个
   - 是否是 holdout restore
   - 是否改了角度
   - 是否限定了平台
   - 是否追加了特殊说明
   - 若未限定平台，则走自动平台束推荐

3. 读取：
   - `th-topic-approval`
   - `09_runbooks/templates/market_approved_topic_template.md`
   - 对应 board 中被选中的条目与 detail block

4. 运行 builder：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_approved_topic_builder.py \
  --board-path <board_path> \
  --rank <rank> \
  --approved-angle "<angle>" \
  --special-instructions "<instructions>" \
  --selection-instruction "<original founder instruction>" \
  --approved-by 老板 \
  --write
```

说明：

- 如果创始人显式指定了平台，可继续传 `--platform`
- 如果创始人没有指定，builder 会自动生成：
  - `platform_selection_mode`
  - `platform_bundle`
  - `platform_selection_reason`
  并据此填充 `requested_platforms`

5. builder 输出后，必须确认两件事：
   - `approved_topic` 已落到 `04_approved_topics/`
   - execution log 已落到 `10_logs/`

## 6. 标准产出

### 6.1 approved topic 卡片

输出到：

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/04_approved_topics/YYYYMMDD_HHMMSS__topic_key__approved-topic.md`

### 6.2 execution log

输出到：

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/YYYYMMDD_HHMMSS__topic_key__topic-approval-execution.md`

## 7. 对外回报方式

`market-editor` 对创始人的回报要尽量短，只说：

- 已锁定哪一个题
- 已归一后的角度是什么
- 为什么选它、为什么不是另外几个
- 会先做哪些平台
- `approved_topic` 文件路径
- 下一步会进入 `Draft Pack`

## 8. 关键边界

- 没有明确人工确认，不准创建 `approved_topic`
- 不能因为老板说“还行”就默认推进
- 不能直接从 `approved` 越级进入 `publish_queue`
- 不得丢失原始链接和 source packet path
