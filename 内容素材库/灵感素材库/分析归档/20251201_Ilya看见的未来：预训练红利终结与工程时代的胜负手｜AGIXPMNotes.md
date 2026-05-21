](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg2OTY0MDk0NQ==&action=getalbum&album_id=4022587657917186053&subscene=126&scenenote=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzg2OTY0MDk0NQ%3D%3D%26mid%3D2247514246%26idx%3D1%26sn%3Dde104fc02cb120d9180f47b22fa4a1ef%26chksm%3Dcf71d6a76892668cf18f007c4c9974e8d4c946ed18281f0143b7aedede4e175cc1910467c9ba%26scene%3D126%26sessionid%3D1750994837%26subscene%3D227%26clicktime%3D1750994839%26enterid%3D1750994839%26key%3Ddaf9bdc5abc4e8d03659350f1d5aeabe879f96bc6ba36414330ae668002f202b47d03b5db81c8b59665b83c1f8583ed968cbf8713d565f7013dadcb18b5804616bb5ce7883c006475ceef002b63ded413b8449bda249ab3abfe984c0cd65c1607e949c660fbedd2861c0575826fd540c6b63d48daf52d266776cd0faaf14674e%26ascene%3D78%26uin%3DMzQ2MTE3Mjg4MA%253D%253D%26devicetype%3DiMac%2BMacBookAir10%252C1%2BOSX%2BOSX%2B15.5%2Bbuild(24F74)%26version%3D13080a10%26nettype%3DWIFI%26lang%3Dzh_CN%26countrycode%3DCN%26fontScale%3D100%26exportkey%3Dn_ChQIAhIQMhoe%252BBPXgCBc6nwySTgX3RKGAgIE97dBBAEAAAAAAGgMKk7HoFYAAAAOpnltbLcz9gKNyK89dVj06DcmtrpDZoWdSCBGOPJA66XNCp0UFc4sLz7qtEx1hnlkVeDHNk5hV7vMNOzdOtOosagsHj5muxBVZo0sOecdPmNP3T7iq4eEBJ9X8vvAnUEDd%252BU8wlAOvWgruJkbS52o0iBCOyQ45RJfP3drPexeLSBfHBUSZHBVBCPfKhi6sGZTy3mF3BXImYm5%252B1TmA7S5HqP6Ok6uUJgKw1Hz195uSKSgWSfUqH9bE6kS8YXBTwekZedpRNiRexmlTSTerks4nboMfPDUUb%252ForaE%252FLMO9NUkzH83hgOjqBw2Q82p8WuY%253D%26acctmode%3D0%26pass_ticket%3DvgeInrhLtYDDMndp7X7xyCAaYKDLCCE2DQ0Rvt2WjIeLFFGTYjZOw1iLHrrMxp7c%26wx_header%3D0%26fasttmpl_type%3D0%26fasttmpl_fullversion%3D7794116-zh_CN-zip%26fasttmpl_flag%3D1&nolastread=1&uin=&key=&devicetype=iMac+MacBookAir10%2C1+OSX+OSX+15.5+build(24F74)&version=13080a10&lang=zh_CN&nettype=WIFI&ascene=78&fontScale=100)

AGIX 指数诞生于我们对“如何捕获 AGI 时代 beta 和 alphas”这一问题的深度思考。毫无疑问，AGI 代表了未来 20 年最重要的科技范式转换，会像互联网那样重塑了人类社会的运行方式，我们希望 AGIX 成为衡量这一新科技范式的重要指标，如同 Nasdaq100 之于互联网时代。

  是我们对 AGI 进程的思考记录，希望通过学习 Warren Buffett、Ray Dalio、Howard Marks 等传奇投资者们的分享精神，与所有 AGIX builders 一同见证并参与这场史无前例的技术革命。

PM Notes

What Ilya sees

作者：Max

Ilya 上周接受的采访应该是市场讨论最多的话题，虽然之后不得不像 Andrej Karpathy 一样特意澄清自己并不是在说模型训练撞墙，当前范式下仍然能够继续提升模型能力，以免太多经济利益攸关的人给他戴上对行业不负责任的帽子。但模型短暂停滞，或至少 OpenAI 预训练停滞是房间里的大象，若干核心人员在夏天离职加入 META 或单独创立公司已经相当于在用实际行动行使对 OpenAI 的看跌期权，这点不言而喻。同时，我们也看到 Gemini 3 能力的高歌猛进，尤其 Google 产品和模型能力同步提升，Nano Banana 和 NotebookLM 的 PPT 生成能力给了用户第一次使用 ChatGPT 的惊艳感觉。

