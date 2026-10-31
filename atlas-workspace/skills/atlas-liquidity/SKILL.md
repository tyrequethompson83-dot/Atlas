---
name: atlas-liquidity
description: Use when mapping likely buy-side or sell-side liquidity, equal highs/lows, stop clusters, liquidity sweeps, or distinguishing a sweep from a breakout.
---

# ATLAS Liquidity Analysis

## Purpose and source

This skill recovers the Liquidity lesson from the supplied XAU Cartel video material, consolidated in:
- `ATLAS_Complete_Market_Reading_Learning_Guide.pdf`
- `ATLAS_Market_Reading_Notes.pdf`

The material teaches liquidity as a way to reason about where orders may cluster. It does not provide direct visibility into hidden orders or prove the identity or intention of market participants.

## 1. Map likely liquidity pools before price arrives

Look for clear, widely visible areas where stop and breakout orders may cluster:
- Equal highs and equal lows.
- Recent prominent swing highs and lows.
- Prior-day and prior-week highs/lows.
- Range highs and lows.
- Asian-session range extremes and London/New York session highs/lows when reliable session data is available.
- Obvious trendline levels when they are genuinely visible and widely watched.

Classify pools by likely side:
- **Buy-side liquidity (BSL):** likely orders above obvious highs, equal highs and range highs.
- **Sell-side liquidity (SSL):** likely orders below obvious lows, equal lows and range lows.

Explain why a level is notable. Do not mark every minor pivot as a liquidity pool.

## 2. Distinguish a possible sweep from a breakout

A **possible sweep** is supported when price trades through an obvious level and then closes back on the original side. A **breakout** is better supported when price closes beyond the level with meaningful displacement and follow-through.

Use:
- Candle close relative to the level.
- Body/displacement and subsequent candles.
- Timeframe significance of the level.
- Higher-timeframe context.
- Whether price holds beyond the level or quickly reclaims it.

A wick alone is not enough. A sweep hypothesis can fail; a breakout can fail. Keep the competing interpretation until follow-through resolves it.

## 3. Follow the liquidity sequence

A common sequence in the source lessons is:

1. Mark an obvious liquidity pool before price reaches it.
2. Wait for price to interact with or run through the level; do not assume it will sweep.
3. Observe the close and the immediate reaction.
4. Look for a meaningful opposite-direction structure break on a relevant lower timeframe.
5. Assess displacement and whether the move leaves an OB/FVG candidate.
6. Study a retest rather than assuming the zone will hold.
7. Use the next opposing liquidity pool as a conditional objective.
8. Define invalidation beyond the sweep extreme or structural point that disproves the idea.

This is a narrative framework, not a mechanical requirement for every market condition.

## 4. Interpret the institutional-liquidity model carefully

The source material uses an institutional-liquidity framework: larger participants may seek counterparties around obvious clusters of orders, and triggered stops can add market orders to the flow. This is a useful working explanation for some price paths.

Use the model actively when the observed sequence fits it. Do not claim that the chart proves a specific bank, fund or participant placed orders at a particular level. Update the explanation when price action contradicts it.

## 5. Combine with the other specialist skills

- Use `atlas-market-structure` for the larger swing sequence and meaningful BOS/CHoCH.
- Use `atlas-smart-money-concepts` for displacement and possible OB/FVG retracement areas.
- Use `atlas-news-impact` or `atlas-macro-research` when a catalyst may explain the liquidity run or volatility.
- Use `atlas-trade-scenario-analysis` to express the conditional path and invalidation.

## Output for a liquidity map

For each important pool, state:
- Level/zone and timeframe, only when supported by chart data.
- BSL or SSL.
- Why it is obvious/relevant.
- Whether it has been approached, swept, reclaimed or broken.
- What price behaviour would support sweep versus breakout.
- The next opposing liquidity area, if visible.

Do not invent price levels or claim that a liquidity pool was swept without the required candle evidence. This skill is analytical only and does not authorise trades.
