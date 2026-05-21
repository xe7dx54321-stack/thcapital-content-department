# 20260417 平台任务单

- `date`: `2026-04-17`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-17 18:20:00 CST`
- `input_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260417__top20-screening-pack.md`
- `top5_board`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260417__daily-top8-to-top5.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `rework + continuity_only 场景；Top5 板为 continuity_recovery final；本单为 limited task sheet，最多 4 个平台×1~2 任务槽位`
- `morning_flash_exclusion_applied`: `yes — hn_frontpage_47793411_claude_opus_4_7_20260417 因 morning_flash 已选同名事件，排除出 day_mainline`

---

## 全局主池 Top6

> 受 `continuity_only` 纪律约束，本日 Top6 全局主池仅含 4 个 day_mainline 可追溯候选；其余 2 槽位因 morning_flash 排除或候选稀缺而空缺，不得自行扩题。

| rank | topic_key | 标题 | 核心判断 | 为什么值得写 | 主要风险 | 来源 |
|------|-----------|------|----------|------------|----------|------|
| 1 | `wechat_zhidx_30_20260417` | 超30亿！中国迄今最大具身智能融资诞生 | P0 continuity | 4.5亿美元具身智能融资，PE+VC+产业资本联合押注，CEO 陈亦伦华为自动驾驶 CTO 出身；事实骨架硬 | 微信正文被截断，需补全关键数字再引用 | Top5 板 rank 1；Top20 mini_slate P0 |
| 2 | `wechat_founder_park_agent_agent_20260417` | 今年最火的开源Agent项目，如何思考Agent的自我进化？ | P1 continuity | 已是国内开发者社区热门讨论题，有 Founder Park 4885字深文章支撑 | partial source，需补原始来源再展开判断 | Top5 板 rank 5；Top20 mini_slate P0 |
| 3 | `hn_frontpage_47796469_codex_for_almost_everything_20260417` | Codex for almost everything | P0 continuity | OpenAI 官方发布，HN 高热，AI coding 工具主线明确，具备天然讨论空间 | 缺原始博客全文；补证前正文角度延展需谨慎 | Top5 板 rank 2；Top20 mini_slate P2（待补证） |
| 4 | `qbitai_site_ppio_pphermes_hermes_agent_20260417` | PPIO上线PPHermes：云端沙箱一键部署Hermes Agent | P1 continuity | AI Agent 部署赛道明确，PPIO 切入开发者工具场景；与主线条高度一致 | partial source，发布时间不够硬；缺全文深抓 | Top5 板 rank 3 |

## 三个最重要平台任务单

---

### `wechat`

#### Task 1
- `topic_key`: `wechat_zhidx_30_20260417`
- `目标读者`: `VC/PE 从业者、科技产业投资分析师、对具身智能和机器人赛道有关注的 high-level 读者`
- `切入角度`: `不以"30亿"数字为卖点，而是拆解：这轮融资背后的结构（高瓴+红杉+美团三路资金同框）意味着什么？小团队（CEO 陈亦伦华为 CTO 背景）经营这种方式的前提条件与边界在哪里？这件事对中国具身智能商业化路径意味着什么？`
- `核心论点`: `具身智能正在从"技术展示"进入"商业验证"阶段；这轮融资的豪华资方组合说明头部机构已在押注商业化拐点；关键看产品化节奏而非单纯估值`
- `证据抓手`: `4.5亿美元（≈30亿人民币）融资额；高瓴+红杉+美团联合领投；CEO 陈亦伦华为自动驾驶 CTO 背景；A1 机器人吉尼斯参数（需补）；天使轮对比（需补）`
- `source_ref_bundle`:
  - `原始微信全文（截断，需重新 x-reader 抓取）`: `https://mp.weixin.qq.com/s/LxIfr1d7zlRlZrRM8c3lMA`
  - `Deep Article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260417_121336__超30亿_中国迄今最大具身智能融资诞生__deep-article.md`
