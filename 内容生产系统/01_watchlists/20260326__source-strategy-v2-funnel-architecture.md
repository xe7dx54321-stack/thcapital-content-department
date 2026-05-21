# 同行资本市场内容系统｜Source Strategy V2｜四层情报漏斗

## 1. 这份文档的作用

这不是“多加几个信息源”的补丁文档，而是内容工厂新的信息源总架构。

它解决三个问题：

1. 我们每天到底应该从哪里发现 AI 圈真正值得写的事件
2. 怎么把“一手事件、技术扩散、中文传播、平台热度”串成同一个事件簇
3. 为什么公众号不需要抢最早，而是要做到“快半拍 + 深一层”

核心原则：

> 不追求全网第一个发；追求第一批把意义讲清楚。

---

## 2. 四层情报漏斗

| 层级 | 名称 | 目标 | 典型信号 | 对系统的作用 |
| --- | --- | --- | --- | --- |
| `L1` | 原始信源 | 拿到一手事件和原始口径 | 官网新闻、官方博客、开发者文档、产品发布页、官方视频 | 判断“到底发生了什么”，确保事实底座不歪 |
| `L2` | 技术 / 产品扩散 | 判断技术圈、产品圈、开发者圈是否真在讨论和采用 | GitHub、HF Papers、arXiv、HN、PH、App 榜单、builder 频道 | 判断“这是不是行业真热点” |
| `L3` | 中文行业传播 | 判断中文互联网怎么讲、怎么转述、怎么放大 | 微信公众号、中文 AI 媒体、中文产品社区 | 判断“中文用户会不会关心、会被什么角度打动” |
| `L4` | 平台热度验证 | 判断是否破圈、是否值得今天正式写 | 百度热搜、B站热榜、知乎热榜、新榜、飞瓜等 | 判断“这件事今天发，胜率高不高” |

注意：

- 这 `4` 层是 **信号角色划分**，不是信息源等级。
- 任何线索都先进公共候选池，再做品牌重排。
- 相邻战场但高热、好写、易破圈的话题，不能因为不在主战场就被机械边缘化。

---

## 3. 当前系统状态

| 层级 | 当前状态 | 已落地情况 | 主要缺口 |
| --- | --- | --- | --- |
| `L1` | 偏弱 | 已有部分官方博客 / 官方视频入口 | 官方新闻页、开发文档页、硬件 / 机器人官方入口仍不够全 |
| `L2` | 中等 | 已有 Reddit、Trend Hunt、YC、部分视频创作者入口 | GitHub Trending、HF Papers、arXiv、HN、App 榜单还没形成正式主链 |
| `L3` | 最强 | 微信 RSS + 微信全文 deep capture 已打通 | 中文媒体网站面、更多公众号订阅还要继续补 |
| `L4` | 偏弱 | B站热榜已接 | 百度 / 新榜 / 飞瓜 / 知乎 / 小红书 / 微博验证层基本未系统化 |

一句话总结：

> 当前内容工厂最强的是中文传播层，最弱的是原始信源层和热度验证层。

---

## 4. 当前应该长期盯的主路径

### 4.1 `L1` 原始信源

- 模型公司官方页：OpenAI、Anthropic、Google DeepMind、xAI
- 机器人 / 具身官方页：Figure、Tesla、DeepMind Robotics
- AI 硬件官方页：NVIDIA 以及后续芯片 / 云厂商官方博客
- 高价值官方视频：OpenAI、Google DeepMind 等官方频道

### 4.2 `L2` 技术 / 产品扩散

- GitHub Trending
- Hugging Face Daily Papers
- arXiv `cs.AI recent`
- Hacker News
- Product Hunt / Trend Hunt
- App 榜单与产品增长面：点点数据、Sensor Tower
- builder / agent 频道：AI Engineer、LangChain、Latent Space、Y Combinator

### 4.3 `L3` 中文行业传播

- 微信公众号：量子位、新智元、机器之心、APPSO、Founder Park、归藏的AI工具箱、硅星人 Pro
- 中文网站面：量子位、机器之心、智东西、36氪 AI、爱范儿、少数派 AI Tag

### 4.4 `L4` 平台热度验证

- 百度热搜
- B站热榜 / B站热视频
- 新榜
- 飞瓜 B站
- 知乎热榜（后续接）
- 小红书站内搜索（后续接）
- 微博热榜 / 热度工具（后续接）

---

## 5. 事件簇，而不是来源堆积

V2 最重要的变化不是多几个 source，而是把线索收束成 **事件簇**。

一个合格的事件簇，至少要能回答：

1. `L1` 原始口径是什么
2. `L2` 技术 / 产品圈有没有真实扩散
3. `L3` 中文互联网是怎么讲的
4. `L4` 有没有破圈验证
5. 我们能不能站在不同角度把它讲得更好

