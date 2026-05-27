# P6-002 Prompt Registry v1 Report

## 本轮目标

- 建立 LLM agent prompt registry。
- 管理 proponent / critic / judge / rewrite agent 的 prompt、输入 schema、输出 schema 和版本。
- 为后续真实 LLM live mode 做 prompt 版本化准备。

## 新增文件

- `config/agent_prompts.json`
- `src/content_system/prompt_registry.py`
- `scripts/validate_agent_prompts.py`

## Prompt 安全原则

- 只使用输入 evidence。
- 不编造事实。
- 不发布内容。
- 不调用外部工具。
- 输出 JSON。

## 新增命令

```bash
make agent-prompts-validate
```

## 验收方式

- `python3 -m py_compile src/content_system/prompt_registry.py`
- `python3 -m py_compile scripts/validate_agent_prompts.py`
- `make agent-prompts-validate`

## 下一步

进入 P6-003 LLM Agent Client v1。
