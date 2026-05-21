---
name: th-market-visual-intelligence
description: Use when TH Capital's market content workflow needs image understanding, source screenshot planning, visual evidence extraction, inline image slot planning, or visual asset sourcing for WeChat, Xiaohongshu, Zhihu, Bilibili, Toutiao, Baijiahao, and X. This skill covers both source-stage visual reasoning and publish-stage screenshot / asset acquisition.
---

# th-market-visual-intelligence

Use this skill when the task touches any of these:

- understand what a source image is doing
- read image-borne information together with text
- decide where our content should insert screenshots / diagrams / cards
- prepare source screenshot plans
- build visual asset sourcing notes
- capture screenshots from source pages

## Load order

1. Read `../../../00_planning/20260324_目录结构规范.md`
2. Read `../../../00_planning/20260324_对象字典与命名规范.md`
3. If available, read `../../../08_brand_assets/latest__head-media-learning-rulebook-v1.md`
4. If available, read `../../../08_brand_assets/learning_knowledge_assets/visual_playbooks/th_capital_visual_playbook_v2.md`
5. If a style route is already chosen, read the selected creator pack's `visual-patterns.md`
6. Read `../../20260326__market-visual-intelligence-runbook.md`

## Core principle

图片不是“装饰”，而是承担以下几类 job：

同时统一遵守一个审美底座：

- `proof-first editorial`
- 纸白 / 浅灰底，深墨文字，只保留 1 个信号色
- 优先对象截图、数字卡、结构图，拒绝抽象 AI 海报

1. `证据`
   - 证明原始事件真的发生
   - 证明原始对象长什么样

2. `解释`
   - 帮用户更快理解结构变化、流程变化、变量关系

3. `节奏`
   - 在长文里形成视觉停顿点，提高阅读时长

4. `传播`
   - 帮助封面、首图、图卡完成点击与转发

## Source-stage workflow

当处理 `source packet` 时，按这个顺序做：

1. 识别有没有可用图片输入
   - 原图
   - 缩略图
   - 榜单图
   - 页面截图候选

2. 判断图片承担什么 job
   - headline proof
   - object identification
   - data proof
   - structure explanation
   - emotional hook

3. 判断它适不适合被我们复用
   - 可直接截图复用
   - 只适合作参考，不适合直接用
   - 需要重画结构图

4. 记录后续建议
   - 我们正文哪个位置适合放这张图
   - 如果不适合直接复用，应该换成什么图

## Draft-pack workflow

当处理 `draft pack` 时：

1. 先决定每个平台需要几张图
2. 给每张图一个明确 slot
3. 给每张图写清 job
4. 为每张图决定 sourcing priority：
   - 原始截图
   - 官方资产
   - 外部补图
   - AI 解释图

   其中要额外遵守：
   - 外部补图当前优先走 `Wikimedia Commons` 开放许可检索
   - 外部补图默认只补 `1` 张，并且必须与主题实体或原始对象有足够相关性
   - 如果已经有可用的一手截图 / 官方资产，外部补图默认不再扩张成整组图片
   - AI 解释图当前走 `OpenAI Images API`；若环境缺少 `OPENAI_API_KEY`，自动退回本地 `structured explainer`

5. 在真正取图前，先走一遍这个判断树：
   - 如果是 `原始帖子 / PDF / repo / 产品页 / 官方页面`，优先取“证据型截图”，只截标题区、hero 区、对象区、README 首屏等重点区域
   - 如果官方站 / 官方 CDN 已经挂了干净的对象图、活动海报、产品图，优先直接下载原图，不要把“图片直链网页”再截图成黑底图
   - 如果官方资产只能证明“对象长什么样”，不能单独证明“这件事确实发生”，正文里要至少再配一张证据型截图
   - 如果手里只有第三方媒体文章，不要直接截文章页；优先回找原始源、官方资产、repo、PDF 或官方活动海报
   - 如果确实找不到安全原图，再决定是搜索安全外部图，还是画解释型图

不要只写“建议配图”。必须写：

- 放在哪一段前后
- 为什么放在这里
- 这张图帮读者完成什么认知动作

## Publish-stage workflow

当进入 `publish queue`：

1. 输出最小可执行取图清单
2. 对每个截图候选写清：
   - 来源 URL
   - 截什么区域
   - 建议保存路径
   - 抓不到时的 fallback
3. 如果来源本身就是 `官方图片直链 / 官方缩略图 / 官方海报`：
   - 默认下载原图文件
   - 不要把浏览器打开图片后的黑底页面当成最终图片
4. 最终进入成稿预览的图，只能是：
   - 原始证据截图
   - 官方资产 / 官方缩略图 / 官方海报
   - 经过明确批准的外部安全图
   - 内部解释图只能辅助内部生产，不默认进入最终发布预览

## Hard constraints

- 不要用抽象图代替事实证据图
- 不要只因为图片好看就放
- 不要让图片和标题表达互相打架
- 不要把一整页截图塞进正文而没有说明它证明什么
- AI 生成图只适合解释结构，不适合证明事实
- 不要把第三方公众号 / 媒体文章页截图直接塞进我们的正文
- 第三方文章里的图只有在能确认无水印、无版权风险、且确实服务正文时才考虑复用；默认优先回找原始信源或官方资产
- 不要把“图片需求说明卡 / slot 占位卡 / 内部解释卡”当成成稿图片直接发出去
- 如果当前图不能直接发，就把它留在内部流程里，不要污染最终成稿页
- 外部补图命中后也要继续问：它是不是在服务当前话题，而不是只是“字面搜到了相关词”

## Screenshot discipline

- 优先抓标题区 / hero 区 / 对象区
- 如果是 `X` 推文，优先保留作者、正文、时间、互动线索
- 如果是 `PDF`，优先抓首页标题和发布主体
- 如果是 `GitHub`，优先抓 repo header、stars、README 首屏
- 如果是视频平台，优先抓标题区或官方缩略图
- 如果是 `官方站 + 官方 CDN 图片`，优先下载官方原图，再决定是否还需要补一张页面级证据截图
- 如果来源是第三方媒体文章，默认不自动截图整页；优先寻找官方公告、原帖、repo、PDF、官方 hero 图或替代安全图

## Output contract

如果任务是 `source packet`，至少输出：

1. visual evidence status
2. source image inputs
3. layout observations
4. our reuse suggestions

如果任务是 `draft pack / publish queue`，至少输出：

1. inline visual slots
2. asset priority
3. capture targets
4. fallback plan
