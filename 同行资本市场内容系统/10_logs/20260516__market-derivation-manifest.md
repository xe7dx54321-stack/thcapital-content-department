# Derivation Manifest 2026-05-16

**运行时**: market-scout | 2026-05-16 08:44 CST
**触发源**: cron market_asset_derivation_round (script absent; executed manually)
**抓取输入**: `20260516__src-web__techcrunch_ai.json` (14 items from TechCrunch AI feed)
**其他源**: `trend__yc_launches_ai` (0 entries), `web__finsmes_ai_gnews` (0 entries)

---

## 派生结果：4个对象链

### 1. Osaurus — macOS AI Server (新co)
- **TC标题**: Osaurus brings both local and cloud AI models to your Mac
- **信号**: score=10 / 新产品信号
- **官网**: ✅ osaurus.ai (live, product清晰)
- **GitHub**: ✅ github.com/osaurus-ai/osaurus (114k downloads, 5.3k stars)
- **创始人**: ✅ LinkedIn → Terence Pae (ex-Tesla/Netflix)
- **弱链补查**: docs site / demo video / X账号
- **资产路径**: `asset_chains/20260516__Osaurus__mac_ai_server.json`

### 2. OpenAI ChatGPT Finance — 产品功能发布
- **TC标题**: OpenAI launches ChatGPT for personal finance, will let you connect bank accounts
- **信号**: score=20 / 新产品信号
- **关键链**: Plaid 集成 → 12,000+ 金融机构；Hiro 团队收购 (April 2026)
- **资产路径**: `asset_chains/20260516__OpenAI__ChatGPT_Finance_launch.json`

### 3. Runway — World Models 对标 Google
- **TC标题**: Runway started by helping filmmakers — now it wants to beat Google at AI
- **信号**: score=5 / 无明确新公司信号（已有知名公司战略叙事）
- **关键链**: 官网 runwayml.com → GWM-1 world model; Gen-4.5
- **资产路径**: `asset_chains/20260516__Runway__world_models_vs_google.json`

### 4. Rapido — 印度$240M融资
- **TC标题**: Indian Uber rival Rapido raises $240M at $3B valuation
- **信号**: score=5 / 非新公司（已有强信号融资事件）
- **关键链**: rapido.bike (官网JS强); app store; wikipedia
- **资产路径**: `asset_chains/20260516__Rapido__240M_series.json`

---

## 跳过对象（无明确公司/项目信号）

| # | TC标题 | 跳过原因 |
|---|--------|---------|
| 1 | RJ Scaringe has raised >$12B across three startups | 人物叙事，非具体公司/项目 |
| 2 | General Catalyst posted VC rage bait | VC机构文章，无新公司信号 |
| 3 | Tesla reveals two Robotaxi crashes | 已有公司负面事件，无新产品信号 |
| 4 | US orders travelers on Air Force One to throw away gifts | 地缘政治事件，无创业公司信号 |
| 5 | OpenAI says Codex is coming to your phone | 已有产品功能扩展，非新公司 |
| 6 | What happens when AI starts building itself? | 哲学/趋势文章，无公司信号 |
| 7 | OpenAI reportedly preparing legal action vs Apple | 持续性法律争议，无新公司信号 |
| 8 | Meridian Ventures – $35M fund | VC基金，非创业公司 |
| 9 | Elon Musk's SpaceXAI bleeding staff | 已有公司内部报道，无新产品信号 |
| 10 | Silicon Valley vacationland energy provider | 基础设施/能源政策分析，非公司/产品 |

---

## YC Launches / FinSMEs 空结果说明

- **trend__yc_launches_ai**: 今日manifest记录 0 entries，YC launches 页面抓取无回源（可能反爬或当日无新 batch 发布）
- **web__finsmes_ai_gnews**: Google News 搜索 FinSMEs AI 无今日回源（可能需换搜索词或 FinSMEs 直连被 Cloudflare 拦）

**建议**: 若内容工厂需要当日 YC/FinSMEs 信号，需补充 alternative source（Product Hunt / Crunchbase daily / Google News 手动搜索）或接受次日补抓。

---

## 派生活动摘要

- **对象总数**: 14 (输入)
- **派生 asset_chains**: 4
- **跳过**: 10 (含泛事件稿、VC机构、已有公司产品扩展)
- **未覆盖源**: trend__yc_launches_ai (0), web__finsmes_ai_gnews (0)
- **写入目录**: `/02_topic_radar/asset_chains/` (内容工厂路径，未触碰虚拟vc运行台)

*market-scout | signal-scout runtime | 2026-05-16T00:44:00Z*