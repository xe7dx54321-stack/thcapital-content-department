---
name: th-seed-refresh-and-source-scouting
description: Use when reselecting, refreshing, or expanding TH Capital's market-content source seeds across fixed watchlists and dynamic discovery lanes such as financing events, expert accounts, Reddit discussion heat, breakout community topics, video creators, official model/platform accounts, WeChat AI media, and open-source ecosystems.
---

# th-seed-refresh-and-source-scouting

Use this skill for Step 3 work when the task is about:

- reselecting source seeds
- refreshing the watchlist weekly
- scouting new source candidates from dynamic rules
- deciding whether a new entrance belongs in A / B / C
- deriving follow-up sources from a company, creator, product, or hot topic
- updating source registries after new discovery lanes prove useful

## Important boundary

- This skill governs **seed discovery and seed maintenance**
- It does **not** decide final topic priority
- It does **not** use “main battlefield / adjacent battlefield” to suppress upstream source intake
- It keeps source discovery broad inside the AI universe, then lets later stages do ranking

## Load order

1. Read `../../../00_planning/20260324_对象字典与命名规范.md`
2. Read `../../../00_planning/20260324_市场内容系统详细施工方案.md`
3. Read `../../../01_watchlists/20260324__watchlist-registry-board.md`
4. Read `../../../01_watchlists/20260325__seed-reselection-strategy.md`
5. Read `../../../01_watchlists/20260325__seed-candidate-pool.md`
6. If available, read `../../../08_brand_assets/latest__head-media-learning-rulebook-v1.md`
7. If the task also includes actual capture or packet preparation, read `../th-source-capture-and-citation/SKILL.md`

## Core workflow

1. Confirm the task type:
   - seed reselect
   - weekly refresh
   - new lane exploration
   - candidate review
   - registry update
   - derived-source creation

2. Separate the work into two buckets:
   - **fixed seeds**
   - **dynamic scouting rules**

3. Choose the relevant discovery lane(s):
   - financing / newco
   - expert view
   - Reddit discussion
   - breakout growth
   - video demo
   - official updates
   - WeChat CN AI
   - open-source / skill ecosystem
   - build in public

4. For each candidate source, record:
   - source name
   - platform
   - handle or URL
   - source type
   - whether it is primary / secondary / mirror / community / fallback
   - why this source is worth tracking
   - expected topic yield
   - citation value
   - capture feasibility
   - which registry it belongs to

5. Classify the candidate:
   - `A` = active now
   - `B` = strategically important but technically high-friction
   - `C` = manual / pending / shortlist

6. If the discovery result is an entity rather than a stable source, create a **derived-source chain**:
   - official site
   - founder or company X
   - YouTube channel or demo video
   - docs / blog / changelog
   - GitHub / skill / repo
   - community discussion entrance

7. Update the right output artifact:
   - source candidate pool
   - platform registry
   - watchlist board note
   - later source packet queue if actual capture starts

## Current proven capture stack

When deciding whether a lane can be promoted, use the **current verified stack** rather than old assumptions:

- **OpenAI News**
  - default: `Jina reader`
  - use for: listing page, article discovery, fast markdown extraction
  - caveat: direct page may still hit Cloudflare; final citation should point back to the original OpenAI URL

- **X**
  - default: `Jina reader`
  - fallback: authenticated X session when excerpt depth is insufficient
  - use for: signal discovery, viewpoint capture, post excerpting
  - caveat: X posts are usually signal sources, not final hard-evidence citations; follow embedded official links when possible

- **Reddit**
  - default: `reddit-readonly` via public JSON endpoints
  - use for: subreddit top/new, keyword search, thread context, top comments
  - caveat: community discussion is discovery-grade evidence; if a post mentions a company/product, derive the chain outward to official assets

- **Product Hunt**
  - default operational lane: `find-products` / `trend-hunt.com` mirror API
  - future upgrade: official Product Hunt API token
  - use for: product discovery, category scan, shortlist generation
  - caveat: third-party mirror output is an entrance, not final factual evidence; follow through to Product Hunt page and company site

- **Financing / newco**
  - default stable entrances: `YC Launches` + `TechCrunch AI`
  - strategic-but-blocked entrances: `FinSMEs AI`, official `Product Hunt` topic page
  - required derived chain: company name → official site → founder / company social → product/demo/docs → later financing confirmation

- **Browser fallback**
  - default: only when the lighter stack is blocked
  - load: `../th-web-access-fallback/SKILL.md`
  - use for: dynamic pages, login-dependent pages, screenshot / media evidence, stubborn anti-bot cases
  - caveat: this is a recovery and verification layer, not the default unattended cron path

## How to think about dynamic scouting

Some high-value work should **not** be forced into a fake fixed URL.

Examples:

- daily top Reddit discussions
- fastest-growing community topics
- latest financing events around agent startups
- 72-hour fast-rising open-source projects
- today’s hottest AI creator videos

For these, the correct output is:

1. the scouting rule
2. the candidate sources found this round
3. the reason they matter
4. whether any of them should be upgraded into a persistent seed

## Source-level judgment rules

When evaluating a seed, judge it on:

- signal quality
- topic production ability
- heat and growth sensitivity
- citation usefulness
- repeatability
- capture feasibility
- whether it can lead us back to primary sources quickly
- whether it fills a blind spot in the current pool

Do **not** judge it on:

- whether it is perfectly inside the main battlefield
- whether it sounds “on-brand” enough upstream

## Derived-source rules

If a source surfaces a promising company, product, creator, or tool:

1. do not stop at the entrance page
2. map the entity outward
3. convert it into follow-up watchlist candidates

Typical patterns:

- financing event → official site → founder X → demo video → docs / repo → community reaction
- hot creator take → original thread → high-signal comments → referenced products → alternative viewpoints
- trending repo → README / docs → maintainer handle → demo video → business use cases
- Reddit hot thread → thread context → top comments → referenced product / repo / workflow → official asset chain
- Product Hunt mirror result → Product Hunt page → official site → founder / demo / docs → whether it is worth long-term monitoring

## Hard constraints

- Do not invent a fake fixed URL for a dynamic rule.
- Do not upgrade a blocked source into `active` unless there is a plausible working capture path.
- Do not confuse a trend entrance with factual evidence.
- Do not let one platform dominate the whole seed pool.
- Do not suppress adjacent AI sources upstream just because they are not the main battlefield.
- Do not treat third-party mirror data as final evidence without following the link chain back to an official object.
- Do not let a high-heat entrance pretend to be a high-evidence source.

## Output guidance

When the task is **seed reselect**, output:

1. the lane structure
2. the A / B / C classification
3. the selected sources
4. the registry placement
5. the technical caveats

When the task is **weekly refresh**, output:

1. newly added seeds
2. downgraded / paused seeds
3. which sources actually produced good topic leads
4. which lanes are still blind

When the task is **derived-source creation**, output:

1. the trigger entity
2. the derived-source chain
3. which ones should enter registry now
4. which ones should stay in the candidate pool
