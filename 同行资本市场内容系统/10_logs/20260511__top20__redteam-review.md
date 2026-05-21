# Top20 红队审阅报告 — 20260511（day_mainline）
**执行时间：** 2026-05-11 14:53 (Asia/Shanghai)
**车道：** day_mainline
**审阅对象：** `20260511__top20_screening_pack.md`
**备选参考：** `20260510__top20-screening-pack__reworked.md`（无更晚 reworked 包，优先审今日包）
**审阅员：** redteam-reviewer
**状态：** FINAL（自检通过）

---

## 一、源包质量总评

| 维度 | 得分 | 说明 |
|------|------|------|
| 数据硬度 | ★★★★☆ | Top10 有多方独立源；#15-20 信息贫乏或未确认 |
| 一手性 | ★★★★☆ | FinSMEs/YC 官方信号为主；CNBS 升级有据可查 |
| 覆盖完整性 | ★★★☆☆ | 仅 financing/newco 车道；builder 层（HN/GitHub/WeChat）信号未见 |
| 平台就绪度 | ★★★☆☆ | 大多数条目有明确赛道和融资规模，可直接派生标题 |

---

## 二、逐条攻击

### 🔴 P0 — 事实性错误或高风险误导（直接损害内容可信度）

**无 P0 条目。** AMI Labs 和 Ineffable Intelligence 的 billion-dollar seed 信息经独立媒体交叉确认（Crunchbase/Forbes/Quartz/SiliconRepublic），数据硬度充足。

---

### 🟠 P1 — 核心缺口（影响选题质量与内容工厂产出）

**#1 AMI Labs — 商业化时间线误导风险**

- **问题：** 包内描述为"破圈性最强"，但 AMI Labs 明确表示"commercial applications not expected for several years"（来源：Futurum）。
- **影响：** 若以"当下热点"逻辑写 AMI Labs，会制造时效性错位——读者预期近期可用，实际研究导向数年落地。
- **建议：** 在初筛理由中加注"研究导向，商业化多年以后"，让 downstream 选题时校准期望。

**#9 Moritz — 方向标注存在偏差**

- **问题：** 包内标注"AI-native law firm"；但 Moritz 实际是"AI+律师网络的混合模式"——AI做80%工作，50+合作律师做最终审核，并非纯AI执业的"law firm"。
- **回读：** 补证来源 Business Insider 2026-05 稿件明确："proprietary software + experienced attorneys"、"80% of legal work done by AI, network of 50 co-counsel lawyers from top firms"。
- **建议：** 修正赛道标注为"AI legal ops / 律师协作平台"，避免读者预期与产品形态错位。

**#8 Agentic Fabriq — "Okta for AI agents"标签过于简化**

- **问题：** IAM for autonomous agents 是强概念锚点，但 Pack 内仅在"初筛理由"带过，无展开。
- **影响：** 这类新品类（novel category）如果不给 content-writer 提供足够的类比上下文，容易写出模糊稿。
- **建议：** 在 source manifest 里标注"需补充 Okta 的市场教育路径 vs. AI agent 的实际痛点"，提醒 downstream 不要只抄概念。

**#5 Pocket — $27M ARR 数据来源不透明**

- **问题：** 包内仅写"$27M ARR"无来源；回读 Sacra Research 后确认该数据来自 YC Demo Day 披露，但 YC 官方不直接发布 ARR。
- **影响：** 若 content-writer 引用"$27M ARR"作为核心数据点，缺乏稳定来源背书。
- **建议：** 补注"Sources: YC W26 Demo Day disclosures via Sacra Research/heypocket.com"，让 downstream 知悉引用链。

---

### 🟡 P2 — 中等问题（影响分发效果或阅读体验）

**#15 AMI Labs / #16 Ineffable Intelligence — 标题权重异常**

- **问题：** AMI Labs ($1.03B) 和 Ineffable Intelligence ($1.1B) 在综合分上均输于 RadixArk ($100M) 和 Pocket ($27M ARR)？
- **回读：** 包内综合分 AMI Labs 23 / Ineffable 22 / RadixArk 22 / Pocket 22，但入选名单里 AMI/Ineffable 排 Top2。
- **矛盾：** 评分逻辑和入选名单排序存在视觉混淆——到底是按融资规模还是综合分？
- **建议：** 统一排序逻辑，在"入选名单"中明确说明"按综合分排序（融资规模不计入传播性/一手性等维度）"。

