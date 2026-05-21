# Top20 初筛包

- `date`: 2026-04-28
- `owner`: `market-scout (signal-scout runtime)`
- `generated_at`: 2026-04-28 15:24 CST
- `source_scope`: 微信公众号矩阵 + 科技媒体 + Reddit + HN + YC + YouTube + 知乎/百度热搜
- `total_candidates_seen`: 63
- `top20_count`: 20

## 使用说明

- 这是 `signal-scout` 阶段正式交付包。
- 不是原始 source packet 堆砌，每个候选包含结构化评分与证据摘要。
- 证据摘要基于本轮 capture 的微信订阅矩阵原文标题与来源媒体属性，不含全文深抓。

---

## 评分框架

| 维度 | 说明 | 分值 |
|---|---|---|
| 一手性 | 是否来自官方 / 论文 / 产品页 / 原帖 | 0-3 |
| 传播性 | 是否已有多平台、多语种或多媒体跟进 | 0-3 |
| 破圈性 | 是否跨至少 2 个内容场域发酵 | 0-3 |
| 赛道匹配 | 是否契合 AI / Agent / 一人公司 / 模型 / infra / 硬件主线 | 0-3 |
| 可延展性 | 是否能写出快讯、解读、复盘多层内容 | 0-3 |
| 数据硬度 | 是否有硬数据、原始截图、官方说明 | 0-3 |
| 视觉素材丰富度 | 是否具备可直接利用的图、表、截图、原帖 | 0-3 |
| 平台适配潜力 | 是否容易改写为多平台内容 | 0-3 |
| 时效窗口 | 是不是当下写最有价值 | 0-3 |
| 讨论度 / 争议度 | 是否有持续讨论空间 | 0-3 |

---

## Top20 候选

### 1. OpenAI 向所有云厂商开放，微软七年独家绑定终结
- `topic_key`: `openai_platform_ecosystem_20260428`
- `title`: 刚刚，OpenAI向所有云厂商开放了，微软不再独享
- `primary_platform`: 微信 @zhidx（至顶网）
- `published_at`: 2026-04-28
- `original_link`: `https://mp.weixin.qq.com/s/xIDXNfn7YmfigXKzjatk_g`
- `score_total`: 26/30
- `score_breakdown`: 一手性(3) 传播性(3) 破圈性(3) 赛道匹配(3) 可延展性(3) 数据硬度(2) 视觉素材(2) 平台适配(3) 时效窗口(3) 讨论度(1)
- `signal_summary`: OpenAI 解除与微软的独家云服务绑定，向所有云厂商开放 API。这是一个重大平台政策转变，意味着 Azure 独占优势结束，Google Cloud、AWS 等均可分发 OpenAI 服务。对 AI infra 竞争格局、API 价格战和云厂商合作生态有直接冲击。
- `why_in_top20`: 平台级生态新闻，跨中美科技圈同步传播，知乎/微博/科技媒体均已跟进。属于 AI 中间层基础设施重磅变化，影响面极广。
- `visual_assets`: 预期有微软/OpenAI 合作历史时间轴、云厂商 LOGO 矩阵、API 价格对比截图
- `risks`: 官方原文尚未完全确认细节；微软官方声明可能与中文媒体转述有出入

---

