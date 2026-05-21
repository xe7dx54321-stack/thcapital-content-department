# 同行资本市场内容系统｜2026-03-25 Seed 重选策略

## 1. 文档目的

这份文档用于把 Step 3 的 `starter seeds` 从“技术占位样本”升级成一版更接近真实业务的 seed 方案。

这次重选不再只按平台随便塞几个账号，而是改成：

> **先按发现路径设计，再把其中适合长期盯的入口落成正式 watchlist。**

---

## 2. 这轮重选的几个硬原则

### 2.1 先尊重市场，再做品牌筛选

source 层只解决一件事：

> **把值得看的信号尽量抓回来。**

它不负责提前压制“不是主战场”的内容。

主战场 / 邻接战场的取舍，放在后面的 Top 8 → Top 5 推荐阶段。

### 2.2 固定种子和动态规则要分开管理

不是所有高价值入口都能被写成固定 URL。

例如：

- 每天 agent 融资线索
- Reddit 当日最热 10 个讨论
- 几天内播放量暴涨的视频
- GitHub 72 小时 star 增长最快的 agent 项目

这类东西本质上是**动态发现规则**，不是单一 source。

因此这轮要把两类对象拆开：

1. **固定 seeds**：适合直接写进 registry，长期盯
2. **动态 scouting rules**：适合写进 skill，让 agent 按规则去找，再把结果回填候选池

### 2.3 业务上高价值，不代表技术上适合先入正式盘

所以本轮把 seeds 分成三层：

- **A 类：技术友好 + 高价值**
  - 直接进正式 watchlist
  - 适合每天跑
- **B 类：高价值 + 高阻力**
  - 业务上必须盯
  - 但抓取依赖浏览器、登录态、特殊 reader 或更强工具链
- **C 类：人工补录 / 待核验短名单**
  - 值得观察
  - 但当前还不适合直接当默认机器入口

### 2.4 发现路径要能往下延伸，而不是只停留在入口

真正有价值的不是“看到一条热点”，而是从热点继续展开：

- 谁融了资
- 公司官网是什么
- 创始人在哪发观点
- 有没有 demo / 视频 / 文档 / GitHub
- 社区里怎么讨论
- 这个方向能不能反推成更值得写的题

所以每条发现路径都要配一条**延伸链**。

---

## 3. 本轮采用的 9 条发现路径

| lane_key | 主要目标 | 代表性入口类型 | 发现后的延伸动作 | 主要价值 | 技术备注 |
| --- | --- | --- | --- | --- | --- |
| `financing_newco` | 找新项目、新融资、新公司 | YC Launches、TechCrunch AI、Product Hunt、融资新闻 | 从项目名继续找官网、创始人 X、YouTube demo、产品文档、GitHub | 最容易挖出“新业务 / 新产品 / 新 idea” | 很多入口不稳定，适合“入口 + 派生链” |
| `expert_view` | 找大神观点、方法论、争议点 | Simon、Latent Space、Karpathy、swyx 等 | 继续找评论、被提到的产品、相关案例、对立观点 | 适合做观点拆解、方法论类内容 | 观点源不能直接当事实证据 |
| `reddit_discussion` | 找真实问题、真实反馈、真实吐槽 | LocalLLaMA、ClaudeAI、ChatGPT 等 | 汇总原帖 + 高赞评论，再去找对应产品/解决方案 | 适合做“为什么热 / 真问题是什么 / 谁在解决” | Reddit 对直接抓取不友好，属于 B 类 |
| `breakout_growth` | 找正在快速变热的话题 | HN frontpage、GitHub Trending、Product Hunt、B 站热门 | 找原始事件、多个角度解读、不同平台扩散证据 | 适合做当天热点和多热点合并 | 趋势入口只证明“热”，不证明“真” |
| `video_demo` | 找演示型、教学型、爆款视频 | YouTube、B 站、官方频道、头部 up 主 | 从视频内容反找原始链接、项目官网、演示工具、作者账号 | 适合做“可视化强、容易传播”的题 | 视频转录可用，但平台入口要分开维护 |
| `official_updates` | 找模型、平台、agent infra 一手变化 | OpenAI、Anthropic、DeepMind、Google AI 等 | 继续找开发者解读、社区反馈、落地案例 | 适合做“为什么这次更新重要” | 官方源权威高，但有些站会被反爬 |
| `wechat_cn_ai` | 找中文 AI 圈高频讨论点 | 公众号媒体号、观察号、工具号 | 继续找原始英文源、竞品视角、空白角度 | 适合做中文语境转译和选题本地化 | 依赖现有微信链或人工核验 |
| `open_source_skill` | 找工具链、skill、workflow 新热点 | GitHub Trending、ClawHub、OpenClaw docs、Hugging Face | 延伸到 repo、文档、作者账号、教程视频 | 适合做“这个工具解决什么问题、能跑什么业务” | 很适合形成可复用内容模版 |
| `build_in_public` | 找一人公司、agent business、快速验证案例 | YC、X、YouTube、创业者博客 | 继续找商业模式、增长路径、stack、创始人观点 | 最契合 TH 自身 build-in-public 叙事 | 很多线索分散在多个平台 |

