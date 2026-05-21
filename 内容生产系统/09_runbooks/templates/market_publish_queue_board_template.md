# Publish Queue Board Template

## 推荐结构

- `generated_at`
- `total_items`
- `queued_items`
- `waiting_human_publish_items`
- `published_items`

| queue_id | topic_key | platform | status | manual_gate | publish_owner | planned_publish_at | actual_publish_at | publish_url |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |

### Human Action Queue

- 哪些待确认发布时间
- 哪些待人工发布
- 哪些延期后待重排

### Published / Review Follow-up

- 哪些已发布
- 哪些待进入 24h review

## 使用要求

- 一个平台一条 queue item
- 当天的 board 要能让人一眼看到：
  - 哪些待发
  - 哪些等人工
  - 哪些已经发
  - 哪些延期 / 取消
- 要一眼看懂当前人工动作是什么
