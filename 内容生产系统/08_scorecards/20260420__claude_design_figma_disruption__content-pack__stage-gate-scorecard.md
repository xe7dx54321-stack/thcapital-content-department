# Stage Gate Scorecard | day_mainline content-pack

- `date`: `2026-04-20`
- `stage`: `day_mainline content-pack stage-gate`
- `owner`: `market-editor`
- `delivery_pack`: `claude_design_figma_disruption`
- `redteam_review`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260420__claude_design_figma_disruption__content-pack__redteam-review.md`
- `redteam_generated_at`: `2026-04-20 21:49 CST`（第二轮红队，替代 19:36 初轮结论）
- `prior_scorecard_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260420__claude_design_figma_disruption__content-pack__stage-gate-scorecard.md`
- `prior_scorecard_generated_at`: `2026-04-20 19:42 CST`
- `generated_at`: `2026-04-20 21:53 CST`
- `scorecard_type`: `day_mainline publish-ready content-pack judgment（第二轮裁判，基于 21:49 红队升级发现）`

---

## 裁判结论

- `score`: `4.5`（从 19:42 初评 6.5 下调至 4.5，反映证据链造假实锤化 + P2 未修复）
- `status`: `rework`
- `status_rule`: `status 只允许写 pass 或 rework；若进入 continuity lane，也仍写 rework，并把 continuity 结果写进下方两个字段`
- `rework_mode`: `supplement_evidence + rewrite_quality`
- `是否保留原对象`: `yes`
- `topic_value_judgment`: `高`
- `execution_readiness`: `暂不可发（truth barrier 未解除）`
- `publish_ready_platforms`: `none`
- `continuity_decision`: `stop_for_truth`（证据链完整性无法通过补证绕过时触发）
- `continuity_output`: `carry_rework_backlog`
- `continuity_rule`: `content-pack <8 且非 truth failure 时必须保留最高分对象继续推进，若已有平台可先行则写 publish_ready_platforms 并用 backlog_publish 标记；只有 truth failure 才允许彻底停下`
- `truth_failure_judgment`: `混合型 truth barrier——7% 数据无法证伪也无法证实（不可验证），且视觉素材层存在系统性造假声张（local-generated 图冒名为原始截图）。两者合并构成 truth barrier，不是单一可修复项`
- `是否进入下一工序`: `否；P1 fatal 未解除，publish gate 仍为 blocked_by_rework`

---

## 评分理由

### 做得好的地方（保留初评 6.5 的优点项）

1. **主题本身信号意义成立**——Claude Design vs Figma 是目前最清晰的"AI 产品层颠覆 SaaS"可量化信号，事件逻辑真实，不因证据问题而消失
2. **三层分析框架逻辑完整**（事件层/市场层/主线路层），可直接复用，是本文最稳固的骨架
3. **结尾 4 个跟踪信号设计到位**，是真正的读者价值输出
4. **risk_note 存在且意识正确**
5. **封面图有生成**，头图意识到位
6. **title-options.md 里有 3 个远优于当前选中标题的备选**，修复路径清晰

### 21:49 红队升级发现的致命问题（相比 19:42 初评新增加重）

**P1 升级：视觉证据链造假（实锤级别）**

- 19:42 初评认定 P1 为"核心数字无可信锚点"，属"补证不足"
- 21:49 红队升级发现：slot_1（80__slot_1.png）正文标注为"原始证据锚点"，但 `asset-manifest.json` 白纸黑字 `source_url: "local://slot-story-card"`，`source_class: "local-generated"`，不是任何形式的真实截图
- Zhihu 原始 URL（https://www.zhihu.com/question/2028817450829976782）在系统内部被标记为 `blocked-source`（来源域名未进入安全抓图白名单），全程没有任何外部真实截图进入 pack
- 全 5 张 visual assets 全部 `local-generated`，`capture-log.md` 确认 `source_asset_count: 0`，`external_safe_count: 0`
- 这不是"补证不足"，是**包装层面对读者声称"先证明对象"，但展示的"证明"是自己生成的插图**

**P1 新增：7% 数据不可验证状态未改善**

- 距 19:42 评分已逾 2 小时，signal-scout 未补入任何真实 Figma 股价数据锚点
- citation-block.md 仍只有一条知乎讨论帖，capture-log.md 确认该知乎帖也是 `skipped` 状态
- 正文"7%"仍是裸奔状态

**P2 未修复（标题仍为零吸力）**

- 21:49 红队确认：wechat.md 最后修改时间 19:33（早于 19:36 红队），之后无任何实质性返工
- 标题仍是"如何评价 Claude Design 发布后 Figma 股价下跌 7%？"——纯问答体，无收益承诺，无好奇缺口

### 为什么是这个分数

- 主题价值高（+1.5）+ 框架完整（+1.5）+ 风控意识（+0.5）+ 有头图（+0.5）→ 基础分约 4
- P1 fatal 证据链造假（视觉层造假 + 数据层不可验证）：-2.5 → 1.5
- P2 标题未修复：-0.5 → 1
- 补投窗已关闭（21:30 CST），无今日 publish-ready 出口：-0.5 → 0.5
- 底分保护（truth barrier 非 outright false，主题本身成立，框架可复用）：+4 → **4.5**

---

## 若打回，必须修的三件事

### 必须修（P1 fatal 解锁前不能进入 publish-ops）

**1. 补入真实 Figma 股价原始数据锚点（signal-scout + content-writer）**
- signal-scout 必须在下一工作窗口内找到 Figma（NYSE 代码 FGRS 或 Figma 股票代码确认）4 月 17 日附近真实股价数据
- 可信来源：Yahoo Finance / Finviz / 官方 IR 公告 / 新闻存档（如 Reuters/Bloomberg）
- 补入 citation-block.md 并在正文中显式标注来源
- 若 2 个工作日内找不到任何真实锚点：content-writer 将"下跌约 7%"改为"出现明显抛售迹象"这类定性表述，同步修改标题去掉具体数字

**2. 修正 slot_1 图的包装说明（content-writer）**
- 不能再把 `local://slot-story-card` 的图标注为"原始证据锚点"
- 若无真实来源截图：删除"原始证据锚点"标注，或改为"事件示意图（AI生成）"，并在 caption 注明实际来源
- citation-block.md 必须反映 slot_1 图的真实 source_url

