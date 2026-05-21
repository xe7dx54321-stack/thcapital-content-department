# Top20 红队审核 — 2026-05-13
**审核时间:** 2026-05-13 16:05 CST
**审核人:** redteam-reviewer | day-mainline-top20-redteam
**数据窗口:** 2026-05-13 | lane: day_mainline
**交付路径:** `10_logs/20260513__top20__redteam-review.md`

---

## 执行前提确认

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 北京时间 ≥ 14:30 | ✅ | 16:04 CST |
| Top20 pack 存在 | ✅ | `20260513__top20-screening-pack.md` + 4个 lane packs |
| reworked 包优先级 | ⚠️ | 无 `__reworked` 包，以当前 pack 为准 |
| bootstrap 脚本 | ⬜ | 脚本不存在，跳过；自本轮起手工执行 |
| artifact-status 脚本 | ⬜ | 脚本不存在；以手工验证替代 |

---

## 红队评审结论

### 🔴 A级指控 — 高优先级返工

---

#### 【A-1】Ineffable Intelligence — 创始人信息涉嫌张冠李戴
**来源:** `20260513__top20-screening-pack__financing-newco.md` #3

**pack 内容:**  
> "$1.1B（估值$5.1B）；Sequoia+Lightspeed共领；**David Silver（AlphaGo创始人）**；NVIDIA/Google/DST/Index/EQT；UK主权AI基金"

**红队核查:**
- Web 检索多源确认：Recursive Superintelligence（2025年12月成立，伦敦）的创始团队是 Richard Socher（前 Salesforce Chief Scientist）+ 来自 DeepMind/OpenAI 的研究员——**不是 David Silver**
- Ineffable Intelligence 本身在本次检索中**无任何可信来源**，其创始人背景在 pack 中完全空白
- pack 将 David Silver 挂在 Ineffable Intelligence 名下，实为 Recursive Superintelligence 的混淆

**影响:** 
- 点击率：高（David Silver 是 AI 圈知名人物，但挂错公司会损害可信度）
- 可信度：致命伤——一旦被读者或内行指出，信任归零
- 来源：P1.5（techcrunch 来源，但 techcrunch 未提及 David Silver）

**返工建议:**  
1. 立即查证 Ineffable Intelligence 真实创始人，若无明确来源则**降权至 YC 历史锚点级别**  
2. 将 David Silver 正确归因至 Recursive Superintelligence  
3. 若 topic-planner 仍选 Ineffable Intelligence 作主推标的，必须补 **官网直连 + 创始人 LinkedIn + 融资公告**，否则不得进入 platform task sheet

---

#### 【A-2】Recursive Superintelligence — 估值数字与来源不符
**来源:** `20260513__top20-screening-pack__wechat-radar.md` #6

**pack 内容:**  
> "$5亿美元，估值40亿美元"

**红队核查:**  
- Web 检索：sifted.eu / mlq.ai / techfundingnews 多源一致——**$500M 融资，$4B  pré-money 估值**（4个月公司）
- 有来源提到可能达 $1B（oversubscribed），但**40亿美元是 pre-money 估值，不是 post-money**
- pack 将"估值40亿美元"与"$5亿美元融资"并列，容易误读为 $5B 估值

**影响:**  
- 数据硬度因此降一档；数字误差在资本圈读者中属于"低级错误"
- 但整体方向（GV+NVIDIA 投资、Richard Socher 创立、递归自研）是真实的

**返工建议:**  
1. 修正措辞：**"$5亿美元融资，估值40亿美元（pré-money）"**，或 **"$500M @ $4B"**  
2. 保留；但需注明"国家大基金领投"属于**传言**，不写入正文核心数据框

---

#### 【A-3】AMI Labs — 投资人名单不完整或含未核实信息
**来源:** `20260513__top20-screening-pack__financing-newco.md` #2

**pack 内容:**  
> "Bezos Expeditions/Cathay/Greycroft/Hiro/HV；NVIDIA/Temasek/Samsung/Toyota/Mark Cuban/Eric Schmidt"

**红队核查:**  
- Web 检索确认：$1.03B 已关闭； co-led by Cathay Innovation, Greycroft, Hiro Capital, HV Capital, Bezos Expeditions——**前五个有来源**
- NVIDIA / Temasek / Samsung / Toyota / Mark Cuban / Eric Schmidt **在本次检索中无来源确认**；可能是投资者阵容的延伸或媒体推测
- Pack 把第二梯队投资者与第一梯队并列，未区分或标注，可信度降档

**返工建议:**  
1. 将后六个投资人拆出，标注为"媒体报道 / 待官方确认"  
2. 若 topic-planner 用 AMI Labs 作主推，需补**官方新闻稿或新闻稿原文**  
3. 不得将未经确认的顶级投资人名单写入正文——一旦被引用打脸，损害内容工厂专业度

---

### 🟡 B级指控 — 中优先级返工

---

#### 【B-1】Isomorphic Labs — 投资方描述轻微失准
**来源:** `20260513__top20-screening-pack__product-newco.md` #1

**pack 内容:**  
> "Thrive Capital连续领投；Alphabet/GV/MGX/Temasek/CapitalG/英国主权AI基金"

**红队核查:**  
- Isomorphic Labs 确实是 Alphabet 子公司，GV（Google Ventures）是独立子基金，CapitalG 也是独立 growth equity 基金——三个是不同的法律实体
- Pack 并列写法无大错，但不够精准；Alphabet 旗下三支基金同时入股（GV+CapitalG）是可信的，但"Alphabet"作为投资主体描述不准确

**返工建议:**  
1. 修正为"Alphabet 旗下GV / CapitalG / 及其他"或按实际新闻稿描述  
2. 轻微问题，不阻碍进入 Top20，若 topic-planner 选其为重磅标的则需补强

