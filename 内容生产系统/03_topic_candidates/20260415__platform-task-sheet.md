# 20260415 平台任务单

- `date`: `2026-04-15`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-15 18:26 CST`
- `run_token`: `20260415`
- `input_scorecard`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260415__top20__stage-gate-scorecard.md`（final，score=8.0，continuity_only）
- `input_top5_board`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260415__daily-top8-to-top5.md`（final，continuity_only，board_mode=inferred_rework_recovery，2 candidates）
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `continuity_only limited task sheet：WeChat 2 主槽；另最多开 2 平台各 1 active slot；其余入 Holdout`
- `morning_flash_exclusion_check`: `已完成 — Top5板2个P2 continuity对象不在morning_flash覆盖范围`
- `supply_note`: `Top5板仅含2个P2 continuity recovery候选；scorecard含12 unconditional+3 conditional；本limited sheet从Top5板承2槽、从scorecard mini_slate扩2槽，共4 active slots；其余候选入Holdout`

---

## 全局主池 Top6（Top5板候选 × 2 + scorecard扩补 × 4）

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|------|-----------|---------|-------------|---------|
| 1 | GPT_5.4_Cyber_vs_Mythos_OpenAI_Anthropic_安全AI竞争 | 双头同日发布安全AI旗舰产品，$300B vs $80B 收入争议是强争议话题 | 4月15日最新事件；安全AI是Agent Safety最重要的商业落地方向；Anthropic估值翻倍至$800B融资热度空前 | 两款产品均早期访问，商业化成熟度待观察；#18 conditional携带补证guardrail |
| 2 | Seedance_2.0_API_字节跳动_火山引擎_1元每秒_视频生成 | "1元/秒"工业定价锚点+贾樟柯creative industry背书 | 中国AI视频生成工业化里程碑；硬数字锚点强传播性；字节+火山引擎供给侧信任 | API质量稳定性待长期验证；"1元/秒"为媒体实测非官方定价，#20 conditional携带标注guardrail |
| 3 | OmniVTA_视触觉世界模型（scorecard P0） | 六机构背书+arXiv+HuggingFace三件套；具身智能赛道核心突破 | 视触觉融合是具身AI最高壁垒方向；学术+工程双验证；22/30 scorecard最高分 | 商业化路径尚不清晰；仅限知乎/X平台轻量切入 |
| 4 | WideSeek-R1_清华×无问芯穹（scorecard P0） | "广度扩展"概念填补R1后开源社区空白 | 清华背景+无问芯穹商业化双背书；R1已成行业基准对比对象；开源可控性是builder关注焦点 | 概念需大众化翻译；仅限知乎/X平台轻量切入 |
| 5 | （Holdout） | 见本文末Holdout清单 | | |
| 6 | （Holdout） | 见本文末Holdout清单 | | |

---

## 六个主战场任务单

## 三个最重要平台任务单

（continuity_only limited sheet：本轮活跃槽位 WeChat×2 + X×1 + Bilibili×1，共4个active slots）

### `wechat`

#### Task 1 — 主稿（Top5板 P2-①）

- `topic_key`: `GPT_5.4_Cyber_vs_Mythos_OpenAI_Anthropic_安全AI竞争`
- `目标读者`: 关注AI投资与科技竞争格局的从业者、builder、一级市场参与者
- `切入角度`: 双头同日发布安全AI旗舰——这不只是产品战，是一场关于"谁在定义AI安全标准"的路线之争
- `核心论点`: GPT-5.4-Cyber与Anthropic Mythos的同日亮相，揭示安全AI已从研究概念进入商业落地冲刺阶段；Anthropic估值翻倍与$300B/$80B争议是这个赛道热度的直接注脚
- `证据抓手`:
  - GPT-5.4-Cyber发布（原始来源待补，content-writer须先查OpenAI官方 announcement）
  - Anthropic Mythos同日发布
  - Business Insider: Anthropic估值$380B→$800B报道
  - $300B vs $80B收入争议（携带"Anthropic尚未公开回应"标注，见scorecard #18 guardrail）
- `source_ref_bundle`:
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260415_121949__wechat_geekpark_ai_23_q1_7200_openai_anthropic_300_80__source-packet.md`
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260415_122356__斯坦福报告_美国ai投资为中国23倍_但模型差距消失_q1豆包海外版下载7200万次_openai指控anthropic_300亿收入80亿造假_极客早知道__deep-article.md`
- `视觉建议`: 双头对峙结构图（OpenAI vs Anthropic），标注关键数字（$300B/$80B/估值翻倍）；安全AI产品发布时间轴
- `为什么适合该平台`: 微信是深度分析主战场；安全AI竞争格局需要完整叙事链
- `platform_slot`: 1/2
- `guardrails`: ①正文必须先补OpenAI/Anthropic各自官方发布来源再展开；②"Anthropic尚未对OpenAI指控作公开回应"须在正文中显式标注

#### Task 2 — 主稿（Top5板 P2-②）

- `topic_key`: `Seedance_2.0_API_字节跳动_火山引擎_1元每秒_视频生成`
- `目标读者`: 关注AI工具工业化与创作者经济的从业者、builder、投资人
- `切入角度`: 视频生成进入"分币级定价"时代——1元/秒意味着什么？
- `核心论点`: 字节Seedance 2.0以"1元/秒"打破视频生成成本壁垒，与Sora/Runway/Pika形成鲜明对比；贾樟柯合作提供creative industry落地的可信背书；版权/肖像安全标准是工业级采用的关键前提
- `证据抓手`:
  - "1元/秒"定价（携带"媒体实测估算"标注，见scorecard #20 guardrail）
  - Lanbow官方GitHub token计价28元/百万tokens（供读者换算）
  - 贾樟柯贺岁短片合作
  - 92%+完成率/~200 sessions（携带"公司口径"标注）
- `source_ref_bundle`:
  - 同上source packet
- `视觉建议`: 视频生成价格对比表（Seedance vs Sora vs Runway vs Pika）；"1元/秒"成本可视化
- `为什么适合该平台`: 微信适合承载"数字+工业"类深度叙事
- `platform_slot`: 2/2
- `guardrails`: ①"1元/秒"须加"媒体实测估算"标注；②补API官方token计价（28元/百万tokens）供读者换算；③92%+完成率标注为公司口径

---

### `x`（Twitter/X）

#### Task 1 — 快讯/观点钩子（scorecard P0扩补，排除morning_flash已覆盖）

- `topic_key`: `OmniVTA_视触觉世界模型`
- `目标读者`: AI开发者、具身智能研究者、开源社区成员
- `切入角度`: 视触觉融合世界模型——六机构背书，GitHub 2,700+ stars，具身智能赛道的新信号
- `核心论点`: OmniVTA是当前视触觉融合研究中最接近工业落地的高分候选；arXiv+HuggingFace+六机构背书三件套提供了可验证的学术+工程双重背书
- `证据抓手`:
  - OmniVTA GitHub（stars数）
  - arXiv论文链接
  - HuggingFace模型页
  - 六机构联合署名
- `source_ref_bundle`: 见scorecard Unconditional Cleared #1
- `视觉建议`: 简洁数字卡片（GitHub stars / 机构数量 / 论文引用）；视触觉 vs 纯视觉对比示意图
- `为什么适合该平台`: X是开发者社区扩散主战场；快讯+观点钩子适合简短有力形式
- `platform_slot`: 1/1
- `guardrails`: 商业化路径尚不清晰，文末需带"本文仅作技术信号跟踪，不构成投资建议"

---

### `bilibili`

#### Task 1 — 科普/深度解说（scorecard P0扩补，排除morning_flash已覆盖）

- `topic_key`: `WideSeek-R1_清华×无问芯穹`
- `目标读者`: AI学习者、技术爱好者、B站科技区观众
- `切入角度`: WideSeek-R1——清华系"广度扩展"能否成为R1之后最重要的开源复现？
- `核心论点`: WideSeek-R1是R1开源热潮后，清华系团队在"广度扩展"方向的重要尝试；无问芯穹的加入提供了从学术到商业化的桥梁；是builder监控开源R1生态的关键节点
- `证据抓手`:
  - 清华大学研究背景
  - 无问芯穹商业化背书
  - "广度扩展"概念（需content-writer大众化翻译）
  - scorecard #2 score=21/30
- `source_ref_bundle`: 见scorecard Unconditional Cleared #2
- `视觉建议`: B站适合技术解读图解；建议用"广度 vs 深度扩展"对比图；开源社区生态简图
- `为什么适合该平台`: B站用户对技术解读接受度高，适合"广度扩展"概念的大众化翻译
- `platform_slot`: 1/1
- `guardrails`: "广度扩展"概念需content-writer做大众化翻译，不得直接使用技术术语堆砌

---

### `xiaohongshu` — Holdout

> Top5板2个P2 continuity对象（安全AI竞争 / 视频生成1元/秒）均为"事件+数据"类深度题，不适合小红书轻量种草节奏；scorecard P0/P1候选（OmniVTA/WideSeek-R1/黄仁勋GTC等）已在morning_flash覆盖；本轮 Xiaohongshu 无合适候选，入Holdout。

---

### `zhihu` — Holdout

> Top5板2个P2 continuity对象适合深度叙事但知乎需要更强的问答式/对比式结构；scorecard P0/P1中适合知乎的候选（OmniVTA/WideSeek-R1/CHI2026 CoBRA）已在morning_flash覆盖或不适合本轮continuity节奏；本轮 Zhihu 入Holdout，下轮premium pass时可优先从scorecard P2中捞回。

---

### `toutiao` — Holdout

> 头条算法偏向大众化、时效性强的内容；Top5板P2 continuity对象（GPT-5.4-Cyber vs Mythos / Seedance 2.0）虽有强时效性，但叙事深度与头条受众匹配度存疑；scorecard P1/P2中适合头条的候选（Apple Siri开放/Context新操作系统）尚未补齐conditional guardrail；本轮 Toutiao 入Holdout。

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: **否**
- `理由`: 
  - Top5板2个P2 continuity候选（GPT-5.4-Cyber vs Mythos / Seedance 2.0）均属强时效事件驱动，SEO长尾价值弱于深度分析类内容
  - scorecard mini_slate中高SEO潜力候选（#12 Context新操作系统 / #14 Apple Siri / #3 天工AI）本轮均因morning_flash覆盖或conditional guardrail未入主池
  - `baijiahao` 作为SEO镜像层，应优先承接下轮premium pass中scorecard P1高品质分析类内容，而非continuity_only稀疏候选
- `承接哪篇主稿更优`: 若下轮出现#12 Context新操作系统或#14 Apple Siri等强SEO分析题，优先进入百家号；本轮不单独立项

---

## Holdout 清单

### OmniVTA_视触觉世界模型
- `为什么能进最终池`: scorecard P0最高分22/30；六机构背书+arXiv+HuggingFace三件套；具身智能是当前最热投资方向之一
- `为什么这轮没选`: 本轮为continuity_only limited sheet，仅开放4个active slots；已分配给Top5板2槽+scorecard P0扩2槽，OmniVTA作为scorecard P0在本轮作为X平台扩补而非独立主战场选题
- `什么时候可捞回`: 下轮premium pass时作为独立WeChat/知乎主战场候选；或当morning_flash无暇覆盖时升格

### WideSeek-R1_清华×无问芯穹
- `为什么能进最终池`: scorecard P0=21/30；清华×无问芯穹双背书；R1开源生态持续受builder关注
- `为什么这轮没选`: 同上，continuity_only limited sheet容量有限，作为Bilibili扩补slot入本轮
- `什么时候可捞回`: 下轮premium pass时作为独立WeChat/知乎主战场候选

### 黄仁勋GTC_双叙事（scorecard #7 P0）
- `为什么能进最终池`: scorecard P0=21/30；黄仁勋GTC是AI行业最高影响力事件之一；双叙事（技术+商业）结构清晰
- `为什么这轮没选`: scorecard标注"补NVIDIA官方announcement（非阻塞，建议）"；且推测已被morning_flash覆盖
- `什么时候可捞回`: morning_flash确认未覆盖时，下轮priority升格；或signal-scout补齐NVIDIA官方来源后

### 天工AI全模态升维（scorecard #3 P1）
- `为什么能进最终池`: scorecard P1=20/30；中关村论坛背书；全模态是今年具身+多模态投资主轴
- `为什么这轮没选`: scorecard建议补中关村论坛原始演讲稿（非阻塞）；本轮active slots已满
- `什么时候可捞回`: signal-scout补齐中关村论坛原始来源后，下轮premium pass优先

### CHI2026_CoBRA（scorecard #4 P2）
- `为什么能进最终池`: scorecard P2=19/30；顶会Best Paper；人机交互方向高质量学术信号
- `为什么这轮没选`: CHI2026为学术顶会，传播门槛较高；更适合知乎/X轻量切入，本轮slots有限
- `什么时候可捞回`: 下轮premium pass且知乎/X平台有空余slot时优先捞回

### aiXcoder_aiX-apply-4B（scorecard #5 P1）
- `为什么能进最终池`: scorecard P1=20/30；代码生成+AI编程工具方向；builder关注度高
- `为什么这轮没选`: scorecard建议补充竞品对比基准（非阻塞）；本轮active slots已满
- `什么时候可捞回`: signal-scout补齐竞品对比基准后，下轮premium pass优先

### Context才是新操作系统（scorecard #12 P1）
- `为什么能进最终池`: scorecard P1=20/30；极客公园完整采访；OS叙事是AI行业最强框架之一；强SEO价值
- `为什么这轮没选`: 本轮continuity_only limited sheet容量有限；强SEO价值应进入下轮百家号镜像层
- `什么时候可捞回`: 下轮premium pass时优先进入WeChat主战场+百家号SEO镜像层双通道

### Apple_Siri_开放（scorecard #14 P1）
- `为什么能进最终池`: scorecard P1=20/30；Apple WWDC 2026（6月8日）预期；Apple生态开发者关注度高
- `为什么这轮没选`: scorecard明确标注"不得作为已发生事实"；属于预期管理类题，本轮slots有限
- `什么时候可捞回`: WWDC 2026前两周，升格为倒计时话题，进入WeChat+头条双通道

### AMI_1.03B_Yann_LeCun（scorecard #15 P1）
- `为什么能进最终池`: scorecard P1=18/30；$1.03B融资金额大；Yann LeCun署名背书强
- `为什么这轮没选`: scorecard标注"公司成立于2026年早期；JEPA世界模型为研究方向非已验证产品"；强争议性有限；本轮slots有限
- `什么时候可捞回`: JEPA世界模型有实质性产品进展时升格

### GLM-5.1（scorecard #17 P2）
- `为什么能进最终池`: scorecard P2=17/30；对标Claude Opus 4.5方向；开源大模型社区关注
- `为什么这轮没选`: scorecard注明"同任务集待独立验证"；属于证据待确认类
- `什么时候可捞回`: 有独立第三方benchmark验证结果后升格

### 大疆_DJI_Air_3S（scorecard #11 P2）
- `为什么能进最终池`: scorecard P2=16/30；消费电子+AI视觉双重赛道；小红书/哔哔适配
- `为什么这轮没选`: 本轮Xiaohongshu/Bilibili slots已用尽；DJI属硬件非AI软件叙事为主
- `什么时候可捞回`: 下轮premium pass时作为小红书/哔哔平台专 slots优先候选

### Claude_Code_Telegram_Discord（scorecard #13 P2）
- `为什么能进最终池`: scorecard P2=14/30；开发者生态扩展信号；Claude Code影响力
- `为什么这轮没选`: 分数相对较低；更适合X/Telegram社区轻量传播而非平台主战场
- `什么时候可捞回`: 若Claude Code有重大生态更新时作为快讯处理

### #6 SakanaAI_AI-Scientist-v2（scorecard P1 conditional）
- `为什么能进最终池`: scorecard P1=17/30；GitHub 2,708 stars真实；ICLR Workshop投稿真实（需补官方链接）
- `为什么这轮没选`: **Fatal证据缺口**：ICLR peer review声明零源可查；叙事核心需从"ICLR认证"调整为"GitHub stars + Workshop投稿"
- `什么时候可捞回`: signal-scout补齐ICLR 2025 Workshop official program链接后，按conditional cleared路径升格

### #18 ATLAS_GPU超越Claude_Sonnet（scorecard P1 conditional）
- `为什么能进最终池`: scorecard P1=17/30；ATLAS benchmark提供量化对比信号
- `为什么这轮没选`: **Narrative pivot required**：Anthropic尚未公开回应OpenAI指控；叙事核心须从财务争议→GPT-5.4-Cyber vs Mythos产品竞争；Top5板#1已覆盖本题
- `什么时候可捞回`: Anthropic正式回应后，或当产品竞争叙事有独立新进展时升格

### #20 Lanbow_开源（scorecard P1 conditional）
- `为什么能进最终池`: scorecard P1=17/30；"1元/秒"是强传播数字锚点
- `为什么这轮没选`: **Pricing claim待确认**："1元/秒"为媒体实测非官方定价；Top5板#2已覆盖本题（Seedance 2.0）
- `什么时候可捞回`: 字节/火山引擎官方API定价确认后，或Lanbow官方定价页上线后升格

---

## 自检确认

| 检查项 | 结果 |
|--------|------|
| stage_gate_status | `continuity_only` ✓ |
| WeChat slots ≤ 2 | 2 slots ✓ |
| 额外平台slots ≤ 2 | X + Bilibili = 2 slots ✓ |
| active slots全部追溯Top5板或scorecard | 4 slots全部可查 ✓ |
| 无morning_flash同题 | 已确认排除 ✓ |
| guardrails注入 | #18/#20 guardrails已写入对应任务 ✓ |
| holdout覆盖率 | scorecard全部15个未入active候选已写入Holdout ✓ |
| baijiahao判断 | 已给出"否"+理由 ✓ |