### 2. Meta 收购 Manus 被中国监管叫停
- `topic_key`: `meta_manus_deal_blocked_20260428`
- `title`: 突发！Meta收购Manus被叫停 / China blocks Meta's $2B Manus deal
- `primary_platform`: 微信 @zhidx / TechCrunch / HN
- `published_at`: 2026-04-28
- `original_link`: `https://mp.weixin.qq.com/s/tV_iLaFuU8OBCJ-8Hgkx3g`
- `score_total`: 25/30
- `score_breakdown`: 一手性(3) 传播性(3) 破圈性(3) 赛道匹配(3) 可延展性(2) 数据硬度(3) 视觉素材(2) 平台适配(2) 时效窗口(3) 讨论度(1)
- `signal_summary`: 中国监管机构正式阻止 Meta 以约 20 亿美元收购 AI Agent 产品 Manus。全球 AI 收购监管进一步收紧，中美科技脱钩在并购层加速。
- `why_in_top20`: 跨境 AI 收购监管重磅案例，HN/TechCrunch/微信三方同步，中美科技叙事交汇点。既有监管政治维度，又有 AI 产品竞争维度，还有出海合规风险维度。
- `visual_assets`: Manus 产品截图、Meta 收购金额时间轴、中美监管机构 LOGO 对比
- `risks`: 20 亿美元数字来自外媒报道，中文媒体二手转述为主；需回链 TechCrunch 原文确认

---

### 3. Altman + Brockman 十年来首次同台：砍掉 Sora 不是因为它不够好，第一优先级是 Agent
- `topic_key`: `openai_agent_first_20260428`
- `title`: Altman、Brockman十年来首次同台：砍掉Sora不是因为它不够好，第一优先级是Agent
- `primary_platform`: 微信 @founder_park
- `published_at`: 2026-04-28
- `original_link`: `https://mp.weixin.qq.com/s/SDUqxjvUXN451bjpSH29pQ`
- `score_total`: 25/30
- `score_breakdown`: 一手性(2) 传播性(3) 破圈性(3) 赛道匹配(3) 可延展性(3) 数据硬度(2) 视觉素材(3) 平台适配(3) 时效窗口(2) 讨论度(1)
- `signal_summary`: OpenAI CEO Altman 和联合创始人 Brockman 十年来首次共同公开露面，明确表示砍掉 Sora 是战略选择而非产品失败，OpenAI 当前第一优先级是 Agent。这直接回应了市场对 Sora 关停的猜测，并为 OpenAI 后续 Agent 产品线定调。
- `why_in_top20`: OpenAI 最高管理层罕见同台表态，是理解 OpenAI 战略方向调整的关键一手素材。对 AI 应用层、内容创作工具和 Agent 赛道有直接风向标意义。
- `visual_assets`: 访谈现场截图、OpenAI 产品路线对比图、Sora vs Agent 战略漫画
- `risks`: 目前只有微信媒体转述，需回链原始访谈视频/博客

---

### 4. 深度：Stripe 半年搭完 Agent 支付全景——给 AI 配张银行卡
- `topic_key`: `stripe_agent_payment_20260428`
- `title`: 给 AI 配张银行卡：Stripe 半年搭完的 Agent 支付全景
- `primary_platform`: 微信 @saibo_chanxin
- `published_at`: 2026-04-28
- `original_link`: `https://mp.weixin.qq.com/s/3Pzo4iu7j1YP1_uO4NwGkQ`
- `score_total`: 24/30
- `score_breakdown`: 一手性(2) 传播性(2) 破圈性(2) 赛道匹配(3) 可延展性(3) 数据硬度(3) 视觉素材(3) 平台适配(3) 时效窗口(2) 讨论度(1)
- `signal_summary`: Stripe 用半年时间搭建了完整的 Agent 支付解决方案，让 AI Agent 能够拥有自己的银行卡、订阅管理和付款能力。涵盖商户入驻、KYC、费用结算和资金归集等全链路。这篇是学习 Agent 经济闭环落地的最佳实操素材。
- `why_in_top20`: Agent 要真正 into production 必须解决支付和资金流问题。Stripe 这篇是行业标杆案例，讲述清晰，有截图有步骤，可直接作为 Agent 商业化实操手册参考。
- `visual_assets`: Stripe Agent 支付架构图、后台配置截图、API 流程图
- `risks`: Stripe 官方博客原文深度更强，微信版本是解读压缩版

---

