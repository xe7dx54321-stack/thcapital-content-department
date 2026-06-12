# Phase 31C Closeout

## 目标

Migrate OpenClaw acquisition know-how into the current Content Factory as configuration-driven playbooks.

## OpenClaw Acquisition Semantics Audit

OpenClaw cron jobs are read only as historical semantics. Valuable acquisition jobs are mapped to current lanes; unsafe publication, draft, full-text, or credentialed behaviors are excluded.

## Acquisition Lane Taxonomy

The project now has a unified lane taxonomy in `config/acquisition_lanes.yaml`.

## Lane-specific Cadence

Lane cadence is configured in `config/acquisition_cadence.yaml`, with grouped windows, catch-up policy, network requirement, and dedup policy.

## Source Fetch Methods

`config/acquisition_source_playbooks.yaml` defines safe metadata fetch methods and explicitly blocks full-text, login, and paywall bypass patterns.

## Query / Keyword / Lookback

`config/acquisition_query_strategies.yaml` centralizes keywords, event terms, exclusions, lookback, max items, sort, expansion, language, and region.

## Fallback / Backfill / Confirmation

`config/acquisition_fallback_strategies.yaml` routes incomplete or weak signals to primary source search, second-source confirmation, manual review, watch, or blocked.

## Downstream Routing

`config/acquisition_downstream_routing.yaml` determines whether lane outputs enter evidence, hot material, weak signal, confirmation, topic scoring, angle library, manual review, watch, or reject.

## Runtime Integration

The Runtime now builds a lane-batched acquisition plan and regression gate without copying OpenClaw jobs or creating source-level daemon tasks.

## Coverage and Duplicate Regression

`make acquisition-playbook-regression` checks mapping coverage, lane completeness, weak-signal boundaries, duplicate source slots, duplicate connector runs, and forbidden fetch behavior.

## Workbench Panel

The Workbench shows the Acquisition Playbook in the Runtime / upstream operations area.

## Autonomous Acquisition Dry Run

`make autonomous-acquisition-dry-run` validates the playbook end to end in dry-run mode.

## OpenClaw 旧经验迁移覆盖率

High-value OpenClaw acquisition jobs are mapped to current lanes where semantics are available. Low-confidence or unsafe jobs remain excluded.

## 未迁移的旧能力

OpenClaw gateway, cron runtime, full-text scraping, WeChat deep fetch, publication, drafts, login-state sources, and automatic publishing are not migrated.

## 安全边界

No auto publish, no WeChat API, no drafts, no full text, no login/paywall bypass, no image generation, no OpenClaw mutation, and no weak-signal promotion to hard evidence.

## 当前限制

The playbook is metadata-first and still requires later connector implementations to consume every strategy deeply.

## 下一阶段

Phase 32：Legacy Content Know-how Migration & Autonomous Topic-to-Article Production v1.
