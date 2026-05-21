# 同行资本市场内容系统｜Watchlist Registry Board

## 1. 这份板子是干什么的

这份板子是 Step 3 的总入口，用来回答三个问题：

1. 我们每天到底看哪些源
2. 这些源分别归在哪个平台 registry 里
3. 哪些源已经进入正式监控，哪些还在观察

### 当前说明

2026-03-25 已完成第一轮业务化 seed 重选。

当前这套 registry 不再只是技术占位样本，而是已经按“发现路径 → 平台 registry → A/B/C 分层”收束过一轮。

相关文档：

- Source Strategy V2：`/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/20260326__source-strategy-v2-funnel-architecture.md`
- seed 重选策略：`/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/20260325__seed-reselection-strategy.md`
- seed 候选池：`/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/20260325__seed-candidate-pool.md`
- OpenAI / X 稳定抓取方案：`/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/20260325__openai-news-and-x-stable-capture-plan.md`
- Reddit / Product Hunt 解决方案评估：`/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/20260325__reddit-and-producthunt-solution-evaluation.md`
- 融资信号线审计：`/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/20260325__financing-signal-lane.md`

其中：

- `A 类`：直接进正式盘
- `B 类`：业务上必须盯，但技术上暂不当默认主盘
- `C 类`：人工补录 / 待核验短名单

注意：

> **这里是信息源管理板，不是选题优先级板。**

信息源是否进入 watchlist，主要看：

- 是否稳定产出 AI 圈信号
- 是否经常带来好选题
- 是否具备可信度或传播度
- 是否方便抓取、方便引用、方便持续跟踪

而不是看：

- 它是不是完全在主战场里
- 它是不是 100% 围绕 agent

---

## 2. 平台 registry 索引

- Source Strategy V2：`/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/20260326__source-strategy-v2-funnel-architecture.md`
- Seed 重选策略：`/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/20260325__seed-reselection-strategy.md`
- Seed 候选池：`/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/20260325__seed-candidate-pool.md`
- X / Twitter：`/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/platform_watchlists/20260324__x-source-registry.md`
- YouTube：`/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/platform_watchlists/20260324__youtube-source-registry.md`
- 微信公众号：`/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/platform_watchlists/20260324__wechat-source-registry.md`
- Web / RSS / 长文站点：`/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/platform_watchlists/20260324__web-rss-source-registry.md`
- 趋势入口 / 榜单 / 聚合面板：`/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/platform_watchlists/20260324__trend-entrance-registry.md`

补充说明：

> 平台 registry 负责“按平台管理 source”，而 Source Strategy V2 负责“按 `L1-L4 四层情报漏斗` 重新组织这些 source 的角色”。

---

## 3. watchlist_source 入池标准

一个 source 进入正式 watchlist，至少满足以下 2 条：

1. 稳定提供 AI 圈相关信息
2. 近一段时间内实际带来过好题、好线索或重要信号

加分项：

1. 热点发现速度快
2. 有一手信息密度
3. 引用价值高
4. 在某个平台有强讨论度
5. 能补足我们当前的信源盲区

减分项：

1. 噪音太大
2. 标题党严重
3. 抓取困难且收益很低
4. 信息真假混杂、引用风险高

---

## 4. 信息源层的管理原则

### 4.1 保持中立

不因为 source 更偏模型、infra、硬件、终端，就天然边缘化。

### 4.2 关注产题能力

一个源最重要的，不是“看起来专业”，而是：

> **能不能持续产出值得进入 topic radar 的题。**

### 4.3 把取舍后移到候选题阶段

高热但不完全贴合主战场的题，依然值得抓回来。

真正的品牌取舍，发生在 Top 8 → Top 5 推荐阶段。

---

## 5. source_type 建议枚举

建议优先使用以下类型：

- `media`
- `newsletter`
- `kol`
- `founder`
- `company`
- `tool_builder`
- `competitor_account`
- `trend_entrance`
- `aggregator`
- `community`

---

## 6. 状态说明

- `active`：正式监控
- `paused`：暂时停看
- `archived`：仅保留历史
- `candidate`：待观察，尚未入正式盘

---

## 7. 每周维护动作

建议每周至少做一次：

1. 新增近一周发现的优质 source
2. 暂停持续低质量 source
3. 记录哪些 source 最近连续带来高质量题
4. 记录哪些 source 看起来很热，但长期转不出好题

---

## 8. 主表字段建议

| 字段 | 含义 |
| --- | --- |
| `source_key` | 稳定键 |
| `source_name` | 源名称 |
| `platform` | 平台 |
| `source_type` | 类型 |
| `region` | 区域 |
| `language` | 语言 |
| `handle_or_url` | 入口 |
| `signal_quality` | 信号质量 |
| `citation_reliability` | 引用可靠性 |
| `capture_method` | 抓取方式 |
| `status` | 状态 |
| `owner` | 维护人 |
| `notes` | 备注 |

---

## 9. 备注

这份总表不承担“今天写什么”的决策。

它只承担：

> **让系统知道应该长期看哪些源，以及这些源分别怎么被管理。**

补充一句：

> **动态发现规则不强行伪装成固定 URL，而是交给动态 scouting skill 去执行，再回填到候选池或 registry。**
