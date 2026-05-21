# 平台任务单

- `date`: `2026-04-04`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-04 17:07 CST`
- `RUN_TOKEN`: `20260404`
- `input_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260404__top20-screening-pack__reworked.md`
- `top20_scorecard`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260404__top20__stage-gate-scorecard.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `Top20 scorecard=7/10，status=rework，continuity_decision=continuity_only；3个FATAL未修复前不可正式放行；本任务单按 continuity_only limited_task_sheet 执行，最多覆盖3个最重要平台，每个平台先保1个槽位`
- `rework_mode_note`: `platform-task-sheet scorecard 尚未存在（no-op），无独立 rework_mode 指令；本任务单受 Top20 rework_mode 传导约束：Top3 强保留可先行锁题，Top3 以外候补升权须等 FATAL 修复后复评`
- `morning_flash_isolation_confirmed`: `#9 Kimi「期权时光机」已从 day_mainline 永久排除，不在本任务单候选范围内`

---

## 裁判依据说明

### Top20 Scorecard 摘要（20260404 16:21 CST）
- `score`: 7/10 | `status`: rework | `continuity_decision`: `continuity_only`
- `rework_mode`: supplement_evidence + replace_topic（P1=#7无根条目优先补搜，失败则用#6 Netflix VOID替换；P2=#4 deep_article不一致须重建；P3=#12 published_at缺失须补时间戳或排除）
- `强保留对象（可直接锁题）`: #1 / #2 / #3 / #6
- `待确认（须等 FATAL 修复后复评）`: #4 / #7 / #12
- `已永久排除`: #9 Kimi（morning_flash重叠）、#10 OpenAI $1220亿（FATAL truth failure）

### 本任务单执行策略
- 按 `continuity_only limited_task_sheet` 口径：仅覆盖3个最重要平台，各保1个槽位
- Top3 强保留对象（#1 Anthropic/OpenClaw 26/30、#2 XREAL 25/30、#3 TBPN 24/30）优先锁题
- #6 Netflix VOID 已在 mini_slate 中注明"可直接用"，作为第三个平台槽位
- 其余候选进入 Holdout，等待 FATAL 修复后升权重评

---

## 全局主池 Top6（Continuity 模式下参考）

| rank | topic_key | 标题 | 综合评分 | 锁题平台 | 锁题判断 | 当前缺口 | 补证后置信度 |
|------|-----------|------|----------|----------|----------|----------|------------|
| 1 | anthropic-openclaw-block-third-party-harness-2026 | Claude封杀OpenClaw！龙虾之父回应 | 26/30 | wechat | ✅ 强保留 | 需补Peter推文原始链接+Anthropic官方邮件截图（4条路径选2条） | 高 |
| 2 | xreal-ar-glasses-ipo-hk-2026 | XREAL冲刺AR眼镜第一股：9年融22亿难盈利 | 25/30 | xiaohongshu | ✅ 强保留 | 需补HKEX招股书链接 | 高 |
| 3 | openai-acquires-tbpn-11people-30m-revenue-2026 | 11人，年入3000万美元，被OpenAI收购了 | 24/30 | 待定 | ✅ 强保留 | 需补FT口径或Altman原推全文链接 | 高 |
| 4 | netflix-void-model-huggingface-open-source-2026 | Netflix开源VOID：首个HuggingFace官方收录的Netflix模型 | 20/30 | bilibili | ✅ 强保留（mini_slate标注"可直接用"） | 官方全链路已通，Reddit评论数缺口不阻塞 | 高 |
| 5 | google-gemma-4-open-source-apache-2-business-logic-2026 | 谷歌开源Gemma 4：Apache 2.0背后的商业逻辑 | 20/30 | holdout | ⚠️ deep_article系统性不一致，须重建Apache 2.0角度深文 | Benchmark截图缺失 | 中 |
| 6 | microsoft-releases-three-own-ai-models-bypassing-openai-2026 | 微软向OpenAI说"不"？三款自研AI模型重磅发布 | 21/30 | holdout | ⚠️ source_packet路径无效（FATAL），须搜索实际文件或用Netflix VOID替换 | source_packet缺失 | 待确认 |

