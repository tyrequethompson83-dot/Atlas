---
name: atlas-macro-research
description: Use for economic releases, central-bank decisions, actual-versus-forecast analysis and macro effects on currencies, gold and oil.
---

# ATLAS Macro Research

## Purpose

Research scheduled economic events and macro policy developments. Establish what was expected, what was released, how the details alter the policy/economic outlook, and which transmission channels matter for the instrument being discussed.

This skill is separate from `atlas-news-impact`: headline/geopolitical intelligence belongs there; scheduled economic releases and macro-event interpretation belong here.

## Source basis and integration boundary

The original Forex Jarvis research layer was inspected in:
- `atlas_auto/tools/research.py`
- `atlas_auto/research/biquote_source.py`
- `atlas_auto/research/sync.py`
- `atlas_auto/research/surprise.py`
- `atlas_auto/research/store.py`
- `atlas_auto/research/reaction.py`
- `tests/test_atlas_research_phase5.py`
- `tests/test_atlas_research_biquote.py`

That implementation separates a configurable calendar provider, event normalization/sync, a persistent research store and deterministic surprise arithmetic. Biquote adapter tests explicitly mock HTTP; they do not prove current live provider availability.

The OpenClaw branch currently has `atlas_economic_surprise`, a deterministic calculator for sourced actual-minus-forecast values. It does not fetch a calendar, synchronize Biquote, or maintain the Forex Jarvis research store. Do not claim those integrations are connected. Use configured OpenClaw search/fetch or calendar tools when present; otherwise report the missing source.

The existing Forex Jarvis historical reaction engine and reaction database are not a prerequisite for this skill. Do not build fixed historical reaction estimates into the workflow.

## Research workflow

### 1. Resolve the event and instrument

Identify:
- Event name and country/region.
- Scheduled or release timestamp with timezone.
- Instrument or market being researched.
- Whether the event is upcoming, released, revised, or from a historical period.
- The time horizon the user cares about.

For a currency pair, consider both currencies. For gold quoted in USD, include USD and US macro/policy events as directly relevant, while checking whether the event actually changes the market's policy expectations.

### 2. Retrieve authoritative event evidence

Prefer official sources:
- National statistics agencies for CPI, PPI, employment, GDP and other releases.
- Central banks for rate decisions, statements, projections, minutes and speeches.
- Treasury/debt offices for auctions and issuance.
- Official agencies for policy, fiscal and trade announcements.

A reputable calendar/news source may be used for consensus forecasts and event schedules when the official publisher does not publish consensus. Keep forecast provenance distinct from the official release.

Capture, where available:
- Actual.
- Consensus forecast.
- Previous reading.
- Revised previous reading.
- Units and period (m/m, y/y, quarterly, annualized, index points, jobs, etc.).
- Headline and core components where relevant.
- Release timestamp and timezone.
- Source URL and retrieval/publication time.

Do not fill a missing value with zero. Do not silently mix monthly and annual rates or different units. A calendar's event-impact label is source metadata, not proof of the market's reaction.

### 3. Calculate and interpret the surprise

When actual and forecast are both sourced numeric values, use `atlas_economic_surprise` for deterministic actual-minus-forecast arithmetic. Preserve units and release provenance.

Interpret the sign according to the indicator:
- A higher CPI reading can increase inflation concern, but the market implication depends on expectations, components and policy context.
- Stronger employment may support growth but can also change the expected rate path.
- A weaker growth reading may support expectations of easing while also raising risk concerns.
- A central-bank hold can still be hawkish or dovish depending on statement, projections, votes and guidance.

Never translate ABOVE/BELOW into a generic bullish/bearish asset direction. Missing actual or forecast means the surprise is unavailable, not zero.

### 4. Interpret policy and transmission

For US macro/Fed research, assess more than the headline decision:
- What was expected before the release?
- Did the statement or guidance change the expected path of rates?
- What do projections, voting differences, press-conference language and policy rationale add?
- Are headline and core inflation, monthly and annual readings, or different labour indicators sending conflicting messages?
- Is the market reacting to the data itself or to its implications for future policy?

For gold and USD-related instruments, consider:
- USD strength/weakness.
- Nominal and real-yield expectations when reliable data exists.
- Inflation expectations.
- Rate-path repricing.
- Risk sentiment and liquidity conditions.

A hawkish repricing may support USD/yields and weigh on gold, all else equal; a dovish repricing may pressure USD/yields and support gold, all else equal. These are conditional transmission channels, not automatic rules. A fully expected decision, contradictory guidance or a different cross-market response can produce a muted or opposite move.

### 5. Compare with observed market behaviour

Only describe an observed response when timestamped price/cross-market data is available in the current turn or valid conversation context. Distinguish:
- Expected policy/economic channel.
- Actual observed USD, yields, gold or other market response.
- Interpretation of whether price confirms, contradicts or has not yet tested the thesis.

If USD or yield data is unavailable, say so. Do not substitute intuition for measured response or claim the original Forex Jarvis reaction engine was run.

### 6. Develop conditional scenarios

Explain:
- The most plausible macro interpretation.
- What would strengthen it (for example, follow-through in related data or markets).
- What would weaken it (for example, revisions, conflicting components, or a market response in the opposite direction).
- The next relevant event or policy communication.

Use qualitative confidence based on evidence quality. Do not invent numerical probabilities or expected percentage moves.

## Historical research boundary

Forex Jarvis contains a separate reaction engine and store that measured event-related price changes across 1m, 5m, 15m, 30m, 60m, 240m and 1d windows, plus descriptive excursion/range/volatility metrics and aggregation. This is existing source code, not a requirement to reproduce it in OpenClaw.

Do not imply those historical measurements are available in this branch. Do not invent event samples, MFE/MAE, historical reaction averages or predictive accuracy. If the user later requests a historical event study, treat it as a separate, explicitly sourced research task with sample size and data-quality limitations.

## Response format

For a full macro report:
1. **Event:** name, region, release time/timezone and source.
2. **Expectations versus actual:** actual, forecast, previous and revisions with units; mark unavailable fields explicitly.
3. **What changed:** interpret the surprise, components and policy implications.
4. **Instrument channels:** explain relevance to the requested market.
5. **Observed reaction:** include only verified, timestamped market evidence.
6. **Scenarios and next catalysts:** what strengthens or weakens the current read.

Answer simple follow-ups directly and reuse valid event evidence from the current conversation. Refresh only when requested or when the information is stale or materially incomplete.

## Safety boundary

Macro research is not trade authorization. Do not access account balances or positions for ordinary research, and do not place, modify or cancel orders. Any future execution remains subject to the separate explicit approval boundary and Live Mode gate.
