# Asset Chain — market-scout | 2026-05-10（第二轮派生）

**Runtime:** market-scout
**Date:** 2026-05-10（派生时间 13:19 UTC）
**触发:** cron — 一跳派生（trend__yc_launches_ai / web__techcrunch_ai / web__finsmes_ai_gnews）
**目标:** 把当天融资/newco入口补成对象链：官网/社交/demo/docs/repo；若无硬链则生成查询链

---

## 执行摘要

| Source Packet | 对象数 | [HARD] | [HARD via YC] | [QUERY] | 说明 |
|---------------|--------|--------|----------------|---------|------|
| trend__yc_launches_ai | 11 | 2 | 6 | 3 | 部分为S26非W26；Motion/Pace存在名称混淆 |
| web__techcrunch_ai | 7 | 7 | 0 | 0 | 全部为已知成熟公司；均已命中官网 |
| web__finsmes_ai_gnews | 3 | 3 | 0 | 0 | Sakana/Berget/Gushwork均已命中官网 |
| **合计** | **21** | **12** | **6** | **3** | |

> 本轮21个对象中，18个（85.7%）已升级为 [HARD] 或 [HARD via YC]；3个保留为 [QUERY]（Motion/Paceconfusion + Pavoot batch归属问题）。

---

## 详细派生结果

### 📦 trend__yc_launches_ai

---

#### 1. Beacon Health — AI agents for primary care

| 字段 | 值 |
|---|---|
| **YC页** | https://www.ycombinator.com/companies/beacon-health |
| **YC Launch页** | https://www.ycombinator.com/launches/POy-beacon-health-ai-agents-for-primary-care |
| **产品官网** | 未找到独立官网 |
| **产品** | AI employees自动化初级保健行政工作流（EHR集成、prior auth/referrals/risk adjustment） |
| **创始人** | Mark Pothen、Obinna |
| **已落地** | 40,000患者独立医师协会已上线 |
| **定位** | 解决基层医生行政过载问题；"bring joy back to primary care" |
| **标注** | **[HARD via YC]** YC Launch页有完整产品描述；医疗AI行政自动化 |

---

#### 2. Lucid — AI workflow orchestration

| 字段 | 值 |
|---|---|
| **YC页** | https://www.ycombinator.com/companies/lucid |
| **公司官网** | https://lucid.so（注意：与Lucid Software的lucid.co无关联） |
| **产品** | AI workflow orchestration — 多agent编排/企业级工作流自动化 |
| **区分** | 与Lucid Software（lucid.co，图表协作工具）完全不同；独立YC公司 |
| **标注** | **[HARD via YC]** YC页+独立官网；W26 batch明确方向 |

---

#### 3. Motion — AI project management

| 字段 | 值 |
|---|---|
| **YC页** | https://www.ycombinator.com/companies/motion |
| **现状** | 实际为YC W20 batch公司（2019年），非W26新成员 |
| **官网** | https://www.usemotion.com/ |
| **产品** | AI work management platform — 任务/项目/日历统一管理；human+AI employees |
| **规模** | 65名员工，活跃运营 |
| **创始人** | Harry Qi、Omid Rooholfada |
| **问题** | source packet将W20历史公司混入W26 batch，存在误标注 |
| **标注** | **[QUERY]** — 名称存在，但非W26新Entry；来源packet存在混淆 |

---

#### 4. Pace — AI insurance automation（与YC W26 "Balance" 名称混淆）

| 字段 | 值 |
|---|---|
| **公司** | Pace — AI驱动的保险业运营自动化 |
| **YC页** | YC W26 batch中无"Pace AI accounting"；实际对应为"Balance" |
| **官网** | 未找到ycombinator.com/companies/pace对应的保险AI公司 |
| **融资** | $10M Series A，Sequoia Capital领投 |
| **产品** | AI agents处理保险业BPO任务（submission intake/policy servicing/claims） |
| **对比** | Balance（ycombinator.com/companies/getbalance）为YC W26 AI会计公司 |
| **问题** | source packet中"Pace"与实际YC W26的"Balance（AI accounting）"存在名称混淆 |
| **标注** | **[QUERY]** — 存在$10M Sequoia融资公司Pace，但非YC W26；source packet描述与实际不符 |

---

#### 5. Hyper — "self-driving company brain"

