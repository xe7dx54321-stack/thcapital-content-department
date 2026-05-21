# market public intake request

- `request_id`: `YYYYMMDD_HHMMSS__slug`
- `created_at`: `ISO8601`
- `source_platform`: `wechat`
- `source_channel`: `wechat_comment | wechat_private_message | manual_copy`
- `source_message_id`: `optional`
- `source_article_queue_key`: `optional`
- `source_article_title`: `optional`
- `requester_handle`: `optional`
- `submitted_at`: `ISO8601`
- `normalized_request_type`: `content_request | research_request | project_review_request | cooperation_request | unknown_request`
- `routed_department`: `market_content_factory | vc_research | vc_project_line | market_business_dev | founder_triage`
- `classification_confidence`: `high | medium | low`
- `status`: `pending_triage | queued | routed | closed`
- `followup_mode`: `manual_first_phase`
- `priority_hint`: `normal | elevated`
- `tags`: `以分号分隔`
- `normalized_brief`: `一句话标准化需求`
- `routing_rationale`: `为什么这样归类`
- `next_action`: `下一步建议`

## Original Message

原始留言或私信全文。

## Notes

- 可补充上下文
- 可补充人工判断
- 若后续进入正式内容 / 研究 / 项目流程，在此补链接
