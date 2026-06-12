# Acquisition Source Playbook

The source playbook answers where a lane fetches from, how much metadata to fetch, how far back to look, and which confirmation sources should be used.

Important rules:

- `metadata_only: true` is the default.
- `full_text_allowed: false` is required.
- Login, API keys, paywall bypass, and full-text scraping are not allowed.
- Weak signal sources cannot be hard evidence.
