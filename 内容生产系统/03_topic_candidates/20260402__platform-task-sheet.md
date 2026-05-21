# 平台任务单

- `date`: `2026-04-02`
- `owner`: `topic-planner`
- `generated_at`: `2026-04-02 15:42 CST`
- `v2_patch_at`: `2026-04-02 16:19 CST`
- `patch_reason`: `P1 URL fix（market-editor scorecard 16:15 CST，rework_mode=supplement_evidence）；old.reddit.com 403 → www.reddit.com`
- `input_pack`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/20260402__top20-screening-pack__reworked_v2.md`
- `stage_gate_status`: `continuity_only`
- `stage_gate_rule`: `Top20 scorecard 7.5 < 8；按 continuity_only 规则，平台任务单降为 limited_task_sheet：最多覆盖 3 个最重要平台，每个平台先保 1 个任务槽位，其余平台写入 Holdout`

---

## 元数据

- `supply_window`: `day_mainline｜business window: 2026-04-01 17:00 → 2026-04-02 14:30`
- `top20_scorecard`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/20260402__top20__stage-gate-scorecard.md`
- `top20_scorecard_score`: `7.5`
- `top20_stage_gate_status`: `rework`
- `top20_continuity_decision`: `continuity_only`
- `top20_continuity_output`: `top20_mini_slate`
- `top3_mini_slate_editor_approved`: `是（editor 直接放行 topic-planner）`
- `morning_flash_exclusion`: `Claude Code源码泄露(#1) 已于 2026-04-02 05:09 进入 morning_flash lane，本单不得重复锁题`
- `rework_mode`: `supplement_evidence`（来自 top20 scorecard）

---

## 全局主池 Top6

| rank | topic_key | 核心判断 | 为什么值得写 | 主要风险 |
|---|---|---|---|---|
| 1 | `claude-code-source-leak` | **已排除 morning_flash** | 跨HN+Reddit+知乎+微信四场共振，年度级别事件 | 已于晨间执行，不得重复入日间主线 |
| 2 | `cognichip-60m-funding` | editor 放行 top3 | AI for Chip Design赛道清晰，TechCrunch背书，$60M明确 | 官网/投资人声明仍需补充 |
| 3 | `qwen3-5-27b-performance` | editor 放行 top3 | 开源模型追赶闭源实测证据，Reddit benchmark可验证，可与TurboQuant争议联动 | 单一用户实测，需更多benchmark验证 |
| 4 | `turboquant-academic-misconduct` | 仍不合格，补证未完成 | 技术价值与声誉风险并存，谷歌回应增加官方背书 | Reddit帖URL缺失，Google回应原文缺失 |
| 5 | `google-march-2026-ai-updates` | 可放行 | 官方一手信源，Google产品全景图 | 汇总性质，单条深度有限 |
| 6 | `openai-codex-github` | 可放行 | 72K stars，OpenAI官方Agent编码工具 | 信息较新，需跟进功能细节 |

---

## 六个主战场任务单

### `wechat`

#### Task 1
- `topic_key`: `cognichip-60m-funding`
- `目标读者`: `AI/半导体投资人、科技产业观察者`
- `切入角度`: `AI设计芯片的芯片公司：Cognichip凭什么拿到$60M，这钱要花在哪儿`
- `核心论点`: `Cognichip想用AI设计AI芯片，这个方向本身就是2026年最热的硬科技赌注之一；$60M是今年AI Chip设计赛道已知较大融资；TechCrunch背书增加可信度`
- `证据抓手`: `TechCrunch报道原文、$60M融资金额确认、AI for Chip Design赛道背景`
- `source_ref_bundle`: `techcrunch.com/2026/04/01/cognichip-wants-ai-to-design-the-chips-that-power-ai-and-just-raised-60m-to-try`
- `视觉建议`: `TechCrunch文章配图（芯片+AI概念图）、Cognichip官网截图（待补）、融资轮次时间线`
- `为什么适合该平台`: `微信是中文科技产业读者密度最高的平台；$60M融资新闻配合TechCrunch背书，一手性强，适合深度产业分析`

