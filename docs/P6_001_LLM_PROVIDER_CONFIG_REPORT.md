# P6-001 LLM Provider Config v1 Report

## 本轮目标

- 建立 LLM provider 配置。
- 默认 mock/dry-run，本地验收不需要 API key。
- 新增并启用 `manimax` 与 `anthropic` provider lane。
- 为 OpenAI / Gemini 保留 provider 占位。
- 建立 agent model map：轻量任务使用 `manimax-2.7`，高判断任务使用 `claude-sonnet-4.6`。

## 新增文件

- `config/llm_providers.json`
- `src/content_system/llm_provider_config.py`
- `scripts/validate_llm_provider_config.py`

## Model Routing

- `llm_proponent_agent`：`manimax` / `manimax-2.7`。
- `llm_critic_agent`：`anthropic` / `claude-sonnet-4.6`。
- `llm_judge_agent`：`anthropic` / `claude-sonnet-4.6`。
- `llm_rewrite_agent`：`anthropic` / `claude-sonnet-4.6`。
- title/opening/structure pattern extractors：`manimax` / `manimax-2.7`。
- content recipe / pattern adapter / rule update suggestion：`anthropic` / `claude-sonnet-4.6`。
- dashboard / run summary：`manimax` / `manimax-2.7`。

## 安全策略

- API key 只从环境变量读取。
- 配置文件只保存环境变量名，不保存真实 key。
- live mode 需要显式开启。
- 默认 provider 是 `mock`，默认 mode 是 `dry_run`。
- 两条真实 provider lane 均记录 Anthropic Messages API 兼容方式：`x-api-key`、`anthropic-version: 2023-06-01`、非 stream。

## 新增命令

```bash
make llm-config-validate
```

## 验收方式

- `python3 -m py_compile src/content_system/llm_provider_config.py`
- `python3 -m py_compile scripts/validate_llm_provider_config.py`
- `make llm-config-validate`

## 下一步

进入 P6-002 Prompt Registry v1。
