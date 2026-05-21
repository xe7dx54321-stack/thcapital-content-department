# 同行资本市场内容系统｜2026-03-25｜Topic Radar 与 Top 8 → Top 5 建议单

## 1. 这份 runbook 的作用

这份 runbook 用来把内容工厂从“会抓素材”推进到“会给创始人做选题建议”。

它解决的是：

> source packet / asset chain / topic cluster 已经有了，今天到底该推荐写什么？

## 2. 当前 owner

- 对外唯一前台 bot：`market-editor`
- 内部素材侦察：`market-scout`

其中：

- `market-scout` 负责抓取、派生、补链
- `market-editor` 负责把素材收束成创始人可拍板的建议单

## 3. 输入

本轮输入只来自内容工厂目录：

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/topic_clusters/`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/YYYYMMDD__market-topic-radar-brief.md`

禁止：

- 回写虚拟 VC 运行台
- 复用研究线对象
- 拿 research queue 充当内容候选题

## 4. 执行步骤

1. 先运行：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_topic_radar_brief_builder.py \
  --date $(date +%F) \
  --write
```

2. 再准备执行日志落盘路径：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_topic_radar_execution_log_builder.py \
  --date $(date +%F) \
  --write
```

3. 读取：
   - `th-topic-radar`
   - `th-market-brand-context`
   - 最新 radar brief
   - `01_watchlists/20260326__source-strategy-v2-funnel-architecture.md`
   - `09_runbooks/templates/market_topic_radar_founder_brief_template.md`
   - `03_topic_candidates/20260324__top8-to-top5-topic-board-template.md`

4. 先做 `Pass 0`：
   - 先把零散线索收束成 `event cluster`
   - 不允许直接拿单条 source packet 排 Top 5

5. 再做 `Pass 1`：
   - 只按市场需求、发酵度、持续性、可写性、用户关心度排
   - 同时检查四层漏斗：`L1 原始信源 → L2 扩散 → L3 中文传播 → L4 热度验证`
   - 并把 `heat signal` 和 `evidence signal` 分开写，不能混成一个感觉分

6. 再做 `Pass 2`：
   - 再按主战场 / 邻接价值 / 品牌身份 / 差异化空间重排
   - 同时补一层“竞品 / 话题竞品 / 产品竞品”视角，回答为什么该我们写
   - 不能因为题材偏相邻战场，就机械压制已经高热、好写、易破圈的话题

7. 先产出板子：

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/YYYYMMDD__daily-top8-to-top5.md`

8. 板子写完后，立即再运行一次执行日志 builder，把最终结果写入：

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/YYYYMMDD__market-topic-radar-execution.md`

## 5. 输出纪律

### 5.1 Top 5

每个推荐项必须写：

- 建议标题
- 一句话判断
- 事件簇键
- 四层漏斗覆盖
- 为什么值得做
- 市场潜力
- Heat signal
- Evidence signal
- 品牌贴合度判断
- 竞品态势 / 为什么该我们写
- 哪些平台在发酵
- 原始链接 / source packet path
- 建议切入角度
- 适合哪些平台 / 形式
- 风险提示

### 5.2 Holdout 3

未进入 Top 5 的 3 个不能消失，必须保留：

- 为什么进 Top 8
- 为什么没进 Top 5
- 事件簇还缺哪一层
- Heat signal
- Evidence signal
- 原始链接 / source packet path
- 是否允许创始人捞回
- 如果捞回，最适合改成什么角度

### 5.3 供给不足

如果今天强候选不足 8 个：

- 不允许凑数
- 必须明确写“今日供给不足”
- 必须点明缺的是哪一类素材

## 6. 对外回报方式

`market-editor` 对创始人的回报要尽量短，只说：

- 今天 Top 5 是什么
- 哪几个被压下去了
- 重点推荐哪 1-2 个先拍板
- 板子文件路径在哪里
- 执行日志文件路径在哪里

详细内容留在建议单里。

前台汇报格式，优先遵守：

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/templates/market_topic_radar_founder_brief_template.md`

---

## 7. V2 补充纪律

- 公众号主阵地的目标不是“最早”，而是“快半拍 + 深一层”
- 微信全文 deep article 不只是信息源，也是内容结构与叙事复盘池
- `L4` 热榜不能替代 `L1` 原始口径；破圈热度高，不代表事实链完整
