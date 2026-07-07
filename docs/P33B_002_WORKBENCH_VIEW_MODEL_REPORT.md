# P33B-002 Workbench View Model Report

## 目标

建立统一的 Workbench 视图模型（View Model），前端只基于这一个结构渲染，
不再在模板中到处拼接 Runtime、OpenClaw、Replay、稿件正文等原始面板字段。

## Schema

```json
{
  "schema_version": "v1",
  "generated_at": "",
  "today_overview": {},
  "today_article": {},
  "quality_check": {},
  "replay_dashboard": {},
  "system_ops": {}
}
```

## 五大区域边界

### 1. today_overview

只放结论，不放过程日志。

字段：
- overall_status: READY_TO_REVIEW | NO_CANDIDATE | NEEDS_ATTENTION | SYSTEM_ISSUE
- system_status: NORMAL | WARNING | ERROR
- candidate_status: READY | MISSING | NEEDS_REVISION | HOLD
- quality_status: PASS | ACTIONABLE | FAIL | UNKNOWN
- next_scheduled_run
- main_topic
- recommended_title
- one_sentence_judgement
- why_worth_reading
- main_risk
- recommended_action
- alerts (最多 3 条)

### 2. today_article

只放今天的最终候选稿，不放系统状态。

字段：
- title
- subtitle
- topic
- generated_at
- status
- quality_rating
- article_markdown
- agent_review_summary
- actions (内容相关动作)

### 3. quality_check

只放内容质量和证据质量。

字段：
- rating
- can_review
- blocking_issue_count
- warning_count
- checklist
- evidence_summary
- human_review_checklist

### 4. replay_dashboard

只放历史回放和校准，不污染今日稿件。

字段：
- summary
- days
- calibration_proposals
- policy.replay_is_not_production

### 5. system_ops

只放 Runtime、LaunchAgent、OpenClaw、日志和调试动作。

字段：
- runtime
- launchagent
- jobs
- acquisition
- openclaw
- debug_actions

## 实现位置

- 核心逻辑：`src/content_system/workbench_view_model.py`
- 构建脚本：`scripts/build_workbench_view_model.py`
- 输出目录：`同行资本市场内容系统/11_frontstage/`

## 验证

测试覆盖：
- today_overview 只包含结论字段
- today_article 不含 Runtime PID / OpenClaw / path-audit
- quality_check 不含 LaunchAgent / heartbeat
- replay_dashboard 不污染 today_article
- system_ops 包含 Runtime / LaunchAgent / OpenClaw
- debug_actions 只出现在 system_ops
