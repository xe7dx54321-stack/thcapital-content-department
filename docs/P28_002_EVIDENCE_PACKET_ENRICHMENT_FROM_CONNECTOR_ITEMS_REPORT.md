# P28-002 Evidence Packet Enrichment from Connector Items Report

Phase 28 enriches normalized upstream connector metadata into connector evidence packets.

Evidence packets are derived only from title, URL, source metadata, published/fetched timestamp, source type, lane, event type, and short metadata summary. They are explicitly marked `metadata_only=true` and `copyright_safe=true`, and they must not be treated as full-text evidence or automatic fact verification.

OpenClaw migration fields are reserved as non-invasive metadata only: `source_origin`, `migration_candidate`, `weak_signal_lane`, and `openclaw_candidate_ref`. Phase 28 does not import OpenClaw cron, gateway, or old source registry.

Command:

```bash
make connector-evidence-enrichment
```

