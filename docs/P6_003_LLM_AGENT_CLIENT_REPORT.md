# P6-003 LLM Agent Client v1 Report

## 本轮目标

- 建立统一 LLM Agent Client。
- 默认 mock/dry-run，不进行真实付费调用。
- 输出结构化 `LLMRequest` / `LLMResponse`。

## 新增文件

- `src/content_system/llm_agent_client.py`
- `scripts/run_llm_agent_client_smoke.py`

## Mock 行为

- `llm_proponent_agent` 输出支持理由。
- `llm_critic_agent` 输出批评和修改建议。
- `llm_judge_agent` 输出旁路裁判建议。
- `llm_rewrite_agent` 输出改稿建议。

## Live Mode 边界

Phase 6 v1 不默认实现真实 HTTP live 调用。非 mock live provider 会先做安全占位，后续 Phase 7 再做灰度 adapter。

## 新增命令

```bash
make llm-agent-smoke
```

## 验收方式

- `python3 -m py_compile src/content_system/llm_agent_client.py`
- `python3 -m py_compile scripts/run_llm_agent_client_smoke.py`
- `make llm-agent-smoke`
