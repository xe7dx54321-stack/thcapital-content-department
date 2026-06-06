# P29-002 OpenClaw Source Risk Classification Report

## Scope

Classifies migrated OpenClaw sources by priority, ingestion allowance, evidence role, copyright risk, and fact risk.

## Classification Rules

- Public media/newsletter metadata can be `metadata_connector`.
- Reddit, YouTube, X, and trend heat are weak signal or heat validation only.
- WeChat is manual metadata/backfill only.
- Login/paywall/full-text/draftbox/publishing flows are blocked.

## Boundary

Risk classification does not fetch sources, mutate config, or promote weak signals to hard evidence.