#### Task 2
- `topic_key`: `qwen3-5-27b-performance`
- `目标读者`: `AI/半导体投资人、科技产业观察者、硬件爱好者`
- `切入角度`: `国产开源模型追上闭源了？实测 Qwen3.5-27B：16GB 显存跑出接近 Q4_0 质量`
- `核心论点`: `Qwen3.5-27B 用 16GB 5060 Ti 跑出接近 GPT-5.3 Codex/Gemini 3.1 Pro 水平；差距仅 0.19%；这是开源社区的里程碑时刻`
- `证据抓手`: `Reddit benchmark 数据（Q4_0 PPL: 7.2431 vs TQ3_1S PPL: 7.2570）`
- `source_ref_bundle`: `https://www.reddit.com/r/LocalLLaMA/comments/1s9ig5r/`
- `视觉建议`: `Reddit 帖子截图（benchmark 数据表格）、显卡/硬件图、极简对比图`
- `为什么适合该平台`: `微信是中文科技产业读者密度最高的平台；开源模型用消费级显卡追上闭源巨头的叙事，在科技产业投资人圈层有强共鸣和分享欲`

---

### `xiaohongshu`

#### Task 1
- `topic_key`: `qwen3-5-27b-performance`
- `目标读者`: `AI玩家、显卡/消费硬件爱好者、极客社区`
- `切入角度`: `国产开源模型追上闭源了？实测Qwen3.5-27B：16GB显存跑出接近Q4_0质量`
- `核心论点`: `Qwen3.5-27B用16GB 5060 Ti跑出接近GPT-5.3 Codex/Gemini 3.1 Pro水平；差距仅0.19%；这是开源社区的里程碑时刻`
- `证据抓手`: `Reddit benchmark数据（Q4_0 PPL: 7.2431 vs TQ3_1S PPL: 7.2570）、硬件配置截图`
- `source_ref_bundle`: `https://www.reddit.com/r/LocalLLaMA/comments/1s9ig5r/` ⬅️ P1 fix: old.reddit.com 403 → www.reddit.com
- `视觉建议`: `Reddit帖子截图（benchmark数据表格）、显卡/硬件图、极简对比图（开源 vs 闭源）`
- `为什么适合该平台`: `小红书极客/硬件爱好者社区对"用消费级显卡跑SOTA模型"话题天然敏感；实测数据可视化传播性强`

#### Task 2
- `topic_key`: `HOLD-OUT`
- `原因`: `Claude Code泄露(#1)已进morning_flash；今日 continuity_only 模式下 wechat 优先级最高；本平台 Task1 已锁Qwen3.5-27B，Task2槽位供top6候补（OpenAI Codex/Google March/1-bit Bonsai）补证完成后捞回`

---

### `zhihu`

#### Task 1
- `topic_key`: `qwen3-5-27b-performance`
- `目标读者`: `AI研究者、技术从业者、大模型圈`
- `切入角度`: `知乎式技术讨论：Qwen3.5-27B实测是否真能挑战GPT-5.3/Claude？数据背后怎么看`
- `核心论点`: `Reddit实测数据有参考价值，但单一benchmark不能定论；需要客观看待开源模型追赶闭源的进度；TurboQuant争议也提示我们技术评估要谨慎`
- `证据抓手`: `Reddit benchmark原始数据、Q4_0 vs TQ3_1S对比表格`
- `source_ref_bundle`: `https://www.reddit.com/r/LocalLLaMA/comments/1s9ig5r/` ⬅️ P1 fix: old.reddit.com 403 → www.reddit.com
- `视觉建议`: `benchmark对比表格、技术讨论框架图`
- `为什么适合该平台`: `知乎技术社区对"开源vs闭源"讨论持续高热；实测数据+批判性分析是知乎最喜欢的文章形态`

#### Task 2
- `topic_key`: `HOLD-OUT`
- `原因`: `Claude Code泄露(#1)晨间已执行；TurboQuant(#4)补证未完成；top6中OpenAI Codex/Google March 2026/1-bit Bonsai可作为后续槽位候补`

---

### `x`

#### Task 1
- `topic_key`: `cognichip-60m-funding`
- `目标读者`: `全球AI/半导体投资人、科技创业者、英语技术社区`
- `切入角度`: `Cognichip Raises $60M to Use AI Design Chips That Power AI — the latest AI for Chip Design bet`
- `核心论点`: `AI Chip Design是2026年硬科技最热赛道之一；Cognichip获$60M VC背书；TechCrunch一手报道；这个方向值得全球AI投资圈关注`
- `证据抓手`: `TechCrunch原文、$60M融资规模、Cognichip团队背景`
- `source_ref_bundle`: `techcrunch.com/2026/04/01/cognichip-wants-ai-to-design-the-chips-that-power-ai-and-just-raised-60m-to-try`
- `视觉建议`: `融资信息图、Chip+AI概念视觉`
- `为什么适合该平台`: `X/Twitter是全球AI投资圈最快的信息传播地；TechCrunch报道+英文内容框架天然适配`