系统最终不应该只说：

> “今天抓到了 20 条 source packet”

而应该说：

> “今天形成了 5 个值得竞争的事件簇，其中 2 个四层走通、1 个还缺原始信源、2 个热度高但证据不够。”

---

## 6. V2 评分机制

### 6.1 六维评分

| 维度 | 含义 | 分值 |
| --- | --- | --- |
| `first_source` | 是否有清晰的一手原始信源 | `0-3` |
| `spread` | 技术 / 产品圈是否已扩散 | `0-3` |
| `breakout` | 是否有跨平台破圈信号 | `0-3` |
| `track_fit` | 是否属于我们的五条主路径之一 | `0-3` |
| `can_we_win` | 我们是否能比别人讲得更清楚 / 更适合公域传播 | `0-3` |
| `extendability` | 能否拆成快讯、解读、复盘等多种内容形态 | `0-3` |

### 6.2 建议解释

- `14-18`：当天高优先级，优先进入 Top 5
- `10-13`：进入候选池，持续观察发酵
- `9` 以下：除非我们有明显优势，否则不建议写

### 6.3 旧评分与新评分的关系

旧评分仍保留：

- `market_score`
- `relevance_score`
- `brand_fit_score`
- `timeliness_score`
- `writeability_score`

但日常执行时，应该用 **事件簇六维评分** 当主框架，用旧评分做补充视角。

---

## 7. 每日执行节奏

| 时间 | 动作 | 目标 |
| --- | --- | --- |
| `08:00-09:00` | 刷 `L1` + `L2` | 先知道“今天新发生了什么” |
| `12:00-13:00` | 刷 `L3` | 看中文互联网开始怎么讲 |
| `17:00-18:00` | 刷 `L4` | 看是否破圈、是否值得今天正式定题 |
| `21:00` | 事件簇评分 + `Top 8 -> Top 5` | 定明天公众号头条和备选 |

注意：

- 公众号主阵地不需要每个事件都当天发
- 关键在于：**该快的时候快，该深的时候深**

---

## 8. 和当前内容工厂的接口关系

### 已经打通

- `L3` 微信 RSS：已接入
- `L3` 微信全文 deep capture：已接入
- `L4` B站热视频验证：已接入

### 下一轮优先补的

1. `L1` 官方新闻 / 官方博客 / 官方发布页主链
2. `L2` GitHub Trending / HF Papers / arXiv / HN / App 榜单
3. `L4` 百度热搜 / 新榜 / 飞瓜

---

## 9. 五条主路径怎么对应

| 主路径 | `L1` 最关键 | `L2` 最关键 | `L3` 最关键 | `L4` 最关键 |
| --- | --- | --- | --- | --- |
| 模型 | 官方 news / docs / release | GitHub、HF Papers、arXiv | 机器之心、量子位、新智元 | 百度、知乎、B站 |
| Agent | 官方产品页 / API / docs | GitHub、PH、HN、builder 频道 | 量子位、36氪 AI、Founder Park | B站、小红书、知乎 |
| 一人公司 | 官方产品页 / 创始人页 | Product Hunt、App 榜单、HN | 36氪、爱范儿、量子位 | 小红书、知乎、公众号热文 |
| 具身智能 | Figure / Tesla / DeepMind Robotics | demo 视频、论文、conference | 智东西、量子位、机器之心 | B站、微博、百度 |
| AI 硬件 | NVIDIA / 终端厂官方博客 | 行业媒体、产品榜单 | 爱范儿、36氪、智东西 | B站、小红书 |

---

## 10. Rollout 建议

### `P0`

- 用四层漏斗重写 watchlist 视角
- 用事件簇重写 topic radar 视角
- 把微信全文 deep capture 正式定义为 `L3 + 学习素材池`

### `P1`

- 接 `L1` 官方源
- 接 `L2` GitHub / HF / arXiv / HN
- 接 `L4` 百度 / 新榜 / 飞瓜

### `P2`

- 接知乎 / 小红书 / 微博的半自动验证层
- 根据平台差异，讨论是否需要“不同平台不同选题重排”

---

## 11. 索引

- 总索引：`/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/20260324__watchlist-registry-board.md`
- Web / RSS：`/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/platform_watchlists/20260324__web-rss-source-registry.md`
- 趋势入口：`/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/platform_watchlists/20260324__trend-entrance-registry.md`
- 微信源：`/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/platform_watchlists/20260324__wechat-source-registry.md`
- Topic Radar runbook：`/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/20260325__market-topic-radar-runbook.md`
- `Top 8 -> Top 5` 模板：`/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260324__top8-to-top5-topic-board-template.md`
- 事件簇模板：`/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/topic_clusters/20260324__topic-cluster-template.md`
