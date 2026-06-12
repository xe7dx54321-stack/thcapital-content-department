# P31C-005 Query / Keyword / Lookback Strategy Report

`config/acquisition_query_strategies.yaml` keeps lane keywords, event terms, exclusions, lookback windows, max items, sort strategy, expansion triggers, language, region, and zero-result fallback in configuration.

Connectors should load these strategies instead of hard-coding keywords.
