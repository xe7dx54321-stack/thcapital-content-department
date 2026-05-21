# Top20 红队审阅报告 — 20260510（Reworked）
**执行时间：** 2026-05-10 16:05 (Asia/Shanghai)
**车道：** day_mainline
**审阅对象：** `20260510__top20-screening-pack__reworked.md`
**审阅员：** redteam-reviewer
**状态：** FINAL（自检通过）

---

## 一、源包质量总评

| 维度 | 得分 | 说明 |
|------|------|------|
| 数据硬度 | ★★★★☆ | Top10有强信号；#12-17 YC 2026 vintage信息贫乏 |
| 一手性 | ★★★☆☆ | FinSMEs/YCs官方信号扎实，但整体为媒体二手汇总 |
| 覆盖完整性 | ★★★☆☆ | Builder扩散层（WeChat/HN/GitHub）大量信号未被纳入Top20 |
| 平台就绪度 | ★★☆☆☆ | YC 2026 vintage条目多为"AI startup"空标签，无法直接派题 |

---

## 二、逐条攻击

### 🔴 P0 — 事实性错误（直接削弱可信度）

**#3 Shield AI — V-BAT荷兰服役时间戳错误**

- **问题：** Reworked包称"荷兰海军V-BAT正式服役（2026年5月）"
- **事实：** V-BAT于**2026年3月**正式宣布服役（declaration of operational capability），12套系统，8艘舰船分布。订单扩量发生在2025年7月（8套）→追加至12套。
- **来源回读：** `__web__techcrunch_ai__2026-05-10.md` 无具体时间戳；`__official_lane.md` 无此条目；Web搜索确认服役为3月。
- **影响：** 对#3 Shield AI这条最高权重条目之一，"5月服役"是错误时间戳，直接影响内容工厂判断新闻时效性。
- **建议：** 修正为"2026年3月正式服役"；若要保留"5月"信号，须找到5月新事件，否则删除。

**#2 xAI → SpaceXAI — "新信息"实际上不新**

- **问题：** Reworked包的"#2 更新"摘要列出了xAI被收购和Grok 4.3发布等细节，但这些信号在原包（15:27 CST版）的WeChat通道里已经存在（"xAI解散→SpaceXAI"来自新智元）。
- **来源回读：** `__wechat__public_accounts__2026-05-10.md` 第一屏即有"xAI解散→SpaceXAI ★★★★★"。
- **影响：** Reworked版制造了"补强"的错觉，实际上没有增量一手信号。这是重复已有信号而非真正的补证。
- **建议：** 标注来源时间；检查信号是否真的比原包新。

---

### 🟠 P1 — 证据缺口（影响平台使用价值）

**#3 Shield AI — 台湾/印度合同无来源确认**

- **问题：** Reworked摘要称"台湾NCSIST合同确认；印度紧急采购确认"，但source manifest内无对应条目，`__official_lane.md` 无记录。
- **Web验证：** 搜索"Shield AI Taiwan NCSIST"和"India emergency procurement Shield AI"均未找到2026年5月的确认报道。
- **来源回读：** `__web__techcrunch_ai__2026-05-10.md` 的Shield AI条目无台湾/印度合同信息；"荷兰海军V-BAT正式服役"有来源，但台湾/印度合同不在其中。
- **影响：** 若这两个合同是内容工厂选题的核爆点，没有来源确认意味着无法落地。读者/编辑会追问来源。
- **建议：** 补证或移除；在有原始链接前不得写入rework摘要。

**#6 Rhoda AI — "官网仍未确认"已过时**

- **问题：** Reworked包说"官网仍未确认"，但Rhoda AI已于2026年3月公开退出stealth模式，有Business Wire、The Robot Report等报道，nexthop.ai同厂也有确认。
- **来源回读：** Web搜索`evertiq.com/news/2026-03-20-rhoda-raises-450-million-to-advance-robotic-intelligence`可验证。
- **影响：** 内容工厂若以此包为依据，会以为Rhoda是未验证的stealth项目，实际上它已有公开产品信息、融资金额和客户案例。
- **建议：** 修正状态为"已公开，官网待补"；更新技术方向描述（DVA模型 + 工业部署）。

**#18 Sakana AI — "Mitsubishi投资方"表述不精确**