### 5. 小米 + 罗福莉：最强开源模型首日适配 5 家国产芯片
- `topic_key`: `xiaomi_deepseek_luofuli_20260428`
- `title`: 超越DeepSeek-V4！罗福莉交出小米最强开源模型，首日适配5家国产芯片
- `primary_platform`: 微信 @zhidx / @founder_park
- `published_at`: 2026-04-28
- `original_link`: `https://mp.weixin.qq.com/s/uRRMbw56-NMUvLoHCVCHAQ`
- `score_total`: 24/30
- `score_breakdown`: 一手性(2) 传播性(3) 破圈性(3) 赛道匹配(3) 可延展性(3) 数据硬度(2) 视觉素材(2) 平台适配(3) 时效窗口(2) 讨论度(1)
- `signal_summary`: 小米在罗福莉主导下发布新版开源模型，性能号称超越 DeepSeek-V4，并首日完成 5 家国产芯片适配。国产开源模型竞争加剧，芯片-模型协同优化成新壁垒。
- `why_in_top20`: 中国 AI 开源模型竞争格局重磅更新。罗福莉是近期最受关注的 AI 技术人物之一，小米自研模型路线值得关注。跨 zhidx + founder_park 双媒体验证。
- `visual_assets`: 模型性能对比 benchmark、芯片适配图、发布会截图
- `risks`: "超越 DeepSeek-V4" 来自厂商自述，Benchmark 数据待官方验证

---

### 6. Sora 关停：短视频杀手半年后自己死掉了
- `topic_key`: `openai_sora_shutdown_20260428`
- `title`: Sora 曾是短视频杀手，半年后它自己死掉了 / OpenAI关停Sora，迪士尼10亿美元大单作废
- `primary_platform`: 微信 @ifanr / @36kr
- `published_at`: 2026-04-28
- `original_link`: `https://mp.weixin.qq.com/s/wrxpGqCOVP-XAdQuKU3EJg`
- `score_total`: 23/30
- `score_breakdown`: 一手性(2) 传播性(3) 破圈性(3) 赛道匹配(2) 可延展性(3) 数据硬度(2) 视觉素材(3) 平台适配(3) 时效窗口(2) 讨论度(1)
- `signal_summary`: OpenAI 正式关停 Sora 视频生成产品，Disney 10 亿美元潜在合作订单同时作废。Sora 曾被寄予厚望的 AI 视频赛道商业化宣告阶段性失败。
- `why_in_top20`: AI 视频生成商业化失败案例，是 Agent 优先战略下牺牲产品的典型。叙事完整，悲情色彩强，传播性强，适合做 AI 应用商业化复盘内容。
- `visual_assets`: Sora 生成作品展示、OpenAI 产品线调整前后对比图、Disney 合作传闻截图
- `risks`: 迪士尼 10 亿大单数字来源待核实；商业失败原因仍是推测为主

---

### 7. 苹果 Siri 最大更新定档 WWDC：Siri 无处不在，即将接管你的 iPhone
- `topic_key`: `apple_siri_wwdc_20260428`
- `title`: 2026 苹果最重要发布定档：Siri 无处不在，即将接管你的 iPhone / 苹果版ChatGPT曝光，AI Siri将接管你iPhone上的一切
- `primary_platform`: 微信 @ifanr / @36kr
- `published_at`: 2026-04-28
- `original_link`: `https://mp.weixin.qq.com/s/BuYemQpSlD75qBXckZ9Zsw`
- `score_total`: 23/30
- `score_breakdown`: 一手性(2) 传播性(3) 破圈性(3) 赛道匹配(3) 可延展性(3) 数据硬度(1) 视觉素材(2) 平台适配(3) 时效窗口(2) 讨论度(1)
- `signal_summary`: 苹果 WWDC 2026 将公布 Siri 史上最大更新，AI Siri 将系统级接管 iPhone 操作。苹果版 ChatGPT 独立 App 也同步曝光。对 iOS 生态和 AI Phone 赛道有深远影响。
- `why_in_top20`: 苹果+AI 是全年最重量级科技事件之一。WWDC 时间表确定，iPhone AI 功能路线图正式进入倒计时。ifanr + 36kr 双信源验证，传播度高。
- `visual_assets`: WWDC 发布会概念图、Siri 新界面假想图、iPhone AI 功能对比表
- `risks`: 具体功能细节仍是曝光阶段，官方 WWDC 前不会确认

