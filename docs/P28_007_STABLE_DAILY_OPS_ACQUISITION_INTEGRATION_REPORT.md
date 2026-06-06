# P28-007 Stable Daily Ops Acquisition Integration Report

Phase 28 extends `make stable-daily-ops` with acquisition-to-content visibility.

The stable daily summary now includes upstream supply, connector item count, evidence packet count, promoted topic count, ready-for-brief count, and needs-evidence count. If new connector topics are ready for brief, the operator is prompted to start brief production after human source review. If topics need evidence, the operator is prompted to backfill evidence first.

This does not automate publishing, drafting, prompt/config/rule mutation, or full-text crawling.

Command:

```bash
make stable-daily-ops
```