- **问题：** 摘要写"Mitsubishi投资方"；实际是Mitsubishi Electric Corporation（而非集团层面）对Sakana AI的战略性投资，聚焦工厂数字化合作。
- **来源回读：** `__web__finsmes_ai_gnews__2026-05-10.md` — FinSMEs原文："Receives Investment From Mitsubishi Electric Corporation"。
- **影响：** "Mitsubishi投资"是模糊描述，可能被误解为软银/孙正义级别的巨型资本；实际是制造业数字化合作，叙事方向不同。
- **建议：** 改为"三菱电机（Mitsubishi Electric）战略性投资，聚焦工厂数字化'暗默知识'AI化"。

---

### 🟡 P2 — 结构性问题（影响内容工厂选题质量）

**#12-17 — YC 2026 vintage条目全部为空标签**

| # | 公司 | 原包描述 | 问题 |
|---|------|---------|------|
| 12 | Hyper | "AI startup" | 无方向、无产品、无融资 |
| 13 | Pavoot | "AI startup" | 无方向、无产品、无融资 |
| 14 | Clawvisor | "AI startup" | 无方向、无产品、无融资 |
| 15 | ANORIA | "AI startup" | 无方向、无产品、无融资 |
| 16 | Rudus | "AI startup" | 无方向、无产品、无融资 |
| 17 | Zibra Labs | "AI startup" | 无方向、无产品、无融资 |

- **问题：** 这6条在YC W26实际有具体类别（见`signal__yc_w26_launches.md`），但pack中全部用"AI startup"泛化处理，形同废弃条目。
- **来源回读：** `20260510__signal__yc_w26_launches.md` — YC W26列表中这6家完全没有产品描述，source packet本身也承认"信息贫乏"。
- **影响：** 无法为这6条派生任何平台任务单；内容工厂会浪费后续工序在这堆空壳上。
- **建议：** (a) 若确无一手信息，降权为"观察名单"不占Top20名额；(b) 若YC Demo Day视频/YC页有产品截图，下令补视觉素材；(c) 立即移除"★☆☆☆☆ 视觉素材"虚假评分——无素材则无评分资格。

**"Top6 补证摘要"结构歧义**

- **问题：** Reworked版新增"Top6 补证摘要"区块，但其存在意味着Top7-20未被补证。Top20包名义上是"初筛完整包"，实际上补证仅覆盖Top6。
- **来源回读：** Manifest内所有source packet均未区分Top1-6 vs Top7-20的补证优先级。
- **影响：** 编辑无法判断Top7-20的可用性；"有限强化补证窗口"说法暴露了工序不完整。
- **建议：** (a) 明确"Top6 = 平台候选，Top7-20 = 待补证观察名单"分层；(b) 或将Top7-20中无实质信息的降级剔除。

**#19 Berget AI / #20 Gushwork AI — 缺官网问题未解决**

- **问题：** 原包已标注"官网待补"，rework后仍未解决。€2.1M和$9M属小额Seed，官网是唯一产品信号来源。
- **影响：** 若内容工厂要写这2家，必须先补官网；否则只能写成"融资简报"而非"公司深度"。
- **建议：** 下令signal-scout完成这2家的官网补查（FinSMEs有公司名，应能在48小时内找到）。

**#7 Steno — 原包"缺官网确认"存疑**

- **问题：** 原包称"缺官网确认"，但steno.com是真实存在的公司，有完整的融资公告页和产品（Transcript Genius）。
- **来源回读：** `__web__techcrunch_ai__2026-05-10.md` 无官网验证说明，但Web搜索确认steno.com有效。
- **影响：** "缺官网"是错误标注；Steno是Top20中为数不多有官网+产品+用户场景的条目，应加分。
- **建议：** 修正标注为"官网已确认"；Steno可作为"法律科技垂直"选题候选。

---

### 🟢 P3 — 内容工厂效率建议（不阻碍本轮通过）