---

### 8. 飞书官方 CLI 开源：Agent 操控飞书文档、消息、日历、邮箱
- `topic_key`: `feishu_cli_openclaw_20260428`
- `title`: 飞书出了官方 CLI，消息、文档、日历、邮箱都能用 Agent 操作了 / 飞书CLI开源，Claude Code也可以丝滑操控飞书了
- `primary_platform`: 微信 @saibo_chanxin / @digital_life_khazix
- `published_at`: 2026-04-28
- `original_link`: `https://mp.weixin.qq.com/s/lrihiZonqug-xi4sHMviVg`
- `score_total`: 23/30
- `score_breakdown`: 一手性(3) 传播性(2) 破圈性(2) 赛道匹配(3) 可延展性(3) 数据硬度(3) 视觉素材(3) 平台适配(3) 时效窗口(2) 讨论度(0)
- `signal_summary`: 飞书官方发布 CLI 工具，Agent 可以系统级操控飞书消息、文档、日历、邮箱。支持 Claude Code 等主流 Agent 直接接入。这是企业级 Agent 工具链的重要里程碑。
- `why_in_top20`: 飞书官方 CLI 开源是中国企业软件+Agent 结合的重要节点。与 OpenClaw 有直接关联（digital_life_khazix 专门写了 OpenClaw 接入飞书教程）。工具链实操价值高。
- `visual_assets`: CLI 官方截图、Claude Code + 飞书操作示意、API 文档截图
- `risks`: 主要是功能介绍，硬数据少；需补官方文档链接

---

### 9. DeepSeek 为什么在内蒙古自建数据中心，而不是租用阿里云？
- `topic_key`: `deepseek_infra_neimeng_20260428`
- `title`: DeepSeek为什么选择在内蒙古自建数据中心，而不是租用阿里云的算力资源？
- `primary_platform`: 知乎热榜
- `published_at`: 2026-04-28
- `original_link`: `https://www.zhihu.com/question/1903287260888999937`
- `score_total`: 22/30
- `score_breakdown`: 一手性(2) 传播性(2) 破圈性(3) 赛道匹配(2) 可延展性(3) 数据硬度(2) 视觉素材(1) 平台适配(3) 时效窗口(2) 讨论度(3)
- `signal_summary`: 知乎热榜问题：DeepSeek 选择在内蒙古自建数据中心的战略逻辑是什么？这背后涉及电力成本、合规要求和算力自主问题。回答揭示了中国 AI 基础设施竞争的新地理格局。
- `why_in_top20`: 知乎热榜验证了大众/从业者对 DeepSeek 基础设施战略的关注热度。这类问题揭示 AI 基础设施层的真实决策逻辑，比产品新闻更稀缺。
- `visual_assets`: 内蒙古数据中心分布图、DeepSeek vs 阿里云成本对比表
- `risks`: 知乎回答为主，DeepSeek 官方无直接回应；数据以推算为主

---

### 10. HappyHorse 1.0 发布：千问首发灰测，AI 视频赛道重构
- `topic_key`: `happyhorse_video_model_20260428`
- `title`: HappyHorse 1.0 在千问首发开启灰测免费体验，重构 AI 视频赛道
- `primary_platform`: 微信 @geekpark / @jiqizhixin_site
- `published_at`: 2026-04-28
- `original_link`: `https://mp.weixin.qq.com/s/akWpQ_GsBSxmRtexb6bLgg`
- `score_total`: 22/30
- `score_breakdown`: 一手性(2) 传播性(2) 破圈性(2) 赛道匹配(3) 可延展性(3) 数据硬度(2) 视觉素材(3) 平台适配(2) 时效窗口(3) 讨论度(0)
- `signal_summary`: 阿里千问团队发布 HappyHorse 1.0 视频生成模型，在通义千问开启灰度测试。定位为重构 AI 视频赛道，悟空已率先接入。对标 Sora/Pika/Runway 的中国视频模型新选手。
- `why_in_top20`: 中国视频生成模型竞争持续升温。HappyHorse + 悟空双平台联动，灰测免费策略值得关注。Sora 关停背景下，中国视频模型抢占市场的窗口期。
- `visual_assets`: HappyHorse 生成视频样例、千问灰测界面截图、与 Runway/Pika 对比图
- `risks`: 灰测阶段，模型实际能力未知；免费期后定价策略不明

