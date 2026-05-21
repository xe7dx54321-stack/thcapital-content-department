# 同行资本市场内容系统｜2026-03-26｜国内融资对象池评估与实施状态

## 1. 本轮最终结论

这轮之后，国内融资线不再停留在“只有评估，没有落地”的状态，而是已经拆成四层并实际跑起来：

1. **背景层已经稳定接入**
   - 源：`web__itjuzi`
   - 形态：`IT 桔子` 官方公开 PDF 报告链路
   - 作用：补中国 AI 一级市场的**规模、轮次结构、地域分布、子赛道分化**

2. **半结构化对象池已经落地**
   - 新脚本：`/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_cn_financing_object_pool_builder.py`
   - 输出目录：`/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/cn_financing_object_pool`
   - 作用：把中文入口源和资产补链结果收束成**对象卡 + 当日 board**

3. **live web 层已出现实质突破**
   - `itjuzi.com` 直连 / `Jina` / 普通 `Playwright` 链路仍会被 `412` / `400` 挡住
   - 但切到 **本机原生 Chrome + CDP 接入** 后，已可稳定进入：
     - `https://www.itjuzi.com/`
     - `https://www.itjuzi.com/company`
     - `https://www.itjuzi.com/investevent`
     - `https://www.itjuzi.com/financing_company`
   - 对应实测日志：
     - `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260326_170108__itjuzi-live-probe.md`
   - 同时确认：
     - `https://www.itjuzi.com/companies` 不是正确 live list 路径，穿透风控后会落到 `404`
   - 所以当前定义应当是：

> **国内融资背景层 + 半结构化对象池已落地；live web 层已通过本机原生 Chrome + CDP 打通，但离“稳定、无头、可批量落表的实时数据库采集器”仍有一段工程化距离。**

4. **daily updates 层已补上“当日可见更新表”**
   - 脚本：
     - `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_itjuzi_live_snapshot_builder.py`
   - 输出：
     - `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/itjuzi_live_snapshot/20260326__itjuzi-live-daily-updates.md`
     - `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/itjuzi_live_snapshot/itjuzi-live-daily-updates.csv`
   - 当前逻辑：
     - 不再按固定条数抓几条
     - 改成抓取 `investevent` 页面中 `event_date = logical_date` 的**全部可见行**
     - 每天把当日抓到的更新写入累计 CSV 台账
   - 当前验证：
     - 首页 `今日概览` 显示 `本日投资数量 = 17`
     - 当前结构化可见行 `= 5`
     - 首页 `事件列表` 额外补出 `1` 条当日结构化补充行
     - 首页 headline 额外保留 `3` 条当日补充信号
     - 因此当前系统已知当日事件信号合计 `= 9`
     - 触发第 2 页 API 后返回 `441 / 缺少令牌`

> **所以当前 daily updates 层已经落地，但它是“当日可见更新表”，不是完整数据库全量分页镜像。**

---

## 2. `IT 桔子 PDF` 与 `live database` 的核心区别

### 2.1 当前能访问到的 PDF 是什么

- 当前稳定可访问链路：
  - `https://cdn.itjuzi.com/pdf/1a5ee188cfde75809136ad47f4077d3a.pdf`
