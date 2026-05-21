# Top20 Stage-Gate Scorecard | 2026-05-20 | day_mainline

> 裁判时间：2026-05-20 17:09 Asia/Shanghai
> 裁判角色：market-editor
> 前置包：20260520__top20-screening-pack.md（final，5584 bytes，生成于 2026-05-20 16:xx CST）
> 前置红队：20260520__top20__redteam-review.md（final，生成于 2026-05-20 17:04 CST）
> 重评分原因：旧 scorecard（16:05）生成早于 redteam 定稿（17:04），结论无效，以本文为准

---

## 评分结论

| 字段 | 值 |
|---|---|
| `score` | 5 |
| `status` | rework |
| `rework_mode` | truthful rework but still recoverable |
| `continuity_decision` | continuity_only |
| `continuity_output` | top20_mini_slate |

---

## 评分依据（基于 redteam 17:04 定稿）

### 🔴 三项硬伤，无法忽视

1. **重复条目**（#16 vs #17）：Karpathy 加入 Anthropic 同一事件占两个坑位，直接浪费配额。
2. **评分失准**：Anthropic 收购 Stainless（>$300M，MCP SDK 生态级并购）仅得 10 分，与 ByteDance 3B 同档，严重低估。
3. **标题错误**（#1）：`[ACM CAIS '26 preprint]` 实为 Demo，误导下游 topic-planner 写错误来源标注。

### 🟡 结构性系统问题

- 全部 20 条信源为 Reddit discussion，零官方 RSS 锚点；signal-scout 官方信源覆盖层系统性缺失。
- 无 platform_hint 字段；所有条目未标注目标平台，平台适配成本全部转移至下游。

### 🟢 可 truthful 推进的锚点（redteam 确认）

红队明确识别出三个经补证后可继续的高价值候选：
- **Forge guardrails**（ACM CAIS 2026 Demo，方向可证）
- **Anthropic 收购 Stainless**（战略级并购，>$300M，生态控制意图清晰）
- **Karpathy 加入 Anthropic**（合并后单条，战略信号强）

---

## top20_mini_slate

> 可进入 continuity lane 的候选（满足 truthful 推进标准）

| 优先级 | 候选 | 当前问题 | 修正条件 | 进入方式 |
|--------|------|----------|----------|----------|
| P0 | **Forge guardrails (#1)** | 标题错标为"preprint"，实为 Demo；无原始链接 | signal-scout 补官方 ACM CAIS Demo 链接；标题改为 `[ACM CAIS 2026 Demo]`；确认 Ministral 8B 锚点 | 补证后 topic-planner 直接产出平台任务单 |
| P0 | **Anthropic 收购 Stainless (#9)** | score=10，严重失准；无金额无 SDK 列表 | signal-scout 补充收购金额（≥$300M）和 Stainless 生成的官方 MCP SDK 列表；重评分至 18+ | 补证后 topic-planner 直接产出平台任务单 |
| P0 | **Karpathy 加入 Anthropic（合并 #16+#17）** | 重复收录占两坑位 | signal-scout 去重合并为一条；补充 Karpathy 汇报对象（Nick Joseph）和战略意图 | 合并后 topic-planner 直接进入 |
| P1 | **ByteDance Lance (#2)** | 描述"3B"严重失准（实为 12-14B 总参，3B 活跃） | signal-scout 修正为「12-14B 总参，3B 活跃参数，40GB VRAM，Apache 2.0」 | 补正后 topic-planner 进入 |
| P1 | **MCP self-hosted sandboxes (#7)** | Reddit 帖子，无官方公告 | signal-scout 补 vendor 官方公告链接 | 补平台映射后 topic-planner 进入 |

### 必须排除的条目（不得进入 continuity lane）

- #18（Claude 关心用户健康）：情绪帖，无信号
- #20（Claude limit 达成帖）：情绪帖，无信号
- #13（48GB VRAM 用户调查）：社区讨论，无新闻价值
- ChatGPT 自嘲帖（#12）、RV 业务帖（#19）：无实质投资信号

---

## 返工责任分配

> 红队骂的不只是 market-scout；责任必须拆清

| 执行方 | 具体任务 |
|--------|----------|
| **signal-scout / market-scout** | ①补全所有条目的官方原始链接（非 Reddit）；②修复 ByteDance Lance 描述；③去重 #16/#17；④补充 Stainless 收购金额与 SDK 列表；⑤补 Forge 官方 ACM CAIS Demo 链接；⑥建立官方 RSS 与 Reddit trending 交叉核验机制 |
| **topic-planner** | ①在 mini_slate 修正后补 platform_hint 字段（wechat/xiaohongshu/zhihu/x/bilibili/toutiao）；②基于 mini_slate 五条产出平台任务单；③不得使用未修正 pack 内的未验证事实 |
| **content-writer** | 等 signal-scout + topic-planner 完成修正后，基于修正包写作 |

---

## 裁判备注

- `score=5 / status=rework`：整体 pack 结构性问题严重，但 3 个 P0 + 2 个 P1 共 5 条经补证后仍有 truthfulness，不得全部挂死。
- `continuity_decision=continuity_only`：仅允许 mini_slate 五条进入后续平台任务单，其他条目需 signal-scout 补证后方可重新提交 stage-gate。
- 当前 pack **不得**直接进入平台任务单生产；必须 signal-scout 提交修正版后重新走 Top20 stage-gate。
- 本轮 `truthful rework but still recoverable` 的判定依据：红队未发现事实失真、方向偏离或无可推进对象；三个 P0 均有清晰战略价值，补证路径明确。

---

> stage-gate 状态：rework
> continuity_decision：continuity_only
> continuity_output：top20_mini_slate（5 条）
> 下一动作：signal-scout 返工，修正版重新提交 Top20 stage-gate
> 重评分标志：本文生成时间（17:09）晚于 redteam 定稿（17:04），为独立重新裁判，非旧版修订