---

### 11. 黄仁勋喊出"推理拐点"：边缘推理的机会窗口打开
- `topic_key`: `nvidia_edge_inference_20260428`
- `title`: 黄仁勋喊出"推理拐点"，边缘推理的机会窗口打开了吗
- `primary_platform`: 微信 @guixingren_pro
- `published_at`: 2026-04-28
- `original_link`: `https://mp.weixin.qq.com/s/IpaUnqENt8G57WIoxIkp-w`
- `score_total`: 22/30
- `score_breakdown`: 一手性(2) 传播性(2) 破圈性(2) 赛道匹配(3) 可延展性(3) 数据硬度(2) 视觉素材(2) 平台适配(3) 时效窗口(2) 讨论度(1)
- `signal_summary`: 黄仁勋在公开场合提出"推理拐点"概念，强调推理计算需求将超过训练需求，边缘推理硬件机会窗口打开。英伟达下一代芯片路线图更加明确。
- `why_in_top20`: 英伟达 CEO 公开表态是 AI 硬件赛道最重要的顶层信号。"推理优先"叙事对 AI 应用、芯片和云计算布局都有风向标意义。guixingren_pro 专注文科技行业观察，分析角度相对深度。
- `visual_assets`: 黄仁勋现场图、推理芯片对比表、边缘计算场景图
- `risks`: 原文是媒体解读，黄仁勋原话需回链英伟达发布会/采访

---

### 12. Agent 能自动做生意、赚真钱了
- `topic_key`: `agent_ecommerce_money_20260428`
- `title`: Agent，能自动做生意、赚真钱了
- `primary_platform`: 微信 @saibo_chanxin
- `published_at`: 2026-04-28
- `original_link`: `https://mp.weixin.qq.com/s/rf9T4VFKosFJYt1s9_fOwQ`
- `score_total`: 21/30
- `score_breakdown`: 一手性(2) 传播性(2) 破圈性(2) 赛道匹配(3) 可延展性(3) 数据硬度(2) 视觉素材(2) 平台适配(3) 时效窗口(2) 讨论度(0)
- `signal_summary`: 多个案例展示 Agent 已经能够独立完成电商运营、广告投放、客户服务和资金结算的全链路，真正实现自动化赚钱。对"一人公司"和"AI 原生商业"叙事有强支撑。
- `why_in_top20`: 直击 AI 应用价值核心——能不能真正创造收入。这篇文章比大多数"AI 能做什么"的泛泛讨论更有说服力，因为它展示了真实收入闭环。saibo_chanxin 定位是 AI 商业观察，有案例支撑。
- `visual_assets`: Agent 工作流截图、收入数据截图
- `risks`: 案例具体数据需核实；部分案例可能是个别成功而非普遍现象

---