- 当前 packet：
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/source_packets/20260326_145231__itjuzi_ai_report_1a5ee188cfde75809136ad47f4077d3a_pdf__source-packet.md`
- Jina 抓到的发布时间：
  - `2025-03-12 15:46:08 CST`
- 报告内数据截止日期：
  - `2024-12-31`

### 2.2 与 live database 的本质差异

| 维度 | IT 桔子 PDF 报告 | IT 桔子 live database |
| --- | --- | --- |
| 数据粒度 | 年度 / 阶段性聚合 | 单条融资事件、单家公司页、单轮融资明细 |
| 时效性 | 报告期更新 | 理论上更接近实时 |
| 适合回答的问题 | 市场冷热、轮次结构、赛道分化、城市分布 | 今天谁融资了、融了多少、谁投的、公司基本面是什么 |
| 可否直接构造对象池 | 只能做背景层，不能做完整事件层 | 可以直接做事件层和公司层 |
| 当前容器可达性 | 已打通 | 直连 / Jina 不通，但本机原生 Chrome + CDP 已可进入 live web 页面 |

补一句更精确的话：

- 当前 `live database` 的**页面态访问**已经打通
- 当前 `live database` 的**完整分页 API** 仍要求 `Authorization token`
- 所以系统里已经有：
  - `背景层`
  - `半结构化对象池层`
  - `可见 live snapshot / daily updates 层`
- 但还没有：
  - `认证后全量分页数据库层`

### 2.3 时效性判断

按当前系统日期 `2026-03-26` 计算：

- **报告发布时间**距离现在约 `12.5 个月`
- **报告数据截止日**距离现在约 `15 个月`

所以：

- `IT 桔子 PDF` **适合做背景层**
- **不适合**承担“每日新融资对象池”的职责

换句话说，PDF 不是错的，而是**用途完全不同**

---

## 3. 已经落地的“更结构化国内融资对象池”长什么样

### 3.1 已落地脚本

- `market_cn_financing_object_pool_builder.py`

这个脚本当前会做三件事：

1. 读取中文融资相关入口 packet
   - `web__itjuzi`
   - `web__36kr_ai`
   - `web__zhidx`
   - `web__qbitai_site`
   - `web__jiqizhixin_site`
   - `web__ifanr_ai`
   - `wechat__36kr`
   - `wechat__zhidx`
   - `wechat__jiqizhixin`
   - `wechat__ifanr`

2. 抽取半结构化字段
   - 公司名
   - 轮次猜测
   - 金额猜测
   - 投资方猜测
   - 官网
   - 验证状态
   - 证据链接

3. 输出两个结果
   - `objects/*.md`：对象卡
   - `20260326__cn-financing-object-pool-board.md`：当日汇总板

### 3.2 输出目录

- 对象卡目录：
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/cn_financing_object_pool/objects`
- board：
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/cn_financing_object_pool/20260326__cn-financing-object-pool-board.md`

### 3.3 当前对象池的定义

当前对象池不是“已经等价于 IT 桔子数据库”，而是：

> **中文入口源 + IT 桔子背景层 + 资产补链结果 = 半结构化国内融资对象池**

它已经能支撑：

- 行业研究中的中国融资背景判断
- 国内项目对象的初筛、留痕和后续补料
- 后续叠加工商 / 官网 / 创始人页 / 融资沿革后，逐步升级成更强对象池

---

## 4. 当前实跑结果

本轮 dry-run 的结果是：

- `packets_scanned = 25`
- `objects_built = 1`
- 当前命中的对象：
  - `中国 AI 融资背景板`

这说明两件事：

1. **系统层已经可运行**
   - 对象池脚本是通的
   - 目录、卡片、board 的生产路径已经固定

2. **当前事件层素材仍偏弱**
   - 这不是对象池脚本没落地
   - 而是截至 `2026-03-26` 这一轮，中文入口里还没有稳定命中高置信的实时融资事件 packet

所以现状要如实定义为：

> **系统层面：对象池已经落地。**
>
> **数据层面：当前背景层强，事件层仍偏稀。**

---

## 5. 为什么当前事件层还不够强

当前还有三个瓶颈：

### 5.1 `IT 桔子` live database 还没有变成稳定采集器

- 现状：
  - HTTP / `Jina` / 普通自动化浏览器直连仍会被 `412` / `400` 挡住
  - 本机原生 Chrome + CDP 已能稳定进入 live 页面
- 影响：
  - 说明“信息访问”这一步已不是 0
  - 但还没有沉淀成适合主链自动运行的稳定、无头、结构化 collector

### 5.2 中文入口源当前更像“媒体入口”，不是“结构化数据库”

- `36氪 / 智东西 / 机器之心 / 微信` 更适合做：
  - 入口发现
  - 叙事判断
  - 补上下文
- 不适合直接当：
  - 标准化轮次库
  - 标准化金额库
  - 标准化投资方库

### 5.3 工商 / 融资沿革 / 对象层 cross-check 连接器还没补齐

后续必须补：

- `企查查 / 天眼查 / 爱企查`
- `IT 桔子 / 烯牛 / 企名片`
- 公司官网 / 官方公众号 / 创始人页

---

## 6. 当前可执行的业务使用方式

现阶段，分析师可以这样使用国内融资线：

### A. 做行业判断时

先看：

- `web__itjuzi`
- 国内融资对象池 board

目的：

- 判断赛道冷热
- 看融资是否集中在早期 / 中后期
- 看资金是否集中在少数热门子赛道

### B. 做项目对象补料时

先看：

- 对象池里的公司卡
- 对应 source packet
- asset resolution 是否已命中官网

目的：

- 判断这个对象是否值得继续补工商、团队、产品、客户、融资沿革

### C. 做 daily financing 线时

先用：

- 中文媒体 / 微信入口
- `IT 桔子` live web 页面：
  - `company`
  - `investevent`
  - `financing_company`
- `IT 桔子` daily updates：
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/itjuzi_live_snapshot/20260326__itjuzi-live-daily-updates.md`
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/02_topic_radar/itjuzi_live_snapshot/itjuzi-live-daily-updates.csv`
- 对象池收束
- 官网与公告补链

不要误以为：

- 现在已经拥有“稳定无头的国内实时融资数据库采集器”
- 当前 daily updates 已可回答“今天可见更新里有哪些对象”
- 但还不能回答“今天数据库里所有更新有哪些对象”

因为这个能力还没有完全工程化

---

## 7. 下一阶段最该补什么

优先级从高到低：

1. **把 `IT 桔子` live web 浏览器链路工程化**
   - 把“本机原生 Chrome + CDP”固化成可复跑脚本
   - 再决定是否需要登录态 / 长 session / 合法 token 管理
   - 再评估怎样把浏览器态结果稳定收束成结构化对象

2. **补国内工商 / 融资 cross-check**
   - 企查查 / 天眼查 / 爱企查
   - 烯牛 / 企名片 / 其他国内数据库

3. **把中文媒体入口升级成“入口 → 正文 → 公司对象”的三段式链路**
   - 现在很多还是入口 packet
   - 下一步要自动深抓正文，再抽对象

---

## 8. 本轮一句话定义

> **国内融资这条线已经从“空白评估”升级成“背景层 + 半结构化对象池 + 可访问的 live web 层 + 当日可见更新表层”，但离“稳定实时中国融资数据库”还差认证后分页能力与工商 cross-check 两块关键拼图。**
