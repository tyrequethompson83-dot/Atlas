---
name: atlas-news-impact
description: Use when the user asks for current news, News Impact, headlines affecting an instrument, geopolitical or macro catalysts, or why a market is moving.
---

# ATLAS News Impact

## Purpose

Recover the useful Forex Jarvis News Impact workflow inside OpenClaw's native skill system. Identify material current developments, classify them, determine which markets are exposed, explain the transmission channels, and compare the news narrative with observable market behaviour.

This skill is an analytical workflow. It does not create a second agent, fetch data by itself, install an RSS reader, or grant tools. Use only search, fetch, calendar, and market-data tools that are actually available in the active OpenClaw runtime.

## When to use

Use this skill for requests such as:
- "News Impact", "what is happening in the markets?", or "what news matters today?"
- "What news could affect gold / XAUUSDm / EURUSD / oil?"
- "Why did gold, oil, or a currency pair just move?"
- A headline or geopolitical development that may affect one or more instruments.
- A cross-asset catalyst outlook or a follow-up about an already displayed/retrieved event set.

For scheduled economic-calendar releases, actual-versus-forecast analysis, and detailed macro-release interpretation, use the separate economic-research workflow when that native skill or a suitable data source is available. Do not collapse scheduled calendar research into headline scanning.

## Source and capability boundary

The original Forex Jarvis implementation was inspected in:
- `atlas_auto/news_scanner.py` — RSS retrieval, keyword/category classification, severity, affected assets, and legacy heuristic impact estimates.
- `atlas_auto/tools/news.py` — read-only event/impact tools and filtering.
- `NEWS_IMPACT_READ_PATH.md` — the documented regression and verification for non-consuming news reads.
- `tests/test_news_feed_read_path.py` — tests using the real scanner with the feed fetch stubbed.
- `atlas_auto/config.py` — configured RSS feed defaults and category weights.

The original scanner's default feeds were ForexLive RSS feeds, configurable through `ATLAS_RSS_FEEDS` (with legacy `JARVIS_AUTO_RSS_FEEDS` compatibility). Those feeds are not automatically connected to OpenClaw by this skill.

**Current OpenClaw boundary:** the ATLAS branch contains the market-reading skill and an opt-in MT5 market plugin, but the Forex Jarvis RSS scanner, event classifier, news feed storage and original news tools have not been ported as working OpenClaw integrations. A skill file is not a live feed. Use available configured web-search/fetch tools for current research; if none are available, state that current news retrieval is unavailable. Never imply the legacy RSS scanner is connected.

## News intelligence workflow

### 1. Establish the scope

Resolve:
- Instrument(s) or market(s) the user cares about.
- Relevant time window: breaking/current, last session, today, this week, or a specified historical period.
- Whether they want headlines, a full impact outlook, or an explanation of a specific move.

Reuse a still-current event set already displayed or retrieved in this conversation. Refresh only when the user requests it, a material event changes, or timestamps/source coverage indicate that the set is stale or incomplete.

### 2. Gather and verify developments

Use configured OpenClaw search/fetch tools. Prefer primary sources for official statements, sanctions, central-bank communications, government announcements, and published data. Use reputable news wires and established financial-news publishers for breaking context.

For every material item, capture where available:
- Headline and concise factual summary.
- Publisher/source and direct article or primary-source link.
- Publication time and, separately, event time; retain timezone.
- Whether the report is confirmed, attributed, developing, disputed, or unverified.
- The latest update or correction when a story is changing.

Do not treat a headline as proof of every claim in its wording. Separate confirmed facts, attributed reports, analysis/opinion, and speculation. Cross-check material or conflicting claims before drawing a conclusion.

Do not present an old RSS item or article as breaking news. If dates, timestamps, or the current status cannot be verified, say so.

### 3. Classify the event

The original scanner's category vocabulary is the source-derived starting point:
- War
- Military escalation
- Sanctions
- Oil disruption
- Central bank
- Inflation
- Employment
- GDP / growth
- Banking crisis
- Natural disaster
- Supply-chain disruption
- Other relevant market development

Choose the primary category that best describes the catalyst; add a secondary category only when useful. Do not force a headline into a category because one keyword happens to appear in it.

### 4. Map exposed markets and instruments

Identify direct exposure first, then plausible secondary channels. Do not assume every headline affects every instrument.

Examples of exposure to investigate:
- **Gold:** real-rate and Treasury-yield expectations, USD, inflation expectations, central-bank credibility, geopolitical risk, safe-haven demand, and liquidity conditions.
- **Oil / energy:** physical supply or demand, OPEC decisions, production and transport infrastructure, shipping routes, inventories, and growth expectations.
- **FX pairs:** both currencies in the pair, relative central-bank expectations, relative yields, growth/inflation outlooks, trade/energy exposure, and risk sentiment.
- **Equities and rates:** earnings/cash-flow expectations, discount rates, sovereign risk, credit conditions, volatility and policy expectations.
- **Other assets:** include only when a credible transmission mechanism is present.

