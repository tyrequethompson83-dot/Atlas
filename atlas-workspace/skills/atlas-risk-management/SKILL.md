---
name: atlas-risk-management
description: Use when the user asks for a trade plan, invalidation, position risk, reward-to-risk, spread/slippage considerations, or risk controls.
---

# ATLAS Risk Management

## Purpose and source

This skill consolidates risk and execution principles in:
- `ATLAS_Complete_Market_Reading_Learning_Guide.pdf`
- `ATLAS_Market_Reading_Notes.pdf`
- Existing ATLAS operating, privacy and trading-approval boundaries.

The source material describes risk planning principles; it does not establish a fully validated risk engine or authorise autonomous execution. Any concrete calculation must use actual, current inputs and the correct instrument contract.

## 1. Separate analysis from execution

A market idea is not an order instruction. Do not assume permission to trade from:
- A market-analysis request.
- A proposed setup or trade scenario.
- A prior approval for a different order.
- A news event or high-severity label.

No live order may be placed without explicit approval for that specific action. Do not silently submit, modify, close or cancel an order. Live Mode remains disabled until the separate CPI-to-gold research prerequisite is completed/reported and the user explicitly directs activation.

## 2. Define the thesis and invalidation first

Before discussing entry or sizing:
- State the structural/price thesis.
- Define the exact condition that makes the thesis wrong.
- Place the invalidation beyond the relevant structural point/zone, not at an arbitrary distance.
- Consider whether the stop/invalidation is beyond a sweep extreme, OB boundary, swing point or other evidence-based level.
- Reject a plan when the invalidation cannot be identified from available evidence.

A stop level is a planning assumption, not a guarantee of execution at that exact price.

## 3. Select realistic objectives

Prefer relevant opposing liquidity or structural levels over targets chosen only to produce an attractive risk/reward ratio.

Check:
- Entry-to-invalidation distance.
- Entry-to-target distance.
- Whether the target is structurally meaningful.
- Whether intervening liquidity or nearby levels make the target unrealistic.
- Whether the proposed plan remains coherent if the market is ranging or volatility changes.

Calculate reward-to-risk from the actual proposed entry, invalidation and target. State assumptions and units. Do not invent lot value, tick value, contract size, account balance or monetary risk.

## 4. Account for trading conditions

Before discussing execution, assess when reliable data is available:
- Current bid/ask and spread.
- Quote age and market-session status.
- Volatility and recent range.
- Slippage and gaps.
- Upcoming or just-released high-impact events.
- Liquidity conditions and time of day.
- Whether the latest candle is complete or still forming.

Major releases can widen spreads, thin liquidity and increase slippage. Stops may execute at worse prices than the requested level. Do not treat a fixed waiting period before/after every release as a universal rule; assess the actual event and current conditions.

If a required input is missing, label it missing. Do not substitute a guessed spread, price, account value or risk amount.

## 5. Size only from verified inputs

A position-size calculation requires, at minimum:
- A user-specified risk budget or explicitly authorised risk rule.
- Entry and stop/invalidation prices.
- Correct symbol contract/tick specifications and account currency conversion where applicable.
- Current, reliable price/contract data.

Do not estimate lot size from generic pip assumptions when the broker symbol is a CFD or metal with different contract specifications. If contract/tick data or risk budget is unavailable, explain that sizing cannot be calculated reliably.

Never access balances or positions for ordinary market research. Account-related information requires explicit account-related intent and the appropriate permitted integration.

## 6. Present risk plainly

A useful conditional plan should state:
- Why the idea is being considered.
- Entry area only if supported by the evidence.
- Invalidation/stop level and the reason it invalidates the thesis.
- Target(s) grounded in structure or liquidity.
- Reward-to-risk calculation and assumptions.
- Spread, volatility, slippage, session and event risks.
- Missing information and what would make the plan unsuitable.

Do not call a setup "safe", guarantee a stop or imply that a high reward-to-risk ratio makes a weak thesis valid.

## 7. ATLAS safety boundaries

The market plugin currently exposes read-only market quote/candle/structure tools and has no order operation. Do not imply an execution tool exists or that risk calculations have been implemented as enforced broker-side limits.

When execution integration is added in the future, it must preserve explicit user approval, the minimum-lot and other broker constraints, account privacy, and fail-closed behaviour. This skill itself cannot submit or approve orders.
