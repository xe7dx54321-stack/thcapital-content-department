# Market Asset Derivation — 2026-05-17 Evening Round

## 执行记录

**时间**: 2026-05-17 19:58 (Asia/Shanghai)  
**执行者**: market-scout cron (signal-scout runtime)  
**触发**: cron job `8f0d4d49-7e9c-4f64-a61d-4a45d4818d63`

## 脚本状态

- `market_asset_derivation_round.py` 不存在于 `/Users/apple/Documents/同行资本市场内容系统/09_runbooks/scripts/`
- **处理方式**: 手动执行派生逻辑，等效覆盖 source-packet 扫描 → 对象一跳派生 → asset chain 输出全流程

## 源覆盖情况

| source-id | 今日存在 | 备注 |
|---|---|---|
| `trend__yc_launches_ai` | ❌ 无对应 packet | 无 YC 相关抓取记录 |
| `web__techcrunch_ai` | ✅ 存在 | 已扫描 |
| `web__finsmes_ai_gnews` | ❌ 无对应 packet | 无 Finsmes 相关抓取记录 |

## 扫描结果

从 `web__techcrunch_ai` (score ≥ 8 筛选):

| 对象 | score | 信号类型 | 处理结果 |
|---|---|---|---|
| Nectar Social ($30M Series A, Menlo) | 10 | 融资 + 明确公司/产品 | ✅ 已在今早晨间处理，asset chain 已生成 |
| Osaurus (macOS 本地 AI server) | 10 | 明确公司/产品 + 开源项目 | ✅ 本轮新增派生 |
| OpenAI ChatGPT Finance (launch) | 20 | 新产品信号 | ⚠️ 已有 asset chain (20260516__OpenAI__ChatGPT_Finance_launch.json)，沿用 |
| RJ Scaringe / 3 startups | 10 | 融资信号 | ⚠️ 泛人物稿，跳过 |
| Greg Brockman (OpenAI) | 10 | 人事信号 | ⚠️ 泛人物稿，跳过 |
| Runway vs Google | 5 | 泛公司报道 | ⚠️ 已有 asset chain，跳过 |
| Meridian Ventures ($35M fund) | 15 | 新基金信号 | ⚠️ 投资方信号而非 newco，跳过 |
| Rapido ($240M, $3B) | 5 | 融资信号 | ⚠️ 印度公司，规模大有现有知名度，跳过 |
| Cerebras ($60B) | 5 | 泛公司深度报道 | ⚠️ 已有资产，跳过 |

**HN 来源**: `trend__hn_frontpage` 扫描 (score ≥ 5 或 pts ≥ 100):

| 对象 | 热度 | 处理结果 |
|---|---|---|
| Zerostack (Rust coding agent) | 267pts/95cmts | ⚠️ 开源工具包，无明确公司/产品实体，跳过 |
| SANA-WM (open world model) | 320pts/132cmts | ⚠️ 学术项目(nvlab)，无公司，跳过 |
| Fisker → open source car | 101pts/37cmts | ⚠️ 事件追踪稿，跳过 |
| 其他 | — | 无 score ≥ 8 或强融资信号 |

## 本轮新增 Asset Chain

### 1. `20260517__Osaurus__mac_ai_server.json`

**对象**: Osaurus  
**赛道**: Local-First AI Infrastructure / macOS LLM Server  
**信号**: TC 报道 + GitHub 5.3k stars + 115k downloads + ex-Tesla/Netflix 创始人  

**链路完成度**: ✅ 完全链接
- 官网: https://osaurus.ai ✅
- GitHub org: https://github.com/osaurus-ai ✅
- Main repo: https://github.com/osaurus-ai/osaurus ✅ (5.3k stars, MIT)
- Blog: https://osaurus.ai/blog ✅ (4 posts)
- Product download: https://github.com/osaurus-ai/osaurus/releases/latest ✅
- Visual materials: GitHub README screenshot ✅

**弱链**: Twitter @OsaurusAI (blog 提及，未独立验证)  
**融资**: 未披露；无 VC 轮次公开  
**内容叙事潜力**: 高 – "Mac 原生 AI 基础设施"定位清晰，开源+隐私叙事契合当下极客关注

### 2. Nectar Social — 沿用今早晨间版本

**文件**: `20260517__Nectar_Social__30m_series_a.json` (已生成于 2026-05-17 08:47 UTC)

**链路状态**: 官网弱链(DNS 解析成功但 TCP 超时)，其余 Business Wire PR + LinkedIn + TC 原文均可用  
**非阻断原因**: 融资事实由双源确认，Menlo/Anthology 背书足够确立公司真实性

## 跳过对象说明

以下今日来源中的高 score 条目，按 runbook 规则跳过：

| 对象 | 跳过理由 |
|---|---|
| Greg Brockman / OpenAI 人事 | 泛人物稿，无明确 newco/产品入口 |
| RJ Scaringe 三轮融资 | 连续创业者融资聚合，非单一 newco |
| Cerebras $60B | 成熟公司深度报道，无 newco 入口 |
| Tesla Robotaxi crashes | 事件稿，无明确 newco/产品信号 |
| Runway vs Google | 已有 asset chain，泛公司报道 |
| Rapido $240M | 印度大公司，有知名度，非 newco |
| Meridian Ventures $35M | 投资方信号，不是 newco |
| ArXiv ban policy | 平台政策报道，无公司/产品信号 |
| Zerostack | 开源工具包，无明确公司实体 |
| SANA-WM | 学术项目(nvlab)，无公司/商业化信号 |

## 边界检查

✅ 未写入 `/Users/apple/Documents/虚拟vc项目开发规划/同行资本运行台/`  
✅ 泛事件稿已跳过  
✅ 弱链已有 query chain，不强行降级为 blocker  
✅ 只在内容工厂目录中输出

## 下一步建议

1. `topic-planner` 可消费今日两个 asset chain (Nectar Social / Osaurus) 作为选题候选
2. Osaurus 若需 Twitter 验证可纳入补查；非 blocker
3. `web__finsmes_ai_gnews` 和 `trend__yc_launches_ai` 若后续抓取到，应触发新一轮派生扫描