# P6-001 LLM Provider Config v1 Report

## 本轮目标

- 建立 LLM provider 配置。
- 默认 mock/dry-run，本地验收不需要 API key。
- 为 OpenAI / Anthropic / Gemini 保留 provider 占位。

## 新增文件

- `config/llm_providers.json`
- `src/content_system/llm_provider_config.py`
- `scripts/validate_llm_provider_config.py`

## 安全策略

- API key 只从环境变量读取。
- 配置文件只保存环境变量名，不保存真实 key。
- live mode 需要显式开启。
- 默认 provider 是 `mock`，默认 mode 是 `dry_run`。

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