| 字段 | 值 |
|---|---|
| **YC页** | https://www.ycombinator.com/companies/hyper-4 |
| **Batch** | YC Spring 2026（S26），非W26 |
| **官网** | hyper.ai（未独立确认，但YC页存在） |
| **产品** | AI平台：默默学习公司Notion/Slack/Google Drive数据→实时共享知识库→AI工具越用越聪明 |
| **创始人** | Shalin Shah（UC Berkeley EECS，前MaticRobots autonomy lead）、Kanyes Thaker（UC Berkeley，前Snorkel AI founding data engineer） |
| **信号** | Forbes 21 most promising YC S26 startups |
| **标注** | **[HARD via YC]** YC页可查；S26非W26；AI记忆/知识管理赛道 |

---

#### 6. Pavoot — AI event marketing agent

| 字段 | 值 |
|---|---|
| **YC页** | https://www.ycombinator.com/companies/pavoot |
| **官网** | https://pavoot.com/ |
| **Batch** | YC Spring 2026（S26），非W26 |
| **产品** | AI agent：会前识别高转化潜客→会中智能对接→会后个性化跟进+CRM集成 |
| **创始人** | Gohar Tamrazyan（6次瑞士象棋冠军）、Ana Yoon Faria de Lima（20+科学奥赛奖牌AI工程师） |
| **视频** | https://www.youtube.com/watch?v=SvJtGNtOS50 |
| **标注** | **[HARD]** 官网+YC页+YouTube三链；S26非W26；活动营销AI垂直 |

---

#### 7. Clawvisor — AI agent security/authorization layer

| 字段 | 值 |
|---|---|
| **YC页** | https://www.ycombinator.com/companies/clawvisor |
| **官网** | 未找到独立官网（仅有YC页） |
| **产品** | AI agent与Gmail/Slack/Google Drive之间的安全授权层；防"rogue AI"；实时策略执行；凭证金库 |
| **创始人背景** | 前Berbix联合创始人（S18，被Socure收购）；Airbnb Trust & Safety；Y Combinator Visiting Group Partner |
| **标注** | **[HARD via YC]** YC页有完整安全机制描述；AI agent安全基础设施 |

---

#### 8. ANORIA — Emotion-reading wearable (EQ bracelet)

| 字段 | 值 |
|---|---|
| **YC页** | https://www.ycombinator.com/companies/anoria |
| **Batch** | YC Spring 2026（S26），非W26 |
| **产品** | 手环读情绪→输出"Flow Score"（能量/心情/专注度量化）；EQ训练设备 |
| **创始人** | Michael Belhassen（前Apple iPhone 17 Pro外壳设计负责人，solo founder→5人团队 Apple/Meta背景） |
| **定位** | 情绪量化赛道；Apple前硬件专家创业；硬件+AI结合 |
| **标注** | **[HARD via YC]** YC页可查；S26非W26；情绪可穿戴新赛道 |

---

#### 9. Rudus — AI for construction (concrete takeoffs)

| 字段 | 值 |
|---|---|
| **YC页** | https://www.ycombinator.com/companies/rudus |
| **Batch** | YC Spring 2026（S26），非W26 |
| **产品** | AI分析建筑蓝图→自动生成材料清单和项目估算 |
| **创始人** | Sahil Goel、Rishi Pankhaniya |
| **定位** | 建筑AI；$175B construction tech市场 |
| **标注** | **[HARD via YC]** YC页可查；S26非W26；建筑科技垂直 |

---

#### 10. Zibra Labs — HPC for quantitative trading

| 字段 | 值 |
|---|---|
| **YC页** | https://www.ycombinator.com/companies/zibra-labs |
| **Batch** | YC Spring 2026（S26），非W26 |
| **产品** | 大规模HPC集群→并行运行数百万backtest任务→解决量化策略回测瓶颈 |
| **创始人** | Zac Policzer、Ibrahim Rabbani |
| **区分** | Zibra AI（乌克兰，游戏3D资产生成，a16z Speedrun）是另一家公司 |
| **标注** | **[HARD via YC]** YC页可查；S26非W26；量化金融基础设施 |

---

#### 11. Pace（独立记录）— Insurance AI automation

