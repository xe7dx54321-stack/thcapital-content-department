# P29-005 Weak Signal Safety Gate Report

## Scope

Prevents OpenClaw migrated weak sources from being treated as hard evidence.

## Gate Behavior

- Reddit, X, YouTube, trend heat, and WeChat default to weak/supporting roles.
- `can_use_as_hard_evidence=false` is enforced for migrated signals.
- Confirmation or manual review is required before content claims.

## Boundary

Weak signal safety gate is advisory and protective; it does not publish, fetch full text, or mutate source config.