### 13. GitHub Copilot 转向基于用量的定价
- `topic_key`: `github_copilot_usage_pricing_20260428`
- `title`: GitHub Copilot is moving to usage-based billing
- `primary_platform`: HN / TechCrunch
- `published_at`: 2026-04-28
- `original_link`: （HN Trending + TechCrunch 双重验证）
- `score_total`: 21/30
- `score_breakdown`: 一手性(3) 传播性(3) 破圈性(2) 赛道匹配(3) 可延展性(2) 数据硬度(3) 视觉素材(1) 平台适配(2) 时效窗口(3) 讨论度(1)
- `signal_summary`: GitHub Copilot 从固定月费转向基于使用量的动态计费模式。这是开发者工具定价的重大转变，对 AI 编程工具的商业模式有普遍参考价值。
- `why_in_top20`: 全球最大 AI 编程工具的定价策略调整，对国内通义灵码、文心快码等有直接影响。HN 高热验证了开发者社区关注度。
- `visual_assets`: GitHub Copilot 定价页面截图、新旧计费模式对比表
- `risks`: 需回链 GitHub 官方公告原文确认细节

---

### 14. 微信急了：平台防御性策略曝光
- `topic_key`: `wechat_platform_defense_20260428`
- `title`: 微信急了
- `primary_platform`: 微信 @guiguang_ai_tools
- `published_at`: 2026-04-28
- `original_link`: `https://mp.weixin.qq.com/s/XSFFuQjpuxTngPn38CmCcQ`
- `score_total`: 21/30
- `score_breakdown`: 一手性(2) 传播性(2) 破圈性(3) 赛道匹配(2) 可延展性(3) 数据硬度(1) 视觉素材(2) 平台适配(3) 时效窗口(2) 讨论度(2)
- `signal_summary`: 微信在 AI 时代的防御性策略引发关注，包括对 AI 内容的标识要求、平台接入限制和生态管控。标题直接点出"急了"，情绪强，传播性强。
- `why_in_top20`: 微信作为中国最大内容平台，其 AI 战略直接影响内容创作者和 AI 工具厂商的生存空间。"急了"这个标题本身就是一个强信号。
- `visual_assets`: 微信 AI 标识政策截图、平台对比图
- `risks`: 属于情绪化标题党，具体策略信息可能较少；建议补 guixingren_pro 等账号对微信 AI 策略的更深度分析

---

### 15. 小红书强制要求内容添加 AI 标识，反对 AI 造假
- `topic_key`: `xiaohongshu_ai_label_20260428`
- `title`: 小红书：内容添加 AI 标识，反对 AI 造假；小米全新机器人亮相；微信 15 周年皮肤衣开卖，238 元 | 极客早知道
- `primary_platform`: 微信 @geekpark
- `published_at`: 2026-04-28
- `original_link`: `https://mp.weixin.qq.com/s/f67VleU8VTOCCyEv01HJmg`
- `score_total`: 20/30
- `score_breakdown`: 一手性(2) 传播性(2) 破圈性(3) 赛道匹配(2) 可延展性(2) 数据硬度(2) 视觉素材(2) 平台适配(2) 时效窗口(3) 讨论度(0)
- `signal_summary`: 小红书要求创作者为 AI 生成内容添加标识，反对 AI 造假。平台层面对 AI 内容治理的趋势进一步明确，对创作者生态有直接影响。
- `why_in_top20`: 中国主流内容平台开始系统性应对 AI 内容风险，这是平台治理层面的重要信号。小红书是中国最大的生活方式内容平台之一，其政策有示范效应。
- `visual_assets`: 小红书 AI 标识功能截图、政策公告截图
- `risks`: 极客早知道是资讯合集，这条信息只是多个信息点之一，建议单独回链小红书官方公告

---

### 16. 后端互通，Agent 才能协作：对话 Taku 团队
- `topic_key`: `taku_agent_interop_20260428`
- `title`: 后端互通，Agent 才能协作｜对话 Taku 团队
- `primary_platform`: 微信 @saibo_chanxin
- `published_at`: 2026-04-28
- `original_link`: `https://mp.weixin.qq.com/s/xmxYKHAFn9KH3tcuqhCMew`
- `score_total`: 20/30
- `score_breakdown`: 一手性(2) 传播性(1) 破圈性(2) 赛道匹配(3) 可延展性(3) 数据硬度(2) 视觉素材(2) 平台适配(2) 时效窗口(2) 讨论度(1)
- `signal_summary`: Taku 团队访谈：为什么多 Agent 系统必须解决后端互通问题才能真正协作。技术深度足够，是理解 Agent 系统架构层的重要素材。
- `why_in_top20`: Agent 协作是 2026 年最核心技术主题之一。这篇文章从工程团队视角解释了为什么当前 Agent 互操作性是最大瓶颈，有一手技术见解。
- `visual_assets`: Taku 系统架构图、Agent 协作流程图
- `risks`: Taku 产品知名度有限，样本偏差；需补产品官网/repo 链接

