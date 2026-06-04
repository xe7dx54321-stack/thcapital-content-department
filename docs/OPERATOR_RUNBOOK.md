# Operator Runbook

## Current Status

- trial_days: `7`
- failure_issue_count: `6`
- failure_blocker_count: `0`
- regression_status: `PASS`
- closeout_blocked_count: `9`

## 每日启动命令

- make phase20-daily
- make wechat-workbench
- python3 scripts/serve_wechat_workbench.py --port 8765
## 每日检查顺序

- 今日运营
- 内容队列
- 图文发布包
- 失败处理
- 发布后复盘
- 运营 closeout
## 今天没有可发内容

- 不要硬发。查看 THIS_WEEK / WATCH。补图、补证据或重写后再进入发布准备。
## 缺图

- 查看 image asset library 和 visual checklist。图片未 AVAILABLE / APPROVED 前不发布。
## 缺证据

- 回到 source/evidence packet，补至少 3 条证据和来源说明。
## 工作台打不开

- 运行 make wechat-workbench；再运行 python3 scripts/serve_wechat_workbench.py --port 8765。
## pipeline degraded

- 打开 latest_content_ops_failure_handling.md，优先处理 BLOCKER，再处理 WARN。
## 创建 publish session

- python3 scripts/create_manual_publish_session.py --create <final_candidate_id> --note '准备手动发布'
## 记录已发布

- python3 scripts/create_manual_publish_session.py --mark-published <publish_session_id> --url '<url>' --note '已手动发布'
## 录入 metrics

- python3 scripts/record_post_publish_metrics.py --session <publish_session_id> --views 1000 --likes 20 --wows 5 --shares 3 --comments 2 --note '人工录入'
## 一周复盘

- 查看 trial issue log、content ops closeout、metrics review、visual feedback，再决定进入 Phase21 trial fix pack。

## Hard Boundaries

- 不自动发布。
- 不接公众号 API。
- 不进入公众号草稿箱。
- 不自动抓取后台数据。
- 不自动生成图片。
- 所有发布和 metrics 都由人工确认。
