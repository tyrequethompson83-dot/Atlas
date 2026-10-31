---
name: atlas-trade-scenario-analysis
description: Use to combine structure, liquidity, price delivery and macro evidence into conditional bullish, bearish or neutral market scenarios.
---

# ATLAS Trade Scenario Analysis

## Purpose and source

This skill consolidates the scenario-building and trade-planning reasoning from:
- `ATLAS_Complete_Market_Reading_Learning_Guide.pdf`
- `ATLAS_Market_Reading_Notes.pdf`
- The ATLAS market-reading specification and existing OpenClaw operating boundaries.

The XAU Cartel material teaches a staged analytical process rather than entering merely because price touches a line. Its examples are educational transcript material, not independently validated performance.

## 1. Build the context before a scenario

Establish:
- Instrument, source, timestamp, freshness and requested timeframe.
- Relevant news and macro catalysts, including event time and whether the event is confirmed.
- Higher-timeframe trend, range, meaningful swing points and major decision boundaries.
- Likely liquidity pools above/below current price.
- Current price delivery: sweep or breakout evidence, structure response, displacement and any relevant OB/FVG candidates.
- Missing evidence and timeframe conflicts.

Use specialist skills when available:
- `atlas-market-structure`
- `atlas-liquidity`
- `atlas-smart-money-concepts`
- `atlas-news-impact`
- `atlas-macro-research`

Do not duplicate or override their source evidence. Bring their conclusions together and identify disagreements.

## 2. Construct conditional scenarios

Consider three possible outcomes when useful:

### Bullish scenario
State:
- What evidence supports upside.
- Which level/condition must hold or be reclaimed.
- What structure confirmation or displacement would strengthen the case.
- The next meaningful opposing liquidity/structural objective.
- What price action would invalidate the bullish interpretation.

### Bearish scenario
State:
- What evidence supports downside.
- Which level/condition must hold or be rejected.
- What structure confirmation or displacement would strengthen the case.
- The next meaningful opposing liquidity/structural objective.
- What price action would invalidate the bearish interpretation.

### Neutral/range scenario
Use when price remains between meaningful boundaries, timeframes conflict, catalysts are unresolved or evidence does not support a directional conclusion. State the range boundaries and what would resolve the balance if those levels are available.

Do not manufacture a bullish and bearish case of equal strength. Weight scenarios according to the quality and relevance of the actual evidence.

## 3. Use the source-taught sequence without forcing it

For a liquidity-based scenario, a common chain is:

1. Define the higher-timeframe trend or range.
2. Mark a meaningful liquidity pool before price reaches it.
3. Observe the interaction: sweep hypothesis or breakout with follow-through.
4. Wait for a meaningful structure response (BOS/CHoCH), not a minor internal fluctuation.
5. Assess displacement.
6. Identify a candidate OB/FVG retracement area if present; record freshness and mitigation.
7. Use the next opposing liquidity/structural area as a conditional objective.
8. Define the price/structure condition that invalidates the thesis.

Not every valid market read follows this sequence. If evidence is absent, state that rather than manufacturing a setup.

## 4. Require clear confirmation and invalidation

For each material scenario, include:
- **Evidence now:** verified observations supporting the interpretation.
- **Next confirmation:** the next observable price/event condition that would strengthen it.
- **Invalidation:** the structural or price condition that would show the thesis is wrong.
- **Objective:** the next relevant liquidity/structure area if the scenario develops.
- **Unknowns:** source, timeframe or market evidence still missing.

A scenario is a conditional explanation, not a prediction that must happen. A wick, one headline, a single FVG, or an OB touch is not sufficient by itself.

## 5. Keep macro and technical evidence connected

For gold, a macro catalyst may change USD/yield expectations or risk sentiment, while technical structure shows where price is positioned and how it reacts. Reconcile them:
- If macro and technical evidence agree, explain the independent channels that align.
- If they conflict, state the conflict and identify what market response would resolve it.
- If the actual market response is not available, do not claim price confirmed the macro story.

Do not infer that a central-bank rate cut is automatically bullish for gold or that geopolitical risk must lift it. Context and observed response matter.

## 6. Communication and confidence

Use plain-language evidence confidence:
- **Strongly supported:** multiple relevant, reasonably independent observations align.
- **Moderately supported:** the interpretation fits, but confirmation or important data remains missing.
- **Tentative:** an early or isolated clue with meaningful alternatives.
- **Balanced/no clear edge:** mixed evidence or range conditions.

Confidence describes evidence quality, not the probability of a winning trade. Do not invent numerical probabilities, fixed percentage impacts or expected price moves.

## Output format

For a full scenario report:
1. **Context:** instrument, source/time and higher-timeframe state.
2. **Most plausible scenario:** evidence, confirmation, invalidation and objective.
3. **Alternative scenario:** what could happen instead and what would confirm it.
4. **Neutral case:** include when range/balance remains credible.
5. **What matters next:** the specific price/event evidence that changes the view.

For a simple question, give a direct answer without forcing a three-scenario report.

## Execution boundary

Only discuss an entry, stop or target plan when requested or directly relevant. Keep it conditional and use the separate `atlas-risk-management` skill for risk and execution checks. No scenario, setup or analysis request authorises an order. Live orders require explicit approval for that specific action; Live Mode remains separately gated.
