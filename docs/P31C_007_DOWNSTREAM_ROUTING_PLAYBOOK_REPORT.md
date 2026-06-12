# P31C-007 Downstream Routing Playbook Report

`config/acquisition_downstream_routing.yaml` routes each lane into normalized items, hot material pool, weak signal pool, evidence packet, evidence backfill, confirmation queue, topic scoring, angle library, manual review, watch, or reject.

Guards prevent weak signals from direct brief routing and prevent manual-only sources from direct topic scoring.
