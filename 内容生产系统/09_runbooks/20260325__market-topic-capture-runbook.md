# 同行资本市场内容系统｜2026-03-25｜市场内容实时捕获主链路

## 1. 这份 runbook 的作用

这不是继续讨论“哪些源有价值”，而是把已经验证可用的入口真正接进市场内容系统的日常运行。

本轮正式落地三条线：

1. `Official update lane`
1. `Reddit discussion lane`
2. `Product discovery lane`
3. `Financing / newco minimal lane`
4. `Video signal lane`
5. `WeChat RSS lane`
6. `WeChat full-text deep-capture lane`
7. `Builder / research diffusion lane`
8. `Heat validation lane`

并且明确：

- 产物只落到 `/Users/apple/Documents/同行资本内容部门/内容生产系统/`
- 不回写 `/Users/apple/Documents/同行资本vc部门/VC系统开发规划/同行资本运行台/`
- 不把市场内容系统和研究运行台混在一起

---

## 2. 当前已经正式接入的执行器

- 当前正式 owner：`market-scout`
- 当前运行工作区：`/Users/apple/.openclaw/workspace-market-scout`
- 当前 cron 已与研究线 `data-star` 解耦，后续市场内容 intake / 发现 / 一跳派生只在内容工厂 agent 内执行
- 研究线 agent 不再承担本系统任何市场内容捕获任务

### 2.1 Reddit

- 执行逻辑：`reddit-readonly` 对应的公开 JSON 抓取链
- 运行形态：脚本直接走 Reddit public JSON
- 当前正式源：
  - `trend__reddit_localllama_daily`
  - `trend__reddit_claude_daily`
  - `trend__reddit_chatgpt_daily`

### 2.1 官方原始信源

- 当前正式源：
  - `web__openai_news`
  - `web__google_blog_ai`
  - `web__anthropic_news`
  - `web__deepmind_blog`
  - `web__xai_news`
  - `web__nvidia_blog`
  - `x__openai`
  - `x__openaidevs`
  - `x__anthropic_ai`

说明：

- 两条线都已切到官方 RSS，优先保证稳定和一手性
- 对没有稳定 RSS 的官方页，当前补了 `jina snapshot` 入口层快照
- `X` 官方账号只承担社交快信号层；硬信息仍优先回链官网 / docs / 单篇原文
- 这条 lane 的目标不是“全网最早”，而是稳定拿到模型、产品、API、平台层的重要更新
- 后续如果事件足够大，再由 topic cluster 去补中文传播层与平台热度验证层

### 2.2 Product Hunt 相关产品发现

- 执行逻辑：`find-products` 对应的 `trend-hunt` API 链
- 运行形态：脚本直接走 `trend-hunt.com/api/search`
- 当前正式源：
  - `trend__trend_hunt_ai`
  - `trend__trend_hunt_ai_agents`
  - `trend__trend_hunt_automation`

### 2.3 Financing / newco minimal lane

- 当前先接稳定可跑的 RSS / JSON / fallback 入口
- 当前正式源：
  - `trend__yc_launches_ai`
  - `web__techcrunch_ai`
  - `web__finsmes_ai_gnews`

说明：

- 这条线本轮先解决“每天有稳定的新融资 / 新产品 / 新公司入口”
- `YC Launches` 已切到直连 `launches.json`
- `FinSMEs` 官方页仍 blocked，但已经有 `Google News site-filter RSS` fallback
- 后续如要继续加深，再补官方融资公告链与 `FinSMEs` 原站直连

### 2.4 Video signal lane

- 当前正式源：
  - `youtube__openai`
  - `youtube__ycombinator`
  - `youtube__googledeepmind`
  - `youtube__aidotengineer`
  - `youtube__latent_space_pod`
  - `youtube__langchain`
  - `trend__bilibili_popular_all`

说明：

