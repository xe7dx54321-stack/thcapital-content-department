# Production Runbook

## 当前生产化边界

系统已经具备采集、结构化、内容生产、Agent 审核、反馈学习、live pilot、调度报告和本地 runtime store。当前仍不是自动发布系统：live mode 必须显式启用，发布 API 只做 dry-run，人工确认仍是硬门槛。

## 每日推荐流程

```bash
make phase7-daily
make runtime-store-sync
make runtime-store-summary
make publishing-dry-run
make human-review-console
```

更完整的 Phase 8 入口：

```bash
make phase8-daily
```

## 每周推荐流程

```bash
make weekly-content-retro
make artifact-repository-sync
```

## 如何开启 live mode

仅在明确灰度时开启，并配置 allowlist：

```bash
export THCAP_LLM_ENABLE_LIVE=1
export THCAP_LLM_MODE=live
export THCAP_LLM_LIVE_AGENT_ALLOWLIST=llm_proponent_agent
```

然后使用单 agent pilot 命令，不要直接把全链路切成 live。

## 如何关闭 live mode

```bash
export THCAP_LLM_ENABLE_LIVE=0
export THCAP_LLM_MODE=dry_run
unset THCAP_LLM_LIVE_AGENT_ALLOWLIST
```

## 如何检查 API key 没有入库

```bash
git grep -n "API_KEY=.*[A-Za-z0-9_-]\\{20,\\}" || true
git status --short
```

不要提交 `.env`、token、cookie、真实平台凭证或本地数据库文件。

## 如何查看 runtime store

默认数据库位置：

```text
同行资本市场内容系统/12_runtime_store/content_system_runtime.db
```

常用命令：

```bash
make runtime-store-summary
sqlite3 同行资本市场内容系统/12_runtime_store/content_system_runtime.db ".tables"
```

## 如何备份 runtime store

```bash
mkdir -p _archive/runtime_store
cp 同行资本市场内容系统/12_runtime_store/content_system_runtime.db _archive/runtime_store/content_system_runtime_$(date +%Y%m%d).db
```

备份目录默认不入库。

## 如何处理失败

```bash
make failure-notification
make retry-fallback-runner
make runtime-store-summary
```

先看 `latest_failure_notification.md`，再决定是否重跑单步命令。

## 如何进行发布 dry-run

```bash
make publishing-dry-run
```

检查 `would_publish` 必须始终为 `false`。发布前必须人工确认事实、标题、风险提示和平台格式。

## 哪些事情仍需要人工确认

- 是否发布。
- 是否采用 LLM rewrite suggestion。
- 是否开启 live mode。
- 是否处理 human exception。
- 是否调整规则或 prompt。
- 是否将内容交给真实平台。

## 禁止事项

- 不自动发布。
- 不提交 API key。
- 不提交 `.env`。
- 不提交 SQLite 数据库。
- 不让 LLM judge 覆盖 rule judge。
- 不让 rewrite 覆盖原稿。
- 不自动修改规则。
