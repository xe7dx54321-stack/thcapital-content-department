# P13-004 Post-publish Manual Metrics Input Report

## 本轮目标

支持人工录入公众号发布后的阅读、点赞、在看、转发、收藏、评论和新增关注等指标。

## 修改文件

- `src/content_system/post_publish_metrics.py`
- `scripts/record_post_publish_metrics.py`
- `scripts/build_post_publish_metrics_board.py`
- `Makefile`

## 已完成能力

- 支持 `--list-sessions` 查看 manual publish sessions。
- 支持按 session 录入 views、likes、wows、shares、saves、comments、new followers。
- 自动生成 LOW/MEDIUM/HIGH/EXCELLENT/UNKNOWN 辅助评级。
- 新增 `make post-publish-metrics-board`。

## 安全边界

- 所有表现数据均为人工录入。
- 不爬取公众号后台。
- 不要求用户提供账号密码。

## 当前限制

指标口径由人工维护，后续可增加多时点记录和增长率分析。
