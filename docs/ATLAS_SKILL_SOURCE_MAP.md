# ATLAS native skill source map

**Branch:** `atlas/v0-foundation`  
**Purpose:** Keep a source-grounded inventory of the separate OpenClaw-native skills ATLAS is intended to use. This is a mapping and implementation record, not a claim that every skill or data integration is already working.

## Architecture

OpenClaw remains the only agent runtime. Each specialist capability is an ordinary workspace skill with its own `SKILL.md` under:

`atlas-workspace/skills/<skill-name>/SKILL.md`

The existing Windows installer copies workspace files recursively, so separately packaged skills in this folder are included by the same workspace installation process. The skill files provide instructions and expertise; they do not install external data sources, add tools, or make a provider live.

- `atlas-market-reading` is the conversational market-reading coordinator.
- Specialist skills hold bounded analytical methods.
- `atlas-evidence` governs source and evidence discipline.
- `atlas-market-stress` is a separate cross-asset stress workflow; it is not the ordinary headline News Impact skill.

## Source-to-skill mapping

| Native skill | Source material | What should be carried across | Status and limits |
|---|---|---|---|
| `atlas-news-impact` | Forex Jarvis: `atlas_auto/news_scanner.py`, `atlas_auto/tools/news.py`, `NEWS_IMPACT_READ_PATH.md`, `tests/test_news_feed_read_path.py`, `atlas_auto/config.py` | Current headline research; source/time verification; category classification; affected-market mapping; event severity and impact-channel reasoning; non-consuming read behaviour. | **Native skill created.** Source was inspected. Original focused read-path tests are documented as 12/12 passing, and the audit records repeated reads returning the same 17 events without changing the watermark. The original RSS scanner is **not** connected to OpenClaw. The skill uses only configured OpenClaw research tools. |
| `atlas-macro-research` | Forex Jarvis: `atlas_auto/tools/research.py`; `atlas_auto/research/biquote_source.py`, `sync.py`, `surprise.py`, `store.py`, `reaction.py`, `aggregation.py`; research test modules. | Scheduled-event research; event/currency relevance; actual, forecast, previous and revised values; units/time/provenance; deterministic surprise arithmetic; interpretation through policy and market context. | **Source recovered; native skill not yet created.** Biquote provider tests mock HTTP, so they do not prove present-day live provider access. The historic reaction database and measured reaction windows are documented source capabilities, but they are not a requirement for the first native skill and will not be hard-coded into News Impact. |
| `atlas-market-structure` | XAU Cartel: Market Structure transcript material in `ATLAS_Complete_Market_Reading_Learning_Guide.pdf` and `ATLAS_Market_Reading_Notes.pdf`. | Meaningful swing sequence; HH/HL and LH/LL; trend versus range; BOS/CHoCH; continuation versus reversal; multi-timeframe reading. | **Reference knowledge recovered; native skill not yet created.** The consolidated guide represents seven supplied video transcripts; it is not independent validation of a trading method. |
| `atlas-liquidity` | XAU Cartel: Liquidity transcript material in the two consolidated learning documents. | BSL/SSL; equal highs/lows; swing, range, prior-day/week and session liquidity; sweep versus breakout; liquidity objective and reaction sequence. | **Reference knowledge recovered; native skill not yet created.** Treat liquidity pools as analytical interpretations; do not claim direct visibility of hidden orders. |
| `atlas-smart-money-concepts` | XAU Cartel: Order Blocks and Fair Value Gaps transcript material in the two consolidated learning documents. | Displacement; candidate OB definition and quality; fresh versus mitigated zones; FVG, CE and IFVG; context, invalidation and confluence. | **Reference knowledge recovered; native skill not yet created.** These are concepts and candidate zones, not guarantees that an OB holds or an FVG fills. |
| `atlas-volume-profile` | No specific XAU Cartel source recovered. | Only after sourcing: POC, VAH, VAL, HVN, LVN and value-area interpretation using genuine volume-at-price/profile data. | **Not sourced; do not implement yet.** The recovered seven-video guide does not teach this method or supply profile data. Ordinary OHLC bars or the current MT5 adapter's volume field cannot be substituted. |
| `atlas-trade-scenario-analysis` | XAU Cartel market-reading notes and learning guide; existing ATLAS market-reading specification. | Join macro, higher-timeframe structure, liquidity, price delivery and retracement areas into conditional scenarios with confirmation, invalidation and opposing liquidity objectives. | **Analytical rules documented; native skill not yet created.** Video case-study levels and claimed outcomes are historical examples and are not validated current signals. |
| `atlas-risk-management` | Risk and execution principles in XAU Cartel notes/guide and existing ATLAS operating/trading-approval boundaries. | Invalidation before entry; realistic targets; independently checked risk/reward; spread, volatility, slippage, session and event risk; explicit approval boundaries. | **Principles documented; separate source review and validation still required.** This is not permission to add automatic order execution or expand trading scope. |

## Forex Jarvis News Impact: recovered facts

The original scanner has two distinct operations:

- `peek()` returns the current classified feed without filtering against or mutating the scanner's seen IDs.
- `scan()` is a consuming new-event scan: it filters already-seen IDs and records new ones in the in-memory seen set.

The Ask-AI read-path defect came from constructing a throwaway scanner and using `scan()`, which caused previously seen headlines to disappear from the answer. The fix reads `peek()` from the orchestrator's existing scanner. Ordinary news reads must never advance the watermark or make the News panel lose events.

The scanner's recovered categories include war, military escalation, sanctions, oil disruption, central bank, inflation, employment, GDP, banking crisis, natural disaster and supply-chain disruption. It used keyword matches to select categories and produce a severity score.

The old `PAIR_IMPACT` table and category weights produce fixed, heuristic percentage estimates. The old `confidence` field was assigned the same value as severity. These are not statistically calibrated forecasts or measured predictive confidence. The first OpenClaw News Impact skill intentionally preserves the research/classification workflow and read-only invariant without porting those percentages as predictions.

The original read-path audit documents:
- 12/12 focused read-path tests passing.
- Repeated Ask-AI reads returning 17 events while the persisted watermark remained unchanged.
- A broader test suite with one documented, pre-existing unrelated failure.

These are historical verification results from the Forex Jarvis repository, not tests run against the OpenClaw skill or current news sources.

## Economic research: keep it separate

Forex Jarvis's research layer is separate from headline scanning. Its source includes a provider adapter, sync layer, persistent research store, actual-minus-forecast calculator, and a measured reaction engine. The Biquote adapter's tests explicitly mock HTTP. They establish parsing/normalisation behaviour under test, not live service availability today.

For the first OpenClaw native capability, prioritise correctly sourced calendar fields and macro interpretation. Do not make the historical reaction database, per-event MT5 measurements, reaction-window aggregation or prediction model a prerequisite. Only claim measured market response when trustworthy timestamped market data is actually available.

## Provenance rules

Keep these statuses separate in code, docs and user-facing output:

1. **Documented knowledge:** appears in a transcript, guide or notes.
2. **Existing implementation:** appears in source code.
3. **Historically verified behaviour:** backed by a specific test or live-check record from that source repository.
4. **Implemented in OpenClaw:** exists as a native skill or registered tool on this branch.
5. **Runtime verified:** has passed checks in an actual OpenClaw Gateway/runtime with the required providers connected.

A skill being present in the repository does not mean its external feed or data provider is connected. A mocked provider test does not establish live availability. A concept in a video or guide does not make it a validated trading method.
