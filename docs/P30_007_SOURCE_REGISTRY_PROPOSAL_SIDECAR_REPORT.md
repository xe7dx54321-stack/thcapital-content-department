# P30-007 Source Registry Proposal Sidecar Report

## Goal

Generate a sidecar proposal for which OpenClaw migrated sources may eventually be added to `config/sources.yaml`.

## Hard Rules

- `auto_apply=false`.
- Do not modify `config/sources.yaml`.
- Do not stage proposed YAML as config.
- Keep manual-only and blocked sources out of enabled automated ingestion.

## Boundary

This is a proposal artifact only.
