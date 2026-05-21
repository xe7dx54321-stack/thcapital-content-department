# 同行资本市场内容系统｜2026-03-25｜Reddit / Product Hunt 解决方案评估

## 1. 背景

这轮不是继续停留在“Reddit / Product Hunt 很重要”这个层面，而是把候选 skill 和工具真的跑了一轮，判断：

1. 当前环境下哪个方案真能用
2. 哪个只是理论上好看
3. 哪个适合马上落到系统

---

## 2. Reddit 方案评估

| 方案 | 本轮结果 | 依赖 | 当前判断 |
| --- | --- | --- | --- |
| `reddit-readonly` | **已实测跑通** | 无额外 key | 当前最佳落地方案 |
| `search-reddit` | 已安装，但因无 `OPENAI_API_KEY` 未跑通 | `OPENAI_API_KEY` | 可作为增强层，不是当前首选 |
| `last30days` | 读过说明，适合多源趋势研究 | `OPENAI_API_KEY` / `XAI_API_KEY` 或外部 provider | 更适合后续综合研究，不是当前 Reddit 首落方案 |
| `reddit-market-insights` | 需外部 API，且偏电商痛点研究 | `REDDIT_INSIGHTS_API_KEY` | 不贴合当前 TH 用例 |
| 浏览器链 / Jina | 本轮失败或不稳定 | 浏览器 / anti-bot | 不再作为 Reddit 首选 |

### 2.1 `reddit-readonly` 实测证据

已验证：

- `posts`
- `search`
- `find`
- `thread`

而且不只是“拿到几个 URL”，还拿到了：

- 标题
- score
- 评论数
- 时间
- permalink
- 帖子摘要
- 顶层评论片段

这已经足够支撑：

- 热帖发现
- 问题归纳
- 社区情绪观察
- 进一步派生到产品 / repo / 官方对象

### 2.2 Reddit 最终落地结论

> **Reddit 这条线当前已经不再是 blocked。**

当前默认方案：

- `reddit-readonly` 作为 daily discussion lane 的执行器

增强方案：

- 等后续补上 `OPENAI_API_KEY` 后，再评估是否叠加 `search-reddit`

---

## 3. Product Hunt 方案评估

| 方案 | 本轮结果 | 依赖 | 当前判断 |
| --- | --- | --- | --- |
| official `Product Hunt` topic page | direct / Jina / browser 都不稳 | anti-bot | 继续保留战略观察位 |
| `product-hunt` | 不是抓取器，是 launch playbook | 无 | 不适合作为采集方案 |
| `product-hunt-launch` | 依赖 `PH_API_TOKEN`，偏 launch stats | `PH_API_TOKEN` | 更适合监控已知项目，不适合 daily 发现 |
| `track-upvotes` | 偏监控单个 launch 页 | 无或页面直连 | 不适合主题发现主流程 |
| `find-products` | **已实测跑通** | 无额外 key | 当前最佳 operational 替代方案 |
| `fast-browser-use-local` | 是浏览器底座，不是现成 Product Hunt 解法 | Chrome / 本地会话 | 可作为后续增强底座，但不当当前默认方案 |

### 3.1 `find-products` 为什么可用

它不是去硬怼 Product Hunt 官网页面，而是走：

- `trend-hunt.com` 的结构化搜索 API

本轮已验证：

- 可返回产品列表
- 可返回 upvotes / hype / utility / Product Hunt 链接 / 官网链接
- 无需额外 token

这意味着它已经能满足当前 TH 的核心诉求：

- 找到值得继续研究的新产品
- 初筛高热产品
- 再顺着 Product Hunt 链接与官网做派生链

### 3.2 Product Hunt 最终落地结论

> **Product Hunt 官方页当前依然没有被真正打通，但 Product Hunt 相关产品发现这件事，已经有 operational 替代方案。**

当前默认方案：

- `find-products` / `trend-hunt.com` mirror API

未来升级方案：

- Product Hunt 官方 API token
- 或本地浏览器登录态 + 更强浏览器执行器

---

## 4. 当前推荐落地

### Reddit

- 正式落地：`reddit-readonly`
- 用途：daily 热帖、问题、评论上下文、观点冲突

### Product Hunt

- 正式落地：`find-products`
- 用途：新产品发现、类别扫描、短名单生成

### 官方 Product Hunt 页

- 暂不进 main loop
- 保留为战略位，等 token / 浏览器链成熟后再接

---

## 5. 总结

这轮真正的结论不是“两个平台都彻底无阻塞”，而是：

- **Reddit：已经从 blocked 变成可正式运行**
- **Product Hunt：官方页仍高阻力，但产品发现已找到能用的替代链**

这已经足够把它们从“纸面上重要”推进到“系统里能实际工作”的阶段。