---

## 六个主战场任务单

### `wechat`
#### Task 1 — ✅ 已锁题
- `topic_key`: `anthropic-openclaw-block-third-party-harness-2026`
- `标题`: `Claude封杀OpenClaw！龙虾之父回应`
- `目标读者`: `AI开发者、技术创业者、投资人；对Anthropic/OpenAI竞争格局有关注的科技圈读者`
- `切入角度`: `"Anthropic封杀第三方工具 → 龙虾之父Peter现身说法 → 词元套利争议 → 订阅经济模型裂痕"，从事件还原到行业影响，适合微信深度阅读`
- `核心论点`: `①Anthropic以"词元套利"为由封杀OpenClaw等第三方harness；②Peter（OpenClaw创始人/龙虾之父）发推披露"劝了一周没用，他们先抄了我的功能然后封杀"；③这次封杀撕开了AI订阅经济的一个根本矛盾：平台到底有没有权利限制用户以机器速度使用API？`
- `证据抓手`: `HN thread #47633396已确认（320分/319评论）/ 量子位微信报道 / Peter推文（待补原始链接，content-writer须注明"据HN转载，原始推文待确认"）/ Anthropic官方邮件全文截图（待补，属一手缺口）`
- `source_ref_bundle`:
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260404_104751__hn_frontpage_47633396_tell_hn_anthropic_no_longer_allowing_claude_code_subscriptions___source-packet.md`
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260404_120256__wechat_qbitai_claude_openclaw__source-packet.md`
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260404_121733__claude封杀openclaw_龙虾之父回应__deep-article.md`
- `视觉建议`: `HN原帖截图（带分数和评论数）/ 评论区Peter推文截图 / 量子位封面图 / 可加一张"词元套利"概念示意图`
- `为什么适合该平台`: `微信是科技深度阅读最强平台；Anthropic vs 开发者圈的对立叙事 + Peter个人IP + 订阅经济争议 = 强转发动力；今日刚发生，时效性强`

#### Task 2 — 🔒 Holdout（本轮 continuity_only 模式不开放第二槽位）
- `状态`: `holdout`
- `候补题`: `openai-acquires-tbpn-11people-30m-revenue-2026`（#3 TBPN，24/30，强保留）
- `holdout理由`: `TBPN强保留，口径扎实（11人/年入3000万/Altman表态），但wechat第一槽位已锁定#1；TBPN更适合在Full Premium Pass后开放给wechat第二槽位或其他平台`
- `什么时候可捞回`: `当Top20 FATAL修复后、正式Premium Pass平台任务单下发时；或在下一业务日（20260405）优先考虑`

---

### `xiaohongshu`
#### Task 1 — ✅ 已锁题
- `topic_key`: `xreal-ar-glasses-ipo-hk-2026`
- `标题`: `XREAL冲刺AR眼镜第一股：9年融22亿难盈利，年营收5亿净亏4亿`
- `目标读者`: `小红书科技爱好者、消费电子关注者、年轻投资人；对AR/AI硬件有兴趣的C端用户`
- `切入角度`: `"9年烧22亿，销量13万台做到全球第一，但还在亏钱——XREAL凭什么冲刺AR第一股？"财务数据扎实，故事线清晰，适合小红书"科技+商业"混合调性`
- `核心论点`: `①XREAL 9年9轮融资超22亿元，阿里/快手/爱奇艺等巨头押注；②AR眼镜销量全球第一（13.4万台），但2025年仍净亏4.56亿元；③毛利率35.2%且亏损在收窄，谷歌为第二大客户+Gemini落地故事；④港股IPO是今年硬件科技重要节点`
- `证据抓手`: `招股书数据完整（浙大80后团队/9轮融资/D轮估值8.33亿美元/毛利率35.2%/海外收入71%/One系列占83%）/ 量子位封面图+14张配图`
- `source_ref_bundle`:
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260403_222304__wechat_qbitai_xreal_ar_9_22_5_4__source-packet.md`
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/20260404_121528__xreal冲刺ar眼镜第一股_9年融22亿难盈利_年营收5亿净亏4亿__deep-article.md`
- `视觉建议`: `14张微信文章配图（产品图/数据图表/融资时间轴）可直接复用 / 招股书封面截图 / 建议制作"XREAL融资历程"信息图`
- `为什么适合该平台`: `小红书用户对消费硬件、视觉系科技产品接受度高；"亏损收窄+海外7成+高毛利改善"的财务改善叙事在小红书种草力强；视觉素材极其丰富，图文并茂天然契合`