- `视觉建议`: `信息图：融资方结构图（高瓴/红杉/美团 logo 并列）+ CEO 履历时间轴 + 具身智能商业化阶段示意`
- `为什么适合该平台`: `微信是这件事的原始来源地，完整叙事和判断力最强的平台；30亿数字天然适配微信的深度阅读生态`
- `stage_gate_status`: `continuity_only`
- `continuity_note`: `正文引用前必须补全截断的微信全文关键段落；不得把 deep article 摘要直接带进正文，需回链原始来源`

#### Task 2
- `topic_key`: `wechat_founder_park_agent_agent_20260417`
- `目标读者`: `AI 开发者、独立开发者、对"一人公司"和 AI Agent 工具有兴趣的技术圈读者`
- `切入角度`: `不止步于"这个项目火"的表面现象，而是拆解：这个开源 Agent 项目在技术上做对了什么，让开发者社区愿意主动传播？它的自我进化思路对中国 AI 开发者有什么启发？`
- `核心论点`: `开源 Agent 的"自我进化"机制代表了一种新的开发者工具思路；不止是效率提升，而是降低 AI 应用开发门槛；这类项目的扩散速度本身就是一个值得关注的信号`
- `证据抓手`: `Founder Park 深文章（4885字，含 Harrison Chase + Daniel 观点）；开发者社区讨论热度；项目 GitHub 星标等可量化指标（需补）`
- `source_ref_bundle`:
  - `原始微信文`: `https://mp.weixin.qq.com/s/Jg1icaZ-W77yupIXcF6Q_A`
  - `Deep Article`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260417_121434__今年最火的开源agent项目_如何思考agent的自我进化__deep-article.md`
  - `Source Packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260417_121157__wechat_founder_park_agent_agent__source-packet.md`
- `视觉建议`: `代码逻辑简图（展示 Agent 自我进化机制）或社区讨论截图拼图（展示热度）`
- `为什么适合该平台`: `Founder Park 本身是微信生态内的深度科技媒体，受众与本文目标读者高度重叠；内容已有完整叙事骨架，可直接承接`
- `stage_gate_status`: `continuity_only`
- `continuity_note`: `本文已有 deep article，事实密度较好；但正文引用的项目原始来源（GitHub/官网）需补强，不得只依赖 Founder Park 二手叙事`

---

### `x`

#### Task 1
- `topic_key`: `hn_frontpage_47796469_codex_for_almost_everything_20260417`
- `目标读者`: `AI 开发者、创业者和对 AI Coding 工具感兴趣的技术社区用户；推特上的科技讨论者`
- `切入角度`: `不是简单报道 Codex 发布，而是抛出观点：这个工具的出现意味着什么级别的 coding 效率提升？它让"一人公司"的可操作性提高了多少？`
- `核心论点`: `OpenAI Codex 不是又一个 copilot，它代表 AI coding 从"辅助"进入"自主"的关键一步；它的边界在哪里、适合什么场景，不适合什么场景？`
- `证据抓手`: `OpenAI 官方博客全文（需补）；HN 热评观点（已有 partial）；与现有工具（Cursor/GitHub Copilot）的差异化对比（需补）`
- `source_ref_bundle`:
  - `OpenAI 官方博客`: `https://openai.com/index/codex-for-almost-everything/`
  - `Source Packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260417_104902__hn_frontpage_47796469_codex_for_almost_everything__source-packet.md`
- `视觉建议`: `短钩子推文（1~2 条）+ 可选：能力对比表（Codex vs Cursor vs Copilot）或 30 秒演示描述`
- `为什么适合该平台`: `OpenAI 发布 + HN 高热天然适配 X/Twitter 的快速传播链；开发者社区讨论热烈，首轮推文放大效果强`
- `stage_gate_status`: `continuity_only`
- `continuity_note`: `x-reader 抓取 openai.com 原始博客是强依赖；若无全文，降权为 holdout；不得只凭 HN 标题直接写判断`

---

### `bilibili`