这一矛盾的原因在于 AI 行业正在从发现新大陆（预训练大爆发）的科研红利期，转入深耕细作（产品化、推理优化、端侧部署）的工程红利期。而 Google 由于 TPU 的 OCS 技术。这使得一个 TPU Pod（包含数千个芯片）在逻辑上表现得就像一块巨大的单一芯片。所以 Google 可以把 1M token 的 KV Cache 极其丝滑地摊大饼在几千个 TPU 核上，而计算注意力时，芯片间的通信几乎不会造成像 GPU 集群那样的阻塞。NotebookLM 这类第一方产品基本上可以紧耦合在这些内部 infra 上，而 OpenAI 和 Nvidia 的产品更像是分层的优化和松耦合，所以在进入极致工程化竞争的时候，Google 就释放出了巨大的潜力。简而言之，就是模型-硅的端到端优化能力是决定下一阶段胜负的关键，OpenAI 当然也有这样的打算，只是需要时间和成本。

但这样的图景也并不为惧，并不是说 OpenAI 没有未来或 Google 一定能够奠定胜局，因为并不存在一个模型通吃所有场景的未来。这可以有两个角度来解读：对于普通用户，当模型越来越趋近前沿，普通用户的感知也就越来越弱，或者模型对于 90%用户的区分度就越来越不明显。在普通用户这里，模型是显而易见的无区分度的商品。最终胜出的是产品化能力和成本，渠道等等外部要素。比如 DOS/Windows 的胜利并非因为它们在技术上最先进（它们往往不是），而是因为微软在分发渠道（Distribution）、兼容性（Compatibility）和生态系统（Ecosystem）上做出了极其正确的战略选择。对于未来的判断极其重要，就像 IBM 当年的失误，以为软件是附件而硬件是核心价值，没想到硬件很快变为了无区分度的商品，造成了 IBM 的大溃败。

而对于复杂用户，或者如果我们相信以后是前 10%的用户消耗了 90%的 token，模型对于他们来讲更像是一个系统。就好像顶尖的程序员已经在同时使用 Codex，Claude Code，Gemini 和 Cursor 等等，不同的模型由于 Ilya 所说锯齿状的智能，各擅其场。所以在平台级玩家（更有可能是云公司或企业 AI OS 公司）的辅助下，综合各个模型的能力，把 AI 模型的使用从单次调用的提示，转向结构化工作流，再到自我驱动的代理，最终能够让复杂用户完成从使用模型到使用系统的转变，会是更高可能性的未来。也即最终胜出的是系统，而非单一模型。

在工程红利期爆发的同时，预训练回归到 Era of Research 也是行业均值回归的必然路径。就像 Ilya 所说，Scaling 已经成了一个 meme，这个动词有一种无脑的行动感和信念感，簇拥了天量的资本和算力涌入其中。但 Scaling law 可能有两个事实，一是 Scaling law 的边际收益递减。不是说模型不再有进展，而是花 100 倍、1000 倍的成本推动额外 1%的进展在经济意义上并不划算。二是我们应该从更宏观的角度看待 Scaling law，它可能是无数小 Scaling law 的切线集合，而 transformer 只是其中的一段。所以我们应该更积极的寻找下一个跳变。

跳变在哪？我们尝试理解一下 Ilya 想讲的方向。如果要构建一种像人类一样学习的机器，我们不应直接训练它“做数学”。我们应该用进化来训练一个“生存机器”（构建所有的进化所得的 Priors），其内部奖励系统（情感）在无意中使它在需要时擅长数学。Ilya 讲述了一个脑损伤患者的故事，该患者失去了所有情感，随后甚至无法做出简单的决定（比如穿哪双袜子）。他假设情感是进化出来的“高效价值函数”，用于在复杂中切入并优先促进行动。很可能这位脑损伤患者失去了他的不确定性最小化（焦虑）和熵最大化（无聊）先验。没有这些，每个决定的权重都相同。

也许下一个跳变的两个方向，第一是如何通过进化甚至是遗传算法获得高效价值函数作为进化的 Prior，用内在动机（好奇心/预测误差）来替代具体的奖励而进行模型训练。或者说与其训练模型去写代码和做数学，不如培养一个只要减少复杂系统的熵就会获得多巴胺冲击（最小化损失）的模型。这样的模型自然会学会编程和数学，因为在复杂环境中，编程和数学是减少熵的最佳工具。在为了求生存而自适应的进化路线上，从  *NEAT （NeuroEvolution of Augmenting Topologies*  ）开始，一直到 2017 年的深度神经进化（  *Deep Neuroevolution*  ）到开放式环境与协同进化（  *Open-Endedness & POET*  ）和 David Ha 2018 年的论文  *World Models*  ，逐步尝试去理解，智能不是被设计来解题的，而是为了在不断变化的复杂环境中活下去而涌现出的副产品这一方向。这一方向和规模化的计算能力并不相悖，或者我们可以说智能本质上就是计算规模化而涌现出来的特性。

