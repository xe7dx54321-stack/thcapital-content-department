# P26-001 Source Coverage Gap Audit Report

## Goal

Audit upstream source coverage so daily content ops can explain weak material supply before downstream production starts.

## Inputs

- `config/sources.yaml`
- source runtime health, daily source run summary, official runtime manifest
- high-value candidates and methodology topic scores
- stable daily ops summary

## Output

Writes sidecar JSON/Markdown reports under `同行资本市场内容系统/10_logs/` and a frontstage board.

## Boundary

This audit does not fetch external sources, bypass logins, mutate `config/sources.yaml`, or fabricate hot topics.
