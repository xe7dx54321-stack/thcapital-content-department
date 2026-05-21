# 同行资本市场内容系统｜2026-03-25｜弱链自动补查 resolver

## 1. 这份 runbook 是干什么的

这一步专门处理：

> **已经做过一跳对象派生，但仍然只有公司名 / 查询链、没有官网的弱链对象。**

它的核心目标不是“重新抓入口”，而是继续补一跳，把弱链尽量抬成可继续研究、可继续选题的正式对象链。

---

## 2. 主脚本

- 脚本路径：
  `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_asset_query_resolution_round.py`

---

## 3. 输入对象

当前默认只处理：

- `asset_chains/` 中最新的一版弱链
- 默认 source：
  - `trend__yc_launches_ai`
  - `web__techcrunch_ai`
  - `web__finsmes_ai_gnews`

但实际最重要的场景是：

- `FinSMEs / Google News fallback`
- 少数媒体稿里没直接给官网、只给公司名的对象

---

## 4. 输出位置

### 4.1 标准化补查结果

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/resolved/`

### 4.2 原始补查记录

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/asset_chains/resolved/raw/`

### 4.3 去重状态

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/runtime_state/market_asset_query_resolution_state.json`

---

## 5. 当前方法

### 5.1 搜索入口

- 当前升级为 **多引擎轻量补查**
- 默认组合：
  - `Bing`（经 `r.jina.ai` 包裹）
  - `DuckDuckGo HTML`
- 目的是提高弱链补官网的稳定性，降低单一搜索入口失真风险

### 5.2 查询链

- 先用对象链里已有的 `entity_name`
- 自动生成：
  - `official site`
  - `company`
  - `funding`
  - `demo`
  - `youtube demo`
- 对英文对象，额外补一轮中文查询尾巴：
  - `官网`
  - `公司`
  - `融资`
  - `产品演示`
- 如果 packet title 有额外语义，也会加入检索

### 5.3 选官网规则

- 不是看到第一个结果就直接认
- 会按：
  - 域名与实体名匹配度
  - 同域多次出现频率
  - 是否是 root domain
  - query 是否本来就在搜 official site
  - 是否明显是 publisher / social / search 噪音
  来打分

### 5.4 命中官网后的二跳补查

- 访问官网
- 从官网继续抠：
  - company social
  - founder contact
  - demo / docs / repo 候选

### 5.5 解析纪律

- 目标是优先命中官网、原始产品页、创始人或官方 docs
- 不允许把媒体稿、社交转发页、搜索结果页误认成官网
- 搜到的结果要保留 engine trail，后续复盘要能看出是哪个搜索入口命中的

---

## 6. 当前边界

- 这条 resolver 仍然是 **best-effort**
- 它最擅长补：
  - 官网
  - 公司社交
  - 下一跳入口
- 对 founder 个人账号，仍不保证每次都能稳定补全
- 对特别歧义的公司名，如果搜索结果不能稳定收敛，会保留低置信度或直接不认官网

---

## 7. 手动执行示例

### 7.1 跑一轮默认弱链补查

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_asset_query_resolution_round.py \
  --write
```

### 7.2 只补某个 source

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_asset_query_resolution_round.py \
  --write \
  --source-id web__finsmes_ai_gnews
```

### 7.3 定点补某个对象

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_asset_query_resolution_round.py \
  --write \
  --source-id web__finsmes_ai_gnews \
  --entity-name Kargo \
  --limit 1
```

---

## 8. 当前结论

现在融资 / newco 入口的链路已经从：

> 入口 → source packet → 一跳对象链

进一步补成：

> 入口 → source packet → 一跳对象链 → 弱链自动补查 resolver

它特别适合把 `query-only` 的对象继续抬成可用对象。
