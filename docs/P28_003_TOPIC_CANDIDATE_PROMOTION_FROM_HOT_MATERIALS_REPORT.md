# P28-003 Topic Candidate Promotion from Hot Materials Report

Phase 28 promotes qualified hot materials into connector topic candidates.

Only materials that pass the hot material quality gate and have traceable medium or high metadata-derived evidence can become `PROMOTED`. Weak evidence becomes `NEEDS_EVIDENCE`, lower urgency items become `WATCH`, and unsuitable items are `REJECTED`.

The promotion output is a sidecar queue. It does not overwrite methodology topic scores, content queue artifacts, drafts, prompts, rules, or source configuration.

Command:

```bash
make promote-hot-materials-to-topics
```