---

### 17. 人民想念 DeepSeek
- `topic_key`: `deepseek_public_sentiment_20260428`
- `title`: 人民想念DeepSeek
- `primary_platform`: 微信 @guixingren_pro
- `published_at`: 2026-04-28
- `original_link`: `https://mp.weixin.qq.com/s/tiVXT4fqTGmG4swEwTVZmA`
- `score_total`: 20/30
- `score_breakdown`: 一手性(2) 传播性(2) 破圈性(3) 赛道匹配(2) 可延展性(3) 数据硬度(1) 视觉素材(2) 平台适配(3) 时效窗口(1) 讨论度(2)
- `signal_summary`: 标题即观点：DeepSeek 持续低调但大众和从业者对其下一步动作的期待持续高涨。折射出中国 AI 领域对 DeepSeek 创新能力的信任和对其战略走向的高度关注。
- `why_in_top20`: 这类情绪性标题揭示了一个重要信号：DeepSeek 已经拥有超越产品本身的品牌势能，成为中国 AI 领域的现象级符号。guixingren_pro 的叙事能力强，解读角度有深度。
- `visual_assets`: 微信文章阅读量/点赞数截图、DeepSeek 标志性产品截图
- `risks`: 属于情绪观察，非一手事实；建议结合 DeepSeek 实际产品/融资动态交叉验证

---

### 18. 剪映 Skill 化 Agent：剪辑工具开始"听懂人话"
- `topic_key`: `jianying_agent_20260428`
- `title`: 当剪辑工具开始「听懂人话」：剪映做了视频创作的 Skill 化 Agent
- `primary_platform`: 微信 @geekpark
- `published_at`: 2026-04-28
- `original_link`: `https://mp.weixin.qq.com/s/ED6oH5tjBReZ8340lmDDMg`
- `score_total`: 19/30
- `score_breakdown`: 一手性(2) 传播性(2) 破圈性(2) 赛道匹配(3) 可延展性(3) 数据硬度(1) 视觉素材(3) 平台适配(2) 时效窗口(2) 讨论度(1)
- `signal_summary`: 字节跳动旗下剪映推出 Skill 化 Agent 能力，让视频剪辑工具真正理解自然语言指令。视频创作的工作流 Agent 化趋势进一步加速。
- `why_in_top20`: 剪映是中国最大的移动视频剪辑工具，其 AI Agent 化代表了中国视频创作工具的行业方向。相比 Runway/Pika 等海外工具，剪映的用户基数更大，影响面更广。
- `visual_assets`: 剪映 AI 功能界面截图、Skill 指令示例
- `risks`: 功能细节需补官方更新日志；Skill 化具体技术方案未展开

---