- YouTube 已支持 direct feed 和 `@handle` 自动解析成 feed
- 当前 YouTube feed 偶发 `curl 56 / peer reset`，系统已改为 soft-fail warning，不中断整轮 capture
- B站当前先走热门榜 API，并加 AI 关键词闸门
- 飞瓜 B站科技热视频榜作为第三方热视频验证源，当前放在 `Heat validation lane`，不和官方 / 直连视频入口混跑
- 视频 lane 的目标是把 demo、访谈、workflow 与中文热视频入口先转成可聚类的 source packet

### 2.5 Builder / research diffusion lane

- 当前正式源：
  - `trend__hn_frontpage`
  - `trend__github_trending`
  - `trend__arxiv_cs_ai_recent`
  - `trend__huggingface_daily_papers`
  - `web__simon_willison`
  - `web__latent_space`
  - `web__one_useful_thing`
  - `web__interconnects`
  - `web__understanding_ai`
  - `web__deeplearningai_batch`
  - `web__infoq_ai_ml`
  - `web__semianalysis`
  - `web__huggingface_blog`
  - `web__openclaw_docs`
  - `x__karpathy`
  - `x__swyx`
  - `x__hwchase17`
  - `web__jiqizhixin_site`
  - `web__qbitai_site`
  - `web__zhidx`
  - `web__36kr_ai`
  - `web__ifanr_ai`
  - `web__sspai_ai`

说明：

- 这一层负责补 `L2`：技术扩散、builder 扩散、研究社区扩散
- `HN` 和 `GitHub Trending` 更偏“builder / open-source traction”
- `HF Daily Papers` 和 `arXiv` 更偏“研究扩散 / 方法前沿”
- expert / docs / 中文网站面负责把方法论、工程经验、中文传播和产业化讨论补齐
- 这条线的目标不是直接出最终结论，而是把“今天技术圈和 builder 圈到底在热什么”稳定抓回来
- 当前 `HF Daily Papers` 已进入默认主链，但仍保留 `451` 软失败兜底，不让整轮 capture 因上游风控打红

### 2.6 Heat validation lane

- 当前正式源：
  - `trend__baidu_realtime`
  - `trend__zhihu_hotlist`
  - `trend__feigua_bilibili`
  - `trend__newrank_ai_media_rank`

说明：

- 这条线负责补 `L4`：判断 AI / agent / robotics 相关话题是否在中文大众传播、问答讨论、视频热榜和平台账号势能层形成共振
- `百度热搜` 负责看更大众的中文破圈
- `知乎热榜` 负责看问答讨论场域的用户关注点、疑问和争议
- `飞瓜 B站科技热视频榜` 负责看中文视频场域是否同步放大
- `飞瓜 B站科技热视频榜` 当前已补 `B站原视频回链`，source packet 会同时保留榜单入口和回链后的视频地址
- `新榜 AI 新媒体影响力排行榜` 不是日级热点，而是月度平台 / 竞品 / 微信生态验证层；当前公开接口原生只返回期次和榜单图片，系统已补本地 OCR，把头部账号和关键字段结构化落盘
- 所有热度源都只用于验证传播，不作为最终事实结论来源

### 2.7 WeChat RSS lane

- 当前正式源：
  - `wechat__liangziwei`
  - `wechat__xinzhiyuan`
  - `wechat__jiqizhixin`
  - `wechat__zhidx`
  - `wechat__36kr`
  - `wechat__ifanr`
  - `wechat__geekpark`
  - `wechat__founder_park`
  - `wechat__appsso`
  - `wechat__guiguang_ai_tools`
  - `wechat__guixingren_pro`

说明：

- 微信链当前走本机 `WeMP-RSS`
- 先用 `market_wechat_subscription_bootstrap.py` 补齐订阅
- 再用 `market_wechat_rss_refresh.py` 做内容工厂自己的 RSS 刷新
- 最后仍由 `market_topic_capture_round.py` 统一落标准化 source packet

### 2.8 WeChat full-text deep-capture lane

- 当前正式执行器：
  - `market_wechat_deep_capture_round.py`
- 当前正式目标：
  - 对已经进入 `source packet` 的微信文章做全文深抓
  - 尽量保留原文全文，而不是只保留 RSS 摘要
  - 为内容工厂沉淀“学习素材池”：方便后续复盘别人为什么能拿结果、怎么切题、怎么展开叙述

