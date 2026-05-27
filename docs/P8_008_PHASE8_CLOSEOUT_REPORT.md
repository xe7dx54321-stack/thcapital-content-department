# P8-008 Phase 8 Closeout Report

## Phase 8 v1 目标

将 Phase 0-7 的文件型透明产物补上一层本地 runtime index、repository 查询、发布 dry-run、人审 console、成本保护和生产化运行手册。

## 已完成能力

- SQLite runtime store。
- Artifact repository API。
- Publishing API dry-run adapter。
- Human review console。
- Cost budget guard。
- Production runbook。
- Phase 8 daily production pipeline。

## Runtime Store

数据库默认写入 `同行资本市场内容系统/12_runtime_store/content_system_runtime.db`，仅作本地索引，数据库文件不入库。

## Artifact Repository

提供统一查询 API，用于近期 content artifacts、agent runs、publishing candidates 和 human feedback 的检索。

## Publishing Dry-run

发布 dry-run 永远不真实发布，`would_publish` 固定为 `false`，人工确认仍是硬门槛。

## Human Review Console

汇总 publishing candidates、human exceptions、pending feedback、publishing dry-run、agent conflicts 和 weekly retro highlights。

## Cost Budget Guard

读取 provider limits、环境变量和 agent run log，输出 `ALLOW/WARN/BLOCK` 与推荐模式。

## Production Pipeline

推荐日常入口：

```bash
make phase8-daily
```

## 当前限制

- SQLite 不是远程数据库，也不是唯一事实源。
- 发布 API 仍为 dry-run。
- human review console 不是 Web UI。
- cost guard 暂不强制拦截所有 live call。
- live mode 仍需显式 env + allowlist。

## 下一阶段建议

Phase 9：真实发布集成与人机协作 UI。

- P9-001：Publishing Platform Credential Config v1。
- P9-002：Wechat Draft API Dry-run to Sandbox v1。
- P9-003：Xiaohongshu Manual Package Export v1。
- P9-004：Review Console UI v2。
- P9-005：Production Backup / Restore v1。
- P9-006：Multi-day Analytics Dashboard v1。