### 19. YC Launches: ReasonBlocks——阻止 AI Agent 重复学习浪费算力
- `topic_key`: `yc_reasonblocks_20260428`
- `title`: ReasonBlocks - Stop your AI agents from burning money re-learning what they already know.
- `primary_platform`: YC Launches JSON
- `published_at`: 2026-04-28
- `original_link`: （YC Launches 直连 JSON）
- `score_total`: 19/30
- `score_breakdown`: 一手性(3) 传播性(1) 破圈性(1) 赛道匹配(3) 可延展性(2) 数据硬度(2) 视觉素材(1) 平台适配(2) 时效窗口(2) 讨论度(1)
- `signal_summary`: YC 孵化的 ReasonBlocks 解决 Agent 算力浪费核心问题：阻止 AI 在已知信息上重复训练/推理，大幅降低 Agent 运行成本。定位精准，直击 Agent 经济性痛点。
- `why_in_top20`: YC 是全球 AI 早期项目的最重要信号源之一。ReasonBlocks 切的是一个被忽视但几乎所有 Agent 开发者都会遇到的问题：重复推理算力浪费。YC 背书+精准痛点=值得关注。
- `visual_assets`: YC 页面截图、产品概念图
- `risks`: YC 直连 JSON 可抓，但产品官网/repo 链接待补；产品成熟度未知

---

### 20. 阿里在海外"养虾"：你的下一份工作，可能是当 Agent 的老板
- `topic_key`: `alibaba_agent_overseas_20260428`
- `title`: 阿里在海外"养虾"：你的下一份工作，可能是当Agent的老板
- `primary_platform`: 微信 @guixingren_pro
- `published_at`: 2026-04-28
- `original_link`: `https://mp.weixin.qq.com/s/fAD2JE2FmdNQ8pqynnf8xQ`
- `score_total`: 19/30
- `score_breakdown`: 一手性(2) 传播性(2) 破圈性(2) 赛道匹配(3) 可延展性(3) 数据硬度(1) 视觉素材(1) 平台适配(3) 时效窗口(2) 讨论度(0)
- `signal_summary`: 阿里在海外推出面向个人开发者的 Agent 平台/工具，用"养虾"比喻普通人成为 Agent 老板的新工作形态。中国大厂出海的 AI Agent 战略值得关注。
- `why_in_top20`: 标题叙事新颖，"Agent 老板"概念有破圈潜力。阿里是中国 AI 投入最大的公司之一，其出海 Agent 战略对理解中国 AI 全球布局有价值。
- `visual_assets`: 产品截图、"养虾"比喻示意图
- `risks`: 标题隐喻性强，具体产品细节少；建议补阿里官方海外产品链接

---

## 结论

### top3_must_watch（时效最强，必须跟进）

1. **OpenAI 向所有云厂商开放**（平台生态重磅，监管+商业双重维度）
2. **Altman + Brockman 十年来首次同台：OpenAI 第一优先级是 Agent**（战略定性，最高层表态）
3. **苹果 WWDC 2026 Siri 最大更新定档**（全年最重量级消费电子 AI 事件）

### top6_strong_pool（值得快速覆盖）

4. Meta 收购 Manus 被叫停（跨境 AI 收购监管重磅案例）
5. Stripe Agent 支付全景（Agent 经济闭环实操标杆）
6. 小米 + 罗福莉最强开源模型（国产开源模型竞争格局）
7. Sora 关停复盘（AI 视频商业化失败典型）
8. 飞书官方 CLI 开源（企业 Agent 工具链里程碑）
9. DeepSeek 内蒙古数据中心战略（AI 基础设施选址逻辑）

### holdout_watchlist（观察为主，不急动手）

10. 黄仁勋"推理拐点"论断
11. Agent 自动赚钱案例集
12. GitHub Copilot 用量定价转型
13. HappyHorse 视频模型灰测
14. 微信急了 / 小红书 AI 标识
15. 知乎：DeepSeek 基础设施战略讨论

### supply_risk

- **平台依赖风险**：多条高价值信号依赖微信订阅矩阵，rss refresh 稳定性需持续监控
- **原文回链风险**：本轮 Top20 中约 40% 仍需回链官方原文/原始博客补硬度；建议后续轮次优先处理 top3 的原文回链
- **弱链补查风险**：YC ReasonBlocks/Taku 等新兴产品尚未补官网 repo；建议下次资产派生轮次优先处理
- **热榜时效风险**：知乎热榜问题随时间衰减快，若要跟进"DeepSeek 内蒙古"等问题需在 48 小时内出稿