#### Task 1
- `topic_key`: `qbitai_site_ppio_pphermes_hermes_agent_20260417`
- `目标读者`: `AI 开发者、对 Agent 部署有兴趣的技术观众、关注 AI infra 的中长视频受众`
- `切入角度`: `PPIO 的 Hermes 解决的是什么具体问题？云端沙箱一键部署对普通开发者和企业用户意味着什么？这个赛道还有哪些玩家？`
- `核心论点`: `AI Agent 部署正在从"自己搭"向"拿来用"演变；PPIO 的沙箱路线切中了一个真实的开发者痛点（快速评估 + 安全隔离）；这个方向的商业化潜力值得持续关注`
- `证据抓手`: `qbitai 报道全文（需补原始官网/产品页）；PPIO 官网产品参数（需补）；与同类产品的差异化点（需补）`
- `source_ref_bundle`:
  - `qbitai 报道`: `https://www.qbitai.com/2026/04/402085.html`
  - `Source Packet`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260416_225005__qbitai_site_ppio_pphermes_hermes_agent__source-packet.md`
- `视觉建议`: `产品演示截图或 1 分钟内功能演示描述（可做成视频脚本）；与同类产品（Docker/云函数）对比表格`
- `为什么适合该平台`: `B 站用户对 AI 工具和开发者技术有强偏好；技术 demo 类内容在 B 站有稳定流量；本话题天然适合中长视频展开`
- `stage_gate_status`: `continuity_only`
- `continuity_note`: `视频脚本制作前需补 PPIO 官网原始产品信息；不得只依赖 qbitai 二手报道`

---

### `xiaohongshu`

> continuity_only 纪律：wechat 已用满 2 slot；X 和 bilibili 各 1 slot；xiaohongshu / zhihu / toutiao 本轮不开放 standalone active slot。无剩余候选供这几个平台 standalone 展开，候选 6~8 整体进 Holdout。

#### Holdout 说明
- 小红书下轮若有新候选进入 Top5 板，可优先从 Holdout 中捞回；
- 理想汽车话题（holdout 7）品牌贴合度为"中"，不符合同行资本品牌定位，暂不安排；
- 若 top5 板中任意候选补证完成后，可从 Holdout 唤醒后在知乎展开（Codex 有天然讨论空间，适合问答/解释式展开）。

---

### `zhihu`
> 见 xiaohongshu holdout 说明。

---

### `toutiao`
> PPIO/PPHermes 话题经 WeChat 或 Bilibili 验证若流量好，可从 Holdout 唤醒后在头条做二次分发；今日头条用户对「具身智能」「机器人」话题有天然兴趣，可承接 WeChat Task 1 的简化版本。

---

## 六个主战场任务单

### `wechat`
- Task 1 + Task 2：见上方 `## 三个最重要平台任务单` — wechat

### `xiaohongshu`
- 本轮 continuity_only 纪律下不开放 standalone active slot；候选 6~8 整体进 Holdout，详见 Holdout 清单

### `zhihu`
- 本轮 continuity_only 纪律下不开放 standalone active slot；详见 Holdout 清单

### `x`
- Task 1：见上方 `## 三个最重要平台任务单` — x

### `bilibili`
- Task 1：见上方 `## 三个最重要平台任务单` — bilibili

### `toutiao`
- 本轮 continuity_only 纪律下不开放 standalone active slot；PPIO/PPHermes 话题经 WeChat 或 Bilibili 验证若流量好，可从 Holdout 唤醒后在头条做二次分发

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: `否`
- `理由`: `本日 4 个 day_mainline 候选均为 AI/Agent 开发者向内容，品牌贴合度符合同行资本人设；baijiahao 用户偏好泛科技和商业话题，与今日候选的主攻方向（开发者工具、AI coding）存在受众错位；若强行镜像，容易产出「标题党 + 低质量转载」，损伤品牌。不如集中资源做好主战场任务。`
- `承接哪篇主稿更优`: `WeChat Task 1（超30亿具身智能融资）适合做标题简写版进 baijiahao，但需等补证完成后判断；若 WeChat 主稿流量验证好，下一轮 Top5 可优先把该题写进 baijiahao 镜像层`