说明：

- 微信全文深抓不替代 RSS；RSS 负责入口广覆盖，deep capture 负责把高价值正文真正拿回系统
- 深抓优先调用本机 `x-reader`
- 落盘位置只在内容工厂目录，不回写研究线

---

## 3. 主脚本

- 脚本路径：
  `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_topic_capture_round.py`

### 3.1 手动执行示例

抓 Reddit：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_topic_capture_round.py \
  --write \
  --source-id trend__reddit_localllama_daily \
  --source-id trend__reddit_claude_daily \
  --source-id trend__reddit_chatgpt_daily
```

抓官方原始信源：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_topic_capture_round.py \
  --write \
  --source-id web__openai_news \
  --source-id web__google_blog_ai
```

抓 Product discovery：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_topic_capture_round.py \
  --write \
  --source-id trend__trend_hunt_ai \
  --source-id trend__trend_hunt_ai_agents \
  --source-id trend__trend_hunt_automation
```

抓 builder / research diffusion lane：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_topic_capture_round.py \
  --write \
  --source-id trend__hn_frontpage \
  --source-id trend__github_trending \
  --source-id trend__arxiv_cs_ai_recent
```

如需手动补抓 `HF Daily Papers`：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_topic_capture_round.py \
  --write \
  --source-id trend__huggingface_daily_papers
```

抓 financing / newco minimal lane：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_topic_capture_round.py \
  --write \
  --source-id trend__yc_launches_ai \
  --source-id web__techcrunch_ai \
  --source-id web__finsmes_ai_gnews
```

补齐微信公众号订阅：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_wechat_subscription_bootstrap.py \
  --apply \
  --write-log
```

刷新微信 RSS 半批：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_wechat_rss_refresh.py \
  --batch a \
  --write-log
```

抓 video lane：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_topic_capture_round.py \
  --write \
  --source-id youtube__openai \
  --source-id youtube__ycombinator \
  --source-id youtube__googledeepmind \
  --source-id youtube__aidotengineer \
  --source-id youtube__latent_space_pod \
  --source-id youtube__langchain \
  --source-id trend__bilibili_popular_all
```

抓 heat validation lane：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_topic_capture_round.py \
  --write \
  --source-id trend__baidu_realtime \
  --source-id trend__zhihu_hotlist \
  --source-id trend__feigua_bilibili \
  --source-id trend__newrank_ai_media_rank
```

依赖说明：

- 如需跑 `trend__newrank_ai_media_rank` 的 OCR 结构化链路，当前运行环境需要安装：

```bash
python3 -m pip install rapidocr_onnxruntime
```

抓 WeChat RSS lane：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_topic_capture_round.py \
  --write \
  --source-id wechat__liangziwei \
  --source-id wechat__xinzhiyuan \
  --source-id wechat__jiqizhixin \
  --source-id wechat__geekpark \
  --source-id wechat__founder_park \
  --source-id wechat__appsso \
  --source-id wechat__guiguang_ai_tools \
  --source-id wechat__guixingren_pro
```

抓微信公众号全文 deep capture：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_wechat_deep_capture_round.py \
  --date $(date +%F) \
  --write \
  --source-id wechat__liangziwei \
  --source-id wechat__xinzhiyuan \
  --source-id wechat__jiqizhixin \
  --source-id wechat__geekpark \
  --source-id wechat__founder_park \
  --source-id wechat__appsso \
  --source-id wechat__guiguang_ai_tools \
  --source-id wechat__guixingren_pro
```

---

## 4. 输出位置

### 4.1 原始材料

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/raw/`

### 4.2 标准化 source packet

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/`

### 4.3 运行日志

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/`

### 4.4 微信全文 deep articles

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/deep_articles/raw/`

### 4.5 去重状态

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/runtime_state/market_topic_capture_state.json`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/runtime_state/market_wechat_deep_capture_state.json`

---

## 5. 当前运行策略

先加一条新的总纪律：

