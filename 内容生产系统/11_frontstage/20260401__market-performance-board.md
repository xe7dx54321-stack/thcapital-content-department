# Market Performance Board

- `generated_at`: `2026-04-01 12:25:28 CST`
- `total_items`: `3`
- `published_items`: `1`
- `waiting_publish_items`: `2`
- `metrics_ready_items`: `0`
- `wechat_local_credentials`: `ready`
- `wechat_official_api_status`: `ready_empty`
- `wechat_official_api_note`: `freepublish reachable, but returned 0 published article(s)`

## Tracker Table

| queue_key | title | status | published_at | metric_status | latest_stat_date | read | share | zaikan | like | comment | collect | finish_rate | avg_read_min | 24h | 72h |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `claude_code_cache_bugs_20260331__wechat` | Claude Code 两个缓存 Bug，为什么会把你的 API 账单悄悄放大 10—20 倍 | `published` | `n/a` | `publish_backfill_pending` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `scheduled` | `scheduled` |
| `robots_bury_you_in_work_17_agents_20260331__wechat` | 17 个 Agent、12 个项目、1400+ commits：AI 没先替掉你，先把你推上了管理岗 | `waiting_human_publish` | `n/a` | `waiting_publish` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `scheduled` | `scheduled` |
| `claude_code_source_leak_agent_capabilities_20260401__wechat` | 看完 Claude Code 51 万行泄漏源码，我真正看清了未来 Agent 最重要的 7 个能力 | `waiting_human_publish` | `n/a` | `waiting_publish` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `n/a` | `scheduled` | `scheduled` |

## Action Queue

- `system`｜公众号官方 API 已连通，但 `freepublish/batchget` 最近返回 0 条已发布文章；如果业务走的是“草稿箱人工发送”，这类记录本来就可能不在这条接口里，建议改成 `freepublish/submit` 正式发布。
- `claude_code_cache_bugs_20260331__wechat`｜这条稿件大概率走的是“草稿箱人工发送”链路，freepublish 列表未必可见；后续建议改用 freepublish/submit 正式发布。
- `robots_bury_you_in_work_17_agents_20260331__wechat`｜等老板发布后自动回填永久链接。
- `claude_code_source_leak_agent_capabilities_20260401__wechat`｜等老板发布后自动回填永久链接。
