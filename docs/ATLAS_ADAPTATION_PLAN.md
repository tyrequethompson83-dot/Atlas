# ATLAS Adaptation Plan — OpenClaw Foundation

**Status:** Plan only. This document does not implement or modify application behavior.  
**Destination:** `tyrequethompson83-dot/Atlas`  
**Plan branch:** `atlas/adaptation-plan`

## 1. Decision

Use OpenClaw as ATLAS's application and agent-runtime foundation. ATLAS is the product identity, local configuration, workspace instructions, and (later) specialized market capability layered on that foundation.

Do not build a second conversational runtime in Python, and do not port the existing ATLAS chat/tool loop into OpenClaw. Do not remove source files merely because their features are outside the initial product. Prefer supported configuration and plugin boundaries; delete or change core code only when a demonstrated product requirement cannot be met through those boundaries.

## 2. Verified repository and release baseline

- The `Atlas` repository is already a fork of `openclaw/openclaw` and contains the full source tree. Do not rename it, fork again, or repeat repository setup.
- At plan creation, `main` points to `ec698cc702caf9694e6d0df3935b4ac0316b4397`. The root includes the agent runtime, `packages/agent-core`, workspace and session code, plugin SDK, bundled extensions, UI, tests, license, and third-party notices.
- The package currently identifies as OpenClaw `2026.10.7`. However, the fork's `main` tracks moving upstream commits; the presence of that package version alone does not prove it is the exact release snapshot.
- The adaptation source is the actual OpenClaw code already present on `tyrequethompson83-dot/Atlas`'s current `main` branch. The inspected fork head is `ec698cc702caf9694e6d0df3935b4ac0316b4397`; upstream `main` was only four commits ahead at the time of the repository check. Start the implementation branch from the fork's inspected `main` head and preserve that head as the reference baseline. Do not rename the repository, fork again, or replace the fork's source with a manually assembled snapshot.
- The package identifies as `2026.10.7`, and the official `v2026.10.7` release tag exists, but this fork's default branch contains later upstream-main commits. Do **not** switch back to the older release tag automatically: the decision was to build on the source fork the user just created. If a specific regression or release-stability concern later justifies a release pin, compare the relevant commits and document that reason first. Do not reset or force-update `main`.
- The repo includes the MIT `LICENSE` and `THIRD_PARTY_NOTICES.md`. Preserve both and retain relevant third-party notices in future distributions.

## 3. What OpenClaw already owns

| Capability | Existing owner to reuse | ATLAS decision |
| --- | --- | --- |
| Agent loop, provider invocation and tool iteration | `src/agents/embedded-agent-runner/`, `packages/agent-core/`, `src/agents/runtime/` | Use as-is for v0; no second loop |
| Conversation/session handling and persisted state | `src/agents/sessions/`, Gateway/session stores | Use native session lifecycle and persistence |
| Streaming | Existing agent/provider transport and Control UI | Use native streaming; prove it end to end |
| Agent context files and instructions | Workspace bootstrap and context assembly | Put ATLAS identity and principles in supported workspace files |
| Skills discovery and precedence | Built-in skill loader | Use native workspace/project/managed/bundled skill roots |
| Community skills store | Native ClawHub integration | Keep available as an optional compatible source; review skills before installing |
| Model providers and custom compatible endpoints | Bundled provider plugins and `models.providers` configuration | Configure first; add no provider code unless a verified protocol gap requires it |
| Local chat interface | Existing Gateway Control UI | Start with it; postpone custom UI work until baseline acceptance |
| Optional channels, providers, tools and integrations | Bundled extensions and config/manifest controls | Disable unneeded capabilities by configuration; do not mass-delete source |

OpenClaw's plugin guidance favors the smallest existing public extension point and forbids plugins from depending directly on private `src/**` internals. Any later ATLAS market capability should follow that boundary.

## 4. Windows, build and licensing constraints

The checked-in documentation describes Windows support, including the native Windows Hub for Windows 10 20H2+ and Windows 11, plus PowerShell CLI and WSL2 paths. This confirms a supported Windows route; it does **not** prove the source checkout has been built on this machine.

The current source-build documentation requires Node.js `>=24.22.1 <25` or `>=26.12.1` (Node 26 recommended) and pnpm. The local machine's installed Node version, pnpm version, available disk space, and successful source build remain to be verified in the actual Windows checkout. The existing Java/JDK installation is not a substitute for the required Node runtime.

Prefer one source install and targeted tests to repeated full downloads. Use the native PowerShell developer route first; switch to WSL2 only if a concrete source-build or runtime blocker requires it. Keep secrets and local runtime state out of the repository.

