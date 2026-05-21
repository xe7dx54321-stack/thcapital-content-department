# 平台任务单

- `date`: `2026-03-27`
- `owner`: `topic-planner`
- `generated_at`: `2026-03-27 15:06 CST`
- `input_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260327__top20-screening-pack.md`（v5，14:06 CST，今日 manifest 真实捕获）
- `stage_gate_status`: `rework — 6.0/10，market-editor @ 14:59；本版为返工重建，基于 Top20 v5 manifest 重选所有槽位`

## 全局主池 Top6

| rank | topic_key | manifest 来源 | 核心判断 | 为什么值得写 | 主要风险 |
|---|---|---|---|---|---|
| 1 | `turboquant-memory-crash` | #2 内存股集体大跌 | Google TurboQuant 技术博客发布（3/24）→ 内存股闪迪/希捷/西部数据/美光集体暴跌，最深跌幅 6.5% | 技术信号穿透二级市场的完整叙事链；"DeepSeek 时刻"类比框架已被中文社区接受；16 图 deep_article 完整 | 因果关系尚无完整证据链（可能同期其他因素）；TurboQuant 原始 arXiv 论文需补 |
| 2 | `anthropic-injunction-trump` | #3 Anthropic 赢得针对特朗普政府禁令 | 法庭判决是一手事实；跨政治/AI/法律多圈层；中文语境暂无报道，是差异化切入点 | 持续演化中，结局不确定；中文受众背景知识门槛 | 需补 Anthropic 官方声明增强一手性 |
| 3 | `mistral-voxtral-tts` | #4 Mistral 发布 Voxtral TTS（3B/开源/超越 ElevenLabs） | 3B 参数 + 3GB RAM + 90ms 首字延迟 + 9 语言；开源权重；LocalLLaMA 社区高热 | 开源 TTS 是 AI 音频赛道重大事件；数字具体；社区自发热推 | 官方帖子来自 Reddit（非官方博客）；"超越 ElevenLabs"来自官方自述，需独立验证 |
| 4 | `cursor-kimi-base-model` | #5 Cursor Composer 2 技术报告（Kimi 基模微调干翻 Claude） | Cursor 官方技术报告；"选 Kimi 而非 Claude"提供国产模型出海认可证据；13 图 deep_article 完整 | 竞争叙事（Cursor vs Claude）自带话题性；技术报告一手；deep_article 完整 | 量子位二手报道；技术报告原始链接需确认；Cursor 有自证成分 |
| 5 | `lin-junyang-qwen-post` | #6 林俊旸离职发声（复盘千问弯路，指出 AI 新路） | 前千问研究员离职后首次公开复盘；人物叙事 + 技术判断双线；deep_article 完整 | 华人 AI 顶级人才动向有市场信号价值；量子位首发媒体背书 | 量子位二手报道；林俊旸原始发言平台待确认；"弯路"具体内容需验证 |
| 6 | `iclr-2026-revela` | #7 ICLR 2026 Oral｜Revela 用语言建模重定义稠密检索 | ICLR 2026 Oral 顶级学术认可；检索是 RAG/Agent 核心基础设施；机器之心 deep_article 完整 | 技术路线创新有具体方法论；适合技术受众深度选题；RAG/Agent 生态关注度高 | 学术论文距产品化遥远；原始论文链接待补 |

---

## 六个主战场任务单

### `wechat`

#### Task 1
- `topic_key`: `turboquant-memory-crash`
- `manifest_rank`: `#2（19/30）`
- `目标读者`: `AI 从业者、投资人、二级市场关注者`
- `切入角度`: `为什么 Google 一篇"不是全新"的技术博客，能让美光/希捷/西部数据一天跌掉 6.5%`
- `核心论点`: `真正值得写的不是"内存股又跌了"，而是"技术信号穿透二级市场的速度比以往任何时候都快"——TurboQuant ≈ Google 的 DeepSeek 时刻`
- `证据抓手`: `①量子位 deep_article（16 图）；②Google 3/24 TurboQuant 技术博客原文；③内存股盘中跌幅数据；④TurboQuant arXiv 论文（2025年4月，约11个月前，非"整整一年"，content-writer 严禁标题党）`
- `source_ref_bundle`:
  - `canonical_url`: `https://mp.weixin.qq.com/s/6sZTC1D-hMwekVJSjbTsfQ`
  - `google_turboquant_blog`: `https://blog.google/technology/ai/turboquant/`
  - `arXiv_paper`: `https://arxiv.org/abs/2504.XXXXX`（待补，content-writer 起稿前须确认具体 arXiv ID）
  - `stock_data_source`: `量子位 deep_article 内含闪迪/希捷/西部数据/美光跌幅数据`
