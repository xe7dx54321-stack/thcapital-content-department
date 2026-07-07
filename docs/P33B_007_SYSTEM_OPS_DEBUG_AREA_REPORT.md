# P33B-007 System Ops / Debug Area Report

## 页面定位

集中放 Runtime、LaunchAgent、OpenClaw、日志、调试信息。

普通每天审稿时不需要看这里。

## 页面结构

### A. 系统健康

展示：
- Runtime 状态
- LaunchAgent 状态
- Heartbeat age
- Next scheduled run
- Go-Live Gate
- blocking failures

### B. 今日任务状态

展示：
- 今日 scheduled jobs
- 成功
- 等待
- 失败
- 重试队列
- missed-run catch-up

### C. 数据采集状态

展示：
- Acquisition lane 状态
- 下一轮采集
- 失败 source
- 延迟 retry
- 网络 readiness

### D. OpenClaw 共存状态

展示：
- OpenClaw conflict_count
- manual_review_count
- safe_to_disable
- gateway 是否未修改
- cron 是否未修改

### E. 调试工具

**只在这里放调试按钮：**
- 刷新系统状态
- 暂停 Runtime
- 恢复 Runtime
- 手动补跑今日内容生产
- 运行 Go-Live Acceptance
- 查看最新日志

危险按钮必须有确认提示。

## 设计原则

- debug actions 只出现在 system_ops
- Runtime PID 只出现在系统运维页
- raw logs 默认折叠
- 系统运维页可以更宽（1180px+）

## 数据来源

来自 `workbench_view_model.system_ops`。

## 安全边界

- 不修改 OpenClaw jobs.json
- 不接 OpenClaw gateway
- 不修改 OpenClaw cron
- 不停用 OpenClaw jobs
- 不关当前 Mac mini Runtime / LaunchAgent
- 不提交 runtime SQLite、PID、lock、heartbeat、运行日志