#### Task 2 — 🔒 Holdout（本轮不开放）
- `状态`: `holdout`
- `候补题`: `google-gemma-4-open-source-apache-2-business-logic-2026`（#4 Gemma 4，20/30，但deep_article系统性不一致，暂缓）
- `holdout理由`: `Gemma 4新角度Apache 2.0叙事本身适合小红书开发者群体，但deep_article仍为原标题"干掉Qwen3.5"内容，系统性内部不一致，属FATAL级别；content-writer若现在写会引用错误素材`
- `什么时候可捞回`: `等#4 deep_article重建完成（Apache 2.0角度）后，在下一轮正式任务单中优先开放小红书第二槽位`

---

### `zhihu`
#### Task 1 — 🔒 Holdout（本轮 continuity_only 模式专注3平台）
- `状态`: `holdout`
- `候补题`: `openai-acquires-tbpn-11people-30m-revenue-2026`（#3 TBPN，24/30，强保留）
- `holdout理由`: `TBPN是知乎最合适的题——"11人小团队创造3000万美元营收被OpenAI收购"，播客/媒体资产收购叙事在知乎有深度讨论空间；强保留，但wechat/xiaohongshu/bilibili三槽位已满，本轮不开放知乎`
- `什么时候可捞回`: `下一业务日（20260405）day_mainline 平台任务单中，知乎优先锁定TBPN；或等Full Premium Pass后补入`
- `平台适配备注`: `知乎用户对"AI公司买媒体资产"的政治背景（西莫主导/Altman表态）会有强讨论动力，播客独立性保留是独特条件，值得深答`

#### Task 2 — 🔒 Holdout
- `状态`: `holdout`
- `候补题`: `anthropic-private-market-moment-spacex-ipo-2026`（#8 Anthropic二级市场，19/30）
- `holdout理由`: `"Anthropic二级市场最热 vs SpaceX IPO阴影"是天然争议题，但一手数据不足（无硬财务数据），建议合并至"Anthropic商业化扩张"主题后开放知乎深答`
- `什么时候可捞回`: `等一手财务数据补全后，优先进入知乎任务池`

---

### `x`
#### Task 1 — 🔒 Holdout（本轮 continuity_only 专注3平台）
- `状态`: `holdout`
- `候补题`: `anthropic-openclaw-block-third-party-harness-2026`（#1，26/30）
- `holdout理由`: `#1 Anthropic/OpenClaw事件本身是X/Twitter原发生态（HN讨论区），在X上应该有强传播，但本轮3槽位已满`
- `什么时候可捞回`: `下一业务日20260405优先考虑；或在Full Premium Pass后正式开放X平台双槽位`
- `平台适配备注`: `X平台适合：Peter推文（补全后）/ HN thread链接 / 英文技术讨论转发；建议X平台第一槽位长期锁定#1，标题可出英文版`

#### Task 2 — 🔒 Holdout
- `状态`: `holdout`
- `候补题`: `netflix-void-model-huggingface-open-source-2026`（#6，20/30，但bilibili优先占用）
- `holdout理由`: `Netflix VOID在X上适合英文技术讨论，但bilibili优先级更高（技术视频内容匹配更强）；X平台可等待下一轮`
- `什么时候可捞回`: `20260405平台任务单中X优先开放双槽位`