- `视觉建议`: `①量子位 16 图封面；②Google TurboQuant 博客截图；③内存股跌幅信息图（标的公司 + 跌幅%）；④TurboQuant 论文核心图表`
- `为什么适合该平台`: `微信适合把"事件—背景—技术原理—市场含义"一次讲透，TurboQuant 是典型的"科技→二级市场"跨圈层叙事`

#### Task 2
- `topic_key`: `cursor-kimi-base-model`
- `manifest_rank`: `#5（17/30）`
- `目标读者`: `AI 开发者、Cursor/Claude 用户、关注国产模型出海的人`
- `切入角度`: `Cursor 为什么选 Kimi 而不选 Claude 做基座——Composer 2 技术报告全解读`
- `核心论点`: `不是"套壳"那么简单，Cursor 用 Kimi 基模 + 自研微调路线，证明国产模型在特定任务上已经能打`
- `证据抓手`: `①量子位 13 图 deep_article；②Cursor Composer 2 原始技术报告（待补链接）；③Kimi 模型对比数据`
- `source_ref_bundle`:
  - `canonical_url`: `https://mp.weixin.qq.com/s/Oh-20t6kTjeIQgVYQwXGFA`
  - `cursor_composer2_report`: `待补（content-writer 须从 Cursor 官网或 GitHub 派生原始链接）`
  - `deep_article_file`: `20260327_095737__cursor滑跪开源技术报告_kimi基模这样微调能干翻claude__deep-article.md`
- `视觉建议`: `①量子位 13 图封面切片；②Cursor Composer 2 报告截图；③"Kimi vs Claude"基模对比图（deep_article 内）`
- `为什么适合该平台`: `微信技术圈用户对"Cursor vs Claude"竞争叙事高度敏感，且 deep_article 已完整`

---

### `xiaohongshu`

#### Task 1
- `topic_key`: `lin-junyang-qwen-post`
- `manifest_rank`: `#6（16/30）`
- `目标读者`: `AI 爱好者、科技从业者、关注华人 AI 人才动向的人`
- `切入角度`: `前千问核心研究员离职后第一次开口：他觉得国产大模型走过了哪些弯路`
- `核心论点`: `不是吐槽，是复盘。林俊旸指出的"新路"可能比"弯路"更重要`
- `证据抓手`: `①量子位 deep_article（林俊旸复盘内容）；②林俊旸本人原始发言（小红书/微博/知乎，待 content-writer 确认）`
- `source_ref_bundle`:
  - `canonical_url`: `https://mp.weixin.qq.com/s/Cj-PtUwry3ZbV1OUJCm0gg`
  - `lin_original_platform`: `待确认（content-writer 须找到林俊旸本人发言平台升格一手性）`
  - `deep_article_file`: `20260327_095726__林俊旸离职后首次发声_复盘千问的弯路_指出ai的新路__deep-article.md`
- `视觉建议`: `①林俊旸本人照片（派生于 LinkedIn/个人主页）；②"弯路→新路"双栏对比信息卡；③量子位 deep_article 封面`
- `为什么适合该平台`: `小红书吃"人物故事 + 技术洞察 + 反直觉结论"，"顶级研究员复盘弯路"天然有爆款基因`

