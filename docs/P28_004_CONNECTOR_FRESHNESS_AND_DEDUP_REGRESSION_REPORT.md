# P28-004 Connector Freshness and Dedup Regression Report

Phase 28 adds a regression gate for connector metadata hygiene.

Checks cover metadata-only/copyright-safe boundaries, duplicate ratio, stale and unknown freshness ratios, evidence traceability for promoted topics, evidence URL presence, and weak-signal handling.

The regression gate is advisory and sidecar-only. It does not fetch external pages, change connectors, or migrate OpenClaw sources.

Command:

```bash
make connector-freshness-dedup-regression
```

