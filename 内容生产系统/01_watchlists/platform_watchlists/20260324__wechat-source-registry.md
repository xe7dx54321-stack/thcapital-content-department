# 同行资本市场内容系统｜微信公众号 Source Registry

## 1. 用途

记录微信公众号、微信文章聚合入口等需要长期监控的 source。

适合收录：

- 媒体号
- 行业观察号
- 创业者 / 投资人公众号
- 工具 / 产品官方号

---

## 2. 表结构

| source_key | source_name | source_type | handle_or_url | region | language | signal_quality | citation_reliability | capture_method | status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| wechat__liangziwei | 量子位 | media | wechat://量子位 | cn | zh | high | medium | wechat-rss / wemp-bootstrap | active | 已接入内容工厂微信链，AI 大盘和热点快讯覆盖全 |
| wechat__xinzhiyuan | 新智元 | media | wechat://新智元 | cn | zh | high | medium | wechat-rss / wemp-bootstrap | active | 已补订阅并接入，模型、产品、行业事件密度高 |
| wechat__jiqizhixin | 机器之心 | media | wechat://机器之心 | cn | zh | high | medium | wechat-rss / wemp-bootstrap | active | 已接入内容工厂微信链，研究与产业报道较全 |
| wechat__geekpark | 极客公园 | media | wechat://极客公园 | cn | zh | medium | medium | wechat-rss / wemp-bootstrap | active | 已接入内容工厂微信链，产品和创业叙事更强 |
| wechat__founder_park | Founder Park | media | wechat://Founder Park | cn | zh | high | medium | wechat-rss / wemp-bootstrap | active | 已接入内容工厂微信链，创业者和 AI 产品观察质量高 |
| wechat__appsso | APPSO | media | wechat://APPSO | cn | zh | medium | medium | wechat-rss / wemp-bootstrap | active | 已补订阅并接入，大众产品热点和传播型题材较多 |
| wechat__guiguang_ai_tools | 归藏的AI工具箱 | kol | wechat://归藏的AI工具箱 | cn | zh | medium | low | wechat-rss / wemp-bootstrap | active | 已补订阅并接入，工具测评 / 教学 / 玩法线索有价值 |
| wechat__guixingren_pro | 硅星人Pro | media | wechat://硅星人Pro | cn | zh | medium | medium | wechat-rss / wemp-bootstrap | active | 已补订阅并接入，海外 AI 创业和产品语境补充强 |
| wechat__zhidx | 智东西 | media | wechat://智东西 | cn | zh | high | medium | wechat-rss / wemp-bootstrap | active | 已验证订阅存在并抓到正文入口，适合产业化、具身、硬件题材 |
| wechat__36kr | 36氪 | media | wechat://36氪 | cn | zh | medium | medium | wechat-rss / wemp-bootstrap | active | 已补订阅并验证抓取，适合创业、融资、产品化与商业化叙事补充 |
| wechat__ifanr | 爱范儿 | media | wechat://爱范儿 | cn | zh | medium | medium | wechat-rss / wemp-bootstrap | active | 已补订阅并验证抓取，适合消费产品、AI 硬件与大众传播型题材补充 |

---

## 3. V2 备注

- 本表中的 `active` 微信源已经同时进入：
  - `L3 中文行业传播层`
  - `微信全文 deep capture 学习素材池`
- 对公众号来说，微信源不只是拿线索，还要拿：
  - 标题写法
  - 切题角度
  - 结构推进
  - 钩子与结尾处理