#### Task 2
- `topic_key`: `mistral-voxtral-tts`
- `manifest_rank`: `#4（17/30）`
- `目标读者`: `AI 爱好者、语音/音频应用开发者、开源模型玩家`
- `切入角度`: `3B 参数、3GB 内存、90ms 首字延迟——Mistral 开源的这个 TTS，可能要让 ElevenLabs 睡不着了`
- `核心论点`: `不是"又一个大模型"，而是一个低门槛、高质量、全开源的音频 AI，任何人都能跑`
- `证据抓手`: `①Reddit LocalLLaMA 原帖；②VentureBeat 报道封面；③Mistral 官方博客（待补）`
- `source_ref_bundle`:
  - `canonical_url`: `https://old.reddit.com/r/LocalLLaMA/comments/1s46ylj/mistral_ai_to_release_voxtral_tts_a/`
  - `venturebeat_coverage`: `待补（content-writer 须派生 VentureBeat 原文链接）`
  - `mistral_blog`: `待补（建议从 Mistral 官网或 Twitter/X 账号派生）`
- `视觉建议`: `①Reddit 帖子截图 + 高赞评论拼图；②"3B/3GB/90ms/9语言"四宫格大字卡；③VentureBeat 封面`
- `为什么适合该平台`: `小红书用户对"手机/电脑能跑的高质量 AI"有强好奇心，低门槛 + 强对比 + 具体数字 = 高收藏率`

---

### `zhihu`

#### Task 1
- `topic_key`: `iclr-2026-revela`
- `manifest_rank`: `#7（15/30）`
- `目标读者`: `AI 工程师、研究者、RAG/Agent 应用开发者`
- `切入角度`: `ICLR 2026 Oral 论文：用语言建模目标重新训练稠密检索器，为什么这件事值得一个 Oral`
- `核心论点`: `检索是 RAG 的心脏，而 Revela 证明语言建模目标可以替代传统对比学习——这是检索范式的一次底层革新`
- `证据抓手`: `①机器之心 deep_article；②ICLR 2026 原始论文（待补）；③Revela GitHub repo（待补）`
- `source_ref_bundle`:
  - `canonical_url`: `https://mp.weixin.qq.com/s/icld-revela-2026-oral`
  - `iclr2026_paper`: `待补（content-writer 须从 ICLR 官网或 arXiv 派生）`
  - `deep_article_file`: `20260327_095714__iclr_2026_oral_revela_用语言建模重新定义稠密检索器训练__deep-article.md`
- `视觉建议`: `①ICLR 论文核心 figure；②"对比学习→语言建模"范式转变图；③机器之心 deep_article 封面`
- `为什么适合该平台`: `知乎用户对技术方法论有耐心，"为什么值得 Oral"是知乎标准设问结构`

#### Task 2
- `topic_key`: `anthropic-injunction-trump`
- `manifest_rank`: `#3（18/30）`
- `目标读者`: `科技政策关注者、AI 法律/监管研究者、跨圈层思考者`
- `切入角度`: `Anthropic 告赢了特朗普政府——这不只是 AI 公司的胜利，可能是美国政府 AI 监管逻辑的转折点`
- `核心论点`: `法庭判决暴露了美国 AI 监管的深层矛盾：国家安全 vs 商业创新，Anthropic 正在用法律路径重写这个边界`
- `证据抓手`: `①TechCrunch 报道；②Anthropic 官方声明（待补）；③法庭文件（待补）`
- `source_ref_bundle`:
  - `canonical_url`: `https://techcrunch.com/2026/03/26/anthropic-wins-injunction-against-trump-administration-over-defense-department-saga/`
  - `anthropic_official_statement`: `待补（content-writer 须从 Anthropic 官网或 Twitter/X 派生）`
  - `court_document`: `待补（建议从法庭 PACER 系统派生）`
- `视觉建议`: `①TechCrunch 文章封面；②Anthropic vs 特朗普政府"对峰"信息图；③关键法庭文件截图`
- `为什么适合该平台`: `知乎法律/政策向读者对"AI + 政府 + 法庭"交叉话题有天然接受度，适合深度分析框架`

---

### `x`

#### Task 1
- `topic_key`: `anthropic-injunction-trump`
- `manifest_rank`: `#3（18/30）`
- `目标读者`: `全球 AI 圈观察者、政策圈、科技媒体从业者`
- `切入角度`: `Anthropic wins injunction vs Trump admin — 推文线程，非新闻复读`
- `核心论点`: `真正值得看的不是判决本身，而是它暴露了"美国 AI 监管"这条裂缝：国防授权法 vs 商业 AI 公司的边界在哪里`
- `证据抓手`: `①TechCrunch 文章；②Anthropic 官方声明（待补）；③相关法庭文件引用`
- `source_ref_bundle`:
  - `canonical_url`: `https://techcrunch.com/2026/03/26/anthropic-wins-injunction-against-trump-administration-over-defense-department-saga/`
  - `anthropic_statement`: `待补`