> **capture 层先追求“广而可追溯”，但每个 packet 必须显式标记 source 类型、primary/source 属性、verification 状态，并同时保留 raw capture 与 distilled body。**

### 5.1 Reddit lane

- 每次抓各 subreddit 当日 top
- 附带抓 thread top comments
- 目标不是直接形成结论，而是把：
  - 真问题
  - 真吐槽
  - 真 workflow
  - 真外链对象
  抓回系统

### 5.2 Product discovery lane

- 每次抓多个 query lens
- 当前 lens：
  - `ai`
  - `ai agents`
  - `automation`
- 目标不是证明“这个产品一定好”，而是把高热产品发现入口拿回来，后续继续回链 Product Hunt / 官网 / 创始人账号

### 5.3 Financing lane

- 当前抓三类入口：
  - `YC Launches` 直连 JSON
  - `TechCrunch AI` RSS
  - `FinSMEs` 的 Google News site-filter fallback
- 目标是每天稳定获得：
  - 新融资
  - 新产品
  - 新公司
  - 大厂新动作

### 5.4 Source packet 新字段纪律

从本轮开始，每个 `source_packet` 都必须显式保留：

- `source_type`
- `primary_source`
- `verification_status`
- `raw_capture_path`
- `distilled_body`

说明：

- 热度入口可以进系统，但不能假装自己是高证据 source
- mirror / fallback / community source 必须老老实实打标
- 后续 radar 排序时，必须把热度和证据分开看

### 5.5 微信全文深抓纪律

- 微信 RSS 只是入口，不能代替正文
- 对进入内容工厂 topic radar 的微信公众号文章，要尽量补全文
- deep capture 产物至少要同时保留：
  - `source_packet_path`
  - `canonical_url`
  - `x-reader` 原始导出副本
  - 可复用的清洗正文
- 微信全文不是为了照抄，而是为了：
  - 学切题角度
  - 学结构推进
  - 学叙述和钩子
  - 支持后续做不同切口的重构

### 5.6 Heat validation enrichment 纪律

- `trend__feigua_bilibili` 的榜单热度只算传播验证，最终 packet 需要尽量回链到 `B站原视频`
- B站回链当前走公开搜索接口 + 标题 / UP 主相似度阈值；若未达到阈值，必须显式保留 `unresolved`，不能硬贴错误原视频
- `trend__newrank_ai_media_rank` 的结构化账号清单来自 `本地 OCR`，属于辅助解析层，不可替代公众号原文、账号对象池与内容复盘
- OCR 抽到的账号 / 字段可以直接进入 topic radar 作为“平台秩序与账号势能”证据，但引用时必须标注为 `OCR-assisted`

---

## 6. 去重与安全边界

### 6.1 去重

- 通过 state file 按 item key 去重
- 同一条 Reddit post / Trend Hunt product / RSS guid 默认不会重复落盘

### 6.2 系统边界

- 本脚本只负责 source intake
- 不负责 topic cluster / candidate / draft 自动推进
- 不调用旧的 VC 研究运行台
- 不把市场内容任务混进 `data-star` 的研究素材目录

---

## 7. 已知边界

### 7.1 已解决

- Reddit 日常抓取不再 blocked
- Product Hunt 官方页虽仍受限，但产品发现已能稳定运行
- `YC Launches` 已从“待研究”变成“可直接结构化抓取”
- `FinSMEs` 虽仍未直连，但已具备可运行 fallback

### 7.2 还没完全解决

- `FinSMEs` 目前仍是 Google News fallback，不是官方原站直连
- Product Hunt 官方页仍未接官方 token / 浏览器链
- 弱链补查虽然已升级为多引擎，但仍是 best-effort，不保证每次都能一步命中官网
- `新榜 AI 榜单` 当前结构化账号明细依赖本地 OCR 辅助提取，不是平台原生结构化字段；关键判断仍需结合公众号原文与账号复盘交叉验证

---

## 8. 当前结论

现在市场内容系统的 Step 3 已经从“只有 watchlist 文档”升级到：

> **有正式入口、有真实产物、有去重状态、有 cron 接法的最小可运行捕获链。**