---

## 4. 每条发现路径应该怎么落地

### 4.1 融资 / 新项目路径

默认动作不是“抓一篇融资新闻就结束”，而是：

1. 先拿到项目名 / 公司名
2. 找官网
3. 找创始人 / 官方 X
4. 找 YouTube demo / 产品演示
5. 找 GitHub / 文档 / 定价页 / ClawHub / App 页面
6. 找社区讨论

最后形成的应该不是一条材料，而是一组可持续跟踪的对象。

### 4.2 大神观点路径

默认动作不是“转述大神发了什么”，而是：

1. 原观点是什么
2. 为什么引发讨论
3. 评论区里有没有共识 / 争议点
4. 能不能延伸到具体产品、具体 workflow、具体 business

### 4.3 Reddit 路径

Reddit 的价值不在于“官方权威”，而在于：

- 真问题
- 真反馈
- 真情绪
- 真使用场景

因此它更像问题发现器和题感放大器，不应该被当成事实主证据。

### 4.4 视频路径

视频不是为了“复述视频内容”，而是为了反向找到：

- 原始信息源
- 更适合图文表达的角度
- 另一种切口
- 相关产品或技能

### 4.5 开源 / Skill 路径

对于 GitHub / ClawHub / OpenClaw / Hugging Face 这类入口，重点不是简单追星，而是判断：

1. 解决了什么问题
2. 这个问题为什么现在值得被解决
3. 能应用在哪种业务里
4. 是否能与最近的热点事件合并成更强选题

---

## 5. 固定 seeds 与动态 scouting rules 的分工

### 5.1 适合写成固定 seed 的

- 稳定存在的官网、博客、栏目页
- 稳定存在的频道 / 账号
- 稳定存在的榜单页 / 入口页

### 5.2 不适合硬写成固定 URL 的

- 每日融资事件集合
- 每日最热视频集合
- 72 小时 star 增长最快项目
- 某平台当日评论增速最快的主题

这类内容应该用 skill 去描述“怎么找”，而不是硬伪装成一个固定 source。

---

## 6. 派生 source 的创建规则

当某条发现路径命中了一个**值得继续追的实体**时，agent 应该继续创建派生 source 候选。

推荐顺序：

1. `company official site`
2. `founder / company x handle`
3. `youtube channel / demo video`
4. `docs / blog / changelog`
5. `github / open-source repo`
6. `community discussion entrance`

也就是说：

> **入口负责发现，派生链负责把这个对象吃透。**

---

## 7. 本轮重选的输出对象

本轮已经同步落下：

1. 正式的 seed 候选池文档  
   `/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/20260325__seed-candidate-pool.md`

2. 更新后的 platform registries

3. 新的动态 scouting skill  
   `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/skills/th-seed-refresh-and-source-scouting/SKILL.md`

---

## 8. 本轮策略结论

这轮的核心变化只有一句话：

> **source 不再按“像不像我们”来收，而是按“能不能帮我们更快发现值得写的题”来收。**

同时再通过：

- A / B / C 三层分级
- 动态 scouting rule
- 派生 source 链

把“广泛发现”和“可执行落地”统一起来。