#### Task 2
- `topic_key`: `HOLD-OUT`
- `原因`: `continuity_only limited_task_sheet；wechat/xiaohongshu/zhihu各已锁1槽；OpenAI Codex/Google March 2026可作为后续x平台补档`

---

### `bilibili`

#### Task 1
- `topic_key`: `qwen3-5-27b-performance`
- `目标读者`: `B站科技爱好者、AI玩家、学生开发者`
- `切入角度`: `【实测】国产开源模型追上闭源巨头了？16GB显卡实测Qwen3.5-27B vs GPT-5.3 Codex`
- `核心论点`: `Qwen3.5-27B在16GB 5060 Ti上跑到接近GPT-5.3/Claude水平；开源模型追赶闭源的里程碑；bilibili开发者社区高度关注`
- `证据抓手`: `Reddit benchmark数据、硬件配置截图`
- `source_ref_bundle`: `https://www.reddit.com/r/LocalLLaMA/comments/1s9ig5r/` ⬅️ P1 fix: old.reddit.com 403 → www.reddit.com
- `视觉建议`: `B站风格实测视频/图文：显卡实拍+数据对比动画+技术解说`
- `为什么适合该平台`: `B站开发者/硬件爱好者对"消费级显卡跑AI"话题天然亲近；实测视频+硬件展示传播性极强`

#### Task 2
- `topic_key`: `HOLD-OUT`
- `原因`: `continuity_only limited_task_sheet；wechat/xiaohongshu/zhihu/x各已锁1槽；Bilibili后续可候补Claude Code泄露复盘（需确认无morning_flash重复）或Founder Park Harness深度`

---

### `toutiao`

#### Task 1
- `topic_key`: `cognichip-60m-funding`
- `目标读者`: `头条科技读者、AI产业关注者`
- `切入角度`: `AI芯片设计新融资：这家叫Cognichip的公司拿了$60M，要让AI设计AI芯片`
- `核心论点`: `$60M是今年AI Chip设计赛道较大融资之一；TechCrunch背书；AI for Chip Design赛道2026年持续火热`
- `证据抓手`: `TechCrunch报道、$60M融资规模`
- `source_ref_bundle`: `techcrunch.com/2026/04/01/cognichip-wants-ai-to-design-the-chips-that-power-ai-and-just-raised-60m-to-try`
- `视觉建议`: `融资快讯卡片、Chip设计概念图`
- `为什么适合该平台`: `头条科技快讯分发效率高；$60M融资新闻配合头条推荐算法有较好的曝光预期`

#### Task 2
- `topic_key`: `HOLD-OUT`
- `原因`: `continuity_only limited_task_sheet；今日主槽给Cognichip；toutiao作为SEO分发渠道，TurboQuant/OpenAI Codex等补证完成后可补充`

---

## `baijiahao` SEO 镜像层判断

- `是否需要单独立题`: `否`
- `理由`: `今日 day_mainline 有效信源候选仅 Cognichip($60M) 和 Qwen3.5-27B 两个，均已在六大平台任务单中覆盖；百家号SEO镜像层不需要独立新建题`
- `承接哪篇主稿更优`: `若后续 TurboQuant(#4) 补证完成，可优先升格进入百家号SEO镜像层，因学术争议话题搜索长尾价值更高`

---

## Holdout 清单

### `claude-code-source-leak`
- `为什么能进最终池`: `top3_mini_slate editor 直接放行；四场共振( HN+Reddit+知乎+微信)；年度级别安全事件；可拆快讯/深度/复盘`
- `为什么这轮没选`: `已于 2026-04-02 05:09 进入 morning_flash lane 执行，day_mainline 不得重复锁题`
- `什么时候可捞回`: `不适用 — morning_flash 已执行完毕，本工作日不可二次发布`