另一个是超越简单优化的共生起源，允许原本独立的实体合并成为“超级实体”，从而实现能力的跃迁（真核细胞，多细胞生物，人类社会）。真核细胞的诞生源于古菌吞噬了细菌（线粒体的前身），两者并未消化彼此，而是保留了各自的基因组。Sakana 的  *Evolutionary Model Merge*  以及一系列相关研究正是这一过程的数学复现。与其强求一个 LLM 既懂日语又懂数学还懂代码，不如让一个日语专家模型和一个数学专家模型在参数空间进行遗传算法引导的层级插值。未来的超级实体可能包含数千个微小的、极端特化的模型，这也和 Ilya 的描述类似。

回到 2017 年，  *Attention is all you need*  甚至不是 NeurlPS 2017 年的 best paper 或者 spotlight paper，但技术的演进却给了它最好的加冕。我们可能又站在了新方向的起点，不过这一次我们有了更多的算力，或者更强智能诞生的土壤，来实现 Scaling law 曲线的下一次跃迁。

01.

上周市场总结

美国多空基金净杠杆大幅上升，对冲基金推动年内最大北美买盘潮

受 AI 板块再度走强带动，全球股指大幅反弹，尽管当周因假期缩短，但仍引发了年内最大规模的全球股票买盘潮之一。此次净买入主要由对冲基金回补空头推动，新增多头贡献相对较小。在北美市场，这一操作使美国多空基金净杠杆环比上升 5 个百分点至 56%，在过去 1 年和 5 年区间均处于上四分位数；总杠杆率则因行情上涨的市值效应上升 1 个百分点至 213%。空头回补主要集中在指数级对冲和部分个股，尤以可选消费和金融板块为主；多头增持则聚焦于 AI 受益的半导体龙头。房地产和医疗保健板块出现显著抛售，医疗保健资金流出主要集中在小盘生物科技公司。美国以外市场资金流动较为温和：欧洲因多头减持出现小幅净卖出，亚洲（日本除外）通过空头回补实现温和净买入（以台湾半导体为主），日本市场则多空增持基本持平。

对冲基金收复部分损失，但多数地区表现仍落后于股指

随着股指收复 11 月初大部分跌幅，全球对冲基金在假期缩短的一周内录得 1.4%的收益，低于 MSCI ACWI 指数 3%的涨幅。美国对冲基金，尤其是多空策略管理人表现优异，收益率达 2%，略低于标普 500 指数的 3.2%。欧洲对冲基金表现落后，仅上涨 0.8%，而欧元区 STOXX 600 指数上涨 2.2%；亚洲对冲基金上涨 2%，低于 MSCI 亚太指数的 2.6%。AGIX 表现突出，上周录得 6.0% 涨幅，显著跑赢主要区域市场。

截至本月，除亚洲对冲基金仍为 -1.3%（指数 -2.3%）外，大多数策略表现基本持平。年初至今，美洲多空基金收益率为 12.6%（标普 500 为 16.7%），而最受拥挤的前 50 只多空组合收益率高达 26.6%，显示拥挤交易持续跑赢大盘。

02.

AI Alphas

微软（MSFT）携手戴尔（DELL）、甲骨文（ORCL）等合作伙伴加速智能体 AI 基础设施布局

在微软 Ignite 2025 大会上，微软联合戴尔、甲骨文等合作伙伴发布了 70 余项产品，标志着 AI 正从辅助型副驾驶全面转向嵌入数据基础设施的智能体时代。核心突破包括推出 Agent 365 智能体控制平面，实现跨平台 AI 代理管理；发布 Fabric IQ 技术预览，通过零拷贝数据互操作构建实时业务视图。戴尔与微软深度整合，推出 Azure 集成的 PowerScale 存储方案，为生命科学等高数据量行业提供低延迟文件服务，同时将网络安全产品引入 Azure 市场。双方还通过 Copilot+ PC 架构推进混合 AI，结合云端与设备端智能。甲骨文则发布 Oracle Database@Azure 和 AI 数据库，将 Azure AI 能力与 Oracle 高性能数据管理融合。分析师指出，51%投入生产的应用已采用 AI，凸显数据基础设施成为智能体 AI 基石。

Meta（META）或采购谷歌（GOOGL）AI 芯片，英伟达（NVDA）股价受挫