**3. 换标题（content-writer，从 title-options.md 直接选）**
- 禁止使用纯问答句作为主标题
- 建议直接采用：选项 3（"Claude Design 颠覆 Figma 背后，真正该看的变量是什么？"）或选项 6（"3 个点看懂：Claude Design 发布后 Figma 股价下跌 7% 到底改变了什么"）

### 建议修（P2-P5，可与 P1 并行处理）

4. 砍掉"本文不只是一条快讯"段落，从"先把事情说清楚"直接开讲
5. 修"关于作者"版块为判断收束句，匹配正文严肃基调
6. 确认 slot_2~4 图是否与正文实际分层结构/可执行 workflow 匹配；若不匹配则移除或调整

---

## 返工顺序说明

- `先补证还是先换题`: **先补 P1（signal-scout 补股价数据 + content-writer 修正 slot 说明），再换标题，最后修 hook 和作者版块**
- `先补证的优先级`: P1 是 truth barrier 的核心，必须先解锁才能评估后续是否具备 publish-ready 条件
- `是否允许补证后原对象复评`: `yes`
- `若建议换题，触发条件`: signal-scout 在 2 个工作日内找不到任何真实金融锚点，且 content-writer 无法将"7%"改为可信的定性表述 → 触发 replace_topic 评估

---

## 21:30 补投窗关闭后状态确认

| 项目 | 状态 |
|------|------|
| 补投窗硬截止 | 21:30 CST |
| 当前时间 | 21:53 CST（裁判时已过窗） |
| P1 补证状态 | **未完成**——signal-scout 未补入真实金融截图 |
| visual assets 状态 | 全量 local-generated，slot_1 仍为假冒"原始证据锚点" |
| publish gate | `blocked_by_rework`（未解除） |
| day_mainline wechat 今日入草稿箱 | **0 篇** |

---

## 给 signal-scout 的指令（P0 动作）

在下一工作窗口内（建议 4 月 21 日上午）：
1. 查 Figma 股票代码（NYSE，若为上市公司）4 月 17 日附近股价数据
2. 可用来源：Yahoo Finance 历史数据、Finviz、Reuters/Bloomberg 财经档案、官方 investor relations 公告
3. 若找到数据：补入 `citation-block.md`，signal-scout 提供原始链接，content-writer 在正文中显式标注
4. 若找不到任何可信数据锚点：显式告知 content-writer，以便将"7%"改为定性表述，并同步修改标题

---

## 给 content-writer 的指令（P0 动作）

在 signal-scout 提供数据或确认无法提供后：
1. 根据数据情况修正正文 P1（补锚点或改定性）
2. 修正 slot_1 图的说明文字，显式注明 source_url = local://slot-story-card（不是原始截图）
3. 从 title-options.md 选一个强标题替换当前弱标题
4. 砍 hook、修作者版块（P2-P5 可并行）
5. 完成后重新提交红队审查

---

## 给 publish-ops 的指令

当前 `claude_design_figma_disruption` **不得进入 publish queue**，原因：
- P1 fatal 未解除（证据链完整性不满足）
- publish gate 仍为 `blocked_by_rework`
- 补投窗已关闭，今日无 wechat 草稿箱入箱

若明日 signal-scout 补到可信数据锚点且 content-writer 完成 P1-P3 修复，重新提交红队审查 → 新评分卡通过后方可入 queue。

---

## 今日裁判总结

| 项目 | 结果 |
|------|------|
| 今日 day_mainline content-pack 红队审查数 | 2（含 2 轮 claude_design_figma_disruption 红队） |
| 今日 day_mainline content-pack 评分卡数 | 2（含本份更新版） |
| 今日 premium pass 数 | 0 |
| 今日 continuity 输出 | carry_rework_backlog（claude_design_figma_disruption，4.5 分） |
| 今日 day_mainline 草稿箱入箱数 | **0** |
| 最接近可发布的 same-day 对象 | 无（truth barrier 未解除） |
| 明日 P0 主推进对象 | claude_design_figma_disruption（P1：signal-scout 补 Figma 股价数据） |
| 是否需要换题 | 暂不换题；若 2 个工作日内 signal-scout 确认无法补证，再触发 replace_topic |
| 今日 zero premium pass | **确认**——硬 deadline 已过，truth barrier 未解除，无可发布成品 |