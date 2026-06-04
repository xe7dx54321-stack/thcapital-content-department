# P20-002 Content Ops Failure Handling Report

## Goal

Convert source, pipeline, queue, visual, publishing, metrics, and workbench failures into operator-facing handling advice.

## Outputs

- `latest_content_ops_failure_handling.json`
- `latest_content_ops_failure_handling.md`
- `latest_content_ops_failure_handling_board.md`

## Boundary

The module only recommends manual actions. It does not retry pipelines, publish, or mutate strategy config.