| 字段 | 值 |
|---|---|
| **官网** | 未找到（融资信息来源于tech/news） |
| **融资** | $10M Series A；Sequoia Capital领投 |
| **产品** | AI agents替代保险业BPO（承保录入/保单服务/理赔处理） |
| **媒体** | fintech.global / ffnews.com 报道 |
| **标注** | **[QUERY]** — 真实公司+$10M Sequoia背书，但无独立官网锚点；非YC W26 |

---

### 📦 web__techcrunch_ai

---

#### 12. xAI — $20B Series E（Jan 2026）

| 字段 | 值 |
|---|---|
| **官网** | https://x.ai/ |
| **总融资** | $42.7B（含历史轮次）；Elon Musk公司 |
| **标注** | **[HARD]** 成熟已知实体 |

---

#### 13. OpenAI — $122B round（Mar 2026）

| 字段 | 值 |
|---|---|
| **官网** | https://openai.com/ |
| **估值** | $852B；SoftBank+Amazon共同领投；Amazon成为exclusive第三方云伙伴 |
| **标注** | **[HARD]** 成熟已知实体 |

---

#### 14. Shield AI — $1.5B Series G

| 字段 | 值 |
|---|---|
| **官网** | https://www.shieldai.com/ |
| **估值** | $12.7B；Defense AI / autonomous pilot |
| **标注** | **[HARD]** 成熟已知实体 |

---

#### 15. Nexthop AI — $500M Series B

| 字段 | 值 |
|---|---|
| **官网** | https://nexthop.ai/（已确认） |
| **总部** | Santa Clara；2024年成立 |
| **创始人** | Anshul Sadana（CEO） |
| **团队背景** | Arista Networks/Broadcom/Cisco/NVIDIA |
| **产品** | AI infrastructure for large-scale cloud operators |
| **标注** | **[HARD]** 官网已确认；AI网络基础设施 |

---

#### 16. Rhoda AI — $450M Series A

| 字段 | 值 |
|---|---|
| **官网** | https://www.rhoda.ai/ |
| **产品** | "FutureVision"平台：视频预测控制机器人；学习互联网视频而非遥操作演示 |
| **投资人** | Khosla Ventures + Temasek + Mayfield |
| **已落地** | 生产环境variable manufacturing workflows |
| **标注** | **[HARD]** 官网已确认；机器人基础模型新范式 |

---

#### 17. LMArena → Arena — $1.7B valuation

| 字段 | 值 |
|---|---|
| **官网** | https://arena.ai/（2026-01-28 rebranding from LMArena） |
| **前名** | Chatbot Arena / LMArena |
| **起源** | UC Berkeley研究项目 |
| **产品** | LLM公开评估平台；用户投票生成leaderboard |
| **客户** | AI labs + enterprises |
| **标注** | **[HARD]** 官网已确认；AI评估平台高估值 |

---

#### 18. Steno — $49M Series C

| 字段 | 值 |
|---|---|
| **官网** | https://www.steno.com/ |
| **产品** | "Transcript Genius"：对话式法律转录分析；找出关键证词/检测不一致/生成摘要 |
| **融资** | $49M Series C（Savano Capital Partners领投；First Round Capital + Legal Tech Fund跟投） |
| **模式** | Hybrid court reporting + AI（支持而非替代人类记录员） |
| **CEO** | Greg Hong |
| **标注** | **[HARD]** 官网已确认；法律科技AI |

---

### 📦 web__finsmes_ai_gnews

---

#### 19. Sakana AI — Mitsubishi Electric投资（2026-03）

| 字段 | 值 |
|---|---|
| **官网** | https://sakana.ai/ |
| **投资方** | Mitsubishi Electric（2026-03-30）；同时Google/Salesforce/Citi也在2026年投资 |
| **总部** | 东京；下一代基础模型 |
| **合作重点** | "Serendie"数字平台；将熟练工人隐性知识数字化；制造业/基础设施自动化 |
| **背景** | 2026年已获多家顶级机构投资；Clarivate AI50 2026 |
| **标注** | **[HARD]** 官网+多顶级投资方背书；日本AI基础模型 |

---

#### 20. Berget AI — €2.1M seed（2026-02）

