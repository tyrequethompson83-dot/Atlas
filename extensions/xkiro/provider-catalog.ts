import { buildManifestModelProviderConfig } from "openclaw/plugin-sdk/provider-catalog-shared";
import type { ModelProviderConfig } from "openclaw/plugin-sdk/provider-model-shared";
import manifest from "./openclaw.plugin.json" with { type: "json" };

export const XKIRO_BASE_URL = manifest.modelCatalog.providers.xkiro.baseUrl;

export function buildXkiroProvider(): ModelProviderConfig {
  return buildManifestModelProviderConfig({
    providerId: "xkiro",
    catalog: manifest.modelCatalog.providers.xkiro,
  });
}