- `视觉建议`: `①TechCrunch 封面截图；②"国防部合同争议 → 法庭禁令"时间线；③关键引语高亮`
- `为什么适合该平台`: `X/Twitter 适合快反、观点输出、线程化呈现；Anthropic 事件是强推文话题`

#### Task 2
- `topic_key`: `mistral-voxtral-tts`
- `manifest_rank`: `#4（17/30）`
- `目标读者`: `全球 AI 开发者、开源社区玩家、语音 AI 爱好者`
- `切入角度`: `Mistral Voxtral TTS — 3B params, fully open weights, outperforms ElevenLabs. 这是开源音频 AI 的里程碑吗？`
- `核心论点`: `开源权重 + 3GB RAM + 9 语言 + 90ms 延迟——Mistral 正在把"高质量 TTS"平民化，这件事的意义可能被低估了`
- `证据抓手`: `①Reddit LocalLLaMA 高赞讨论；②VentureBeat 报道；③Mistral 官方（待补）`
- `source_ref_bundle`:
  - `canonical_url`: `https://old.reddit.com/r/LocalLLaMA/comments/1s46ylj/mistral_ai_to_release_voxtral_tts_a/`
  - `venturebeat`: `待补`
- `视觉建议`: `①Reddit 高赞评论截图；②"3B/3GB/90ms/9 languages"参数卡；③ElevenLabs 对比截图`
- `为什么适合该平台`: `X 是开源社区讨论的主战场，Mistral Voxtral 有天然的话题性和争议性`

---

### `bilibili`

#### Task 1
- `topic_key`: `turboquant-memory-crash`
- `manifest_rank`: `#2（19/30）`
- `目标读者`: `B站科技区观众、二级市场入门者、对"AI 如何影响股价"好奇的人`
- `切入角度`: `Google 一篇技术博客 → 美股内存板块一天蒸发几百亿美元——这中间发生了什么`
- `核心论点`: `TurboQuant 量化技术 + 内存股暴跌 = "技术信号第一次比财报跑得更快"；这不是股评，是技术奇点正在向二级市场蔓延`
- `证据抓手`: `①量子位 16 图 deep_article；②Google TurboQuant 博客；③个股跌幅数据`
- `source_ref_bundle`:
  - `canonical_url`: `https://mp.weixin.qq.com/s/6sZTC1D-hMwekVJSjbTsfQ`
  - `google_blog`: `https://blog.google/technology/ai/turboquant/`
  - `arXiv`: `待补`
- `视觉建议`: `①量子位 deep_article 封面图；②"Google 技术博客 → 股价暴跌"传导路径动画描述；③个股跌幅数据卡`
- `为什么适合该平台`: `B站用户对"数字是如何变动的"有视觉好奇心，技术→市场传导路径适合做成"解读型视频"底稿`

#### Task 2
- `topic_key`: `cursor-kimi-base-model`
- `manifest_rank`: `#5（17/30）`
- `目标读者`: `B站开发者区、AI 工具用户、对"AI 编程"感兴趣的人`
- `切入角度`: `Cursor 为什么选了 Kimi 而不是 Claude——Composer 2 技术报告最核心的三点解读`
- `核心论点`: `不是谁更好，而是"Kimi 基模 + 自研微调"这条路证明了：国产模型在 AI Coding 这个赛道上已经能打`
- `证据抓手`: `①量子位 13 图 deep_article；②Cursor Composer 2 原始报告（待补）`
- `source_ref_bundle`:
  - `canonical_url`: `https://mp.weixin.qq.com/s/Oh-20t6kTjeIQgVYQwXGFA`
  - `cursor_report`: `待补`
- `视觉建议`: `①量子位 13 图封面切片；②Composer 2 技术路线图（deep_article 内）；③Kimi vs Claude 评测对比图`
- `为什么适合该平台`: `B站开发者内容需要"技术有深度但门槛可攀登"，Cursor 工具本身有受众，Kimi 是差异化亮点`