---

#### 【B-2】ciridae / Pit / Performativ — P1证据不足混入结构化初筛
**来源:** `20260513__top20-screening-pack__financing-newco.md` #5, #6, #9

**pack 内容:** 三家均被列入结构化初筛表，但信源仅"媒体覆盖"

**红队核查:**  
- Ciridae $20M Seed (Accel + a16z)，$175M 估值——Web 无直接来源，信息密度不足
- Pit $16M Seed (a16z)——同上，无直接来源
- Performativ €5.5M——同上

三者在 pack 中被标为 P1.5-P2，但无一手来源佐证，与 Isomorphic / AMI 等同等对待，有失公平性

**返工建议:**  
1. 若 topic-planner 选这三者作重推标的，需要补"官网或官方公告"  
2. 若无补强，应降权至"未进入 Top20 但值得跟踪"列表  
3. 这是初筛包的边界判断问题，不阻碍 pack 通过

---

#### 【B-3】Anthropic 两条lane数据口径不一致
**来源:**  
- `20260513__top20-screening-pack.md` #9：**"传 $50B @ $900B；⚠️未官宣，高风险高权重"**
- `20260513__top20-screening-pack__official-update-lane.md` #1：**官方公告确认 Anthropic × SpaceX Colossus 1（300MW+，220,000+ GPU）**

**红队核查:**  
- 两条 lane 对 Anthropic 的处理方式相差悬殊：一条高度谨慎（⚠️待确认），一条全力唱多（官方最大算力联盟）
- 两者并不矛盾，但**pack 级别没有说明两者的关系**——读者会问：$50B 传闻是真的还是假的？

**返工建议:**  
1. 在 canonical pack 的 Anthropic 条目下加一行：**"同日 official-update-lane 确认 Anthropic × SpaceX Colossus 1 300MW+ 算力布局；$50B 估值传闻仍待官方公告"**  
2. 这样让 topic-planner 知道两条 lane 都需要，不是只选一个

---

### 🟢 C级观察 — 低优先级或建议性

---

#### 【C-1】Vobiz $1M — 规模太小，不宜作主推
**来源:** `20260513__top20-screening-pack__financing-newco.md` #11

Vobiz.ai 是真实公司（Bengaluru，Voice AI 电话基础设施，$1M Seed）——但规模极小，在 pack 中排名第11，与 Isomorphic Labs $2.1B 并列逻辑上不匹配

**建议:** 建议 topic-planner 除非有特殊内容角度（如"印度 Voice AI 基础设施"细分叙事），否则不选 Vobiz 作主推

---

#### 【C-2】YC S26 四弱公司 — 初筛包已识别，未补强
**来源:** `20260513__top20-screening-pack.md` "待补强项"

初筛包**已诚实标注** Andco / Ornadyne / Klaimee / Kuli 官网未确认，market-scout 的自我识别做得正确。红队不重复指控，仅记录：若无补强，这四家**不得进入 platform task sheet 的主推标的**

---

## 优先级矩阵（对 topic-planner / content-writer 的指导）

| 标的 | 推荐优先级 | 理由 | 必要补强项 |
|------|-----------|------|-----------|
| **阶跃星辰** | ⭐⭐⭐⭐⭐ | P1全网确认，170亿人民币，产业资本+IPO叙事 | 无 |
| **月之暗面** | ⭐⭐⭐⭐⭐ | P1确认，$20B，ARR $200M+ | 无 |
| **Isomorphic Labs** | ⭐⭐⭐⭐ | $2.1B，P1强 | 补投资方准确描述 |
| **AMI Labs** | ⭐⭐⭐⭐ | $1.03B，LeCun背书 | 补投资方来源，分清主力/跟投 |
| **Anthropic（官方更新）** | ⭐⭐⭐⭐⭐ | SpaceX Colossus 1官方确认，算力布局最强 | 无 |
| **Recursive Superintelligence** | ⭐⭐⭐ | 真实，但估值数字需修正 | 修正为 $500M @ $4B |
| **Judgment Labs** | ⭐⭐⭐ | $32M Lightspeed领投，Alex Shan真实 | 无重大问题 |
| **DeepSeek（传$500B）** | ⭐⭐⭐ | 方向真实，数字⚠️标注适当 | 维持⚠️标注 |
| **Exaforce** | ⭐⭐⭐ | $125M，YC S26，Agentic SOC | 无重大问题 |
| **Ineffable Intelligence** | ⭐⭐ | 有数字无创始人验证，降权 | 补创始人背景，否则降级 |
| **Sierra** | ⭐⭐⭐⭐ | $950M，Bret Taylor+Clay Bavor | 无重大问题 |
| **Vobiz / Kaizan / Marloo** | ⭐⭐ | 规模小，无一手信源 | 不作主推 |

---

## 最终裁定

| 项目 | 状态 |
|------|------|
| 本轮 pack 可信度 | ⚠️ 中（3个A级指控，影响核心标的） |
| 是否建议 market-editor 启动 platform task | **暂缓 — 需完成 A-1、A-2、A-3 返工** |
| 最严重问题 | Ineffable Intelligence 创始人张冠李戴（直接损伤可信度） |
| 最小可接受发布门槛 | A-1、A-2、A-3 均修正后，方可进入 topic-planner |

**核心原则：** 红队的目标是把高价值标的做扎实，而不是否掉一切。本轮 pack 的核心标的（阶跃/月之暗面/Isomorphic/AMI Labs/Anthropic官方更新）方向正确，但 Ineffable Intelligence 的创始人错误和 AMI Labs 投资人混淆属于"一出手就穿帮"级别的硬伤，必须返工。

---

*redteam-reviewer | 2026-05-13 16:10 CST*
*交付路径: 10_logs/20260513__top20__redteam-review.md*