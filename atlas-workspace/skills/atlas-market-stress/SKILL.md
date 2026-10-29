---
name: atlas-market-stress
description: Use when the user asks what markets could crash, whether stress is spreading across asset classes, or requests a cross-market risk scan.
---

# ATLAS cross-market stress scan

Use the existing OpenClaw agent turn and its configured research/search/fetch tools. This is an evidence-gathering and scenario-analysis skill, not a second runtime, price feed, trading strategy, or crash predictor.

## Mission

Answer: "What is under pressure, what could transmit the stress to other markets, what evidence confirms or weakens a systemic-risk thesis, and what should be watched next?"

Always distinguish:
- **A correction** in one asset or sector.
- **A cross-asset risk-off move** confirmed by multiple independent markets.
- **Systemic stress** where credit, funding, liquidity, or core market functioning is impaired.
- **A plausible tail risk** from an event that has not yet caused broad market damage.

Do not label a crash as imminent just because headlines sound alarming. Do not provide a numerical crash probability unless a calibrated, identified model and data are actually available.

## Evidence-gathering procedure

1. **Anchor time.** State the scan's date, time and timezone. Prioritize the latest 24 hours for price/news changes and the latest 2–4 weeks for context. Label older official risk reports as background, not today's market movement.
2. **Identify the catalyst set.** Collect the most material confirmed developments: central-bank decisions and guidance; inflation, employment and growth data; sovereign debt/auction and fiscal concerns; bank or private-credit stress; corporate earnings/concentration; geopolitics and energy supply; cyber or market-infrastructure incidents. Separate confirmed facts from proposals, anonymous reports, opinions and speculation.
3. **Check at least these asset groups where reliable current data exists:**
   - **Equities:** major US, European and Asian indexes; index leadership/concentration; market breadth; volatility measures.
   - **Rates and sovereign bonds:** short and long yields, curve moves, auction/funding concerns and abrupt yield volatility.
   - **Credit and funding:** high-yield/investment-grade spreads, distressed/default news, private-credit redemptions, repo or dollar-funding stress. If current spread/funding data is unavailable, say so.
   - **FX:** broad USD, JPY/CHF safe-haven behaviour, major pairs and emerging-market currencies where relevant. Do not infer risk-off from one currency move alone.
   - **Commodities:** oil/gas supply risk, gold and silver, and industrial metals where they reveal demand or supply stress.
   - **Crypto:** BTC/ETH and liquidation/leverage reports if credible data is accessible. Treat crypto as a separate high-volatility market, not a standalone systemic-stress gauge.
4. **Triangulate rather than cherry-pick.** Look for simultaneous confirmation across markets. A tech selloff with positive equity breadth, falling volatility and stable credit is materially different from an equity decline accompanied by volatility spikes, widening credit spreads, disorderly sovereign yields and funding/liquidity problems. These are diagnostic patterns, not fixed laws.
5. **Use primary sources where practical.** Prefer central banks, national statistics agencies, treasury/debt offices, official exchange data and published financial-stability reports. Use reputable news wires for breaking developments. Cite links for material claims, show publication/event dates, and note when a story may have changed.
6. **Preserve source limitations.** If configured OpenClaw search/fetch tools are unavailable, say that current verification could not be completed. Never claim live quotes, credit spreads, VIX, flow data, or calendar events were checked when they were not. Use MT5 tools only for the explicit symbols/timeframes they actually return; MT5 OHLC is not a substitute for credit/funding data.
7. **Reuse context intelligently.** Reuse valid evidence already gathered in the current conversation. Refresh when the user asks, a material catalyst changes, or timestamps make the evidence stale; do not repeat searches just to make the answer look busy.

## Required response format

Start with a one-paragraph **overall assessment** using one of: **localized stress**, **cross-asset warning**, or **systemic stress evidence**. This is a qualitative evidence label, not a prediction.

Then provide a compact table:

| Market/risk channel | Latest verified evidence | Why it matters | What would confirm escalation | What weakens the concern |
|---|---|---|---|---|

Group the material catalysts by market and include equities, rates, credit/funding, FX, commodities and crypto when current evidence exists. It is acceptable—and preferable—to mark a field **not verified from available sources** rather than fill it with a guess.

Give three scenarios:
- **Base case:** what current evidence supports, plus the next observable conditions.
- **Escalation case:** specific events/market behaviour that would signal contagion or a sharp deterioration.
- **Relief case:** evidence that would reduce stress (for example, easing volatility, stabilizing yields/credit, broader equity participation, or credible de-escalation).

For each scenario state observable triggers and invalidation evidence. Avoid invented target prices or time-to-crash claims.

Finish with **next things to watch**, ordered by how much they could change the assessment. Distinguish "important catalyst" from "proof of stress." Use a clear timestamp and cite each key claim.

## Interpretation guardrails

- Falling prices are not sufficient to establish systemic risk. Seek independent confirmation from credit, volatility, rates, funding or liquidity indicators.
- Higher yields can indicate stronger growth or inflation risk; falling yields can indicate safe-haven demand or expected easing. Explain context before interpreting.
- Gold can fall during inflation/rate repricing or liquidity-driven selling; do not assume it must rise during every crisis.
- Oil may rise on supply disruption even while risk assets fall; relief headlines may not remove physical supply risk.
- An economic release beating/missing consensus is a data surprise, not automatically a bullish/bearish signal. When actual and forecast values are verified, use `atlas_economic_surprise` for deterministic arithmetic and preserve units/source/timestamp.
- Distinguish an announced event, a credible report, an analyst opinion, and an unconfirmed social-media claim.
- Never treat a scenario as certainty or a market opinion as permission to trade. Do not access accounts/positions or place/modify orders for a risk scan.
