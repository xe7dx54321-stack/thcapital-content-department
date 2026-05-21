# market public intake board

- date: 2026-04-02
- updated_at: 2026-04-02T02:18:48+08:00
- purpose: 把公众号留言 / 私信等外部输入先落成正式对象，形成后续内容、研究、项目、合作的统一入口。
- mode: 第一阶段仅支持人工 / 半自动录入，不直接承诺实时自动抓取微信真实留言。
- total_requests: 0
- pending_triage: 0
- queued_or_routed: 0
- content_request: 0
- research_request: 0
- project_review_request: 0
- cooperation_request: 0

## By route

- none

## Latest requests

| request_id | type | route | status | priority | requester | source_article | brief | next_action | file |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `-` | `-` | `-` | `-` | `-` | `-` | `-` | `none` | `-` | `-` |

## Rule

- 这块当前是正式对象入口，不是自动客服系统；系统先保证“接得住”，再谈“自动吃得下”。
- `content_request / research_request / project_review_request / cooperation_request` 是当前唯一正式分类，超出边界的输入先回 `founder_triage`。
- 留言如果同时包含多个意图，第一阶段优先按主意图落一个对象，不追求一次性拆成多个工单。
- 没有真实流量也照样保留这套对象，因为它是后续自动抓微信留言、接 bot、接网页抓取的统一契约。
