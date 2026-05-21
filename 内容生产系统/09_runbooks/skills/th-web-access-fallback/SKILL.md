---
name: th-web-access-fallback
description: Use when TH Capital market-content source capture hits dynamic pages, login walls, anti-bot friction, missing media evidence, or other cases where the normal RSS / API / HTML / Jina stack is not enough and browser-grade fallback is required.
---

# th-web-access-fallback

Use this skill when source capture or source verification hits one of these situations:

- the normal stack cannot read the page reliably
- the target page is heavily dynamic and needs a real browser
- the page requires an already logged-in session
- the task needs screenshots, image extraction, or video frame evidence
- a source exists, but static entry points keep returning the wrong result

## Important boundary

- This skill is a **fallback layer**, not the default daily intake path.
- Daily unattended cron capture should still prefer:
  - RSS
  - official JSON / API
  - direct HTML parsing
  - stable Jina snapshots
- Only escalate here when the lighter path is blocked or clearly low-confidence.

## Load order

1. Read `../th-source-capture-and-citation/SKILL.md`
2. Read `../../20260325__market-topic-capture-runbook.md`
3. Read the installed global skill:
   - `/Users/apple/.codex/skills/web-access/SKILL.md`

## When to escalate

- `YouTube`:
  - static channel parsing fails
  - you need to inspect a specific video page, transcript surface, or screenshot frame
- `GitHub`:
  - trending or repo page is reachable but static parsing loses key data
  - you need to verify README / release / demo behavior in-browser
- `X / 小红书 / 微信公开页`:
  - static layer is blocked or incomplete
  - login state or browser interaction is required
- `截图 / 媒体取证`:
  - the packet needs visual evidence instead of text-only capture

## Core workflow

1. Try the normal stack first.
2. If the normal stack fails, record exactly which path failed and how.
3. Load `web-access`.
4. Use the lightest browser-capable path that can recover the target:
   - page read
   - DOM extraction
   - screenshot
   - media URL extraction
   - interaction only if necessary
5. Preserve:
   - original URL
   - capture timestamp
   - what failed before fallback
   - what was recovered by browser fallback
6. If the fallback reveals a reusable pattern, update the relevant runbook or parser so future rounds can move back to the automated lane.

## Environment check

Before CDP mode, verify:

```bash
bash /Users/apple/.codex/skills/web-access/scripts/check-deps.sh
```

Current requirement:

- `Node.js 22+`
- Chrome remote debugging enabled in `chrome://inspect/#remote-debugging`

## Output guidance

When using this fallback, always report:

1. the blocked source
2. the failed default path
3. the fallback method used
4. the recovered evidence
5. whether this should become:
   - permanent parser upgrade
   - manual business fallback only
   - temporary one-off recovery