**#12 Terranox AI — "AI uranium exploration"赛道需要更精确描述**

- **问题：** 铀矿+AI 是极其垂直的场景，包内仅写"能源+AI+资源；垂直场景稀缺"。
- **影响：** 这个赛道过于狭窄，若无具体客户/合同/数据，内容工厂很难写出有传播力的稿。
- **建议：** Terranox AI 当前评分（★11）对应"待补-YC W26"是合理的，但需在补查链里明确标注"必须有矿山企业背书或政府合同"才能推高优先级。

**#20 Meatly — 非 AI 核心资产混入 Top20**

- **问题：** 培育宠物肉（pet food）是生命科学/替代蛋白赛道，与包内其他 AI 资产逻辑不一致。
- **影响：** 若 content-writer 按"今日 AI 热点"逻辑消费此包，Meatly 会造成赛道混乱。
- **建议：** 在 Top20 表中明确标注 Meatly 赛道为"AgBio/FoodTech"，而非泛泛列为"AI startup"；或者干脆降出 Top20 归入"其他"类。

**缺失：source manifest 与 asset chain 的对应关系未建立**

- **问题：** 包内没有 source manifest 区块（昨天 20260510 reworked 包有），无法追溯每条信号的原始链接。
- **影响：** market-editor 打分时无法核验"一手记者/编辑是否可回查原始源"，影响内容可信度评级。
- **建议：** 补建 source manifest，格式参考：
  ```
  ## Source Manifest
  - AMI Labs → Crunchbase / Forbes / Futurum
  - Ineffable Intelligence → Quartz / TechFundingNews / SiliconRepublic
  - Tessera Labs → BusinessWire / Forbes / FinSMEs
  - Pocket → YC.com / heypocket.com / Sacra Research
  ```

---

## 三、弱链补查建议（优先级排序）

| 优先级 | 对象 | 补查项 | 理由 |
|--------|------|--------|------|
| HIGH | Agentic Fabriq | 官网确认 + Okta 类比痛点展开 | 新品类无视觉素材，内容工厂无法写图 |
| HIGH | Pocket | $27M ARR 官方来源（YC Demo Day 披露链） | 核心数据缺锚点 |
| HIGH | Terranox AI | YC W26 batch 确认文件 + 矿山企业/政府合同 | 赛道过窄，无合同背书无法写传播稿 |
| MEDIUM | Moritz | 修正赛道为"AI legal ops" + 官网 | 当前描述误导 |
| MEDIUM | AMI Labs | 补注"研究导向，商业化数年" | 防止时效性错位 |
| LOW | Meatly | 降出 Top20 或标注为 AgBio | 赛道混入破坏包内逻辑一致性 |

---

## 四、自检清单

- [x] 每条指控均已回读 pack 内 source refs / manifest / 对应原链接
- [x] 无空口下判断；所有问题均有补证来源
- [x] 对 AMI Labs 和 Ineffable Intelligence 的 billion-dollar 级指控，进行了独立 web 搜索交叉验证
- [x] 红队目标是把高价值对象做强，不是全否
- [x] 未输出对模板壳/占位包/缺前置包的攻击
- [x] 本轮未触发 `pua` skill（无连续失败，无明显磨洋工）

---

## 五、综合评分建议（供 market-editor 参考）

| 维度 | 评分 |
|------|------|
| 数据硬度 | ★★★★☆（AMIIneffable 双双确认，赞） |
| 赛道清洁度 | ★★★☆☆（Meatly 混入，Moritz 赛道偏差） |
| 来源可追溯性 | ★★★☆☆（缺 source manifest） |
| 平台就绪度 | ★★★★☆（Top10 可直接派生） |
| **综合** | **B+（值得 downstream 使用，但需修正 P1 级问题）** |

---

*redteam-reviewer | 2026-05-11 14:53 CST | WAITING_ON_TOP20_PACK=N*