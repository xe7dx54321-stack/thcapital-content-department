---
name: th-market-hook-title-cover
description: Use when TH Capital public AI content needs a stronger title, cover copy, first-screen hook, or opening package for WeChat, Xiaohongshu, Zhihu, or X. This skill optimizes for click-through, cold-start clarity, and continued reading without drifting into clickbait or losing the real topic background.
---

# th-market-hook-title-cover

Use this skill when working on:

- title option design
- cover copy design
- first-screen / opening hook design
- packaging a topic before drafting
- re-packaging a weak draft before publish
- diagnosing whether a weak result is a packaging problem

This skill exists to solve one specific problem:

> 让“对的人愿意点、点进来能看懂、看懂后愿意继续读”。

## Important boundary

- This skill does **not** decide whether a topic should exist.
- This skill does **not** replace `th-topic-radar`.
- This skill does **not** replace full drafting or polishing.
- This skill does **not** permit clickbait that the body cannot cash.
- This skill does **not** remove the need for a context block.

Its job is:

> 把一个已经值得写的题，包装成更容易被点开、被读下去、又不失真的平台成品入口。

## Load order

1. Read `../../../00_planning/20260325_内容增长方法论与平台黄金标准.md`
2. Read `../../../08_brand_assets/20260324_公域品牌上下文手册.md`
3. Read `../../../08_brand_assets/20260324_平台定位与表达规范.md`
4. Read `../../../08_brand_assets/20260324_主战场与邻接选题判定框架.md`
5. If available, read `../../../08_brand_assets/latest__head-media-learning-rulebook-v1.md`
6. If available, read `../../../08_brand_assets/learning_knowledge_assets/latest__style-router.md`
7. If available, read `../../../08_brand_assets/learning_knowledge_assets/visual_playbooks/th_capital_visual_playbook_v2.md`
8. Read `references/platform-packaging-rules.md`
9. Read `references/hook-library.md`
10. If packaging is being reviewed after publish, read `references/packaging-diagnosis.md`
11. If a concrete formatting example would help, read `references/example-minicor-package.md`
12. Read the selected `approved_topic`, `draft_pack`, or `performance_review`

## Core workflow

1. Confirm the packaging target.
   - which platform
   - which audience layer
   - what matters most now:
     - click-through
     - cold-start clarity
     - read-through
     - conversion quality

2. Confirm the one thing the reader must understand.

Extract:

- what happened
- what changed
- why it matters
- who should care
- what TH Capital is actually saying

3. Identify the cold-start gap.

Ask:

- If a reader sees only the title, what will they misunderstand?
- If a reader enters with zero context, what is the minimum background they need?
- What is the strongest promise we can make **without** overselling?

4. Choose one primary hook family.

Use one of:

- result-first
- anti-consensus
- user-stake
- structural-shift
- risk-warning
- opportunity-window

Do **not** mix three hook families into one muddy title.

5. Build a packaging bundle, not a single line.

If a `style route` is already chosen:

- load the selected creator pack's `text-patterns.md` for标题/开头节奏
- load the selected creator pack's `visual-patterns.md` for封面 job 和图卡审美
- only borrow the declared layers; do not let packaging drift into cosplay

For each platform, generate:

- title options
- cover copy options
- first-screen / opening hook options
- cover job
- background cash line
- one recommended package
- one backup package

Additional packaging rule:

- Every package must explicitly answer at least one of these:
  - what the reader gains
  - what the reader should worry about
  - what changed for the reader
  - what opportunity is opening

If it answers none of them, it is likely still a research title, not a public title.

6. Force the hook to cash quickly.

The opening can lead with the hook, but the context must appear early enough that a cold-start reader does not stay confused.

Default rule:

- WeChat / Zhihu: the context bridge should appear within the first `10-20%` of the piece
- Xiaohongshu: context should land within the first `1-2` screens
- X: context must usually be compressed into the same post or the next line

Additional packaging rule:

- the cover and title can be strong, but they must not force the body to stay mysterious for too long
- every package should include one short line that immediately answers: `这到底是什么事`
- if the package only sells emotion and hides the object, reject it

7. Run the anti-fake-interest check.

Reject any package that:

- sounds hotter than the evidence
- hides the real object too long
- uses generic “机会来了 / 风口来了” hype
- would produce disappointment once the body starts

8. Score the final bundle.

Judge each package by:

- click strength
- clarity
- cold-start friendliness
- promise/body match
- platform fit
- TH Capital voice fit

## Title discipline

When optimizing titles, prefer:

- a real object, not a vague theme
- a real action/change, not only a conclusion
- a reader-facing stake, payoff, warning, or shortcut
- a natural spoken question on Zhihu, not nested `如何看待`

Reject titles that are:

- half-finished phrases
- ellipsis-heavy
- only a technical noun / repo / model name with no user meaning
- only a number with no object
- internal research phrasing pretending to be a public title

Platform shortcuts:

- WeChat: object + stakes first, then judgment
- Xiaohongshu: user scene / shortcut / warning beats abstract industry framing
- Zhihu: the question itself must read like a real search query
- Bilibili: object + “值不值得跟 / 对 builder 有什么意义” can work, but the object must be explicit
- X: one-line propagation is good, but still anchor to a concrete object

## Required output format

When this skill is used, output:

1. `target_platform`
2. `target_audience`
3. `core_claim`
4. `cold_start_gap`
5. `title_options`
6. `cover_options`
7. `opening_hook_options`
8. `cover_job`
9. `background_cash_line`
10. `recommended_package`
11. `why_this_package_wins`
12. `what_to_avoid`

If revising an existing draft, also output:

13. `why_the_old_package_was_weak`
14. `what changed`

## Platform guidance

### WeChat

- Optimize for: click + continued reading
- The title should tell users what insight they get, not just what happened
- The opening should give a hook first, then quickly bridge to context
- Avoid empty newsletter-style seriousness
- Prefer a title that contains:
  - a concrete object
  - a concrete stakes line
  - one clear contradiction
- The first screen should not become a wall of explanation

### Xiaohongshu

- Optimize for: immediate stop-scroll + easy understanding
- Use lower-threshold language
- Make the reader feel “this is about me / my opportunity / my workflow”
- Avoid abstract industry framing too early
- Prefer titles that feel like:
  - a warning
  - a shortcut
  - a translation
  - a “3 points” breakdown
- Cover and title should help the user decide to save, not just to click

### Zhihu

- Optimize for: question-fit + answer-first trust
- The packaging must imply a clear question being answered
- Make the opening useful even to search readers who skip the background
- Prefer titles that make the hidden question obvious

### X

- Optimize for: one-line propagation + high-signal opening
- The first line must survive on its own
- Do not bury the claim under context
- The first line should feel quotable even if screenshot alone gets shared

## Hard constraints

- No clickbait that the article cannot cash.
- No title/body mismatch.
- No package that requires prior context to even understand the subject.
- No fake urgency unless the timing claim is actually true.
- No packaging that drifts away from TH Capital’s main battlefield logic.
- No generic “AI media account” language.

## Output guidance

When the task is **topic packaging before drafting**, produce:

1. recommended hook family
2. 5 title options
3. 3 cover options
4. 3 opening options
5. recommended bundle
6. context-bridge reminder
7. user-stake sentence
8. first-screen risk if this package is too weak

When the task is **repairing weak performance**, produce:

1. likely failure layer:
   - click problem
   - clarity problem
   - read-through problem
2. why the current package failed
3. replacement package options
4. what to test next