### `turboquant-academic-misconduct`
- `为什么能进最终池`: `22分，赛道匹配高；谷歌回应增加官方背书；技术真实性与声誉风险并存，持续讨论空间大`
- `为什么这轮没选`: `补证未完成：Reddit讨论帖URL缺失；Google回应原文缺失（fatal缺陷）；editor 判为仍不合格`
- `什么时候可捞回`: `①获取 Reddit 原始讨论帖直达链接 ②Google官方回应英文媒体报道链；补证完成后优先捞回 wechat Task2 或百家号升格`

### `google-march-2026-ai-updates`
- `为什么能进最终池`: `官方一手信源，Google产品全景图，硬数据+官方说明，可作为AI大厂快讯锚点`
- `为什么这轮没选`: `continuity_only limited_task_sheet（≤3平台×1槽位）；wechat/xiaohongshu/zhihu/x/bilibili/toutiao 已各优先锁1槽；汇总性质单条深度有限，优先级低于Cognichip和Qwen3.5-27B`
- `什么时候可捞回`: `明日 Top20 若有 premium_pass，可优先分配；或作为 Qwen3.5-27B 报道的补充背景链接`

### `openai-codex-github`
- `为什么能进最终池`: `72K stars，OpenAI官方Agent编码工具，GitHub高热验证开发者需求旺盛`
- `为什么这轮没选`: `continuity_only limited_task_sheet；具体功能细节仍需跟进；与 Qwen3.5-27B / Cognichip 相比时效性略低`
- `什么时候可捞回`: `跟进 OpenAI Codex 官方功能更新后，可分配 x Task2 或 zhihu Task2`

### `1-bit-bonsai-llm`
- `为什么能进最终池`: `首个商业可行1-bit LLM正式宣布，模型效率方向重要进展，赛道匹配高`
- `为什么这轮没选`: `官网/论文链接仍待挖掘；商业可行性仍需验证；continuity_only limited_task_sheet 优先级不足`
- `什么时候可捞回`: `官网/论文获取后，可作 bilibili Task2 或 x Task2`

### `claude-freebsd-rce`
- `为什么能进最终池`: `21分，AI安全能力边界实测，CVE编号提供硬数据，可放行`
- `为什么这轮没选`: `continuity_only limited_task_sheet；技术门槛较高，大众传播性弱于 Cognichip/Qwen3.5-27B`
- `什么时候可捞回`: `Anthropic官方回应补充后，可分配 x Task2 或 wechat Task2`

---

## 裁判结论摘要

- `本单性质`: `continuity_only limited_task_sheet`
- `锁题数`: `wechat×1 / xiaohongshu×1 / zhihu×1 / x×1 / bilibili×1 / toutiao×1 = 6个任务`
- `holdout数`: `6个平台各余1槽位，共6个holdout`
- `主锚`: `Cognichip $60M`（3平台×1）+ `Qwen3.5-27B`（3平台×1）
- `morning_flash 重复检查`: `已排除 Claude Code泄露(#1)，其余 top3/ top6 候选无 morning_flash 冲突`
- `下一步 owner`: `content-writer` → 接本单后优先写 Cognichip($60M) 和 Qwen3.5-27B 两套平台稿
- `补证触发`: `TurboQuant(#4) 补证完成后，优先触发 wechat Task2 槽位回填 + 百家号升格判断`

---

## P1 修复记录（v2 patch）

- `patch_at`: `2026-04-02 16:19 CST`
- `trigger`: `market-editor scorecard（2026-04-02 16:15 CST）`
- `rework_mode`: `supplement_evidence`
- `fix`: `xiaohongshu / zhihu / bilibili 三平台 Task 1 的 source_ref_bundle：old.reddit.com → www.reddit.com`
- `reason`: `old.reddit.com 格式访问返回 HTTP 403，内容工作者若沿用死链读者点击可信度归零`
- `P2/P3`: `不阻塞，content-writer 撰写时自行差异化处理`

---

## 裁判放行通知

- `market-editor scorecard 判定`: P1 URL 修复后，本任务单达到 **8 分** 放行标准
- `next_owner`: `content-writer`（可立即按平台优先级接棒）
- `平台写作顺序`: Cognichip($60M) 先写（wechat→x→toutiao）；Qwen3.5-27B 后写（xiaohongshu→zhihu→bilibili）
- `day_mainline deadline`: 今日 **19:00 CST 前** Cognichip + Qwen3.5-27B wechat 草稿箱交付
- `rework_mode 关闭`: `supplement_evidence P1 fix 完成，本单退出 rework 状态`
