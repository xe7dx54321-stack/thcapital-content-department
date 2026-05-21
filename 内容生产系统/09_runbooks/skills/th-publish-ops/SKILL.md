---
name: th-publish-ops
description: Use when a polished draft pack must be turned into concrete publish queue items, human publishing reminders, and explicit queue state updates without auto-posting to platforms.
---

# th-publish-ops

Use this skill for Step 8 publish queue work:

- create publish queue items
- update queue status
- generate queue board
- remind human owners to publish

## Important boundary

- This skill works **after** Draft Pack reaches `ready`.
- It does **not** auto-post to platforms.
- It does **not** invent publish completion.
- It does **not** skip queue state transitions.

Its job is:

> 把“内容已经写好了”推进成“哪条内容在哪个平台、由谁、什么时候发、现在处于什么状态”。

## Load order

1. Read `../../../00_planning/20260324_对象字典与命名规范.md`
2. Read `../../../00_planning/20260324_状态流转规范.md`
3. Read `../../../00_planning/20260324_目录结构规范.md`
4. Read `../th-market-platform-renderer/SKILL.md`
5. Read `../../../09_runbooks/20260325__market-publish-and-review-runbook.md`
6. Read `../../../09_runbooks/templates/market_publish_queue_item_template.md`
7. Read `../../../09_runbooks/templates/market_publish_queue_board_template.md`
8. Read the selected Draft Pack

## Core workflow

1. Confirm Draft Pack is `ready`.
   - If not, do not queue it as if it were finished.
   - Also confirm render handoff assets are not obviously missing for the selected platform.

2. Decide the platform scope.
   - Use requested platforms from the Draft Pack unless a human explicitly narrows it.

3. Create or update one queue item per platform.

4. Keep the queue board visible.

5. Update only honest status:
   - `queued`
   - `waiting_human_publish`
   - `published`
   - `deferred`
   - `cancelled`

6. When something is actually published:
   - record `actual_publish_at`
   - record `publish_url`
   - do not leave it at `waiting_human_publish`

## Hard constraints

- No Draft Pack `ready`, no publish queue creation.
- No fake `published` without a real publish link or explicit note.
- One platform, one queue item.
- Queue state must stay auditable.

## Output guidance

Output:

1. queue item card(s)
2. updated queue board
3. short human reminder summary
