# P28-005 Acquisition-to-Content Bridge Report

Phase 28 adds a bridge from connector-promoted topic candidates to daily content operations.

The bridge classifies promoted connector topics as `READY_FOR_BRIEF`, `NEEDS_EVIDENCE`, `WATCH`, or `REJECTED`, and gives the operator the recommended next pipeline step. It does not create briefs or drafts automatically and does not overwrite the content queue.

Command:

```bash
make acquisition-to-content-bridge
```

