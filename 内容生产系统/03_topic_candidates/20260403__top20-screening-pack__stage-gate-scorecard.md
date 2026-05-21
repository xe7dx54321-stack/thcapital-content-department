# Stage Gate Scorecard｜2026-04-03 Top20 初筛包

- `date`: `2026-04-03`
- `stage`: `top20-screening-pack`
- `owner`: `market-editor（裁判）`
- `delivery_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260403__top20-screening-pack.md`
- `redteam_review`: `n/a（scout 阶段交付包，非内容成品，无需红队骂稿）`
- `generated_at`: `2026-04-03 07:30:00 CST`

---

## 裁判结论

- `score`: `7.5`
- `status`: `rework`
- `status_rule`: `Top20 screening pack < 8 且非 truth failure；按 continuity_only lane 处理`
- `rework_mode`: `supplement_evidence / expand_validation`
- `是否保留原对象`: `yes`
- `topic_value_judgment`: `高`
- `execution_readiness`: `可补强`
- `continuity_decision`: `continuity_only`
- `continuity_output`: `top20_mini_slate`
- `continuity_rule`: `Top20 < 8 且非 truth failure 时默认写 continuity_only，优先产出 top20_mini_slate`
- `是否进入下一工序`: `yes（进入 platform-task-sheet 阶段，但需先完成以下补强）`

---

## 评分理由

### 做得好的地方

- **信源密度扎实**：225 份 source packet 收束成 20 个结构化候选，转化率合理，未堆砌原始材料
- **Top 层真实强**：`karpathy-openai-return`（28/30）、`gemma-4-multimodal-on-device`（26/30）、`openai-acquires-tbpn`（25/30）、`qwen3-6-plus-real-world-agents`（25/30）四个候选均有一手官方锚或 HN 300+ 分验证，质量可信
- **多平台多语种覆盖**：X / HN / B站 / 知乎 / Reddit / GitHub Trending / 专家媒体（The Batch / Substack）均有交叉验证
- **风险标注诚实**：x.ai 快照页 SpaceX 收购 xAI / xAI $20B Series E 未独立核实这件事已明确标出，未粉饰
- **候选分层结构清晰**：`top3_must_watch` / `top6_strong_pool` / `holdout_watchlist` 三层结构合理，裁判和老板都能快速定位重点
- **supply_risk 坦诚**：35% 一手 / 65% 转层、Axelera/Deeptune 归档日期等问题均主动说明

### 当前主要缺口

- **x.ai 官方单页高价值信号未核实**：SpaceX 收购 xAI 和 xAI $20B Series E 若为真，是 MAJOR 级事件，但报告本身无法确认；这是 Top3 候选 `xai-grok-business-enterprise` 的核心风险
- **xAI 三条同发（Business + Enterprise + Voice Agent API）信号强度被高估**：当前给分 22-23/30，但三条均依赖快照层，同页 SpaceX/xAI 高强度上下文尚未独立核实，visual_assets 和平台适配分可能虚高
- **归档候选拖累整体水位**：`deeptune-43m-series-a`（3月19日）和 `axelera-ai-250m`（2月24日）各占一个 Top20 席位，在当日时效口径下价值有限，建议降级为情报补录而非当日主推
- **部分候选证据链单薄**：`replicas-yc-background-coding-agents`、`veo-3-1-lite` 等候选只有快照层或 YC Launch 页，visual_assets 仅 1 分，数据硬度 2 分的候选偏多

### 为什么是这个分数

- 结构完整性和候选质量（Top4）给 8-9 分
- 证据核实透明度（主动标注 xAI 未核实）和信源多样性给 8 分
- 补强空间（xAI 核实、归档候选降级、证据链加固）扣分后给出 7.5 分

### 先改什么

1. **优先回链 x.ai/news 官方单页**，独立核实 SpaceX 收购 xAI 和 xAI $20B Series E 是否为真；若核实为真，立即升级为 Top1 并补充 `xai-mxa-acquisition` 独立候选
2. **将 Deeptune 和 Axelera AI 两个归档候选移出 Top20**：更新 `holdout_watchlist` 并替换为当日更新的其他候选（如有）
3. **加固 Top5 候选的 visual_assets 评分依据**：对照各平台已有截图/视频，明确写出可复用素材数量

### 后改什么

4. 对 `replicas-yc`、`veo-3-1-lite`、`ethan-mollick-agents` 等快照层候选补充原始链接可访问性说明
5. 完善 supply_risk 章节，对 225 份 packet 中"未进入 Top20 但值得关注"的候选做简单索引

---

## 若打回，必须修的三件事

1. **x.ai 官方单页回链核实**（blocker）：不核实则 `xai-grok-business-enterprise` 的 23/30 分无法支撑
2. **归档候选降级**：将 Deeptune / Axelera AI 从 Top20 候选降入情报补录，释放两个席位
3. **补充 Top3 候选的视觉素材清单**：明确列出已有截图/图表/视频数量，不足者注明缺口

---

## 返工顺序说明

- `先补证还是先换题`: **先补证**（xAI 核实）——信号强度够，补证成本低，补完后可直接升级
- `是否允许补证后原对象复评`: `yes`
- `若建议换题，触发条件`: xAI 同页两条高强度信号（SpaceX 收购 / $20B 融资）若核实为假，且 xAI 三条产品发布本身无可用细节，则换题

---

## 若放行，进入下一步的明确动作

- `next_owner`: `topic-planner`
- `next_output`: `20260403__platform-task-sheet.md`（正式任务单）
- `deadline_or_expectation`: `2026-04-03 12:00 CST 前产出；若 xAI 核实结果在 12:00 前回链，以核实结论更新 top3 候选后再进入 platform-task-sheet`
- `备注`: karpathy_openai_return 已于 05:08 CST 进入 approved_topic 并完成 draft pack，优先推进其 publish-ready 成品包评审；Top20 中其他候选的 platform-task-sheet 并行推进
