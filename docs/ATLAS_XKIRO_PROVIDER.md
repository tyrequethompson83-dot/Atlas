# ATLAS BYOK provider: xKiro

This is an opt-in provider profile for the ordinary OpenClaw chat/runtime path. It is not automatically loaded just because the file is present.

## What the profile targets

- Provider ID: **xkiro**
- OpenAI-compatible base URL: **https://api.xkiro.com/v1**
- API dialect: **openai-completions**
- Model ID in xKiro: **qwen/qwen3.8-omni-flash:free**
- Model reference in OpenClaw: **xkiro/qwen/qwen3.8-omni-flash:free**
- Model listing currently reports a 1,000,000-token context, 65,536-token output limit, vision and tool-use support, and free token pricing subject to the service's allowance.

References: [xKiro's OpenClaw guide](https://docs.xkiro.com/guides/tools/openclaw/), [xKiro model page](https://xkiro.com/models/qwen/qwen3.8-omni-flash%3Afree), and [OpenClaw custom-provider documentation](https://docs.openclaw.ai/concepts/model-providers/custom-providers).

## Apply it deliberately

The matching example is **config/atlas-xkiro.example.json5**. Merge its provider block and model selection into the local OpenClaw config at **~/.openclaw/openclaw.json** using the Control UI's Config tab or the OpenClaw config CLI. Do not replace the entire existing config: keep other settings and use merge semantics.

The Gateway process must be able to resolve **XKIRO_API_KEY**. Keep the actual key only in local environment/secret configuration. Never paste it into this repository, this example file, or a public issue.

## Verification required before relying on it

The provider's shape and model capabilities are documented by xKiro, but this repo has not yet made authenticated requests with your account. After applying it, verify in order:

1. A normal text prompt returns a real model answer.
2. Streaming delivers incremental output.
3. A harmless tool call is selected and completed using a tool enabled in this OpenClaw installation.
4. A new turn preserves conversation context after restarting the Gateway.
5. An invalid-key test yields an understandable error without exposing the key in logs or the user-facing response.

This profile does not configure realtime audio, Live Mode, a voice/avatar UI, market-data access, MT5, or trading. It does not clear the prerequisite for the separate CPI-to-gold research gate before Live Mode.
