# P28-008 Phase 28 Daily Enrichment Pipeline Report

Phase 28 adds a daily enrichment pipeline:

1. Run Phase 27 connector pipeline.
2. Build connector reliability guidance.
3. Enrich connector metadata into evidence packets.
4. Promote qualified hot materials to topic candidates.
5. Run freshness and dedup regression.
6. Build acquisition-to-content bridge.
7. Run stable daily ops.
8. Rebuild workbench data and frontend.

The pipeline is sidecar-only and does not publish, call WeChat API, generate images, fetch full text, mutate config/prompt/rules, overwrite mainline content, or migrate OpenClaw sources.

Command:

```bash
make phase28-daily
```

