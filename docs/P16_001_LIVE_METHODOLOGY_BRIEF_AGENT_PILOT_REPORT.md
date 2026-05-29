# P16-001 Live Methodology Brief Agent Pilot Report

## 本轮目标

为 methodology-aware brief 增加 Claude/Anthropic live pilot sidecar。默认 dry-run，live 必须显式 env + allowlist + API key + cost guard。

## 已完成

- 新增 `live_methodology_brief_agent`。
- 输出 `latest_live_methodology_brief_pilot.json/md`。
- 默认 `limit=1`，不覆盖 `latest_methodology_content_briefs.json`。
- 所有调用写入 `agent_run_log`。

## 安全边界

- live 输出只作为 sidecar candidate。
- 不自动发布。
- 不自动替换规则型 brief。
