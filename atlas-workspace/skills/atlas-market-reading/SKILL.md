---
name: atlas-market-reading
description: Use for market questions requiring MT5 price evidence, chart structure, news impact, or economic-event research.
---

# ATLAS market reading

Use OpenClaw's normal conversation and tool loop. Do not create a second agent loop or turn every exchange into a fixed workflow.

## Price and chart evidence

1. Establish the exact symbol and timeframe. Use trusted active-chart context only when the current runtime explicitly supplies it. The first ATLAS MT5 plugin does not receive Forex Jarvis's frontend chart context yet; if symbol/timeframe are not clear, ask or use explicit values rather than guessing.
2. Call atlas_market_quote for a quote. Preserve bid and ask separately, along with the broker timestamp, age, source, and retrieval time. An unavailable or old quote is not a live quote.
3. Call atlas_market_candles for bounded OHLC evidence, or atlas_market_structure when swing/range context will materially help. Do not make redundant calls when the same valid bars are already available in the turn.
4. Treat the structure result as descriptive calculations from the returned bars, not an indicator overlay, signal, or guaranteed forecast. Fractal swings require two bars on each side; the newest two bars cannot yet confirm a new swing.
5. State what the data supports, what is inferred, and what remains uncertain. Mention session/closed-market context when relevant. Never fabricate missing values.

## News Impact and economic research

- Use configured OpenClaw web-search/fetch tools when current headlines, official releases, or economic-calendar facts are needed. If those tools are not available, state the missing source rather than claiming a fresh search.
- Prefer official releases and primary sources for event times, actual/forecast/previous readings, central-bank statements, and macro data. Keep event dates, timezone, assets, and instrument scope explicit.
- Distinguish reported data from interpretation. For gold and USD-related instruments, assess competing rate, dollar, and risk-sentiment channels rather than assuming one headline dictates direction.
- For News Impact follow-ups, reuse the displayed/retrieved event set if it remains current; refresh only when requested or when the evidence is stale or incomplete. Group material catalysts by asset/market and give a concise impact table and practical takeaways when that is the user's request.
- The Forex Jarvis RSS scanner, its economic-calendar database, and numeric impact model are not connected by this skill or by the first MT5 plugin. Never imply they are.

- When an official release or reliable calendar/news source provides numeric actual and consensus forecast values, use `atlas_economic_surprise` to calculate actual-minus-forecast consistently. Pass the source URL and release timestamp when available, and preserve the provider's units. Do not convert ABOVE/BELOW into bullish/bearish direction: the tool reports the data surprise only, while market direction requires event-specific interpretation and observed price response. If actual or forecast is missing, pass null rather than substituting zero.
- This tool is a deterministic calculator, not a calendar feed. It does not fetch events, maintain a calendar database, classify headlines, or refresh any scanner state. Use configured OpenClaw research tools for source retrieval and say when a source is unavailable.

## Safety and privacy

This market plugin is read-only: it does not read account balances or positions and has no trade execution tools. Analysis can discuss scenarios, evidence, invalidation, and risks, but it must not place orders or treat a market opinion as trade authorization. Never expose credentials or unnecessary account data.
