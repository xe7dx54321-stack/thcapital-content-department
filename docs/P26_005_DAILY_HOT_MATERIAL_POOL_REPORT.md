# P26-005 Daily Hot Material Pool Report

## Goal

Combine hot signals, official manifest signals, topic candidates, and backfill tasks into a daily upstream material pool.

## Output

Materials are tagged as `write_now`, `develop_topic`, `watch`, `backfill_first`, or `hold`.

## Boundary

The material pool is upstream supply. It does not create mainline topics, drafts, or publishing actions.
