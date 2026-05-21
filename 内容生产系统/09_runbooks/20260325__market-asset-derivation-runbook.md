# 同行资本市场内容系统｜2026-03-25｜对象一跳派生链

## 1. 这份 runbook 是干什么的

这一步不是继续抓“入口”，而是把入口抓回来的新对象继续往下推一跳，尽量自动补出：

1. 公司官网
2. 公司社交账号
3. founder 相关名字 / 联系方式 / 社交候选
4. demo / docs / repo / launch 页

它服务的核心目标是：

> **让“融资 / newco 入口”不只停留在一篇快讯，而是尽快长成一个可继续研究、可继续选题、可继续派生的对象链。**

---

## 2. 主脚本

- 脚本路径：
  `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_asset_derivation_round.py`

## 3. 当前默认支持的入口

- `trend__yc_launches_ai`
- `web__techcrunch_ai`
- `web__finsmes_ai_gnews`

说明：

- `YC Launches`：最强，因为能给出 launch 页 + 官方站点
- `TechCrunch AI`：次强，因为文章里常有外链能回到官方对象
- `FinSMEs fallback`：当前最弱，更多是生成对象名与查询链，后续仍需继续补官网 / 公告

---

## 4. 输出位置

### 4.1 标准化对象链

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/`

### 4.2 原始派生记录

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/raw/`

### 4.3 去重状态

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/runtime_state/market_asset_derivation_state.json`

---

## 5. 手动执行示例

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_asset_derivation_round.py \
  --write \
  --source-id trend__yc_launches_ai \
  --source-id web__techcrunch_ai \
  --source-id web__finsmes_ai_gnews
```

---

## 6. 当前策略

### 6.1 YC

- 直接读 launch detail JSON
- 拿官网、launch 页、CTA 链接、founder contact
- 再从官网抠 social / demo / docs

### 6.2 TechCrunch

- 先从文章 HTML 抽外链
- 再按公司名匹配最像官方域名的链接
- 命中官网后继续抠 company social / founder social / demo / docs
- 如果只是泛事件稿、没有明确公司 / 项目信号，就跳过，不生成误导性的对象链

### 6.3 FinSMEs fallback

- 当前更多是先拿对象名
- 如果没有直接外链官网，就先生成查询链
- 后续再靠下一轮补查把官网和 founder 补全
- 不再去抓 Google News 中间页的整页资源，避免把 gstatic / 字体 / 脚本噪音写进证据链

### 6.4 证据链清洗

- 静态资源（图片 / 字体 / css / js）默认不进入 evidence
- 社交分享链接默认过滤
- 只保留对“下一跳补查”真正有用的 article / 官网 / 官方候选链接

### 6.5 与新 packet 纪律的关系

对象一跳派生要尊重 capture 层的 `verification_status`：

- `community-signal` / `mirror-signal` / `fallback-entry` 的 packet，要优先补官网与原始来源
- `official-platform-listing` 的 packet，可以直接优先派生官网、demo、founder 线索
- 不允许把媒体稿或社区帖直接误认成 primary source

---

## 7. 边界

- 这条链是 **best-effort one-hop derivation**
- 它不保证所有对象都能一次把 founder 账号抠全
- 但它能显著减少“只知道公司名，不知道下一步去哪看”的空转

---

## 8. 当前结论

现在融资 / newco 线已经不是：

> 入口 → source packet 就停住

而是已经变成：

> 入口 → source packet → 一跳对象链

并且这条链已经接入日常 cron，位于融资 / newco 入口之后自动执行。
