# Market-Scout Runtime State — 2026-05-11

**Runtime:** market-scout | **Lane:** financing / newco minimal lane
**Captured:** 2026-05-11 21:38 CST | **Sources:** trend__yc_launches_ai · web__techcrunch_ai · web__finsmes_ai_gnews

---

## 本轮执行摘要

### ✅ 已完成

| Source ID | 输出文件 | 置信度 | 状态 |
|-----------|---------|--------|------|
| trend__yc_launches_ai | 2026-05-11__signal__yc_s26_launches_may2026.md | MEDIUM（校正） | ✅ 已写 |
| web__techcrunch_ai | 2026-05-11__signal__techcrunch_ai_funding_may2026.md | MEDIUM | ✅ 已写 |
| web__finsmes_ai_gnews | 2026-05-11__signal__finsmes_ai_may2026.md | HIGH | ✅ 已写 |

### 📦 交付物

- **Top20 初筛包:** 20260511__top20-screening-pack.md
- **Source Packets (3份):** 见上表

### 🔴 重要校正

YC Summer 2026 batch **未launch**。原"May 2026 YC launches"为pre-announcement状态，Demo Day = Sep 10, 2026。任何在此日期前发布的"YC S26 launches"内容可信度存疑。本轮已对YC源做了明确置信度降级标注。

### 📊 信号统计

- FinSMEs week May 1: 120 deals total; AI占20.8%赛道
- Q1 2026 global VC ~$300B; AI ~$242B (80%), +150% YoY
- 新增今日新鲜信号: Lyrie.ai ($2M pre-seed, May 11)
- 新增高金额信号: Ineffable Intelligence ($1.1B seed)

### ⚠️ Script缺失说明

`market_topic_capture_round.py` 不存在于 `/Users/apple/Documents/同行资本市场内容系统/09_runbooks/scripts/`。现有脚本仅有：
- `market_learning_memo_builder.py`
- `market_learning_pool_board_builder.py`
- `market_wechat_deep_capture_round.py`

本轮改用 web_search + 手动结构化完成。未来如需自动化，应创建专用 capture script 或确认原 script 路径。

### 边界遵守检查

| 边界 | 状态 |
|------|------|
| 只写内容工厂目录 | ✅ |
| 不写虚拟VC运行台 | ✅ |
| intake only，不当结论 | ✅ |
| 媒体稿标注置信度 | ✅ |

### 下轮待办

- [ ] 补 Ineffable Intelligence 官网/产品
- [ ] 补 Lyrie.ai 官网/demo
- [ ] 补 QuTwo 官网
- [ ] 确认 YC S26 公司列表来源（9月前保持pre-launch状态）
