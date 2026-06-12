# P31C-006 Fallback / Backfill / Confirmation Strategy Report

`config/acquisition_fallback_strategies.yaml` defines what happens when acquisition is weak, empty, incomplete, or needs confirmation.

Supported outcomes include primary source required, second source required, manual review required, keyword expansion, alternative source, watch only, and blocked.

Weak signal lanes remain unable to become hard evidence by themselves.