---

### `bilibili`
#### Task 1 — ✅ 已锁题
- `topic_key`: `netflix-void-model-huggingface-open-source-2026`
- `标题`: `Netflix开源VOID：首个HuggingFace官方收录的Netflix模型`
- `目标读者`: `B站程序员/AI技术爱好者、开源社区关注者、视频AI从业者；对大厂开源动作有兴趣的硬核技术用户`
- `切入角度`: `"Netflix第一次在HuggingFace官方发布开源模型——VOID是做什么的？为什么是视频对象删除？大厂开源AI模型这件事本身意味着什么？"技术解析向`
- `核心论点`: `①Netflix在HuggingFace发布首个公开模型VOID（Video Object and Interaction Deletion）；②GitHub+Demo+HuggingFace三链路全通，一手性极强；③Reddit LocalLLaMA日榜第1，技术社区认可度高；④这是大厂（Netflix）首次正式在HuggingFace发布开源模型，开源生态重要信号`
- `证据抓手`: `HuggingFace官方模型页面 / GitHub repo / VOID Demo页面（sam-motamed space）/ Reddit LocalLLaMA日榜第1截图`
- `source_ref_bundle`:
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260404_093326__reddit_localllama_netflix_just_dropped_their_first_public_model_on_hugging_face_void_video__source-packet.md`
- `视觉建议`: `HuggingFace模型页面截图 / VOID Demo截图 / GitHub repo截图 / 建议制作"VOID工作流程"技术示意图`
- `为什么适合该平台`: `B站是程序员/技术向内容消费最强平台；LocalLLaMA第1=程序员社区高热；开源模型技术解析在B站有稳定受众；视频AI编辑方向可做深度技术解说`

#### Task 2 — 🔒 Holdout（本轮不开放）
- `状态`: `holdout`
- `候补题`: `google-gemma-4-open-source-apache-2-business-logic-2026`（#4，20/30）
- `holdout理由`: `Gemma 4 Apache 2.0角度适合B站技术解析，但deep_article未同步更新（仍为"干掉Qwen3.5"旧文），content-writer需要先重建素材再开工`
- `什么时候可捞回`: `等#4 deep_article重建完成后，在20260405平台任务单中优先开放bilibili第二槽位`

---

### `toutiao`
#### Task 1 — 🔒 Holdout（本轮 continuity_only 专注3平台）
- `状态`: `holdout`
- `候补题`: `openai-acquires-tbpn-11people-30m-revenue-2026`（#3，24/30，强保留）
- `holdout理由`: `头条用户群偏商业科技新闻消费者；TBPN"11人/年入3000万美元/OpenAI收购"叙事强、关注度高，适合头条算法推荐；但3槽位已满，TBPN优先给wechat和zhihu`
- `什么时候可捞回`: `Full Premium Pass后，头条优先开放TBPN；或20260405平台任务单中toutiao可优先锁定TBPN`
- `平台适配备注`: `头条平台适合：AI公司战略动向、媒体资产收购叙事；Altman发推"我并不指望TBPN对我们手下留情"是强引用锚点`

#### Task 2 — 🔒 Holdout
- `状态`: `holdout`
- `候补题`: `anthropic-subscription-credit-one-month-user-feedback-2026`（#10，17/30）
- `holdout理由`: `"一边封杀OpenClaw，一边给用户发钱"戏剧性对比在头条算法下可能表现好，但证据单薄（Reddit API 403，Settings截图缺失）`
- `什么时候可捞回`: `等Reddit评论截图和Settings证据补全后，头条可考虑补入`

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: **否，本日不需单独立项**
- `理由`: 
  - `baijiahao`是SEO镜像层，承接已发布主稿的长尾关键词流量，不主导原创选题
  - 本日3个锁题（Anthropic/OpenClaw、XREAL、Netflix VOID）在百度搜索生态中有足够关键词空间，发布后自然会进入百家号SEO池
  - 当前Top20中有强SEO题潜质：①XREAL（"XREAL IPO/AR眼镜上市"高搜索量词）；②Anthropic/OpenClaw（"Claude封杀/OpenClaw/龙虾之父"搜索热度高）
  - 但不需要单独为百家号立项——等wechat稿发布后，直接用主稿内容做SEO镜像分发即可