---

## Holdout 清单

### Holdout 1｜`hn_frontpage_47793411_claude_opus_4_7_20260417`
- `标题`: `Claude Opus 4.7`
- `为什么能进最终池`: `HN 高热；Anthropic 官方发布；市场潜力高；品牌贴合度高；有明确扩散热度入口`
- `为什么这轮没选`: `该事件已入选今日 morning_flash（20260417__morning-flash-source-bundle.md），按硬约束「已进 morning_flash 的同题对象必须排除出 day_mainline」`
- `什么时候可捞回`: `morning_flash 完成后（当日草稿箱已发出）；若 morning_flash 版本展开不足，可接力做差异化角度（如：与 OpenAI Codex 的横向对比，或 Opus 4.7 的实际测试体验）`

### Holdout 2｜`36kr_ai_claude_opus_4_7_20260417`
- `标题`: `刚刚，Claude Opus 4.7突然发布：不是最强，但奥特曼又得失眠`
- `为什么能进最终池`: `36kr 中文报道有原始锚点；标题反差感强，适配传播`
- `为什么这轮没选`: `与 hn_frontpage_47793411_claude_opus_4_7 同题（均指向 Opus 4.7 发布事件）；morning_flash 已排除同类项，day_mainline 不得重复；且 36kr 角度与 morning_flash 版本可能高度重叠`
- `什么时候可捞回`: `morning_flash 版发出后；若该版缺少技术细节或开发者视角，可做「36kr 版本 vs 官方版本的 Gap 分析」`

### Holdout 3｜`zhihu_hot_ai_zhihu_hot_20260417`
- `标题`: `理想净利降八成，有部门全员无年终奖，理想当前面临怎样的经营困境？`
- `为什么能进最终池`: `知乎热题；有明确扩散热度入口；具备天然讨论空间`
- `为什么这轮没选`: `品牌贴合度仅为"中"；同行资本的人设是 AI/Agent/科技金融，不是汽车消费；且硬数据偏少，展开判断风险高`
- `什么时候可捞回`: `若有理想汽车一手财报数字或高管发言原始来源补入，且该题与 AI/科技金融主线条产生明确连接点（如：理想如何用 AI 降本），可重新评估`

### Holdout 4｜`wechat_geekpark_15_pocket_4_opus4_7_20260417`
- `标题`: `雷军15小时直播验证「一次充电」到上海；大疆 Pocket 4 上市即售罄；Opus4.7 正式上线 | 极客早知道`
- `为什么能进最终池`: `partial source；极客公园有完整报道；仍处业务窗时效内`
- `为什么这轮没选`: `该题打包了 3 个不同事件（小米直播/大疆/Pocket4/Opus4.7），缺乏统一核心论点；题目偏硬件消费电子，与 AI/Agent 主线条偏离；Pocket4 泛流量适配有限`
- `什么时候可捞回`: `若大疆 Pocket4 与 AI/影像 Agent 工具产生明确连接（如：用 AI 工具自动化影像生产），可拆解单独立项；其余子题不适合同行资本品牌`

---

## 任务单生成说明

- `platform_task_sheet_status`: `limited_continuity`
- `active_slots_total`: `4`（wechat×2 + x×1 + bilibili×1）
- `holdout_slots_total`: `4`（含 morning_flash 排除 1 个，同题 1 个，品牌偏离 2 个）
- `baijiahao_judge`: `否，不立镜像题`
- `next_trigger`: `信号：任一 source_ref_bundle 原始来源补证完成后，可从对应 Holdout 唤醒重新评估；优先唤醒 Codex（X slot）和 PPIO/PPHermes（头条二次分发）`
- `supply_gap_note`: `今日可用 day_mainline 候选共 5 个（Top5 板），扣除 morning_flash 排除 1 个，实际可推进 4 个。WeChat 2 slot 用满；X 和 Bilibili 各 1 slot。供给侧偏少但真实，不凑数。`