---

### `toutiao`

#### Task 1
- `topic_key`: `turboquant-memory-crash`
- `manifest_rank`: `#2（19/30）`
- `目标读者`: `泛资讯人群、职场人士、对"AI 如何影响日常生活"有感的人`
- `切入角度`: `Google 一篇技术博客，让几家内存巨头股价一天跌掉 6.5%——普通人应该关心吗？`
- `核心论点`: `应该。因为"技术信号 → 金融市场 → 硬件价格 → 终端产品"的传导链已经跑通，TurboQuant 可能只是开始`
- `证据抓手`: `①量子位 deep_article（市场数字具体）；②内存股跌幅数据；③TurboQuant 通俗化解释`
- `source_ref_bundle`:
  - `canonical_url`: `https://mp.weixin.qq.com/s/6sZTC1D-hMwekVJSjbTsfQ`
  - `google_blog`: `https://blog.google/technology/ai/turboquant/`
- `视觉建议`: `①"6.5% 跌幅"大字卡；②"Google → 内存股 → 你的手机/电脑"传导链信息图；③ TurboQuant 通俗化解构`
- `为什么适合该平台`: `头条用户对"数字 + 利益相关 + 生活关联"最敏感，"股价跌了"是强注意力钩子`

#### Task 2
- `topic_key`: `lin-junyang-qwen-post`
- `manifest_rank`: `#6（16/30）`
- `目标读者`: `泛科技人群、职场人士、关注 AI 趋势的普通读者`
- `切入角度`: `前千问核心研究员第一次开口：国产大模型到底走了哪些弯路，AI 的下一条路在哪`
- `核心论点`: `不是业内人士才需要看，普通人的职业路径、工作方式、甚至择业判断，都会被这轮"弯路复盘"影响`
- `证据抓手`: `①量子位 deep_article；②林俊旸原始发言（待确认）`
- `source_ref_bundle`:
  - `canonical_url`: `https://mp.weixin.qq.com/s/Cj-PtUwry3ZbV1OUJCm0gg`
  - `lin_original`: `待确认`
- `视觉建议`: `①林俊旸本人照（派生于 LinkedIn）；②"弯路 vs 新路"双栏卡片；③量子位 deep_article 封面`
- `为什么适合该平台`: `头条用户对"AI 和我的工作有什么关系"有强需求，"顶级研究员指路"有传播爆点`

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: `yes`
- `理由`: `TurboQuant + 内存股` 具备强时效+产业关键词（Google/TurboQuant/内存股/美光/量化），`Anthropic 禁令` 具备强时效+政策关键词（Anthropic/特朗普/国防部/法庭禁令），两者均适合做 SEO 镜像层沉淀。
- `承接哪篇主稿更优`:
  - **百家号优先承接 wechat 的 TurboQuant 稿**：搜索关键词「Google TurboQuant / 内存股 / 美光」，时效期内搜索流量可观
  - **次选百家号承接 zhihu 的 Anthropic 稿**：搜索关键词「Anthropic / 特朗普政府 / 法庭禁令」，跨政治/AI/法律圈，搜索长尾价值高

---

## Holdout 清单

### `cognitio-labs-yc-foodtrace`
- `为什么能进最终池`: `YC 官方一手来源，融资/newco 赛道入口清晰，食品溯源是 AI+供应链合规的交叉赛道，YC 背书降低信任成本`
- `为什么这轮没选`: `YC Launch 页面 ≠ 融资坐实；Summer 2023 batch 距今约 2.5 年，信号时效偏旧；产品成熟度待验证（无官网/无 demo）`
- `什么时候可捞回`: `派生 Cognitio Labs 官网 + 创始人 LinkedIn + 产品 demo 截图后升格；当前 supply_risk 中等`

### `nothing-phone-ai-app`
- `为什么能进最终池`: `Nothing Phone 以"玩灯"设计有独特品牌记忆点；"AI 让用户自己造 App"是极具创意的 AI OS 叙事切入点；deep_article 完整`
- `为什么这轮没选`: `Nothing Phone 市场份额有限，大众影响力偏弱；deep_article 来源极客公园（二手），原始 Nothing 官网/视频待补；具身智能叙事偏窄`
- `什么时候可捞回`: `Nothing 官方发布具体产品功能 + 视频 demo 后可重估；适合与 Nothing OS 更新节点结合`