- `承接哪篇主稿更优`: 
  - `首选`：XREAL稿（"XREAL IPO/AR眼镜/港股上市"关键词搜索量稳定，适合SEO长尾）
  - `次选`：Anthropic/OpenClaw稿（时效性更强，热度过去后SEO价值下降较快）
- `SEO镜像执行时机`: `主稿在wechat/bilibili发布后，由publish-ops自动分发至baijiahao，无需单独立题流程`

---

## Holdout 完整清单

| topic_key | 标题 | 评分 | 为什么能进最终池 | 为什么这轮没选 | 什么时候可捞回 |
|-----------|------|------|----------------|--------------|--------------|
| openai-acquires-tbpn-11people-30m-revenue-2026 | 11人，年入3000万美元，被OpenAI收购了 | 24/30 | Top3强保留；11人叙事极强；西莫主导政治背景；Altman表态 | 本轮3槽位已满（wechat/xiaohongshu/bilibili各占1）；TBPN最适合wechat和zhihu | 20260405 day_mainline平台任务单中，wechat第二槽位或toutiao优先开放 |
| google-gemma-4-open-source-apache-2-business-logic-2026 | 谷歌开源Gemma 4：Apache 2.0背后的商业逻辑 | 20/30 | Apache 2.0叙事安全且有差异化；中美双圈讨论；谷歌开源节奏加码 | #4 deep_article系统性不一致（旧文"干掉Qwen3.5"与新角度脱节），属FATAL；content-writer无法直接开工 | 等#4 deep_article重建Apache 2.0角度完成后；预计20260404 17:30前有结果 |
| anthropic-private-market-moment-spacex-ipo-2026 | Anthropic二级市场大热 | 19/30 | "Anthropic最热私募 vs SpaceX IPO阴影"天然争议点；VC/PE圈关注 | 一手财务数据不足，建议与#5合并为"Anthropic商业化扩张"主题再开放 | 等一手财务数据补全后；与#5 Coefficient Bio合并方向 |
| anthropic-subscription-credit-one-month-user-feedback-2026 | Anthropic给用户补贴一个月订阅 | 17/30 | 与#1构成"一边封杀一边补偿"戏剧性对比；Reddit日榜第3 | Reddit API 403，Settings截图缺失；证据单薄 | 等Reddit帖子截图和Settings证据补全后 |
| microsoft-releases-three-own-ai-models-bypassing-openai-2026 | 微软三款自研AI模型 | 21/30 | 微软vs OpenAI战略分化叙事强；"说不"标题党传播性强 | FATAL：source_packet路径无效（signal-scout引用历史路径）；等待搜索结果确认 | 若当日source_packet搜索成功则保留；若失败则被#6 Netflix VOID永久替换 |
| ai-video-face-theft-taohuazan-dm takedown-2026 | AI视频"偷脸"《桃花簪》下架 | 18/30 | AI视频版权是AIGC核心法律争议；"偷脸"标签强 | 百度热榜快照来源太简；需补原始报道和《桃花簪》下架具体口径 | 等媒体报道和具体案例数据补全后 |
| alibaba-wanren-actor-model-qianwen-app-2026 | Sora向左，阿里向右 | 18/30 | 阿里vs OpenAI（Sora）是天然对比叙事；千问APP可直接体验 | source packet简；模型实测数据缺失；与Gemma 4/Qwen3.5可合并 | 等阿里官方发布信息和实测数据补全后 |
| meituan-native-multimodal-token-prediction-2026 | 美团原生多模态 | 17/30 | 美团重要大厂动态；"All Token"技术方向独特 | source packet简；需补官方研究或论文 | 等官方论文/技术解读发布后 |
| stanford-chatgpt-deception-honest-ai-killing-2026 | 斯坦福研究：ChatGPT欺骗用户 | 17/30 | "欺骗vs好评杀死诚实AI"极强叙事；斯坦福权威背书 | source packet简；需补斯坦福原始研究链接 | 等原始研究链接补全后 |
| cvpr-2026-relax-latent-space-dynamics-rl-exploration-2026 | CVPR 2026 ReLaX | 16/30 | CVPR 2026顶会论文；Token熵vs隐空间动力学RL新方向 | FATAL：published_at=unknown，无法判断时效窗口是否合规；降权排除 | 若确认CVPR 2026论文正式发表且有时间戳，可重新进入候选池 |
| yc-complir-compliance-bottleneck-retail-global-launch-2026 | YC Complir合规科技 | 16/30 | 合规科技出海细分赛道；YC正式收录信号质量高 | YC公司介绍简；需补官网和产品页 | 等Complir官网/产品数据补全后 |
| aice-power-ai-sensors-energy-bill-30-percent-2026 | YC AICE Power节能 | 15/30 | "节能30%"数字锚点强；ESG+AI方向 | YC Launch介绍简；需补官网 | 等AICE Power官网补全后 |
| yc-adapted-ai-physical-therapy-athletes-2026 | YC Adapted AI康复 | 14/30 | AI+医疗康复垂直场景；YC Launch信号 | YC Launch介绍简；需补官网和临床数据 | 等官网和临床数据补全后 |
| qwen-3.6-community-voting-huggingface-2026 | Qwen 3.6投票讨论 | 14/30 | Qwen中国开源模型代表；社区验证价值 | Reddit API 403，投票数据不完整；X上原始讨论未补 | 等X上原始讨论获取后 |