| 字段 | 值 |
|---|---|
| **官网** | https://berget.ai/ |
| **总部** | 斯德哥尔摩；2024年成立 |
| **定位** | "AI sovereignty" — 瑞典本地托管AI推理/基础设施 |
| **投资人** | Luminar Ventures（领投）、Wellstreet、Norrsken Evolve |
| **资金** | SEK24M；用于扩大瑞典AI服务器基础设施 |
| **产品** | 基于开源模型；瑞典地下数据中心；EU AI Act合规 |
| **创始人** | Christian Landgren（企业家）、Andreas Lundmark（前BCG AI专家） |
| **标注** | **[HARD]** 官网已确认；欧洲数据主权AI |

---

#### 21. Gushwork AI — $9M seed（2026-02）

| 字段 | 值 |
|---|---|
| **官网** | https://www.gushwork.ai/ |
| **产品** | AI agents SEO+外链建设+潜客追踪→网站 inbound leads |
| **融资** | $9M seed（SIG+Lightspeed联合领投；B Capital/Seaborne/Beenext/Sparrow/2.2 Capital跟投） |
| **估值** | $33M seed |
| **指标** | $1.5M ARR；300+付费客户（主要美国）；2023年成立 |
| **总部** | Delaware注册；班加罗尔运营 |
| **创始人** | Nayrhit Bhattacharya、Adithya Venkatesh |
| **标注** | **[HARD]** 官网已确认；AI SEO/潜客获取 |

---

## 汇总：[HARD] 覆盖率

| 状态 | 数量 | 占比 |
|------|------|------|
| **[HARD] 官网/独立账号可查** | 12 | 57.1% |
| **[HARD via YC] YC公司页可查** | 6 | 28.6% |
| **[QUERY] 弱链保留** | 3 | 14.3% |
| **合计** | 21 | 100% |

---

## 关键发现

1. **YC batch归属问题（重要）**：source packet中的Pavoot/Hyper/Rudus/Zibra Labs/ANORIA 实际属于 **YC Spring 2026（S26）**，非 W26。可能原因：tldl.io合成时将S26信息混入，或YC尚未正式发布W26 batch。
2. **Motion = 历史公司**：Motion在YC W20（2019年）已出现，65人公司持续运营，非W26新Entry。
3. **Pace名称混淆**：Pace是保险AI运营公司（$10M Sequoia），非YC W26 AI accounting（真实对应为"Balance"）。
4. **Pavoot独立官网确认**：pavoot.com存在，产品完整（S26非W26）。
5. **Clawvisor**：AI agent安全授权层，前Berbix创始人，差异化明确。
6. **ANORIA**：Apple前硬件专家创业，情绪可穿戴新硬件赛道。
7. **LMArena → Arena**：已完成 rebranding，2026-01-28；$1.7B valuation。

---

## 本轮信号强度更新（建议 topic-planner 关注）

| 公司 | 赛道 | 信号强度 | 优先级 |
|------|------|---------|--------|
| Rhoda AI | 机器人基础模型 | HIGH | $450M + Khosla/Temasek/Mayfield |
| Nexthop AI | AI网络基础设施 | HIGH | $500M + ex-Arista/NVIDIA团队 |
| Steno | 法律科技AI | MEDIUM-HIGH | $49M + Transcript Genius |
| LMArena→Arena | AI评估平台 | MEDIUM-HIGH | $1.7B valuation rebranding |
| Sakana AI | 基础模型 | HIGH | Google/Salesforce/Citi/Mitsubishi四重背书 |
| Berget AI | 数据主权AI | MEDIUM | €2.1M + EU AI Act合规 |
| Clawvisor | AI安全基础设施 | MEDIUM-HIGH | YC背书 + Berbix创始人背景 |
| Gushwork AI | SEO AI | MEDIUM | $9M + $1.5M ARR |

---

## 执行记录

- **派生时间:** 2026-05-10 13:19 UTC
- **源Packet:** trend__yc_launches_ai / web__techcrunch_ai / web__finsmes_ai_gnews
- **对象总数:** 21
- **升级为 [HARD]:** 12
- **升级为 [HARD via YC]:** 6
- **保留 [QUERY]:** 3（Motion / Pace混淆 / Pavoot batch归属）
- **写入路径:** `02_topic_radar/asset_chains/20260510__asset-chain__derivation-round-2.md`
- **虚拟VC运行台写入:** 无

---

*market-scout runtime | 2026-05-10 | 一跳派生轮次 | 21 objects processed | 18 upgraded to HARD | 3 QUERY retained*