References: [Windows](https://github.com/tyrequethompson83-dot/Atlas/blob/main/docs/platforms/windows.md), [install requirements](https://github.com/tyrequethompson83-dot/Atlas/blob/main/docs/install/index.md), [Node compatibility](https://github.com/tyrequethompson83-dot/Atlas/blob/main/docs/install/node-compatibility.md).

## 5. Smallest useful ATLAS v0

Keep only these product capabilities enabled and verified:

1. One local OpenClaw Gateway and one primary agent, accessed through the existing local Control UI.
2. A BYOK model-provider connection with clear setup and error handling.
3. Native streaming responses and conversations that persist across a Gateway restart.
4. OpenClaw's existing skills loader and compatible skills-store workflow.
5. ATLAS's persona, identity, operating principles and a small set of relevant user preferences, expressed through workspace files rather than changes to OpenClaw core.

Use the standard workspace surfaces documented by OpenClaw:
- `SOUL.md`: persona, voice, conversational stance and boundaries.
- `IDENTITY.md`: name and concise identity.
- `AGENTS.md`: operating rules and priorities.
- `USER.md`: only stable preferences/context useful to the agent; do not copy unrelated private or historic data wholesale.

Port content selectively from the existing [ATLAS soul](https://github.com/tyrequethompson83-dot/forex_jarvis/blob/main/soul.md), [identity](https://github.com/tyrequethompson83-dot/forex_jarvis/blob/main/identity.md), and [operating principles](https://github.com/tyrequethompson83-dot/forex_jarvis/blob/main/principles.md). Retain ATLAS's she/her presentation, candid evidence-led voice, continuity, humility about uncertainty, and separation of observed fact from interpretation. Do not bring along the old Python app runtime or its database as a dependency.

## 6. Initial provider strategy

Investigate the existing xKiro BYOK account as the first candidate, using its known base URL `https://api.xkiro.com/v1`. OpenClaw documents `models.providers` for custom OpenAI/Anthropic-compatible endpoints.

Do not assume protocol compatibility from the URL alone. Verify with the exact model and account that ordinary completion, incremental streaming, and required tool-calling behavior work through the supported OpenClaw provider interface. Respect the selected model's context limit. If xKiro cannot satisfy the native interface, document the actual incompatibility before choosing a supported alternate route; do not immediately create a new model transport.

- Store the API key only in the local credential/configuration mechanism or an untracked local environment file.
- Never commit API keys, tokens, private user data, or the contents of secret settings.
- Verify errors and diagnostics do not echo credentials.
- Keep the Qwen realtime/Live Mode work outside v0. Live Mode must not be started as part of this adaptation plan.

Reference: [custom provider configuration](https://github.com/tyrequethompson83-dot/Atlas/blob/main/docs/concepts/model-providers/custom-providers.md) and the existing [xKiro integration tests](https://github.com/tyrequethompson83-dot/forex_jarvis/blob/main/tests/test_xkiro_integration.py).

## 7. Explicitly out of scope for v0

- MetaTrader 5, chart and market-data tools, trading, order execution, strategies, backtesting and market-specific research.
- Live Mode, realtime voice, holographic presence, and custom avatar/UI work.
- Extra messaging channels, remote Gateway exposure, multi-agent configurations, background autonomy and unattended tasks.
- New memory engines, new conversation databases, a second skill system, or a duplicate provider framework.
- Broad deletion/refactoring of bundled plugins, providers, channels, tests, generated output or core runtime code.

Keep optional integrations disabled through supported configuration and manifests wherever possible. If the default install activates capabilities beyond this minimal scope, identify the owning config/plugin and disable them narrowly. Record what was disabled and how to re-enable it.

## 8. Execution sequence — no application code until the baseline is accepted

### Stage A — Reproducible source baseline
1. Create a dedicated implementation branch from the official `v2026.10.7` tag target; keep `main` unchanged.
2. On the Windows checkout, inspect `git status -sb`, remotes and branch head before changing anything.
3. Verify Node and pnpm requirements, install the checked-in workspace dependencies once, and follow the repository's current source-build instructions.
4. Start the uncustomized Gateway and Control UI, then record concrete startup/build errors and the exact commands used.

**Gate A:** source installs and starts on the user's Windows environment without ATLAS customization. No claim of success based only on remote source inspection.

### Stage B — Minimal configuration
1. Configure a single agent and local Control UI.
2. Configure the first BYOK provider and test a real response, then streaming and tool use.
3. Use native conversation/session persistence.
4. Port ATLAS workspace files and add one harmless test skill in the standard skill format.
5. Disable unrelated integrations using supported configuration; do not delete their code.

**Gate B:** a clean local ATLAS conversation works and survives restart, with secrets kept private and no trading/MT5 capabilities configured.

### Stage C — Verify and document
Run targeted checks through the actual Windows product flow, not only mocks:
- Gateway starts, status/health is understandable, and the local UI connects.
- The selected model returns a normal answer and visibly streamed answer.
- A conversation survives Gateway restart and remains in the expected local state directory.
- ATLAS's identity and operating rules are present in a new session.
- A local test skill is discovered and can guide an appropriate request.
- Missing/invalid provider credentials produce an actionable error and never leak the key.
- Unneeded messaging/market/trading integrations are not active.
- `openclaw doctor` and the targeted tests applicable to the changes report their actual results.

Only after these pass should we propose the next specialized capability.

## 9. Update and change discipline

- Keep the fork's `main` and all upstream source intact during planning and initial proof.
- Use dedicated, small ATLAS branches/commits. Keep a clear record of the upstream baseline and ATLAS-only changes.
- Prefer configuration and workspace files, then a supported plugin, then a narrowly justified SDK seam. Touch OpenClaw core only when the product requirement cannot be expressed through existing surfaces.
- Every changed behavior needs an end-to-end acceptance check that could fail on the unmodified baseline.
- Do not claim the project runs locally until the Windows build and user-facing flow have actually been exercised.

## 10. Acceptance definition

ATLAS v0 is complete when the user can launch it locally on Windows, configure their own provider credential without committing it, have natural conversations with incremental streaming, restart without losing the conversation, and use a supported custom skill, while ATLAS's identity is present and unneeded integrations remain disabled.

This is a reliable OpenClaw-based conversational foundation—not yet a market-reading agent. MT5, news analysis and trading capabilities are later, separately scoped work.