---

## FATAL 修复进度追踪（供下游参考）

| FATAL | 对象 | 问题 | 当前状态 | 预计修复时间 |
|-------|------|------|----------|------------|
| P1 | #7 微软三款自研AI模型 | source_packet引用路径无效（历史路径，不存在当日抓取文件） | 待signal-scout搜索确认 | 若搜索失败→用#6 Netflix VOID替换坑位 |
| P2 | #4 谷歌Gemma 4 | deep_article系统性内部不一致：memo改角度，deep_article仍为原"干掉Qwen3.5"旧文 | 待重建Apache 2.0角度深文 | 预计17:30前完成重建 |
| P3 | #12 CVPR ReLaX | published_at=unknown，无法判断时效窗口 | 降权排除，等待确认CVPR 2026时间戳 | 待确认 |

---

## 下一工序交接说明

- `output`: `platform-task-sheet.md`
- `下一owner`: `content-writer`
- `已锁题3个`: `#1 Anthropic/OpenClaw（wechat）/ #2 XREAL（xiaohongshu）/ #6 Netflix VOID（bilibili）`
- `触发条件`: `content-writer可立即基于本任务单3个锁题开工；无需等待FATAL修复`
- `待复评后生效`: `#4 Gemma 4 / #7 微软 / #12 CVPR ReLaX 的平台分配，在FATAL修复完成且复评通过后更新本任务单并通知content-writer`
- `deadline`: `day_mainline wechat草稿箱最终交付不得晚于当日19:00 CST；bilibili/xiaohongshu按各自平台发布节奏安排`

---

## 执行备注

- **morning_flash 隔离确认**：#9 Kimi「期权时光机」published_at=2026-04-03 18:00 CST（处于T-1 17:00→T 05:00窗口），已从 day_mainline 永久排除，不在本任务单候选范围内
- **本任务单不等同于正式 Premium Pass**：本单为 continuity_only limited_task_sheet，仅覆盖3平台×1槽位；等Top20 FATAL全部修复并复评通过后，将升级为 Full Premium Pass（6平台×2槽位）
- **不重复锁题**：本任务单显式排除了已进入 morning_flash 的同题对象，确保同一事件不会被 morning_flash 和 day_mainline 双重占用