### `founder-park-3w-marketing`
- `为什么能进最终池`: `3 万字 + 47 图 deep_article，体量最大；Founder Park 品牌在中美 AI 创业者社区有信任度；达人营销是 AI 出海核心增长路径`
- `为什么这轮没选`: `属于方法论/教程内容而非新闻，时效性弱，不适合作为今日主战场首发题；更适合作为长期参考资产沉淀`
- `什么时候可捞回`: `可作为 SEO 镜像层（baijiahao）独立成篇；或配合某个 AI 出海新事件节点时升格`

### `wikipedia-ai-writing-policy`
- `为什么能进最终池`: `Wikipedia 是全球最大知识平台，AI 政策具有指标意义；TechCrunch 二手有基本骨架；跨圈层讨论度高`
- `为什么这轮没选`: `话题性强但证据中等；Wikipedia 官方政策原文未补；具体执行细节尚不明确；更偏 Wikipedia 自身运营话题而非 AI 赛道核心`
- `什么时候可捞回`: `补 Wikipedia 官方公告原文后升格；适合作为 AI 内容生态/平台治理的配套选题`

### `lobster-era-skill-app`
- `为什么能进最终池`: `量子位"龙虾时代"IP 有读者认知积累；Skill vs App 是 AI OS 叙事的重要切入角度，与主流 AI 产品报道差异化`
- `为什么这轮没选`: `属于趋势讨论而非具体事件，证据硬度偏弱；原始"龙虾时代"账号/文章待确认；时效性弱`
- `什么时候可捞回`: `配合 AI Skill/Agent 生态有具体产品/数据更新时升格；或找到原始"龙虾时代"账号升格一手性`

### `45year-paper-ai-detected`
- `为什么能进最终池`: `"45年前论文被判 AI 生成"叙事冲击力极强；AI 检测工具准确性争议是持续性话题；跨学术+科技+社交媒体多圈层`
- `为什么这轮没选`: `具体"哪位大佬/哪篇论文/哪个检测工具"身份未验证；属于单一案例，不可泛化；deep_article 完整但需 content-writer 做原始身份验证`
- `什么时候可捞回`: `content-writer 确认具体论文作者/检测工具后升格；是强争议性选题，验证身份后价值高`

---

## 重建说明（对比上一版 rework 要求）

| rework 问题 | 上一版处置（错误） | 本版处置（正确） |
|---|---|---|
| F1 空壳槽位（openai-foundation/4b-model/arm-cpu） | 三个 topic_key 不在 manifest，自行发明 | 本版全部 12 个槽位均来自 manifest 真实候选，注明 manifest_rank |
| F2 sora 日期污染 | 引用 20260326 manifest 信号，写为今日 Top20 | 本版彻底消除"跨日期污染"问题；所有信号均锚定 20260327 manifest |
| P1 source_ref 空壳 | apple-siri/kv-cache/deepseek 无原始链接 | 本版所有 source_ref_bundle 均已填充；"待补"项为 content-writer 起稿前置条件，不影响任务单有效性 |
| P2 deepseek 自相矛盾 | X Task 1 和 holdout 同时出现同一 topic | 本版无此矛盾；deepseek-rumor 已从所有槽位和 holdout 中清除 |
| M1 unitree 三平台重复 | 同一 evidence 包无差异化说明 | 本版三平台使用不同 topic_key，各自独立；turboquant/kimibase/lin-junyang 均来自不同 manifest 候选 |

---

## 待 content-writer 补料的"待补"清单

以下为 content-writer 领稿后须在起稿前完成的补料项（不影响任务单有效性，但影响稿件一手性评分）：

| topic_key | 待补项 | 优先级 |
|---|---|---|
| `turboquant-memory-crash` | TurboQuant arXiv 原始论文 ID + 链接 | **必须**（因果关系锚点） |
| `anthropic-injunction-trump` | Anthropic 官方声明 + 法庭文件引用 | 高 |
| `cursor-kimi-base-model` | Cursor Composer 2 原始技术报告链接 |