报道称 Meta 正考虑向谷歌采购价值数十亿美元的 TPU 人工智能芯片，可能于明年启动合作，初期通过租赁方式使用谷歌托管的 TPU，并计划从 2027 年起在自有数据中心部署。谷歌今年 4 月发布的最新 TPU Ironwood 采用双芯片设计，集成 192GB HBM 内存和六个人工智能处理模块，单个液冷集群可提供 42.5 exaflops 算力。此合作可能影响 Meta 自研推理芯片 MTIA 的发展规划。英伟达随后发布声明强调其技术领先地位，称 Blackwell Ultra 加速器可提供 10 petaflops 性能，即将推出的 Rubin 系列将实现更高算力。

2025 年美国 AI 初创企业融资热度持续，多家企业年内多轮获巨额投资

2025 年美国 AI 初创企业融资市场延续了去年的火热态势，截至 11 月已有 49 家公司完成单轮 1 亿美元以上的融资，与 2024 年全年总数持平。其中多家企业年内完成多轮大额融资，显示资本对 AI 领域的持续追捧。Anysphere 在 11 月完成了 23 亿美元融资，估值达到 293 亿美元；OpenAI 于 3 月创下了 400 亿美元融资纪录，估值达到 3000 亿美元；Anthropic 在 9 月完成了 130 亿美元 F 轮融资，估值达到 1830 亿美元。医疗 AI、企业软件、AI 基础设施和 AI 代理成为投资热点，Nvidia、Snowflake、AMD 等科技巨头积极参与投资。值得注意的是，今年完成多轮大额融资的企业数量显著超过去年，反映出 AI 行业资本集中度进一步提升。

ServiceNow（NOW）洽谈收购网络安全初创公司 Veza，交易金额或超 10 亿美元

据  *The Information*  报道，ServiceNow 正就收购网络安全初创公司 Veza 进行深入谈判，交易金额可能超过 10 亿美元，这一估值是 Veza 迄今融资总额的四倍多。Veza 专注于身份管理平台，帮助企业保护员工访问工作应用的账户安全，检测未使用账户和权限过大的活跃账户。该公司平台还能管理机器身份，自动创建企业网络中机器身份的清单。此次收购将弥补 ServiceNow 在用户账户和机器身份管理方面的功能缺口。这并非 ServiceNow 首次进行十位数规模的初创公司收购，今年 3 月该公司以 28.5 亿美元收购了 AI 生产力平台开发商 Moveworks，近期还收购了数据管理初创公司 data.world。Veza 的投资者包括 Workday、Salesforce 和 Alphabet 旗下的 GV 基金。

Zscaler（ZS）业绩超预期但展望温和，股价下跌超 7%

云安全公司 Zscaler 在公布 2026 财年第一季度业绩后股价下跌超 7%。尽管当季业绩表现强劲，但温和的业绩展望未能满足投资者预期。截至 10 月 31 日的第一季度，Zscaler 调整后每股收益为 96 美分，同比增长 25%，营收为 7.881 亿美元，同比增长 26%，均超出分析师预期。运营现金流达 4.483 亿美元，递延收入为 23.51 亿美元，同比增长 32%。季度内公司推出了 Zscaler Digital Experience 创新功能，并在伦敦和巴黎设立了 FedRAMP Moderate 授权数据中心。11 月 3 日，Zscaler 宣布收购安全平台 SplxAI，以加强企业团队 AI 资产发现和保护能力。对于第二季度，公司预计调整后每股收益为 89-90 美分，营收为 7.97-7.99 亿美元，与预期持平；全年预计每股收益为 3.78-3.82 美元，营收为 32.82-33.01 亿美元，略高于预期。与同日公布业绩的 Workday 类似，尽管财务数据稳健，但投资者对科技公司增长预期更为苛刻，导致股价承压。

排版：夏悦涵

延伸阅读

](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247519757&idx=1&sn=c5321e03051d5858314508605403bee1&scene=21#wechat_redirect)

礼来模式揭秘：GLP-1，AI 加速药物发现，礼来如何突破“创新者窘境”？

](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247519630&idx=1&sn=b1014658d7af834f0c871c9764e63360&scene=21#wechat_redirect)

深度讨论 Gemini 3 ：Google 王者回归，LLM 新一轮排位赛猜想｜Best Ideas

](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247519510&idx=1&sn=2a304792d77687172dad568d43281cae&scene=21#wechat_redirect)

Periodic Labs：ChatGPT 创始成员打造的 AI 物理学家，让 Agent 在现实实验中学习

](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247519468&idx=1&sn=7966d04995a859f4a138abc1d676c7f2&scene=21#wechat_redirect)

Snowflake CEO 复盘：为什么 LLM 时代企业需要一个 AI Data Cloud？

](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247519409&idx=1&sn=ff433823fb92ddc4ba0e9aa55966952c&scene=21#wechat_redirect)

AI Bubble 深度讨论：万亿美元 CapEx，Dark GPU，广告电商如何带飞 AI｜Best Ideas

