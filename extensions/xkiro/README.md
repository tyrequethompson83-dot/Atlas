# xKiro

This extension registers xKiro as a native OpenClaw model provider and exposes
Qwen3.8 Omni Flash in the existing Models catalog.

## Configure the API key

1. Open Settings → Models → Providers.
2. Select xKiro and choose **Set API Key**.
3. Paste your xKiro API key and save.

OpenClaw stores the key in its native auth-profile credential store. No
`XKIRO_API_KEY` environment variable or plaintext key in the model configuration
is required. The provider uses `https://api.xkiro.com/v1` and the
`openai-completions` API.

The extension does not create a second credential store or agent runtime.