State which instruments are directly exposed, which are secondary/conditional, and which have no established connection from the evidence gathered.

### 5. Assess materiality and severity

Give a qualitative severity label (Low, Moderate, High, or Critical) and explain it. Consider:
- Credibility and independence of the source(s).
- Scale and geographic/economic reach.
- Whether the event is new, escalating, resolved, or already widely anticipated.
- Directness of the transmission channel to the instrument.
- Proximity to a market session or a key scheduled catalyst.
- Confirmed market response, when reliable observations exist.

Severity is an assessment of the event's significance, not a calibrated forecast of price movement or probability of a successful trade. Do not manufacture a numerical confidence score.

### 6. Explain possible impact channels

Explain the mechanism rather than assigning a fixed direction to a category. For each affected market, describe:
- The plausible supportive, negative, or mixed pressure.
- The intermediate variables that transmit the event (for example USD, yields, supply, demand, policy expectations or risk appetite).
- The time horizon: immediate headline reaction, near-term repricing, or a longer-running structural effect.
- What would strengthen or weaken that interpretation.

A geopolitical escalation can support safe-haven demand, but gold may still fall if USD/yields rise or liquidity selling dominates. An oil supply disruption can lift oil while also worsening inflation expectations. A central-bank headline matters through how it changes the expected policy path relative to what was already priced in. Keep these channels conditional.

### 7. Check the actual market response

Only describe a reaction as observed when actual, timestamped market data is available in the current turn or valid conversation context. Use the available quote/candle tool for the explicit instrument and timeframe when appropriate; preserve source, timestamp, freshness, spread and timeframe.

Distinguish:
- **Expected channel:** the mechanism that could affect price.
- **Observed response:** what verified price or cross-market data actually did.
- **Interpretation:** whether the observed response supports, contradicts or has not yet tested the expected channel.

If no reliable market data is available, say "market reaction not verified" rather than guessing. A news article describing a price move is not a substitute for a verified quote/candle series when precise reaction measurement is required.

### 8. Build a useful outlook

For a full News Impact report:
- Group events by affected asset/market, not only by publisher or headline category.
- Rank the most material catalysts first.
- Show severity and the reason for it.
- Explain direct and secondary impact channels.
- Give bullish/supportive, bearish/negative, and mixed/neutral implications only where the evidence warrants them.
- State what to watch next and what new evidence would change the assessment.

For a single-headline question, answer directly without generating an unnecessary full-market report.

## Legacy-model limitations — do not present as forecasts

The original scanner's `PAIR_IMPACT` table and category weights produced fixed heuristic percentage estimates, scaled by a keyword-derived severity score. The `confidence` value was set equal to that severity score. These fields were part of the old implementation, but they were not statistically calibrated forecasts or independently measured predictive confidence.

Do not recreate or quote those percentages as expected market moves. Do not turn keyword counts into a probability that price will rise or fall. The useful capability to recover is event collection/classification, affected-market reasoning, severity context, and an explanation of the transmission mechanism—not the old hard-coded percentage table.

This first News Impact skill does not require a historical event-reaction database. Do not invent historical samples, event-study results, MFE/MAE, reaction windows, or predictive accuracy.

## Read-only behaviour and feed integrity

The original Forex Jarvis bug showed that an AI read could consume the NewsScanner's seen-watermark and cause later News-panel reads to lose events. The fixed source used `NewsScanner.peek()` on the orchestrator's existing scanner.

Preserve that invariant in any future feed integration:
- Reading or summarising news must not advance a seen watermark, consume a headline, clear a feed, or change what another surface displays.
- Do not instantiate a separate scanner with a different watermark for an answer.
- An explicit user-requested refresh may use a separately defined refresh operation, but never hide such a state change inside an ordinary question.
- Distinguish an empty result from a feed/provider failure. "No matching events" is not proof that there is no market impact.
- Repeated reads of an unchanged feed should return a consistent event set; do not progressively drain it.

The source audit in Forex Jarvis documented 12/12 focused read-path tests passing and a live check where repeated answers returned 17 events while the persisted watermark remained unchanged. Its broader suite had one documented pre-existing unrelated failure. These are historical results recorded in that repository, not tests run against the OpenClaw skill or current feeds.

## Response format

For a full report, use a compact table:

| Event / catalyst | Source and time | Category / severity | Affected markets | Plausible impact channel | What to watch |
|---|---|---|---|---|---|

Then add:
1. **Overall picture:** the two or three developments that matter most.
2. **Market implications:** instrument-specific channels, clearly conditional.
3. **Observed response:** include only when supported by timestamped market data; otherwise mark it unverified.
4. **Next catalysts:** what is upcoming or what new evidence would change the view.

Cite each material claim with the source actually consulted. Keep event time distinct from publication time. Do not fill the table with low-value headlines just to increase its length.

## Safety and execution boundary

This is research and analysis only. It does not authorise trading, retrieve account balances or positions, or place/modify/cancel orders. Never convert a headline, severity label, or impact interpretation into trade authorization. Any future execution remains subject to the separate explicit approval boundary and Live Mode gate.
