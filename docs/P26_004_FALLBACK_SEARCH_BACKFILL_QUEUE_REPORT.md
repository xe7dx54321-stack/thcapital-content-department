# P26-004 Fallback Search & Backfill Queue Report

## Goal

When hot signals are weak, create manual-first backfill tasks with lane, priority, query, target sources, and expected output.

## Boundary

All tasks are `do_not_auto_fetch=true`. The queue does not run searches, scrape paid/login sources, or mutate source configuration.
