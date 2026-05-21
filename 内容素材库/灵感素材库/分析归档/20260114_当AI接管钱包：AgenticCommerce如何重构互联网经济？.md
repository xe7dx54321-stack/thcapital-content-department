](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247519866&idx=1&sn=179a2ec7519d8f7a1bc41958a847e7e9&scene=21#wechat_redirect)

作者：Freda Duan （Partner@Alitmeter）

本文是 Altiemeter 合伙人 Freda Duan 对 Agentic Commerce 的深度解读，原文发布于她的 Substack Robonomics。

Agentic Commerce 带来的不只是购物方式的变化，如果它跑通、大规模应用，整个互联网广告、电商以及支付基础设施格局都会因此发生变化。也因此，在这个领域中除了 OpenAI、perplexity 等 AI-native 公司外，Google 作为大厂也相当积极，在 A2A、A2P 协议之外，本周的 NRF 2026 零售大会上发布了一套名为 UCP 的开源标准，期望为 AI Agent 驱动的电商交易建立一套“通用语言”，且 UCP 与 A2A、A2P 还有 MCP 协议兼容。

本篇文章主要探讨了 2 个核心问题：1）Agentic Commerce 在商业上究竟能否跑通？2）如果跑通了，它将如何重塑互联网的利益分配机制？

就当下的 timing 的来看，Stripe 作为支付基础设施的位置在 Agentic Commerce play 中极具优势，此外 Shopify 是目前看来最为 clean 的二级市场受益者。

TL;DR

Agentic Commerce 来了，互联网的玩法变了。很多人都在谈论它，但只有少数人能从 Commerce 的底层逻辑读懂它。在这篇文章中，我们主要探讨两个问题：

• Agentic Commerce 在商业上究竟能否跑通？

• 如果跑通了，它将如何重塑互联网的利益分配机制？

文章前半部分集中探讨其 商业可行性 。通过复盘 Meta 和 Google 在电商领域的失败尝试，以及对比 OpenAI 与 Perplexity 截然不同的切入路径，并分析在众多的 3P Model 中，哪一种最有可能在未来跑通。

后半部分则聚焦于 利益分配机制的重塑 。一旦 Agentic Commerce 成真，互联网的底层逻辑将从“广告变现”转向“交易抽成”，这将深刻改变 Shopify 等基础设施玩家与 Amazon 等流量巨头的命运，甚至重写支付（Stripe）与广告（Google）行业的版图。

01 .

Commerce 并非只有一种模式

在探讨 Agentic Commerce 之前，必须先明确一个前提：Commerce 这个概念下到底涵盖了什么。我们可以参考 a16z 的 Alex Rampell 提出的框架作为讨论 Agentic Commerce 的基础。

Alex Rampell 将消费行为分为三类： Impulse Buys（冲动消费）、Routine Essentials（日常必需品） 和 Life Purchases（重大生活消费）。 这三者完全是不同的物种。

Source: a16z —  *AI × Commerce*

Impulse Buys (冲动消费) ：无需预先计划或研究的即时消费行为。例如 TikTok Shop 上的爆款新奇特商品，或者超市收银台旁的糖果。你不需要“想”，只需要“买”。

Routine Essentials (日常必需品) ：高频、重复且不需要花时间决策的购买行为。例如定期补货的狗粮、牙膏或尿布等。通常消费者已经有了认准的品牌，需要的只是最便捷的购买渠道。

Life Purchases (重大生活消费) ：低频、高风险且需要大量信息辅助决策的购买行为。例如买房、买车、装修或复杂的旅行计划。这类消费通常伴随着大量的搜索、比价和咨询。

对于 Agentic Commerce 而言，Lifestyle 和 Functional Purchases 是目前最有潜力的领域。因为这两类消费通常需要做功课、参考他人意见，并且极度依赖信任感，而这正是 AI Agent 擅长的地方。随着时间的推移，AI 甚至可能进化到能够帮我们处理那些 Impulse Buys。

根据 GPT 的估算， 仅这三个类别的 TAM 就高达 3 万亿美元。

这也解释了为什么 ChatGPT 选择从 Etsy (覆盖了 540 万个卖家) 和 Shopify (覆盖约 300 万商家) 切入是极其明智的。这两个平台聚集了大量需要“consultative（咨询式导购）”的商品，与 Agentic Commerce 的特质十分契合。

02 .

E-commerce 是一个连续的光谱

大多数人在谈论 3 方卖家为主体的电商（3P Commerce）时，往往把它当成一个单一的模式，但实际上，“电商”这个概念是一个连续光谱， 光谱的两端分别是 Platform is the MoR 和 Merchant is the MoR。 Amazon 和 Shopify 分别位于这个光谱的两个极端，而其他的平台则散落在中间的某个位置。

这里的区分标准在于“谁是 MoR”：

MoR：Merchant of Record，指在法律上代表商户向终端用户出售商品或服务的实体。在电商业务流中，MoR 需要负责支付处理、退款与退单处理、税务合规、货币转换等事务，常用于跨境业务，帮助商户减轻支付与合规负担。

• Amazon：Platform is the MoR

在这里，平台是名义上的商家 (Merchant of Record, MoR)。退款、拒付、统一支付、税务等所有 dirty work 都由平台一手包办。但代价是， 平台上的卖家并不拥有任何客户关系。

• Shopify：Merchant is the MoR

即商家自己处理才是真正的 MoR。一切都由商家自己搞定——选择支付服务商 (PSP)、管理物流、处理退货。作为回报， 商家拥有 100% 的客户关系 。

• 中间地带

Etsy、 eBay：逻辑上它们更靠近“Platform is the MoR”这一侧。平台负责统一收款。但在退货问题上，买家首先得联系卖家；如果卖家装死（2-3 天不回复），平台才会介入。

淘宝、拼多多：逻辑上它们更靠近 “Merchant is the MoR”这一侧。虽然商家负责绝大部分运营，但平台的手伸得很长 —— 提供担保交易、代收代付服务，并强势介入纠纷调解。

为什么理解 E-commerce 光谱这很重要？因为 Agentic Commerce 本质上就是一种 3P 电商。

不同模式在 E-Commerce Spectrum 这件事很重要？因为这将决定：

• 这门生意能做多大，即商业上限；

• 商家能保留多少流量和数据控制权，即商家利益会如何受到影响；

• 支付体系将面临多大的颠覆。

03 .

Agentic Commerce 的两个路径：Perplexity 与 ChatGPT

虽然都是在尝试 Agentic Commerce，但 Perplexity 和 ChatGPT 的打法其实截然不同。在 Perplexity 的 “Buy with Pro” 中， Perplexity 自己就是 MoR (即用户的信用卡账单上会显示 Perplexity)；而 ChatGPT 明确表示商家才是 MoR。

OpenAI: Stripe Agentic Commerce Protocol (“ACP”)

OpenAI 的 ACP 协议是独立于 PSP（支付服务商协议）的，也就是说无论商家用哪家 PSP，也无论使用哪个 Agent，这套协议都能跑通。

OpenAI 与 Stripe 合作推出的 Agentic Commerce Protocol (ACP) 其核心突破在于彻底解耦了“前端结账体验”与“后端支付处理”，例如 Etsy 本身不使用 Stripe 处理支付，却能无缝接入 ACP。ACP 的机制逻辑是：通过标准化的 Token 传递支付凭证与风控信号，让用户无需离开 ChatGPT 即可完成“即时购买”，同时允许商家保留原有的支付服务商（如 Adyen、Checkout.com 等）。

这一点还没被很多人所关注到，但其实非常关键：即便 Etsy 本身并不使用 Stripe 进行支付处理，它依然可以无缝接入 ACP。

• OpenAI ACP 逻辑下的支付链路：

1、OpenAI 将支付凭证打包进一个共享 Token；

2、Etsy 收到 Token 后转发给自家的 PSP；

3、Etsy 的 PSP 解包 Token，提取凭证，完成扣款。

• 对于商家：除了支付给 OpenAI 一笔抽佣金外，原本的支付手续费维持不变。目前还不清楚 Stripe 能从 ACP 中分到多少羹 (或者是否分羹)，但历史经验告诉我们，广泛采用的开放标准通常会笑到最后， Android 是一个很好的例证。

Perplexity: “Buy with Pro”

Perplexity 的电商方案中选择亲自来充当 MoR 的角色，而 Walmart 等商家仅仅是负责发货的履约方。这意味着 Perplexity 承担了比 OpenAI 多得多的责任。

Buy with Pro 逻辑下的支付链路：

• 资金首先进入 Perplexity 的口袋；

• Stripe (通过 Link) 处理用户在 Perplexity 上的结账；

• 然后 Perplexity 再通过 Walmart 的 PSP 向 Walmart 下单。

对于商家而言，如果看重对支付、税务、退款、反欺诈、CRM 和第一方数据的掌控权，同时又想蹭上 Agent 的流量红利，显然 OpenAI ACP 是更好的选择。对于平台而言，ChatGPT 的模式更容易规模化，因为它几乎不承担任何连带责任。

在我的实际测试中，OpenAI 的 Agentic Commerce 在逻辑上更顺畅，这才是正确的打开方式。如果 OpenAI 哪天想不开非要自己做 MoR，就值得市场去重点关注了。

04 .

历史复盘：Google 和 Meta 为什么没能把电商做起来？

Google 和 Meta 其实都不想当 MoR，所以它们在做电商的时候都把这个烫手山芋扔给了商家。不过，不当 MoR 并不是它们做不成 3P 电商的根本原因。

最本质的原因可能是，这两家巨头可能早就意识到：相比电商，卖广告显然是一门更轻松、也更暴利的生意，所以它们最终还是把重心全押在了广告上。

Google 的电商梦从未真正起飞过。今天它剩下的功能纯粹就是展示广告，外加一些基础的比价工具。

而 Meta 投入了相当大的资源和警力来搞定 App 内的 Checkout ，比如在 2023 年的时候甚至强制商家使用，但到了 2025 年 9 月，FB/IG 上的店铺又默认回退到了外链结算 (link-out)， 这也正式宣告了 Meta Commerce 的“死亡”。

Meta 的支付体验可以说是灾难级别：8 个以上的步骤，强制登录，无休止的跳转…Meta Pay (前身是 Facebook Pay) 从未真正普及，即便后来接入了 PayPal、Shop Pay 或 Amazon Pay，也没能解决体验上的摩擦。

之所以要复盘 Google 和 Meta 的案例是因为我们必须彻底理解为什么过去的 3P 电商尝试都失败了，这一点和是否有 Agent 参与并不相关。

从目前观察到的来看， OpenAI 联手 Stripe 推出 ACP 绝对是一步大棋。 如果 Meta 或 Google 当年能搞出类似的东西，它们的电商之路可能会是另外一种可能。

05 .

Google 与 OTA 的博弈

如果要真正讨论 Agentic Commerce 可能带来的影响，就一定绕不开 Google，作为流量漏斗的顶层，Google 一定程度上重塑了 OTA 等其他互联网平台。

• 以 Booking 和 Expedia 为例

这两家公司的预订量和流量大约有一半来自直接流量，另一半来自间接流量，而间接流量的核心来源就是 Google。

考虑到支付给 Google 的高昂 CPC (每次点击成本)，间接部分流量的 UE 基本上只能勉强维持盈亏平衡，这里可以算一笔账：假设一晚酒店 $300，抽佣率 15%，CPC 为 $1–3，点击到预订的转化率为 3–4%。 这意味着每完成一笔预订，营销成本约为 $50 ，基本上把从间接流量赚到的钱都赔进去了。

相比之下，直接流量简直就是金矿。它不仅利润丰厚，还能通过付费广告变现 (广告收入占 Expedia 营收的 ~10%，Booking 的 ~5%；约占 EBIT 的 25%)。

Etsy 的情况也类似。营销成本占营收的 ~30% ，这个数据意味着间接流量部分的 UE 也只是在盈亏及格线徘徊。

以上例子很直接的说明，对于 OTA（以及其他电商消费平台来说），来自 Google 的间接流量是一场昂贵的压榨。 Google 从旅游行业榨取的总利润，比所有 OTA 平台加起来还要多。

06 .

新数字税：广告费 ≈ 抽佣率

讨论广告费或抽佣率本身是一个非常有趣的消费互联网思维框架： 广告费和抽佣率本质上都是“数字税”，只是两种不同叫法。 每一个网络经济体都可以被视为在征收某种形式的“抽佣”。

• YouTube 对创作者征收的“税”是 45%。

• Meta 通过广告拿走了创作者 ~99% 的经济价值。

• Apple App Store 的“税率”是 15–30%。

在上面的 OTA 案例中，间接流量的实际净抽佣率只有 0–5%，尽管名义上的抽佣率是 15%。这意味着，如果 ChatGPT 向 Booking 或 Expedia 收取 10–15% 的抽佣率，反映到成本上其实跟从 Google 买流量是一样的（都是盈亏平衡）。

而这种广告模式与电商模式的融合其实在中国已经发生了。拼多多、阿里巴巴等平台早就模糊了向商家收费的界限，不管是叫广告费还是抽佣率，本质上都是商家给到平台的“税”。

Agentic Commerce 接下来的“剧本”：ChatG PT 一开始可能会设定一个较低的抽佣率 (比如 2%)，然后逐渐提高，直到达到市场均衡点 (10–15%)。无论这笔钱叫“抽佣率”还是“广告费”，都只是语义上的区别，因为掌握漏斗顶端的网络永远是收税的一方！

07 .

Agentic Commerce 对商家与平台的影响

Agentic Commerce 对商家的冲击将来自多个维度：

• 流量角度：直接流量和间接流量分别会带来不同的影响

1、直接流量：最直接的自然是广告收入会受到什么影响？

2、间接流量：

1）Unit Economics 会如何变化？(即上文提到的“实际抽佣率”概念)

2）转化率会如何变化？

3）市场份额将如何重新分配？

• 行业在线渗透率：很多卖方分析师鼓吹 Agentic Commerce 会推高在线渗透率，但这其中的逻辑还有待验证。

这就像奇异博士看到了 1400 万种未来，考虑到直接流量占比可能会被进一步压缩，对商家和平台来说，大多数结局都不太好，这种挤压可能比 Apple 的 30% 税或 Google 的 CPC 过路费还要狠。

传统上，商家依赖用户在网站上的浏览行为来通过 Upsells 和 Cross-sells 提升客单价，但 Agentic Commerce 改变了这一切：购买发生在站外，没有访问记录，没有 Pixel 追踪，没有浏览数据。商家也许还能拿到买家的邮箱，但失去了用户行为的可视度和再营销的能力。

所以问题的关键就来到了： Agentic Commerce 如此高的转化率能否抵消这些损失？

对于小商家来说，也许可以。但对于那些建立在 AOV 优化之上的大型零售商来说，情况恐怕不容乐观。

在上面的表格中：

• 营销支出：流向了“漏斗顶端”，无论是通过广告费还是抽佣率的形式。

• 广告收入 (这部分仅来自直接流量)：如果 Agentic Commerce 进一步把流量从直接渠道抽走，这部分收入会去哪儿？

08 .

Shopify：Agentic Commerce 最明显的赢家

Shopify 可能是 Agentic Commerce 语境下最干净、最契合的结构性赢家。

Shopify 从未做过 MoR，也不会像平台那样去“策展”商家。所以，前文提到的“直接 vs. 间接流量”的矛盾对它来说并不适用。多年来，Shopify 一直因为没有成为一个真正的消费者平台而饱受诟病 —— 但在这个新世界里，这反而可能是一种 “因祸得福”。

具体影响：

• GMV 向优质 SMB 倾斜。Shopify 的 300 多万商家中，有很多都在销售独特、高质量的产品，但它们根本打不起烧钱的广告战。Agent 的出现可能会拉平这个赛场。

• 更高的渗透率。那些苦于无法为 Agent 建立数据/目录管道的 SMB，可能会为了省事而迁移到 Shopify 的标准化技术栈上。

• 营销变得更高效。Shopify 自身的营销支出约为 $14 亿 (占营收的 16%)，而其商家总共花费了估计 $200–500 亿 (基于 ~$3000 亿 GMV 和典型的 7–15% 营销占比)。在 Agentic 的世界里，这种重复的“数字税”有望被精简。

09 .

支付变革：Stripe 的隐形杠杆

无论是 OpenAI 的 Agentic Commerce Protocol (ACP) 还是 Perplexity 的模式，都允许商家保留现有的 PSP ，而 Stripe 同时为这二者提供支付 infra 环节的支持。

随着 Agentic Checkout 的普及，Stripe 作为中立的连接角色，其地位只会越来越稳固。

10 .

Agentic Commerce 对 Google / Ads 的冲击

Google 的 Bull case 逻辑拥有近乎完美的“T 型”价值主张：

• 垂直整合：从应用层到云，再到芯片，全栈打通；

• 水平布局：产品线极其丰富 —— 生产力工具 (Google Suite)、娱乐 (YouTube)、公用设施 (Google Home 等)。最终，最好的商业模式往往会胜出。

到目前为止，Google 的搜索广告收入并没有真正受到 GPT 的实质性冲击。理论上，Google 即使失去了 95% 的搜索量，营收依然可能增长 —— 只要它能留住那些 高价值 的 querie，而这些查询主要都与 Commerce 相关。

但是，Google 的广告模式能否在 Agentic 时代完好无损地活下来目前还是个未知数。

11 .

What's Next？

Stripe CEO Patrick Collison 在和 Shopify CEO Tobi Lütke 的访谈中设想过一个情境：应该有人去构建一个 Universal Catalog，不仅仅是针对 Shopify 的商家，而是囊括世间万物。这正是 Agentic Commerce 的终极梦想：用标准化的产品数据驱动 AI Agent 进行智能化购物。

在今天，“帮我找双女士跑鞋”这样的 prompt 依然过于笼统。但也许接下来Agent 就可以精准理解“一件带有大写字母 G 的黑白马海毛毛衣”这样的需求了，而要实现这一点不仅需要针对特定商品的模型，更需要极其丰富和结构化的元数据支撑。

此外，为了形成完整的商业闭环， 一个基于真实反馈的评价层也将必不可少。

延伸阅读

](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247520510&idx=1&sn=ffb241930b5b6fe38203e2c4dbefd129&scene=21#wechat_redirect)

深度解读 AGI-Next 2026：分化、新范式、Agent 与全球 AI 竞赛的 40 条重要判断

](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247520443&idx=1&sn=e025ef2b59fd69c56e294d5f163beda6&scene=21#wechat_redirect)

拾象 2026 AI Best Ideas：20 大关键预测

](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247520406&idx=1&sn=8e95b0b7825e3ddfa4c1bcca44b51755&scene=21#wechat_redirect)

Benchmark 新合伙人 Everett Randle: 忘掉 SaaS 逻辑与毛利率，AI 时代估值看单客价值

](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247520371&idx=1&sn=e92361c3d521d0bb77c5b7cc95d84978&scene=21#wechat_redirect)

AI 医疗全景更新：为什么硅谷 healthcare 领域出现了最多的 AI 独角兽？

](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247520307&idx=1&sn=46ccaa78062881bd289894f72420b5ae&scene=21#wechat_redirect)

深度讨论 2026 年 AI 预测：最关键的下注点在哪？｜Best Ideas

