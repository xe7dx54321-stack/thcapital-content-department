# Daily Scheduler Runbook

## 当前策略

Phase 7 只提供本地调度 runner 和文档，不自动创建系统任务。

默认命令：

```bash
make daily-scheduler
```

该命令运行安全 pipeline，不会自动启用 live mode。

## Dry-run 检查

```bash
python3 scripts/run_daily_scheduler.py --dry-run
```

## 指定 Pipeline

```bash
python3 scripts/run_daily_scheduler.py --pipeline learning-daily
python3 scripts/run_daily_scheduler.py --pipeline phase6-daily
```

## macOS cron 示例

```cron
0 9 * * * cd /path/to/thcapital-content-department && /usr/bin/make daily-scheduler
```

## macOS launchd 建议

使用 launchd 时，将工作目录设为仓库根目录，将命令设为：

```bash
make daily-scheduler
```

不要在 plist 中写 API key。真实 live key 应只存在于本机安全环境变量或密钥管理工具中。

## 安全边界

- 不自动开启 live。
- 不自动发布。
- 不自动改规则。
- 不创建数据库。
