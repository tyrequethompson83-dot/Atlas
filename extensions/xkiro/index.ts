import { defineSingleProviderPluginEntry } from "openclaw/plugin-sdk/provider-entry";
import { applyXkiroConfig, XKIRO_DEFAULT_MODEL_REF } from "./onboard.js";
import manifest from "./openclaw.plugin.json" with { type: "json" };

export default defineSingleProviderPluginEntry({
  id: "xkiro",
  name: "xKiro Provider",
  description: "OpenAI-compatible xKiro model provider",
  manifest,
  provider: {
    label: "xKiro",
    docsPath: "/providers/xkiro",
    manifestAuth: {
      defaultModel: XKIRO_DEFAULT_MODEL_REF,
      applyConfig: applyXkiroConfig,
    },
  },
});
