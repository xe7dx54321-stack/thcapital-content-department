# market-scout runtime state — 20260520

## meta
- run_token: 20260520
- run_date: 2026-05-20
- lanes_active: day_mainline
- business_window: T-1 17:00 → T 14:30
- current_time: 2026-05-20 16:55 CST (outside business window)
- agent: market-scout / day-mainline-top20-pack

## top20 pack status
- canonical_path: /Users/apple/Documents/同行资本市场内容系统/03_topic_candidates/20260520__top20-screening-pack.md
- canonical_size: 5584 bytes
- artifact_status: FINAL (confirmed via market_stage_artifact_status.py, exit 0)
- reworked_version_written: false
- reworked_path: (none)

## top6 candidates (limited enhancement scope)
1. Guardrails 8B model 53%→99% agentic tasks (score=20, ACM CAIS '26 preprint)
2. Bytedance 3B open source model (score=15, new product signal)
3. Google AI Edge Gallery v1.0.13/14 Gemma 4 MCP (score=15, new product signal)
4. HRM-text New SOTA 1B model (score=15, new product signal)
5. Anthropic announced vs current compute capacity (score=15, new product signal)
6. Pacman benchmark Qwen 3.6 27B local coding agent (score=10)

## lane guard check
- morning_flash objects: (isolated lane, not tracked here)
- publish_queue objects: (isolated lane, not tracked here)
- re-injection into day_mainline: BLOCKED — morning_flash / publish_queue isolation respected

## official lane evidence (for record)
- official_lane entries captured 2026-05-20 13:58 CST (before business window)
- Top official lane entries by score:
  - score=47: OpenAI GPT-5.5 Powers Codex on NVIDIA Infrastructure
  - score=39: NVIDIA and SAP Bring Trust to Specialized Agents
  - score=36: Parloa builds service agents (voice-driven AI customer service)
  - score=32: NVIDIA Nemotron 3 Nano Omni Model
  - score=31: Vera CPU — NVIDIA's first CPU built for agents
  - score=29: OpenAI and Dell partner on Codex hybrid/on-premise
  - score=29: Databricks brings GPT-5.5 to enterprise agent workflows
- These did NOT appear in today's Top20 pack (pack is purely Reddit-sourced)

## enforcement actions taken
- guard.py ran: OK (20260520__top20-screening-pack.md written, 5585 bytes)
- artifact_status confirmed: FINAL, exit 0 — no rewrite triggered
- Business window expired before limited enhancement could be executed

## outcome
- Status: COMPLETE (pack already final; business window expired → no new deep reads)
- Top20 pack: final and scoreable
- Pack path: /Users/apple/Documents/同行资本市场内容系统/03_topic_candidates/20260520__top20-screening-pack.md
- Runtime log: /Users/apple/Documents/同行资本市场内容系统/10_logs/20260520__market-scout-runtime-state.md
- Final candidate count: 20
- Reworked version written: no