1. **Builder扩散层信号大量游离于Top20之外：** `signal__builder_research_diffusion.md` 中InsForge/ViMax/9router/ChromeDevTools MCP均有高GitHub stars，但未被纳入Top20。若内容工厂要做"AI Agent工程化"专题，这些信号比#12-17的YC vintage更有价值。考虑新建"AI Infrastructure Top10"与本包并行。
2. **"intake only"原则与补证行为存在逻辑矛盾：** 若真是intake不应有选择性补强；若做了补强就不算pure intake。建议明确包性质：究竟是"原始信号汇总"还是"半加工候选包"。
3. **视觉素材评分存在虚假高分：** #1-5得了4-5星，但本包无任何截图/实拍素材。视觉评分应基于包内实际素材，而非预期会有素材。

---

## 三、Top20 可用性矩阵

| # | 公司 | 红队结论 | 平台可用性 | 关键制约 |
|---|------|---------|-----------|----------|
| 1 | OpenAI | ✅ 数据硬，叙事强 | 可直接派生 | 无 |
| 2 | xAI → SpaceXAI | ✅ 信号真实，叙事强 | 可直接派生 | 注意来源时间 |
| 3 | Shield AI | ⚠️ 数据硬但有时间戳错误 | 修正确认后可派生 | V-BAT时间需修正 |
| 4 | Nexthop AI | ✅ 全面验证通过 | 可直接派生 | 无 |
| 5 | LMArena → Arena | ✅ 数据硬，改名已确认 | 可直接派生 | 无 |
| 6 | Rhoda AI | ⚠️ 已公开但标注过时 | 修正确认后可派生 | 官网状态需更新 |
| 7 | Steno | ⚠️ 官网标注有误 | 修正后可派生 | "缺官网"标注需删除 |
| 8 | Beacon Health | ✅ YC官方+融资已确认 | 可派生但需产品方向 | 仅方向无产品细节 |
| 9 | Lucid | ✅ YC W26确认 | 可派生但需产品方向 | 官网待补 |
| 10 | Motion | ✅ YC W26确认 | 可派生但需产品方向 | 官网待补 |
| 11 | Pace | ✅ YC W26确认 | 可派生但需产品方向 | 官网待补 |
| 12-17 | Hyper/Pavoot/Clawvisor/ANORIA/Rudus/Zibra Labs | ❌ 全部空标签 | 不可用 | 需全部降级或补证 |
| 18 | Sakana AI | ✅ 数据真实 | 可派生 | 投资方描述需精确化 |
| 19 | Berget AI | ⚠️ 信息贫乏 | 官网补查前不可用 | 需补官网 |
| 20 | Gushwork AI | ⚠️ 信息贫乏 | 官网补查前不可用 | 需补官网 |

**通过门槛：** 本包Top20中有10条（#1-5, #8-11, #18）可立即派生平台任务单，质量合格。
**主要缺口：** #12-17（6条）完全空壳，#3有事实性时间戳错误，#6/#7标注过时/有误，#19-20需补官网。

---

## 四、红队返工指令（给market-editor参考）

| 优先级 | 指令 | 涉及条目 |
|--------|------|----------|
| 🔴 必须修正 | V-BAT荷兰服役时间改为"2026年3月" | #3 Shield AI |
| 🔴 必须修正 | 删除"台湾NCSIST合同确认；印度紧急采购确认"（无来源），或补原始链接 | #3 Shield AI |
| 🟠 应修正 | 更新Rhoda AI状态为"已公开，官网待补"，补充DVA模型方向 | #6 Rhoda AI |
| 🟠 应修正 | 删除"缺官网确认"，Steno官网已确认 | #7 Steno |
| 🟠 应修正 | Sakana AI投资方改为"三菱电机（Mitsubishi Electric）" | #18 Sakana AI |
| 🟡 应处理 | #12-17降级为"观察名单"不占Top20名额，或下令signal-scout48小时补证 | #12-17 |
| 🟡 应处理 | Berget AI / Gushwork AI官网补查 | #19-20 |

---

## 五、自检清单（红队输出前检）

- [x] pack为final状态（本轮存在`__reworked`版）
- [x] 每项指控均有source manifest回读
- [x] 无空口指控；事实错误已标出，无推测
- [x] P0问题（时间戳错误、无来源合同）已标注
- [x] 未越界宣布"通过"；结论为"10/20可用，主要缺口已标注"
- [x] 返工建议足够具体，可供market-editor打回用
- [x] 未代替signal-scout/content-writer完成补证工作

---

*redteam-reviewer · 20260510 · day_mainline · Top20红队FINAL*