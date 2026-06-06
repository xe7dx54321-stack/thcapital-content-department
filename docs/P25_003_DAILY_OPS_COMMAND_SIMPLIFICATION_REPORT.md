# P25-003 Daily Ops Command Simplification Report

## Goal

Expose one primary command for daily operations: `make stable-daily-ops`.

## Pipeline

1. Run Phase 24 stable trial pipeline.
2. Build stable daily ops baseline.
3. Build operator acceptance checklist.
4. Build workbench data.
5. Build workbench frontend.

## Boundary

The command is manual-ops only and does not publish.
