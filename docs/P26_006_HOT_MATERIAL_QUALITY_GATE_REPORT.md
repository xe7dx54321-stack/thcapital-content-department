# P26-006 Hot Material Quality Gate Report

## Goal

Prevent noisy upstream materials from flowing into content production without evidence and freshness checks.

## Decisions

- `PROMOTE_TO_TOPIC_PIPELINE`
- `WATCH`
- `BACKFILL_REQUIRED`
- `REJECT`

## Boundary

The gate only recommends. It does not promote mainline topics or fetch external evidence.
