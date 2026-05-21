---
name: th-market-context-bridge
description: Use when TH Capital public AI content needs a cold-start-friendly context block so readers can quickly understand what happened, who is involved, why it matters now, and how the coming analysis connects to the real event. This skill prevents drafts from feeling insider-only, overly abstract, or confusing in the first screen.
---

# th-market-context-bridge

Use this skill when working on:

- background / context block design
- cold-start readability repair
- opening section restructuring
- converting insider shorthand into public-facing context
- repairing drafts that “start mid-thought”
- making a topic understandable before deeper analysis begins

This skill exists to solve one specific problem:

> 让一个完全不知道原始事件的读者，也能在很短时间内知道“发生了什么、为什么值得继续读”。

## Important boundary

- This skill does **not** decide the topic.
- This skill does **not** replace title / hook packaging.
- This skill does **not** replace full drafting.
- This skill does **not** turn the opening into a long news recap.
- This skill does **not** flatten TH Capital’s judgment into bland background text.

Its job is:

> 在“不拖沓”的前提下，把读者从“我不知道你在说啥”桥接到“我知道接下来该看什么了”。

## Load order

1. Read `../../../00_planning/20260325_内容增长方法论与平台黄金标准.md`
2. Read `../../../08_brand_assets/20260324_公域品牌上下文手册.md`
3. Read `../../../08_brand_assets/20260324_平台定位与表达规范.md`
4. If available, read `../../../08_brand_assets/latest__head-media-learning-rulebook-v1.md`
5. If title / hook packaging matters, read `../th-market-hook-title-cover/SKILL.md`
6. Read `references/context-block-patterns.md`
7. Read `references/platform-context-rules.md`
8. If debugging a weak draft, read `references/context-failure-diagnosis.md`
9. If a concrete example helps, read `references/example-openai-context-bridge.md`
10. Read the selected `approved_topic`, `draft_pack`, or live draft

## Core workflow

1. Confirm what the reader already knows — or more importantly, does **not** know.

Ask:

- If a smart but cold-start reader sees this piece, what is the missing minimum context?
- What names, products, or events are currently assumed but not explained?
- Which missing fact would cause the rest of the argument to feel like fog?

2. Extract the minimum event kernel.

Every context bridge should identify:

- who
- what happened
- when / what changed
- why this event is worth talking about now

3. Separate “background” from “main argument”.

Background answers:

- what is this thing?
- what happened?

Argument answers:

- why it matters
- what TH Capital thinks

Do not collapse them into one vague paragraph.

4. Choose the correct context depth.

Possible depth levels:

- `micro`: one sentence
- `short`: one compact paragraph
- `medium`: 2 short paragraphs

Default:

- X: `micro`
- Xiaohongshu: `micro` to `short`
- WeChat: `short` to `medium`
- Zhihu: `short`

Additional rule:

- If the object is obscure, the bridge must name the object earlier.
- If the object is famous but the implication is obscure, the bridge should explain the implication earlier.

5. Place the context bridge in the right position.

The context does **not** always need to be the first sentence.

Recommended placement:

- after the first strong hook
- before the reader starts needing specific background knowledge
- before abstract analysis becomes confusing

6. Translate insider language into public language.

If the raw topic says:

- `ACP`
- `agent harness`
- `legacy desktop integration`
- `merchant integration`

then the bridge must explain them in reader-facing terms before the piece leans on them heavily.

7. Connect the bridge to the coming argument.

The last line of the context block should naturally hand off into:

- the main contradiction
- the key variable
- the TH Capital judgment

8. Run the anti-drift check.

Reject any bridge that:

- becomes a dry news summary
- delays the argument too long
- explains too much irrelevant history
- still assumes the reader knows the object

## Required output format

When this skill is used, output:

1. `target_platform`
2. `target_audience`
3. `cold_start_gap`
4. `minimum_event_kernel`
5. `recommended_context_depth`
6. `recommended_placement`
7. `context_block_options`
8. `best_context_block`
9. `handoff_line_to_main_argument`
10. `what_to_avoid`

If revising an existing draft, also output:

11. `why_the_existing_opening_is_confusing`
12. `what_context_was_missing`
13. `how_the_new_bridge_fixes_it`

## Platform guidance

### WeChat

- The context bridge can follow a strong opening claim
- It should quickly answer “what exactly is this event/object”
- It should prepare the reader for a mid-depth argument
- The bridge should usually land within the first 3 screens

### Xiaohongshu

- Keep it very short
- Use plain language
- Make the object legible in everyday terms
- The bridge should usually be readable in one glance or one swipe

### Zhihu

- The answer can come first
- The context bridge should make the object concrete before detailed reasoning
- Avoid sounding like copied media summary
- Search readers should understand the object without reading the whole article

### X

- Compress context into the same line or next line
- If the object is obscure, clarify it immediately
- No hidden-subject threads
- If the object needs 3 lines to explain, the hook is probably wrong

## Hard constraints

- No opening that assumes insider context.
- No context block so long that the argument disappears.
- No acronym-heavy bridge without translation.
- No generic “recently, in the AI field…” filler.
- No background recap that fails to answer why this piece matters now.

## Output guidance

When the task is **draft support**, produce:

1. cold-start gap
2. recommended context depth
3. 3 context block options
4. recommended option
5. handoff line into the main argument
6. first-screen placement note

When the task is **draft repair**, produce:

1. what the reader likely failed to understand
2. where confusion begins
3. replacement bridge options
4. whether the hook should stay before the context or not
