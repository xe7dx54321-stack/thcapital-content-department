# Stable Daily Ops Baseline

## Daily Command

Run:

```bash
make stable-daily-ops
```

This command rebuilds the stable trial baseline, operator acceptance checklist, and workbench data. It is an operations assistant command, not a publishing command.

## Normal Result

`SUCCESS` or `ACTIONABLE` is acceptable when there are no blockers and every content issue has a next operator action.

`ready_to_publish=0` does not mean the system failed. It means the current content inventory still needs human quality, evidence, rewrite, visual, or publishing checklist work.

## True Blockers

- Pipeline crash.
- Safety boundary violation.
- Remaining blocking issue in stable ops readiness.
- Publishing checklist regression failure.
- Workbench cannot be generated or opened.

## Safety Boundaries

- No automatic publishing.
- No WeChat API.
- No draft-box creation.
- No backend metric scraping.
- No image generation.
- No image model call.
- No automatic prompt/config/rule changes.
- No mainline content overwrite.
