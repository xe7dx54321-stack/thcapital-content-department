# P29-004 Selected OpenClaw Metadata Connector Report

## Scope

Runs selected metadata-only connector sidecars for P0/P1 OpenClaw migration candidates.

## Connector Types

- `reddit_metadata`
- `media_metadata`
- `newsletter_metadata`
- `wechat_metadata`
- `youtube_metadata`
- `x_metadata`
- `trend_heat_metadata`
- `manual_backfill`

## Boundary

The connector emits metadata only. It does not fetch article bodies, use API keys, bypass login/paywalls, start OpenClaw gateway, or migrate cron jobs.
